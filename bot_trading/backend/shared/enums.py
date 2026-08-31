"""Enums unificados compartidos entre Pydantic, SQLAlchemy y adaptadores de broker.

Fuente única de verdad para los tipos transversales del motor de trading.
Los enums heredan de ``str`` para garantizar compatibilidad con:
- Pydantic (serialización automática al valor).
- SQLAlchemy (``SQLEnum`` almacena el valor/name idénticos).
- Comparaciones de negocio contra literales de cadena (``OrderSide.BUY == "BUY"``).
"""
import enum


class OrderSide(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class SignalType(str, enum.Enum):
    NEW_ORDER = "NEW_ORDER"
    MOVE_SL = "MOVE_SL"
    MOVE_BE = "MOVE_BE"
    CLOSE_ORDER = "CLOSE_ORDER"
    CANCEL_ORDER = "CANCEL_ORDER"


class ParserType(str, enum.Enum):
    REGEX = "REGEX"
    AI_FALLBACK = "AI_FALLBACK"


class TradeStatus(str, enum.Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    TP1_HIT = "TP1_HIT"
    TP2_HIT = "TP2_HIT"
    TP3_TRAILING = "TP3_TRAILING"
    CLOSED_TP = "CLOSED_TP"
    CLOSED_SL = "CLOSED_SL"
    CLOSED_MANUAL = "CLOSED_MANUAL"
    CLOSED_REBOOT_NO_MILESTONE = "CLOSED_REBOOT_NO_MILESTONE"
    CLOSED_KILL_SWITCH = "CLOSED_KILL_SWITCH"
    REJECTED = "REJECTED"


class ExecutionMode(str, enum.Enum):
    AUDIT = "AUDIT"
    PRODUCTION = "PRODUCTION"
