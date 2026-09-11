import asyncio
from decimal import Decimal
from backend.ingesta.schemas import TradingSignalEvent, OrderSide as SchemaOrderSide
from backend.main import app_state
from backend.shared.enums import ExecutionMode

async def test_exhaustion():
    risk_engine = app_state["risk_engine"]
    state_machine = app_state["state_machine"]
    
    print("=== TEST DE SATURACIÓN DE SLOTS (REGLA DE 4 SLOTS) ===")
    print(f"Slots iniciales ocupados: {len(state_machine.active_slots)} / {risk_engine.max_slots}")
    
    # Simular 6 señales distintas
    for i in range(1, 7):
        side = SchemaOrderSide.BUY if i % 2 != 0 else SchemaOrderSide.SELL
        entry_px = Decimal("4389.00") + Decimal(str(i * 3.0))
        sig = TradingSignalEvent(
            asset="XAUUSD",
            side=side,
            entry_price=entry_px,
            sl_price=entry_px - Decimal("10.00"),
            tp_levels=[entry_px + Decimal("5.00")],
            requires_dynamic_sl=False,
            raw_text=f"STRESS TEST SIGNAL {i}",
            message_id=9000 + i,
            channel_id=-1002763662248,
            channel_name="Stress Test Channel",
            execution_mode="AUDIT"
        )
        
        # 1. Evaluar si hay slot disponible
        can_execute, slot_id, reason = risk_engine.evaluate_signal_for_slot(sig, state_machine.active_slots)
        if can_execute:
            print(f"✅ Señal #{i} ({side.value} @ {entry_px}): ACEPTADA -> Asignada a Slot {slot_id}")
            # Abrir trade en ese slot
            await state_machine.open_new_trade(
                slot_id=slot_id,
                side=sig.side,
                lot_size=Decimal("0.01"),
                entry_price=entry_px,
                sl=sig.sl_price,
                tp_levels=sig.tp_levels,
                raw_signal_id=sig.message_id,
                channel_id=sig.channel_id,
                channel_name=sig.channel_name,
                execution_mode=ExecutionMode.AUDIT
            )
        else:
            print(f"⛔️ Señal #{i} ({side.value} @ {entry_px}): RECHAZADA -> Motivo: {reason} (Límite de 4 slots alcanzado)")
            
    print("\n=== ESTADO FINAL TRAS LAS 6 SEÑALES ===")
    print(f"Total Slots Ocupados: {len(state_machine.active_slots)} / {risk_engine.max_slots}")
    for s_id in range(1, 5):
        tr = state_machine.active_slots.get(s_id)
        if tr:
            print(f"  Slot {s_id}: OCUPADO por Trade {tr.ticket_id} ({tr.side.value} @ {tr.entry_price})")
        else:
            print(f"  Slot {s_id}: LIBRE")
            
    # Limpiar los slots de prueba
    print("\n🧹 Limpiando slots de prueba...")
    for s_id in list(state_machine.active_slots.keys()):
        await state_machine.close_slot_manually(s_id)
    print("Slots limpiados con éxito. Estado restaurado a 0 slots.")

if __name__ == "__main__":
    asyncio.run(test_exhaustion())
