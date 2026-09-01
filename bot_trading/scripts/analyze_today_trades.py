import sqlite3
import os
import sys
import json
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

# Localizar la base de datos
db_candidates = [
    "data/trading_bot.db",
    "trading_bot.db",
    "/app/data/trading_bot.db",
    "/app/trading_bot.db"
]

db_path = None
for p in db_candidates:
    if os.path.exists(p) and os.path.getsize(p) > 0:
        db_path = p
        break

if not db_path:
    # Buscar recursivamente
    import glob
    for p in glob.glob("**/*.db", recursive=True):
        if "trading" in p and os.path.getsize(p) > 0:
            db_path = p
            break

if not db_path:
    print("❌ No se encontró la base de datos SQLite.")
    sys.exit(1)

print(f"📦 Analizando base de datos: {db_path}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Obtener mensajes de hoy (o los últimos 50)
cur.execute("""
    SELECT id, message_id, channel_name, raw_text, error_reason, received_at 
    FROM raw_telegram_messages 
    ORDER BY id DESC 
    LIMIT 50;
""")
rows = cur.fetchall()

print("=" * 80)
print(f"📊 INFORME DE SEÑALES RECIBIDAS (Últimos {len(rows)} mensajes)")
print("=" * 80)

# Importar parser para extraer niveles
try:
    from backend.ingesta.parser import parse_signal
    from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent
except Exception as e:
    parse_signal = None

today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

signals_found = []
updates_found = []

for r in reversed(rows):
    mid, msg_id, channel, text, error_reason, received_at = r
    if not text:
        continue
    
    parsed = parse_signal(text, message_id=msg_id, channel_name=channel) if parse_signal else None
    
    if isinstance(parsed, TradingSignalEvent):
        signals_found.append({
            "id": mid,
            "msg_id": msg_id,
            "channel": channel,
            "date": received_at,
            "side": parsed.side.value if hasattr(parsed.side, 'value') else str(parsed.side),
            "entry": float(parsed.entry_price or 0),
            "entry_min": float(parsed.entry_min) if parsed.entry_min else None,
            "entry_max": float(parsed.entry_max) if parsed.entry_max else None,
            "sl": float(parsed.sl_price) if parsed.sl_price else None,
            "tp1": float(parsed.tp_levels[0]) if len(parsed.tp_levels) > 0 else None,
            "tp2": float(parsed.tp_levels[1]) if len(parsed.tp_levels) > 1 else None,
            "tp3": float(parsed.tp_levels[2]) if len(parsed.tp_levels) > 2 else None,
            "reason": error_reason,
            "raw": text
        })
    else:
        # Mensajes de seguimiento (TP hits, BE, etc.)
        t_upper = text.upper()
        if any(w in t_upper for w in ["TP", "TARGET", "HIT", "PIPS", "STOP", "PROFIT", "CLOSE"]):
            updates_found.append({
                "channel": channel,
                "date": received_at,
                "text": text.strip().replace("\n", " | ")
            })

print(f"\n🎯 SEÑALES DETECTADAS: {len(signals_found)}")
for i, s in enumerate(signals_found, 1):
    print(f"\n--- SEÑAL #{i} ---")
    print(f" Canal:      {s['channel']}")
    print(f" Fecha/Hora: {s['date']}")
    print(f" Operación:  {s['side']} XAUUSD")
    entry_desc = f"${s['entry']:.2f}"
    if s['entry_min'] and s['entry_max']:
        entry_desc += f" (Rango: ${s['entry_min']:.2f} - ${s['entry_max']:.2f})"
    print(f" Entrada:    {entry_desc}")
    print(f" Stop Loss:  ${s['sl']:.2f}" if s['sl'] else " Stop Loss:  ---")
    print(f" TP1 / TP2:  ${s['tp1']} / ${s['tp2']}")
    print(f" TP3:        ${s['tp3']}")
    print(f" Estado:     {s['reason'] or 'EJECUTADA / SIN ERROR'}")
    print(f" Texto Original:\n{s['raw']}")

print("\n" + "=" * 80)
print(f"📢 MENSAJES DE SEGUIMIENTO / HITOS DEL CANAL ({len(updates_found)} avisos)")
print("=" * 80)
for u in updates_found[-15:]:
    print(f"[{u['date']}] ({u['channel']}) {u['text']}")

conn.close()
