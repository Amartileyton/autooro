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
    assert str(getattr(event.execution_mode, 'value', event.execution_mode)) in ("AUDIT", "PRODUCTION")


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


def test_move_your_sl_modifier_parsing():
    from backend.ingesta.parsers.green_pips import GreenPipsParser
    from backend.ingesta.parsers.chartoro import ChartoroParser
    from backend.ingesta.schemas import SignalType

    gp_parser = GreenPipsParser()
    chartoro_parser = ChartoroParser()

    # Green Pips: "MOVE YOUR SL 4603"
    event_gp = gp_parser.parse("MOVE YOUR SL 4603", message_id=2633)
    assert event_gp is not None
    assert event_gp.signal_type == SignalType.MOVE_SL
    assert event_gp.target_price == Decimal("4603.00")

    # Green Pips: "MOVE SL 4603"
    event_gp2 = gp_parser.parse("MOVE SL 4603", message_id=2634)
    assert event_gp2 is not None
    assert event_gp2.signal_type == SignalType.MOVE_SL
    assert event_gp2.target_price == Decimal("4603.00")

    # Chartoro: "MOVE YOUR SL 4610"
    event_ch = chartoro_parser.parse("MOVE YOUR SL 4610", message_id=8016)
    assert event_ch is not None
    assert event_ch.signal_type == SignalType.MOVE_SL
    assert event_ch.target_price == Decimal("4610.00")


def test_risk_engine_sl_circuit_breaker():
    from backend.broker.paper import LocalPaperBroker
    from backend.risk.engine import RiskEngine
    from backend.ingesta.schemas import OrderSide

    broker = LocalPaperBroker()
    risk = RiskEngine(broker=broker)

    # 1. SL desorbitado de $108.50 en BUY (ej. señal real: Entry 4616.50, SL 4508)
    entry_buy = Decimal("4616.50")
    exorbitant_sl_buy = Decimal("4508.00")
    sanitized_buy = risk.sanitize_sl(OrderSide.BUY, entry_buy, exorbitant_sl_buy)
    # Debe topar a máx $15 USD: 4616.50 - 15.00 = 4601.50
    assert sanitized_buy == Decimal("4601.50")

    # 2. SL normal de $8.50 en BUY (Entry 4616.50, SL 4608.00)
    normal_sl_buy = Decimal("4608.00")
    sanitized_normal = risk.sanitize_sl(OrderSide.BUY, entry_buy, normal_sl_buy)
    assert sanitized_normal == Decimal("4608.00")

    # 3. SL desorbitado en SELL (Entry 4600.00, SL 4750.00)
    entry_sell = Decimal("4600.00")
    exorbitant_sl_sell = Decimal("4750.00")
    sanitized_sell = risk.sanitize_sl(OrderSide.SELL, entry_sell, exorbitant_sl_sell)
    # Debe topar a máx $15 USD: 4600.00 + 15.00 = 4615.00
    assert sanitized_sell == Decimal("4615.00")


def test_green_pips_sell_with_incoherent_sl_typo():
    from backend.ingesta.parsers.green_pips import GreenPipsParser
    from backend.ingesta.schemas import OrderSide

    text = """Pair (Gold vs USD)
 
    Direction:  SELL 
Entry :  4615 / 4610

✔️Take Profit 1       4600
✔️Take Profit 2       4590
✔️Take Profit 3       4580

😢Sop Loss            4520


🫣🔤Risk Management Is Important"""

    parser = GreenPipsParser()
    event = parser.parse(text, message_id=2671)
    assert event is not None
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("4612.50")
    assert event.requires_dynamic_sl is True


def test_trade_lifecycle_cards_pnl_sync_loss_and_win():
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    from unittest.mock import MagicMock
    from datetime import datetime, timezone, timedelta
    from backend.database.models import TradeStatus, OrderSide

    t0 = datetime(2026, 8, 28, 10, 0, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(minutes=5)
    t2 = t0 + timedelta(minutes=10)

    # 1. Mensaje de señal
    msg1 = MagicMock()
    msg1.id = 1
    msg1.message_id = 7001
    msg1.channel_name = "Chartoro FX"
    msg1.channel_id = -1002763662248
    msg1.raw_text = "BUY XAUUSD 2650.00 SL 2640.00 TP1 2655.00"
    msg1.received_at = t0
    msg1.error_reason = None

    # 2. Trade 1 ejecutado en DB que cerró en LOSS (-$135.00)
    db_trade1 = MagicMock()
    db_trade1.id = 10
    db_trade1.ticket_id = "TKT-LOSS-01"
    db_trade1.slot_id = 1
    db_trade1.channel_name = "Chartoro FX"
    db_trade1.side = OrderSide.BUY
    db_trade1.entry_price = 2650.00
    db_trade1.close_price = 2635.00
    db_trade1.current_sl = 2635.00
    db_trade1.initial_sl = 2640.00
    db_trade1.tp1 = 2655.00
    db_trade1.tp2 = 2660.00
    db_trade1.tp3 = 2670.00
    db_trade1.lot_size = 0.09
    db_trade1.status = TradeStatus.CLOSED_SL
    db_trade1.pnl = -135.00
    db_trade1.realized_cash_pnl = 0.00
    db_trade1.close_reason = "SL_HIT (2635.00)"
    db_trade1.open_time = t0
    db_trade1.close_time = t1
    db_trade1.raw_signal_id = 7001

    # 3. Trade 2 ejecutado en DB que cerró en WIN (+$315.00)
    db_trade2 = MagicMock()
    db_trade2.id = 11
    db_trade2.ticket_id = "TKT-WIN-02"
    db_trade2.slot_id = 2
    db_trade2.channel_name = "XAU(USD) GREEN PIPS"
    db_trade2.side = OrderSide.SELL
    db_trade2.entry_price = 2660.00
    db_trade2.close_price = 2625.00
    db_trade2.current_sl = 2630.00
    db_trade2.initial_sl = 2670.00
    db_trade2.tp1 = 2655.00
    db_trade2.tp2 = 2645.00
    db_trade2.tp3 = 2630.00
    db_trade2.lot_size = 0.09
    db_trade2.status = TradeStatus.CLOSED_TP
    db_trade2.pnl = 315.00
    db_trade2.realized_cash_pnl = 100.00
    db_trade2.close_reason = "TRAILING_SL_HIT"
    db_trade2.open_time = t1
    db_trade2.close_time = t2
    db_trade2.raw_signal_id = None

    cards = consolidate_telegram_trade_lifecycle([msg1], executed_trades=[db_trade1, db_trade2])

    assert len(cards) == 2
    # El más reciente (Trade 2 cerrado a las t2) debe ser el primero (index 0)
    assert cards[0]["ticket_id"] == "TKT-WIN-02"
    assert cards[0]["status"] == "WIN"
    assert cards[0]["outcome_text"] == "GANADA"
    assert cards[0]["pnl_usd"] == 315.00
    assert cards[0]["exit_price"] == 2625.00

    # Trade 1 cerrado en LOSS (-$135.00)
    assert cards[1]["ticket_id"] == "TKT-LOSS-01"
    assert cards[1]["status"] == "LOSS"
    assert cards[1]["outcome_text"] == "PERDIDA"
    assert cards[1]["pnl_usd"] == -135.00
    assert cards[1]["exit_price"] == 2635.00


def test_trade_lifecycle_always_shows_last_10_trades_sorted():
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    from unittest.mock import MagicMock
    from datetime import datetime, timezone, timedelta
    from backend.database.models import TradeStatus, OrderSide

    base_time = datetime(2026, 8, 28, 8, 0, 0, tzinfo=timezone.utc)
    executed_trades = []

    for i in range(15):
        t = MagicMock()
        t.id = i + 1
        t.ticket_id = f"TKT-BATCH-{i:02d}"
        t.slot_id = (i % 4) + 1
        t.channel_name = "Chartoro FX" if i % 2 == 0 else "XAU(USD) GREEN PIPS"
        t.side = OrderSide.BUY if i % 2 == 0 else OrderSide.SELL
        t.entry_price = 2650.0 + i
        t.close_price = 2655.0 + i
        t.current_sl = 2640.0
        t.initial_sl = 2640.0
        t.tp1 = 2655.0
        t.tp2 = 2660.0
        t.tp3 = 2670.0
        t.lot_size = 0.05
        t.status = TradeStatus.CLOSED_TP
        t.pnl = 50.0 + i * 10
        t.realized_cash_pnl = 20.0
        t.close_reason = "TP1_HIT"
        t.open_time = base_time + timedelta(hours=i)
        t.close_time = base_time + timedelta(hours=i, minutes=30)
        t.raw_signal_id = None
        executed_trades.append(t)

    cards = consolidate_telegram_trade_lifecycle([], executed_trades=executed_trades)
    assert len(cards) == 15

    # Tomar los últimos 10 trades
    last_10 = cards[:10]
    assert len(last_10) == 10

    # El primero debe ser el trade número 15 (el más reciente, i=14)
    assert last_10[0]["ticket_id"] == "TKT-BATCH-14"
    assert last_10[0]["pnl_usd"] == 190.0

    # El décimo debe ser el trade número 6 (i=5)
    assert last_10[9]["ticket_id"] == "TKT-BATCH-05"
    assert last_10[9]["pnl_usd"] == 100.0


def test_tp2_hit_detection_from_messages_and_db():
    from backend.ingesta.trade_lifecycle import consolidate_telegram_trade_lifecycle
    from unittest.mock import MagicMock
    from datetime import datetime, timezone, timedelta
    from backend.database.models import TradeStatus, OrderSide

    t0 = datetime(2026, 8, 28, 12, 0, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(minutes=10)

    # 1. Señal inicial BUY con TP1=2655, TP2=2660, TP3=2670
    msg1 = MagicMock()
    msg1.id = 1
    msg1.message_id = 8801
    msg1.channel_name = "Chartoro FX"
    msg1.channel_id = -1002763662248
    msg1.raw_text = "BUY XAUUSD 2650.00 SL 2640.00 TP1 2655.00 TP2 2660.00 TP3 2670.00"
    msg1.received_at = t0
    msg1.error_reason = None

    # 2. Mensaje de Telegram indicando TP2 alcanzado
    msg2 = MagicMock()
    msg2.id = 2
    msg2.message_id = 8802
    msg2.channel_name = "Chartoro FX"
    msg2.channel_id = -1002763662248
    msg2.raw_text = "**MOMENTUM A TODO RITMO ****💥** **#XAUUSD**** TP2 HIT, +80 Pips 🏆**"
    msg2.received_at = t1
    msg2.error_reason = None

    # 3. Trade en DB con TP2_HIT y trailing activo
    db_trade = MagicMock()
    db_trade.id = 50
    db_trade.ticket_id = "TKT-TP2-HIT"
    db_trade.slot_id = 1
    db_trade.channel_name = "Chartoro FX"
    db_trade.side = OrderSide.BUY
    db_trade.entry_price = 2650.00
    db_trade.close_price = 2655.00
    db_trade.current_sl = 2655.00  # SL subido a TP1 (2655)
    db_trade.initial_sl = 2640.00
    db_trade.tp1 = 2655.00
    db_trade.tp2 = 2660.00
    db_trade.tp3 = 2670.00
    db_trade.lot_size = 0.09
    db_trade.status = TradeStatus.CLOSED_TP
    db_trade.pnl = 180.00
    db_trade.realized_cash_pnl = 135.00  # Cobro de 75%
    db_trade.close_reason = "TRAILING_SL_HIT (2655.00)"
    db_trade.peak_price = 2662.50  # Pico superó TP2 (2660.00)
    db_trade.open_time = t0
    db_trade.close_time = t1
    db_trade.raw_signal_id = 8801

    cards = consolidate_telegram_trade_lifecycle([msg1, msg2], executed_trades=[db_trade])
    assert len(cards) == 1
    card = cards[0]

    assert card["status"] == "WIN"
    assert card["tp1_hit"] is True
    assert card["tp2_hit"] is True
    assert card["highest_tp"] >= 2
    assert any("TP2" in m for m in card["modifications"])





