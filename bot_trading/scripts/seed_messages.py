import os
import re
import sqlite3

def seed_database():
    db_path = "trading_bot.db"
    dump_candidates = ["dump.sql", "bot_trading/dump.sql", "/app/dump.sql"]
    dump_path = None
    for dp in dump_candidates:
        if os.path.exists(dp):
            dump_path = dp
            break

    if not dump_path:
        print("No se encontró dump.sql")
        return

    print(f"Leyendo señales históricas desde {dump_path}...")
    with open(dump_path, "r", encoding="utf-8") as f:
        dump_text = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Asegurar que la tabla existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_telegram_messages (
        id INTEGER NOT NULL, 
        message_id INTEGER, 
        channel_id INTEGER, 
        channel_name VARCHAR(120), 
        raw_text TEXT NOT NULL, 
        parsed_success BOOLEAN NOT NULL, 
        parser_used VARCHAR(30) NOT NULL, 
        error_reason VARCHAR(255), 
        received_at DATETIME NOT NULL, 
        PRIMARY KEY (id)
    );
    """)

    count = 0
    # Extraer y ejecutar los INSERT de raw_telegram_messages
    for stmt in dump_text.split(";\n"):
        stmt = stmt.strip()
        if "raw_telegram_messages" in stmt and stmt.startswith("INSERT INTO"):
            stmt = stmt.replace('INSERT INTO "raw_telegram_messages"', 'INSERT OR IGNORE INTO raw_telegram_messages (id, message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)')
            stmt = stmt.replace('INSERT INTO raw_telegram_messages', 'INSERT OR IGNORE INTO raw_telegram_messages (id, message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)')
            try:
                cursor.execute(stmt + ";")
                count += 1
            except Exception as e:
                print(f"Error en sentencia: {e}")

    conn.commit()
    cursor.execute("SELECT count(*) FROM raw_telegram_messages;")
    total = cursor.fetchone()[0]
    print(f"Seeding completado. Mensajes procesados: {count} | Total en base de datos: {total}")
    conn.close()

if __name__ == "__main__":
    seed_database()
