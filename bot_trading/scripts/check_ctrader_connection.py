import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.broker.live_adapter import LiveBrokerAdapter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s")
logger = logging.getLogger("check_ctrader")

async def test_connection():
    print("=" * 60)
    print("PROBANDO CONEXIÓN A CTRADER OPEN API 2.0")
    print(f"Host: {settings.CTRADER_HOST}:{settings.CTRADER_PORT}")
    print(f"Account ID: {settings.CTRADER_ACCOUNT_ID}")
    print(f"Client ID: {settings.CTRADER_CLIENT_ID[:12]}...")
    print(f"Access Token: {settings.CTRADER_ACCESS_TOKEN[:8]}... (longitud: {len(settings.CTRADER_ACCESS_TOKEN)})")
    print("=" * 60)

    adapter = LiveBrokerAdapter()
    ok = await adapter.connect()
    if ok:
        print("\n[OK] CONEXION Y AUTENTICACION EXITOSAS EN CTRADER!")
        print(f"Symbol ID de XAUUSD: {adapter.symbol_id} (Digits: {adapter.symbol_digits})")
        print(f"Balance en Broker: ${adapter.balance:.2f} USD | Apalancamiento: {adapter.leverage:.0f}:1")
        
        # Esperar 2 segundos para recibir algun spot
        await asyncio.sleep(2.0)
        tick = await adapter.get_current_tick("XAUUSD")
        print(f"Ultima cotizacion XAUUSD recibida: Bid={tick.bid} | Ask={tick.ask}")
        
        acc = await adapter.get_account_info()
        print(f"Account Info: Equidad=${acc.equity:.2f} | Margen Libre=${acc.free_margin:.2f}")
        
        await adapter.disconnect()
    else:
        print("\n[ERROR] La conexion no se pudo completar. Revisa los logs anteriores.")

if __name__ == "__main__":
    asyncio.run(test_connection())
