import json
import re
import sys
from collections import Counter
from decimal import Decimal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

with open("deep_channel_history.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

print(f"Total mensajes cargados: {len(messages)}")

signals = [m for m in messages if m["parsed_type"] == "TradingSignalEvent"]
modifiers = [m for m in messages if m["parsed_type"] == "ModifierSignalEvent"]
discarded = [m for m in messages if m["parsed_type"] is None and m["text"].strip()]

print(f"Señales detectadas: {len(signals)}")
print(f"Modificadores detectados: {len(modifiers)}")
print(f"Descartados: {len(discarded)}")

print("\n" + "="*70)
print("1. ANÁLISIS DE FALSOS NEGATIVOS (Mensajes descartados con palabras de trading)")
print("="*70)

trading_keywords = re.compile(r'\b(BUY|SELL|COMPRA|VENTA|LONG|SHORT|ENTRY|ENTRADA|SL|TP|XAUUSD|GOLD|ORO|PIPS)\b', re.IGNORECASE)

potential_missed = []
for m in discarded:
    text = m["text"]
    # Si contiene palabras de trading pero fue descartado
    if trading_keywords.search(text):
        potential_missed.append(m)

print(f"Mensajes descartados que contienen alguna palabra clave de trading: {len(potential_missed)}")

# Imprimir una muestra de 20 mensajes sospechosos para verificar si eran spam o señales reales no capturadas
print("\nMuestra de 25 mensajes descartados con palabras de trading:")
for i, m in enumerate(potential_missed[:25]):
    preview = m['text'].replace('\n', ' ')[:100]
    print(f"[{m['message_id']}] ({m['date'][:10]}): {preview}")

print("\n" + "="*70)
print("2. ANÁLISIS DE PAREJAS: ALERTA RÁPIDA (NOW) vs PLANTILLA OFICIAL (SIGNAL ALERT)")
print("="*70)

quick_alerts = [m for m in signals if "NOW" in m["text"].upper() or "PIPS" in m["text"].upper()]
templates = [m for m in signals if "SIGNAL ALERT" in m["text"].upper() or "ENTRY POINT" in m["text"].upper()]

print(f"Total Alertas Rápidas (BUY NOW / SELL NOW): {len(quick_alerts)}")
print(f"Total Plantillas Completas (SIGNAL ALERT): {len(templates)}")

# Ver si están vinculadas por tiempo (dentro de 1-3 minutos)
paired_count = 0
for q in quick_alerts:
    q_date = q["date"]
    q_entry = q["parsed_data"]["entry_price"]
    q_side = q["parsed_data"]["side"]
    
    # Buscar si hay un template en los siguientes 5 minutos con el mismo precio
    for t in templates:
        t_entry = t["parsed_data"]["entry_price"]
        t_side = t["parsed_data"]["side"]
        if q_entry == t_entry and q_side == t_side and t["date"] >= q_date:
            paired_count += 1
            break

print(f"Alertas Rápidas seguidas de una Plantilla Completa con el mismo precio: {paired_count} / {len(quick_alerts)}")

print("\n" + "="*70)
print("3. ANÁLISIS DE MODIFICADORES (Move SL, BE, Cierres)")
print("="*70)

for mod in modifiers:
    data = mod["parsed_data"]
    print(f"[{mod['message_id']}] ReplyTo: {mod['reply_to_msg_id']} | Tipo: {data['signal_type']} | Precio: {data['target_price']} | Texto: '{mod['text'].strip()}'")

print("\n" + "="*70)
print("4. BÚSQUEDA DE OTROS PATRONES DE MODIFICACIÓN EN DESCARTADOS")
print("="*70)

mod_keywords = re.compile(r'\b(MOVE|MOVER|BREAK\s*EVEN|CLOSE|CIERRA|CERRAR|PARTIAL|PARCIAL|PROTECT|PROTEGER|BE)\b', re.IGNORECASE)
for m in discarded:
    if mod_keywords.search(m["text"]):
        # Ver si tiene formato de acción
        print(f"[{m['message_id']}] Posible modificador ignorado: '{m['text'].strip().replace(chr(10), ' ')[:90]}'")
