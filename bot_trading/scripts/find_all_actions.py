import json
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

with open("deep_channel_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pats = re.compile(
    r'\b(cerrar|cerramos|cierra|close|cancel|cancela|cancelar|salgan|salir|invalida|invalidado|'
    r'breakeven|break\s*even|be|sl\s*a|sl\s*to|move\s*sl|mover\s*sl)\b',
    re.IGNORECASE
)

matches = [x for x in data if pats.search(x.get('text', ''))]
print(f"Total coincidencias: {len(matches)}\n")

for x in matches:
    preview = x['text'].replace('\n', ' ')[:120]
    print(f"[{x['message_id']}] reply_to={x['reply_to_msg_id']} | Type={x['parsed_type']} | Text: {preview}")
