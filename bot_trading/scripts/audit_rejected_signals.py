import sqlite3
import re
from datetime import datetime

conn = sqlite3.connect('/home/adriamartileyton2/app/autooro/bot_trading/data/trading_bot.db')
c = conn.cursor()

c.execute("""
SELECT id, message_id, channel_name, raw_text, parsed_success, error_reason, received_at 
FROM raw_telegram_messages 
WHERE id IN (
    SELECT id FROM raw_telegram_messages 
    WHERE (raw_text LIKE '%Pair (Gold vs USD)%' OR raw_text LIKE '%XAUUSD%' OR raw_text LIKE '%GOLD%')
    AND received_at >= '2026-08-27'
)
ORDER BY id ASC
""")

rows = c.fetchall()
print(f"Total mensajes relevantes: {len(rows)}")
for r in rows:
    print(f"\n==================================================")
    print(f"DB ID: {r[0]} | MsgID: {r[1]} | Canal: {r[2]} | Fecha: {r[6]} | Error: {r[5]}")
    print(f"Texto:\n{r[3]}")
