import os
import sqlite3

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
    if dump_path and os.path.exists(dump_path):
        print(f"Leyendo senales historicas desde {dump_path} para {db_path}...")
        try:
            with open(dump_path, "r", encoding="utf-8") as f:
                dump_text = f.read()
            cursor.executescript(dump_text)
            conn.commit()
        except Exception as e:
            print(f"Aviso al ejecutar dump: {e}")

    cursor.execute("SELECT count(*) FROM raw_telegram_messages;")
    total = cursor.fetchone()[0]
    print(f"Seeding completado. Total en base de datos: {total}")
    conn.close()

if __name__ == "__main__":
    seed_database()
