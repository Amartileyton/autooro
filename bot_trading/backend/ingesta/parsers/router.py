import logging
from typing import Optional, Union, Dict
from backend.config import settings
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent
from backend.ingesta.parsers.base import BaseSignalParser
from backend.ingesta.parsers.chartoro import ChartoroParser
from backend.ingesta.parsers.green_pips import GreenPipsParser

logger = logging.getLogger("trading_bot.parser.router")

_PARSERS: Dict[str, BaseSignalParser] = {
    "chartoro": ChartoroParser(),
    "green_pips": GreenPipsParser(),
}

import unicodedata

def get_channel_metadata(channel_id: Optional[int] = None, channel_name: Optional[str] = None) -> dict:
    """Obtiene la configuración de canal registrada en settings.CHANNELS_CONFIG."""
    channels = getattr(settings, 'CHANNELS_CONFIG', []) or []
    
    # Búsqueda por ID exacto
    if channel_id:
        for c in channels:
            if c.get("id") and int(c.get("id")) == int(channel_id):
                return c

    # Búsqueda por coincidencia de nombre (normalizando fuentes unicode/negritas como 𝐗𝐀𝐔(𝐔𝐒𝐃) 𝐆𝐑𝐄𝐄𝐍 𝐏𝐈𝐏𝐒)
    if channel_name:
        name_norm = unicodedata.normalize('NFKD', str(channel_name)).upper()
        for c in channels:
            cname_norm = unicodedata.normalize('NFKD', str(c.get("name", ""))).upper()
            if cname_norm in name_norm or name_norm in cname_norm or ("GREEN" in name_norm and "GREEN" in cname_norm):
                return c

    # Fallback predeterminado según nombre o ID
    is_green = False
    if channel_id and int(channel_id) == -1003674180002:
        is_green = True
    elif channel_name:
        norm = unicodedata.normalize('NFKD', str(channel_name)).upper()
        if "GREEN" in norm or "ACCESS" in norm:
            is_green = True

    if is_green:
        return {
            "id": channel_id or -1003674180002,
            "name": channel_name or "XAU(USD) GREEN PIPS",
            "parser": "green_pips",
            "mode": "AUDIT",
            "enabled": True
        }

    return {
        "id": channel_id or -1002763662248,
        "name": channel_name or "Chartoro FX",
        "parser": "chartoro",
        "mode": "AUDIT",
        "enabled": True
    }


def parse_signal_by_channel(
    raw_text: str,
    message_id: Optional[int] = None,
    channel_id: Optional[int] = None,
    channel_name: Optional[str] = None,
    reply_to_msg_id: Optional[int] = None
) -> Optional[Union[TradingSignalEvent, ModifierSignalEvent]]:
    """
    Enruta el mensaje al parser correspondiente según el canal configurado.
    Si el canal no tiene parser asignado o falla, prueba el parser de fallback.
    """
    meta = get_channel_metadata(channel_id=channel_id, channel_name=channel_name)
    parser_key = meta.get("parser", "chartoro")
    ch_name = meta.get("name", channel_name or "Chartoro FX")
    mode = meta.get("mode", "AUDIT")

    parser = _PARSERS.get(parser_key, _PARSERS["chartoro"])
    
    # 1. Intento con el parser asignado al canal
    res = parser.parse(
        raw_text=raw_text,
        message_id=message_id,
        channel_id=channel_id,
        channel_name=ch_name,
        execution_mode=mode,
        reply_to_msg_id=reply_to_msg_id
    )

    if res:
        return res

    # 2. Si falla y era green_pips, probar chartoro como respaldo cruzado
    if parser_key != "chartoro":
        res_alt = _PARSERS["chartoro"].parse(
            raw_text=raw_text,
            message_id=message_id,
            channel_id=channel_id,
            channel_name=ch_name,
            execution_mode=mode,
            reply_to_msg_id=reply_to_msg_id
        )
        if res_alt:
            return res_alt

    return None
