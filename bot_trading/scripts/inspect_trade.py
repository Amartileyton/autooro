import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

with open("deep_channel_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

msgs = [x for x in data if x['message_id'] in (7616, 7617, 7618)]
print(json.dumps(msgs, indent=2, ensure_ascii=False))
