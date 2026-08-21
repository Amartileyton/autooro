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

    # 2. Tick alcanza TP1 (2350.50) -> Cierra 50% parcial y mueve SL a Break-Even + Spread (2340.30)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2350.50"), ask=Decimal("2350.70"), timestamp=1.0)
    await sm.on_market_tick(tick_tp1)

    assert sm.active_slots[1].status == TradeStatus.TP1_HIT
    assert sm.active_slots[1].current_sl == Decimal("2340.30")
    assert sm.active_slots[1].lot_size == Decimal("0.25")

    # 3. Tick alcanza TP2 (2361.00) -> Cierra 25% del total (0.13L) y SL debe moverse a TP1 (2350.00)
    tick_tp2 = BrokerTick(symbol="XAUUSD", bid=Decimal("2361.00"), ask=Decimal("2361.20"), timestamp=2.0)
    await sm.on_market_tick(tick_tp2)

    assert sm.active_slots[1].status == TradeStatus.TP2_HIT
    assert sm.active_slots[1].current_sl == Decimal("2350.00")
    assert sm.active_slots[1].lot_size == Decimal("0.13")

    # 4. Tick alcanza TP3 (2370.50) -> Activa Infinite Runner con SL inicial en TP3 (2370.00)
    tick_tp3 = BrokerTick(symbol="XAUUSD", bid=Decimal("2370.50"), ask=Decimal("2370.70"), timestamp=3.0)
    await sm.on_market_tick(tick_tp3)

    assert sm.active_slots[1].status == TradeStatus.TP3_TRAILING
    assert sm.active_slots[1].is_infinite_trailing is True
    assert sm.active_slots[1].current_sl == Decimal("2370.00")

    # 5. Tick sube a 2375.00 y luego retrocede por debajo del trailing SL (2372.00)
    tick_surge = BrokerTick(symbol="XAUUSD", bid=Decimal("2375.00"), ask=Decimal("2375.20"), timestamp=4.0)
    await sm.on_market_tick(tick_surge)
    assert sm.active_slots[1].current_sl == Decimal("2372.00")

    tick_retrace = BrokerTick(symbol="XAUUSD", bid=Decimal("2371.50"), ask=Decimal("2371.70"), timestamp=5.0)
    await sm.on_market_tick(tick_retrace)

    # El slot 1 debe quedar libre y cerrado
    assert 1 not in sm.active_slots
