"""Tests unitarios del módulo extraído backend.models.card (TradeLifecycleCard)."""
import pytest

from backend.models.card import TradeLifecycleCard, safe_num


def test_card_initializes_defaults():
    card = TradeLifecycleCard(
        trade_id="t1",
        channel_name="Chartoro FX",
        side="buy",
        entry_price=2650.0,
        created_at="2025-01-01T10:00:00+00:00",
    )
    assert card.trade_id == "t1"
    assert card.side == "BUY"               # normalizado a mayúsculas
    assert card.entry_price == 2650.0
    assert card.status == "OPEN"
    assert card.outcome_text == "EN CURSO"
    assert card.lot_size == 0.09
    assert card.margin_usd == 250.0


def test_card_mark_tp_hit_computes_pnl_buy():
    card = TradeLifecycleCard(
        "t2", "Chartoro FX", "BUY", 2650.0,
        "2025-01-01T10:00:00+00:00", tp1=2655.0,
    )
    card.mark_tp_hit(1, "+50 Pips", "2025-01-01T11:00:00+00:00")
    assert card.tp1_hit is True
    assert card.status == "WIN"
    assert card.outcome_text == "GANADA"
    assert card.exit_price == 2655.0
    assert card.pnl_usd == pytest.approx(45.0)  # (2655-2650)*100*0.09


def test_card_close_trade_computes_pnl_sell():
    card = TradeLifecycleCard(
        "t3", "Chartoro FX", "SELL", 2650.0,
        "2025-01-01T10:00:00+00:00",
    )
    card.close_trade("LOSS", 2655.0, "PERDIDA", "2025-01-01T11:00:00+00:00")
    assert card.status == "LOSS"
    assert card.outcome_text == "PERDIDA"
    assert card.pnl_usd == pytest.approx(-45.0)  # (2650-2655)*100*0.09


def test_card_calculate_trade_costs_updates_fields():
    card = TradeLifecycleCard(
        "t4", "Chartoro FX", "BUY", 2650.0,
        "2025-01-01T10:00:00+00:00",
    )
    card.pnl_usd = 45.0
    card.exit_price = 2655.0
    gross, spread, commission, net = card.calculate_trade_costs()
    assert gross == 45.0
    assert card.spread_cost_usd == pytest.approx(1.35)
    assert card.commission_usd == pytest.approx(1.43)
    assert card.net_pnl_usd == pytest.approx(42.22)
    assert net == pytest.approx(42.22)


def test_card_to_dict_shape():
    card = TradeLifecycleCard(
        "t5", "Chartoro FX", "BUY", 2650.0,
        "2025-01-01T10:00:00+00:00", sl_price=2640.0, tp1=2655.0,
    )
    d = card.to_dict()
    assert d["trade_id"] == "t5"
    assert d["side"] == "BUY"
    assert d["sl_price"] == 2640.0
    assert d["tp1"] == 2655.0
    assert "spread_cost_usd" in d
    assert "commission_usd" in d
    assert "net_pnl_usd" in d


def test_safe_num_coercion():
    assert safe_num("2,5") == 2.5
    assert safe_num(None) is None
    assert safe_num("", 0.0) == 0.0
    assert safe_num(2650) == 2650.0
    assert safe_num("no-es-numero", 1.0) == 1.0
