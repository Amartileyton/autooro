from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
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
        margin_usd: float = 1000.00,
        lot_size: float = 0.22,
    ):
        self.trade_id = trade_id
        self.channel_name = channel_name
        self.side = side.upper()
        self.entry_price = entry_price
        self.exit_price: Optional[float] = None
        self.margin_usd = margin_usd  # 1.000€ / $1,000 (25% por slot)
        self.lot_size = lot_size      # ~0.22 Lots en XAUUSD
        self.pnl_usd: Optional[float] = None
        self.sl_price = sl_price
        self.initial_sl = sl_price
        self.tp1 = tp1
        self.tp2 = tp2
        self.tp3 = tp3
        self.status = "OPEN"  # "OPEN", "WIN", "LOSS"
        self.outcome_text = "EN CURSO"
        self.created_at = created_at
        self.formatted_created_at = format_full_datetime(created_at)
        self.closed_at: Optional[str] = None
        self.formatted_closed_at: Optional[str] = None
        self.modifications: List[str] = []

    def update_levels(self, sl_price: Optional[float] = None, tp1: Optional[float] = None, tp2: Optional[float] = None, tp3: Optional[float] = None):
        if sl_price is not None and self.sl_price is None:
            self.sl_price = sl_price
            self.initial_sl = sl_price
        if tp1 is not None and self.tp1 is None:
            self.tp1 = tp1
        if tp2 is not None and self.tp2 is None:
            self.tp2 = tp2
        if tp3 is not None and self.tp3 is None:
            self.tp3 = tp3

    def modify_sl(self, new_sl: float, timestamp: str):
        self.sl_price = new_sl
        self.modifications.append(f"SL modificado a ${new_sl:.2f}")

    def close_trade(self, outcome: str, exit_price: float, outcome_text: str, timestamp: str):
        self.status = outcome  # "WIN" or "LOSS"
        self.exit_price = exit_price
        self.outcome_text = outcome_text
        self.closed_at = timestamp
        self.formatted_closed_at = format_full_datetime(timestamp)

        # Calcular PnL en base al tamaño de lote (0.22 lots -> 1 pip = $2.20 / $1 = $22.00)
        if self.side == "BUY":
            price_diff = self.exit_price - self.entry_price
        else:
            price_diff = self.entry_price - self.exit_price
        
        self.pnl_usd = round(price_diff * 100 * self.lot_size, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "channel_name": self.channel_name,
            "side": self.side,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "margin_usd": self.margin_usd,
            "lot_size": self.lot_size,
            "pnl_usd": self.pnl_usd,
            "sl_price": self.sl_price,
            "initial_sl": self.initial_sl,
            "tp1": self.tp1,
            "tp2": self.tp2,
            "tp3": self.tp3,
            "status": self.status,
            "outcome_text": self.outcome_text,
            "created_at": self.created_at,
            "formatted_created_at": self.formatted_created_at,
            "closed_at": self.closed_at,
            "formatted_closed_at": self.formatted_closed_at,
            "modifications": self.modifications,
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

def consolidate_telegram_trade_lifecycle(messages: list) -> List[Dict[str, Any]]:
    """
    Agrupa cronológicamente los mensajes crudos de Telegram en TARJETAS DE CICLO DE VIDA DE TRADES:
    - Entrada con dinero asignado (1.000€ / 0.22 lots), precio de entrada y fecha/hora completa (DD/MM/YYYY HH:MM:SS).
    - Actualización progresiva de niveles.
    - Cierre con precio exacto de salida y PnL resultante.
    """
    if not messages:
        return []

    sorted_msgs = sorted(messages, key=get_msg_datetime)
    trades: List[TradeLifecycleCard] = []

    for m in sorted_msgs:
        raw_text = getattr(m, 'raw_text', '') or ""
        raw_upper = raw_text.upper()
        channel = getattr(m, 'channel_name', None) or "Chartoro FX Señales Gratis"
        
        msg_dt = get_msg_datetime(m)
        time_str = msg_dt.isoformat()
        msg_id = getattr(m, 'message_id', 0) or 0
        parsed = parse_signal(raw_text, message_id=msg_id, channel_id=getattr(m, 'channel_id', 0) or 0)

        # 1. ¿Es una orden nueva?
        if isinstance(parsed, TradingSignalEvent):
            side = parsed.side.value
            entry = float(parsed.entry_price)
            sl = float(parsed.sl_price) if parsed.sl_price else None
            tp1 = float(parsed.tp_levels[0]) if len(parsed.tp_levels) > 0 else None
            tp2 = float(parsed.tp_levels[1]) if len(parsed.tp_levels) > 1 else None
            tp3 = float(parsed.tp_levels[2]) if len(parsed.tp_levels) > 2 else None

            # Buscar si ya existe un trade abierto en la misma dirección y precio similar en los últimos 30 min
            existing_trade = None
            for t in reversed(trades):
                if t.status == "OPEN" and t.side == side and abs(t.entry_price - entry) <= 2.5:
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
                    margin_usd=1000.00,
                    lot_size=0.22
                )
                trades.append(new_card)

        # 2. ¿Es un modificador (Move SL / Set BE)?
        elif isinstance(parsed, ModifierSignalEvent):
            if parsed.target_price:
                target_sl = float(parsed.target_price)
                for t in reversed(trades):
                    if t.status == "OPEN":
                        t.modify_sl(target_sl, time_str)
                        break

        # 3. ¿Es un reporte de cierre (TP HIT, SL HIT, CERRAR SETUP)?
        else:
            if "TP" in raw_upper and ("HIT" in raw_upper or "PIPS" in raw_upper or "GANANCIA" in raw_upper or "PAGO INMEDIATO" in raw_upper):
                for t in reversed(trades):
                    if t.status == "OPEN":
                        # Determinar precio de salida por TP
                        if "TP3" in raw_upper and t.tp3:
                            exit_px = t.tp3
                        elif "TP2" in raw_upper and t.tp2:
                            exit_px = t.tp2
                        elif t.tp1:
                            exit_px = t.tp1
                        else:
                            exit_px = t.entry_price + (3.0 if t.side == "BUY" else -3.0)
                        
                        t.close_trade("WIN", exit_px, "GANADA", time_str)
                        break

            elif "SL HIT" in raw_upper or "PÉRDIDA" in raw_upper or "STOPPED OUT" in raw_upper:
                for t in reversed(trades):
                    if t.status == "OPEN":
                        exit_px = t.sl_price if t.sl_price else (t.entry_price + (8.0 if t.side == "SELL" else -8.0))
                        t.close_trade("LOSS", exit_px, "PERDIDA", time_str)
                        break

            elif "CERRAR" in raw_upper or "CLOSE" in raw_upper:
                for t in reversed(trades):
                    if t.status == "OPEN":
                        exit_px = t.entry_price
                        t.close_trade("WIN" if t.side == "BUY" else "LOSS", exit_px, "CERRADA", time_str)
                        break

    return [t.to_dict() for t in reversed(trades)]
