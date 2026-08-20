from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, List, Optional, Any, Callable, Tuple
from pydantic import BaseModel
from backend.database.models import OrderSide, TradeStatus


class AccountInfo(BaseModel):
    balance: Decimal
    equity: Decimal
    margin_used: Decimal
    free_margin: Decimal
    margin_level_pct: Decimal
    currency: str = "USD"


class BrokerTick(BaseModel):
    symbol: str
    bid: Decimal
    ask: Decimal
    timestamp: float


class BrokerPosition(BaseModel):
    ticket_id: str
    symbol: str
    side: OrderSide
    lot_size: Decimal
    entry_price: Decimal
    current_price: Decimal
    sl: Optional[Decimal]
    tp: Optional[Decimal]
    unrealized_pnl: Decimal
    open_time: float


class BaseBrokerAdapter(ABC):
    """Interfaz abstracta estándar para cualquier broker (Paper, cTrader, MetaApi)."""

    @abstractmethod
    async def connect(self) -> bool:
        """Establece conexión con el broker."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Cierra la conexión con el broker."""
        pass

    @abstractmethod
    async def get_account_info(self) -> AccountInfo:
        """Retorna balance, equidad, margen libre y margen usado."""
        pass

    @abstractmethod
    async def get_current_tick(self, symbol: str = "XAUUSD") -> BrokerTick:
        """Retorna el último tick (bid/ask) de mercado."""
        pass

    @abstractmethod
    async def subscribe_ticks(self, symbol: str, callback: Callable[[BrokerTick], Any]) -> None:
        """Suscribe una función callback al flujo de ticks en tiempo real."""
        pass

    @abstractmethod
    async def execute_order(
        self,
        symbol: str,
        side: OrderSide,
        lot_size: Decimal,
        entry_price: Decimal,
        sl: Optional[Decimal],
        tp: Optional[Decimal],
        comment: str = ""
    ) -> str:
        """Ejecuta una orden a mercado y retorna el ticket_id único generado."""
        pass

    @abstractmethod
    async def modify_order(
        self,
        ticket_id: str,
        new_sl: Optional[Decimal] = None,
        new_tp: Optional[Decimal] = None
    ) -> bool:
        """Modifica los niveles de SL y/o TP de una orden abierta."""
        pass

    @abstractmethod
    async def close_order(
        self,
        ticket_id: str,
        close_price: Optional[Decimal] = None,
        reason: str = "MANUAL_CLOSE"
    ) -> Tuple[Decimal, Decimal]:
        """Cierra una posición y retorna (precio_cierre, pnl_realizado)."""
        pass

    @abstractmethod
    async def get_open_positions(self) -> List[BrokerPosition]:
        """Retorna la lista de todas las posiciones activas en el broker."""
        pass
