import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.database.session import AsyncSessionLocal
from backend.database.models import RawTelegramMessage
from sqlalchemy import select

async def main():
    print("SETTINGS DATABASE_URL:", settings.DATABASE_URL)
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(RawTelegramMessage))
        msgs = result.scalars().all()
        print(f"TOTAL MENSAJES ENCONTRADOS: {len(msgs)}")
        for m in msgs[-5:]:
            print(f" - #{m.id} (msg_id={m.message_id}) {m.channel_name}: {m.raw_text[:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
