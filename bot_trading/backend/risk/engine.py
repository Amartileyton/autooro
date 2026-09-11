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
        self.base_lot_size = getattr(settings, 'BASE_LOT_SIZE', Decimal("0.04"))
        self.min_lot = settings.MIN_LOT_SIZE
        self.lot_step = settings.LOT_STEP
        self.slippage_tolerance = settings.SLIPPAGE_TOLERANCE_USD
        self.dynamic_sl_delta = settings.DEFAULT_DYNAMIC_SL_DELTA_USD
        self.max_allowed_sl_delta = getattr(settings, 'MAX_ALLOWED_SL_DELTA_USD', Decimal("5.00"))

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
        - Si el SL explícito supera MAX_ALLOWED_SL_DELTA_USD (5.00 USD = 50 pips), lo recorta automáticamente al límite de seguridad máximo (Circuit Breaker).
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
        entry_max: Optional[Decimal] = None,
        current_tick: Optional[Any] = None
    ) -> Tuple[bool, Decimal, Decimal]:
        """
        Comprueba el tick actual contra el precio de entrada de la señal o rango seguro.
        Si hay un rango seguro [entry_min, entry_max] y el precio actual está dentro, diff = 0.
        Retorna (is_valid, market_price, diff).
        """
        if current_tick is None:
            tick = await self.broker.get_current_tick("XAUUSD")
        else:
            tick = current_tick
        market_price = tick.ask if side == OrderSide.BUY else tick.bid

        if entry_min is not None and entry_max is not None:
            # Caso 1: Dentro del rango seguro de entrada
            if entry_min <= market_price <= entry_max:
                return True, market_price, Decimal("0.00")
            elif market_price < entry_min:
                diff = entry_min - market_price
                # En BUY, entrar por debajo es precio con descuento (favorable).
                # En SELL, entrar por debajo es PERSEGUIR hacia TP (desfavorable).
                chase_tol = getattr(settings, 'MAX_CHASE_SLIPPAGE_USD', Decimal("1.50"))
                allowed_tol = chase_tol if side == OrderSide.SELL else self.slippage_tolerance
                return diff <= allowed_tol, market_price, diff
            else:
                diff = market_price - entry_max
                # En BUY, entrar por encima es PERSEGUIR hacia TP (desfavorable).
                # En SELL, entrar por encima es precio con prima (favorable).
                chase_tol = getattr(settings, 'MAX_CHASE_SLIPPAGE_USD', Decimal("1.50"))
                allowed_tol = chase_tol if side == OrderSide.BUY else self.slippage_tolerance
                return diff <= allowed_tol, market_price, diff

        diff = abs(market_price - signal_entry)
        # Sin rango explícito, verificar si es persecución hacia la dirección de ganancia
        if (side == OrderSide.SELL and market_price < signal_entry) or (side == OrderSide.BUY and market_price > signal_entry):
            chase_tol = getattr(settings, 'MAX_CHASE_SLIPPAGE_USD', Decimal("1.50"))
            is_valid = diff <= chase_tol
        else:
            is_valid = diff <= self.slippage_tolerance
        return is_valid, market_price, diff

    async def calculate_lot_size(self, entry_price: Decimal, account_info: AccountInfo) -> Decimal:
        """
        Calcula el tamaño de lote institucional para la orden:
        - Si se especifica BASE_LOT_SIZE (0.04L para división limpia 50% TP1=0.02, 25% TP2=0.01, 25% Runner=0.01):
          Verifica que el margen libre sea suficiente para soportar la orden con apalancamiento 1:30.
        - De lo contrario, calcula el lote dinámico proporcional al margen por slot.
        """
        free_margin = account_info.free_margin
        target_lot = self.base_lot_size

        if entry_price <= Decimal("0.00") or free_margin <= Decimal("0.00"):
            return self.min_lot

        contract_value_per_lot = entry_price * self.contract_size

        if target_lot is not None and target_lot > Decimal("0"):
            # Margen requerido para target_lot (ej. 0.04L * 100 oz * precio / apalancamiento)
            required_margin_target = (target_lot * contract_value_per_lot) / self.leverage

            # Ajuste de conversión si la cuenta es EUR (típicamente ~0.86 EUR por USD)
            fx_rate = getattr(settings, 'ACCOUNT_FX_RATE', Decimal("0.861"))
            required_margin_acc = required_margin_target * fx_rate

            # Si el margen libre cubre la orden base con colchón de seguridad
            if free_margin >= required_margin_acc * Decimal("1.20"):
                return target_lot.quantize(Decimal("0.01"))

        # Fallback proporcional si el margen libre es más reducido
        slot_margin = free_margin * self.slot_margin_pct
        purchasing_power = slot_margin * self.leverage
        raw_lot = purchasing_power / contract_value_per_lot
        steps = (raw_lot / self.lot_step).quantize(Decimal("1"), rounding=ROUND_FLOOR)
        calculated_lot = steps * self.lot_step
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
