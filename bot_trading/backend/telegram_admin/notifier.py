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

    elif event_type == "SIGNAL_REJECTED":
        reason = data.get("reason", "FUERA PRECIO")
        entry = data.get("entry_price", 0.0)
        market = data.get("market_price", 0.0)
        diff = data.get("diff", 0.0)
        entry_str = f"${entry:.2f}" if entry else "N/A"
        market_str = f"${market:.2f}" if market else "N/A"
        diff_str = f"+${diff:.2f} USD" if diff else "N/A"
        return (
            "🚫 *ALERTA GOLD-EX: SEÑAL RECHAZADA (FUERA PRECIO)*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `🚫 NO EJECUTADA (PROTECCIÓN CAPITAL)`\n"
            f"• *Motivo:* `{reason}`\n"
            f"• *Precio Señal:* `{entry_str}`\n"
            f"• *Precio Mercado al llegar:* `{market_str}`\n"
            f"• *Desvío / Slippage:* `{diff_str}` (Tolerancia: `$2.00 USD`)\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "🛡️ _La orden no se ejecutó para proteger tu balance de deslizamientos negativos o entradas tardías._"
        )

    elif event_type == "SIGNAL_PENDING_PULLBACK":
        entry = data.get("entry_price", 0.0)
        market = data.get("market_price", 0.0)
        diff = data.get("diff", 0.0)
        timeout = data.get("timeout_minutes", 15)
        entry_str = f"${entry:.2f}" if entry else "N/A"
        market_str = f"${market:.2f}" if market else "N/A"
        diff_str = f"+${diff:.2f} USD" if diff else "N/A"
        return (
            "⏳ *ALERTA GOLD-EX: EN ESPERA DE RETROCESO (PULLBACK)*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `⏳ VIGILANDO RETROCESO EN MERCADO`\n"
            f"• *Precio Señal:* `{entry_str}`\n"
            f"• *Precio Mercado al llegar:* `{market_str}` (Desfase: `{diff_str}`)\n"
            f"• *Tiempo Límite:* `{timeout} min`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "🎯 _Si el precio retrocede a la zona segura se abrirá la orden. Si toca TP1 antes, se cancelará._"
        )

    elif event_type == "PULLBACK_EXPIRED":
        channel = data.get("channel", "Chartoro FX")
        reason = data.get("reason", "Timeout alcanzado sin retroceso")
        return (
            "⌛ *ALERTA GOLD-EX: VIGILANCIA EXPIRADA (FUERA PRECIO)*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `⌛ CANCELADA TRAS TIMEOUT`\n"
            f"• *Canal:* `{channel}`\n"
            f"• *Motivo:* `{reason}`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "ℹ️ _El precio no regresó a la zona de entrada durante el tiempo límite. Orden descartada._"
        )

    elif event_type == "PULLBACK_CANCELLED_TP":
        channel = data.get("channel", "Chartoro FX")
        tp1 = data.get("tp1", 0.0)
        return (
            "🎯 *ALERTA GOLD-EX: SEÑAL INVALIDADA POR TP1 (FUERA PRECIO)*\n"
            "══════════════════════════════════════\n"
            "• *Estado:* `🚫 CANCELADA (OBJETIVO TOCADO DIRECTO)`\n"
            f"• *Canal:* `{channel}`\n"
            f"• *TP1 Alcanzado:* `${tp1:.2f}`\n"
            f"• *Hora (Madrid):* `{now_str}`\n"
            "──────────────────────────────────────\n"
            "ℹ️ _El mercado alcanzó el objetivo sin retroceder a la zona de entrada. Orden descartada por seguridad._"
        )

    elif event_type == "ORDER_OPENED":
        ticket = data.get("ticket_id", "")
        side = data.get("side", "")
        entry = data.get("entry_price", 0.0)
        lot = data.get("lot_size", 0.0)
        sl = data.get("sl", 0.0)
        return (
            f"🚀 *ALERTA GOLD-EX: ORDEN EJECUTADA ({side} XAUUSD)*\n"
            "══════════════════════════════════════\n"
            f"• *Ticket:* `{ticket}`\n"
            f"• *Entrada Ejecutada:* `${entry:.2f}`\n"
            f"• *Volumen:* `{lot} Lotes`\n"
            f"• *Stop Loss:* `${sl:.2f}`\n"
            f"• *Hora (Madrid):* `{now_str}`"
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
