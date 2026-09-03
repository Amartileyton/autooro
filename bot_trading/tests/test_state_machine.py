import pytest
from decimal import Decimal
from backend.risk.state_machine import TradeStateMachine
from backend.broker.paper import LocalPaperBroker
from backend.broker.base import BrokerTick
from backend.database.models import OrderSide, TradeStatus, Base
from backend.database.session import engine
from backend.config import settings

be_buffer = getattr(settings, 'DEFAULT_BE_BUFFER_USD', Decimal("0.80"))


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
    assert sm.active_slots[1].current_sl == (Decimal("2340.00") + be_buffer)
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


@pytest.mark.asyncio
async def test_pip_by_pip_tp1_partial_close_and_breakeven_buy():
    """
    Verifica que el bot monitorea tick a tick el mercado y, al tocar TP1 por precio
    (sin requerir ningún aviso de Telegram), vende el 50% y mueve el SL a Break-Even + Spread.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # Abrir BUY: Entrada 2650.00, SL inicial 2640.00, TP1 2653.00 (+30 pips), Lote 0.04
    trade = await sm.open_new_trade(
        slot_id=2,
        side=OrderSide.BUY,
        lot_size=Decimal("0.04"),
        entry_price=Decimal("2650.00"),
        sl=Decimal("2640.00"),
        tp_levels=[Decimal("2653.00"), Decimal("2660.00")]
    )

    assert trade.status == TradeStatus.OPEN
    assert trade.lot_size == Decimal("0.04")
    assert trade.current_sl == Decimal("2640.00")
    assert trade.realized_cash_pnl == Decimal("0.00")

    # Tick 1: Precio sube cerca pero no toca TP1 (2652.50)
    tick1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2652.50"), ask=Decimal("2652.70"), timestamp=10.0)
    await sm.on_market_tick(tick1)
    assert sm.active_slots[2].status == TradeStatus.OPEN
    assert sm.active_slots[2].lot_size == Decimal("0.04")

    # Tick 2: Precio TOCA TP1 (2653.00) -> COBRO 50% (0.02L) Y BLINDAJE SL (2650.30)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2653.00"), ask=Decimal("2653.20"), timestamp=11.0)
    await sm.on_market_tick(tick_tp1)

    active = sm.active_slots[2]
    assert active.status == TradeStatus.TP1_HIT
    assert active.lot_size == Decimal("0.02")  # 50% de 0.04
    # Ganancia asegurada en caja: (2653 - 2650) * 0.02 * 100 = 6.00 USD
    assert active.realized_cash_pnl == Decimal("6.00")
    # SL blindado a Break-Even + Spread (2650.00 + be_buffer)
    assert active.current_sl == (Decimal("2650.00") + be_buffer)

    # Tick 3: Precio retrocede hasta tocar el SL blindado
    tick_sl = BrokerTick(symbol="XAUUSD", bid=active.current_sl - Decimal("0.05"), ask=active.current_sl + Decimal("0.15"), timestamp=12.0)
    await sm.on_market_tick(tick_sl)

    # El trade debe cerrarse en positivo (CLOSED_TP) con beneficio total > 0
    assert 2 not in sm.active_slots


@pytest.mark.asyncio
async def test_pip_by_pip_tp1_partial_close_and_breakeven_sell():
    """
    Verifica el flujo completo de cobro de TP1 y blindaje para órdenes SELL.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # Abrir SELL: Entrada 2650.00, SL inicial 2660.00, TP1 2647.00 (-30 pips), Lote 0.02
    trade = await sm.open_new_trade(
        slot_id=3,
        side=OrderSide.SELL,
        lot_size=Decimal("0.02"),
        entry_price=Decimal("2650.00"),
        sl=Decimal("2660.00"),
        tp_levels=[Decimal("2647.00"), Decimal("2640.00")]
    )

    # Tick toca TP1 SELL (2647.00)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2646.80"), ask=Decimal("2647.00"), timestamp=20.0)
    await sm.on_market_tick(tick_tp1)

    active = sm.active_slots[3]
    assert active.status == TradeStatus.TP1_HIT
    assert active.lot_size == Decimal("0.01")  # 50% vendido
    # Ganancia asegurada en caja: (2650 - 2647) * 0.01 * 100 = 3.00 USD
    assert active.realized_cash_pnl == Decimal("3.00")
    # SL blindado SELL a Break-Even - Spread (2650.00 - be_buffer)
    assert active.current_sl == (Decimal("2650.00") - be_buffer)


@pytest.mark.asyncio
async def test_tp1_minimum_lot_moves_sl_without_splitting():
    """
    Verifica que con un lote mínimo indivisible (0.01), al tocar TP1 por precio,
    se mantiene el lote de 0.01 pero el Stop Loss se mueve obligatoriamente a Break-Even.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # Abrir BUY con 0.01L
    await sm.open_new_trade(
        slot_id=4,
        side=OrderSide.BUY,
        lot_size=Decimal("0.01"),
        entry_price=Decimal("2650.00"),
        sl=Decimal("2640.00"),
        tp_levels=[Decimal("2653.00")]
    )

    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2653.00"), ask=Decimal("2653.20"), timestamp=30.0)
    await sm.on_market_tick(tick_tp1)

    active = sm.active_slots[4]
    assert active.status == TradeStatus.TP1_HIT
    assert active.lot_size == Decimal("0.01")
    assert active.current_sl == (Decimal("2650.00") + be_buffer)
