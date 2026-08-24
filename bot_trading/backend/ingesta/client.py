import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
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
        """Inicializa y arranca el listener de Telethon de forma no bloqueante."""
        if not settings.TG_API_ID or not settings.TG_API_HASH:
            logger.warning("TG_API_ID o TG_API_HASH no configurados. Ingesta de Telethon deshabilitada.")
            return

        session_candidates = [
            "bot_session",
            "/app/bot_session",
            "data/bot_session",
            "/app/data/bot_session",
            settings.TG_SESSION_NAME
        ]
        session_name = "bot_session"
        for candidate in session_candidates:
            if os.path.exists(f"{candidate}.session") or os.path.exists(candidate):
                session_name = candidate
                break

        logger.info(f"Iniciando Telethon MTProto Client usando sesión '{session_name}' para canal {settings.TARGET_CHANNEL_ID}...")
        self.client = TelegramClient(
            session_name,
            settings.TG_API_ID,
            settings.TG_API_HASH
        )

        await self.client.connect()
        is_authorized = await self.client.is_user_authorized()
        
        if not is_authorized:
            logger.warning("Telethon MTProto: Sesión no autorizada o expirada. Por favor autentica con scripts/auth_telegram.py.")
            return

        self._is_running = True
        logger.info("Telethon MTProto: Sesión AUTORIZADA correctamente y conectada.")

        # Registrar handler de eventos
        target = settings.TARGET_CHANNEL_ID if settings.TARGET_CHANNEL_ID != 0 else None
        
        @self.client.on(events.NewMessage(chats=target))
        async def on_new_message(event):
            await self._handle_incoming_message(event)

        logger.info("Telethon MTProto escuchando eventos NewMessage en vivo.")

    async def stop(self):
        """Detiene el cliente de Telethon de forma limpia."""
        self._is_running = False
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Telethon desconectado limpiamente.")

    async def _handle_incoming_message(self, event):
        """Procesa cada mensaje entrante aplicando filtros, auditoría y parsing."""
        if not settings.INGESTION_ENABLED:
            return

        text = event.raw_text
        msg_id = event.id
        channel_id = event.chat_id
        timestamp = event.date or datetime.now(timezone.utc)

        # 1. Guardar mensaje RAW en base de datos para auditoría inmutable
        try:
            async with AsyncSessionLocal() as session:
                raw_msg = RawTelegramMessage(
                    message_id=msg_id,
                    channel_id=channel_id,
                    raw_text=text,
                    is_signal=False,
                    received_at=timestamp
                )
                session.add(raw_msg)
                await session.commit()
        except Exception as e:
            logger.error(f"Error al guardar mensaje raw en DB: {e}")

        logger.info(f"Mensaje recibido [{msg_id}] en canal {channel_id}: '{text[:60]}...'")

        # 2. Intento de Parsing Primario con Regex Determinista (< 1ms)
        parsed_event = parse_signal(text, msg_id, channel_id)

        # 3. Si falla y la IA está habilitada, intento de Parsing Fallback con LLM
        if not parsed_event and settings.AI_FALLBACK_ENABLED:
            logger.info(f"Regex no detectó señal en [{msg_id}]. Intentando Fallback IA ({settings.AI_PROVIDER})...")
            parsed_event = await parse_with_ai(text, msg_id, channel_id)

        if parsed_event:
            logger.info(
                f"SEÑAL DETECTADA [{parsed_event.parser_used.value}]: "
                f"{type(parsed_event).__name__} en canal {channel_id}"
            )
            # Encolar en la cola asíncrona para consumo desacoplado
            await self.signal_queue.put(parsed_event)

            # Notificar WebSocket en tiempo real
            try:
                from backend.api.ws import manager
                await manager.broadcast({
                    "type": "SIGNAL_PARSED",
                    "event": parsed_event.model_dump() if hasattr(parsed_event, "model_dump") else str(parsed_event)
                })
            except Exception as ws_err:
                logger.debug(f"Aviso al notificar señal por WS: {ws_err}")
