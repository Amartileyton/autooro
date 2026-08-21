import sqlite3

conn = sqlite3.connect('trading_bot.db')
with open('dump.sql', 'w', encoding='utf-8') as f:
    for line in conn.iterdump():
        f.write(f"{line}\n")
conn.close()
print("✅ dump.sql generado exitosamente.")
