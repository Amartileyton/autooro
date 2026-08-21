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
from backend.ingesta.client import TelegramIngestionClient
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, OrderSide
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
    "telegram_client": None,
    "telegram_bot": None,
    "signal_queue": None
}


async def signal_consumer_worker(
    queue: asyncio.Queue,
    risk_engine: RiskEngine,
    state_machine: TradeStateMachine,
    broker
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

            # 1. Comprobar si es la plantilla formal de una orden rápida ya abierta (Enriquecimiento)
            matching_trade = await state_machine.find_matching_active_trade(event.side, event.entry_price)
            if matching_trade:
                match_slot_id, _ = matching_trade
                logger.info(f"Plantilla formal recibida para posición previa en Slot {match_slot_id}. Enriqueciendo SL y TPs...")
                await state_machine.enrich_active_trade(
                    slot_id=match_slot_id,
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

            # 3. Comprobar Slippage Zero-Tolerance
            is_slippage_ok, market_price, diff = await risk_engine.check_slippage(event.entry_price, event.side)
            if not is_slippage_ok:
                logger.warning(
                    f"Señal RECHAZADA por Slippage: Entrada={event.entry_price}, "
                    f"Mercado={market_price}, Diff={diff:.2f} > Tolerancia={risk_engine.slippage_tolerance}"
                )
                await state_machine.emit_alert("SIGNAL_REJECTED", {
                    "reason": "REJECTED_PRICE_MISMATCH",
                    "diff": float(diff),
                    "market_price": float(market_price)
                })
                queue.task_done()
                continue

            # 3. Calcular Stop Loss (explícito o dinámico)
            sl = event.sl_price
            if event.requires_dynamic_sl or sl is None:
                sl = risk_engine.calculate_dynamic_sl(event.side, event.entry_price)

            # 4. Calcular Lot Sizing exacto (25% del Margen Libre)
            account_info = await broker.get_account_info()
            lot_size = await risk_engine.calculate_lot_size(event.entry_price, account_info)

            # 5. Abrir Trade y activar en State Machine
            trade = await state_machine.open_new_trade(
                slot_id=slot_id,
                side=event.side,
                lot_size=lot_size,
                entry_price=event.entry_price,
                sl=sl,
                tp_levels=event.tp_levels,
                raw_signal_id=event.message_id
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

    # 1. Crear tablas en SQLite WAL
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Base de datos SQLite WAL inicializada correctamente.")

    # 1.1 Si la base de datos está vacía, sembrar historial desde dump.sql
    try:
        import os
        import sqlite3
        async with AsyncSessionLocal() as session:
            check_msg = await session.execute(select(RawTelegramMessage).limit(1))
            if not check_msg.scalars().first():
                dump_candidates = ["dump.sql", "bot_trading/dump.sql", "/app/dump.sql"]
                for dp in dump_candidates:
                    if os.path.exists(dp):
                        logger.info(f"Cargando histórico inicial de mensajes desde {dp}...")
                        sync_conn = sqlite3.connect("trading_bot.db")
                        with open(dp, "r", encoding="utf-8") as f:
                            sync_conn.executescript(f.read())
                        sync_conn.close()
                        logger.info("Histórico inicial cargado exitosamente en SQLite.")
                        break
    except Exception as e:
        logger.warning(f"Aviso al sembrar dump.sql inicial: {e}")

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

    # 4. Inicializar Risk Engine y State Machine
    risk_engine = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)
    app_state["risk_engine"] = risk_engine
    app_state["state_machine"] = state_machine

    # 5. Ejecutar Protocolo de Reconciliación Post-Reinicio
    await run_startup_reconciliation(broker=broker, state_machine=state_machine)

    # 6. Suscribir State Machine y WebSocket al flujo de ticks de alta frecuencia
    async def on_tick_received(tick):
        # A) Procesar hitos en State Machine (< 100ms)
        await state_machine.on_market_tick(tick)
        # B) Retransmitir al Dashboard WebSocket
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
        signal_consumer_worker(signal_queue, risk_engine, state_machine, broker)
    )

    logger.info("Sistema completamente operativo y listo para recibir señales.")

    yield

    # Apagado limpio y seguro
    logger.info("Deteniendo servicios...")
    consumer_task.cancel()
    await telegram_client.stop()
    await telegram_bot.stop()
    await broker.disconnect()
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
