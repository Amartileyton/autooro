import asyncio
import httpx
from decimal import Decimal

API_URL = "http://localhost:8000/api/v1"
HEADERS = {"X-API-KEY": "sec_xauusd_trading_key_2026"}

async def test_saturation():
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Estado inicial
        res = await client.get(f"{API_URL}/state")
        spot = res.json()["xauusd_spot"]
        base_px = Decimal(str(spot["ask"]))
        print(f"=== PRUEBA DE SATURACIÓN DE SLOTS VÍA API ===")
        print(f"Precio Base: {base_px}")
        
        # Inyectaremos 6 señales en modo AUDIT para ver la lógica de slots:
        # Para que no se consideren la misma orden (enrichment), alternamos lados y precios con más de $2.00 de diferencia
        signals_data = [
            {"side": "BUY",  "delta": Decimal("0.00")},   # Slot 1
            {"side": "SELL", "delta": Decimal("0.00")},   # Slot 2 (Lado opuesto -> nuevo slot)
            {"side": "BUY",  "delta": Decimal("2.10")},   # Slot 3 (Mismo lado pero delta > $2.00 -> nuevo slot)
            {"side": "SELL", "delta": Decimal("2.10")},   # Slot 4 (Lado opuesto y delta > $2.00 -> nuevo slot)
            {"side": "BUY",  "delta": Decimal("-2.10")},  # Señal 5 -> ¿Qué pasa cuando ya hay 4 slots ocupados?
            {"side": "SELL", "delta": Decimal("-2.10")},  # Señal 6 -> ¿Qué pasa cuando ya hay 4 slots ocupados?
        ]
        
        for idx, s in enumerate(signals_data, 1):
            px = base_px + s["delta"]
            payload = {
                "side": s["side"],
                "entry_price": float(px),
                "sl_price": float(px - Decimal("10.00") if s["side"] == "BUY" else px + Decimal("10.00")),
                "tp1": float(px + Decimal("5.00") if s["side"] == "BUY" else px - Decimal("5.00")),
                "channel_name": f"Stress Channel {idx}",
                "execution_mode": "AUDIT"
            }
            print(f"-> Inyectando Señal #{idx}: {s['side']} @ {px:.2f}...")
            r = await client.post(f"{API_URL}/signal/test", json=payload, headers=HEADERS)
            await asyncio.sleep(0.4)
            
        print("\nEsperando 4 segundos a que el motor procese los 6 eventos...")
        await asyncio.sleep(4.0)
        
        # Consultar estado final de slots
        res_after = await client.get(f"{API_URL}/state")
        st = res_after.json()
        print("\n=== RESULTADO DE ASIGNACIÓN DE SLOTS ===")
        print(f"Slots Ocupados: {st['active_slots_count']} / {st['max_slots']}")
        for slot in st["slots"]:
            s_id = slot["slot_id"]
            if slot.get("is_active"):
                print(f"  ✅ Slot {s_id}: OCUPADO | Trade: {slot.get('ticket_id')} | {slot.get('side')} @ {slot.get('entry_price')}")
            else:
                print(f"  ⭕️ Slot {s_id}: DISPONIBLE")
                
        # Limpieza
        print("\n🧹 Limpiando los slots ocupados...")
        for slot in st["slots"]:
            if slot.get("is_active"):
                await client.post(f"{API_URL}/control/close-slot/{slot['slot_id']}", headers=HEADERS)
        print("Limpieza completada.")

if __name__ == "__main__":
    asyncio.run(test_saturation())
