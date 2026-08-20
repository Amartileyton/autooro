import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

with open("deep_channel_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

signals = [x for x in data if x["parsed_type"] == "TradingSignalEvent"]
print(f"Total señales a auditar: {len(signals)}\n")

anomalies = []
for s in signals:
    d = s["parsed_data"]
    entry = float(d["entry_price"])
    sl = float(d["sl_price"]) if d["sl_price"] else None
    tps = [float(tp) for tp in d["tp_levels"]]
    side = d["side"]
    
    # Comprobaciones de coherencia
    if side == "BUY":
        if sl and sl >= entry:
            anomalies.append((s["message_id"], "BUY SL >= Entry", s))
        if tps and tps[0] <= entry:
            anomalies.append((s["message_id"], "BUY TP1 <= Entry", s))
    elif side == "SELL":
        if sl and sl <= entry:
            anomalies.append((s["message_id"], "SELL SL <= Entry", s))
        if tps and tps[0] >= entry:
            anomalies.append((s["message_id"], "SELL TP1 >= Entry", s))

print(f"Total anomalías encontradas en 91 señales: {len(anomalies)}")
for aid, reason, s in anomalies:
    print(f"Anomalía en [{aid}]: {reason}")
