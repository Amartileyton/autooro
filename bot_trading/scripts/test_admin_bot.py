import asyncio
import os
import sys
from aiogram import Bot

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings

async def main():
    if not settings.TELEGRAM_BOT_TOKEN or not settings.ADMIN_TELEGRAM_USER_ID:
        print("❌ Token o User ID no configurados.")
        return

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        msg = (
            "🤖 <b>GOLD-EX TERMINAL CONECTADO</b>\n\n"
            "✅ <i>Autenticación con BotFather exitosa.</i>\n"
            "📊 Canal de señales vinculado: <code>-1002763662248</code>\n"
            "⚙️ Modo actual: <b>Paper Trading (Simulación Local)</b>\n\n"
            "¡Listo para desplegar en la nube!"
        )
        await bot.send_message(
            chat_id=settings.ADMIN_TELEGRAM_USER_ID,
            text=msg,
            parse_mode="HTML"
        )
        print("✅ Mensaje de prueba enviado con éxito a tu Telegram personal.")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
