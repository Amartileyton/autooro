import asyncio
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from telethon import TelegramClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.ingesta.parser import parse_signal

async def fetch_and_dump():
    session_candidates = [
        "data/bot_session",
        "/app/data/bot_session",
        "bot_session",
        "/app/bot_session"
    ]
    session_name = "data/bot_session"
    for candidate in session_candidates:
        if os.path.exists(f"{candidate}.session") or os.path.exists(candidate):
            session_name = candidate
            break

    print(f"Conectando a Telethon con sesion: {session_name}...")
    client = TelegramClient(session_name, settings.TG_API_ID, settings.TG_API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("ERROR: Sesion de Telethon no autorizada.")
        return

    target = settings.TARGET_CHANNEL_ID
    entity = await client.get_entity(target)
    channel_name = getattr(entity, 'title', 'Chartoro FX')
    print(f"Canal detectado: '{channel_name}' (ID: {target})")

    print("Obteniendo los ultimos 1000 mensajes...")
    messages = await client.get_messages(entity, limit=1000)
    print(f"Total mensajes descargados del canal: {len(messages)}")

    madrid_tz = ZoneInfo("Europe/Madrid")
    signals = []
    all_msgs_data = []

    for msg in reversed(messages): # orden cronologico (mas antiguo a mas reciente)
        if not msg.text:
            continue
        
        # Fecha en Madrid
        utc_date = msg.date
        madrid_date = utc_date.astimezone(madrid_tz)
        madrid_str = madrid_date.strftime("%d/%m/%Y %H:%M:%S")

        parsed = parse_signal(msg.text, message_id=msg.id, channel_id=target)
        is_signal = bool(parsed)

        all_msgs_data.append({
            "message_id": msg.id,
            "channel_id": target,
            "channel_name": channel_name,
            "raw_text": msg.text,
            "parsed_success": is_signal,
            "parser_used": "REGEX" if is_signal else "NONE",
            "received_at": utc_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "madrid_str": madrid_str
        })

        if is_signal:
            signals.append({
                "msg_id": msg.id,
                "madrid_time": madrid_str,
                "type": parsed.event_type if hasattr(parsed, 'event_type') else type(parsed).__name__,
                "side": getattr(parsed, 'side', None),
                "entry": getattr(parsed, 'entry_price', None),
                "sl": getattr(parsed, 'sl_price', None),
                "tp1": getattr(parsed, 'tp1', None) or (parsed.tp_levels[0] if getattr(parsed, 'tp_levels', None) else None),
                "tp2": getattr(parsed, 'tp2', None) or (parsed.tp_levels[1] if getattr(parsed, 'tp_levels', None) and len(parsed.tp_levels) > 1 else None),
                "tp3": getattr(parsed, 'tp3', None) or (parsed.tp_levels[2] if getattr(parsed, 'tp_levels', None) and len(parsed.tp_levels) > 2 else None),
                "raw": msg.text.replace("\n", " ")[:60]
            })

    print(f"\n--- SEÑALES DETECTADAS ({len(signals)}) ---")
    for s in signals:
        side_val = s['side'].value if hasattr(s['side'], 'value') else s['side']
        print(f"ID: {s['msg_id']} | Fecha: {s['madrid_time']} | Tipo: {s['type']} | Lado: {side_val} | Entrada: {s['entry']} | SL: {s['sl']} | TP1: {s['tp1']} | Texto: {s['raw']}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(fetch_and_dump())
