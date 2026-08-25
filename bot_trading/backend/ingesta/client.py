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
            "data/bot_session",
            "/app/data/bot_session",
            "bot_session",
            "/app/bot_session",
            settings.TG_SESSION_NAME
        ]
        session_name = "data/bot_session"
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

        # Sincronización inicial de arranque: sincronizar últimos 50 mensajes para capturar señales recientes
        if target:
            asyncio.create_task(self._sync_recent_channel_history(target))

    async def _sync_recent_channel_history(self, target):
        """Descarga e indexa los mensajes recientes del canal para asegurar que las tarjetas estén al día."""
        try:
            entity = await self.client.get_entity(target)
            channel_title = getattr(entity, 'title', 'Chartoro FX')
            recent_msgs = await self.client.get_messages(entity, limit=50)
            logger.info(f"Sincronizando {len(recent_msgs)} mensajes recientes de '{channel_title}'...")
            for msg in reversed(recent_msgs):
                await self._sync_history_message(msg, channel_title)
            logger.info("Sincronización de historial reciente completada con éxito.")
        except Exception as sync_err:
            logger.warning(f"Aviso al sincronizar historial reciente de Telegram: {sync_err}")

    async def _sync_history_message(self, msg, channel_name: str = "Chartoro FX"):
        """Inserta mensajes recientes en base de datos si no existían previamente."""
        text = msg.raw_text or ""
        msg_id = msg.id
        if not text.strip():
            return
        
        channel_id = getattr(msg, 'chat_id', None) or settings.TARGET_CHANNEL_ID
        timestamp = msg.date or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        try:
            from sqlalchemy import select
            async with AsyncSessionLocal() as session:
                stmt = select(RawTelegramMessage).where(RawTelegramMessage.message_id == msg_id)
                res = await session.execute(stmt)
                existing = res.scalars().first()
                if not existing:
                    parsed_event = parse_signal(text, msg_id, channel_id)
                    is_sig = bool(parsed_event)
                    p_used = (parsed_event.parser_type.value if hasattr(parsed_event, 'parser_type') else "REGEX") if is_sig else "NONE"
                    
                    raw_msg = RawTelegramMessage(
                        message_id=msg_id,
                        channel_id=channel_id,
                        channel_name=channel_name,
                        raw_text=text,
                        parsed_success=is_sig,
                        parser_used=p_used,
                        error_reason=None,
                        received_at=timestamp
                    )
                    session.add(raw_msg)
                    await session.commit()
        except Exception as e:
            logger.debug(f"Aviso al sincronizar mensaje {msg_id}: {e}")

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

        text = event.raw_text or ""
        msg_id = event.id
        channel_id = event.chat_id
        timestamp = event.date or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        logger.info(f"Mensaje recibido [{msg_id}] en canal {channel_id}: '{text[:60]}...'")

        # 1. Intento de Parsing Primario con Regex Determinista (< 1ms)
        parsed_event = parse_signal(text, msg_id, channel_id)

        # 2. Si falla y la IA está habilitada, intento de Parsing Fallback con LLM
        if not parsed_event and settings.AI_FALLBACK_ENABLED:
            logger.info(f"Regex no detectó señal en [{msg_id}]. Intentando Fallback IA ({settings.AI_PROVIDER})...")
            parsed_event = await parse_with_ai(text, msg_id, channel_id)

        is_sig = bool(parsed_event)
        p_used = (parsed_event.parser_type.value if hasattr(parsed_event, 'parser_type') else "REGEX") if is_sig else "NONE"

        # 3. Guardar mensaje RAW en base de datos para auditoría inmutable
        try:
            async with AsyncSessionLocal() as session:
                raw_msg = RawTelegramMessage(
                    message_id=msg_id,
                    channel_id=channel_id,
                    channel_name="Chartoro FX Señales Gratis",
                    raw_text=text,
                    parsed_success=is_sig,
                    parser_used=p_used,
                    error_reason=None,
                    received_at=timestamp
                )
                session.add(raw_msg)
                await session.commit()
        except Exception as e:
            logger.error(f"Error al guardar mensaje raw en DB: {e}")

        # 4. Encolar señal si es una orden ejecutable
        if parsed_event:
            logger.info(
                f"SEÑAL DETECTADA [{p_used}]: "
                f"{type(parsed_event).__name__} en canal {channel_id}"
            )
            # Encolar en la cola asíncrona para consumo desacoplado
            await self.signal_queue.put(parsed_event)

        # 5. Notificar WebSocket en tiempo real para refrescar tarjetas del dashboard
        try:
            from backend.api.ws import manager
            await manager.broadcast({
                "type": "SIGNAL_PARSED",
                "message_id": msg_id,
                "is_signal": is_sig,
                "event": parsed_event.model_dump() if hasattr(parsed_event, "model_dump") else str(parsed_event) if parsed_event else None
            })
        except Exception as ws_err:
            logger.debug(f"Aviso al notificar señal por WS: {ws_err}")
