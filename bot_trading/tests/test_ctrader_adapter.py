import pytest
import asyncio
from decimal import Decimal
from backend.broker.ctrader_protocol import *
from backend.broker.live_adapter import LiveBrokerAdapter
from backend.broker.base import BrokerPosition
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
    # Simular payload oficial de ProtoOASpotEvent (PayloadType 2131):
    # Tag 2: accountId (48390676), Tag 3: symbolId (41), Tag 4: Bid 445198000 (4451.98), Tag 5: Ask 445218000 (4452.18)
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SPOT_EVENT))
    buf.extend(encode_int64(2, 48390676))  # ctidTraderAccountId
    buf.extend(encode_int64(3, 41))        # symbolId = 41
    buf.extend(encode_int64(4, 445198000)) # bid = 4451.98 * 100,000
    buf.extend(encode_int64(5, 445218000)) # ask = 4452.18 * 100,000
    buf.extend(encode_int64(8, 1724920000000))  # timestamp

    spot = parse_spot_event(bytes(buf), digits=2)
    assert spot["account_id"] == 48390676
    assert spot["symbol_id"] == 41
    assert spot["bid"] == Decimal("4451.98")
    assert spot["ask"] == Decimal("4452.18")


def test_protobuf_spot_event_delta_parsing():
    # Simular tick delta de cTrader donde solo cambia Bid
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SPOT_EVENT))
    buf.extend(encode_int64(2, 48390676))
    buf.extend(encode_int64(3, 41))
    buf.extend(encode_int64(4, 445350000))  # bid = 4453.50 * 100,000

    spot = parse_spot_event(bytes(buf), digits=2)
    assert spot["symbol_id"] == 41
    assert spot["bid"] == Decimal("4453.50")
    assert spot["ask"] is None


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


@pytest.mark.asyncio
async def test_live_adapter_partial_close_pnl_and_balance():
    """Verifica que el cierre parcial calcula el PnL positivo real y actualiza el balance."""
    adapter = LiveBrokerAdapter()
    adapter.balance = Decimal("1000.00")
    adapter.contract_size = Decimal("100.0")
    
    # Registrar posición simulada en memoria
    adapter._positions["12345"] = BrokerPosition(
        ticket_id="12345",
        symbol="XAUUSD",
        side=OrderSide.BUY,
        lot_size=Decimal("0.04"),
        entry_price=Decimal("2650.00"),
        current_price=Decimal("2653.00"),
        sl=Decimal("2640.00"),
        tp=Decimal("2660.00"),
        unrealized_pnl=Decimal("12.00"),
        open_time=1.0
    )

    # Cierre parcial de 0.02L a precio 2653.00 (+3.00 USD de ganancia por oz)
    close_px, partial_pnl = await adapter.close_partial_order("12345", lot_size=Decimal("0.02"), close_price=Decimal("2653.00"))

    # PnL parcial = (2653 - 2650) * 0.02 * 100 = 6.00 USD
    assert partial_pnl == Decimal("6.00")
    assert adapter.balance == Decimal("1006.00")
    assert adapter._positions["12345"].lot_size == Decimal("0.02")


@pytest.mark.asyncio
async def test_live_adapter_trader_update_event():
    """Verifica que el evento ProtoOATraderUpdateEvent actualiza el balance en tiempo real."""
    adapter = LiveBrokerAdapter()
    adapter.balance = Decimal("1000.00")

    # Construir ProtoOATraderUpdateEvent con nuevo balance de $1050.00 (105000 centavos)
    trader_buf = bytearray()
    trader_buf.extend(encode_int64(1, 48390676))
    trader_buf.extend(encode_int64(2, 105000))
    trader_buf.extend(encode_int32(10, 3000))

    wrapped_buf = bytearray()
    wrapped_buf.extend(encode_int64(1, 48390676))
    wrapped_buf.extend(encode_bytes(2, bytes(trader_buf)))

    await adapter._handle_incoming_message(
        payload_type=ProtoPayloadType.PROTO_OA_TRADER_UPDATE_EVENT,
        payload=bytes(wrapped_buf),
        client_msg_id=None
    )

    assert adapter.balance == Decimal("1050.00")
    assert adapter.leverage == Decimal("30.00")


def test_protobuf_new_market_order_tags_17_and_18():
    """Verifica que build_new_market_order_req empaqueta clientOrderId tanto en tag 17 como en tag 18."""
    order_msg = build_new_market_order_req(
        account_id=48390676,
        symbol_id=1,
        trade_side=ProtoOATradeSide.BUY,
        volume=300,
        comment="AUTOORO TEST",
        label="AUTOORO",
        client_order_id="ORD-TEST999"
    )
    _, payload, _ = decode_proto_message(order_msg[4:])
    fields = parse_protobuf_fields(payload)
    assert 17 in fields, "Tag 17 (clientOrderId oficial) debe estar presente"
    assert 18 in fields, "Tag 18 (clientOrderId compatibilidad) debe estar presente"
    assert fields[17][0][1].decode("utf-8") == "ORD-TEST999"
    assert fields[18][0][1].decode("utf-8") == "ORD-TEST999"


@pytest.mark.asyncio
async def test_close_order_synthetic_ticket_resolution():
    """Verifica que si se invoca close_order con un ticket sintético (p.ej. CTR-1788931807550),
    el adaptador mapea automáticamente a la posición real viva de cTrader."""
    adapter = LiveBrokerAdapter()
    adapter.balance = Decimal("1000.00")
    adapter.contract_size = Decimal("100.0")

    # Posición viva real en cTrader
    adapter._positions["286937833"] = BrokerPosition(
        ticket_id="286937833",
        symbol="XAUUSD",
        side=OrderSide.BUY,
        lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_price=Decimal("4404.55"),
        sl=Decimal("4376.00"),
        tp=Decimal("4396.00"),
        unrealized_pnl=Decimal("57.66"),
        open_time=1.0
    )

    # Simular _send_raw para responder inmediatamente la confirmación de cTrader
    sent_requests = []
    async def fake_send_raw(req_bytes):
        sent_requests.append(req_bytes)
        if 286937833 in adapter._pending_close_responses:
            fut = adapter._pending_close_responses[286937833]
            if not fut.done():
                fut.set_result((ProtoPayloadType.PROTO_OA_EXECUTION_EVENT, b""))
    adapter._send_raw = fake_send_raw

    close_px, realized_pnl = await adapter.close_order("CTR-1788931807550", close_price=Decimal("4404.55"))
    assert close_px == Decimal("4404.55")
    # PnL = (4404.55 - 4385.33) * 0.03 * 100 = 57.66 USD
    assert realized_pnl == Decimal("57.66")
    assert adapter.balance == Decimal("1057.66")
    assert "286937833" not in adapter._positions

