import pytest
from decimal import Decimal
from backend.ingesta.parsers import parse_signal_by_channel
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType


def test_green_pips_buy_range():
    text = """
    🟢 GOLD BUY NOW: 2650.00 - 2652.00
    SL: 2642.00
    TP1: 2655.00
    TP2: 2660.00
    TP3: 2670.00
    TP4: 2680.00
    Proper risk management!
    """
    event = parse_signal_by_channel(text, message_id=301, channel_name="XAU(USD) GREEN PIPS")
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("2651.00")
    assert event.sl_price == Decimal("2642.00")
    assert len(event.tp_levels) == 4
    assert event.channel_name == "XAU(USD) GREEN PIPS"
    assert event.execution_mode == "AUDIT"


def test_green_pips_sell_explicit():
    text = """
    🔴 XAUUSD SELL @ 2675.50
    STOP LOSS: 2685.00
    TARGET 1: 2670.00
    TARGET 2: 2665.00
    TARGET 3: 2655.00
    """
    event = parse_signal_by_channel(text, message_id=302, channel_name="XAU(USD) GREEN PIPS")
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("2675.50")
    assert event.sl_price == Decimal("2685.00")
    assert len(event.tp_levels) == 3


def test_green_pips_modifiers():
    text_be = "MOVE SL TO BREAKEVEN FOR GOLD"
    event_be = parse_signal_by_channel(text_be, message_id=303, channel_name="XAU(USD) GREEN PIPS")
    assert isinstance(event_be, ModifierSignalEvent)
    assert event_be.signal_type == SignalType.MOVE_BE

    text_half = "CLOSE HALF NOW AND SECURE GAINS"
    event_half = parse_signal_by_channel(text_half, message_id=304, channel_name="XAU(USD) GREEN PIPS")
    assert isinstance(event_half, ModifierSignalEvent)
    assert event_half.signal_type == SignalType.CLOSE_ORDER
    assert event_half.close_percentage == Decimal("50.0")


def test_green_pips_slash_range_sop_loss_and_take_profit():
    """Valida la extracción exacta de señales con Sop Loss, rango con / y Take Profit 1..3."""
    text = """Pair (Gold vs USD)

 
Direction: BUY 
Entry : 4658 / 4660

✔️Take Profit 1 4663
✔️Take Profit 2 4666
✔️Take Profit 3 4670

😢Sop Loss 4652


🫣🔤Risk Management Is Important"""
    event = parse_signal_by_channel(text, message_id=305, channel_name="XAU(USD) GREEN PIPS")
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("4659.00")
    assert event.entry_min == Decimal("4658.00")
    assert event.entry_max == Decimal("4660.00")
    assert event.sl_price == Decimal("4652.00")
    assert event.requires_dynamic_sl is False
    assert event.tp_levels == [Decimal("4663.00"), Decimal("4666.00"), Decimal("4670.00")]
    assert event.channel_name == "XAU(USD) GREEN PIPS"


@pytest.mark.asyncio
async def test_safe_entry_range_slippage_check():
    from backend.broker.paper import LocalPaperBroker
    from backend.risk.engine import RiskEngine

    broker = LocalPaperBroker()
    broker._current_ask = Decimal("4659.00")  # Dentro de 4658 - 4660
    broker._current_bid = Decimal("4659.00")
    risk = RiskEngine(broker=broker)

    # 1. Precio dentro del rango seguro [4658, 4660] -> diff = 0.00
    is_ok, mkt_px, diff = await risk.check_slippage(
        signal_entry=Decimal("4659.00"),
        side=OrderSide.BUY,
        entry_min=Decimal("4658.00"),
        entry_max=Decimal("4660.00")
    )
    assert is_ok is True
    assert diff == Decimal("0.00")

    # 2. Precio ligeramente fuera por encima (4661.00 -> diff = 1.00 <= 2.00)
    broker._current_ask = Decimal("4661.00")
    broker._current_bid = Decimal("4661.00")
    is_ok, mkt_px, diff = await risk.check_slippage(
        signal_entry=Decimal("4659.00"),
        side=OrderSide.BUY,
        entry_min=Decimal("4658.00"),
        entry_max=Decimal("4660.00")
    )
    assert is_ok is True
    assert diff <= Decimal("2.00")

    # 3. Precio muy lejos (4665.00 -> diff = 5.00 > 2.00)
    broker._current_ask = Decimal("4665.00")
    broker._current_bid = Decimal("4665.00")
    is_ok, mkt_px, diff = await risk.check_slippage(
        signal_entry=Decimal("4659.00"),
        side=OrderSide.BUY,
        entry_min=Decimal("4658.00"),
        entry_max=Decimal("4660.00")
    )
    assert is_ok is False
    assert diff > Decimal("2.00")


@pytest.mark.asyncio
async def test_channels_performance_endpoint():
    from backend.database.session import AsyncSessionLocal
    from backend.api.routes import get_channels_performance

    async with AsyncSessionLocal() as session:
        result = await get_channels_performance(db=session)
        assert result["status"] == "success"
        assert result["channels_count"] >= 2
        
        channel_names = [c["name"] for c in result["channels"]]
        assert "Chartoro FX" in channel_names
        assert any("GREEN" in name for name in channel_names)


def test_unexecuted_signal_lifecycle_card_marked_fuera_precio():
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    from unittest.mock import MagicMock
    from datetime import datetime, timezone

    # Mensaje de señal no ejecutado
    msg = MagicMock()
    msg.id = 101
    msg.message_id = 2632
    msg.channel_name = "XAU(USD) GREEN PIPS"
    msg.channel_id = -1003674180002
    msg.raw_text = """Pair (Gold vs USD)
Direction: BUY 
Entry : 4618 / 4615
✔️Take Profit 1 4623
😢Sop Loss 4508"""
    msg.received_at = datetime(2026, 8, 27, 5, 23, 51, tzinfo=timezone.utc)
    msg.error_reason = "FUERA PRECIO"

    # Sin trades ejecutados
    cards = consolidate_telegram_trade_lifecycle([msg], executed_trades=[])
    assert len(cards) == 1
    assert cards[0]["status"] == "REJECTED"
    assert cards[0]["outcome_text"] == "FUERA PRECIO"
    assert cards[0]["entry_price"] == 4616.50

