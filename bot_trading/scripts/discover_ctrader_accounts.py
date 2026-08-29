import asyncio
import ssl
import struct
from backend.config import settings
from backend.broker.ctrader_protocol import (
    ProtoPayloadType,
    encode_proto_message,
    decode_proto_message,
    build_app_auth_req,
    build_get_accounts_by_access_token_req,
    parse_accounts_by_access_token_res
)

async def discover():
    print("=" * 60)
    print("DESCUBRIENDO CUENTAS DISPONIBLES EN SPOTWARE OPEN API")
    print(f"Client ID: {settings.CTRADER_CLIENT_ID[:12]}...")
    print(f"Access Token: {settings.CTRADER_ACCESS_TOKEN[:10]}...")
    print("=" * 60)

    # Intentar tanto en demo como en live
    for host in ["demo.ctraderapi.com", "live.ctraderapi.com"]:
        print(f"\n--- Consultando endpoint: {host}:5035 ---")
        try:
            reader, writer = await asyncio.open_connection(
                host=host,
                port=5035,
                ssl=ssl.create_default_context()
            )

            # 1. App Auth
            app_req = build_app_auth_req(settings.CTRADER_CLIENT_ID, settings.CTRADER_CLIENT_SECRET)
            writer.write(app_req)
            await writer.drain()

            # Leer respuesta de App Auth
            len_b = await reader.readexactly(4)
            msg_len = struct.unpack(">I", len_b)[0]
            body = await reader.readexactly(msg_len)
            ptype, payload, _ = decode_proto_message(body)
            if ptype != ProtoPayloadType.PROTO_OA_APPLICATION_AUTH_RES:
                print(f"[{host}] Respuesta inesperada de App Auth: {ptype}")
                writer.close()
                continue
            print(f"[{host}] App Auth OK.")

            # 2. Consultar cuentas por Access Token
            acc_req = build_get_accounts_by_access_token_req(settings.CTRADER_ACCESS_TOKEN)
            writer.write(acc_req)
            await writer.drain()

            len_b = await reader.readexactly(4)
            msg_len = struct.unpack(">I", len_b)[0]
            body = await reader.readexactly(msg_len)
            ptype, payload, _ = decode_proto_message(body)
            
            if ptype == ProtoPayloadType.PROTO_OA_GET_ACCOUNTS_BY_ACCESS_TOKEN_RES:
                from backend.broker.ctrader_protocol import parse_protobuf_fields
                raw_fields = parse_protobuf_fields(payload)
                print(f"[{host}] Raw fields in response: {raw_fields}")
                accounts = parse_accounts_by_access_token_res(payload)
                print(f"[{host}] Cuentas vinculadas encontradas: {len(accounts)}")
                for acc in accounts:
                    mode = "REAL (LIVE)" if acc['is_live'] else "DEMO (TEST)"
                    print(f"  -> ctidTraderAccountId: {acc['ctid_trader_account_id']} | Login: {acc['trader_login']} | Tipo: {mode} | Broker: {acc['broker_title']}")
            else:
                print(f"[{host}] Tipo de respuesta recibida: {ptype}")

            writer.close()
            await writer.wait_closed()

        except Exception as e:
            print(f"[{host}] Error: {e}")

if __name__ == "__main__":
    asyncio.run(discover())
