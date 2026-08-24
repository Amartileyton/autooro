import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Dict, Any

logger = logging.getLogger("trading_bot.notifier")


def get_madrid_time_str() -> str:
    """Obtiene la hora actual en zona horaria de España (Europe/Madrid)."""
    try:
        return datetime.now(ZoneInfo("Europe/Madrid")).strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def build_alert_message(event_type: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Construye el texto formateado en Markdown para la notificación de Telegram."""
    data = data or {}
    now_str = get_madrid_time_str()

    if event_type in ("EMERGENCY_SHUTDOWN", "KILL_SWITCH"):
        reason = data.get("reason", "KILL SWITCH (MÓVIL / DASHBOARD)")
        closed_count = data.get("closed_count", 0)
        return (
            "🚨 *ALERTA GOLD-EX: APAGADO GENERAL (KILL SWITCH)*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `🔴 BOT DETENIDO Y PAUSADO`\n"
            f"• *Motivo:* `{reason}`\n"
            f"• *Posiciones Cerradas:* `{closed_count}`\n"
            "• *Ingesta Telegram:* `🔴 PAUSADA`\n"
            "• *Auto-Ejecución:* `🔴 DESACTIVADA`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "⚠️ _Todas las posiciones han sido cerradas a mercado. El bot no abrirá operaciones hasta ser rearmado._"
        )

    elif event_type in ("BOT_REARMED", "REARM"):
        reason = data.get("reason", "REARME DESDE TERMINAL / MÓVIL")
        return (
            "🟢 *ALERTA GOLD-EX: SISTEMA REENCENDIDO Y REARMADO*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `🟢 BOT EN VIVO Y ACTIVO`\n"
            f"• *Acción:* `{reason}`\n"
            "• *Ingesta Telegram:* `🟢 ESCUCHANDO SEÑALES`\n"
            "• *Auto-Ejecución:* `🟢 HABILITADA`\n"
            "• *Slots Disponibles:* `4 / 4` (100% Margen Libre)\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "⚡ _El sistema está listo y operará de forma autónoma ante nuevas señales._"
        )

    elif event_type == "INGESTION_PAUSED":
        return (
            "⏸️ *ALERTA GOLD-EX: INGESTA DE SEÑALES PAUSADA*\n"
            "══════════════════════════════════════\n"
            "• *Ingesta Telegram:* `⏸️ PAUSADA`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "ℹ️ _Los mensajes recibidos en el canal serán ignorados._"
        )

    elif event_type == "INGESTION_RESUMED":
        return (
            "▶️ *ALERTA GOLD-EX: INGESTA DE SEÑALES REANUDADA*\n"
            "══════════════════════════════════════\n"
            "• *Ingesta Telegram:* `🟢 ACTIVA`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "ℹ️ _El bot vuelve a procesar las señales del canal._"
        )

    return f"🔔 *ALERTA GOLD-EX:* `{event_type}` | {now_str}"


async def dispatch_telegram_alert(event_type: str, data: Optional[Dict[str, Any]] = None):
    """
    Envía notificaciones push de sistema por Telegram.
    Intenta enviar por el Bot Administrativo (Aiogram) y por el cliente MTProto (Telethon).
    """
    from backend.main import app_state
    from backend.config import settings

    msg = build_alert_message(event_type, data)
    sent_any = False

    # 1. Enviar vía Bot Administrativo de Aiogram (si está configurado)
    telegram_bot = app_state.get("telegram_bot")
    if telegram_bot and telegram_bot.bot and settings.ADMIN_TELEGRAM_USER_ID:
        try:
            await telegram_bot._safe_send_message(settings.ADMIN_TELEGRAM_USER_ID, msg)
            sent_any = True
            logger.info(f"[NOTIFIER] Alerta '{event_type}' enviada por Bot de Telegram al admin.")
        except Exception as e:
            logger.warning(f"[NOTIFIER] Error enviando por bot aiogram: {e}")

    # 2. Enviar vía Cliente Telethon MTProto a 'me' (Mensajes Guardados) o al admin
    telegram_client = app_state.get("telegram_client")
    if telegram_client and telegram_client.client and telegram_client._is_running:
        try:
            target = settings.ADMIN_TELEGRAM_USER_ID if settings.ADMIN_TELEGRAM_USER_ID else "me"
            await telegram_client.client.send_message(target, msg, parse_mode="md")
            sent_any = True
            logger.info(f"[NOTIFIER] Alerta '{event_type}' enviada vía Telethon MTProto a '{target}'.")
        except Exception as e:
            logger.debug(f"[NOTIFIER] No se pudo enviar por Telethon: {e}")

    if not sent_any:
        logger.info(f"[NOTIFIER] Alerta '{event_type}' generada localmente: {msg.splitlines()[0]}")
