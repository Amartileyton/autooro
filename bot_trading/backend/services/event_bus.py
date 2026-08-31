"""Event Bus centralizado: despacho de eventos de trading a WebSocket y Telegram.

Centraliza el patrón que antes vivía inline en ``main.on_state_machine_alert``.
Cada canal se despacha de forma independiente: un fallo en uno no interrumpe al
otro (los errores se registran y no se propagan).
"""
import logging

logger = logging.getLogger("trading_bot.event_bus")


async def publish_trade_event(event_type: str, data: dict) -> None:
    """Despacha un evento de trading al WebSocket y al notificador de Telegram.

    Args:
        event_type: Tipo de evento (ej. ``ORDER_OPENED``, ``SIGNAL_REJECTED``).
        data: Carga útil del evento, serializada tal cual a cada canal.
    """
    # 1. WebSocket (dashboard institucional en tiempo real)
    try:
        from backend.api.ws import manager
        await manager.broadcast({
            "type": "TRADE_EVENT",
            "event": event_type,
            "data": data,
        })
    except Exception as ws_err:
        logger.debug(f"Aviso al emitir WebSocket del evento '{event_type}': {ws_err}")

    # 2. Notificador de Telegram (Bot Aiogram + cliente Telethon MTProto)
    try:
        from backend.telegram_admin.notifier import dispatch_telegram_alert
        await dispatch_telegram_alert(event_type, data)
    except Exception as notif_err:
        logger.debug(f"Aviso al despachar alerta Telegram '{event_type}': {notif_err}")
