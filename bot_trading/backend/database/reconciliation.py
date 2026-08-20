import logging
import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from sqlalchemy import select, update

from backend.database.session import AsyncSessionLocal
from backend.database.models import Trade, TradeStatus, OrderSide, SystemAuditLog
from backend.broker.base import BaseBrokerAdapter, BrokerTick
from backend.risk.state_machine import TradeStateMachine, ActiveSlotTrade

logger = logging.getLogger("trading_bot.reconciliation")


async def run_startup_reconciliation(
    broker: BaseBrokerAdapter,
    state_machine: TradeStateMachine
):
    """
    Protocolo Estricto de Reconciliación Post-Reinicio:
    Al iniciar el sistema:
    1. Cruza las órdenes con estado abierto en SQLite con las posiciones activas del broker.
    2. Si el precio actual ya superó TP2 -> asegura SL en TP2 y restaura en memoria (STATE_2_TP2_HIT).
    3. Si el precio actual ya superó TP1 -> asegura SL en TP1 y restaura en memoria (STATE_1_TP1_HIT).
    4. REGLA ESTRICTA: Si NO se ha alcanzado ningún hito -> ejecuta inmediatamente EMERGENCY_CLOSE_MARKET
       en el broker, actualiza en DB como CLOSED_REBOOT_NO_MILESTONE y libera el slot.
    """
    logger.info("Iniciando Protocolo de Reconciliación Post-Reinicio...")

    async with AsyncSessionLocal() as session:
        # 1. Consultar trades abiertos en DB
        stmt = select(Trade).where(
            Trade.status.in_([
                TradeStatus.OPEN,
                TradeStatus.TP1_HIT,
                TradeStatus.TP2_HIT,
                TradeStatus.PENDING
            ])
        )
        result = await session.execute(stmt)
        open_trades: List[Trade] = list(result.scalars().all())

        if not open_trades:
            logger.info("Reconciliación completa: No existen órdenes abiertas en base de datos.")
            return

        # 2. Consultar cotización de mercado actual
        tick: BrokerTick = await broker.get_current_tick("XAUUSD")
        reconciled_count = 0
        emergency_closed_count = 0

        for trade in open_trades:
            market_price = tick.bid if trade.side == OrderSide.BUY else tick.ask

            # Comprobar si se alcanzó TP2
            is_tp2_reached = False
            if trade.tp2:
                is_tp2_reached = (market_price >= trade.tp2) if trade.side == OrderSide.BUY else (market_price <= trade.tp2)

            # Comprobar si se alcanzó TP1
            is_tp1_reached = (market_price >= trade.tp1) if trade.side == OrderSide.BUY else (market_price <= trade.tp1)

            if is_tp2_reached:
                # Actualizar a TP2 HIT
                trade.status = TradeStatus.TP2_HIT
                trade.current_sl = trade.tp2
                await broker.modify_order(trade.ticket_id, new_sl=trade.tp2)
                
                # Restaurar en memoria
                state_machine.active_slots[trade.slot_id] = ActiveSlotTrade(
                    slot_id=trade.slot_id,
                    ticket_id=trade.ticket_id,
                    db_trade_id=trade.id,
                    symbol=trade.symbol,
                    side=trade.side,
                    status=TradeStatus.TP2_HIT,
                    entry_price=trade.entry_price,
                    current_sl=trade.tp2,
                    initial_sl=trade.initial_sl,
                    tp1=trade.tp1,
                    tp2=trade.tp2,
                    tp3=trade.tp3,
                    lot_size=trade.lot_size,
                    open_time=trade.open_time.timestamp() if trade.open_time else datetime.now(timezone.utc).timestamp(),
                    current_price=market_price
                )
                reconciled_count += 1
                logger.info(f"Reconciliación: Slot {trade.slot_id} ({trade.ticket_id}) restaurado en TP2_HIT (SL: {trade.tp2}).")

            elif is_tp1_reached:
                # Actualizar a TP1 HIT
                trade.status = TradeStatus.TP1_HIT
                trade.current_sl = trade.tp1
                await broker.modify_order(trade.ticket_id, new_sl=trade.tp1)

                # Restaurar en memoria
                state_machine.active_slots[trade.slot_id] = ActiveSlotTrade(
                    slot_id=trade.slot_id,
                    ticket_id=trade.ticket_id,
                    db_trade_id=trade.id,
                    symbol=trade.symbol,
                    side=trade.side,
                    status=TradeStatus.TP1_HIT,
                    entry_price=trade.entry_price,
                    current_sl=trade.tp1,
                    initial_sl=trade.initial_sl,
                    tp1=trade.tp1,
                    tp2=trade.tp2,
                    tp3=trade.tp3,
                    lot_size=trade.lot_size,
                    open_time=trade.open_time.timestamp() if trade.open_time else datetime.now(timezone.utc).timestamp(),
                    current_price=market_price
                )
                reconciled_count += 1
                logger.info(f"Reconciliación: Slot {trade.slot_id} ({trade.ticket_id}) restaurado en TP1_HIT (SL: {trade.tp1}).")

            else:
                # REGLA ESTRICTA: Sin hitos alcanzados -> Cierre de emergencia inmediato
                logger.warning(
                    f"Reconciliación: Slot {trade.slot_id} ({trade.ticket_id}) no alcanzó TP1 tras reinicio "
                    f"(Entrada: {trade.entry_price}, Actual: {market_price}). Ejecutando EMERGENCY_CLOSE_MARKET..."
                )
                exec_price, realized_pnl = await broker.close_order(
                    trade.ticket_id,
                    close_price=market_price,
                    reason="REBOOT_NO_MILESTONE_EMERGENCY_CLOSE"
                )
                trade.status = TradeStatus.CLOSED_REBOOT_NO_MILESTONE
                trade.close_price = exec_price
                trade.pnl = realized_pnl
                trade.close_reason = "REBOOT_NO_MILESTONE_EMERGENCY_CLOSE"
                trade.close_time = datetime.now(timezone.utc)
                emergency_closed_count += 1

        # Guardar cambios y registrar auditoría
        audit_entry = SystemAuditLog(
            event_type="RECONCILIATION_COMPLETED",
            severity="INFO" if emergency_closed_count == 0 else "WARNING",
            details_json=json.dumps({
                "total_trades_checked": len(open_trades),
                "reconciled_slots": reconciled_count,
                "emergency_closed_slots": emergency_closed_count,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        )
        session.add(audit_entry)
        await session.commit()

    logger.info(
        f"Reconciliación finalizada con éxito. "
        f"Restaurados: {reconciled_count} | Cerrados por seguridad: {emergency_closed_count}"
    )
