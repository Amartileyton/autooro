import pytest
from decimal import Decimal
from backend.risk.state_machine import TradeStateMachine
from backend.broker.paper import LocalPaperBroker
from backend.broker.base import BrokerTick
from backend.database.models import OrderSide, TradeStatus, Base
from backend.database.session import engine


@pytest.mark.asyncio
async def test_full_trade_lifecycle_trailing_milestones():
    # Inicializar DB en memoria para el test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # 1. Abrir trade BUY en Slot 1
    # Entrada: 2340.00, SL: 2330.00, TP1: 2350.00, TP2: 2360.00, TP3: 2370.00
    trade = await sm.open_new_trade(
        slot_id=1,
        side=OrderSide.BUY,
        lot_size=Decimal("0.50"),
        entry_price=Decimal("2340.00"),
        sl=Decimal("2330.00"),
        tp_levels=[Decimal("2350.00"), Decimal("2360.00"), Decimal("2370.00")]
    )

    assert trade is not None
    assert 1 in sm.active_slots
    assert sm.active_slots[1].status == TradeStatus.OPEN
    assert sm.active_slots[1].current_sl == Decimal("2330.00")

    # 2. Tick alcanza TP1 (2350.50) -> SL debe moverse a TP1 (2350.00) y estado a TP1_HIT
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2350.50"), ask=Decimal("2350.70"), timestamp=1.0)
    await sm.on_market_tick(tick_tp1)

    assert sm.active_slots[1].status == TradeStatus.TP1_HIT
    assert sm.active_slots[1].current_sl == Decimal("2350.00")

    # 3. Tick alcanza TP2 (2361.00) -> SL debe moverse a TP2 (2360.00) y estado a TP2_HIT
    tick_tp2 = BrokerTick(symbol="XAUUSD", bid=Decimal("2361.00"), ask=Decimal("2361.20"), timestamp=2.0)
    await sm.on_market_tick(tick_tp2)

    assert sm.active_slots[1].status == TradeStatus.TP2_HIT
    assert sm.active_slots[1].current_sl == Decimal("2360.00")

    # 4. Tick alcanza TP3 (2370.50) -> Posición debe cerrarse completamente con CLOSED_TP
    tick_tp3 = BrokerTick(symbol="XAUUSD", bid=Decimal("2370.50"), ask=Decimal("2370.70"), timestamp=3.0)
    await sm.on_market_tick(tick_tp3)

    # El slot 1 debe quedar libre
    assert 1 not in sm.active_slots
