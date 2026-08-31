"""Sincronización multi-pass entre mensajes de Telegram y trades de la base de datos.

Extraído de ``ingesta/trade_lifecycle.py`` (Zero-Regression): agrupa señales,
aplica modificadores (Move SL / Break-Even), detecta hitos de Take Profit y
vincula las tarjetas con los trades ejecutados en el motor (tabla ``trades``).
"""
import re
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from backend.ingesta.parser import parse_signal
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, SignalType
from backend.models.card import safe_num, TradeLifecycleCard


RE_TP_HIT = re.compile(
    r'(?:#|\b)?(?:XAUUSD|GOLD|ORO)?\s*(?:TAKE\s*PROFIT|TP|TARGET|OBJETIVO)\s*([1-5])\s*(?:HIT|ALCANZADO|TOCADO|DONE|SUPERADO|RUNNING|\+?\d+\s*PIPS)',
    re.IGNORECASE
)
RE_PIPS_EXTRACT = re.compile(r'(\+\d+\s*PIPS?)', re.IGNORECASE)


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
    from datetime import timedelta
    from backend.config import settings
    now_utc = datetime.now(timezone.utc)
    timeout_mins = getattr(settings, 'PULLBACK_TIMEOUT_MINUTES', 15)

    for card in trades:
        if id(card) not in matched_card_ids:
            is_pb = bool(card.error_reason and "PULLBACK" in card.error_reason and "EN ESPERA" in card.error_reason)
            card_dt = get_card_timestamp(card)
            # Si tiene timestamp válido, comprobar si han pasado más de 15 minutos
            is_expired = False
            if card_dt != datetime.min.replace(tzinfo=timezone.utc):
                is_expired = (now_utc - card_dt) > timedelta(minutes=timeout_mins)

            if is_pb and not is_expired:
                card.status = "PENDING_PULLBACK"
                card.outcome_text = card.error_reason or "EN ESPERA (PULLBACK)"
                card.modifications = ["Vigilando retroceso hacia rango de entrada..."]
            elif is_pb and is_expired:
                card.status = "REJECTED"
                card.outcome_text = "FUERA PRECIO (TIMEOUT PULLBACK)"
                card.pnl_usd = None
                card.gross_pnl_usd = None
                card.net_pnl_usd = None
                card.modifications = [f"Timeout de retroceso ({timeout_mins} min) expirado sin volver a rango"]
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
