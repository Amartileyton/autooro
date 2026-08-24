import asyncio
import logging
from decimal import Decimal
from typing import Optional, Any, Dict, List
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from backend.config import settings
from backend.risk.state_machine import TradeStateMachine
from backend.broker.base import BaseBrokerAdapter

logger = logging.getLogger("trading_bot.telegram_admin")


class TelegramAdminBot:
    """
    Bot Privado de Control y Auditoría en Telegram (Aiogram 3.x).
    Exclusivo para el ADMIN_TELEGRAM_USER_ID.
    Envía alertas en tiempo real de aperturas, trailing SL, PnL y ofrece comandos de gestión.
    """

    def __init__(self, state_machine: TradeStateMachine, broker: BaseBrokerAdapter):
        self.state_machine = state_machine
        self.broker = broker
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self._polling_task: Optional[asyncio.Task] = None
        self.admin_id = settings.ADMIN_TELEGRAM_USER_ID

    async def start(self):
        """Inicializa el bot y arranca el polling en segundo plano."""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN no configurado. Bot Admin deshabilitado.")
            return

        self.bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )
        self.dp = Dispatcher()

        # Registrar handlers
        self._register_handlers()

        # Registrar callback en la State Machine para recibir eventos
        self.state_machine.register_alert_callback(self.send_system_alert)

        # Iniciar polling en background task
        self._polling_task = asyncio.create_task(self.dp.start_polling(self.bot))
        logger.info(f"Bot Admin de Telegram iniciado para Admin ID: {self.admin_id}")

        # Mensaje de arranque al admin
        if self.admin_id:
            await self._safe_send_message(
                self.admin_id,
                "🤖 *GOLD-EX TERMINAL INICIADO*\n"
                "═══════════════════════\n"
                "• *Activo:* XAUUSD (Gold)\n"
                f"• *Broker:* `{settings.BROKER_TYPE.upper()}`\n"
                f"• *Slots de Capital:* 4 (25% c/u)\n"
                f"• *Ingesta:* `{'ACTIVA' if settings.INGESTION_ENABLED else 'PAUSADA'}`\n\n"
                "Usa `/status` para consultar la matriz de slots."
            )

    async def stop(self):
        """Detiene el bot de forma limpia."""
        if self._polling_task:
            self._polling_task.cancel()
            try:
                await self._polling_task
            except asyncio.CancelledError:
                pass
        if self.bot:
            await self.bot.session.close()
        logger.info("Bot Admin de Telegram detenido.")

    def _is_admin(self, message: types.Message) -> bool:
        """Middleware de seguridad: Solo permite acceso al administrador configurado."""
        return self.admin_id == 0 or message.from_user.id == self.admin_id

    def _register_handlers(self):
        """Registra los comandos administrativos del bot."""

        @self.dp.message(Command("start", "help"))
        async def cmd_start(message: types.Message):
            if not self._is_admin(message):
                await message.reply("⛔ Acceso Denegado. Este es un bot privado institucional.")
                return

            text = (
                "⚡ *COMANDOS DISPONIBLES — GOLD-EX TERMINAL*\n"
                "════════════════════════════════\n"
                "📊 `/status` — Telemetría, balance y estado de los 4 slots\n"
                "🎯 `/slots` — Detalle individual de operaciones vivas\n"
                "⏸️ `/pause` — Pausar ingesta de nuevas señales\n"
                "▶️ `/resume` — Reanudar ingesta de señales\n"
                "🚨 `/kill` — Panic Stop: Cierra todo inmediatamente\n"
            )
            await message.reply(text)

        @self.dp.message(Command("status"))
        async def cmd_status(message: types.Message):
            if not self._is_admin(message):
                return

            acc = await self.broker.get_account_info()
            tick = await self.broker.get_current_tick("XAUUSD")
            active_count = len(self.state_machine.active_slots)

            slots_preview = []
            for slot_id in range(1, settings.MAX_CONCURRENT_SLOTS + 1):
                if slot_id in self.state_machine.active_slots:
                    t = self.state_machine.active_slots[slot_id]
                    pnl_sign = "+" if t.current_pnl >= Decimal("0.00") else ""
                    slots_preview.append(
                        f"• *Slot {slot_id}:* `{t.side.value}` {t.lot_size}L @ {t.entry_price:.2f} "
                        f"| SL: `{t.current_sl:.2f}` | PnL: `{pnl_sign}${t.current_pnl:.2f}` ({t.status.value})"
                    )
                else:
                    slots_preview.append(f"• *Slot {slot_id}:* `DISPONIBLE` ⚪")

            text = (
                "📊 *TELEMETRÍA GLOBAL DE TRADING*\n"
                "════════════════════════════════\n"
                f"• *XAUUSD Spot:* `${tick.bid:.2f}` / `${tick.ask:.2f}`\n"
                f"• *Balance:* `${acc.balance:.2f} USD`\n"
                f"• *Equidad:* `${acc.equity:.2f} USD`\n"
                f"• *Margen Libre:* `${acc.free_margin:.2f} USD`\n"
                f"• *Slots Ocupados:* `{active_count} / {settings.MAX_CONCURRENT_SLOTS}`\n"
                f"• *Ingesta:* `{'🟢 ACTIVA' if settings.INGESTION_ENABLED else '⏸️ PAUSADA'}`\n"
                "────────────────────────────────\n"
                "*Matriz de Slots:*\n" + "\n".join(slots_preview)
            )
            await message.reply(text)

        @self.dp.message(Command("slots"))
        async def cmd_slots(message: types.Message):
            if not self._is_admin(message):
                return

            if not self.state_machine.active_slots:
                await message.reply("⚪ No hay posiciones activas en este momento. Todos los slots están disponibles.")
                return

            lines = ["🎯 *DETALLE DE POSICIONES ACTIVAS:*"]
            for slot_id, t in self.state_machine.active_slots.items():
                pnl_sign = "+" if t.current_pnl >= Decimal("0.00") else ""
                lines.append(
                    f"\n🔹 *SLOT #{slot_id}* (`{t.ticket_id}`)\n"
                    f"• Tipo: `{t.side.value}` | Lote: `{t.lot_size}`\n"
                    f"• Entrada: `{t.entry_price:.2f}` | Actual: `{t.current_price:.2f}`\n"
                    f"• SL Actual: `{t.current_sl:.2f}` (Inicial: `{t.initial_sl:.2f}`)\n"
                    f"• TP1: `{t.tp1:.2f}` | TP2: `{t.tp2 or '-'}` | TP3: `{t.tp3 or '-'}`\n"
                    f"• PnL Flotante: `{pnl_sign}${t.current_pnl:.2f} USD`\n"
                    f"• Estado: `{t.status.value}`"
                )
            await message.reply("\n".join(lines))

        @self.dp.message(Command("pause"))
        async def cmd_pause(message: types.Message):
            if not self._is_admin(message):
                return
            settings.INGESTION_ENABLED = False
            await message.reply("⏸️ *INGESTA PAUSADA:* No se ejecutarán nuevas señales entrantes.")

        @self.dp.message(Command("resume"))
        async def cmd_resume(message: types.Message):
            if not self._is_admin(message):
                return
            settings.INGESTION_ENABLED = True
            await message.reply("▶️ *INGESTA REANUDADA:* El sistema procesará nuevas señales entrantes.")

        @self.dp.message(Command("kill"))
        async def cmd_kill(message: types.Message):
            if not self._is_admin(message):
                return
            await message.reply("🚨 *EJECUTANDO KILL-SWITCH:* Cerrando todas las operaciones a mercado de inmediato...")
            await self.state_machine.panic_close_all(reason="TELEGRAM_ADMIN_KILL_COMMAND")
            settings.INGESTION_ENABLED = False
            await message.reply("✅ Todas las posiciones han sido liquidadas. Ingesta pausada.")

    async def send_system_alert(self, event_type: str, data: dict):
        """Envía notificaciones push al administrador según los eventos de trading."""
        if not self.bot or not self.admin_id:
            return

        text = ""
        if event_type == "ORDER_OPENED":
            text = (
                "🟢 *NUEVA ORDEN EJECUTADA*\n"
                "═══════════════════════\n"
                f"• *Slot:* `#{data.get('slot_id')}`\n"
                f"• *Ticket:* `{data.get('ticket_id')}`\n"
                f"• *Operación:* `{data.get('side')}` `{data.get('lot_size')} lotes`\n"
                f"• *Precio Entrada:* `${data.get('entry_price'):.2f}`\n"
                f"• *Stop Loss:* `${data.get('sl'):.2f}`\n"
                f"• *TP1:* `${data.get('tp1'):.2f}` | *TP2:* `${data.get('tp2') or '-'}` | *TP3:* `${data.get('tp3') or '-'}`"
            )
        elif event_type == "TP1_HIT":
            text = (
                "🛡️ *HITO TP1 ALCANZADO — TRAILING SL*\n"
                "════════════════════════════════\n"
                f"• *Slot:* `#{data.get('slot_id')}` (`{data.get('ticket_id')}`)\n"
                f"• *Precio Mercado:* `${data.get('market_price'):.2f}`\n"
                f"• *Nuevo Stop Loss:* `${data.get('new_sl'):.2f}` (Break-Even asegurado) 🔒"
            )
        elif event_type == "TP2_HIT":
            text = (
                "🚀 *HITO TP2 ALCANZADO — TRAILING SL*\n"
                "════════════════════════════════\n"
                f"• *Slot:* `#{data.get('slot_id')}` (`{data.get('ticket_id')}`)\n"
                f"• *Precio Mercado:* `${data.get('market_price'):.2f}`\n"
                f"• *Nuevo Stop Loss:* `${data.get('new_sl'):.2f}` (Beneficio asegurado en TP2) 💰"
            )
        elif event_type == "ORDER_CLOSED":
            pnl = data.get('pnl', 0.0)
            pnl_emoji = "💰" if pnl >= 0 else "🛑"
            text = (
                f"{pnl_emoji} *POSICIÓN CERRADA*\n"
                "═══════════════════════\n"
                f"• *Slot:* `#{data.get('slot_id')}` (`{data.get('ticket_id')}`)\n"
                f"• *Estado Final:* `{data.get('status')}`\n"
                f"• *Precio Cierre:* `${data.get('close_price'):.2f}`\n"
                f"• *PnL Neto:* `{'+' if pnl >= 0 else ''}${pnl:.2f} USD`\n"
                f"• *Motivo:* `{data.get('reason')}`"
            )
        elif event_type in ("EMERGENCY_SHUTDOWN", "KILL_SWITCH"):
            text = (
                "🚨 *ALERTA GOLD-EX: APAGADO GENERAL (KILL SWITCH)*\n"
                "══════════════════════════════════════\n"
                "• *Estado:* `🔴 BOT DETENIDO Y PAUSADO`\n"
                f"• *Motivo:* `{data.get('reason', 'KILL SWITCH')}`\n"
                f"• *Posiciones Cerradas:* `{data.get('closed_count', 0)}`\n"
                "• *Ingesta Telegram:* `🔴 PAUSADA`\n"
                "• *Auto-Ejecución:* `🔴 DESACTIVADA`\n"
                "──────────────────────────────────────\n"
                "⚠️ _Todas las posiciones han sido cerradas a mercado._"
            )
        elif event_type in ("BOT_REARMED", "REARM"):
            text = (
                "🟢 *ALERTA GOLD-EX: SISTEMA REENCENDIDO Y REARMADO*\n"
                "══════════════════════════════════════\n"
                "• *Estado:* `🟢 BOT EN VIVO Y ACTIVO`\n"
                f"• *Acción:* `{data.get('reason', 'REARME DE SISTEMA')}`\n"
                "• *Ingesta Telegram:* `🟢 ESCUCHANDO SEÑALES`\n"
                "• *Auto-Ejecución:* `🟢 HABILITADA`\n"
                "• *Slots Disponibles:* `4 / 4` (100% Margen Libre)\n"
                "──────────────────────────────────────\n"
                "⚡ _El sistema operará normalmente ante cualquier nueva señal._"
            )
        elif event_type == "CRITICAL_ERROR":
            text = f"🚨 *ALERTA CRÍTICA:* `{data.get('message')}`"

        if text:
            await self._safe_send_message(self.admin_id, text)

    async def _safe_send_message(self, chat_id: int, text: str):
        """Envío seguro con captura de excepciones para no interrumpir el flujo."""
        try:
            if self.bot:
                await self.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logger.error(f"Error al enviar mensaje de Telegram a {chat_id}: {e}")
