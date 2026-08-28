import sqlite3
import os

db_path = os.path.expanduser('~/app/autooro/bot_trading/data/trading_bot.db')
if not os.path.exists(db_path):
    db_path = 'data/trading_bot.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

print("==================================================")
print(" 1. MENSAJES DE TELEGRAM REGISTRADOS (2026-08-27 / 2026-08-28)")
print("==================================================")
c.execute("""
SELECT id, message_id, channel_name, raw_text, parsed_success, parser_used, error_reason, received_at 
FROM raw_telegram_messages 
WHERE received_at >= '2026-08-27' 
ORDER BY id ASC
""")
rows = c.fetchall()
for r in rows:
    print(f"ID: {r[0]} | MsgID: {r[1]} | Canal: {r[2]} | Parsed: {r[4]} | Parser: {r[5]} | Error: {r[6]} | Fecha: {r[7]}")
    print(f"Texto:\n{r[3]}")
    print("-" * 50)

print("\n==================================================")
print(" 2. TRADES EJECUTADOS EN LA BASE DE DATOS")
print("==================================================")
c.execute("""
SELECT id, ticket_id, channel_name, side, entry_price, close_price, initial_sl, current_sl, tp1, tp2, tp3, status, pnl, open_time, close_time, close_reason
FROM trades 
ORDER BY id ASC
""")
trades = c.fetchall()
for t in trades:
    print(f"ID: {t[0]} | Ticket: {t[1]} | Canal: {t[2]} | Side: {t[3]} | Entrada: {t[4]} | Salida: {t[5]} | PnL: ${t[12]} | Estado: {t[11]}")
    print(f"   SL: {t[7]} (Init: {t[6]}) | TPs: [{t[8]}, {t[9]}, {t[10]}]")
    print(f"   Open: {t[13]} | Close: {t[14]} | Motivo: {t[15]}")
    print("-" * 50)
