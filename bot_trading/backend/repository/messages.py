"""Repositorio de mensajes crudos de Telegram (tabla ``raw_telegram_messages``).

Centraliza las mutaciones inline sobre ``RawTelegramMessage`` que estaban
dispersas en ``main.py`` y ``risk/pullback_watcher.py``.
"""
from typing import Optional

from sqlalchemy import update

from backend.database.models import RawTelegramMessage
from backend.database.session import AsyncSessionLocal


async def update_message_error_reason(message_id: int, reason: Optional[str]) -> None:
    """Actualiza (o limpia, si ``reason`` es None) el ``error_reason`` de un mensaje.

    Las excepciones se propagan al llamador para que mantenga su propio logging
    contextual (comportamiento idéntico al código original).
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            update(RawTelegramMessage)
            .where(RawTelegramMessage.message_id == message_id)
            .values(error_reason=reason)
        )
        await session.execute(stmt)
        await session.commit()
