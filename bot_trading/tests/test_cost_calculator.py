"""Tests unitarios del módulo extraído backend.services.cost_calculator."""
import pytest

from backend.services.cost_calculator import calculate_trade_costs


def test_calculate_trade_costs_known_values():
    """Valida el desglose exacto para un trade BUY con lot_size=0.09."""
    gross, spread, commission, net = calculate_trade_costs(
        entry_price=2650.0,
        exit_price=2655.0,
        lot_size=0.09,
        pnl_usd=45.0,
    )
    assert gross == 45.0
    assert spread == pytest.approx(1.35)      # 0.15 * 9 onzas
    assert commission == pytest.approx(1.43)  # 3$ / 100k por lado
    assert net == pytest.approx(42.22)        # 45 - 1.43 - 1.35


def test_calculate_trade_costs_no_pnl():
    """Sin PnL real, gross y net son None pero spread/comisión sí se calculan."""
    gross, spread, commission, net = calculate_trade_costs(
        entry_price=2650.0,
        exit_price=2655.0,
        lot_size=0.09,
        pnl_usd=None,
    )
    assert gross is None
    assert net is None
    assert spread == pytest.approx(1.35)
    assert commission == pytest.approx(1.43)


def test_calculate_trade_costs_none_exit_uses_entry():
    """exit_price=None usa el entry como precio de salida (apertura == cierre)."""
    gross, spread, commission, net = calculate_trade_costs(
        entry_price=2650.0,
        exit_price=None,
        lot_size=0.09,
        pnl_usd=0.0,
    )
    # Apertura y cierre al mismo notional => comisión duplicada por lado.
    expected_commission = round((2650.0 * 9.0 / 100000.0) * 3.00 * 2, 2)
    assert commission == pytest.approx(expected_commission)
    assert gross == 0.0
    assert net == pytest.approx(round(0.0 - expected_commission - 1.35, 2))


def test_calculate_trade_costs_small_lot_no_floor():
    """Con oz < 1.0 no se aplica el suelo de comisión de 0.16."""
    gross, spread, commission, net = calculate_trade_costs(
        entry_price=2650.0,
        exit_price=2650.0,
        lot_size=0.001,   # oz = 0.1
        pnl_usd=0.0,
    )
    assert commission < 0.10
    assert gross == 0.0
