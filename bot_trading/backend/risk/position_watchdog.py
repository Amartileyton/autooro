import asyncio
import logging
from decimal import Decimal
from typing import Optional, Dict
from datetime import datetime, timezone

from backend.broker.base import BaseBrokerAdapter, OrderSide
from backend.risk.state_machine import TradeStateMachine, TradeStatus
from backend.telegram_admin.notifier import dispatch_telegram_alert

logger = logging.getLogger("trading_bot.position_watchdog")


class PositionWatchdog:
    """
    Guardián Autónomo de Posiciones y Discrepancias Broker <-> Bot.
    Se ejecuta de forma continua cada 12 segundos para garantizar que:
    1. No existan posiciones 'fantasma' en cTrader sin gestión ni Stop Loss.
    2. No existan slots abiertos en el bot si cTrader ya cerró la posición.
    3. Toda posición viva en cTrader tenga SIEMPRE un Stop Loss activo en el servidor del broker.
    4. Sincronice de inmediato cualquier discordancia de tickets.
    """
    def __init__(self, broker: BaseBrokerAdapter, state_machine: TradeStateMachine, check_interval: float = 12.0):
        self.broker = broker
        self.state_machine = state_machine
        self.check_interval = check_interval
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._last_notified_orphans = set()

    async def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"🛡️ [POSITION WATCHDOG] Guardián de discrepancias activo (intervalo: {self.check_interval:.1f}s).")

    async def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🛡️ [POSITION WATCHDOG] Guardián detenido.")

    async def _run_loop(self):
        await asyncio.sleep(8.0)
        while self._running:
            try:
                await self.audit_positions()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"🛡️ [POSITION WATCHDOG] Error en ciclo de auditoría: {e}", exc_info=True)
            await asyncio.sleep(self.check_interval)

    async def audit_positions(self):
        # 1. Sincronizar y obtener posiciones vivas reales del broker
        if hasattr(self.broker, "_sync_open_positions") and getattr(self.broker, "_connected", False):
            try:
                await self.broker._sync_open_positions()
            except Exception as e:
                logger.debug(f"[WATCHDOG] Aviso al sincronizar posiciones: {e}")

        open_positions = await self.broker.get_open_positions()
        broker_pos_by_id = {str(p.ticket_id).strip(): p for p in open_positions}

        active_slots = self.state_machine.active_slots

        # 2. Auditar cada slot activo en el bot
        for slot_id, trade in list(active_slots.items()):
            clean_ticket = str(trade.ticket_id).replace("CTR-", "").replace("TKT-", "").strip()

            # Caso 1: Comprobar si el ticket coincide exactamente o se puede resolver
            matched_pos = broker_pos_by_id.get(clean_ticket)
            if not matched_pos and len(broker_pos_by_id) == 1:
                candidate = next(iter(broker_pos_by_id.values()))
                if candidate.symbol == trade.symbol and candidate.side == trade.side:
                    matched_pos = candidate
                    if trade.ticket_id != candidate.ticket_id:
                        logger.warning(
                            f"🛡️ [WATCHDOG] Corrigiendo ticket en Slot {slot_id}: "
                            f"{trade.ticket_id} -> {candidate.ticket_id}"
                        )
                        trade.ticket_id = candidate.ticket_id
                        try:
                            from backend.repository.trades import update_trade_ticket
                            if getattr(trade, 'db_trade_id', None):
                                await update_trade_ticket(trade.db_trade_id, candidate.ticket_id)
                        except Exception as sync_err:
                            logger.error(f"🛡️ [WATCHDOG] Error al persistir ticket corregido en DB: {sync_err}")

            if matched_pos:
                # La posición existe en el broker. ¡VERIFICAR QUE TENGA STOP LOSS EN EL SERVIDOR!
                if matched_pos.sl is None or matched_pos.sl <= Decimal("0"):
                    logger.critical(
                        f"🚨 [WATCHDOG CRÍTICO] La posición {matched_pos.ticket_id} en cTrader NO TIENE STOP LOSS! "
                        f"Aplicando Stop Loss de protección inmediatamente: ${trade.current_sl}..."
                    )
                    await self.broker.modify_order(matched_pos.ticket_id, new_sl=trade.current_sl)
                    try:
                        await dispatch_telegram_alert("SYSTEM_INFO", {
                            "text": f"🛡️ *[WATCHDOG DEFENSA]* Se ha restituido el Stop Loss `${trade.current_sl}` en cTrader para la posición `{matched_pos.ticket_id}` que estaba desprotegida."
                        })
                    except Exception:
                        pass
            else:
                # El slot figura en memoria del bot, pero la posición YA NO EXISTE en cTrader
                # (fue cerrada por el broker en SL, TP o cierre manual directo)
                logger.warning(
                    f"🛡️ [WATCHDOG] El slot {slot_id} ({trade.ticket_id}) ya no existe en el broker. "
                    f"Liberando slot y sincronizando cierre en base de datos..."
                )
                tick = await self.broker.get_current_tick(trade.symbol)
                px = tick.bid if trade.side == OrderSide.BUY else tick.ask
                try:
                    await self.state_machine._close_slot(
                        slot_id,
                        close_price=px,
                        status=TradeStatus.CLOSED_SL,
                        reason="BROKER_RECONCILE_CLOSED"
                    )
                    await dispatch_telegram_alert("SYSTEM_INFO", {
                        "text": f"ℹ️ *[WATCHDOG]* Slot {slot_id} ({trade.symbol} {trade.side.value}) liberado automáticamente tras confirmación de cierre en broker."
                    })
                except Exception as close_err:
                    logger.error(f"[WATCHDOG] Error al cerrar slot huérfano {slot_id}: {close_err}")

        # 3. Auditar si hay posiciones vivas en cTrader que NO están en ningún slot del bot (Huérfanas / Fantasmas)
        current_orphan_ids = set()
        for pos_id, b_pos in broker_pos_by_id.items():
            is_managed = False
            for trade in active_slots.values():
                t_clean = str(trade.ticket_id).replace("CTR-", "").replace("TKT-", "").strip()
                if t_clean == pos_id or str(trade.ticket_id) == pos_id:
                    is_managed = True
                    break

            if not is_managed:
                current_orphan_ids.add(pos_id)
                if pos_id not in self._last_notified_orphans:
                    logger.critical(
                        f"🚨 [WATCHDOG CRÍTICO] Posición HUÉRFANA detectada en cTrader sin supervisión del bot: "
                        f"Pos ID: {pos_id} | {b_pos.side.value} {b_pos.lot_size}L @ {b_pos.entry_price} | SL={b_pos.sl}"
                    )
                    try:
                        await dispatch_telegram_alert("SYSTEM_INFO", {
                            "text": (
                                f"🚨 *[ALERTA DE SEGURIDAD: POSICIÓN HUÉRFANA EN CTRADER]*\n"
                                f"══════════════════════════════════════\n"
                                f"• *ID Posición:* `{pos_id}`\n"
                                f"• *Operación:* `{b_pos.side.value} {b_pos.lot_size} Lotes`\n"
                                f"• *Precio Entrada:* `${b_pos.entry_price}`\n"
                                f"• *Stop Loss:* `${b_pos.sl or 'SIN SL'}`\n"
                                f"⚠️ _Esta posición existe en tu broker pero no está asignada a ningún slot activo del bot._"
                            )
                        })
                    except Exception:
                        pass

        self._last_notified_orphans = current_orphan_ids
