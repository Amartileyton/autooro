import pytest
from decimal import Decimal
from datetime import datetime, timezone
from backend.database.session import engine, AsyncSessionLocal
from backend.database.models import Trade, TradeStatus, OrderSide, Base
from backend.database.reconciliation import run_startup_reconciliation
from backend.broker.paper import LocalPaperBroker
from backend.risk.state_machine import TradeStateMachine
from sqlalchemy import select


@pytest.mark.asyncio
async def test_reconciliation_post_reboot_rules():
    # Inicializar base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # Insertar 3 órdenes en DB:
    # 1) Trade 1: Entrada 2340, TP1=2350, TP2=2360. Mercado estará en 2365 -> Debe restaurar en TP2_HIT
    # 2) Trade 2: Entrada 2340, TP1=2350, TP2=2360. Mercado estará en 2355 -> Debe restaurar en TP1_HIT
    # 3) Trade 3: Entrada 2340, TP1=2350, TP2=2360. Mercado estará en 2342 -> SIN HITOS -> Debe CERRARSE INMEDIATAMENTE
    async with AsyncSessionLocal() as session:
        t1 = Trade(
            ticket_id="TKT-REC-01",
            slot_id=1,
            symbol="XAUUSD",
            side=OrderSide.BUY,
            status=TradeStatus.OPEN,
            entry_price=Decimal("2340.00"),
            current_sl=Decimal("2330.00"),
            initial_sl=Decimal("2330.00"),
            tp1=Decimal("2350.00"),
            tp2=Decimal("2360.00"),
            tp3=Decimal("2370.00"),
            lot_size=Decimal("0.50"),
            open_time=datetime.now(timezone.utc)
        )
        t2 = Trade(
            ticket_id="TKT-REC-02",
            slot_id=2,
            symbol="XAUUSD",
            side=OrderSide.BUY,
            status=TradeStatus.OPEN,
            entry_price=Decimal("2340.00"),
            current_sl=Decimal("2330.00"),
            initial_sl=Decimal("2330.00"),
            tp1=Decimal("2350.00"),
            tp2=Decimal("2360.00"),
            tp3=Decimal("2370.00"),
            lot_size=Decimal("0.50"),
            open_time=datetime.now(timezone.utc)
        )
        t3 = Trade(
            ticket_id="TKT-REC-03",
            slot_id=3,
            symbol="XAUUSD",
            side=OrderSide.BUY,
            status=TradeStatus.OPEN,
            entry_price=Decimal("2340.00"),
            current_sl=Decimal("2330.00"),
            initial_sl=Decimal("2330.00"),
            tp1=Decimal("2350.00"),
            tp2=Decimal("2360.00"),
            tp3=Decimal("2370.00"),
            lot_size=Decimal("0.50"),
            open_time=datetime.now(timezone.utc)
        )
        session.add_all([t1, t2, t3])
        await session.commit()

    # Ejecutamos reconciliación para Trade 3 con precio de mercado en 2342 (no alcanzó TP1)
    broker._current_bid = Decimal("2342.00")
    broker._current_ask = Decimal("2342.20")

    await run_startup_reconciliation(broker=broker, state_machine=sm)

    # Verificar estados en DB
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Trade).where(Trade.ticket_id == "TKT-REC-03"))
        t3_updated = res.scalar_one()
        # Debe haberse cerrado por la regla estricta sin hitos
        assert t3_updated.status == TradeStatus.CLOSED_REBOOT_NO_MILESTONE
        assert t3_updated.close_reason == "REBOOT_NO_MILESTONE_EMERGENCY_CLOSE"
        # Slot 3 debe estar libre en memoria
        assert 3 not in sm.active_slots
