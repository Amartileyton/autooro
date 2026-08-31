"""Repositorio de operaciones (tabla ``trades``).

Centraliza las mutaciones inline sobre ``Trade`` que estaban dispersas en
``risk/state_machine.py``.
"""
from sqlalchemy import update

from backend.database.models import Trade
from backend.database.session import AsyncSessionLocal


async def update_trade(ticket_id: str, **values) -> None:
    """Actualiza columnas de una operación localizada por ``ticket_id``.

    Las excepciones se propagan al llamador para que mantenga su propio logging
    contextual (comportamiento idéntico al código original).
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Trade)
            .where(Trade.ticket_id == ticket_id)
            .values(**values)
        )
        await session.execute(stmt)
        await session.commit()
