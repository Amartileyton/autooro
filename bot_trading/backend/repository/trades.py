"""Repositorio de operaciones (tabla ``trades``).

Centraliza las mutaciones inline sobre ``Trade`` que estaban dispersas en
``risk/state_machine.py``.
"""
from typing import Optional
from sqlalchemy import update

from backend.database.models import Trade
from backend.database.session import AsyncSessionLocal


async def update_trade(ticket_id: Optional[str] = None, trade_id: Optional[int] = None, **values) -> None:
    """Actualiza columnas de una operación localizada por ``trade_id`` (PK) o ``ticket_id``.

    Si se suministra ``trade_id``, se prioriza por ser la clave primaria inmutable.
    """
    if not trade_id and not ticket_id:
        return

    async with AsyncSessionLocal() as session:
        if trade_id:
            stmt = (
                update(Trade)
                .where(Trade.id == trade_id)
                .values(**values)
            )
        else:
            stmt = (
                update(Trade)
                .where(Trade.ticket_id == ticket_id)
                .values(**values)
            )
        await session.execute(stmt)
        await session.commit()


async def update_trade_ticket(trade_id: int, new_ticket_id: str) -> None:
    """Actualiza el ticket_id en base de datos cuando se resuelve un ticket sintético CTR-... a cTrader ID."""
    if not trade_id or not new_ticket_id:
        return
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Trade)
            .where(Trade.id == trade_id)
            .values(ticket_id=str(new_ticket_id))
        )
        await session.execute(stmt)
        await session.commit()

