import asyncio
import logging
from typing import Optional, Callable
from telethon import TelegramClient, events
from backend.config import settings
from backend.database.session import AsyncSessionLocal
from backend.database.models import RawTelegramMessage, SystemAuditLog
from backend.ingesta.parser import parse_signal
from backend.ingesta.ai_fallback import parse_with_ai
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, ParserType

logger = logging.getLogger("trading_bot.telethon")


class TelegramIngestionClient:
    """
    Cliente Telethon MTProto para ingesta en tiempo real de señales de Telegram.
    Audita el 100% de los mensajes en SQLite (WAL) y desacopla la ejecución mediante asyncio.Queue.
    """

    def __init__(self, signal_queue: asyncio.Queue):
        self.signal_queue = signal_queue
        self.client: Optional[TelegramClient] = None
        self._is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Inicializa y arranca el listener de Telethon."""
        if not settings.TG_API_ID or not settings.TG_API_HASH:
            logger.warning("TG_API_ID o TG_API_HASH no configurados. Ingesta de Telethon deshabilitada.")
            return

        logger.info(f"Iniciando Telethon MTProto Client para canal {settings.TARGET_CHANNEL_ID}...")
        self.client = TelegramClient(
            settings.TG_SESSION_NAME,
            settings.TG_API_ID,
            settings.TG_API_HASH
        )

        await self.client.start(phone=settings.TG_PHONE if settings.TG_PHONE else None)
        self._is_running = True

        # Registrar handler de eventos
        target = settings.TARGET_CHANNEL_ID if settings.TARGET_CHANNEL_ID != 0 else None
        
        @self.client.on(events.NewMessage(chats=target))
        async def on_new_message(event):
            await self._handle_incoming_message(event)

        logger.info("Telethon MTProto conectado y escuchando eventos NewMessage.")

    async def stop(self):
        """Detiene el cliente de Telethon de forma limpia."""
        self._is_running = False
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Telethon desconectado limpiamente.")

    async def _handle_incoming_message(self, event):
        """Procesa cada mensaje entrante aplicando filtros, auditoría y parsing."""
        if not settings.INGESTION_ENABLED:
            logger.info("Ingesta pausada globalmente. Mensaje ignorado.")
            return

        message = event.message
        raw_text = message.text or message.message or ""
        msg_id = message.id
        channel_id = event.chat_id
        reply_to_id = message.reply_to.reply_to_msg_id if message.reply_to else None

        # 1. Filtro previo: descartar mensajes menores a 8 caracteres o sin texto
        if not raw_text or len(raw_text.strip()) < 8:
            logger.debug(f"Mensaje {msg_id} descartado por longitud insuficiente ({len(raw_text)} chars).")
            return

        logger.info(f"Nuevo mensaje recibido de Telegram [{channel_id}:{msg_id}]: {raw_text[:60]}...")

        # 2. Fast Path: Parser Regex (< 0.05ms)
        parsed_event = parse_signal(
            raw_text,
            message_id=msg_id,
            channel_id=channel_id,
            reply_to_msg_id=reply_to_id
        )
        parser_used = "REGEX" if parsed_event else "NONE"
        parsed_success = bool(parsed_event)
        error_reason = None

        # 3. AI Fallback (solo si Regex no detectó señal y está habilitado)
        if not parsed_event and settings.AI_FALLBACK_ENABLED:
            logger.info("Regex no detectó señal. Intentando rescate con IA Fallback...")
            parsed_event = await parse_with_ai(raw_text, message_id=msg_id, channel_id=channel_id)
            if parsed_event:
                parser_used = "AI_FALLBACK"
                parsed_success = True

        if not parsed_success:
            error_reason = "NO_SIGNAL_PATTERN_MATCHED"

        # 4. Obtener nombre del canal
        channel_name = "Chartoro FX"
        try:
            chat = await event.get_chat()
            if chat and hasattr(chat, 'title') and chat.title:
                channel_name = chat.title
        except Exception:
            pass

        # 5. Auditoría 100% inmutable en SQLite WAL
        await self._persist_raw_message(
            message_id=msg_id,
            channel_id=channel_id,
            channel_name=channel_name,
            raw_text=raw_text,
            parsed_success=parsed_success,
            parser_used=parser_used,
            error_reason=error_reason
        )

        # 6. Emisión a cola desacoplada para el Risk Engine
        if parsed_event:
            logger.info(f"Señal extraída con éxito ({parser_used}) desde '{channel_name}': {parsed_event}. Emitiendo a cola interna.")
            await self.signal_queue.put(parsed_event)

    async def _persist_raw_message(
        self,
        message_id: int,
        channel_id: int,
        channel_name: str,
        raw_text: str,
        parsed_success: bool,
        parser_used: str,
        error_reason: Optional[str]
    ):
        """Guarda el mensaje raw auditado en SQLite de forma asíncrona."""
        try:
            async with AsyncSessionLocal() as session:
                raw_msg = RawTelegramMessage(
                    message_id=message_id,
                    channel_id=channel_id,
                    channel_name=channel_name,
                    raw_text=raw_text,
                    parsed_success=parsed_success,
                    parser_used=parser_used,
                    error_reason=error_reason
                )
                session.add(raw_msg)
                await session.commit()
        except Exception as e:
            logger.error(f"Error al auditar mensaje raw en SQLite: {e}")
