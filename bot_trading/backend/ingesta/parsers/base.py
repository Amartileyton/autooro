import re
import logging
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from typing import Optional, Union, List, Tuple
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType, ParserType
)

logger = logging.getLogger("trading_bot.parser.base")


def sanitize_price_str(raw_str: str) -> Optional[Decimal]:
    """
    Sanitiza y normaliza cualquier formato de precio eliminando separadores de miles
    y asegurando el punto (.) decimal estándar requerido por Python Decimal.
    Ejemplos:
    - '4383.69'  -> Decimal('4383.69')
    - '4383,69'  -> Decimal('4383.69')
    - '4.383,69' -> Decimal('4383.69')
    - '4,383.69' -> Decimal('4383.69')
    - '2650'     -> Decimal('2650')
    """
    if not raw_str:
        return None
    s = raw_str.strip()
    
    if '.' in s and ',' in s:
        if s.find('.') < s.find(','):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif ',' in s:
        s = s.replace(',', '.')
    
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


class BaseSignalParser(ABC):
    """Interfaz abstracta para todos los parsers específicos de canales de Telegram."""

    @abstractmethod
    def parse(
        self,
        raw_text: str,
        message_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        channel_name: Optional[str] = None,
        execution_mode: str = "AUDIT",
        reply_to_msg_id: Optional[int] = None
    ) -> Optional[Union[TradingSignalEvent, ModifierSignalEvent]]:
        """Analiza el texto del mensaje y retorna un evento de señal normalizado o None."""
        pass
