import os
import sqlite3
import re
import logging

logger = logging.getLogger("trading_bot.seed")

def seed_database():
    db_candidates = ["trading_bot.db", "bot_trading/trading_bot.db", "/app/trading_bot.db"]
    db_path = "trading_bot.db"
    for db in db_candidates:
        if os.path.exists(db):
            db_path = db
            break

    dump_candidates = ["dump.sql", "bot_trading/dump.sql", "/app/dump.sql"]
    dump_path = None
    for dp in dump_candidates:
        if os.path.exists(dp):
            dump_path = dp
            break

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Asegurar que las tablas existan con IF NOT EXISTS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_telegram_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            message_id INTEGER, 
            channel_id INTEGER, 
            channel_name VARCHAR(120), 
            raw_text TEXT NOT NULL, 
            parsed_success BOOLEAN NOT NULL, 
            parser_used VARCHAR(30) NOT NULL, 
            error_reason VARCHAR(255), 
            received_at DATETIME NOT NULL
        );
        """)

        cursor.execute("SELECT count(*) FROM raw_telegram_messages;")
        existing_count = cursor.fetchone()[0]

        if existing_count == 0 and dump_path and os.path.exists(dump_path):
            print(f"Poblando señales históricas desde {dump_path} en {db_path}...")
            with open(dump_path, "r", encoding="utf-8") as f:
                dump_text = f.read()

            # Extraer y ejecutar solo los INSERT OR IGNORE limpios
            insert_statements = re.findall(r'INSERT INTO "raw_telegram_messages".*?;', dump_text, re.DOTALL)
            if not insert_statements:
                insert_statements = re.findall(r'INSERT INTO raw_telegram_messages.*?;', dump_text, re.DOTALL)

            inserted = 0
            for stmt in insert_statements:
                safe_stmt = stmt.replace('INSERT INTO', 'INSERT OR IGNORE INTO')
                try:
                    cursor.execute(safe_stmt)
                    inserted += 1
                except Exception:
                    pass

            conn.commit()
            print(f"-> Insertados {inserted} mensajes históricos de Telegram con éxito.")

        cursor.execute("SELECT count(*) FROM raw_telegram_messages;")
        total = cursor.fetchone()[0]
        print(f"Total de mensajes en base de datos: {total}")
        conn.close()
    except Exception as e:
        print(f"Aviso en seed_database: {e}")

if __name__ == "__main__":
    seed_database()
