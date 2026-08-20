import pytest
from decimal import Decimal
from backend.risk.engine import RiskEngine
from backend.broker.paper import LocalPaperBroker
from backend.broker.base import AccountInfo, BrokerTick
from backend.ingesta.schemas import TradingSignalEvent, OrderSide


@pytest.mark.asyncio
async def test_slot_allocation_max_4():
    broker = LocalPaperBroker()
    engine = RiskEngine(broker=broker)

    occupied = {}
    signal = TradingSignalEvent(
        asset="XAUUSD",
        side=OrderSide.BUY,
        entry_price=Decimal("2345.00"),
        sl_price=Decimal("2335.00"),
        tp_levels=[Decimal("2355.00")],
        raw_text="BUY"
    )

    # Llenar slots 1 a 4
    for expected_slot in range(1, 5):
        can_open, slot_id, reason = engine.evaluate_signal_for_slot(signal, occupied)
        assert can_open is True
        assert slot_id == expected_slot
        occupied[slot_id] = "DUMMY_TRADE"

    # Intentar slot 5 -> Debe rechazar con SLOTS_EXHAUSTED
    can_open, slot_id, reason = engine.evaluate_signal_for_slot(signal, occupied)
    assert can_open is False
    assert slot_id is None
    assert reason == "SLOTS_EXHAUSTED"


@pytest.mark.asyncio
async def test_exact_lot_sizing_calculation():
    broker = LocalPaperBroker()
    engine = RiskEngine(broker=broker)

    # Balance/Margen Libre = 10,000 USD
    # Slot Margin (25%) = 2,500 USD
    # Apalancamiento = 100:1 -> Poder de compra = 250,000 USD
    # Entry Price = 2,500 USD | Tamaño Contrato = 100 oz -> Valor por lote = 250,000 USD
    # Lote esperado = 250,000 / 250,000 = 1.00 lote
    account_info = AccountInfo(
        balance=Decimal("10000.00"),
        equity=Decimal("10000.00"),
        margin_used=Decimal("0.00"),
        free_margin=Decimal("10000.00"),
        margin_level_pct=Decimal("9999.99")
    )

    lot = await engine.calculate_lot_size(entry_price=Decimal("2500.00"), account_info=account_info)
    assert lot == Decimal("1.00")


@pytest.mark.asyncio
async def test_slippage_check():
    broker = LocalPaperBroker()
    engine = RiskEngine(broker=broker)
    engine.slippage_tolerance = Decimal("0.50")

    # Forzar precio actual en broker
    broker._current_ask = Decimal("2345.40")
    broker._current_bid = Decimal("2345.20")

    # Señal con entrada 2345.00 -> diff 0.40 <= 0.50 -> Válido
    is_valid, market_p, diff = await engine.check_slippage(Decimal("2345.00"), OrderSide.BUY)
    assert is_valid is True

    # Señal con entrada 2340.00 -> diff 5.40 > 0.50 -> Rechazado
    is_valid, market_p, diff = await engine.check_slippage(Decimal("2340.00"), OrderSide.BUY)
    assert is_valid is False
