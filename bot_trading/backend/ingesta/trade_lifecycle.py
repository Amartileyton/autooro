"""Shim de compatibilidad retroactiva (Zero-Regression).

Los símbolos del ciclo de vida de trades han sido modularizados en:
  - backend.models.card              -> TradeLifecycleCard, safe_num, format_full_datetime
  - backend.services.cost_calculator -> calculate_trade_costs
  - backend.services.reconciler      -> consolidate_telegram_trade_lifecycle, get_msg_datetime, get_card_timestamp

Este módulo se conserva para no romper importadores existentes
(``api/routes.py`` y ``tests/test_multichannel.py``).
"""
from backend.models.card import (
    format_full_datetime,
    safe_num,
    TradeLifecycleCard,
)
from backend.services.cost_calculator import calculate_trade_costs
from backend.services.reconciler import (
    get_msg_datetime,
    get_card_timestamp,
    consolidate_telegram_trade_lifecycle,
)

__all__ = [
    "format_full_datetime",
    "safe_num",
    "TradeLifecycleCard",
    "calculate_trade_costs",
    "get_msg_datetime",
    "get_card_timestamp",
    "consolidate_telegram_trade_lifecycle",
]
