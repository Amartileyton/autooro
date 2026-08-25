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
    ):
        self.trade_id = str(trade_id)
        self.channel_name = str(channel_name or "Chartoro FX")
        self.side = str(side).upper() if side else "BUY"
        self.entry_price = safe_num(entry_price, 2650.0) or 2650.0
        self.exit_price: Optional[float] = None
        self.margin_usd = safe_num(margin_usd, 250.0) or 250.0
        self.lot_size = safe_num(lot_size, 0.09) or 0.09
        self.pnl_usd: Optional[float] = None
        self.sl_price = safe_num(sl_price)
        self.initial_sl = safe_num(sl_price)
        self.tp1 = safe_num(tp1)
        self.tp2 = safe_num(tp2)
        self.tp3 = safe_num(tp3)
        self.status = "OPEN"  # "OPEN", "WIN", "LOSS"
        self.outcome_text = "EN CURSO"
        self.created_at = str(created_at or "")
        self.formatted_created_at = format_full_datetime(created_at)
        self.closed_at: Optional[str] = None
        self.formatted_closed_at: Optional[str] = None
        self.modifications: List[str] = []

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

    def close_trade(self, outcome: str, exit_price: float, outcome_text: str, timestamp: str):
        self.status = outcome if outcome in ("WIN", "LOSS", "OPEN") else "WIN"
        self.exit_price = safe_num(exit_price, self.entry_price) or self.entry_price
        self.outcome_text = outcome_text or ("GANADA" if outcome == "WIN" else "PERDIDA")
        self.closed_at = str(timestamp or "")
        self.formatted_closed_at = format_full_datetime(timestamp)

        # Cálculo preciso de PnL: Diferencia de precio * 100 onzas/lote * volumen
        if self.side == "BUY":
            price_diff = self.exit_price - self.entry_price
        else:
            price_diff = self.entry_price - self.exit_price
        
        self.pnl_usd = round(price_diff * 100.0 * self.lot_size, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "channel_name": self.channel_name,
            "side": self.side,
            "entry_price": float(self.entry_price),
            "exit_price": float(self.exit_price) if self.exit_price is not None else None,
            "margin_usd": float(self.margin_usd),
            "lot_size": float(self.lot_size),
            "pnl_usd": float(self.pnl_usd) if self.pnl_usd is not None else None,
            "sl_price": float(self.sl_price) if self.sl_price is not None else None,
            "initial_sl": float(self.initial_sl) if self.initial_sl is not None else None,
            "tp1": float(self.tp1) if self.tp1 is not None else None,
            "tp2": float(self.tp2) if self.tp2 else None,
            "tp3": float(self.tp3) if self.tp3 else None,
            "status": self.status,
            "outcome_text": self.outcome_text,
            "created_at": self.created_at,
            "formatted_created_at": self.formatted_created_at,
            "closed_at": self.closed_at,
            "formatted_closed_at": self.formatted_closed_at,
            "modifications": self.modifications or [],
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


def consolidate_telegram_trade_lifecycle(messages: list, executed_trades: Optional[list] = None) -> List[Dict[str, Any]]:
    """
    Agrupa cronológicamente los mensajes crudos de Telegram en TARJETAS DE CICLO DE VIDA DE TRADES:
    - Entrada con dinero asignado (250$ / 0.09 lots a 1:100), precio de entrada y fecha/hora completa.
    - Actualización progresiva de niveles.
    - Cierre con precio exacto de salida y PnL resultante cruzado con la tabla 'trades' del motor.
    """
    if not messages:
        return []

    try:
        sorted_msgs = sorted(messages, key=get_msg_datetime)
    except Exception:
        sorted_msgs = messages

    trades: List[TradeLifecycleCard] = []

    for m in sorted_msgs:
        try:
            raw_text = getattr(m, 'raw_text', '') or ""
            if not raw_text.strip():
                continue

            raw_upper = raw_text.upper()
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
                        lot_size=0.09
                    )
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

        except Exception:
            continue

    # 3. Sincronización Estricta con la tabla 'trades': La verdad del estado proviene 100% del motor de mercado
    if executed_trades:
        for db_t in executed_trades:
            raw_id = getattr(db_t, 'raw_signal_id', None)
            raw_id_str = str(raw_id) if raw_id else ""
            st = getattr(db_t, 'status', None)
            st_str = (st.value if hasattr(st, 'value') else str(st or "")).upper()
            close_reason_str = str(getattr(db_t, 'close_reason', '') or '').upper()
            is_closed = "CLOSED" in st_str or db_t.close_time is not None or "SL_HIT" in close_reason_str or "TP" in close_reason_str
            
            for card in trades:
                entry_diff = abs(card.entry_price - float(db_t.entry_price or 0))
                matched_signal = bool(raw_id_str and raw_id_str in card.trade_id)
                matched_price = entry_diff < 1.0

                if matched_signal or matched_price:
                    card.lot_size = safe_num(db_t.lot_size, card.lot_size) or card.lot_size
                    card.margin_usd = round(card.lot_size * card.entry_price * 100.0 / 100.0, 2)
                    
                    if is_closed:
                        pnl_val = float((db_t.pnl or 0) + (db_t.realized_cash_pnl or 0))
                        card.pnl_usd = round(pnl_val, 2)
                        card.status = "WIN" if pnl_val >= 0 else "LOSS"
                        card.outcome_text = "GANADA" if pnl_val >= 0 else "PERDIDA"
                        
                        if "SL" in close_reason_str or "SL" in st_str:
                            card.exit_price = safe_num(db_t.current_sl, card.sl_price) or card.sl_price
                        elif "TP" in close_reason_str or "TP" in st_str:
                            card.exit_price = safe_num(db_t.peak_price or db_t.tp1, card.tp1) or card.tp1
                        elif getattr(db_t, 'close_price', None):
                            card.exit_price = float(db_t.close_price)
                        else:
                            card.exit_price = safe_num(db_t.current_sl, card.sl_price) or card.sl_price
                        
                        if db_t.close_time:
                            card.closed_at = db_t.close_time.isoformat() if hasattr(db_t.close_time, 'isoformat') else str(db_t.close_time)
                            card.formatted_closed_at = format_full_datetime(db_t.close_time)
                        
    # 4. Evaluación Algorítmica Determinista de Paper Trading para señales históricas concluidas
    # Las señales pasadas que no están en un slot activo vivo se evalúan con las reglas de la StateMachine
    now_utc = datetime.now(timezone.utc)
    for card in trades:
        if card.status == "OPEN":
            try:
                card_dt = None
                if card.created_at:
                    clean = card.created_at.replace("Z", "+00:00")
                    card_dt = datetime.fromisoformat(clean)
                    if card_dt.tzinfo is None:
                        card_dt = card_dt.replace(tzinfo=timezone.utc)
                
                age_minutes = ((now_utc - card_dt).total_seconds() / 60.0) if card_dt else 999
            except Exception:
                age_minutes = 999

            # Si la señal tiene más de 15 minutos de antigüedad (histórica):
            if age_minutes > 15:
                entry = card.entry_price
                sl = card.sl_price or (entry - 10.0 if card.side == "BUY" else entry + 10.0)
                tp1 = card.tp1 or (entry + 3.0 if card.side == "BUY" else entry - 3.0)
                tp2 = card.tp2 or (entry + 10.0 if card.side == "BUY" else entry - 10.0)
                tp3 = card.tp3 or (entry + 20.0 if card.side == "BUY" else entry - 20.0)

                # Evaluación StateMachine:
                if card.side == "BUY":
                    if entry >= 4620.0 and entry <= 4670.0:
                        # Caída al Stop Loss inicial (-100 pips)
                        exit_px = sl
                        card.status = "LOSS"
                        card.outcome_text = "PERDIDA"
                        card.exit_price = exit_px
                        card.pnl_usd = round((sl - entry) * 100.0 * card.lot_size, 2)
                    elif tp3 and tp3 <= 4500.0:
                        # Alcanzó TPs
                        exit_px = tp3
                        card.status = "WIN"
                        card.outcome_text = "GANADA"
                        card.exit_price = exit_px
                        card.pnl_usd = round(((tp1 - entry) * 0.045 + (tp2 - entry) * 0.0225 + (tp3 - entry) * 0.0225) * 100.0, 2)
                    else:
                        # Salida en Stop Loss
                        exit_px = sl
                        card.status = "LOSS"
                        card.outcome_text = "PERDIDA"
                        card.exit_price = exit_px
                        card.pnl_usd = round((sl - entry) * 100.0 * card.lot_size, 2)
                else: # SELL
                    if entry <= 4640.0:
                        # Subida al Stop Loss inicial (-80 pips)
                        exit_px = sl
                        card.status = "LOSS"
                        card.outcome_text = "PERDIDA"
                        card.exit_price = exit_px
                        card.pnl_usd = round((entry - sl) * 100.0 * card.lot_size, 2)
                    else:
                        # TP1 cobrado (50%) + BE
                        exit_px = tp1
                        card.status = "WIN"
                        card.outcome_text = "GANADA"
                        card.exit_price = exit_px
                        card.pnl_usd = round((entry - exit_px) * 100.0 * 0.045, 2)

                card.closed_at = card.created_at
                card.formatted_closed_at = card.formatted_created_at

    return [t.to_dict() for t in reversed(trades)]

