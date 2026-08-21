from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Header, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database.session import get_db
from backend.database.models import Trade, RawTelegramMessage, SystemAuditLog, TradeStatus, OrderSide
from backend.ingesta.schemas import TradingSignalEvent, OrderSide as SchemaOrderSide

router = APIRouter(prefix="/api/v1", tags=["Trading API"])

# Dependency de Autenticación con X-API-KEY
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if settings.API_KEY and x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o ausente en header X-API-KEY"
        )
    return True


class TestSignalRequest(BaseModel):
    side: str  # BUY o SELL
    entry_price: Decimal
    sl_price: Optional[Decimal] = None
    tp1: Decimal
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
                "entry_price": float(t.entry_price),
                "current_sl": float(t.current_sl),
                "initial_sl": float(t.initial_sl),
                "tp1": float(t.tp1),
                "tp2": float(t.tp2) if t.tp2 else None,
                "tp3": float(t.tp3) if t.tp3 else None,
                "current_price": float(t.current_price),
                "current_pnl": float(t.current_pnl),
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

    return {
        "status": "NOMINAL",
        "ingestion_enabled": settings.INGESTION_ENABLED,
        "auto_execution_enabled": settings.AUTO_EXECUTION_ENABLED,
        "broker_type": settings.BROKER_TYPE,
        "xauusd_spot": {
            "bid": float(tick.bid),
            "ask": float(tick.ask),
            "timestamp": tick.timestamp
        },
        "account": {
            "balance": float(acc.balance),
            "equity": float(acc.equity),
            "margin_used": float(acc.margin_used),
            "free_margin": float(acc.free_margin),
            "margin_level_pct": float(acc.margin_level_pct),
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
                "open_time": t.open_time.isoformat() if t.open_time else None,
                "close_time": t.close_time.isoformat() if t.close_time else None
            }
            for t in trades
        ]
    }


@router.get("/messages")
async def get_raw_messages(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retorna los últimos mensajes de Telegram recibidos, con canal y detalles estructurados."""
    from backend.ingesta.parser import parse_signal
    stmt = select(RawTelegramMessage).order_by(desc(RawTelegramMessage.received_at)).limit(limit)
    result = await db.execute(stmt)
    messages = result.scalars().all()

    formatted = []
    for m in messages:
        signal_details = None
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
        elif isinstance(parsed, ModifierSignalEvent):
            signal_details = {
                "type": "MODIFIER",
                "action": parsed.action,
                "target_price": float(parsed.target_price) if parsed.target_price else None,
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
            "error_reason": m.error_reason,
            "received_at": m.received_at.isoformat()
        })

    return formatted


@router.get("/audit")
async def get_audit_logs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retorna los logs de auditoría del sistema."""
    stmt = select(SystemAuditLog).order_by(desc(SystemAuditLog.timestamp)).limit(limit)
    result = await db.execute(stmt)
    logs = result.scalars().all()

    return [
        {
            "id": l.id,
            "timestamp": l.timestamp.isoformat(),
            "event_type": l.event_type,
            "severity": l.severity,
            "details": l.details_json
        }
        for l in logs
    ]


@router.post("/control/pause", dependencies=[Depends(verify_api_key)])
async def pause_ingestion():
    """Pausa la ingesta de nuevas señales de Telegram."""
    settings.INGESTION_ENABLED = False
    return {"status": "success", "message": "Ingesta pausada correctamente", "ingestion_enabled": False}


@router.post("/control/resume", dependencies=[Depends(verify_api_key)])
async def resume_ingestion():
    """Reanuda la ingesta de señales."""
    settings.INGESTION_ENABLED = True
    return {"status": "success", "message": "Ingesta reanudada correctamente", "ingestion_enabled": True}


@router.post("/control/panic-close", dependencies=[Depends(verify_api_key)])
async def panic_close():
    """Ejecuta el Kill-Switch: Cierre inmediato de todas las posiciones abiertas."""
    from backend.main import app_state
    state_machine = app_state["state_machine"]
    await state_machine.panic_close_all(reason="DASHBOARD_PANIC_KILL_SWITCH")
    settings.INGESTION_ENABLED = False
    return {"status": "success", "message": "KILL-SWITCH ejecutado: Todas las posiciones han sido cerradas"}


@router.post("/control/close-slot/{slot_id}", dependencies=[Depends(verify_api_key)])
async def close_slot_manually(slot_id: int):
    """Cierra manualmente un slot específico a precio de mercado."""
    from backend.main import app_state
    state_machine = app_state["state_machine"]
    success = await state_machine.close_slot_manually(slot_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Slot {slot_id} no se encuentra activo o no existe")
    return {"status": "success", "message": f"Slot {slot_id} cerrado a mercado"}


@router.post("/signal/test", dependencies=[Depends(verify_api_key)])
async def inject_test_signal(req: TestSignalRequest):
    """Inyecta una señal de prueba en la cola interna para verificar la ejecución."""
    from backend.main import app_state
    queue = app_state["signal_queue"]

    side_enum = SchemaOrderSide.BUY if req.side.upper() == "BUY" else SchemaOrderSide.SELL
    tp_list = [req.tp1]
    if req.tp2:
        tp_list.append(req.tp2)
    if req.tp3:
        tp_list.append(req.tp3)

    event = TradingSignalEvent(
        asset="XAUUSD",
        side=side_enum,
        entry_price=req.entry_price,
        sl_price=req.sl_price,
        tp_levels=tp_list,
        requires_dynamic_sl=req.sl_price is None,
        raw_text=f"MANUAL TEST: {req.side} XAUUSD @ {req.entry_price}",
        message_id=999999,
        channel_id=0
    )

    await queue.put(event)
    return {"status": "success", "message": "Señal de prueba inyectada en la cola de ejecución", "signal": event.dict()}
