import asyncio
import os
import sys
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from telethon import TelegramClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.ingesta.parser import parse_signal

async def main():
    session_candidates = [
        "data/bot_session",
        "/app/data/bot_session",
        "bot_session",
        "/app/bot_session"
    ]
    session_name = "data/bot_session"
    for candidate in session_candidates:
        if os.path.exists(f"{candidate}.session") or os.path.exists(candidate):
            session_name = candidate
            break

    print(f"[1/4] Conectando a Telethon con sesión '{session_name}'...")
    client = TelegramClient(session_name, settings.TG_API_ID, settings.TG_API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("ERROR: Sesión de Telethon no autorizada.")
        return

    target = settings.TARGET_CHANNEL_ID
    entity = await client.get_entity(target)
    channel_name = getattr(entity, 'title', 'Chartoro FX')
    print(f"[2/4] Descargando últimos 1000 mensajes de '{channel_name}' ({target})...")

    messages = await client.get_messages(entity, limit=1000)
    print(f"-> Descargados {len(messages)} mensajes en total.")

    # Conectar a la base de datos de producción
    db_candidates = ["/app/trading_bot.db", "trading_bot.db", "bot_trading/trading_bot.db"]
    db_path = "/app/trading_bot.db" if os.path.exists("/app/trading_bot.db") else "trading_bot.db"
    
    print(f"[3/4] Reiniciando y saneando base de datos SQLite en: {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Recrear tablas
    cursor.execute("DROP TABLE IF EXISTS raw_telegram_messages;")
    cursor.execute("DROP TABLE IF EXISTS trades;")
    cursor.execute("DROP TABLE IF EXISTS system_audit_logs;")
    cursor.execute("DROP TABLE IF EXISTS news_interactions;")

    cursor.execute("""
    CREATE TABLE raw_telegram_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER UNIQUE,
        channel_id INTEGER,
        channel_name VARCHAR(120),
        raw_text TEXT NOT NULL,
        parsed_success BOOLEAN NOT NULL,
        parser_used VARCHAR(30) NOT NULL,
        error_reason VARCHAR(255),
        received_at DATETIME NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id VARCHAR(50) UNIQUE,
        raw_signal_id INTEGER,
        side VARCHAR(10) NOT NULL,
        status VARCHAR(20) NOT NULL,
        slot_id INTEGER NOT NULL,
        lot_size NUMERIC(10, 2) NOT NULL,
        initial_lot_size NUMERIC(10, 2) NOT NULL,
        entry_price NUMERIC(10, 2) NOT NULL,
        current_sl NUMERIC(10, 2) NOT NULL,
        initial_sl NUMERIC(10, 2) NOT NULL,
        tp1 NUMERIC(10, 2) NOT NULL,
        tp2 NUMERIC(10, 2),
        tp3 NUMERIC(10, 2),
        current_price NUMERIC(10, 2) NOT NULL,
        current_pnl NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
        realized_pnl NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
        close_price NUMERIC(10, 2),
        close_reason VARCHAR(100),
        opened_at DATETIME NOT NULL,
        closed_at DATETIME,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE system_audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type VARCHAR(50) NOT NULL,
        actor VARCHAR(50) NOT NULL,
        slot_id INTEGER,
        ticket_id VARCHAR(50),
        details_json TEXT,
        created_at DATETIME NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE news_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_id VARCHAR(100) NOT NULL,
        news_title VARCHAR(255) NOT NULL,
        news_url TEXT,
        news_asset VARCHAR(50) DEFAULT 'MACRO',
        action_type VARCHAR(30) NOT NULL,
        created_at DATETIME NOT NULL
    );
    """)

    madrid_tz = ZoneInfo("Europe/Madrid")
    signals_detected = []

    # Insertar mensajes cronológicamente (antiguo -> reciente)
    for msg in reversed(messages):
        if not msg.text or len(msg.text.strip()) == 0:
            continue

        utc_dt = msg.date
        madrid_dt = utc_dt.astimezone(madrid_tz)
        madrid_str = madrid_dt.strftime("%d/%m/%Y %H:%M:%S")

        parsed = parse_signal(msg.text, message_id=msg.id, channel_id=target)
        parsed_success = bool(parsed)
        parser_used = "REGEX" if parsed_success else "NONE"

        cursor.execute(
            """
            INSERT OR IGNORE INTO raw_telegram_messages 
            (message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                msg.id,
                target,
                channel_name,
                msg.text,
                parsed_success,
                parser_used,
                None,
                utc_dt.strftime("%Y-%m-%d %H:%M:%S.%f")
            )
        )

        if parsed_success:
            signals_detected.append({
                "msg_id": msg.id,
                "madrid_time": madrid_str,
                "type": parsed.event_type if hasattr(parsed, 'event_type') else type(parsed).__name__,
                "side": getattr(parsed, 'side', None),
                "entry": getattr(parsed, 'entry_price', None),
                "sl": getattr(parsed, 'sl_price', None),
                "tp1": getattr(parsed, 'tp1', None) or (parsed.tp_levels[0] if getattr(parsed, 'tp_levels', None) else None),
                "tp2": getattr(parsed, 'tp2', None) or (parsed.tp_levels[1] if getattr(parsed, 'tp_levels', None) and len(parsed.tp_levels) > 1 else None),
                "tp3": getattr(parsed, 'tp3', None) or (parsed.tp_levels[2] if getattr(parsed, 'tp_levels', None) and len(parsed.tp_levels) > 2 else None),
                "text": msg.text.replace('\n', ' ')[:70]
            })

    conn.commit()

    # Generar dump.sql actualizado
    dump_path = "/app/dump.sql" if os.path.exists("/app") else "dump.sql"
    with open(dump_path, "w", encoding="utf-8") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    print(f"[4/4] Base de datos regenerada y dump.sql guardado con éxito ({len(signals_detected)} señales detectadas).")

    conn.close()
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
