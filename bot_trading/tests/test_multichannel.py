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
