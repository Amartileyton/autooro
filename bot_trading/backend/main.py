import asyncio
import logging
from contextlib import asynccontextmanager
from decimal import Decimal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database.session import engine, AsyncSessionLocal
from backend.database.models import Base, Trade, TradeStatus, RawTelegramMessage, SystemAuditLog
from backend.database.reconciliation import run_startup_reconciliation
from backend.broker.paper import LocalPaperBroker
from backend.broker.live_adapter import LiveBrokerAdapter
from backend.risk.engine import RiskEngine
from backend.risk.state_machine import TradeStateMachine
from backend.risk.pullback_watcher import PullbackWatcher
from backend.ingesta.client import TelegramIngestionClient
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, OrderSide
from backend.repository.messages import update_message_error_reason
from backend.services.event_bus import publish_trade_event
from backend.services.event_bus import publish_trade_event
from backend.telegram_admin.bot import TelegramAdminBot
from backend.api.routes import router as api_router
from backend.api.ws import router as ws_router, broadcast_tick_update

# Configuración del Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
)
logger = logging.getLogger("trading_bot.main")

# Estado global compartido
app_state = {
    "broker": None,
    "risk_engine": None,
    "state_machine": None,
    "pullback_watcher": None,
    "telegram_client": None,
    "telegram_bot": None,
    "signal_queue": None
}


async def signal_consumer_worker(
    queue: asyncio.Queue,
    risk_engine: RiskEngine,
    state_machine: TradeStateMachine,
    broker,
    pullback_watcher: PullbackWatcher = None
):
    """
    Consumidor desacoplado de la cola de señales:
    Evalúa slots de capital, calcula lot sizing exacto (25%), verifica slippage y ejecuta.
    """
    logger.info("Signal Consumer Worker iniciado y esperando señales...")
    while True:
        try:
            event = await queue.get()
            logger.info(f"Worker: Procesando evento desde cola -> {type(event).__name__}")

            if isinstance(event, ModifierSignalEvent):
                await state_machine.handle_modifier_signal(event)
                queue.task_done()
                continue

            if not isinstance(event, TradingSignalEvent):
                queue.task_done()
                continue

            if not settings.AUTO_EXECUTION_ENABLED:
                logger.info("Auto-ejecución deshabilitada. Señal descartada.")
                queue.task_done()
                continue

            # 1. Comprobar si es la plantilla formal de una orden previa (Enriquecimiento o Anti-Reapertura)
            matching = await state_machine.find_matching_active_trade(
                event.side,
                event.entry_price,
                channel_name=getattr(event, 'channel_name', None)
            )
            if matching:
                match_slot_id, match_trade, is_recently_closed = matching
                if not is_recently_closed and match_slot_id is not None:
                    logger.info(f"Plantilla formal recibida para posición activa en Slot {match_slot_id}. Enriqueciendo SL y TPs...")
                    await state_machine.enrich_active_trade(
                        slot_id=match_slot_id,
                        sl=event.sl_price,
                        tp_levels=event.tp_levels,
                        raw_signal_id=event.message_id
                    )
                else:
                    ticket_closed = match_trade.get("ticket_id") if isinstance(match_trade, dict) else getattr(match_trade, "ticket_id", "")
                    logger.info(
                        f"🛡️ [ANTI-REAPERTURA] Plantilla formal recibida para setup ya cerrado recientemente ({ticket_closed}). "
                        f"Enriqueciendo registro histórico en BD sin abrir nueva orden en broker."
                    )
                    await state_machine.enrich_closed_trade(
                        ticket_id=ticket_closed,
                        sl=event.sl_price,
                        tp_levels=event.tp_levels,
                        raw_signal_id=event.message_id
                    )
                queue.task_done()
                continue

            # 2. Evaluar Disponibilidad de Slots (Máximo 4)
            can_execute, slot_id, reason = risk_engine.evaluate_signal_for_slot(
                event, state_machine.active_slots
            )
            if not can_execute:
                logger.warning(f"Señal RECHAZADA por Motor de Riesgo: {reason} (4 Slots ocupados)")
                await state_machine.emit_alert("SLOTS_EXHAUSTED", {
                    "signal": event.model_dump(),
                    "active_slots": len(state_machine.active_slots)
                })
                queue.task_done()
                continue

            # 3. Comprobar Slippage Zero-Tolerance o Rango Seguro de Entrada
            entry_min = getattr(event, 'entry_min', None)
            entry_max = getattr(event, 'entry_max', None)
            is_slippage_ok, market_price, diff = await risk_engine.check_slippage(
                event.entry_price, event.side, entry_min=entry_min, entry_max=entry_max
            )

            # En modo Paper (simulación), si el precio simulado está descalibrado del precio real de la señal (>50 USD),
            # calibrar automáticamente el simulador al precio real del activo para simulación de alta fidelidad.
            if settings.BROKER_TYPE.lower() == "paper" and hasattr(broker, 'set_market_price') and diff > Decimal("50.0"):
                logger.info(f"🔄 [PAPER SIMULATION] Calibrando precio de mercado simulado a {event.entry_price} (Desvío previo: {diff:.2f} USD)")
                broker.set_market_price(event.entry_price)
                is_slippage_ok, market_price, diff = await risk_engine.check_slippage(
                    event.entry_price, event.side, entry_min=entry_min, entry_max=entry_max
                )

            if not is_slippage_ok:
                logger.warning(
                    f"Señal fuera de precio inicial: Entrada={event.entry_price} (Rango: {entry_min}-{entry_max}), "
                    f"Mercado={market_price}, Diff={diff:.2f} > Tolerancia={risk_engine.slippage_tolerance}"
                )
                
                # Si el Pullback Watcher está habilitado, poner la señal en vigilancia de retroceso
                if getattr(settings, 'PULLBACK_WATCHER_ENABLED', True) and pullback_watcher:
                    added = await pullback_watcher.add_signal(event, entry_min=entry_min, entry_max=entry_max)
                    if added:
                        if event.message_id:
                            try:
                                await update_message_error_reason(
                                    event.message_id,
                                    f"EN ESPERA PULLBACK (Mercado: ${float(market_price):.2f} | Desvío: +${float(diff):.2f})"
                                )
                            except Exception as db_err:
                                logger.debug(f"Aviso al actualizar error_reason en DB: {db_err}")

                        await state_machine.emit_alert("SIGNAL_PENDING_PULLBACK", {
                            "diff": float(diff),
                            "market_price": float(market_price),
                            "message_id": event.message_id,
                            "entry_price": float(event.entry_price),
                            "timeout_minutes": getattr(settings, 'PULLBACK_TIMEOUT_MINUTES', 15)
                        })
                        queue.task_done()
                        continue

                # Si no se pudo poner en vigilancia (ej. TP1 ya alcanzado), descartar
                if event.message_id:
                    try:
                        await update_message_error_reason(
                            event.message_id,
                            f"FUERA PRECIO (Mercado: ${float(market_price):.2f} | Desvío: +${float(diff):.2f})"
                        )
                    except Exception as db_err:
                        logger.debug(f"Aviso al actualizar error_reason en DB: {db_err}")

                await state_machine.emit_alert("SIGNAL_REJECTED", {
                    "reason": f"FUERA PRECIO (Mercado: ${float(market_price):.2f} | Desvío: +${float(diff):.2f})",
                    "diff": float(diff),
                    "market_price": float(market_price),
                    "message_id": event.message_id,
                    "entry_price": float(event.entry_price)
                })
                queue.task_done()
                continue

            # Precio de cotización actual de mercado al momento del envío de la orden
            actual_entry = market_price

            # 4. Calcular Stop Loss (explícito sanitizado con Circuit Breaker máx $15 USD o dinámico)
            sl = risk_engine.sanitize_sl(event.side, actual_entry, event.sl_price)

            # 5. Calcular Lot Sizing exacto (25% del Margen Libre)
            account_info = await broker.get_account_info()
            lot_size = await risk_engine.calculate_lot_size(actual_entry, account_info)

            # 6. Abrir Trade y activar en State Machine
            trade = await state_machine.open_new_trade(
                slot_id=slot_id,
                side=event.side,
                lot_size=lot_size,
                entry_price=actual_entry,
                sl=sl,
                tp_levels=event.tp_levels,
                raw_signal_id=event.message_id,
                channel_id=event.channel_id,
                channel_name=getattr(event, 'channel_name', 'Chartoro FX'),
                execution_mode=getattr(event, 'execution_mode', 'AUDIT')
            )

            # 6. Notificar inmediatamente a clientes WebSocket
            if trade:
                try:
                    from backend.api.ws import manager, broadcast_tick_update
                    tick = await broker.get_current_tick("XAUUSD")
                    acc = await broker.get_account_info()
                    await broadcast_tick_update(tick, acc, state_machine.active_slots)
                    await manager.broadcast({
                        "type": "TRADE_EVENT",
                        "event": "ORDER_OPENED",
                        "slot_id": slot_id,
                        "ticket_id": trade.ticket_id
                    })
                except Exception as ws_err:
                    logger.warning(f"Aviso al emitir WebSocket de orden abierta: {ws_err}")

            queue.task_done()

        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error crítico en Signal Consumer Worker: {e}", exc_info=True)
            await asyncio.sleep(1.0)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle Manager de FastAPI: arranque y apagado seguro."""
    logger.info("==================================================")
    logger.info(" INICIANDO MOTOR DE TRADING AUTÓNOMO XAUUSD")
    logger.info("==================================================")

    # 1. Crear tablas en SQLite WAL con sync_engine seguro
    from backend.database.session import sync_engine
    Base.metadata.create_all(bind=sync_engine)
    logger.info("Base de datos SQLite WAL inicializada limpiamente.")

    # 2. Inicializar Cola Asíncrona desacoplada
    signal_queue = asyncio.Queue()
    app_state["signal_queue"] = signal_queue

    # 3. Inicializar Broker Adapter (Paper o Live)
    if settings.BROKER_TYPE.lower() == "ctrader":
        broker = LiveBrokerAdapter()
    else:
        broker = LocalPaperBroker()

    app_state["broker"] = broker
    await broker.connect()

    # 3.1 Lanzar reconexión automática si el broker es cTrader (Live)
    reconnect_task = None
    if settings.BROKER_TYPE.lower() == "ctrader":
        from backend.broker.live_adapter import LiveBrokerAdapter as _LiveAdapterClass
        if isinstance(broker, _LiveAdapterClass):
            reconnect_task = asyncio.create_task(broker._reconnect_loop())
            app_state["reconnect_task"] = reconnect_task
            logger.info("[MAIN] Tarea de reconexión automática cTrader iniciada.")

    # 4. Inicializar Risk Engine, State Machine y Pullback Watcher
    risk_engine = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)
    pullback_watcher = PullbackWatcher(risk_engine=risk_engine, state_machine=state_machine, broker=broker)
    app_state["risk_engine"] = risk_engine
    app_state["state_machine"] = state_machine
    app_state["pullback_watcher"] = pullback_watcher

    # 4.1 Registrar callbacks de alertas para WebSocket y Notificador
    async def on_state_machine_alert(event_type: str, data: dict):
        await publish_trade_event(event_type, data)

    state_machine.register_alert_callback(on_state_machine_alert)

    # 5. Ejecutar Protocolo de Reconciliación Post-Reinicio
    await run_startup_reconciliation(broker=broker, state_machine=state_machine)

    # 6. Suscribir State Machine, Pullback Watcher y WebSocket al flujo de ticks de alta frecuencia
    async def on_tick_received(tick):
        # A) Evaluar Pullback Watcher en señales en espera (< 10ms)
        if getattr(settings, 'PULLBACK_WATCHER_ENABLED', True) and pullback_watcher:
            await pullback_watcher.on_market_tick(tick)
        # B) Procesar hitos en State Machine (< 100ms)
        await state_machine.on_market_tick(tick)
        # C) Retransmitir al Dashboard WebSocket
        acc = await broker.get_account_info()
        await broadcast_tick_update(tick, acc, state_machine.active_slots)

    await broker.subscribe_ticks("XAUUSD", on_tick_received)

    # 7. Iniciar Bot Administrativo en Telegram (Aiogram)
    try:
        telegram_bot = TelegramAdminBot(state_machine=state_machine, broker=broker)
        app_state["telegram_bot"] = telegram_bot
        await telegram_bot.start()
    except Exception as e:
        logger.warning(f"Aviso al iniciar Bot Admin de Telegram: {e}")

    # 8. Iniciar Cliente MTProto Telethon
    try:
        telegram_client = TelegramIngestionClient(signal_queue=signal_queue)
        app_state["telegram_client"] = telegram_client
        await telegram_client.start()
    except Exception as e:
        logger.warning(f"Aviso al iniciar Telethon MTProto: {e}")

    # 9. Iniciar Worker Consumidor de Señales
    consumer_task = asyncio.create_task(
        signal_consumer_worker(signal_queue, risk_engine, state_machine, broker, pullback_watcher)
    )

    # 10. Iniciar Worker de Actualización Horaria de Noticias (cada 3600s)
    async def news_hourly_refresh_worker():
        from backend.news.news_service import refresh_news_from_sources
        while True:
            try:
                await asyncio.sleep(3600)
                logger.info("[NEWS WORKER] Ejecutando actualización horaria de noticias macro...")
                await refresh_news_from_sources()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[NEWS WORKER] Error en actualización de noticias: {e}")
                await asyncio.sleep(60)

    news_task = asyncio.create_task(news_hourly_refresh_worker())

    logger.info("Sistema completamente operativo y listo para recibir señales.")

    yield

    # Apagado limpio y seguro
    logger.info("Deteniendo servicios...")
    consumer_task.cancel()
    news_task.cancel()

    # Detener reconexión automática antes de desconectar el broker
    reconnect_task = app_state.get("reconnect_task")
    if reconnect_task and not reconnect_task.done():
        from backend.broker.live_adapter import LiveBrokerAdapter as _LiveAdapterClass
        if isinstance(broker, _LiveAdapterClass):
            broker._reconnect_enabled = False
        reconnect_task.cancel()

    await telegram_client.stop()
    await telegram_bot.stop()
    await broker.disconnect()

    
    # Consolidar SQLite WAL al disco antes de cerrar
    try:
        from backend.database.session import sync_engine
        with sync_engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA wal_checkpoint(FULL);")
            logger.info("SQLite WAL Checkpoint consolidado exitosamente en disco.")
    except Exception as cp_err:
        logger.warning(f"Aviso en SQLite checkpoint al apagar: {cp_err}")

    await engine.dispose()
    logger.info("Motor de Trading apagado correctamente.")


# Aplicación FastAPI
app = FastAPI(
    title="XAUUSD Trading Engine API",
    description="Motor de Trading Autónomo para Oro (XAUUSD): Telegram MTProto -> 4 Slots Risk Engine -> Broker",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Rutas
from backend.api.auth import router as auth_router
app.include_router(auth_router)
app.include_router(api_router)
app.include_router(ws_router)


@app.get("/health")
async def health_check():
    """Endpoint de salud del servicio."""
    return {"status": "ok", "service": "xauusd_trading_engine"}
