"""Estructura de datos y tipos del ciclo de vida de una operación (tarjeta).

Extraído de ``ingesta/trade_lifecycle.py`` (Zero-Regression): la clase
``TradeLifecycleCard`` y sus helpers de coerción/formato se conservan intactos.
El cálculo financiero se delega en ``backend.services.cost_calculator``.
"""
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple

from backend.services.cost_calculator import calculate_trade_costs as _calculate_trade_costs

try:
    from zoneinfo import ZoneInfo
    MADRID_TZ = ZoneInfo("Europe/Madrid")
except Exception:
    MADRID_TZ = None


def format_full_datetime(dt_val: Any) -> str:
    """Formatea la fecha y hora al formato DD/MM/YYYY HH:MM:SS en hora local de España (Europe/Madrid)."""
    if not dt_val:
        return ""
    if isinstance(dt_val, str):
        try:
            clean_str = dt_val.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if MADRID_TZ:
                dt = dt.astimezone(MADRID_TZ)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            return dt_val
    elif isinstance(dt_val, datetime):
        if dt_val.tzinfo is None:
            dt = dt_val.replace(tzinfo=timezone.utc)
        else:
            dt = dt_val
        if MADRID_TZ:
            dt = dt.astimezone(MADRID_TZ)
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    return str(dt_val)


def safe_num(val: Any, default: Optional[float] = None) -> Optional[float]:
    """Convierte de forma ultra segura cualquier valor a float válido."""
    if val is None or val == "":
        return default
    try:
        if isinstance(val, (int, float)):
            return float(val)
        clean = str(val).replace(",", ".").strip()
        f = float(clean)
        return f if not (f != f) else default  # Comprueba NaN
    except Exception:
        return default


class TradeLifecycleCard:
    def __init__(
        self,
        trade_id: str,
        channel_name: str,
        side: str,
        entry_price: float,
        created_at: str,
        sl_price: Optional[float] = None,
        tp1: Optional[float] = None,
        tp2: Optional[float] = None,
        tp3: Optional[float] = None,
        margin_usd: float = 250.00,
        lot_size: float = 0.09,
        message_id: Optional[int] = None,
        ticket_id: Optional[str] = None,
    ):
        self.trade_id = str(trade_id)
        self.message_id = message_id
        self.ticket_id = ticket_id
        self.channel_name = str(channel_name or "Chartoro FX")
        self.side = str(side).upper() if side else "BUY"
        self.entry_price = safe_num(entry_price, 2650.0) or 2650.0
        self.exit_price: Optional[float] = None
        self.margin_usd = safe_num(margin_usd, 250.0) or 250.0
        self.lot_size = safe_num(lot_size, 0.09) or 0.09
        self.pnl_usd: Optional[float] = None
        self.gross_pnl_usd: Optional[float] = None
        self.spread_cost_usd: float = 0.15
        self.commission_usd: float = 0.16
        self.net_pnl_usd: Optional[float] = None
        self.sl_price = safe_num(sl_price)
        self.initial_sl = safe_num(sl_price)
        self.tp1 = safe_num(tp1)
        self.tp2 = safe_num(tp2)
        self.tp3 = safe_num(tp3)
        self.tp1_hit = False
        self.tp2_hit = False
        self.tp3_hit = False
        self.highest_tp = 0
        self.account_tp1_hit = False
        self.account_tp2_hit = False
        self.account_tp3_hit = False
        self.highest_account_tp = 0
        self.channel_tp1_hit = False
        self.channel_tp2_hit = False
        self.channel_tp3_hit = False
        self.highest_channel_tp = 0
        self.security_exit_before_tp = False
        self.security_exit_reason: Optional[str] = None
        self.is_closed_in_broker = False
        self.status = "OPEN"  # "OPEN", "WIN", "LOSS", "PENDING_PULLBACK", "REJECTED"
        self.outcome_text = "EN CURSO"
        self.created_at = str(created_at or "")
        self.formatted_created_at = format_full_datetime(created_at)
        self.closed_at: Optional[str] = None
        self.formatted_closed_at: Optional[str] = None
        self.modifications: List[str] = []
        self.error_reason: Optional[str] = None

    def calculate_trade_costs(self) -> Tuple[Optional[float], float, float, Optional[float]]:
        """
        Calcula el desglose financiero exacto de costes para XAUUSD:
        - Spread cTrader: 0.15$ USD por onza * volumen de onzas (lot_size * 100).
        - Comisión IC Markets cTrader: 3.00$ USD por cada 100.000$ negociados por lado (apertura + cierre).
        - Ganancia Bruta: PnL generado únicamente por la distancia de cotización.
        - Beneficio/Pérdida Neto Final: Bruto - Comisión IC Markets - Spread cTrader.
        """
        gross, spread_cost, commission, net = _calculate_trade_costs(
            entry_price=self.entry_price,
            exit_price=self.exit_price,
            lot_size=self.lot_size,
            pnl_usd=self.pnl_usd,
        )
        self.spread_cost_usd = spread_cost
        self.commission_usd = commission
        self.gross_pnl_usd = gross
        self.net_pnl_usd = net
        return self.gross_pnl_usd, self.spread_cost_usd, self.commission_usd, self.net_pnl_usd

    def update_levels(self, sl_price: Optional[float] = None, tp1: Optional[float] = None, tp2: Optional[float] = None, tp3: Optional[float] = None):
        if sl_price is not None and self.sl_price is None:
            self.sl_price = safe_num(sl_price)
            self.initial_sl = self.sl_price
        if tp1 is not None and self.tp1 is None:
            self.tp1 = safe_num(tp1)
        if tp2 is not None and self.tp2 is None:
            self.tp2 = safe_num(tp2)
        if tp3 is not None and self.tp3 is None:
            self.tp3 = safe_num(tp3)

    def modify_sl(self, new_sl: float, timestamp: str):
        parsed_sl = safe_num(new_sl)
        if parsed_sl is not None:
            self.sl_price = parsed_sl
            self.modifications.append(f"SL modificado a ${parsed_sl:.2f}")

    def mark_tp_hit(self, tp_num: int, pips_text: str = "", timestamp: str = ""):
        """Registra el alcance de un Take Profit distinguiendo hitos de canal vs ejecución real en cuenta."""
        # 1. Registrar siempre el hito alcanzado por el canal de Telegram
        if tp_num >= 1:
            self.channel_tp1_hit = True
        if tp_num >= 2:
            self.channel_tp2_hit = True
        if tp_num >= 3:
            self.channel_tp3_hit = True
        self.highest_channel_tp = max(self.highest_channel_tp, tp_num)

        # 2. Si la orden ya estaba cerrada en el broker previamente:
        # No sobreescribir la ejecución real ni marcar como cobrado por la cuenta si salió en SL o BE
        if self.is_closed_in_broker or self.closed_at:
            exit_px = self.exit_price or self.entry_price
            target_tp_px = self.tp1 if tp_num == 1 else (self.tp2 if tp_num == 2 else self.tp3)
            was_stopped_early = False
            if self.side == "BUY" and target_tp_px and exit_px < (target_tp_px - 0.50):
                was_stopped_early = True
            elif self.side == "SELL" and target_tp_px and exit_px > (target_tp_px + 0.50):
                was_stopped_early = True

            if was_stopped_early:
                self.security_exit_before_tp = True
                self.security_exit_reason = f"Canal reportó TP{tp_num}, pero la posición fue cerrada previamente por seguridad en ${exit_px:.2f}"
                msg = f"ℹ️ Canal reporta TP{tp_num} ({pips_text or 'HIT'}) [Posición cerrada en ${exit_px:.2f}]"
                if msg not in self.modifications:
                    self.modifications.append(msg)
                return

        # 3. La posición estaba abierta y capturó el Take Profit
        if tp_num >= 1:
            self.tp1_hit = True
            self.account_tp1_hit = True
        if tp_num >= 2:
            self.tp2_hit = True
            self.account_tp2_hit = True
        if tp_num >= 3:
            self.tp3_hit = True
            self.account_tp3_hit = True
        self.highest_tp = max(self.highest_tp, tp_num)
        self.highest_account_tp = max(self.highest_account_tp, tp_num)
        self.status = "WIN"
        self.outcome_text = "GANADA"

        if timestamp and not self.closed_at:
            self.closed_at = str(timestamp)
            self.formatted_closed_at = format_full_datetime(timestamp)

        if tp_num == 1 and self.tp1:
            self.exit_price = self.exit_price or self.tp1
        elif tp_num == 2 and self.tp2:
            self.exit_price = self.tp2
        elif tp_num == 3 and self.tp3:
            self.exit_price = self.tp3

        if self.exit_price and self.entry_price and (self.pnl_usd is None or self.pnl_usd <= 0):
            if self.side == "BUY":
                price_diff = self.exit_price - self.entry_price
            else:
                price_diff = self.entry_price - self.exit_price
            self.pnl_usd = round(price_diff * 100.0 * self.lot_size, 2)

        msg = f"🏆 TP{tp_num} alcanzado" + (f" ({pips_text})" if pips_text else "")
        if msg not in self.modifications:
            self.modifications.append(msg)

    def close_trade(self, outcome: str, exit_price: float, outcome_text: str, timestamp: str):
        self.status = outcome if outcome in ("WIN", "LOSS", "OPEN") else "WIN"
        self.exit_price = safe_num(exit_price, self.entry_price) or self.entry_price
        self.outcome_text = outcome_text or ("GANADA" if outcome == "WIN" else "PERDIDA")
        self.closed_at = str(timestamp or "")
        self.formatted_closed_at = format_full_datetime(timestamp)

        # Cálculo de PnL base
        if self.side == "BUY":
            price_diff = self.exit_price - self.entry_price
        else:
            price_diff = self.entry_price - self.exit_price

        self.pnl_usd = round(price_diff * 100.0 * self.lot_size, 2)

    def apply_db_trade(self, db_t: Any):
        """Sincroniza la tarjeta directamente con los datos reales y oficiales del motor de trading (tabla 'trades')."""
        self.ticket_id = getattr(db_t, 'ticket_id', self.ticket_id) or self.ticket_id
        if getattr(db_t, 'raw_signal_id', None):
            self.message_id = getattr(db_t, 'raw_signal_id')
        if getattr(db_t, 'channel_name', None):
            self.channel_name = str(db_t.channel_name)
        if getattr(db_t, 'side', None):
            self.side = (db_t.side.value if hasattr(db_t.side, 'value') else str(db_t.side)).upper()

        db_entry = getattr(db_t, 'entry_price', None)
        if db_entry is not None:
            self.entry_price = float(db_entry)

        self.lot_size = safe_num(getattr(db_t, 'lot_size', None), self.lot_size) or self.lot_size
        self.margin_usd = round(self.lot_size * self.entry_price * 100.0 / 100.0, 2)

        if getattr(db_t, 'initial_sl', None):
            self.initial_sl = safe_num(db_t.initial_sl, self.initial_sl)
        if getattr(db_t, 'current_sl', None):
            self.sl_price = safe_num(db_t.current_sl, self.sl_price)
        if getattr(db_t, 'tp1', None):
            self.tp1 = safe_num(db_t.tp1, self.tp1)
        if getattr(db_t, 'tp2', None):
            self.tp2 = safe_num(db_t.tp2, self.tp2)
        if getattr(db_t, 'tp3', None):
            self.tp3 = safe_num(db_t.tp3, self.tp3)

        open_time_val = getattr(db_t, 'open_time', None)
        if open_time_val and not self.created_at:
            self.created_at = open_time_val.isoformat() if hasattr(open_time_val, 'isoformat') else str(open_time_val)
            self.formatted_created_at = format_full_datetime(open_time_val)

        st = getattr(db_t, 'status', None)
        st_str = (st.value if hasattr(st, 'value') else str(st or "")).upper()
        close_reason_str = str(getattr(db_t, 'close_reason', '') or '').upper()
        close_time_val = getattr(db_t, 'close_time', None)
        is_closed = "CLOSED" in st_str or close_time_val is not None
        realized_cash = float(getattr(db_t, 'realized_cash_pnl', 0.0) or 0.0)
        peak_px = float(getattr(db_t, 'peak_price', 0.0) or 0.0)
        close_px = float(getattr(db_t, 'close_price', 0.0) or 0.0)
        curr_sl = float(self.sl_price or 0.0)
        tp1_px = float(self.tp1 or 0.0)
        tp2_px = float(self.tp2 or 0.0)
        tp3_px = float(self.tp3 or 0.0)

        # Detección exhaustiva de TP1, TP2 y TP3 reales alcanzados por la cuenta mientras estuvo abierta
        if "TP1" in st_str or "TP2" in st_str or "TP3" in st_str or "TRAILING" in st_str or realized_cash > 0:
            self.account_tp1_hit = True
        if "TP1" in close_reason_str or "TP2" in close_reason_str or "TP3" in close_reason_str or "TRAILING" in close_reason_str:
            self.account_tp1_hit = True

        if "TP2" in st_str or "TP3" in st_str:
            self.account_tp1_hit = True
            self.account_tp2_hit = True
        if "TP2" in close_reason_str or "TP3" in close_reason_str:
            self.account_tp1_hit = True
            self.account_tp2_hit = True

        if "TP3" in st_str or "TP3" in close_reason_str:
            self.account_tp1_hit = True
            self.account_tp2_hit = True
            self.account_tp3_hit = True

        # Comprobación por niveles de precio alcanzados (Peak Price y Close Price)
        if self.side == "BUY":
            if peak_px > 0:
                if tp1_px > 0 and peak_px >= tp1_px - 0.20:
                    self.account_tp1_hit = True
                if tp2_px > 0 and peak_px >= tp2_px - 0.20:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                if tp3_px > 0 and peak_px >= tp3_px - 0.20:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                    self.account_tp3_hit = True
            if close_px > 0:
                if tp1_px > 0 and close_px >= tp1_px - 0.50:
                    self.account_tp1_hit = True
                if tp2_px > 0 and close_px >= tp2_px - 0.50:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                if tp3_px > 0 and close_px >= tp3_px - 0.50:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                    self.account_tp3_hit = True
            if curr_sl > 0 and tp2_px > 0 and curr_sl >= tp2_px - 0.50:
                self.account_tp1_hit = True
                self.account_tp2_hit = True
            elif curr_sl > 0 and tp1_px > 0 and curr_sl >= tp1_px - 0.50:
                self.account_tp1_hit = True
        else:  # SELL
            if peak_px > 0:
                if tp1_px > 0 and peak_px <= tp1_px + 0.20:
                    self.account_tp1_hit = True
                if tp2_px > 0 and peak_px <= tp2_px + 0.20:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                if tp3_px > 0 and peak_px <= tp3_px + 0.20:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                    self.account_tp3_hit = True
            if close_px > 0:
                if tp1_px > 0 and close_px <= tp1_px + 0.50:
                    self.account_tp1_hit = True
                if tp2_px > 0 and close_px <= tp2_px + 0.50:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                if tp3_px > 0 and close_px <= tp3_px + 0.50:
                    self.account_tp1_hit = True
                    self.account_tp2_hit = True
                    self.account_tp3_hit = True
            if curr_sl > 0 and tp2_px > 0 and curr_sl <= tp2_px + 0.50:
                self.account_tp1_hit = True
                self.account_tp2_hit = True
            elif curr_sl > 0 and tp1_px > 0 and curr_sl <= tp1_px + 0.50:
                self.account_tp1_hit = True

        if self.account_tp3_hit:
            self.highest_account_tp = 3
        elif self.account_tp2_hit:
            self.highest_account_tp = 2
        elif self.account_tp1_hit:
            self.highest_account_tp = 1

        # Sincronizar tpX_hit como account_tpX_hit para reflejar fielmente la ejecución de la cuenta
        self.tp1_hit = self.account_tp1_hit
        self.tp2_hit = self.account_tp2_hit
        self.tp3_hit = self.account_tp3_hit
        self.highest_tp = self.highest_account_tp

        if is_closed:
            self.is_closed_in_broker = True
            pnl_val = float(getattr(db_t, 'pnl', 0.0) or 0.0)
            self.pnl_usd = round(pnl_val, 2)
            if pnl_val > 0:
                self.status = "WIN"
                self.outcome_text = "GANADA"
            elif pnl_val < 0:
                self.status = "LOSS"
                self.outcome_text = "PERDIDA"
            else:
                self.status = "WIN"
                self.outcome_text = "BREAK-EVEN"

            self.exit_price = safe_num(close_px, self.sl_price) or self.sl_price

            if close_time_val:
                self.closed_at = close_time_val.isoformat() if hasattr(close_time_val, 'isoformat') else str(close_time_val)
                self.formatted_closed_at = format_full_datetime(close_time_val)

            # Detectar si el canal reportó TPs que la cuenta no llegó a cobrar por haberse cerrado por seguridad
            if self.highest_channel_tp > self.highest_account_tp:
                self.security_exit_before_tp = True
                self.security_exit_reason = f"Posición cerrada por seguridad en ${float(self.exit_price or 0.0):.2f} antes de TP{self.highest_channel_tp}"

            # Historial de modificaciones e hitos documentados del trade
            mods = []
            if self.account_tp3_hit:
                mods.append("🏆 TP1, TP2 y TP3 alcanzados (Runner completado)")
            elif self.account_tp2_hit:
                mods.append("🏆 TP1 y TP2 alcanzados (+75% asegurado)")
            elif self.account_tp1_hit:
                mods.append("🏆 TP1 alcanzado (+50% asegurado)")

            if self.security_exit_before_tp and self.highest_channel_tp > self.highest_account_tp:
                mods.append(f"🛡️ Salida defensiva en ${float(self.exit_price or 0.0):.2f} antes de TP{self.highest_channel_tp}")
                mods.append(f"ℹ️ El canal alcanzó hasta TP{self.highest_channel_tp} tras el cierre de seguridad")

            if realized_cash > 0:
                mods.append(f"Cobro parcial en TP (+${realized_cash:.2f} USD)")

            if "SL_HIT" in close_reason_str or "TRAILING_SL" in close_reason_str:
                entry_px = float(self.entry_price or 0.0)
                if self.side == "BUY" and curr_sl >= entry_px:
                    mods.append(f"Cierre de remanente en Break-Even + Spread (${curr_sl:.2f})")
                elif self.side == "SELL" and curr_sl <= entry_px:
                    mods.append(f"Cierre de remanente en Break-Even + Spread (${curr_sl:.2f})")
                else:
                    mods.append(f"Cierre por Stop Loss (${curr_sl:.2f})")
            elif "TP" in close_reason_str:
                mods.append(f"Cierre en Take Profit (${float(self.exit_price or 0.0):.2f})")
            elif close_reason_str:
                mods.append(f"Cierre ({close_reason_str})")

            self.modifications = mods or ([close_reason_str] if close_reason_str else [])
        else:
            # El trade se encuentra actualmente ACTIVO y EN CURSO en el motor
            self.status = "OPEN"
            self.exit_price = None
            self.pnl_usd = round(float(getattr(db_t, 'pnl', 0.0) or 0.0), 2) if getattr(db_t, 'pnl', None) is not None else None
            self.closed_at = None
            self.formatted_closed_at = None

            if "TP1" in st_str or realized_cash > 0:
                self.outcome_text = "EN CURSO (TP1 Cobrado 50% + BE)"
                self.modifications = [
                    "TP1 cobrado (50% asegurado en caja)",
                    f"SL blindado a Break-Even (${float(self.sl_price or self.entry_price):.2f})"
                ]
            elif "TP2" in st_str or self.tp2_hit:
                self.outcome_text = "EN CURSO (TP2 Cobrado 75% + Runner)"
                self.modifications = [
                    "TP1 y TP2 cobrados",
                    f"Trailing SL ajustado a ${float(self.sl_price or self.entry_price):.2f}"
                ]
            elif "TP3" in st_str or "TRAILING" in st_str or self.tp3_hit:
                self.outcome_text = "EN CURSO (Infinite Runner)"
                self.modifications = [
                    f"Trailing SL dinámico persiguiendo pico (${float(self.sl_price or self.entry_price):.2f})"
                ]
            else:
                self.outcome_text = "EN CURSO"
                self.modifications = []

    def to_dict(self) -> Dict[str, Any]:
        gross, spread, commission, net = self.calculate_trade_costs()
        return {
            "trade_id": self.trade_id,
            "message_id": self.message_id,
            "ticket_id": self.ticket_id,
            "channel_name": self.channel_name,
            "side": self.side,
            "entry_price": float(self.entry_price),
            "exit_price": float(self.exit_price) if self.exit_price is not None else None,
            "margin_usd": float(self.margin_usd),
            "lot_size": float(self.lot_size),
            "pnl_usd": float(self.pnl_usd) if self.pnl_usd is not None else None,
            "gross_pnl_usd": float(gross) if gross is not None else None,
            "spread_cost_usd": float(spread),
            "commission_usd": float(commission),
            "net_pnl_usd": float(net) if net is not None else None,
            "sl_price": float(self.sl_price) if self.sl_price is not None else None,
            "initial_sl": float(self.initial_sl) if self.initial_sl is not None else None,
            "tp1": float(self.tp1) if self.tp1 is not None else None,
            "tp2": float(self.tp2) if self.tp2 else None,
            "tp3": float(self.tp3) if self.tp3 else None,
            "tp1_hit": self.tp1_hit,
            "tp2_hit": self.tp2_hit,
            "tp3_hit": self.tp3_hit,
            "highest_tp": self.highest_tp,
            "account_tp1_hit": self.account_tp1_hit,
            "account_tp2_hit": self.account_tp2_hit,
            "account_tp3_hit": self.account_tp3_hit,
            "highest_account_tp": self.highest_account_tp,
            "channel_tp1_hit": self.channel_tp1_hit,
            "channel_tp2_hit": self.channel_tp2_hit,
            "channel_tp3_hit": self.channel_tp3_hit,
            "highest_channel_tp": self.highest_channel_tp,
            "security_exit_before_tp": self.security_exit_before_tp,
            "security_exit_reason": self.security_exit_reason,
            "status": self.status,
            "outcome_text": self.outcome_text,
            "created_at": self.created_at,
            "formatted_created_at": self.formatted_created_at,
            "closed_at": self.closed_at,
            "formatted_closed_at": self.formatted_closed_at,
            "modifications": self.modifications or [],
            "error_reason": self.error_reason,
        }
