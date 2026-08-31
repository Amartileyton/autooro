"""Cálculo financiero de costes para XAUUSD (cTrader + IC Markets).

Módulo puro (sin dependencias de base de datos ni de ingesta): recibe valores
numéricos y devuelve el desglose (ganancia bruta, coste de spread, comisión y
beneficio neto). Extraído de ``ingesta/trade_lifecycle.py`` manteniendo intacta
la fórmula original (Zero-Regression).
"""
from typing import Optional, Tuple


def calculate_trade_costs(
    entry_price: float,
    exit_price: Optional[float],
    lot_size: float,
    pnl_usd: Optional[float],
) -> Tuple[Optional[float], float, float, Optional[float]]:
    """
    Calcula el desglose financiero exacto de costes para XAUUSD:
    - Spread cTrader: 0.15$ USD por onza * volumen de onzas (lot_size * 100).
    - Comisión IC Markets cTrader: 3.00$ USD por cada 100.000$ negociados por lado (apertura + cierre).
    - Ganancia Bruta: PnL generado únicamente por la distancia de cotización.
    - Beneficio/Pérdida Neto Final: Bruto - Comisión IC Markets - Spread cTrader.
    """
    oz = float(lot_size or 0.01) * 100.0
    entry_px = float(entry_price or 2650.0)
    exit_px = float(exit_price or entry_px)

    # 1. Coste del Spread (~0.15$ USD por onza)
    spread_cost = round(0.15 * oz, 2)

    # 2. Comisión IC Markets cTrader (3$ / 100k USD por lado)
    entry_notional_usd = entry_px * oz
    exit_notional_usd = exit_px * oz
    comm_open = (entry_notional_usd / 100000.0) * 3.00
    comm_close = (exit_notional_usd / 100000.0) * 3.00
    commission = round(comm_open + comm_close, 2)
    if commission < 0.10 and oz >= 1.0:
        commission = 0.16

    if pnl_usd is not None:
        gross = round(float(pnl_usd), 2)
        # El beneficio o pérdida final entrega el valor con comisiones y spreads ya descontados
        net = round(gross - commission - spread_cost, 2)
    else:
        gross = None
        net = None

    return gross, spread_cost, commission, net
