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


def test_protobuf_new_market_order_tags():
    """Verifica que build_new_market_order_req empaqueta clientOrderId en tag 18 y positionId opcional en tag 17."""
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
    assert 18 in fields, "Tag 18 (clientOrderId oficial) debe estar presente"
    assert fields[18][0][1].decode("utf-8") == "ORD-TEST999"
    assert 17 not in fields, "Tag 17 no debe estar presente si no se especifica position_id"

    # Con position_id explícito
    order_with_pos = build_new_market_order_req(
        account_id=48390676,
        symbol_id=1,
        trade_side=ProtoOATradeSide.BUY,
        volume=300,
        client_order_id="ORD-TEST999",
        position_id=987654
    )
    _, payload_pos, _ = decode_proto_message(order_with_pos[4:])
    fields_pos = parse_protobuf_fields(payload_pos)
    assert 17 in fields_pos
    assert fields_pos[17][0][1] == 987654


def test_proto_execution_type_enum_official_values():
    """Verifica que los valores de ProtoOAExecutionType coinciden 100% con la especificación cTrader Open API 2.0."""
    assert ProtoOAExecutionType.ORDER_ACCEPTED == 2
    assert ProtoOAExecutionType.ORDER_FILLED == 3
    assert ProtoOAExecutionType.ORDER_REPLACED == 4
    assert ProtoOAExecutionType.ORDER_CANCELLED == 5
    assert ProtoOAExecutionType.ORDER_EXPIRED == 6
    assert ProtoOAExecutionType.ORDER_REJECTED == 7
    assert ProtoOAExecutionType.ORDER_CANCEL_REJECTED == 8
    assert ProtoOAExecutionType.SWAP == 9
    assert ProtoOAExecutionType.DEPOSIT_WITHDRAW == 10
    assert ProtoOAExecutionType.ORDER_PARTIALLY_FILLED == 11
    assert ProtoOAExecutionType.BONUS_DEPOSIT_WITHDRAW == 12


def test_parse_deal_execution_price_official_tag_10():
    """Verifica que parse_execution_event extrae el precio de ejecución de Tag 10 (double) y el volumen de Tag 5."""
    # Construir sub-mensaje ProtoOADeal (tag 1: dealId=555, tag 3: posId=777, tag 4: vol=100, tag 5: filledVol=100, tag 10: price=2650.75)
    deal_buf = bytearray()
    deal_buf.extend(encode_int64(1, 555))
    deal_buf.extend(encode_int64(3, 777))
    deal_buf.extend(encode_int64(4, 100))
    deal_buf.extend(encode_int64(5, 100))  # filledVolume
    deal_buf.extend(encode_double(10, 2650.75))  # executionPrice oficial (Tag 10)

    # Envolver en ProtoOAExecutionEvent (tag 3: executionType=3 (FILLED), tag 6: deal)
    event_buf = bytearray()
    event_buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_EXECUTION_EVENT))
    event_buf.extend(encode_int64(2, 48390676))
    event_buf.extend(encode_int32(3, ProtoOAExecutionType.ORDER_FILLED))
    event_buf.extend(encode_bytes(6, bytes(deal_buf)))

    ev = parse_execution_event(bytes(event_buf))
    assert ev["execution_type"] == ProtoOAExecutionType.ORDER_FILLED
    assert ev["deal"] is not None
    assert ev["deal"]["deal_id"] == 555
    assert ev["deal"]["position_id"] == 777
    assert ev["deal"]["volume"] == 100
    assert ev["deal"]["filled_volume"] == 100
    assert ev["deal"]["execution_price"] == Decimal("2650.75")


def test_bidirectional_lot_volume_conversion():
    """Verifica simetría matemática perfecta entre _convert_lot_to_ctrader_volume y _convert_ctrader_volume_to_lot."""
    adapter = LiveBrokerAdapter()
    adapter.symbol_min_volume = 100

    test_lots = [Decimal("0.01"), Decimal("0.02"), Decimal("0.05"), Decimal("0.10"), Decimal("0.50"), Decimal("1.00"), Decimal("2.50")]
    for lot in test_lots:
        vol = adapter._convert_lot_to_ctrader_volume(lot)
        recovered_lot = adapter._convert_ctrader_volume_to_lot(vol)
        assert recovered_lot == lot, f"Fallo en conversión bidireccional para {lot} lotes (vol: {vol})"


def test_spot_event_delta_price_preservation():
    """Verifica que cotizaciones parciales no destruyen el valor previo de Bid o Ask."""
    adapter = LiveBrokerAdapter()
    adapter.symbol_digits = 2

    # Primer spot completo: Bid 2650.00, Ask 2650.20
    buf1 = bytearray()
    buf1.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SPOT_EVENT))
    buf1.extend(encode_int64(2, 48390676))
    buf1.extend(encode_int64(3, 1))  # symbol_id = 1
    buf1.extend(encode_int64(4, 265000000))  # bid = 2650.00
    buf1.extend(encode_int64(5, 265020000))  # ask = 2650.20
    buf1.extend(encode_int64(8, 1724920000000))

    asyncio.run(adapter._handle_incoming_message(ProtoPayloadType.PROTO_OA_SPOT_EVENT, bytes(buf1), None))
    assert adapter._last_tick.bid == Decimal("2650.00")
    assert adapter._last_tick.ask == Decimal("2650.20")
    assert adapter.get_current_spread() == Decimal("0.20")

    # Segundo spot: Solo cambia Ask a 2650.35 (Bid debe preservarse en 2650.00)
    buf2 = bytearray()
    buf2.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SPOT_EVENT))
    buf2.extend(encode_int64(2, 48390676))
    buf2.extend(encode_int64(3, 1))
    buf2.extend(encode_int64(5, 265035000))  # ask = 2650.35

    asyncio.run(adapter._handle_incoming_message(ProtoPayloadType.PROTO_OA_SPOT_EVENT, bytes(buf2), None))
    assert adapter._last_tick.bid == Decimal("2650.00")
    assert adapter._last_tick.ask == Decimal("2650.35")


def test_protobuf_truncated_buffer_guard():
    """Verifica que buffers incompletos en parse_protobuf_fields elevan EOFError de forma segura."""
    # Tag para WIRE_64BIT (wire type 1) en campo 1: tag = (1 << 3) | 1 = 9
    corrupted_data = bytes([9, 1, 2, 3])  # Solo 3 bytes en vez de 8
    with pytest.raises(EOFError):
        parse_protobuf_fields(corrupted_data)


def test_varint_overflow_guard():
    """Verifica que secuencias varint interminables elevan ValueError por desbordamiento."""
    infinite_varint = io.BytesIO(b"\x80" * 15)
    with pytest.raises(ValueError, match="desbordamiento"):
        decode_varint(infinite_varint)


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

