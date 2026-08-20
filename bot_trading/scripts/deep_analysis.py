import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telethon import TelegramClient
from backend.config import settings
from backend.ingesta.parser import parse_signal

logging.basicConfig(level=logging.WARNING)


async def main():
    target_channel = -1002763662248
    start_date = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)

    print(f"==================================================")
    print(f" ANÁLISIS PROFUNDO DE MENSAJES TELEGRAM")
    print(f" Canal Objetivo: {target_channel}")
    print(f" Desde: {start_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"==================================================")

    client = TelegramClient(
        settings.TG_SESSION_NAME,
        settings.TG_API_ID,
        settings.TG_API_HASH
    )

    await client.start(phone=settings.TG_PHONE if settings.TG_PHONE else None)
    print("Conectado a Telegram con éxito.")

    all_messages = []
    total_fetched = 0

    print("Descargando mensajes históricos...")

    try:
        async for msg in client.iter_messages(target_channel, limit=1000):
            total_fetched += 1
            if msg.date < start_date:
                break

            text = msg.text or msg.message or ""
            parsed_res = parse_signal(
                text,
                message_id=msg.id,
                channel_id=target_channel,
                reply_to_msg_id=msg.reply_to.reply_to_msg_id if msg.reply_to else None
            ) if text else None

            all_messages.append({
                "message_id": msg.id,
                "date": msg.date.isoformat(),
                "reply_to_msg_id": msg.reply_to.reply_to_msg_id if msg.reply_to else None,
                "has_media": bool(msg.media),
                "text": text,
                "parsed_type": type(parsed_res).__name__ if parsed_res else None,
                "parsed_data": parsed_res.model_dump(mode='json') if parsed_res else None
            })

        print(f"Total mensajes examinados: {len(all_messages)} (de {total_fetched} iterados)")

        # Guardar en JSON
        output_file = "deep_channel_history.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_messages, f, indent=2, ensure_ascii=False, default=str)

        print(f"Historial completo guardado en '{output_file}'.")

        # Estadísticas y Categorización
        signals = [m for m in all_messages if m["parsed_type"] == "TradingSignalEvent"]
        modifiers = [m for m in all_messages if m["parsed_type"] == "ModifierSignalEvent"]
        discarded = [m for m in all_messages if m["parsed_type"] is None and m["text"]]

        print("\n" + "="*50)
        print(" RESUMEN ESTADÍSTICO")
        print("="*50)
        print(f"• Total Mensajes analizados: {len(all_messages)}")
        print(f"• Señales Nuevas de Entrada: {len(signals)}")
        print(f"• Modificadores (Move SL / Close): {len(modifiers)}")
        print(f"• Mensajes Descartados (Spam/Info/Promos): {len(discarded)}")
        print("="*50)

    except Exception as e:
        print(f"Error durante el análisis: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
