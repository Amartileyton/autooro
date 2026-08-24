import os
import sqlite3

EXTRA_MESSAGES_2026_08_24 = [
    (
        901,
        7915,
        -1002763662248,
        "Chartoro FX Señales Gratis",
        "XAUUSD BUY NOW 4635.20\nSet TP1 +68 Pips",
        1,
        "REGEX",
        None,
        "2026-08-24 07:15:22.000000"
    ),
    (
        902,
        7916,
        -1002763662248,
        "Chartoro FX Señales Gratis",
        "**🚨 SIGNAL ALERT🚨**\n\n**📊 **#XAUUSD** **\n\n**Direction: 📈 **#BUY** **\n\n** Entry Point: **4635.20\n**⛔️ Stop Loss (SL): **4627.00\n\n**🏆 TP1: 4642.00\n**🏆 TP2:** 4647.00\n**🏆 TP3:** 4655.00",
        1,
        "REGEX",
        None,
        "2026-08-24 07:16:10.000000"
    ),
    (
        903,
        7917,
        -1002763662248,
        "Chartoro FX Señales Gratis",
        "⚡️ Move SL to 4635.20 (Break Even)",
        1,
        "REGEX",
        None,
        "2026-08-24 07:22:45.000000"
    ),
    (
        904,
        7918,
        -1002763662248,
        "Chartoro FX Señales Gratis",
        "**DIRECTO A LAS GANANCIAS **⚡️\n\n**#XAUUSD**** TP1 HIT, +68 Pips 🏆**\n\n__Sesión de madrugada completada con éxito.__",
        0,
        "NONE",
        None,
        "2026-08-24 07:28:15.000000"
    )
]


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
        with open(dump_path, "r", encoding="utf-8") as f:
            dump_text = f.read()

        for stmt in dump_text.split(";\n"):
            stmt = stmt.strip()
            if "raw_telegram_messages" in stmt and stmt.startswith("INSERT INTO"):
                stmt = stmt.replace('INSERT INTO "raw_telegram_messages"', 'INSERT OR IGNORE INTO raw_telegram_messages (id, message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)')
                stmt = stmt.replace('INSERT INTO raw_telegram_messages', 'INSERT OR IGNORE INTO raw_telegram_messages (id, message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)')
                try:
                    cursor.execute(stmt + ";")
                    count += 1
                except Exception as e:
                    pass

    # Insertar siempre de forma explicita los mensajes de 24/08/2026
    for msg in EXTRA_MESSAGES_2026_08_24:
        cursor.execute(
            """
            INSERT OR REPLACE INTO raw_telegram_messages 
            (id, message_id, channel_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            msg
        )
        count += 1

    conn.commit()
    cursor.execute("SELECT count(*) FROM raw_telegram_messages;")
    total = cursor.fetchone()[0]
    print(f"Seeding completado. Mensajes procesados: {count} | Total en base de datos: {total}")
    conn.close()

if __name__ == "__main__":
    seed_database()
