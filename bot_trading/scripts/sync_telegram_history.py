import asyncio
import os
import sys
from datetime import datetime, timezone
from telethon import TelegramClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.database.session import AsyncSessionLocal
from backend.database.models import RawTelegramMessage
from backend.ingesta.parser import parse_signal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

async def sync():
    session_path = os.path.abspath(settings.TG_SESSION_NAME)
    client = TelegramClient(session_path, settings.TG_API_ID, settings.TG_API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Sesión no autorizada")
        return

    entity = await client.get_entity(settings.TARGET_CHANNEL_ID)
    channel_name = getattr(entity, 'title', 'Chartoro FX')
    print(f"Sincronizando mensajes de: {channel_name} ({settings.TARGET_CHANNEL_ID})...")

    messages = await client.get_messages(entity, limit=40)
    
    async with AsyncSessionLocal() as db:
        for msg in messages:
            if not msg.text or len(msg.text.strip()) < 8:
                continue

            parsed = parse_signal(msg.text, message_id=msg.id, channel_id=settings.TARGET_CHANNEL_ID)
            parsed_success = bool(parsed)
            parser_used = "REGEX" if parsed_success else "NONE"

            # Check if message already exists in DB
            from sqlalchemy import select
            stmt = select(RawTelegramMessage).where(RawTelegramMessage.message_id == msg.id)
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()

            if not existing:
                raw_msg = RawTelegramMessage(
                    message_id=msg.id,
                    channel_id=settings.TARGET_CHANNEL_ID,
                    channel_name=channel_name,
                    raw_text=msg.text,
                    parsed_success=parsed_success,
                    parser_used=parser_used,
                    received_at=msg.date
                )
                db.add(raw_msg)
        
        await db.commit()
    
    print("✅ Sincronización de historial completada.")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(sync())
