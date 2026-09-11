import asyncio
import httpx
from decimal import Decimal

API_URL = "http://localhost:8000/api/v1"
HEADERS = {"X-API-KEY": "sec_xauusd_trading_key_2026"}

async def main():
    async with httpx.AsyncClient(timeout=15.0) as client:
        # 1. Estado inicial
        resp = await client.get(f"{API_URL}/state")
        state = resp.json()
        spot = state["xauusd_spot"]
        ask_px = spot["ask"]
        active_cnt = state["active_slots_count"]
        max_cnt = state["max_slots"]
        print("=== ESTADO INICIAL ===")
        print(f"XAUUSD Spot: Ask=${ask_px:.2f} | Bid=${spot['bid']:.2f}")
        print(f"Slots Activos Iniciales: {active_cnt} / {max_cnt}")
        print("======================\n")
        
        # 2. Enviar 6 señales consecutivas
        print("🚀 Disparando 6 señales consecutivas en ráfaga...")
        for i in range(1, 7):
            entry = Decimal(str(ask_px)) + Decimal(str(round((i - 3) * 0.05, 2)))
            payload = {
                "side": "BUY",
                "entry_price": float(entry),
                "sl_price": float(entry - Decimal("12.00")),
                "tp1": float(entry + Decimal("3.00")),
                "tp2": float(entry + Decimal("8.00")),
                "tp3": float(entry + Decimal("15.00")),
                "channel_name": f"Chartoro Stress-{i}",
                "execution_mode": "PRODUCTION"
            }
            print(f"-> Inyectando Señal #{i}: BUY @ {entry:.2f}...")
            r = await client.post(f"{API_URL}/signal/test", json=payload, headers=HEADERS)
            await asyncio.sleep(0.3)
            
        print("\nEsperando 8 segundos a que el Signal Consumer Worker procese la cola y cTrader responda...")
        await asyncio.sleep(8.0)
        
        # 3. Consultar estado resultante de los slots
        resp_after = await client.get(f"{API_URL}/state")
        state_after = resp_after.json()
        print("\n=== ESTADO RESULTANTE DE LOS SLOTS TRAS LA RÁFAGA ===")
        print(f"Slots Activos Ocupados: {state_after['active_slots_count']} / {state_after['max_slots']}")
        for slot in state_after["slots"]:
            status = slot.get("status")
            trade = slot.get("trade")
            if trade:
                print(f"  [Slot {slot['slot_id']}] OCUPADO -> Ticket cTrader: {trade.get('ticket_id')} | Entrada: {trade.get('entry_price')} | SL: {trade.get('sl')} | TP1: {trade.get('tp1')}")
            else:
                print(f"  [Slot {slot['slot_id']}] {status}")
        print("====================================================\n")
        
        # 4. Limpieza: Cerrar las órdenes de prueba para dejar la cuenta limpia
        print("🧹 Limpiando: Cerrando los slots ocupados para dejar la cuenta demo en $1,000...")
        for slot in state_after["slots"]:
            if slot.get("is_active") or slot.get("trade"):
                slot_id = slot["slot_id"]
                print(f"  Cerrando Slot {slot_id}...")
                r_close = await client.post(f"{API_URL}/trade/close/{slot_id}", headers=HEADERS)
                print(f"  Slot {slot_id} cerrado: {r_close.json().get('message', 'OK')}")
                await asyncio.sleep(0.8)
                
        print("\n✅ Prueba de estrés y limpieza completadas exitosamente.")

if __name__ == "__main__":
    asyncio.run(main())
