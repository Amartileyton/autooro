from decimal import Decimal, InvalidOperation

def sanitize_price_str(raw: str):
    if not raw:
        return None
    s = raw.strip()
    if '.' in s and ',' in s:
        if s.find('.') < s.find(','):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif ',' in s:
        s = s.replace(',', '.')
    
    try:
        return Decimal(s)
    except InvalidOperation:
        return None

test_cases = [
    ("4383.69", Decimal("4383.69")),
    ("4383,69", Decimal("4383.69")),
    ("4.383,69", Decimal("4383.69")),
    ("4,383.69", Decimal("4383.69")),
    ("4491", Decimal("4491")),
    ("4491.5", Decimal("4491.5")),
    ("4491,5", Decimal("4491.5")),
]

all_passed = True
for inp, expected in test_cases:
    res = sanitize_price_str(inp)
    status = "OK" if res == expected else "FAIL"
    print(f"Input: '{inp}' -> Output: {res} (Expected: {expected}) -> {status}")
    if res != expected:
        all_passed = False

if all_passed:
    print("\n✅ Todos los casos de normalización decimal pasaron al 100%.")
