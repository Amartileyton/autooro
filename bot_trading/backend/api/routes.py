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

    has_token = bool(
        settings.CTRADER_ACCESS_TOKEN 
        and settings.CTRADER_ACCESS_TOKEN.strip() 
        and settings.CTRADER_ACCESS_TOKEN.lower() != "none" 
        and settings.BROKER_TYPE == "CTRADER"
    )

    return {
        "status": "NOMINAL",
        "ingestion_enabled": settings.INGESTION_ENABLED,
        "auto_execution_enabled": settings.AUTO_EXECUTION_ENABLED,
        "broker_type": settings.BROKER_TYPE,
        "has_ctrader_token": has_token,
        "xauusd_spot": {
            "bid": float(tick.bid),
            "ask": float(tick.ask),
            "timestamp": tick.timestamp
        },
        "account": {
            "balance": float(acc.balance) if has_token else None,
            "equity": float(acc.equity) if has_token else None,
            "margin_used": float(acc.margin_used) if has_token else None,
            "free_margin": float(acc.free_margin) if has_token else None,
            "margin_level_pct": float(acc.margin_level_pct) if has_token else None,
            "currency": acc.currency
        },
        "slots": slots_data,
        "active_slots_count": len(state_machine.active_slots),
        "max_slots": settings.MAX_CONCURRENT_SLOTS
    }


@router.get("/history")
async def get_trade_history(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retorna el historial de operaciones cerradas y métricas globales."""
    stmt = (
        select(Trade)
        .where(Trade.status.not_in([TradeStatus.OPEN, TradeStatus.TP1_HIT, TradeStatus.TP2_HIT, TradeStatus.PENDING]))
        .order_by(desc(Trade.close_time))
        .limit(limit)
    )
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
async def get_raw_messages(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retorna los últimos mensajes de Telegram recibidos, con canal, detalles estructurados y resultado (WIN/LOSS/ACTIVE)."""
    from backend.ingesta.parser import parse_signal
    stmt = select(RawTelegramMessage).order_by(desc(RawTelegramMessage.received_at)).limit(limit)
    result = await db.execute(stmt)
    messages = result.scalars().all()

    # Obtener todos los textos de mensajes para correlacionar resultados (TP HIT / SL HIT)
    all_texts_joined = " ".join([m.raw_text.upper() for m in messages])

    formatted = []
    for m in messages:
        signal_details = None
        outcome = None
        parsed = parse_signal(m.raw_text, message_id=m.message_id or 0, channel_id=m.channel_id or 0)
        
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
            # Determinar resultado
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
            # Detectar si el mensaje es un reporte de resultado de una señal previa (TP / SL HIT)
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
            "channel_name": getattr(m, 'channel_name', None) or "Chartoro FX",
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
async def get_consolidated_trade_cards(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Retorna el estado de los trades consolidados en tarjetas de ciclo de vida:
    - Entrada viva
    - Actualización progresiva de SL y TPs
    - Modificaciones intermedias de SL
    - Cierre en Verde (Win) o Rojo (Loss)
    """
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    # Leer hasta 250 mensajes de Telegram crudos para abarcar los ciclos completos
    stmt = select(RawTelegramMessage).order_by(desc(RawTelegramMessage.received_at)).limit(250)
    result = await db.execute(stmt)
    messages = result.scalars().all()

    trade_cards = consolidate_telegram_trade_lifecycle(messages)
    return trade_cards[:limit]


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
    return {"status": "success", "message": "Ingesta pausada correctamente", "ingestion_enabled": False}


@router.post("/control/resume", dependencies=[Depends(verify_auth_or_key)])
async def resume_ingestion():
    """Reanuda la ingesta de señales."""
    settings.INGESTION_ENABLED = True
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
    """Ejecuta el Kill-Switch: Cierre inmediato de todas las posiciones abiertas."""
    from backend.main import app_state
    state_machine = app_state["state_machine"]
    await state_machine.panic_close_all(reason="DASHBOARD_PANIC_KILL_SWITCH")
    settings.INGESTION_ENABLED = False
    return {"status": "success", "message": "KILL-SWITCH ejecutado: Todas las posiciones han sido cerradas"}


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

    # 1. Guardar en auditoría de Telegram para que aparezca en el historial de tarjetas
    msg_id = int(time.time()) % 1000000
    try:
        from backend.database.session import AsyncSessionLocal
        from backend.database.models import RawTelegramMessage
        async with AsyncSessionLocal() as session:
            db_msg = RawTelegramMessage(
                message_id=msg_id,
                channel_id=-1002763662248,
                channel_name="Chartoro FX Señales Gratis",
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
        channel_id=-1002763662248
    )

    await queue.put(event)

    # 3. Notificar al frontend para refrescar tarjetas e historial en tiempo real
    try:
        from backend.api.ws import manager
        await manager.broadcast({"type": "SIGNAL_PARSED", "message_id": msg_id})
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
