import pytest
import asyncio
import time
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from backend.ingesta.schemas import TradingSignalEvent, OrderSide, ParserType
from backend.broker.base import BrokerTick
from backend.broker.paper import LocalPaperBroker
from backend.risk.engine import RiskEngine
from backend.risk.state_machine import TradeStateMachine
from backend.risk.pullback_watcher import PullbackWatcher, PendingSignal


@pytest.mark.asyncio
async def test_pullback_watcher_triggers_on_retracement():
    broker = LocalPaperBroker()
    await broker.connect()
    # Poner precio inicial en 4604.50 (fuera de rango para entrada 4600-4602)
    broker._current_price = Decimal("4604.50")

    risk = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)
    watcher = PullbackWatcher(risk_engine=risk, state_machine=state_machine, broker=broker)

    event = TradingSignalEvent(
        asset="XAUUSD",
        side=OrderSide.BUY,
        entry_price=Decimal("4601.00"),
        sl_price=Decimal("4593.00"),
        tp_levels=[Decimal("4608.00"), Decimal("4614.00")],
        parser_type=ParserType.REGEX,
        raw_text="BUY 4600-4602",
        message_id=9001,
        channel_name="XAU(USD) GREEN PIPS"
    )

    # 1. Registrar señal desfasada (Entrada 4600-4602 vs Mercado 4604.50)
    added = await watcher.add_signal(event, entry_min=Decimal("4600.00"), entry_max=Decimal("4602.00"))
    assert added is True
    assert 9001 in watcher.pending_signals
    assert watcher.pending_signals[9001].status == "WATCHING"

    # 2. Tick intermedio que sigue fuera de rango (4603.50 -> diff = 1.50 desde 4602)
    # diff = 4603.50 - 4602.00 = 1.50 <= 2.00 -> ¡En este tick ya está dentro de tolerancia de 2.00!
    # Probemos con un tick a 4605.00 primero (fuera)
    tick_fuera = BrokerTick(
        symbol="XAUUSD",
        bid=Decimal("4604.80"),
        ask=Decimal("4605.00"),
        timestamp=time.time()
    )
    await watcher.on_market_tick(tick_fuera)
    assert 9001 in watcher.pending_signals  # Aún en espera

    # 3. Tick que retrocede a la zona de entrada (Ask = 4601.50, diff = 0.00)
    tick_pullback = BrokerTick(
        symbol="XAUUSD",
        bid=Decimal("4601.30"),
        ask=Decimal("4601.50"),
        timestamp=time.time()
    )
    await watcher.on_market_tick(tick_pullback)

    # Debe haberse ejecutado y eliminado de las pendientes
    assert 9001 not in watcher.pending_signals
    assert len(state_machine.active_slots) == 1
    active_trade = list(state_machine.active_slots.values())[0]
    assert active_trade.side == OrderSide.BUY
    assert active_trade.entry_price == Decimal("4601.50")


@pytest.mark.asyncio
async def test_pullback_watcher_expires_after_timeout():
    broker = LocalPaperBroker()
    await broker.connect()
    broker._current_price = Decimal("4605.00")

    risk = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)
    watcher = PullbackWatcher(risk_engine=risk, state_machine=state_machine, broker=broker)

    event = TradingSignalEvent(
        asset="XAUUSD",
        side=OrderSide.BUY,
        entry_price=Decimal("4600.00"),
        sl_price=Decimal("4592.00"),
        tp_levels=[Decimal("4608.00")],
        parser_type=ParserType.REGEX,
        raw_text="BUY 4600",
        message_id=9002,
        channel_name="Chartoro FX"
    )

    await watcher.add_signal(event, entry_min=Decimal("4600.00"), entry_max=Decimal("4600.00"))
    assert 9002 in watcher.pending_signals

    # Forzar que el timeout_at sea en el pasado
    watcher.pending_signals[9002].timeout_at = datetime.now(timezone.utc) - timedelta(seconds=1)

    tick = BrokerTick(
        symbol="XAUUSD",
        bid=Decimal("4604.80"),
        ask=Decimal("4605.00"),
        timestamp=time.time()
    )
    await watcher.on_market_tick(tick)

    # Debe haber expirado
    assert 9002 not in watcher.pending_signals
    assert len(state_machine.active_slots) == 0


@pytest.mark.asyncio
async def test_pullback_watcher_cancels_if_tp1_reached():
    broker = LocalPaperBroker()
    await broker.connect()
    broker._current_price = Decimal("4604.00")

    risk = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)
    watcher = PullbackWatcher(risk_engine=risk, state_machine=state_machine, broker=broker)

    event = TradingSignalEvent(
        asset="XAUUSD",
        side=OrderSide.BUY,
        entry_price=Decimal("4600.00"),
        sl_price=Decimal("4592.00"),
        tp_levels=[Decimal("4608.00")],
        parser_type=ParserType.REGEX,
        raw_text="BUY 4600 TP 4608",
        message_id=9003,
        channel_name="Chartoro FX"
    )

    await watcher.add_signal(event, entry_min=Decimal("4600.00"), entry_max=Decimal("4600.00"))
    assert 9003 in watcher.pending_signals

    # El precio vuela directo a 4608.50 sin retroceder
    tick_tp = BrokerTick(
        symbol="XAUUSD",
        bid=Decimal("4608.50"),
        ask=Decimal("4608.70"),
        timestamp=time.time()
    )
    await watcher.on_market_tick(tick_tp)

    # Debe cancelarse por TP alcanzado sin haber retrocedido
    assert 9003 not in watcher.pending_signals
    assert len(state_machine.active_slots) == 0
