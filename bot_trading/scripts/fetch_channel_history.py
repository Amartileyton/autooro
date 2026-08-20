import asyncio
import json
import logging
import os
import sys

# Configurar encoding UTF-8 para consola de Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Añadir el directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telethon import TelegramClient
from backend.config import settings
from backend.ingesta.parser import parse_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fetch_history")


async def main():
    target_channel = -1002763662248

    print(f"==================================================")
    print(f" EXTRACTOR DE HISTORIAL DE TELEGRAM")
    print(f" Canal Objetivo: {target_channel}")
    print(f"==================================================")

    if not settings.TG_API_ID or not settings.TG_API_HASH:
        print("\n❌ ERROR: Debes configurar TG_API_ID y TG_API_HASH en tu archivo .env")
        print("Obténlos en https://my.telegram.org -> API development tools")
        return

    client = TelegramClient(
        settings.TG_SESSION_NAME,
        settings.TG_API_ID,
        settings.TG_API_HASH
    )

    await client.start(phone=settings.TG_PHONE if settings.TG_PHONE else None)
    print("✅ Conectado a Telegram con éxito.")

    messages_data = []
    print(f"Descargando los últimos 50 mensajes del canal {target_channel}...")

    try:
        async for msg in client.iter_messages(target_channel, limit=50):
            if not msg.text:
                continue

            parsed_res = parse_signal(msg.text, message_id=msg.id, channel_id=target_channel)
            
            item = {
                "message_id": msg.id,
                "date": msg.date.isoformat(),
                "reply_to_msg_id": msg.reply_to.reply_to_msg_id if msg.reply_to else None,
                "text": msg.text,
                "is_signal": parsed_res is not None,
                "parsed_type": type(parsed_res).__name__ if parsed_res else None,
                "parsed_data": parsed_res.model_dump(mode='json') if parsed_res else None
            }
            messages_data.append(item)

        output_file = "channel_history_dump.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(messages_data, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n✅ Se han guardado {len(messages_data)} mensajes en '{output_file}'.")
        print("Resumen de parsing:")
        signals_count = len([m for m in messages_data if m["is_signal"]])
        print(f"• Señales/Modificadores detectados: {signals_count}")
        print(f"• Mensajes descartados (spam/info): {len(messages_data) - signals_count}")

    except Exception as e:
        print(f"❌ Error al acceder al canal: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
