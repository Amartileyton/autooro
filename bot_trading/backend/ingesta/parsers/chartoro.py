import re
import logging
from decimal import Decimal
from typing import Optional, Union, List, Tuple
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType, ParserType
)
from backend.ingesta.parsers.base import BaseSignalParser, sanitize_price_str

logger = logging.getLogger("trading_bot.parser.chartoro")

# Regex compilados para máxima velocidad (< 0.05 ms)
RE_ASSET = re.compile(r'(?:#|\b)(XAUUSD|XAU/USD|XAU|GOLD|ORO)\b', re.IGNORECASE)

# Prioridad a Palabras Clave explícitas sobre emojis decorativos
RE_KEYWORD_BUY = re.compile(r'(?:#|\b)(BUY|LONG|COMPRA|COMPRAR)\b', re.IGNORECASE)
RE_KEYWORD_SELL = re.compile(r'(?:#|\b)(SELL|SHORT|VENTA|VENDER)\b', re.IGNORECASE)
RE_EMOJI_BUY = re.compile(r'[🟢🔼⬆️🚀]', re.IGNORECASE)
RE_EMOJI_SELL = re.compile(r'[🔴🔽⬇️]', re.IGNORECASE)

RE_IGNORE_INFORMATIONAL = re.compile(
    r'\b(TP[1-5]\s+HIT|SL\s+HIT|TP\s+CARGANDO|GANANCIAS\s+TEMPRANAS|ACCESO\s+VIP|'
    r'UNIRTE|RECLAMA|MENTOR|MENTORÍA|MIEMBROS\s+VIP|SEÑALES\s+PREMIUM|'
    r'COPIAR.*PEGAR|TRANSPARENCIA|CONFIGURACIONES\s+CON)\b',
    re.IGNORECASE
)

RE_PRICE_PATTERN = r'(?:[0-9]{1,2}[.,][0-9]{3}(?:[.,][0-9]+)?|[0-9]{4}(?:[.,][0-9]+)?)'
RE_MOVE_SL = re.compile(
    rf'(?:MOVE|SET|SHIFT|UPDATE|MOVER|AJUSTAR)\s*(?:YOUR\s+|TU\s+)?(?:STOP\s*LOSS|SOP\s*LOSS|STP\s*LOSS|SL)\s*(?:TO|A|AT|->|:|\s)\s*({RE_PRICE_PATTERN})'
    rf'|(?:SL|SOP|STOP)\s*(?:TO|A|AT|->)\s*({RE_PRICE_PATTERN})',
    re.IGNORECASE
)
RE_MOVE_BE = re.compile(r'\b(SET\s+BE|MOVE\s+SL\s+TO\s+BREAK[-\s]?EVEN|MOVER\s+A\s+BE|BREAK[-\s]?EVEN|BE)\b', re.IGNORECASE)
RE_CLOSE = re.compile(
    r'(?:CLOSE\s+NOW|CLOSE\s+ORDER|CLOSE\s+SETUP|CLOSE\s+TRADE|'
    r'CERRAR\s+AHORA|CERRAR\s+ORDEN|CERRAR\s+(?:EL\s+)?SETUP|'
    r'CERRAMOS\s+(?:LA\s+)?OPERACI[OÓ]N|CERRAMOS\s+SETUP|CERRAR\s+OPERACI[OÓ]N|'
    r'CERRAR\s+POSICI[OÓ]N|CERRAR\s+TODO|CANCELAR\s+ORDEN|'
    r'CLOSE\s+(\d+)%|CERRAR\s+(\d+)%|CERRAR\s+PARCIAL)',
    re.IGNORECASE
)

RE_ENTRY_EXPLICIT = re.compile(rf'(?:ENTRY\s*POINT|ENTRY\s*PRICE|ENTRADA|PRECIO|ENTRY|OPEN|@|NOW)[*_~:\s]*[:@\s]*[*_~:\s]*({RE_PRICE_PATTERN})', re.IGNORECASE)
RE_SL_EXPLICIT = re.compile(rf'(?:STOP\s*LOSS\s*(?:\(SL\))?|SOP\s*LOSS|STP\s*LOSS|STOP|SOP|STP|S[./\s]*L)[*_~:\s]*[:=@\s\-]*[*_~:\s]*({RE_PRICE_PATTERN})', re.IGNORECASE)
RE_TP_NUMBERED = re.compile(rf'(?:TAKE\s*PROFIT|TP|TARGET|OBJETIVO|T)[*_~:\s]*([1-5])[*_~:\s]*[:=@\s\-]*[*_~:\s]*({RE_PRICE_PATTERN})', re.IGNORECASE)
RE_TP_GENERIC = re.compile(rf'(?:TAKE\s*PROFITS?|TPS?|TARGETS?|OBJETIVOS?)[*_~:\s]*[:=@\s]*({RE_PRICE_PATTERN}(?:\s*[,/\-\n\s]+\s*{RE_PRICE_PATTERN})*)', re.IGNORECASE)
RE_TP_PIPS = re.compile(r'(?:TP[1-5]?|SET\s+TP[1-5]?)[*_~:\s]*[:@\s]*\+?(\d+)\s*PIPS?', re.IGNORECASE)
RE_ALL_NUMBERS = re.compile(r'\b[0-9]{1,2}[.,][0-9]{3}(?:[.,][0-9]+)?\b|\b[0-9]{4}(?:[.,][0-9]+)?\b')


class ChartoroParser(BaseSignalParser):
    """Parser determinista de alto rendimiento para el canal Chartoro FX."""

    def parse(
        self,
        raw_text: str,
        message_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        channel_name: Optional[str] = "Chartoro FX",
        execution_mode: str = "AUDIT",
        reply_to_msg_id: Optional[int] = None
    ) -> Optional[Union[TradingSignalEvent, ModifierSignalEvent]]:
        if not raw_text or len(raw_text.strip()) < 8:
            return None

        cleaned_text = raw_text.strip()

        # 1. Modificadores
        modifier_event = self._check_modifiers(cleaned_text, message_id, channel_id, channel_name, execution_mode, reply_to_msg_id)
        if modifier_event:
            return modifier_event

        # 2. Descartar spam/informativos
        if RE_IGNORE_INFORMATIONAL.search(cleaned_text):
            return None

        # 3. Comprobar activo XAUUSD
        if not RE_ASSET.search(cleaned_text):
            raw_nums = RE_ALL_NUMBERS.findall(cleaned_text)
            sanitized_nums = [sanitize_price_str(n) for n in raw_nums]
            valid_nums = [n for n in sanitized_nums if n is not None and n >= Decimal("1500")]
            if len(valid_nums) < 2:
                return None

        # 4. Dirección BUY / SELL
        side = self._determine_order_side(cleaned_text)
        if not side:
            return None

        # 5. Precio de entrada
        entry_price = self._extract_entry_price(cleaned_text)
        if not entry_price:
            return None

        # 6. Stop Loss
        sl_price, requires_dynamic_sl = self._extract_sl(cleaned_text)

        # 7. Take Profits
        tp_levels = self._extract_tps(cleaned_text, entry_price, side)
        if not tp_levels:
            return None

        # 8. Validación matemática
        tp1 = tp_levels[0]
        if side == OrderSide.BUY and tp1 <= entry_price:
            logger.warning(f"Señal Chartoro BUY rechazada por TP1 incoherente: {tp1} <= {entry_price}")
            return None
        elif side == OrderSide.SELL and tp1 >= entry_price:
            logger.warning(f"Señal Chartoro SELL rechazada por TP1 incoherente: {tp1} >= {entry_price}")
            return None

        if not requires_dynamic_sl and sl_price is not None:
            if side == OrderSide.BUY and sl_price >= entry_price:
                logger.warning(f"Chartoro: Errata en SL para BUY ({sl_price} >= {entry_price}). Aplicando SL dinámico.")
                sl_price = None
                requires_dynamic_sl = True
            elif side == OrderSide.SELL and sl_price <= entry_price:
                logger.warning(f"Chartoro: Errata en SL para SELL ({sl_price} <= {entry_price}). Aplicando SL dinámico.")
                sl_price = None
                requires_dynamic_sl = True

        return TradingSignalEvent(
            asset="XAUUSD",
            side=side,
            entry_price=entry_price,
            sl_price=sl_price,
            tp_levels=tp_levels,
            requires_dynamic_sl=requires_dynamic_sl,
            parser_type=ParserType.REGEX,
            raw_text=raw_text,
            message_id=message_id,
            channel_id=channel_id,
            channel_name=channel_name or "Chartoro FX",
            execution_mode=execution_mode
        )

    def _determine_order_side(self, text: str) -> Optional[OrderSide]:
        has_kw_buy = bool(RE_KEYWORD_BUY.search(text))
        has_kw_sell = bool(RE_KEYWORD_SELL.search(text))
        if has_kw_buy and not has_kw_sell:
            return OrderSide.BUY
        if has_kw_sell and not has_kw_buy:
            return OrderSide.SELL
        if has_kw_buy and has_kw_sell:
            pos_b = RE_KEYWORD_BUY.search(text).start()
            pos_s = RE_KEYWORD_SELL.search(text).start()
            return OrderSide.BUY if pos_b < pos_s else OrderSide.SELL
        if RE_EMOJI_BUY.search(text):
            return OrderSide.BUY
        if RE_EMOJI_SELL.search(text):
            return OrderSide.SELL
        return None

    def _check_modifiers(self, text: str, message_id: Optional[int], channel_id: Optional[int], channel_name: Optional[str], execution_mode: str, reply_to_msg_id: Optional[int]) -> Optional[ModifierSignalEvent]:
        match_sl = RE_MOVE_SL.search(text)
        if match_sl:
            raw_val = match_sl.group(1) or match_sl.group(2)
            target_price = sanitize_price_str(raw_val)
            if target_price:
                return ModifierSignalEvent(
                    signal_type=SignalType.MOVE_SL,
                    target_price=target_price,
                    raw_text=text,
                    message_id=message_id,
                    channel_id=channel_id,
                    channel_name=channel_name or "Chartoro FX",
                    execution_mode=execution_mode,
                    reply_to_msg_id=reply_to_msg_id
                )

        if RE_MOVE_BE.search(text):
            return ModifierSignalEvent(
                signal_type=SignalType.MOVE_BE,
                raw_text=text,
                message_id=message_id,
                channel_id=channel_id,
                channel_name=channel_name or "Chartoro FX",
                execution_mode=execution_mode,
                reply_to_msg_id=reply_to_msg_id
            )

        match_close = RE_CLOSE.search(text)
        if match_close:
            pct = Decimal("100.0")
            if match_close.group(1):
                pct = Decimal(match_close.group(1))
            elif match_close.group(2):
                pct = Decimal(match_close.group(2))
            return ModifierSignalEvent(
                signal_type=SignalType.CLOSE_ORDER,
                close_percentage=pct,
                raw_text=text,
                message_id=message_id,
                channel_id=channel_id,
                channel_name=channel_name or "Chartoro FX",
                execution_mode=execution_mode,
                reply_to_msg_id=reply_to_msg_id
            )
        return None

    def _extract_entry_price(self, text: str) -> Optional[Decimal]:
        match_exp = RE_ENTRY_EXPLICIT.search(text)
        if match_exp:
            price = sanitize_price_str(match_exp.group(1))
            if price and price >= Decimal("1500"):
                return price

        lines = text.split('\n')
        for line in lines:
            if re.search(r'\b(BUY|SELL|COMPRA|VENTA|ENTRY|ENTRADA)\b', line, re.IGNORECASE):
                matches = RE_ALL_NUMBERS.findall(line)
                for m in matches:
                    price = sanitize_price_str(m)
                    if price and price >= Decimal("1500"):
                        return price

        all_numbers = [sanitize_price_str(n) for n in RE_ALL_NUMBERS.findall(text)]
        valid_nums = [n for n in all_numbers if n and n >= Decimal("1500")]
        if valid_nums:
            return valid_nums[0]
        return None

    def _extract_sl(self, text: str) -> Tuple[Optional[Decimal], bool]:
        match = RE_SL_EXPLICIT.search(text)
        if match:
            sl = sanitize_price_str(match.group(1))
            if sl and sl >= Decimal("1500"):
                return sl, False
        return None, True

    def _extract_tps(self, text: str, entry: Decimal, side: OrderSide) -> List[Decimal]:
        tps_dict = {}
        for match in RE_TP_NUMBERED.finditer(text):
            idx = int(match.group(1))
            val = sanitize_price_str(match.group(2))
            if val and val >= Decimal("1500"):
                tps_dict[idx] = val

        if tps_dict:
            sorted_keys = sorted(tps_dict.keys())
            return [tps_dict[k] for k in sorted_keys]

        match_pips = RE_TP_PIPS.search(text)
        if match_pips:
            pips_val = Decimal(match_pips.group(1))
            delta_usd = pips_val * Decimal("0.10")
            tp1_calculated = (entry + delta_usd) if side == OrderSide.BUY else (entry - delta_usd)
            return [tp1_calculated.quantize(Decimal("0.01"))]

        match_gen = RE_TP_GENERIC.search(text)
        if match_gen:
            nums_str = RE_ALL_NUMBERS.findall(match_gen.group(1))
            tps = []
            for n in nums_str:
                val = sanitize_price_str(n)
                if val and val >= Decimal("1500") and val != entry:
                    tps.append(val)
            if tps:
                return tps

        all_nums = [sanitize_price_str(n) for n in RE_ALL_NUMBERS.findall(text)]
        remaining = [n for n in all_nums if n and n >= Decimal("1500") and n != entry]
        if side == OrderSide.BUY:
            valid_tps = [n for n in remaining if n > entry]
        else:
            valid_tps = [n for n in remaining if n < entry]

        return valid_tps[:3] if valid_tps else []

    def _validate_coherence(self, side: OrderSide, entry: Decimal, sl: Decimal, tps: List[Decimal]) -> Tuple[bool, str]:
        tp1 = tps[0]
        if side == OrderSide.BUY:
            if sl >= entry:
                return False, f"BUY: SL ({sl}) >= Entry ({entry})"
            if tp1 <= entry:
                return False, f"BUY: TP1 ({tp1}) <= Entry ({entry})"
        elif side == OrderSide.SELL:
            if sl <= entry:
                return False, f"SELL: SL ({sl}) <= Entry ({entry})"
            if tp1 >= entry:
                return False, f"SELL: TP1 ({tp1}) >= Entry ({entry})"
        return True, "OK"
