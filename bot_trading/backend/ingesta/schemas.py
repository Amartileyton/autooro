from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
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


class TradingSignalEvent(BaseModel):
    """Esquema normalizado para una nueva señal de entrada."""
    asset: str = Field(default="XAUUSD", description="Activo financiero normalizado")
    side: OrderSide = Field(description="Dirección de la orden: BUY o SELL")
    entry_price: Decimal = Field(description="Precio de entrada")
    sl_price: Optional[Decimal] = Field(default=None, description="Stop Loss explícito si fue provisto")
    tp_levels: List[Decimal] = Field(min_length=1, max_length=5, description="Lista ordenada de Take Profits [TP1, TP2, TP3...]")
    requires_dynamic_sl: bool = Field(default=False, description="True si falta SL y debe calcularse dinámicamente")
    parser_type: ParserType = Field(default=ParserType.REGEX, description="Indica qué parser extrajo la señal")
    raw_text: str = Field(description="Texto original del mensaje de Telegram")
    message_id: Optional[int] = Field(default=None, description="ID del mensaje en Telegram")
    channel_id: Optional[int] = Field(default=None, description="ID del canal de Telegram")
    channel_name: Optional[str] = Field(default="Chartoro FX", description="Nombre del canal emisor")
    execution_mode: str = Field(default="AUDIT", description="Modo operativo: AUDIT o PRODUCTION")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("asset")
    @classmethod
    def normalize_asset(cls, v: str) -> str:
        v_upper = v.upper().strip()
        if "XAU" in v_upper or "GOLD" in v_upper or "ORO" in v_upper:
            return "XAUUSD"
        return v_upper


class ModifierSignalEvent(BaseModel):
    """Esquema para señales de modificación posterior (Move SL, Set BE, Close Now)."""
    signal_type: SignalType = Field(description="Tipo de modificación")
    target_price: Optional[Decimal] = Field(default=None, description="Nuevo precio de SL si aplica")
    close_percentage: Optional[Decimal] = Field(default=Decimal("100.0"), description="Porcentaje a cerrar (1-100%)")
    raw_text: str = Field(description="Texto original del mensaje")
    message_id: Optional[int] = Field(default=None)
    channel_id: Optional[int] = Field(default=None)
    channel_name: Optional[str] = Field(default="Chartoro FX")
    execution_mode: str = Field(default="AUDIT")
    reply_to_msg_id: Optional[int] = Field(default=None, description="ID del mensaje padre al que responde")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
