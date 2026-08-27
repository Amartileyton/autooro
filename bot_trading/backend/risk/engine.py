import logging
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple
from backend.config import settings
from backend.broker.base import BaseBrokerAdapter, AccountInfo
from backend.ingesta.schemas import TradingSignalEvent, OrderSide
from backend.database.models import Trade, TradeStatus, OrderSide as DBOrderSide

logger = logging.getLogger("trading_bot.risk_engine")


class RiskEngine:
    """
    Motor de Gestión de Riesgo Institucional:
    - 4 Slots de capital fijos (25% del margen libre por slot).
    - Límite de 4 operaciones concurrentes.
    - Lot sizing exacto según apalancamiento y tamaño de contrato de XAUUSD.
    - Zero-tolerance slippage check.
    - Regla de Stop Loss dinámico por defecto.
    """

    def __init__(self, broker: BaseBrokerAdapter):
        self.broker = broker
        self.max_slots = settings.MAX_CONCURRENT_SLOTS
        self.slot_margin_pct = settings.SLOT_MARGIN_PERCENT
        self.leverage = settings.LEVERAGE
        self.contract_size = settings.CONTRACT_SIZE
        self.min_lot = settings.MIN_LOT_SIZE
        self.lot_step = settings.LOT_STEP
        self.slippage_tolerance = settings.SLIPPAGE_TOLERANCE_USD
        self.dynamic_sl_delta = settings.DEFAULT_DYNAMIC_SL_DELTA_USD
        self.max_allowed_sl_delta = getattr(settings, 'MAX_ALLOWED_SL_DELTA_USD', Decimal("15.00"))

    def calculate_dynamic_sl(self, side: OrderSide, entry_price: Decimal) -> Decimal:
        """Calcula el SL dinámico si la señal no especificó uno explícito."""
        if side == OrderSide.BUY:
            return entry_price - self.dynamic_sl_delta
        else:
            return entry_price + self.dynamic_sl_delta

    def sanitize_sl(self, side: OrderSide, entry_price: Decimal, sl_price: Optional[Decimal]) -> Decimal:
        """
        Valida y acota el Stop Loss de una señal:
        - Si no tiene SL o es None: usa calculate_dynamic_sl (ej. 8.50 USD).
        - Si el SL explícito supera MAX_ALLOWED_SL_DELTA_USD (ej. 15.00 USD), lo recorta automáticamente al límite de seguridad máximo.
        - Garantiza coherencia matemática (para BUY, SL < Entry; para SELL, SL > Entry).
        """
        if sl_price is None:
            return self.calculate_dynamic_sl(side, entry_price)

        if side == OrderSide.BUY:
            if sl_price >= entry_price:
                logger.warning(f"SL incoherente para BUY ({sl_price} >= {entry_price}). Aplicando SL dinámico.")
                return self.calculate_dynamic_sl(side, entry_price)
            
            delta = entry_price - sl_price
            if delta > self.max_allowed_sl_delta:
                capped_sl = (entry_price - self.max_allowed_sl_delta).quantize(Decimal("0.01"))
                logger.warning(
                    f"⚠️ [CIRCUIT BREAKER] SL explícito desorbitado (${delta:.2f} USD vs max ${self.max_allowed_sl_delta:.2f} USD). "
                    f"Ajustado automáticamente de {sl_price} a {capped_sl}"
                )
                return capped_sl
            return sl_price

        else:  # SELL
            if sl_price <= entry_price:
                logger.warning(f"SL incoherente para SELL ({sl_price} <= {entry_price}). Aplicando SL dinámico.")
                return self.calculate_dynamic_sl(side, entry_price)
            
            delta = sl_price - entry_price
            if delta > self.max_allowed_sl_delta:
                capped_sl = (entry_price + self.max_allowed_sl_delta).quantize(Decimal("0.01"))
                logger.warning(
                    f"⚠️ [CIRCUIT BREAKER] SL explícito desorbitado (${delta:.2f} USD vs max ${self.max_allowed_sl_delta:.2f} USD). "
                    f"Ajustado automáticamente de {sl_price} a {capped_sl}"
                )
                return capped_sl
            return sl_price

    async def check_slippage(
        self,
        signal_entry: Decimal,
        side: OrderSide,
        entry_min: Optional[Decimal] = None,
        entry_max: Optional[Decimal] = None
    ) -> Tuple[bool, Decimal, Decimal]:
        """
        Comprueba el tick actual contra el precio de entrada de la señal o rango seguro.
        Si hay un rango seguro [entry_min, entry_max] y el precio actual está dentro, diff = 0.
        Retorna (is_valid, market_price, diff).
        """
        tick = await self.broker.get_current_tick("XAUUSD")
        market_price = tick.ask if side == OrderSide.BUY else tick.bid

        if entry_min is not None and entry_max is not None:
            # Caso 1: Dentro del rango seguro de entrada
            if entry_min <= market_price <= entry_max:
                return True, market_price, Decimal("0.00")
            elif market_price < entry_min:
                diff = entry_min - market_price
                return diff <= self.slippage_tolerance, market_price, diff
            else:
                diff = market_price - entry_max
                return diff <= self.slippage_tolerance, market_price, diff

        diff = abs(market_price - signal_entry)
        is_valid = diff <= self.slippage_tolerance
        return is_valid, market_price, diff

    async def calculate_lot_size(self, entry_price: Decimal, account_info: AccountInfo) -> Decimal:
        """
        Calcula el tamaño de lote exacto para 1 slot (25% del margen libre disponible):
        Margen por Slot = Margen Libre * 0.25
        Lote = (Margen Slot * Apalancamiento) / (Precio Entrada * Tamaño Contrato)
        """
        free_margin = account_info.free_margin
        slot_margin = free_margin * self.slot_margin_pct

        if slot_margin <= Decimal("0.00") or entry_price <= Decimal("0.00"):
            return self.min_lot

        # Nominal = Margen * Apalancamiento
        purchasing_power = slot_margin * self.leverage
        contract_value_per_lot = entry_price * self.contract_size

        raw_lot = purchasing_power / contract_value_per_lot
        
        # Redondear hacia abajo según el step (0.01)
        steps = (raw_lot / self.lot_step).quantize(Decimal("1"), rounding=ROUND_FLOOR)
        calculated_lot = steps * self.lot_step

        # Garantizar límites mínimos
        final_lot = max(self.min_lot, calculated_lot)
        return final_lot.quantize(Decimal("0.01"))

    def evaluate_signal_for_slot(
        self,
        signal: TradingSignalEvent,
        occupied_slots: Dict[int, Any]
    ) -> Tuple[bool, Optional[int], str]:
        """
        Evalúa si hay slots disponibles y asigna el primer slot libre (1 a 4).
        """
        for slot_id in range(1, self.max_slots + 1):
            if slot_id not in occupied_slots:
                return True, slot_id, "OK"

        return False, None, "SLOTS_EXHAUSTED"
