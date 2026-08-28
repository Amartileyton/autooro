import pytest
from decimal import Decimal
from backend.ingesta.parser import parse_signal
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType, ParserType
)


def test_parse_standard_buy_signal():
    text = """
    🟢 BUY GOLD (XAUUSD) @ 2345.50
    SL: 2335.00
    TP1: 2352.00
    TP2: 2360.00
    TP3: 2375.00
    """
    event = parse_signal(text, message_id=101, channel_id=-1001)
    assert isinstance(event, TradingSignalEvent)
    assert event.asset == "XAUUSD"
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("2345.50")
    assert event.sl_price == Decimal("2335.00")
    assert event.requires_dynamic_sl is False
    assert len(event.tp_levels) == 3
    assert event.tp_levels[0] == Decimal("2352.00")
    assert event.tp_levels[1] == Decimal("2360.00")
    assert event.tp_levels[2] == Decimal("2375.00")


def test_parse_sell_signal_dynamic_sl():
    text = """
    🔴 SELL XAUUSD NOW @ 2350.00
    TP1: 2342.00
    TP2: 2335.00
    """
    event = parse_signal(text, message_id=102, channel_id=-1001)
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("2350.00")
    assert event.sl_price is None
    assert event.requires_dynamic_sl is True
    assert event.tp_levels == [Decimal("2342.00"), Decimal("2335.00")]


def test_parse_spanish_compra_with_emojis():
    text = """
    🥇 NUEVA SEÑAL ORO
    COMPRA EN 2340.00
    STOP LOSS 2332.00
    TP 2348.00, 2355.00, 2365.00
    """
    event = parse_signal(text, message_id=103, channel_id=-1001)
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("2340.00")
    assert event.sl_price == Decimal("2332.00")
    assert event.tp_levels == [Decimal("2348.00"), Decimal("2355.00"), Decimal("2365.00")]


def test_parse_modifier_move_sl():
    text = "Move SL to 2345.50 now"
    event = parse_signal(text)
    assert isinstance(event, ModifierSignalEvent)
    assert event.signal_type == SignalType.MOVE_SL
    assert event.target_price == Decimal("2345.50")


def test_parse_modifier_break_even():
    text = "Set BE on XAUUSD"
    event = parse_signal(text)
    assert isinstance(event, ModifierSignalEvent)
    assert event.signal_type == SignalType.MOVE_BE


def test_parse_modifier_close_order():
    text = "Close Now XAUUSD taking profits"
    event = parse_signal(text)
    assert isinstance(event, ModifierSignalEvent)
    assert event.signal_type == SignalType.CLOSE_ORDER
    assert event.close_percentage == Decimal("100.0")


def test_reject_incoherent_math_buy():
    # BUY con TP1 menor que entrada (incoherencia fatal -> rechazar)
    text = """
    BUY XAUUSD 2345.00
    SL 2335.00
    TP1 2330.00
    """
    event = parse_signal(text)
    assert event is None

    # BUY con errata en SL (SL mayor que entrada) -> rescatar aplicando SL dinámico
    text_typo = """
    BUY XAUUSD 2345.00
    SL 2355.00
    TP1 2360.00
    """
    event_typo = parse_signal(text_typo)
    assert event_typo is not None
    assert event_typo.requires_dynamic_sl is True
    assert event_typo.sl_price is None


def test_reject_incoherent_math_sell():
    # SELL con TP1 mayor que entrada
    text = """
    SELL XAUUSD 2345.00
    SL 2355.00
    TP1 2360.00
    """
    event = parse_signal(text)
    assert event is None


def test_ignore_chat_messages():
    text = "Buenos días traders, hoy esperamos alta volatilidad en el oro por datos de IPC."
    event = parse_signal(text)
    assert event is None
