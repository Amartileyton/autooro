import pytest
import asyncio
import time
from decimal import Decimal
from backend.broker.paper import LocalPaperBroker
from backend.broker.base import BrokerTick
from backend.database.models import OrderSide, TradeStatus
from backend.risk.state_machine import TradeStateMachine, ActiveSlotTrade
from backend.config import settings

be_buf = getattr(settings, 'DEFAULT_BE_BUFFER_USD', Decimal("0.80"))


@pytest.mark.asyncio
async def test_tiered_buy_full_lifecycle():
    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # 1. Abrir orden BUY de 0.20 lotes @ 2000.00
    entry_price = Decimal("2000.00")
    initial_sl = Decimal("1990.00")
    tp_levels = [Decimal("2005.00"), Decimal("2015.00"), Decimal("2025.00")]

    trade = await sm.open_new_trade(
        slot_id=1,
        side=OrderSide.BUY,
        lot_size=Decimal("0.20"),
        entry_price=entry_price,
        sl=initial_sl,
        tp_levels=tp_levels
    )

    assert trade is not None
    assert trade.lot_size == Decimal("0.20")
    assert trade.initial_lot_size == Decimal("0.20")
    assert trade.current_sl == Decimal("1990.00")
    assert trade.status == TradeStatus.OPEN

    # 2. Enviar tick TP1 (2005.50 >= 2005.00)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("2005.50"), ask=Decimal("2005.70"), timestamp=time.time())
    await sm.on_market_tick(tick_tp1)

    assert trade.status == TradeStatus.TP1_HIT
    # Debe haber cerrado 50% (0.10L) y quedar 0.10L
    assert trade.lot_size == Decimal("0.10")
    # PnL cobrado en caja: (2005.50 - 2000.00) * 0.10 * 100 = $55.00
    assert trade.realized_cash_pnl == Decimal("55.00")
    # SL debe subir a Entrada + Spread Buffer ($2000.00 + be_buf)
    assert trade.current_sl == (Decimal("2000.00") + be_buf)

    # 3. Enviar tick TP2 (2015.50 >= 2015.00)
    tick_tp2 = BrokerTick(symbol="XAUUSD", bid=Decimal("2015.50"), ask=Decimal("2015.70"), timestamp=time.time())
    await sm.on_market_tick(tick_tp2)

    assert trade.status == TradeStatus.TP2_HIT
    # Debe haber cerrado 25% del total (0.05L) y quedar 0.05L de Runner
    assert trade.lot_size == Decimal("0.05")
    # PnL cobrado adicional: (2015.50 - 2000.00) * 0.05 * 100 = $77.50 ➔ Total = 55.00 + 77.50 = 132.50
    assert trade.realized_cash_pnl == Decimal("132.50")
    # SL del Runner debe subir al precio de TP1 ($2005.00)
    assert trade.current_sl == Decimal("2005.00")

    # 4. Enviar tick TP3 (2026.00 >= 2025.00) ➔ Activación de Infinite Runner
    tick_tp3 = BrokerTick(symbol="XAUUSD", bid=Decimal("2026.00"), ask=Decimal("2026.20"), timestamp=time.time())
    await sm.on_market_tick(tick_tp3)

    assert trade.status == TradeStatus.TP3_TRAILING
    assert trade.is_infinite_trailing is True
    assert trade.peak_price == Decimal("2026.00")
    # SL inicial en nivel TP3
    assert trade.current_sl == Decimal("2025.00")

    # 5. El oro explota a 2040.00 (+14.00 pips de nuevo pico)
    tick_surge = BrokerTick(symbol="XAUUSD", bid=Decimal("2040.00"), ask=Decimal("2040.20"), timestamp=time.time())
    await sm.on_market_tick(tick_surge)

    assert trade.peak_price == Decimal("2040.00")
    # Trailing SL debe situarse a 30 pips ($3.00) del pico: 2040.00 - 3.00 = 2037.00
    assert trade.current_sl == Decimal("2037.00")

    # 6. El oro retrocede y toca el Trailing SL (2036.50 <= 2037.00)
    tick_retrace = BrokerTick(symbol="XAUUSD", bid=Decimal("2036.50"), ask=Decimal("2036.70"), timestamp=time.time())
    await sm.on_market_tick(tick_retrace)

    # El slot debe haberse cerrado con beneficio acumulado total
    assert 1 not in sm.active_slots
    # Balance del broker debe haber incrementado considerablemente
    acc = await broker.get_account_info()
    assert acc.balance > settings.INITIAL_PAPER_BALANCE


@pytest.mark.asyncio
async def test_tiered_sell_full_lifecycle():
    broker = LocalPaperBroker()
    sm = TradeStateMachine(broker=broker)

    # 1. Abrir orden SELL de 0.20 lotes @ 2000.00
    entry_price = Decimal("2000.00")
    initial_sl = Decimal("2010.00")
    tp_levels = [Decimal("1995.00"), Decimal("1985.00"), Decimal("1975.00")]

    trade = await sm.open_new_trade(
        slot_id=2,
        side=OrderSide.SELL,
        lot_size=Decimal("0.20"),
        entry_price=entry_price,
        sl=initial_sl,
        tp_levels=tp_levels
    )

    assert trade is not None
    assert trade.status == TradeStatus.OPEN

    # 2. TP1 SELL (1994.50 <= 1995.00)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("1994.30"), ask=Decimal("1994.50"), timestamp=time.time())
    await sm.on_market_tick(tick_tp1)

    assert trade.status == TradeStatus.TP1_HIT
    assert trade.lot_size == Decimal("0.10")
    # SL SELL sube a Entrada - Spread Buffer ($2000.00 - be_buf)
    assert trade.current_sl == (Decimal("2000.00") - be_buf)
    assert trade.realized_cash_pnl > Decimal("0.00")

    # 3. TP2 SELL (1984.50 <= 1985.00)
    tick_tp2 = BrokerTick(symbol="XAUUSD", bid=Decimal("1984.30"), ask=Decimal("1984.50"), timestamp=time.time())
    await sm.on_market_tick(tick_tp2)

    assert trade.status == TradeStatus.TP2_HIT
    assert trade.lot_size == Decimal("0.05")
    # SL SELL del Runner se bloquea en TP1 ($1995.00)
    assert trade.current_sl == Decimal("1995.00")

    # 4. TP3 SELL (1974.00 <= 1975.00) ➔ Infinite Runner
    tick_tp3 = BrokerTick(symbol="XAUUSD", bid=Decimal("1973.80"), ask=Decimal("1974.00"), timestamp=time.time())
    await sm.on_market_tick(tick_tp3)

    assert trade.status == TradeStatus.TP3_TRAILING
    assert trade.is_infinite_trailing is True
    assert trade.current_sl == Decimal("1975.00")

    # 5. El oro cae aún más a 1960.00 (Nuevo fondo para SELL)
    tick_drop = BrokerTick(symbol="XAUUSD", bid=Decimal("1959.80"), ask=Decimal("1960.00"), timestamp=time.time())
    await sm.on_market_tick(tick_drop)

    assert trade.peak_price == Decimal("1960.00")
    # Trailing SL SELL debe situarse a 30 pips ($3.00) por encima del fondo: 1960.00 + 3.00 = 1963.00
    assert trade.current_sl == Decimal("1963.00")

    # 6. El oro rebota y toca el Trailing SL SELL (1963.50 >= 1963.00)
    tick_bounce = BrokerTick(symbol="XAUUSD", bid=Decimal("1963.30"), ask=Decimal("1963.50"), timestamp=time.time())
    await sm.on_market_tick(tick_bounce)

    assert 2 not in sm.active_slots
    acc = await broker.get_account_info()
    assert acc.balance > settings.INITIAL_PAPER_BALANCE
