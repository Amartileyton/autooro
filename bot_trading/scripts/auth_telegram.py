import asyncio
import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TG_API_ID", "31637828"))
API_HASH = os.getenv("TG_API_HASH", "69d1f0402fd2ada9bbe830db9e7036ab")
PHONE = os.getenv("TG_PHONE", "+34635031231")
SESSION_NAME = os.getenv("TG_SESSION_NAME", "data/bot_session")

async def main():
    os.makedirs("data", exist_ok=True)
    print(f"Iniciando autenticacion interactiva de Telethon para {PHONE}...")
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start(phone=PHONE)
    print("\n¡Autenticacion completada con exito!")
    me = await client.get_me()
    print(f"Conectado como: {me.first_name} (@{me.username}) ID: {me.id}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
