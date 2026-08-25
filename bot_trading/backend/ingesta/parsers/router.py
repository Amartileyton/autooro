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

def get_channel_metadata(channel_id: Optional[int] = None, channel_name: Optional[str] = None) -> dict:
    """Obtiene la configuración de canal registrada en settings.CHANNELS_CONFIG."""
    channels = getattr(settings, 'CHANNELS_CONFIG', []) or []
    
    # Búsqueda por ID exacto
    if channel_id:
        for c in channels:
            if c.get("id") and int(c.get("id")) == int(channel_id):
                return c

    # Búsqueda por coincidencia de nombre
    if channel_name:
        name_upper = channel_name.upper()
        for c in channels:
            cname = c.get("name", "").upper()
            if cname in name_upper or name_upper in cname or ("GREEN" in name_upper and "GREEN" in cname):
                return c

    # Fallback predeterminado: Chartoro FX en AUDIT
    return {
        "id": channel_id or -1002763662248,
        "name": channel_name or "Chartoro FX",
        "parser": "green_pips" if (channel_name and "GREEN" in channel_name.upper()) else "chartoro",
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
