import pytest
import asyncio
from decimal import Decimal
from backend.broker.ctrader_protocol import *
from backend.broker.live_adapter import LiveBrokerAdapter
from backend.database.models import OrderSide


def test_protobuf_app_auth_encoding():
    client_id = "test_client_id"
    client_secret = "test_client_secret"
    msg = build_app_auth_req(client_id, client_secret)
    assert len(msg) > 4
    
    # Decodificar longitud y cuerpo
    payload_type, payload, client_msg_id = decode_proto_message(msg[4:])
    assert payload_type == ProtoPayloadType.PROTO_OA_APPLICATION_AUTH_REQ
    assert client_msg_id is None


def test_protobuf_new_market_order():
    order_msg = build_new_market_order_req(
        account_id=5888542,
        symbol_id=1,
        trade_side=ProtoOATradeSide.BUY,
        volume=1000,
        stop_loss=2650.50,
        take_profit=2670.00,
        slippage_in_points=20,
        comment="TEST ORDER",
        label="AUTOORO",
        client_order_id="ORD-TEST-1"
    )
    payload_type, payload, client_msg_id = decode_proto_message(order_msg[4:])
    assert payload_type == ProtoPayloadType.PROTO_OA_NEW_ORDER_REQ
    assert client_msg_id == "ORD-TEST-1"


def test_protobuf_spot_event_parsing():
    # Simular payload de ProtoOASpotEvent con PayloadType 2131, Symbol ID 1, Bid 265050 (digits=2 -> 2650.50), Ask 265070 (2650.70)
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SPOT_EVENT))
    buf.extend(encode_int64(2, 1))  # symbolId = 1
    buf.extend(encode_int64(3, 265050))  # bid = 265050
    buf.extend(encode_int64(4, 265070))  # ask = 265070
    buf.extend(encode_int64(7, 1724920000000))  # timestamp

    spot = parse_spot_event(bytes(buf), digits=2)
    assert spot["symbol_id"] == 1
    assert spot["bid"] == Decimal("2650.50")
    assert spot["ask"] == Decimal("2650.70")


def test_protobuf_trader_info_parsing():
    # Simular ProtoOATraderRes con Balance 500000 centavos ($5000.00) y apalancamiento 10000 centavos (100:1)
    trader_buf = bytearray()
    trader_buf.extend(encode_int64(1, 5888542))
    trader_buf.extend(encode_int64(2, 500000))  # balance in cents
    trader_buf.extend(encode_int32(10, 10000))  # leverage in cents

    # Wrapper de ProtoOATraderRes (campo 2 es ProtoOATrader embebido como bytes)
    wrapped_buf = bytearray()
    wrapped_buf.extend(encode_int64(1, 5888542))
    wrapped_buf.extend(encode_bytes(2, bytes(trader_buf)))

    trader_info = parse_trader_res(bytes(wrapped_buf))
    assert trader_info["account_id"] == 5888542
    assert trader_info["balance"] == Decimal("5000.00")
    assert trader_info["leverage"] == Decimal("100.00")


def test_live_adapter_volume_conversion():
    adapter = LiveBrokerAdapter()
    adapter.symbol_min_volume = 100
    
    # 0.01 lotes -> 100 unidades (min_volume)
    v1 = adapter._convert_lot_to_ctrader_volume(Decimal("0.01"))
    assert v1 == 100

    # 0.05 lotes -> 500 unidades
    v2 = adapter._convert_lot_to_ctrader_volume(Decimal("0.05"))
    assert v2 == 500

    # 0.10 lotes -> 1000 unidades
    v3 = adapter._convert_lot_to_ctrader_volume(Decimal("0.10"))
    assert v3 == 1000


@pytest.mark.asyncio
async def test_live_adapter_account_info_math():
    adapter = LiveBrokerAdapter()
    adapter.balance = Decimal("10000.00")
    adapter.leverage = Decimal("100.0")
    adapter.contract_size = Decimal("100.0")

    info = await adapter.get_account_info()
    assert info.balance == Decimal("10000.00")
    assert info.equity == Decimal("10000.00")
    assert info.margin_used == Decimal("0.00")
    assert info.free_margin == Decimal("10000.00")
