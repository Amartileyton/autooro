from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, OrderSide
from backend.ingesta.parser import parse_signal

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


import re

RE_TP_HIT = re.compile(
    r'(?:#|\b)?(?:XAUUSD|GOLD|ORO)?\s*(?:TAKE\s*PROFIT|TP|TARGET|OBJETIVO)\s*([1-5])\s*(?:HIT|ALCANZADO|TOCADO|DONE|SUPERADO|RUNNING|\+?\d+\s*PIPS)',
    re.IGNORECASE
)
RE_PIPS_EXTRACT = re.compile(r'(\+\d+\s*PIPS?)', re.IGNORECASE)


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
        oz = float(self.lot_size or 0.01) * 100.0
        entry_px = float(self.entry_price or 2650.0)
        exit_px = float(self.exit_price or entry_px)

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

        self.spread_cost_usd = spread_cost
        self.commission_usd = commission

        if self.pnl_usd is not None:
            gross = round(float(self.pnl_usd), 2)
            # El beneficio o pérdida final entrega el valor con comisiones y spreads ya descontados
            net = round(gross - commission - spread_cost, 2)
            self.gross_pnl_usd = gross
            self.net_pnl_usd = net
        else:
            self.gross_pnl_usd = None
            self.net_pnl_usd = None

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
        """Registra el alcance de un Take Profit (TP1, TP2, TP3...) y actualiza el estado."""
        if tp_num >= 1:
            self.tp1_hit = True
        if tp_num >= 2:
            self.tp2_hit = True
        if tp_num >= 3:
            self.tp3_hit = True
        self.highest_tp = max(self.highest_tp, tp_num)
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

        # Detección exhaustiva de TP1, TP2 y TP3
        if "TP1" in st_str or "TP2" in st_str or "TP3" in st_str or "TRAILING" in st_str or realized_cash > 0:
            self.tp1_hit = True
        if "TP1" in close_reason_str or "TP2" in close_reason_str or "TP3" in close_reason_str or "TRAILING" in close_reason_str:
            self.tp1_hit = True

        if "TP2" in st_str or "TP3" in st_str:
            self.tp1_hit = True
            self.tp2_hit = True
        if "TP2" in close_reason_str or "TP3" in close_reason_str:
            self.tp1_hit = True
            self.tp2_hit = True

        if "TP3" in st_str or "TP3" in close_reason_str:
            self.tp1_hit = True
            self.tp2_hit = True
            self.tp3_hit = True

        # Comprobación por niveles de precio (Peak Price y Close Price)
        if self.side == "BUY":
            if peak_px > 0:
                if tp1_px > 0 and peak_px >= tp1_px - 0.20:
                    self.tp1_hit = True
                if tp2_px > 0 and peak_px >= tp2_px - 0.20:
                    self.tp1_hit = True
                    self.tp2_hit = True
                if tp3_px > 0 and peak_px >= tp3_px - 0.20:
                    self.tp1_hit = True
                    self.tp2_hit = True
                    self.tp3_hit = True
            if close_px > 0:
                if tp1_px > 0 and close_px >= tp1_px - 0.50:
                    self.tp1_hit = True
                if tp2_px > 0 and close_px >= tp2_px - 0.50:
                    self.tp1_hit = True
                    self.tp2_hit = True
                if tp3_px > 0 and close_px >= tp3_px - 0.50:
                    self.tp1_hit = True
                    self.tp2_hit = True
                    self.tp3_hit = True
            if curr_sl > 0 and tp1_px > 0 and curr_sl >= tp1_px - 0.50:
                self.tp1_hit = True
                self.tp2_hit = True
        else:  # SELL
            if peak_px > 0:
                if tp1_px > 0 and peak_px <= tp1_px + 0.20:
                    self.tp1_hit = True
                if tp2_px > 0 and peak_px <= tp2_px + 0.20:
                    self.tp1_hit = True
                    self.tp2_hit = True
                if tp3_px > 0 and peak_px <= tp3_px + 0.20:
                    self.tp1_hit = True
                    self.tp2_hit = True
                    self.tp3_hit = True
            if close_px > 0:
                if tp1_px > 0 and close_px <= tp1_px + 0.50:
                    self.tp1_hit = True
                if tp2_px > 0 and close_px <= tp2_px + 0.50:
                    self.tp1_hit = True
                    self.tp2_hit = True
                if tp3_px > 0 and close_px <= tp3_px + 0.50:
                    self.tp1_hit = True
                    self.tp2_hit = True
                    self.tp3_hit = True
            if curr_sl > 0 and tp1_px > 0 and curr_sl <= tp1_px + 0.50:
                self.tp1_hit = True
                self.tp2_hit = True

        if self.tp3_hit:
            self.highest_tp = 3
        elif self.tp2_hit:
            self.highest_tp = 2
        elif self.tp1_hit:
            self.highest_tp = 1

        if is_closed:
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

            # Historial de modificaciones e hitos documentados del trade
            mods = []
            if self.tp3_hit:
                mods.append(f"🏆 TP1, TP2 y TP3 alcanzados (Runner completado)")
            elif self.tp2_hit:
                mods.append(f"🏆 TP1 y TP2 alcanzados (+75% asegurado)")
            elif self.tp1_hit:
                mods.append(f"🏆 TP1 alcanzado (+50% asegurado)")

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
            "status": self.status,
            "outcome_text": self.outcome_text,
            "created_at": self.created_at,
            "formatted_created_at": self.formatted_created_at,
            "closed_at": self.closed_at,
            "formatted_closed_at": self.formatted_closed_at,
            "modifications": self.modifications or [],
            "error_reason": self.error_reason,
        }


def get_msg_datetime(msg: Any) -> datetime:
    """Extrae el datetime UTC garantizando compatibilidad total de comparación."""
    val = getattr(msg, 'received_at', None)
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=timezone.utc)
        return val.astimezone(timezone.utc)
    if isinstance(val, str) and val.strip():
        try:
            clean = val.strip().replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)
    return datetime.min.replace(tzinfo=timezone.utc)


def get_card_timestamp(c: TradeLifecycleCard) -> datetime:
    """Extrae la fecha/hora más relevante para ordenar las tarjetas (más reciente primero)."""
    for raw_dt in [c.closed_at, c.created_at]:
        if raw_dt:
            try:
                clean = str(raw_dt).replace("Z", "+00:00")
                dt = datetime.fromisoformat(clean)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                pass
    return datetime.min.replace(tzinfo=timezone.utc)


def consolidate_telegram_trade_lifecycle(messages: list, executed_trades: Optional[list] = None) -> List[Dict[str, Any]]:
    """
    Agrupa y sincroniza cronológicamente los mensajes de Telegram y los trades ejecutados en la base de datos:
    - Las tarjetas sincronizan 100% sus métricas de PnL (ganancias y pérdidas reales descontadas/añadidas).
    - Multi-pass matching exacto para vincular trades de BD con tarjetas de señales sin falsos duplicados ni sobrescrituras.
    - Sincroniza hitos de Take Profit alcanzados (TP1, TP2, TP3) desde avisos de Telegram y base de datos.
    - Ordena estrictamente de más reciente a más antiguo garantizando que los últimos trades siempre aparezcan al inicio.
    """
    if not messages and not executed_trades:
        return []

    try:
        sorted_msgs = sorted(messages, key=get_msg_datetime)
    except Exception:
        sorted_msgs = messages or []

    trades: List[TradeLifecycleCard] = []

    for m in sorted_msgs:
        try:
            raw_text = getattr(m, 'raw_text', '') or ""
            if not raw_text.strip():
                continue

            channel = getattr(m, 'channel_name', None) or "Chartoro FX"
            channel_id = getattr(m, 'channel_id', 0) or 0
            msg_dt = get_msg_datetime(m)
            time_str = msg_dt.isoformat()
            msg_id = getattr(m, 'message_id', 0) or getattr(m, 'id', 0) or 0
            
            parsed = parse_signal(raw_text, message_id=msg_id, channel_id=channel_id, channel_name=channel)

            # 1. ¿Es una orden nueva?
            if isinstance(parsed, TradingSignalEvent):
                side = parsed.side.value if hasattr(parsed.side, 'value') else str(parsed.side)
                entry = safe_num(parsed.entry_price)
                if not entry or entry <= 0:
                    continue

                sl = safe_num(parsed.sl_price)
                tp1 = safe_num(parsed.tp_levels[0]) if len(parsed.tp_levels) > 0 else None
                tp2 = safe_num(parsed.tp_levels[1]) if len(parsed.tp_levels) > 1 else None
                tp3 = safe_num(parsed.tp_levels[2]) if len(parsed.tp_levels) > 2 else None

                # Buscar si ya existe un trade abierto en el MISMO canal en la misma dirección y precio similar
                existing_trade = None
                for t in reversed(trades):
                    if t.status == "OPEN" and t.channel_name == channel and t.side == side and abs(t.entry_price - entry) <= 3.0:
                        existing_trade = t
                        break

                if existing_trade:
                    existing_trade.update_levels(sl_price=sl, tp1=tp1, tp2=tp2, tp3=tp3)
                else:
                    new_card = TradeLifecycleCard(
                        trade_id=f"trade-{msg_id}-{int(entry)}",
                        channel_name=channel,
                        side=side,
                        entry_price=entry,
                        sl_price=sl,
                        tp1=tp1,
                        tp2=tp2,
                        tp3=tp3,
                        created_at=time_str,
                        margin_usd=250.00,
                        lot_size=0.09,
                        message_id=msg_id
                    )
                    new_card.error_reason = getattr(m, 'error_reason', None)
                    trades.append(new_card)

            # 2. ¿Es un modificador explícito de niveles (Move SL / Set BE)?
            elif isinstance(parsed, ModifierSignalEvent):
                for t in reversed(trades):
                    if t.status == "OPEN" and t.channel_name == channel:
                        if parsed.signal_type == SignalType.MOVE_BE:
                            t.modify_sl(t.entry_price, time_str)
                        elif parsed.target_price:
                            target_sl = safe_num(parsed.target_price)
                            if target_sl:
                                t.modify_sl(target_sl, time_str)
                        break

            # 3. ¿Es un mensaje informativo de TP alcanzado (ej. "TP1 HIT, +30 Pips", "TP2 HIT, +80 Pips")?
            else:
                tp_hit_m = RE_TP_HIT.search(raw_text)
                if tp_hit_m:
                    tp_num = int(tp_hit_m.group(1))
                    pips_m = RE_PIPS_EXTRACT.search(raw_text)
                    pips_txt = pips_m.group(1) if pips_m else ""
                    for t in reversed(trades):
                        if t.channel_name == channel and (t.status == "OPEN" or t.status == "WIN"):
                            t.mark_tp_hit(tp_num, pips_txt, time_str)
                            break

        except Exception:
            continue

    # 3. Sincronización Multi-Pass con la tabla 'trades' del motor de mercado
    matched_card_ids = set()
    matched_db_ids = set()

    if executed_trades:
        # Pase 1: Coincidencia exacta por raw_signal_id / message_id
        for db_t in executed_trades:
            raw_id = getattr(db_t, 'raw_signal_id', None)
            if not raw_id:
                continue

            for card in trades:
                if id(card) in matched_card_ids:
                    continue
                if card.message_id == raw_id or f"-{raw_id}-" in f"-{card.trade_id}-":
                    card.apply_db_trade(db_t)
                    matched_card_ids.add(id(card))
                    matched_db_ids.add(getattr(db_t, 'id', id(db_t)))
                    break

        # Pase 2: Coincidencia por canal, dirección y precio cercano (dentro de 3.0 USD)
        for db_t in executed_trades:
            db_id = getattr(db_t, 'id', id(db_t))
            if db_id in matched_db_ids:
                continue

            db_side = (db_t.side.value if hasattr(db_t.side, 'value') else str(db_t.side or "")).upper()
            db_entry = float(getattr(db_t, 'entry_price', 0.0) or 0.0)
            db_channel = str(getattr(db_t, 'channel_name', '') or '').lower()

            best_card = None
            best_diff = 999.0
            for card in reversed(trades):
                if id(card) in matched_card_ids:
                    continue
                if card.side.upper() == db_side:
                    card_channel = str(card.channel_name or '').lower()
                    channel_match = (db_channel in card_channel or card_channel in db_channel) if (db_channel and card_channel) else True
                    diff = abs(card.entry_price - db_entry)
                    if channel_match and diff <= 3.0 and diff < best_diff:
                        best_diff = diff
                        best_card = card

            if best_card:
                best_card.apply_db_trade(db_t)
                matched_card_ids.add(id(best_card))
                matched_db_ids.add(db_id)

        # Pase 3: Para trades en DB sin tarjeta asociada en raw_messages, crear la tarjeta directamente
        for db_t in executed_trades:
            db_id = getattr(db_t, 'id', id(db_t))
            if db_id in matched_db_ids:
                continue

            db_side = (db_t.side.value if hasattr(db_t.side, 'value') else str(db_t.side or "")).upper()
            db_entry = float(getattr(db_t, 'entry_price', 0.0) or 0.0)
            open_time_val = getattr(db_t, 'open_time', None)
            open_time_str = open_time_val.isoformat() if hasattr(open_time_val, 'isoformat') else str(open_time_val or "")
            
            new_card = TradeLifecycleCard(
                trade_id=f"trade-db-{getattr(db_t, 'id', '0')}-{getattr(db_t, 'ticket_id', 'TKT')}",
                channel_name=getattr(db_t, 'channel_name', None) or "Chartoro FX",
                side=db_side,
                entry_price=db_entry,
                sl_price=safe_num(getattr(db_t, 'current_sl', None)),
                tp1=safe_num(getattr(db_t, 'tp1', None)),
                tp2=safe_num(getattr(db_t, 'tp2', None)),
                tp3=safe_num(getattr(db_t, 'tp3', None)),
                created_at=open_time_str,
                margin_usd=round(float(getattr(db_t, 'lot_size', 0.03)) * db_entry * 100.0 / 100.0, 2),
                lot_size=float(getattr(db_t, 'lot_size', 0.03)),
                message_id=getattr(db_t, 'raw_signal_id', None),
                ticket_id=getattr(db_t, 'ticket_id', None)
            )
            new_card.apply_db_trade(db_t)
            matched_card_ids.add(id(new_card))
            matched_db_ids.add(db_id)
            trades.append(new_card)

    # 4. Señales no ejecutadas: clasificar si están en espera de retroceso (Pullback) o rechazadas
    for card in trades:
        if id(card) not in matched_card_ids:
            if card.error_reason and "PULLBACK" in card.error_reason and "EN ESPERA" in card.error_reason:
                card.status = "PENDING_PULLBACK"
                card.outcome_text = card.error_reason or "EN ESPERA (PULLBACK)"
                card.modifications = ["Vigilando retroceso hacia rango de entrada..."]
            else:
                card.status = "REJECTED"
                card.outcome_text = card.error_reason or "FUERA PRECIO"
                # Limpiar cualquier PnL teórico para garantizar que no se confunda con balance real
                card.pnl_usd = None
                card.gross_pnl_usd = None
                card.net_pnl_usd = None
                if not card.modifications:
                    card.modifications = [f"Orden no ejecutada: {card.outcome_text}"]

    # 5. Ordenación cronológica estricta: los trades más recientes van SIEMPRE al inicio
    trades.sort(key=get_card_timestamp, reverse=True)

    return [t.to_dict() for t in trades]



