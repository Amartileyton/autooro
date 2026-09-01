import asyncio
import logging
import time
import os
import sys
from decimal import Decimal

# Garantizar que el directorio raíz de bot_trading esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.broker.ctrader_protocol import (
    decode_proto_message,
    encode_proto_message,
    parse_protobuf_fields,
    build_app_auth_req,
    build_account_auth_req,
    build_symbols_list_req,
    build_subscribe_spots_req,
    parse_symbols_list_res,
    ProtoPayloadType
)
import ssl

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("inspect_ctrader")

async def test_live_gold_spot():
    print("=" * 60)
    print("INSPECCION EN VIVO DE CTRADER OPEN API - COTIZACION XAUUSD")
    print(f"Host: {settings.CTRADER_HOST}:{settings.CTRADER_PORT}")
    print(f"Account ID: {settings.CTRADER_ACCOUNT_ID}")
    print("=" * 60)

    if not settings.CTRADER_CLIENT_ID or not settings.CTRADER_ACCESS_TOKEN:
        print("[AVISO] Credenciales de cTrader no configuradas localmente en .env.")
        print("Este script puede ejecutarse directamente en la VM donde .env tiene las credenciales:")
        print("  python scripts/inspect_ctrader_live_gold.py")
        return

    ssl_ctx = ssl.create_default_context()
    account_id = int(settings.CTRADER_ACCOUNT_ID)
    reader, writer = await asyncio.open_connection(
        host=settings.CTRADER_HOST,
        port=settings.CTRADER_PORT,
        ssl=ssl_ctx
    )
    print("TLS Conectado.")

    async def send_msg(data):
        writer.write(data)
        await writer.drain()

    async def read_msg():
        import struct
        len_bytes = await reader.readexactly(4)
        msg_len = struct.unpack(">I", len_bytes)[0]
        body = await reader.readexactly(msg_len)
        return decode_proto_message(body)

    # 1. App Auth
    await send_msg(build_app_auth_req(settings.CTRADER_CLIENT_ID, settings.CTRADER_CLIENT_SECRET))
    p_type, payload, _ = await read_msg()
    print(f"App Auth Response: PayloadType={p_type}")

    # 2. Account Auth
    await send_msg(build_account_auth_req(account_id, settings.CTRADER_ACCESS_TOKEN))
    p_type, payload, _ = await read_msg()
    print(f"Account Auth Response: PayloadType={p_type}")

    # 3. Resolve XAUUSD symbolId
    await send_msg(build_symbols_list_req(account_id))
    p_type, payload, _ = await read_msg()
    symbols = parse_symbols_list_res(payload)
    gold_id = None
    for s in symbols:
        name = s["symbol_name"].upper().replace("/", "").replace(".", "").replace("_", "")
        if name in ["XAUUSD", "GOLD"]:
            gold_id = s["symbol_id"]
            print(f"Detectado {s['symbol_name']} con Symbol ID: {gold_id}")
            break

    if not gold_id:
        gold_id = 41
        print("Fallback Symbol ID: 41")

    # 4. Subscribe spots
    print(f"Suscribiendo a Spots para Symbol ID {gold_id}...")
    await send_msg(build_subscribe_spots_req(account_id, [gold_id]))

    # 5. Escuchar eventos entrantes (esperar ProtoOASpotEvent)
    print("Escuchando ticks de mercado en tiempo real...")
    for _ in range(10):
        try:
            p_type, payload, _ = await asyncio.wait_for(read_msg(), timeout=5.0)
            if p_type == ProtoPayloadType.PROTO_OA_SPOT_EVENT:
                fields = parse_protobuf_fields(payload)
                print("\n>>> [PROTO_OA_SPOT_EVENT RECIBIDO!]")
                print("Campos Protobuf crudos detectados:")
                for tag, vals in fields.items():
                    print(f"  Tag {tag}: {vals}")

                # Extracción con Tags Oficiales
                tag2_acc = fields.get(2, [(0, None)])[0][1]
                tag3_sym = fields.get(3, [(0, None)])[0][1]
                tag4_bid_raw = fields.get(4, [(0, None)])[0][1]
                tag5_ask_raw = fields.get(5, [(0, None)])[0][1]
                
                bid_usd = (Decimal(tag4_bid_raw) / Decimal("100000.0")) if tag4_bid_raw else None
                ask_usd = (Decimal(tag5_ask_raw) / Decimal("100000.0")) if tag5_ask_raw else None

                print(f"  - Account ID (Tag 2): {tag2_acc}")
                print(f"  - Symbol ID  (Tag 3): {tag3_sym} (Coincide: {tag3_sym == gold_id})")
                print(f"  - Bid crudo  (Tag 4): {tag4_bid_raw} -> ${bid_usd} USD")
                print(f"  - Ask crudo  (Tag 5): {tag5_ask_raw} -> ${ask_usd} USD")
                break
            elif p_type == ProtoPayloadType.PROTO_OA_SUBSCRIBE_SPOTS_RES:
                print("Confirmacion de suscripcion recibida (PROTO_OA_SUBSCRIBE_SPOTS_RES).")
        except asyncio.TimeoutError:
            print("Esperando tick...")

    writer.close()
    await writer.wait_closed()
    print("\nPrueba finalizada.")

if __name__ == "__main__":
    asyncio.run(test_live_gold_spot())
