import re
import logging
from decimal import Decimal
from typing import Optional, Union, List, Tuple
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType, ParserType
)
from backend.ingesta.parsers.base import BaseSignalParser, sanitize_price_str

logger = logging.getLogger("trading_bot.parser.green_pips")

# Patrones para activo y dirección
RE_GP_ASSET = re.compile(r'(?:#|\b)(XAUUSD|XAU/USD|GOLD|ORO|XAU)\b', re.IGNORECASE)
RE_GP_BUY = re.compile(r'(?:#|\b)(BUY|BUY\s+NOW|COMPRA|LONG)\b', re.IGNORECASE)
RE_GP_SELL = re.compile(r'(?:#|\b)(SELL|SELL\s+NOW|VENTA|SHORT)\b', re.IGNORECASE)

# Rango de entrada: ej. "GOLD BUY 2650-2652" o "BUY XAUUSD @ 2650 - 2653" o "Entry : 4658 / 4660"
RE_ENTRY_RANGE = re.compile(
    r'(?:BUY|SELL|ENTRY|ENTRADA|PRECIO|PRICE|ZONE|ZONA|@)?\s*[:=@\s]*([0-9]{4}(?:[.,][0-9]+)?)\s*(?:/|-|–|—|TO|\s+A\s+|\s+HASTA\s+|~|->)\s*([0-9]{4}(?:[.,][0-9]+)?)',
    re.IGNORECASE
)

# Precios individuales
RE_PRICE_PATTERN = r'(?:[0-9]{1,2}[.,][0-9]{3}(?:[.,][0-9]+)?|[0-9]{4}(?:[.,][0-9]+)?)'
RE_GP_ENTRY_SINGLE = re.compile(rf'(?:ENTRY|ENTRY\s*POINT|PRICE|@|NOW|PRECIO|ENTRADA)[*_~:\s]*[:=@\s]*({RE_PRICE_PATTERN})', re.IGNORECASE)

# Sop Loss / Stop Loss / Stp Loss / SL / S/L / Stop
RE_GP_SL = re.compile(
    rf'(?:STOP\s*LOSS|SOP\s*LOSS|STP\s*LOSS|STOP|SOP|STP|S[./\s]*L)[*_~:\s]*[:=@\s\-]*[*_~:\s]*({RE_PRICE_PATTERN})',
    re.IGNORECASE
)

# Take Profit numerado: TP 1, Take Profit 1, Target 1, T1, Objetivo 1, etc.
RE_GP_TP_NUMBERED = re.compile(
    rf'(?:TAKE\s*PROFIT|TP|TARGET|OBJETIVO|T)[*_~:\s]*([1-5])[*_~:\s]*[:=@\s\-]*[*_~:\s]*({RE_PRICE_PATTERN})',
    re.IGNORECASE
)
RE_GP_TP_GENERIC = re.compile(
    rf'(?:TAKE\s*PROFITS?|TPS?|TARGETS?|OBJETIVOS?)[*_~:\s]*[:=@\s]*({RE_PRICE_PATTERN}(?:\s*[/,\-\n\s]+\s*{RE_PRICE_PATTERN})*)',
    re.IGNORECASE
)
RE_GP_TP_OPEN = re.compile(r'(?:TP|TAKE\s*PROFIT|TARGET)\s*:\s*OPEN', re.IGNORECASE)

# Modificadores de Green Pips (Break Even, Close Half, SL modification)
RE_GP_MOVE_BE = re.compile(r'\b(SET\s*BE|MOVE\s*SL\s*TO\s*BE|BREAK[-\s]?EVEN|SL\s*TO\s*ENTRY|SL\s*->\s*BE|MOVE\s*SL\s*TO\s*BREAKEVEN)\b', re.IGNORECASE)
RE_GP_MOVE_SL = re.compile(rf'(?:MOVE\s*SL\s*TO|SET\s*SL\s*TO|SL\s*TO|SL\s*->|MOVER\s*SL\s*A)\s*({RE_PRICE_PATTERN})', re.IGNORECASE)
RE_GP_CLOSE_PARTIAL = re.compile(r'\b(CLOSE\s*HALF|CLOSE\s*50%|CERRAR\s*MITAD|CERRAR\s*PARCIAL|BOOK\s*PROFIT|SECURE\s*GAINS)\b', re.IGNORECASE)
RE_GP_CLOSE_FULL = re.compile(r'\b(CLOSE\s*NOW|CLOSE\s*ALL|CLOSE\s*TRADE|CERRAR\s*TODO|EXIT\s*NOW)\b', re.IGNORECASE)

# Ruido/Marketing a ignorar
RE_GP_IGNORE = re.compile(
    r'\b(VIP\s*CHANNEL|PREMIUM\s*GROUP|DISCOUNT|CONTACT|LIFETIME|'
    r'CRYPTO|BTC|ETH|USDT|JOIN\s*NOW|TESTIMONIAL|FEEDBACK)\b',
    re.IGNORECASE
)


class GreenPipsParser(BaseSignalParser):
    """
    Parser especializado para el canal 'XAU(USD) GREEN PIPS':
    - Detecta señales directas o por rango (GOLD BUY 2650-2652).
    - Extrae SL y múltiples TPs numerados (TP1 a TP5).
    - Soporta modificadores típicos (SL to Entry/BE, Close Half, Book Profit).
    """

    def parse(
        self,
        raw_text: str,
        message_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        channel_name: Optional[str] = "XAU(USD) GREEN PIPS",
        execution_mode: str = "AUDIT",
        reply_to_msg_id: Optional[int] = None
    ) -> Optional[Union[TradingSignalEvent, ModifierSignalEvent]]:
        if not raw_text or len(raw_text.strip()) < 6:
            return None

        cleaned = raw_text.strip()

        # 1. Comprobar Modificadores
        mod_event = self._check_modifiers(cleaned, message_id, channel_id, channel_name, execution_mode, reply_to_msg_id)
        if mod_event:
            return mod_event

        # 2. Descartar spam/publicidad
        if RE_GP_IGNORE.search(cleaned):
            return None

        # 3. Comprobar si es BUY o SELL
        has_buy = bool(RE_GP_BUY.search(cleaned))
        has_sell = bool(RE_GP_SELL.search(cleaned))

        if not has_buy and not has_sell:
            return None

        side = OrderSide.BUY if has_buy else OrderSide.SELL
        if has_buy and has_sell:
            pos_b = RE_GP_BUY.search(cleaned).start()
            pos_s = RE_GP_SELL.search(cleaned).start()
            side = OrderSide.BUY if pos_b < pos_s else OrderSide.SELL

        # 4. Extraer Precio de Entrada (Soporte para Rango o Precio Único)
        entry_price, entry_min, entry_max = self._extract_entry(cleaned, side)
        if not entry_price:
            return None

        # 5. Extraer Stop Loss (Soporte laxo para Sop Loss, Stp, Stop, SL)
        sl_price, requires_dynamic_sl = self._extract_sl(cleaned)

        # 6. Extraer Take Profits
        tp_levels = self._extract_tps(cleaned, entry_price, side, entry_min, entry_max)
        if not tp_levels:
            # Si no hay TPs explícitos, calcular TP1 = +3.0 USD por defecto
            ref_entry = entry_max if (side == OrderSide.BUY and entry_max) else (entry_min if entry_min else entry_price)
            default_tp1 = (ref_entry + Decimal("3.00")) if side == OrderSide.BUY else (ref_entry - Decimal("3.00"))
            tp_levels = [default_tp1]

        # 7. Validar coherencia matemática básica
        if not requires_dynamic_sl and sl_price is not None:
            ref_entry_low = entry_min if entry_min else entry_price
            ref_entry_high = entry_max if entry_max else entry_price
            if side == OrderSide.BUY and (sl_price >= ref_entry_low or tp_levels[0] <= ref_entry_low):
                logger.warning(f"GreenPips: Señal BUY inconsistente (Entry:{entry_price}, SL:{sl_price}, TP1:{tp_levels[0]})")
                return None
            elif side == OrderSide.SELL and (sl_price <= ref_entry_high or tp_levels[0] >= ref_entry_high):
                logger.warning(f"GreenPips: Señal SELL inconsistente (Entry:{entry_price}, SL:{sl_price}, TP1:{tp_levels[0]})")
                return None

        return TradingSignalEvent(
            asset="XAUUSD",
            side=side,
            entry_price=entry_price,
            entry_min=entry_min,
            entry_max=entry_max,
            sl_price=sl_price,
            tp_levels=tp_levels,
            requires_dynamic_sl=requires_dynamic_sl,
            parser_type=ParserType.REGEX,
            raw_text=raw_text,
            message_id=message_id,
            channel_id=channel_id,
            channel_name=channel_name or "XAU(USD) GREEN PIPS",
            execution_mode=execution_mode
        )

    def _check_modifiers(self, text: str, message_id: Optional[int], channel_id: Optional[int], channel_name: Optional[str], execution_mode: str, reply_to_msg_id: Optional[int]) -> Optional[ModifierSignalEvent]:
        # Move SL to specific price
        match_sl = RE_GP_MOVE_SL.search(text)
        if match_sl:
            px = sanitize_price_str(match_sl.group(1))
            if px and px >= Decimal("1500"):
                return ModifierSignalEvent(
                    signal_type=SignalType.MOVE_SL,
                    target_price=px,
                    raw_text=text,
                    message_id=message_id,
                    channel_id=channel_id,
                    channel_name=channel_name or "XAU(USD) GREEN PIPS",
                    execution_mode=execution_mode,
                    reply_to_msg_id=reply_to_msg_id
                )

        # Move to Break Even
        if RE_GP_MOVE_BE.search(text):
            return ModifierSignalEvent(
                signal_type=SignalType.MOVE_BE,
                raw_text=text,
                message_id=message_id,
                channel_id=channel_id,
                channel_name=channel_name or "XAU(USD) GREEN PIPS",
                execution_mode=execution_mode,
                reply_to_msg_id=reply_to_msg_id
            )

        # Close Partial / Close Half (50%)
        if RE_GP_CLOSE_PARTIAL.search(text):
            return ModifierSignalEvent(
                signal_type=SignalType.CLOSE_ORDER,
                close_percentage=Decimal("50.0"),
                raw_text=text,
                message_id=message_id,
                channel_id=channel_id,
                channel_name=channel_name or "XAU(USD) GREEN PIPS",
                execution_mode=execution_mode,
                reply_to_msg_id=reply_to_msg_id
            )

        # Close Full
        if RE_GP_CLOSE_FULL.search(text):
            return ModifierSignalEvent(
                signal_type=SignalType.CLOSE_ORDER,
                close_percentage=Decimal("100.0"),
                raw_text=text,
                message_id=message_id,
                channel_id=channel_id,
                channel_name=channel_name or "XAU(USD) GREEN PIPS",
                execution_mode=execution_mode,
                reply_to_msg_id=reply_to_msg_id
            )

        return None

    def _extract_entry(self, text: str, side: OrderSide) -> Tuple[Optional[Decimal], Optional[Decimal], Optional[Decimal]]:
        """
        Extrae el precio de entrada y los límites inferior y superior del rango si aplica.
        Retorna (entry_price, entry_min, entry_max).
        """
        # 1. Comprobar si es un rango tipo "4658 / 4660" o "2650-2652"
        range_match = RE_ENTRY_RANGE.search(text)
        if range_match:
            p1 = sanitize_price_str(range_match.group(1))
            p2 = sanitize_price_str(range_match.group(2))
            if p1 and p2 and p1 >= Decimal("1500") and p2 >= Decimal("1500"):
                entry_min = min(p1, p2)
                entry_max = max(p1, p2)
                avg = ((entry_min + entry_max) / Decimal("2.0")).quantize(Decimal("0.01"))
                return avg, entry_min, entry_max

        # 2. Entrada explícita
        single_match = RE_GP_ENTRY_SINGLE.search(text)
        if single_match:
            px = sanitize_price_str(single_match.group(1))
            if px and px >= Decimal("1500"):
                return px, None, None

        # 3. Buscar cualquier número de 4 dígitos en la línea de BUY/SELL
        for line in text.split('\n'):
            if re.search(r'\b(BUY|SELL|GOLD|XAUUSD)\b', line, re.IGNORECASE):
                nums = re.findall(r'\b[0-9]{4}(?:[.,][0-9]+)?\b', line)
                for n in nums:
                    px = sanitize_price_str(n)
                    if px and px >= Decimal("1500"):
                        return px, None, None

        # 4. Fallback: primer número de 4 dígitos encontrado
        all_nums = re.findall(r'\b[0-9]{4}(?:[.,][0-9]+)?\b', text)
        for n in all_nums:
            px = sanitize_price_str(n)
            if px and px >= Decimal("1500"):
                return px, None, None

        return None, None, None

    def _extract_sl(self, text: str) -> Tuple[Optional[Decimal], bool]:
        match = RE_GP_SL.search(text)
        if match:
            sl = sanitize_price_str(match.group(1))
            if sl and sl >= Decimal("1500"):
                return sl, False
        return None, True

    def _extract_tps(
        self,
        text: str,
        entry: Decimal,
        side: OrderSide,
        entry_min: Optional[Decimal] = None,
        entry_max: Optional[Decimal] = None
    ) -> List[Decimal]:
        """
        Extrae lista ordenada de Take Profits de forma flexible:
        - TP 1, Take Profit 1, Target 1, etc.
        - Bloques genéricos tipo 'Take Profits: 4663 / 4666 / 4670'
        - Fallback filtrando líneas de entrada y Stop Loss para evitar colisiones.
        """
        tps_dict = {}
        # 1. Búsqueda de TP numerados
        for m in RE_GP_TP_NUMBERED.finditer(text):
            idx_str = m.group(1)
            idx = int(idx_str) if idx_str else (len(tps_dict) + 1)
            val = sanitize_price_str(m.group(2))
            if val and val >= Decimal("1500"):
                tps_dict[idx] = val

        if tps_dict:
            return [tps_dict[k] for k in sorted(tps_dict.keys())]

        # 2. Bloque genérico Take Profits: 4663 / 4666 / 4670
        gen_match = RE_GP_TP_GENERIC.search(text)
        if gen_match:
            raw_tps = re.findall(r'\b[0-9]{4}(?:[.,][0-9]+)?\b', gen_match.group(1))
            extracted = []
            for n in raw_tps:
                val = sanitize_price_str(n)
                if val and val >= Decimal("1500") and val != entry:
                    if entry_min and entry_max and (entry_min <= val <= entry_max):
                        continue
                    extracted.append(val)
            if extracted:
                return extracted

        # 3. Fallback: extraer números ignorando líneas de Entry, SL, etc.
        ignored_lines_pattern = re.compile(
            r'\b(BUY|SELL|ENTRY|ENTRADA|SL|SOP|STOP|LOSS|STP|RANGE|ZONA|ZONE)\b',
            re.IGNORECASE
        )
        remaining_nums = []
        for line in text.split('\n'):
            if ignored_lines_pattern.search(line):
                continue
            for n in re.findall(r'\b[0-9]{4}(?:[.,][0-9]+)?\b', line):
                val = sanitize_price_str(n)
                if val and val >= Decimal("1500"):
                    if entry_min and entry_max and (entry_min <= val <= entry_max):
                        continue
                    if val != entry:
                        remaining_nums.append(val)

        if side == OrderSide.BUY:
            cmp_price = entry_max if entry_max else entry
            tps = [n for n in remaining_nums if n > cmp_price]
        else:
            cmp_price = entry_min if entry_min else entry
            tps = [n for n in remaining_nums if n < cmp_price]

        return tps[:5] if tps else []
