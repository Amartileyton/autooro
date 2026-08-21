import asyncio
import logging
import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List, Optional, Callable, Any, Tuple
from pydantic import BaseModel

from backend.broker.base import BaseBrokerAdapter, BrokerTick
from backend.database.session import AsyncSessionLocal
from backend.database.models import Trade, TradeStatus, OrderSide, SystemAuditLog
from backend.ingesta.schemas import ModifierSignalEvent, SignalType
from sqlalchemy import select, update

logger = logging.getLogger("trading_bot.state_machine")


class ActiveSlotTrade(BaseModel):
    """Representación en memoria de alta velocidad para una orden activa en un slot."""
    slot_id: int
    ticket_id: str
    db_trade_id: int
    raw_signal_id: Optional[int] = None
    symbol: str = "XAUUSD"
    side: OrderSide
    status: TradeStatus
    entry_price: Decimal
    current_sl: Decimal
    initial_sl: Decimal
    tp1: Decimal
    tp2: Optional[Decimal] = None
    tp3: Optional[Decimal] = None
    lot_size: Decimal
    open_time: float
    current_pnl: Decimal = Decimal("0.00")
    current_price: Decimal = Decimal("0.00")


class TradeStateMachine:
    """
    Máquina de Estados de Trailing SL por Hitos y Gestor de Slots:
    - STATE 0 (OPEN): SL original y TP3 como take-profit final.
    - STATE 1 (TP1 superado): Modificación inmediata de SL a TP1_Price (Break-Even asegurado).
    - STATE 2 (TP2 superado): Modificación de SL a TP2_Price.
    - STATE 3 (TP3 alcanzado): Cierre automático total por Take Profit.
    - Procesa ticks con latencia sub-100ms.
    """

    def __init__(self, broker: BaseBrokerAdapter):
        self.broker = broker
        # Slots activos en memoria: {slot_id: ActiveSlotTrade}
        self.active_slots: Dict[int, ActiveSlotTrade] = {}
        # Callback para notificaciones (ej. Bot de Telegram o WebSocket)
        self.alert_callbacks: List[Callable[[str, dict], Any]] = []
        self._lock = asyncio.Lock()

    def register_alert_callback(self, callback: Callable[[str, dict], Any]):
        """Registra un receptor de alertas (Bot de Telegram / WS)."""
        if callback not in self.alert_callbacks:
            self.alert_callbacks.append(callback)

    async def emit_alert(self, event_type: str, data: dict):
        """Dispara alertas a todos los listeners registrados."""
        for cb in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(event_type, data)
                else:
                    cb(event_type, data)
            except Exception as e:
                logger.error(f"Error al emitir alerta {event_type}: {e}")

    async def open_new_trade(
        self,
        slot_id: int,
        side: OrderSide,
        lot_size: Decimal,
        entry_price: Decimal,
        sl: Decimal,
        tp_levels: List[Decimal],
        raw_signal_id: Optional[int] = None
    ) -> Optional[ActiveSlotTrade]:
        """
        Ejecuta la orden en el broker, persiste en SQLite y activa el Slot en la máquina de estados.
        """
        async with self._lock:
            if slot_id in self.active_slots:
                logger.error(f"Slot {slot_id} ya se encuentra ocupado.")
                return None

            tp1 = tp_levels[0]
            tp2 = tp_levels[1] if len(tp_levels) > 1 else None
            tp3 = tp_levels[2] if len(tp_levels) > 2 else (tp2 or tp1)

            # 1. Ejecución instantánea en el broker
            ticket_id = await self.broker.execute_order(
                symbol="XAUUSD",
                side=side,
                lot_size=lot_size,
                entry_price=entry_price,
                sl=sl,
                tp=tp3,
                comment=f"Slot-{slot_id}"
            )

            # 2. Persistencia en SQLite (WAL)
            db_trade_id = 0
            try:
                async with AsyncSessionLocal() as session:
                    db_trade = Trade(
                        ticket_id=ticket_id,
                        slot_id=slot_id,
                        symbol="XAUUSD",
                        side=side,
                        status=TradeStatus.OPEN,
                        entry_price=entry_price,
                        current_sl=sl,
                        initial_sl=sl,
                        tp1=tp1,
                        tp2=tp2,
                        tp3=tp3,
                        lot_size=lot_size,
                        pnl=Decimal("0.00"),
                        open_time=datetime.now(timezone.utc),
                        raw_signal_id=raw_signal_id
                    )
                    session.add(db_trade)
                    await session.commit()
                    await session.refresh(db_trade)
                    db_trade_id = db_trade.id
            except Exception as e:
                logger.error(f"Error al guardar trade en DB: {e}")

            # 3. Registrar en memoria activa
            active_trade = ActiveSlotTrade(
                slot_id=slot_id,
                ticket_id=ticket_id,
                db_trade_id=db_trade_id,
                raw_signal_id=raw_signal_id,
                symbol="XAUUSD",
                side=side,
                status=TradeStatus.OPEN,
                entry_price=entry_price,
                current_sl=sl,
                initial_sl=sl,
                tp1=tp1,
                tp2=tp2,
                tp3=tp3,
                lot_size=lot_size,
                open_time=time.time(),
                current_price=entry_price
            )

            self.active_slots[slot_id] = active_trade

            logger.info(f"Slot {slot_id} ABIERTO: {ticket_id} | {side.value} {lot_size}L @ {entry_price} | SL: {sl} | TP1: {tp1}")
            
            await self.emit_alert("ORDER_OPENED", {
                "slot_id": slot_id,
                "ticket_id": ticket_id,
                "side": side.value,
                "lot_size": float(lot_size),
                "entry_price": float(entry_price),
                "sl": float(sl),
                "tp1": float(tp1),
                "tp2": float(tp2) if tp2 else None,
                "tp3": float(tp3) if tp3 else None
            })

            return active_trade

    async def find_matching_active_trade(
        self,
        side: OrderSide,
        entry_price: Decimal,
        max_price_delta: Decimal = Decimal("2.00"),
        max_age_seconds: float = 300.0
    ) -> Optional[Tuple[int, ActiveSlotTrade]]:
        """
        Busca si ya existe una orden activa reciente en la misma dirección y precio similar.
        Permite enriquecer órdenes abiertas por alertas rápidas (BUY NOW) cuando llega la plantilla formal (SIGNAL ALERT).
        """
        now = time.time()
        async with self._lock:
            for slot_id, trade in self.active_slots.items():
                if trade.side == side:
                    price_diff = abs(trade.entry_price - entry_price)
                    age = now - trade.open_time
                    if price_diff <= max_price_delta and age <= max_age_seconds:
                        return slot_id, trade
        return None

    async def enrich_active_trade(
        self,
        slot_id: int,
        sl: Optional[Decimal],
        tp_levels: List[Decimal],
        raw_signal_id: Optional[int] = None
    ) -> bool:
        """
        Actualiza el SL y Take Profits extendidos de una orden activa cuando llega la plantilla oficial posterior.
        """
        async with self._lock:
            if slot_id not in self.active_slots:
                return False

            trade = self.active_slots[slot_id]
            modified = False

            # Actualizar SL si viene explícito en la plantilla oficial
            if sl is not None and sl != trade.current_sl:
                trade.current_sl = sl
                trade.initial_sl = sl
                await self.broker.modify_order(trade.ticket_id, new_sl=sl)
                modified = True
                logger.info(f"Slot {slot_id} ENRIQUECIDO: SL oficial actualizado a {sl}")

            # Actualizar TP2 y TP3 si vienen en la plantilla oficial
            if len(tp_levels) > 1:
                trade.tp1 = tp_levels[0]
                trade.tp2 = tp_levels[1]
                trade.tp3 = tp_levels[2] if len(tp_levels) > 2 else trade.tp2
                modified = True
                logger.info(f"Slot {slot_id} ENRIQUECIDO: TPs extendidos actualizados a TP1={trade.tp1}, TP2={trade.tp2}, TP3={trade.tp3}")

            if raw_signal_id and not trade.raw_signal_id:
                trade.raw_signal_id = raw_signal_id

            if modified:
                try:
                    async with AsyncSessionLocal() as session:
                        stmt = (
                            update(Trade)
                            .where(Trade.ticket_id == trade.ticket_id)
                            .values(
                                current_sl=trade.current_sl,
                                initial_sl=trade.initial_sl,
                                tp1=trade.tp1,
                                tp2=trade.tp2,
                                tp3=trade.tp3
                            )
                        )
                        await session.execute(stmt)
                        await session.commit()
                except Exception as e:
                    logger.error(f"Error al actualizar enriquecimiento en DB: {e}")

                await self.emit_alert("ORDER_ENRICHED", {
                    "slot_id": slot_id,
                    "ticket_id": trade.ticket_id,
                    "new_sl": float(trade.current_sl),
                    "tp1": float(trade.tp1),
                    "tp2": float(trade.tp2) if trade.tp2 else None,
                    "tp3": float(trade.tp3) if trade.tp3 else None
                })

            return True

    async def on_market_tick(self, tick: BrokerTick):
        """
        Handler de ticks en tiempo real (<100ms):
        Evalúa Stop Loss y transiciones de hitos TP1, TP2, TP3 para todos los slots activos.
        """
        if not self.active_slots:
            return

        for slot_id, trade in list(self.active_slots.items()):
            price = tick.bid if trade.side == OrderSide.BUY else tick.ask
            trade.current_price = price

            # Calcular PnL flotante
            if trade.side == OrderSide.BUY:
                trade.current_pnl = (price - trade.entry_price) * trade.lot_size * Decimal("100.0")
            else:
                trade.current_pnl = (trade.entry_price - price) * trade.lot_size * Decimal("100.0")

            # 1. Comprobar STOP LOSS HIT
            is_sl_hit = (price <= trade.current_sl) if trade.side == OrderSide.BUY else (price >= trade.current_sl)
            if is_sl_hit:
                await self._close_slot(slot_id, close_price=price, status=TradeStatus.CLOSED_SL, reason=f"SL_HIT ({trade.current_sl})")
                continue

            # 2. Comprobar HITO TP1 (STATE 0 -> STATE 1) - CIERRE PARCIAL DEL 50% + SL A BREAK-EVEN
            if trade.status == TradeStatus.OPEN:
                is_tp1_hit = (price >= trade.tp1) if trade.side == OrderSide.BUY else (price <= trade.tp1)
                if is_tp1_hit:
                    trade.status = TradeStatus.TP1_HIT
                    
                    # Cierre parcial del 50% del volumen
                    half_lot = (trade.lot_size / Decimal("2.0")).quantize(Decimal("0.01"))
                    if half_lot >= Decimal("0.01"):
                        partial_pnl = abs(price - trade.entry_price) * half_lot * Decimal("100.0")
                        trade.lot_size = trade.lot_size - half_lot
                        logger.info(f"Slot {slot_id} [CIERRE PARCIAL 50%]: Cerrados {half_lot} lotes @ {price}. Beneficio asegurado: +${partial_pnl:.2f}")
                    
                    # Mover Stop Loss del 50% restante a PRECIO DE ENTRADA (BREAK-EVEN)
                    new_sl = trade.entry_price
                    trade.current_sl = new_sl
                    
                    # Modificar en broker instantáneamente
                    await self.broker.modify_order(trade.ticket_id, new_sl=new_sl)
                    await self._update_trade_in_db(trade)
                    
                    logger.info(f"Slot {slot_id} [HITO TP1 ALCANZADO]: SL movido a Break-Even (${new_sl}). 50% restante corriendo libre de riesgo.")
                    await self.emit_alert("TP1_PARTIAL_CLOSE", {
                        "slot_id": slot_id,
                        "ticket_id": trade.ticket_id,
                        "new_sl": float(new_sl),
                        "market_price": float(price),
                        "closed_lots": float(half_lot),
                        "remaining_lots": float(trade.lot_size)
                    })

            # 3. Comprobar HITO TP2 (STATE 1 -> STATE 2) - MOVER SL DEL RESTO A TP1
            if trade.status == TradeStatus.TP1_HIT and trade.tp2:
                is_tp2_hit = (price >= trade.tp2) if trade.side == OrderSide.BUY else (price <= trade.tp2)
                if is_tp2_hit:
                    trade.status = TradeStatus.TP2_HIT
                    new_sl = trade.tp1  # Asegurar ganancias de TP1 en el 50% restante
                    trade.current_sl = new_sl
                    
                    await self.broker.modify_order(trade.ticket_id, new_sl=new_sl)
                    await self._update_trade_in_db(trade)
                    
                    logger.info(f"Slot {slot_id} [HITO TP2 ALCANZADO]: SL del 50% restante subido a TP1 ({new_sl})")
                    await self.emit_alert("TP2_HIT", {
                        "slot_id": slot_id,
                        "ticket_id": trade.ticket_id,
                        "new_sl": float(new_sl),
                        "market_price": float(price)
                    })

            # 4. Comprobar HITO TP3 / CIERRE FINAL (STATE 2 -> STATE 3)
            target_tp3 = trade.tp3 or trade.tp2 or trade.tp1
            is_tp3_hit = (price >= target_tp3) if trade.side == OrderSide.BUY else (price <= target_tp3)
            if is_tp3_hit and trade.status in (TradeStatus.OPEN, TradeStatus.TP1_HIT, TradeStatus.TP2_HIT):
                await self._close_slot(slot_id, close_price=price, status=TradeStatus.CLOSED_TP, reason=f"TP_FINAL_REACHED ({target_tp3})")

    async def handle_modifier_signal(self, event: ModifierSignalEvent):
        """Procesa señales de modificación provenientes de Telegram vinculándolas al trade correspondiente."""
        if not self.active_slots:
            logger.info("No hay slots activos para aplicar modificador.")
            return

        async with self._lock:
            target_trades = []
            if event.reply_to_msg_id:
                # Buscar trade específico que fue abierto por ese mensaje padre
                for slot_id, trade in self.active_slots.items():
                    if trade.raw_signal_id == event.reply_to_msg_id:
                        target_trades.append((slot_id, trade))
            
            # Si no vino como reply o no se encontró, aplicar a los slots activos
            if not target_trades:
                target_trades = list(self.active_slots.items())

            for slot_id, trade in target_trades:
                if event.signal_type == SignalType.MOVE_SL and event.target_price:
                    trade.current_sl = event.target_price
                    await self.broker.modify_order(trade.ticket_id, new_sl=event.target_price)
                    await self._update_trade_in_db(trade)
                    logger.info(f"Modificador aplicado Slot {slot_id} ({trade.ticket_id}): SL movido a {event.target_price}")
                    await self.emit_alert("SL_MODIFIED", {"slot_id": slot_id, "new_sl": float(event.target_price)})

                elif event.signal_type == SignalType.MOVE_BE:
                    trade.current_sl = trade.entry_price
                    await self.broker.modify_order(trade.ticket_id, new_sl=trade.entry_price)
                    await self._update_trade_in_db(trade)
                    logger.info(f"Modificador aplicado Slot {slot_id} ({trade.ticket_id}): SL a Break-Even ({trade.entry_price})")
                    await self.emit_alert("SL_BE_APPLIED", {"slot_id": slot_id, "be_price": float(trade.entry_price)})

                elif event.signal_type == SignalType.CLOSE_ORDER:
                    tick = await self.broker.get_current_tick("XAUUSD")
                    price = tick.bid if trade.side == OrderSide.BUY else tick.ask
                    await self._close_slot(slot_id, close_price=price, status=TradeStatus.CLOSED_MANUAL, reason="TELEGRAM_CLOSE_SIGNAL")

    async def panic_close_all(self, reason: str = "KILL_SWITCH_ACTIVATED"):
        """Cierre de emergencia de todos los slots activos simultáneamente."""
        async with self._lock:
            slots_to_close = list(self.active_slots.keys())
            logger.warning(f"EJECUTANDO PANIC CLOSE en {len(slots_to_close)} slots activos. Motivo: {reason}")
            
            for slot_id in slots_to_close:
                tick = await self.broker.get_current_tick("XAUUSD")
                trade = self.active_slots.get(slot_id)
                if trade:
                    price = tick.bid if trade.side == OrderSide.BUY else tick.ask
                    await self._close_slot(slot_id, close_price=price, status=TradeStatus.CLOSED_KILL_SWITCH, reason=reason)

    async def close_slot_manually(self, slot_id: int) -> bool:
        """Cierra manualmente un slot individual desde la API o Dashboard."""
        async with self._lock:
            if slot_id not in self.active_slots:
                return False
            trade = self.active_slots[slot_id]
            tick = await self.broker.get_current_tick("XAUUSD")
            price = tick.bid if trade.side == OrderSide.BUY else tick.ask
            await self._close_slot(slot_id, close_price=price, status=TradeStatus.CLOSED_MANUAL, reason="MANUAL_DASHBOARD_CLOSE")
            return True

    async def _close_slot(
        self,
        slot_id: int,
        close_price: Decimal,
        status: TradeStatus,
        reason: str
    ):
        """Cierra el trade en el broker, liquida en DB y libera el slot."""
        if slot_id not in self.active_slots:
            return

        trade = self.active_slots.pop(slot_id)
        
        # 1. Cerrar en Broker
        exec_price, realized_pnl = await self.broker.close_order(trade.ticket_id, close_price=close_price, reason=reason)

        # 2. Actualizar en DB
        try:
            async with AsyncSessionLocal() as session:
                stmt = (
                    update(Trade)
                    .where(Trade.ticket_id == trade.ticket_id)
                    .values(
                        status=status,
                        close_price=exec_price,
                        pnl=realized_pnl,
                        close_reason=reason,
                        close_time=datetime.now(timezone.utc)
                    )
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.error(f"Error al actualizar cierre de trade en DB: {e}")

        logger.info(f"Slot {slot_id} CERRADO [{status.value}] @ {exec_price} | PnL: ${realized_pnl:+.2f} USD | Motivo: {reason}")

        await self.emit_alert("ORDER_CLOSED", {
            "slot_id": slot_id,
            "ticket_id": trade.ticket_id,
            "status": status.value,
            "close_price": float(exec_price),
            "pnl": float(realized_pnl),
            "reason": reason
        })

    async def _update_trade_in_db(self, trade: ActiveSlotTrade):
        """Actualiza el estado y SL de la orden en SQLite."""
        try:
            async with AsyncSessionLocal() as session:
                stmt = (
                    update(Trade)
                    .where(Trade.ticket_id == trade.ticket_id)
                    .values(
                        status=trade.status,
                        current_sl=trade.current_sl
                    )
                )
                await session.execute(stmt)
                await session.commit()
        except Exception as e:
            logger.error(f"Error al actualizar estado en DB: {e}")
