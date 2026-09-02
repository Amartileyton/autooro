"""Cálculo financiero de costes para XAUUSD (cTrader + IC Markets).

Módulo puro (sin dependencias de base de datos ni de ingesta): recibe valores
numéricos y devuelve el desglose (ganancia bruta, coste de spread, comisión y
beneficio neto). Extraído de ``ingesta/trade_lifecycle.py`` manteniendo intacta
la fórmula original (Zero-Regression).
"""
from typing import Optional, Tuple

# Spread de referencia fijo (fallback si no hay conexión live al broker)
# 0.15 USD por onza es el spread típico de IC Markets cTrader en XAUUSD en sesión europea.
FALLBACK_SPREAD_PER_OZ_USD = 0.15


def calculate_trade_costs(
    entry_price: float,
    exit_price: Optional[float],
    lot_size: float,
    pnl_usd: Optional[float],
    spread_usd: Optional[float] = None,
) -> Tuple[Optional[float], float, float, Optional[float]]:
    """
    Calcula el desglose financiero exacto de costes para XAUUSD:
    - Spread cTrader: coste real del spread (ask - bid) en el momento de apertura
      si viene informado como ``spread_usd`` (por onza), o fallback a $0.15/oz.
    - Comisión IC Markets cTrader: 3.00$ USD por cada 100.000$ negociados por lado
      (apertura + cierre).
    - Ganancia Bruta: PnL generado únicamente por la distancia de cotización.
    - Beneficio/Pérdida Neto Final: Bruto - Comisión IC Markets - Spread cTrader.

    Args:
        entry_price: Precio de entrada del trade.
        exit_price:  Precio de salida del trade (None si sigue abierto).
        lot_size:    Tamaño del lote (e.g. 0.01, 0.09).
        pnl_usd:     PnL bruto en USD ya calculado por el broker (None si no disponible).
        spread_usd:  Spread real en USD por onza obtenido de la API de cTrader
                     (ask - bid en el momento de apertura). Si es None se usa fallback.
    """
    oz = float(lot_size or 0.01) * 100.0
    entry_px = float(entry_price or 2650.0)
    exit_px = float(exit_price or entry_px)

    # 1. Coste del Spread
    # Si viene el spread real de la API de cTrader, usarlo; si no, usar fallback $0.15/oz
    spread_per_oz = float(spread_usd) if (spread_usd is not None and spread_usd > 0.0) else FALLBACK_SPREAD_PER_OZ_USD
    spread_cost = round(spread_per_oz * oz, 2)

    # 2. Comisión IC Markets cTrader (3$ / 100k USD por lado: apertura + cierre)
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
