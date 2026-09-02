import asyncio
import logging
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, Optional, List
from backend.ingesta.schemas import TradingSignalEvent, OrderSide
from backend.repository.messages import update_message_error_reason
from backend.config import settings

logger = logging.getLogger("trading_bot.risk.pullback_watcher")


class PendingSignal:
    def __init__(
        self,
        event: TradingSignalEvent,
        entry_min: Optional[Decimal] = None,
        entry_max: Optional[Decimal] = None,
        timeout_minutes: int = 15
    ):
        self.event = event
        self.entry_min = entry_min
        self.entry_max = entry_max
        self.created_at = datetime.now(timezone.utc)
        self.timeout_at = self.created_at + timedelta(minutes=timeout_minutes)
        self.message_id = event.message_id
        self.channel_name = getattr(event, 'channel_name', 'Chartoro FX')
        self.side = event.side
        self.entry_price = event.entry_price
        self.tp1 = event.tp_levels[0] if event.tp_levels else None
        self.status = "WATCHING"  # WATCHING, TRIGGERED, EXPIRED, CANCELLED_TP_REACHED


class PullbackWatcher:
    """
    Vigilante de Retroceso (Pullback Watcher):
    Gestiona señales que llegaron con desfase respecto al precio de mercado.
    En lugar de descartarlas inmediatamente, las vigila durante un tiempo límite (ej. 15 min):
    - Si el precio retrocede a la zona segura (diff <= 2.00 USD), ejecuta la orden con R:R óptimo.
    - Si el precio alcanza TP1 sin retroceder, cancela la orden sin arriesgar capital.
    - Si se supera el timeout sin retroceso, expira la orden limpiamente.
    """

    def __init__(self, risk_engine, state_machine, broker):
        self.risk_engine = risk_engine
        self.state_machine = state_machine
        self.broker = broker
        self.pending_signals: Dict[int, PendingSignal] = {}
        self.timeout_minutes = getattr(settings, 'PULLBACK_TIMEOUT_MINUTES', 15)
        self._lock = asyncio.Lock()

    async def add_signal(
        self,
        event: TradingSignalEvent,
        entry_min: Optional[Decimal] = None,
        entry_max: Optional[Decimal] = None
    ) -> bool:
        """
        Registra una señal fuera de precio inicial para vigilar su posible retroceso.
        Retorna True si fue añadida a la cola de vigilancia.
        """
        if not event.message_id:
            return False

        try:
            current_tick = await self.broker.get_current_tick("XAUUSD")
            market_price = current_tick.ask if event.side == OrderSide.BUY else current_tick.bid
            tp1 = event.tp_levels[0] if event.tp_levels else None

            # Validar coherencia matemática del TP1 con la dirección ANTES de usarlo como filtro.
            # Si el parser confundió SL con TP1 (e.g. TP1 < entry_price en un BUY),
            # el TP1 es incoherente y NO debe usarse para cancelar el pullback.
            tp1_is_coherent = False
            if tp1:
                if event.side == OrderSide.BUY:
                    tp1_is_coherent = tp1 > event.entry_price
                else:  # SELL
                    tp1_is_coherent = tp1 < event.entry_price

            # Solo cancelar si el TP1 es válido Y el mercado ya lo ha alcanzado
            # (el movimiento ya ocurrió sin nosotros — no tiene sentido entrar ahora)
            if tp1 and tp1_is_coherent:
                if event.side == OrderSide.BUY and market_price >= tp1:
                    logger.info(
                        f"🚫 [PULLBACK WATCHER] Señal {event.message_id} descartada: "
                        f"mercado ({market_price}) ya alcanzó TP1 ({tp1}) sin dar opción a pullback."
                    )
                    return False
                elif event.side == OrderSide.SELL and market_price <= tp1:
                    logger.info(
                        f"🚫 [PULLBACK WATCHER] Señal {event.message_id} descartada: "
                        f"mercado ({market_price}) ya alcanzó TP1 ({tp1}) sin dar opción a pullback."
                    )
                    return False
            elif tp1 and not tp1_is_coherent:
                logger.warning(
                    f"⚠️ [PULLBACK WATCHER] Señal {event.message_id}: TP1={tp1} incoherente "
                    f"con dirección {event.side.value} (entry={event.entry_price}). "
                    f"Ignorando filtro de TP1 — posible confusión SL/TP1 en el parser."
                )
                tp1 = None  # No usar TP1 incoherente para ningún filtro

            async with self._lock:
                pending = PendingSignal(
                    event=event,
                    entry_min=entry_min,
                    entry_max=entry_max,
                    timeout_minutes=self.timeout_minutes
                )
                self.pending_signals[event.message_id] = pending

            logger.info(
                f"⏳ [PULLBACK WATCHER] Señal {event.message_id} ({event.side.value} @ {event.entry_price}) "
                f"en VIGILANCIA DE RETROCESO (timeout {self.timeout_minutes} min hasta {pending.timeout_at.strftime('%H:%M:%S')} UTC)"
            )
            return True

        except Exception as e:
            logger.error(f"[PULLBACK WATCHER] Error registrando señal {event.message_id}: {e}")
            return False

    async def on_market_tick(self, tick) -> None:
        """
        Evalúa en cada tick de mercado las señales en espera.
        """
        if not self.pending_signals:
            return

        now = datetime.now(timezone.utc)
        to_remove = []

        async with self._lock:
            for msg_id, pending in list(self.pending_signals.items()):
                # 1. Comprobar Expiración por Tiempo
                if now >= pending.timeout_at:
                    logger.info(f"⌛ [PULLBACK WATCHER] Señal {msg_id} expiró tras {self.timeout_minutes}m sin retroceso.")
                    await self._update_db_error_reason(msg_id, "FUERA PRECIO (TIMEOUT PULLBACK)")
                    await self.state_machine.emit_alert("PULLBACK_EXPIRED", {
                        "message_id": msg_id,
                        "channel": pending.channel_name,
                        "reason": f"Timeout de {self.timeout_minutes} min alcanzado"
                    })
                    to_remove.append(msg_id)
                    continue

                # 2. Comprobar Invalidación por TP1 alcanzado sin retroceder
                # Solo aplica si el TP1 es coherente con la dirección de la señal.
                if pending.tp1:
                    tp1_coherent = (
                        (pending.side == OrderSide.BUY and pending.tp1 > pending.entry_price) or
                        (pending.side == OrderSide.SELL and pending.tp1 < pending.entry_price)
                    )
                    if tp1_coherent:
                        if pending.side == OrderSide.BUY and tick.bid >= pending.tp1:
                            logger.info(f"🎯 [PULLBACK WATCHER] Señal {msg_id} cancelada: TP1 ({pending.tp1}) alcanzado sin retroceso previo.")
                            await self._update_db_error_reason(msg_id, "FUERA PRECIO (TP ALCANZADO)")
                            await self.state_machine.emit_alert("PULLBACK_CANCELLED_TP", {
                                "message_id": msg_id,
                                "channel": pending.channel_name,
                                "tp1": float(pending.tp1)
                            })
                            to_remove.append(msg_id)
                            continue
                        elif pending.side == OrderSide.SELL and tick.ask <= pending.tp1:
                            logger.info(f"🎯 [PULLBACK WATCHER] Señal {msg_id} cancelada: TP1 ({pending.tp1}) alcanzado sin retroceso previo.")
                            await self._update_db_error_reason(msg_id, "FUERA PRECIO (TP ALCANZADO)")
                            await self.state_machine.emit_alert("PULLBACK_CANCELLED_TP", {
                                "message_id": msg_id,
                                "channel": pending.channel_name,
                                "tp1": float(pending.tp1)
                            })
                            to_remove.append(msg_id)
                            continue

                # 3. Comprobar si el precio ha retrocedido a la zona segura (Slippage <= 2.00 USD)
                is_slippage_ok, market_price, diff = await self.risk_engine.check_slippage(
                    pending.entry_price,
                    pending.side,
                    entry_min=pending.entry_min,
                    entry_max=pending.entry_max,
                    current_tick=tick
                )

                if is_slippage_ok:
                    logger.info(
                        f"🎯 [PULLBACK WATCHER] ¡RETROCESO DETECTADO para señal {msg_id}! "
                        f"Mercado={market_price} en rango seguro (Diff={diff:.2f} <= {self.risk_engine.slippage_tolerance} USD). "
                        f"Ejecutando orden con R:R óptimo..."
                    )
                    executed = await self._execute_pending_signal(pending, market_price)
                    if executed:
                        to_remove.append(msg_id)

            for mid in to_remove:
                self.pending_signals.pop(mid, None)

    async def _execute_pending_signal(self, pending: PendingSignal, market_price: Decimal) -> bool:
        """Abre la orden cuando el retroceso se cumple y hay slot libre."""
        can_execute, slot_id, reason = self.risk_engine.evaluate_signal_for_slot(
            pending.event, self.state_machine.active_slots
        )
        if not can_execute or slot_id is None:
            logger.warning(f"⚠️ [PULLBACK WATCHER] Pullback cazado para señal {pending.message_id} pero NO hay slots libres ({reason}).")
            return False

        event = pending.event
        actual_entry = market_price if (pending.entry_min and pending.entry_max and pending.entry_min <= market_price <= pending.entry_max) else event.entry_price
        sl = self.risk_engine.sanitize_sl(event.side, actual_entry, event.sl_price)
        account_info = await self.broker.get_account_info()
        lot_size = await self.risk_engine.calculate_lot_size(actual_entry, account_info)

        trade = await self.state_machine.open_new_trade(
            slot_id=slot_id,
            side=event.side,
            lot_size=lot_size,
            entry_price=actual_entry,
            sl=sl,
            tp_levels=event.tp_levels,
            raw_signal_id=event.message_id,
            channel_id=event.channel_id,
            channel_name=pending.channel_name,
            execution_mode=getattr(event, 'execution_mode', 'AUDIT')
        )

        if trade:
            await self._update_db_error_reason(pending.message_id, None)
            logger.info(f"🚀 [PULLBACK WATCHER] Trade {trade.ticket_id} abierto exitosamente tras retroceso de mercado.")
            return True
        else:
            return False

    async def _update_db_error_reason(self, message_id: int, reason: Optional[str]) -> None:
        try:
            await update_message_error_reason(message_id, reason)
        except Exception as e:
            logger.debug(f"Aviso actualizando DB en PullbackWatcher: {e}")
