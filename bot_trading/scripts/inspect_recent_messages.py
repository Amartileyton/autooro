import asyncio
import os
import sys
from datetime import datetime, timezone
from telethon import TelegramClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.ingesta.parser import parse_signal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

async def main():
    print("==================================================")
    print(" REVISIÓN DE MENSAJES Y SEÑALES DEL CANAL")
    print(f" Canal: {settings.TARGET_CHANNEL_ID}")
    print("==================================================")

    session_path = os.path.abspath(settings.TG_SESSION_NAME)
    client = TelegramClient(
        session_path,
        settings.TG_API_ID,
        settings.TG_API_HASH
    )

    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Sesión no autorizada localmente.")
        return

    entity = await client.get_entity(settings.TARGET_CHANNEL_ID)
    print(f"✅ Conectado a: {getattr(entity, 'title', entity.id)}")

    # Obtener últimos 30 mensajes
    messages = await client.get_messages(entity, limit=30)
    print(f"Total mensajes recuperados: {len(messages)}\n")

    for msg in reversed(messages):
        if not msg.text:
            continue
        
        parsed = parse_signal(
            msg.text,
            message_id=msg.id,
            channel_id=settings.TARGET_CHANNEL_ID,
            reply_to_msg_id=getattr(msg.reply_to, "reply_to_msg_id", None) if msg.reply_to else None
        )

        date_str = msg.date.strftime("%Y-%m-%d %H:%M:%S UTC")
        msg_preview = msg.text.replace("\n", " ")[:80]

        if parsed:
            print(f"🔔 [SEÑAL VÁLIDA #{msg.id}] ({date_str})")
            print(f"   Tipo: {type(parsed).__name__}")
            if hasattr(parsed, 'side'):
                print(f"   Operación: {parsed.side.value} @ Entry: {parsed.entry_price} | SL: {parsed.sl_price} | TPs: {parsed.tp_levels}")
            elif hasattr(parsed, 'action'):
                print(f"   Modificador: {parsed.action} -> Precio: {getattr(parsed, 'target_price', 'N/A')}")
            print(f"   Texto: \"{msg_preview}...\"\n")
        else:
            print(f"⚪ [INFO / SPAM / RESULTADO #{msg.id}] ({date_str})")
            print(f"   Texto: \"{msg_preview}...\"\n")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
