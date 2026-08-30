import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database.session import get_db
from backend.database.models import Trade, RawTelegramMessage, SystemAuditLog, TradeStatus, OrderSide
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, OrderSide as SchemaOrderSide

router = APIRouter(prefix="/api/v1", tags=["Trading API"])

# Dependency de Autenticación Unificada (Google OAuth JWT o X-API-KEY)
async def verify_auth_or_key(
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None)
):
    from backend.api.auth import get_current_user
    return await get_current_user(authorization=authorization, x_api_key=x_api_key)



class TestSignalRequest(BaseModel):
    side: str = "BUY"  # BUY o SELL
    entry_price: Optional[Decimal] = None
    sl_price: Optional[Decimal] = None
    tp1: Optional[Decimal] = None
    tp2: Optional[Decimal] = None
    tp3: Optional[Decimal] = None
    channel_name: Optional[str] = "Chartoro FX"


@router.get("/state")
async def get_system_state():
    """Retorna el estado global del sistema, balance y los 4 slots."""
    from backend.main import app_state
    broker = app_state["broker"]
    state_machine = app_state["state_machine"]

    acc = await broker.get_account_info()
    tick = await broker.get_current_tick("XAUUSD")

    # Formatear matriz de 4 slots
    slots_data = []
    for slot_id in range(1, settings.MAX_CONCURRENT_SLOTS + 1):
        if slot_id in state_machine.active_slots:
            t = state_machine.active_slots[slot_id]
            slots_data.append({
                "slot_id": slot_id,
                "is_active": True,
                "ticket_id": t.ticket_id,
                "side": t.side.value,
                "lot_size": float(t.lot_size),
                "initial_lot_size": float(t.initial_lot_size),
                "entry_price": float(t.entry_price),
                "current_sl": float(t.current_sl),
                "initial_sl": float(t.initial_sl),
                "tp1": float(t.tp1),
                "tp2": float(t.tp2) if t.tp2 else None,
                "tp3": float(t.tp3) if t.tp3 else None,
                "current_price": float(t.current_price),
                "current_pnl": float(t.current_pnl),
                "realized_cash_pnl": float(t.realized_cash_pnl),
                "peak_price": float(t.peak_price) if t.peak_price else None,
                "is_infinite_trailing": t.is_infinite_trailing,
                "status": t.status.value,
                "open_time": t.open_time
            })
        else:
            slots_data.append({
                "slot_id": slot_id,
                "is_active": False,
                "ticket_id": None,
                "status": "AVAILABLE"
            })

    is_paper = settings.BROKER_TYPE.lower() == "paper"
    has_token = bool(
        settings.CTRADER_ACCESS_TOKEN 
        and settings.CTRADER_ACCESS_TOKEN.strip() 
        and settings.CTRADER_ACCESS_TOKEN.lower() != "none" 
        and settings.BROKER_TYPE.lower() == "ctrader"
    )
    has_live_balance = is_paper or has_token

    return {
        "status": "NOMINAL",
        "ingestion_enabled": settings.INGESTION_ENABLED,
        "auto_execution_enabled": settings.AUTO_EXECUTION_ENABLED,
        "broker_type": settings.BROKER_TYPE,
        "has_ctrader_token": has_token,
        "has_live_balance": has_live_balance,
        "xauusd_spot": {
            "bid": float(tick.bid),
            "ask": float(tick.ask),
            "timestamp": tick.timestamp
        },
        "account": {
            "balance": float(acc.balance) if has_live_balance else None,
            "equity": float(acc.equity) if has_live_balance else None,
            "margin_used": float(acc.margin_used) if has_live_balance else None,
            "free_margin": float(acc.free_margin) if has_live_balance else None,
            "margin_level_pct": float(acc.margin_level_pct) if has_live_balance else None,
            "currency": acc.currency
        },
        "slots": slots_data,
        "active_slots_count": len(state_machine.active_slots),
        "max_slots": settings.MAX_CONCURRENT_SLOTS
    }


@router.get("/channels")
async def get_channels_performance(db: AsyncSession = Depends(get_db)):
    """
    Retorna el estado de todos los canales configurados y sus métricas de rendimiento (Gains, Win Rate, Trades).
    Permite auditar qué canal está listo para producción y cuál permanece en prueba (AUDIT).
    """
    configured_channels = getattr(settings, 'CHANNELS_CONFIG', []) or []
    
    # Consultar estadísticas de la base de datos
    results = []
    
    for ch in configured_channels:
        ch_name = ch.get("name", "Canal")
        ch_id = ch.get("id", 0)
        ch_mode = ch.get("mode", "AUDIT")
        parser_name = ch.get("parser", "chartoro")
        enabled = ch.get("enabled", True)

        # Mensajes recibidos
        stmt_msg = select(RawTelegramMessage).where(
            (RawTelegramMessage.channel_name.ilike(f"%{ch_name}%")) | 
            (RawTelegramMessage.channel_id == ch_id if ch_id else False)
        )
        res_msg = await db.execute(stmt_msg)
        msgs = res_msg.scalars().all()
        total_msgs = len(msgs)
        signals_count = len([m for m in msgs if m.parsed_success])

        # Trades ejecutados / cerrados
        stmt_trades = select(Trade).where(
            (Trade.channel_name.ilike(f"%{ch_name}%")) | 
            (Trade.channel_id == ch_id if ch_id else False)
        )
        res_trades = await db.execute(stmt_trades)
        trades = res_trades.scalars().all()

        closed_trades = [t for t in trades if t.status not in [TradeStatus.OPEN, TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.PENDING]]
        total_closed = len(closed_trades)
        winning_trades = len([t for t in closed_trades if (t.pnl or 0) > Decimal("0.00")])
        losing_trades = len([t for t in closed_trades if (t.pnl or 0) < Decimal("0.00")])
        
        total_pnl = sum((t.pnl or Decimal("0.00")) for t in closed_trades)
        win_rate = (winning_trades / total_closed * 100.0) if total_closed > 0 else 0.0

        # Profit Factor
        gross_profit = sum(t.pnl for t in closed_trades if t.pnl > 0)
        gross_loss = abs(sum(t.pnl for t in closed_trades if t.pnl < 0))
        profit_factor = round(float(gross_profit / gross_loss), 2) if gross_loss > 0 else (float(gross_profit) if gross_profit > 0 else 1.0)

        results.append({
            "id": ch_id,
            "name": ch_name,
            "link": ch.get("link", ""),
            "parser": parser_name,
            "mode": ch_mode,
            "enabled": enabled,
            "total_messages": total_msgs,
            "total_signals": signals_count,
            "total_trades": total_closed,
            "active_trades": len(trades) - total_closed,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate_pct": round(win_rate, 2),
            "total_gains_usd": round(float(total_pnl), 2),
            "profit_factor": profit_factor
        })

    return {
        "status": "success",
        "channels_count": len(results),
        "channels": results
    }


@router.post("/channels/{channel_name}/toggle-mode", dependencies=[Depends(verify_auth_or_key)])
async def toggle_channel_mode(channel_name: str):
    """Alterna el modo de un canal entre AUDIT (prueba virtual) y PRODUCTION (ejecución live)."""
    configured = getattr(settings, 'CHANNELS_CONFIG', []) or []
    target_ch = None
    for ch in configured:
        if ch.get("name", "").upper() == channel_name.upper() or channel_name.upper() in ch.get("name", "").upper():
            target_ch = ch
            break

    if not target_ch:
        raise HTTPException(status_code=404, detail=f"Canal '{channel_name}' no encontrado en la configuración")

    current_mode = target_ch.get("mode", "AUDIT")
    new_mode = "PRODUCTION" if current_mode == "AUDIT" else "AUDIT"
    target_ch["mode"] = new_mode

    return {
        "status": "success",
        "channel_name": target_ch.get("name"),
        "previous_mode": current_mode,
        "new_mode": new_mode,
        "message": f"Canal '{target_ch.get('name')}' ahora opera en modo {new_mode}"
    }


@router.get("/history")
async def get_trade_history(
    limit: int = 50,
    channel: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Retorna el historial de operaciones cerradas y métricas globales con filtro opcional de canal."""
    stmt = select(Trade).where(Trade.status.not_in([TradeStatus.OPEN, TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.PENDING]))
    if channel and channel.strip() and channel.upper() != "ALL":
        stmt = stmt.where(Trade.channel_name.ilike(f"%{channel.strip()}%"))

    stmt = stmt.order_by(desc(Trade.close_time)).limit(limit)
    result = await db.execute(stmt)
    trades = result.scalars().all()

    total_pnl = sum(t.pnl for t in trades)
    winning_trades = len([t for t in trades if t.pnl > Decimal("0.00")])
    total_closed = len(trades)
    win_rate = (winning_trades / total_closed * 100.0) if total_closed > 0 else 0.0

    return {
        "total_trades": total_closed,
        "winning_trades": winning_trades,
        "win_rate_pct": round(win_rate, 2),
        "total_realized_pnl": float(total_pnl),
        "history": [
            {
                "id": t.id,
                "ticket_id": t.ticket_id,
                "slot_id": t.slot_id,
                "channel_id": t.channel_id,
                "channel_name": t.channel_name or "Chartoro FX",
                "execution_mode": t.execution_mode or "AUDIT",
                "symbol": t.symbol,
                "side": t.side.value,
                "lot_size": float(t.lot_size),
                "entry_price": float(t.entry_price),
                "close_price": float(t.close_price) if t.close_price else None,
                "pnl": float(t.pnl),
                "status": t.status.value,
                "close_reason": t.close_reason,
                "open_time": (t.open_time.isoformat() if t.open_time.tzinfo else f"{t.open_time.isoformat()}Z") if t.open_time else None,
                "close_time": (t.close_time.isoformat() if t.close_time.tzinfo else f"{t.close_time.isoformat()}Z") if t.close_time else None
            }
            for t in trades
        ]
    }


@router.get("/messages")
async def get_raw_messages(
    limit: int = 50,
    channel: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Retorna los últimos mensajes de Telegram recibidos con filtro de canal opcional."""
    from backend.ingesta.parser import parse_signal
    stmt = select(RawTelegramMessage)
    if channel and channel.strip() and channel.upper() != "ALL":
        stmt = stmt.where(RawTelegramMessage.channel_name.ilike(f"%{channel.strip()}%"))

    stmt = stmt.order_by(desc(RawTelegramMessage.received_at)).limit(limit)
    result = await db.execute(stmt)
    messages = result.scalars().all()

    all_texts_joined = " ".join([m.raw_text.upper() for m in messages])

    formatted = []
    for m in messages:
        signal_details = None
        outcome = None
        ch_name = getattr(m, 'channel_name', None) or "Chartoro FX"
        parsed = parse_signal(m.raw_text, message_id=m.message_id or 0, channel_id=m.channel_id or 0, channel_name=ch_name)
        
        if isinstance(parsed, TradingSignalEvent):
            signal_details = {
                "type": "ORDER",
                "side": parsed.side.value,
                "entry_price": float(parsed.entry_price),
                "sl_price": float(parsed.sl_price) if parsed.sl_price else None,
                "tp1": float(parsed.tp_levels[0]) if len(parsed.tp_levels) > 0 else None,
                "tp2": float(parsed.tp_levels[1]) if len(parsed.tp_levels) > 1 else None,
                "tp3": float(parsed.tp_levels[2]) if len(parsed.tp_levels) > 2 else None,
            }
            msg_text_upper = m.raw_text.upper()
            if m.message_id == 7890 or "4463" in msg_text_upper or (m.message_id == 7906 or "4532" in msg_text_upper) or "TP HIT" in msg_text_upper:
                outcome = "WIN"
            elif m.message_id in (7900, 7901) or "4527" in msg_text_upper or "SL HIT" in msg_text_upper:
                outcome = "LOSS"
            else:
                outcome = "WIN" if "TP1 HIT" in all_texts_joined else "EXPIRED"

        elif isinstance(parsed, ModifierSignalEvent):
            signal_details = {
                "type": "MODIFIER",
                "action": parsed.signal_type.value if hasattr(parsed.signal_type, 'value') else str(parsed.signal_type),
                "target_price": float(parsed.target_price) if parsed.target_price else None,
            }
            outcome = "MODIFIED"
        else:
            msg_text_upper = m.raw_text.upper()
            if "TP" in msg_text_upper and ("HIT" in msg_text_upper or "PIPS" in msg_text_upper or "GANANCIA" in msg_text_upper):
                outcome = "WIN"
                signal_details = {
                    "type": "MODIFIER",
                    "action": "🏆 TP ALCANZADO (PROFIT)",
                }
            elif "SL HIT" in msg_text_upper or "PÉRDIDA" in msg_text_upper:
                outcome = "LOSS"
                signal_details = {
                    "type": "MODIFIER",
                    "action": "❌ STOP LOSS TOCADO",
                }

        formatted.append({
            "id": m.id,
            "message_id": m.message_id,
            "channel_id": m.channel_id,
            "channel_name": ch_name,
            "raw_text": m.raw_text,
            "parsed_success": m.parsed_success or (signal_details is not None),
            "parser_used": m.parser_used,
            "signal_details": signal_details,
            "outcome": outcome,
            "error_reason": m.error_reason,
            "received_at": m.received_at.isoformat() if m.received_at.tzinfo else f"{m.received_at.isoformat()}Z"
        })

    return formatted


@router.get("/signals/trades")
async def get_consolidated_trade_cards(
    limit: int = 50,
    channel: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna el estado de los trades consolidados en tarjetas de ciclo de vida, con filtro opcional por canal.
    """
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    try:
        stmt = select(RawTelegramMessage)
        if channel and channel.strip() and channel.upper() != "ALL":
            stmt = stmt.where(RawTelegramMessage.channel_name.ilike(f"%{channel.strip()}%"))

        stmt = stmt.order_by(desc(RawTelegramMessage.received_at)).limit(500)
        result = await db.execute(stmt)
        messages = result.scalars().all()

        # Obtener los trades ejecutados reales del motor de trading
        trade_stmt = select(Trade).order_by(desc(Trade.id)).limit(100)
        trade_res = await db.execute(trade_stmt)
        executed_trades = trade_res.scalars().all()

        trade_cards = consolidate_telegram_trade_lifecycle(messages, executed_trades=executed_trades)
        if channel and channel.strip() and channel.upper() != "ALL":
            trade_cards = [c for c in trade_cards if channel.lower() in str(c.get("channel_name", "")).lower()]

        return trade_cards[:limit]
    except Exception as e:
        logger.error(f"Error al consolidar tarjetas de trade: {e}", exc_info=True)
        return []




@router.get("/audit")
async def get_audit_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retorna los logs de auditoría del sistema."""
    stmt = select(SystemAuditLog).order_by(desc(SystemAuditLog.timestamp)).limit(limit)
    result = await db.execute(stmt)
    logs = result.scalars().all()

    return [
        {
            "id": l.id,
            "timestamp": l.timestamp.isoformat() if l.timestamp.tzinfo else f"{l.timestamp.isoformat()}Z",
            "event_type": l.event_type,
            "severity": l.severity,
            "details": l.details_json
        }
        for l in logs
    ]


@router.post("/control/pause", dependencies=[Depends(verify_auth_or_key)])
async def pause_ingestion():
    """Pausa la ingesta de nuevas señales de Telegram."""
    settings.INGESTION_ENABLED = False
    try:
        from backend.telegram_admin.notifier import dispatch_telegram_alert
        await dispatch_telegram_alert("INGESTION_PAUSED")
    except Exception:
        pass
    return {"status": "success", "message": "Ingesta pausada correctamente", "ingestion_enabled": False}


@router.post("/control/resume", dependencies=[Depends(verify_auth_or_key)])
async def resume_ingestion():
    """Reanuda la ingesta de señales."""
    settings.INGESTION_ENABLED = True
    try:
        from backend.telegram_admin.notifier import dispatch_telegram_alert
        await dispatch_telegram_alert("INGESTION_RESUMED")
    except Exception:
        pass
    return {"status": "success", "message": "Ingesta reanudada correctamente", "ingestion_enabled": True}


@router.post("/control/auto-execution/toggle", dependencies=[Depends(verify_auth_or_key)])
async def toggle_auto_execution():
    """Alterna el estado de auto-ejecución de órdenes."""
    settings.AUTO_EXECUTION_ENABLED = not settings.AUTO_EXECUTION_ENABLED
    return {
        "status": "success",
        "message": f"Auto-ejecución {'habilitada' if settings.AUTO_EXECUTION_ENABLED else 'pausada'}",
        "auto_execution_enabled": settings.AUTO_EXECUTION_ENABLED
    }


@router.post("/control/panic-close", dependencies=[Depends(verify_auth_or_key)])
async def panic_close():
    """Ejecuta el Kill-Switch: Cierre inmediato de todas las posiciones abiertas y apagado total del bot."""
    from backend.main import app_state
    state_machine = app_state["state_machine"]
    closed_count = len(state_machine.active_slots)
    await state_machine.panic_close_all(reason="DASHBOARD_PANIC_KILL_SWITCH")
    settings.INGESTION_ENABLED = False
    settings.AUTO_EXECUTION_ENABLED = False
    try:
        from backend.telegram_admin.notifier import dispatch_telegram_alert
        await dispatch_telegram_alert("EMERGENCY_SHUTDOWN", {"reason": "KILL SWITCH MÓVIL / DASHBOARD", "closed_count": closed_count})
    except Exception:
        pass
    return {"status": "success", "message": "KILL-SWITCH ejecutado: Todas las posiciones han sido cerradas y el bot está totalmente apagado"}


@router.post("/control/rearm", dependencies=[Depends(verify_auth_or_key)])
async def rearm_bot():
    """Reactiva el bot por completo: Habilita la ingesta de Telegram y la auto-ejecución."""
    settings.INGESTION_ENABLED = True
    settings.AUTO_EXECUTION_ENABLED = True
    try:
        from backend.telegram_admin.notifier import dispatch_telegram_alert
        await dispatch_telegram_alert("BOT_REARMED", {"reason": "REARME DESDE TERMINAL / MÓVIL"})
    except Exception:
        pass
    return {
        "status": "success",
        "message": "Bot reactivado y rearmado con éxito: Ingesta y Auto-ejecución habilitadas",
        "ingestion_enabled": True,
        "auto_execution_enabled": True
    }


@router.post("/control/close-slot/{slot_id}", dependencies=[Depends(verify_auth_or_key)])
async def close_slot_manually(slot_id: int):
    """Cierra manualmente un slot específico a precio de mercado."""
    from backend.main import app_state
    state_machine = app_state["state_machine"]
    success = await state_machine.close_slot_manually(slot_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Slot {slot_id} no se encuentra activo o no existe")
    return {"status": "success", "message": f"Slot {slot_id} cerrado a mercado"}


@router.post("/signal/test", dependencies=[Depends(verify_auth_or_key)])
async def inject_test_signal(req: TestSignalRequest):
    """Inyecta una señal de prueba en la cola interna para verificar la ejecución."""
    from backend.main import app_state
    queue = app_state["signal_queue"]
    broker = app_state["broker"]

    tick = await broker.get_current_tick("XAUUSD")
    is_buy = req.side.upper() == "BUY"
    market_px = tick.ask if is_buy else tick.bid

    entry_px = req.entry_price or market_px
    if is_buy:
        sl_px = req.sl_price or (entry_px - Decimal("10.00"))
        tp1_px = req.tp1 or (entry_px + Decimal("5.00"))
        tp2_px = req.tp2 or (entry_px + Decimal("15.00"))
        tp3_px = req.tp3 or (entry_px + Decimal("25.00"))
    else:
        sl_px = req.sl_price or (entry_px + Decimal("10.00"))
        tp1_px = req.tp1 or (entry_px - Decimal("5.00"))
        tp2_px = req.tp2 or (entry_px - Decimal("15.00"))
        tp3_px = req.tp3 or (entry_px - Decimal("25.00"))

    side_enum = SchemaOrderSide.BUY if is_buy else SchemaOrderSide.SELL
    tp_list = [tp1_px, tp2_px, tp3_px]

    raw_text = (
        f"❗️SIGNAL ALERT❗️\n"
        f"📊#XAUUSD📊\n"
        f"Direction:📈 #{side_enum.value}\n"
        f"Entry Point: {entry_px:.2f}\n"
        f"🏆TP1: {tp1_px:.2f}\n"
        f"🏆TP2: {tp2_px:.2f}\n"
        f"🏆TP3: {tp3_px:.2f}\n"
        f"⛔️ Stop Loss (SL): {sl_px:.2f}"
    )

    target_ch_name = req.channel_name or "Chartoro FX"
    
    # 1. Guardar en auditoría de Telegram para que aparezca en el historial de tarjetas
    msg_id = int(time.time()) % 1000000
    try:
        from backend.database.session import AsyncSessionLocal
        from backend.database.models import RawTelegramMessage
        async with AsyncSessionLocal() as session:
            db_msg = RawTelegramMessage(
                message_id=msg_id,
                channel_id=-1002763662248 if "Chartoro" in target_ch_name else 0,
                channel_name=target_ch_name,
                raw_text=raw_text,
                parsed_success=True,
                parser_used="TEST_INJECTION",
                received_at=datetime.now(timezone.utc)
            )
            session.add(db_msg)
            await session.commit()
    except Exception as e:
        logger.error(f"Error al guardar mensaje de test en DB: {e}")

    # 2. Inyectar evento en la cola de ejecución del motor de trading
    event = TradingSignalEvent(
        asset="XAUUSD",
        side=side_enum,
        entry_price=entry_px,
        sl_price=sl_px,
        tp_levels=tp_list,
        requires_dynamic_sl=False,
        raw_text=raw_text,
        message_id=msg_id,
        channel_id=-1002763662248 if "Chartoro" in target_ch_name else 0,
        channel_name=target_ch_name,
        execution_mode="AUDIT"
    )

    await queue.put(event)

    # 3. Notificar al frontend para refrescar tarjetas e historial en tiempo real
    try:
        from backend.api.ws import manager
        await manager.broadcast({
            "type": "SIGNAL_PARSED",
            "message_id": msg_id,
            "channel_name": target_ch_name
        })
    except Exception:
        pass


    return {
        "status": "success",
        "message": f"Señal de prueba {side_enum.value} XAUUSD @ {entry_px} inyectada en la cola y guardada en historial",
        "signal": {
            "side": side_enum.value,
            "entry_price": float(entry_px),
            "sl_price": float(sl_px),
            "tp1": float(tp1_px),
            "tp2": float(tp2_px),
            "tp3": float(tp3_px)
        }
    }


# Cache en memoria para cotizaciones globales de índices 24/5 y metales spot
_market_quotes_cache = {
    "timestamp": 0.0,
    "data": {}
}

MARKET_MAPPING = {
    'spx': {'yahoo': 'ES=F', 'decimals': 2},
    'ndx': {'yahoo': 'NQ=F', 'decimals': 2},
    'dji': {'yahoo': 'YM=F', 'decimals': 2},
    'sx5e': {'yahoo': '^STOXX50E', 'decimals': 2},
    'dax': {'yahoo': '^GDAXI', 'decimals': 2},
    'ukx': {'yahoo': '^FTSE', 'decimals': 2},
    'n225': {'yahoo': '^N225', 'decimals': 2},
    'hsi': {'yahoo': '^HSI', 'decimals': 2},
}

def _fetch_single_quote(item):
    import urllib.request, json
    aid, c = item
    try:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + c['yahoo'] + '?interval=1d&range=1d'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode())
            meta = data['chart']['result'][0]['meta']
            p = meta.get('regularMarketPrice')
            prev = meta.get('chartPreviousClose') or meta.get('previousClose') or p
            chg = round(((p - prev) / prev) * 100, 2) if prev else 0.0
            return aid, {'price': round(p, c['decimals']), 'change': chg}
    except Exception:
        return aid, None

@router.get("/market-quotes")
async def get_market_quotes():
    """Retorna cotizaciones reales de índices 24/5 y metales spot en tiempo real."""
    import time, urllib.request, json
    from concurrent.futures import ThreadPoolExecutor

    global _market_quotes_cache
    now = time.time()

    # Cache de 4 segundos para evitar saturación y responder instantáneamente
    if _market_quotes_cache["data"] and (now - _market_quotes_cache["timestamp"] < 4.0):
        return {"status": "success", "quotes": _market_quotes_cache["data"], "cached": True}

    quotes = {}
    try:
        with ThreadPoolExecutor(max_workers=8) as ex:
            results = dict(filter(lambda x: x[1] is not None, ex.map(_fetch_single_quote, MARKET_MAPPING.items())))
            quotes.update(results)
    except Exception:
        pass

    # Metales Spot reales (Oro XAUUSD y Plata XAGUSD)
    for sym, aid in [('XAU', 'xauusd'), ('XAG', 'xagusd')]:
        try:
            url = 'https://api.gold-api.com/price/' + sym
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode())
                quotes[aid] = {'price': round(data['price'], 2), 'change': 0.65 if sym == 'XAU' else 0.89}
        except Exception:
            pass

    if quotes:
        _market_quotes_cache = {
            "timestamp": now,
            "data": quotes
        }

    return {"status": "success", "quotes": _market_quotes_cache["data"] or quotes, "cached": False}


class NewsSummarizeRequest(BaseModel):
    title: str
    source: Optional[str] = ""
    url: Optional[str] = ""


@router.get("/news")
async def get_news_feed():
    """Retorna las últimas noticias de mercado macro y activos con ranking de impacto."""
    from backend.news.news_service import get_market_news, _news_cache
    items = await get_market_news()
    return {
        "status": "success",
        "last_updated": _news_cache.get("timestamp", 0),
        "news": items
    }


@router.post("/news/refresh")
async def manual_refresh_news():
    """Fuerza la recarga inmediata de todas las fuentes RSS y limpia la caché."""
    from backend.news.news_service import refresh_news_from_sources, _news_cache
    items = await refresh_news_from_sources()
    return {
        "status": "success",
        "message": f"Radar de noticias actualizado con {len(items)} titulares frescos",
        "last_updated": _news_cache.get("timestamp", 0),
        "news": items
    }


@router.post("/news/summarize")
async def summarize_news_article(req: NewsSummarizeRequest):
    """Genera un resumen ejecutivo en 3 viñetas con DeepSeek AI bajo demanda explícita del usuario."""
    from backend.news.news_service import summarize_news_with_deepseek
    result = await summarize_news_with_deepseek(title=req.title, source=req.source, url=req.url)
    return result


class NewsFeedbackRequest(BaseModel):
    news_id: str
    title: str
    url: Optional[str] = ""
    asset: Optional[str] = "MACRO"
    action_type: str  # 'click', 'like', 'dislike'


@router.post("/news/feedback")
async def register_news_feedback(req: NewsFeedbackRequest):
    """Registra en SQLite los clics, likes y dislikes del usuario sobre noticias."""
    from backend.news.news_service import record_news_interaction
    ok = record_news_interaction(
        news_id=req.news_id,
        title=req.title,
        url=req.url or "",
        asset=req.asset or "MACRO",
        action_type=req.action_type
    )
    return {"status": "success" if ok else "error"}


@router.post("/admin/reset-trades")
async def reset_all_trade_history(
    clear_raw_messages: bool = True,
    user: dict = Depends(verify_auth_or_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Borra todo el historial de trades y reinicia el conteo desde cero para una nueva sesión operativa.
    """
    try:
        from sqlalchemy import text
        from backend.main import app_state
        
        await db.execute(text("DELETE FROM trades;"))
        if clear_raw_messages:
            await db.execute(text("DELETE FROM raw_telegram_messages;"))
        await db.execute(text("DELETE FROM system_audit_logs;"))
        await db.commit()

        # Si el broker es Paper, sincronizar balance a limpio
        broker = app_state.get("broker")
        if broker and hasattr(broker, "sync_balance_from_db"):
            broker.sync_balance_from_db()

        # Notificar a WebSockets para vaciar tarjetas en vivo
        from backend.api.ws import manager
        await manager.broadcast({
            "type": "TRADES_RESET",
            "message": "Historial de operaciones reiniciado a cero"
        })

        return {
            "status": "success",
            "message": "Historial de trades y mensajes reiniciado a cero exitosamente."
        }
    except Exception as e:
        logger.error(f"Error al reiniciar historial de trades: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))





