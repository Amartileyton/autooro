import asyncio
import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from decimal import Decimal
from backend.broker.paper import LocalPaperBroker
from backend.database.models import OrderSide
from backend.ingesta.parser import parse_signal

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


async def main():
    print("==================================================")
    print(" TEST DE PRECISIÓN DECIMAL Y API DEL BROKER")
    print("==================================================")

    broker = LocalPaperBroker()
    await broker.connect()

    # 1. Simular señal recibida con comas (4383,69)
    signal_text_comma = """
    🚨 SIGNAL ALERT🚨
    📊 #XAUUSD
    Direction: #BUY
    Entry Point: 4383,69
    ⛔️ Stop Loss (SL): 4375,50
    🏆 TP1: 4386,69
    🏆 TP2: 4392,00
    🏆 TP3: 4400,00
    """
    event = parse_signal(signal_text_comma)
    print(f"\n1. Ingesta con coma española:")
    print(f"• Entry Parseado: {event.entry_price} (Tipo: {type(event.entry_price).__name__})")
    print(f"• SL Parseado: {event.sl_price} (Tipo: {type(event.sl_price).__name__})")
    print(f"• TP1 Parseado: {event.tp_levels[0]} (Tipo: {type(event.tp_levels[0]).__name__})")

    # 2. Ejecutar Orden en el Broker
    ticket = await broker.execute_order(
        symbol="XAUUSD",
        side=event.side,
        lot_size=Decimal("0.50"),
        entry_price=event.entry_price,
        sl=event.sl_price,
        tp=event.tp_levels[2],
        comment="Test-Precision"
    )
    pos = broker.positions[ticket]
    print(f"\n2. Orden ejecutada en Broker [Ticket: {ticket}]:")
    print(f"• Precio de Entrada en Broker: {pos.entry_price}")
    print(f"• Stop Loss en Broker: {pos.sl}")
    print(f"• Take Profit en Broker: {pos.tp}")
    print(f"• Lote: {pos.lot_size}")

    # 3. Modificar SL con decimales
    mod_text = "Move SL to 4385,25"
    mod_event = parse_signal(mod_text)
    print(f"\n3. Modificador recibido: '{mod_text}' -> Precio normalizado: {mod_event.target_price}")
    
    await broker.modify_order(ticket, new_sl=mod_event.target_price)
    print(f"• Nuevo SL confirmado en Broker: {broker.positions[ticket].sl}")

    # 4. Simular cierre a mercado y verificar cálculo de PnL
    close_price = Decimal("4395.75")
    exec_price, pnl = await broker.close_order(ticket, close_price=close_price, reason="TP_HIT")
    print(f"\n4. Orden cerrada @ {exec_price}:")
    print(f"• PnL Realizado exacto: ${pnl:.2f} USD")
    # Cálculo manual: (4395.75 - 4383.69) * 0.50 lots * 100 = 12.06 * 50 = +603.00 USD
    expected_pnl = (Decimal("4395.75") - Decimal("4383.69")) * Decimal("0.50") * Decimal("100.0")
    print(f"• PnL Esperado matemáticamente: ${expected_pnl:.2f} USD")
    assert pnl == expected_pnl, f"PnL {pnl} no coincide con {expected_pnl}"

    await broker.disconnect()
    print("\n✅ Verificación de precisión y compatibilidad con el Broker completada con éxito.")


if __name__ == "__main__":
    asyncio.run(main())
