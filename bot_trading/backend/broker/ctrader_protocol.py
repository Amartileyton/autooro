"""
cTrader Open API 2.0 Pure-Python Protobuf Protocol Codec.
Maneja la codificación y decodificación de mensajes Protobuf sobre TLS TCP (puerto 5035)
sin requerir Twisted ni compiladores binarios externos. Compatible al 100% con asyncio.
"""

import struct
import io
from enum import IntEnum
from decimal import Decimal
from typing import Dict, List, Optional, Any, Tuple


class ProtoPayloadType(IntEnum):
    HEARTBEAT_EVENT = 51
    PROTO_OA_APPLICATION_AUTH_REQ = 2100
    PROTO_OA_APPLICATION_AUTH_RES = 2101
    PROTO_OA_ACCOUNT_AUTH_REQ = 2102
    PROTO_OA_ACCOUNT_AUTH_RES = 2103
    PROTO_OA_VERSION_REQ = 2104
    PROTO_OA_VERSION_RES = 2105
    PROTO_OA_NEW_ORDER_REQ = 2106
    PROTO_OA_TRAILING_SL_CHANGED_EVENT = 2107
    PROTO_OA_CANCEL_ORDER_REQ = 2108
    PROTO_OA_AMEND_ORDER_REQ = 2109
    PROTO_OA_AMEND_POSITION_SLTP_REQ = 2110
    PROTO_OA_CLOSE_POSITION_REQ = 2111
    PROTO_OA_ASSET_LIST_REQ = 2112
    PROTO_OA_ASSET_LIST_RES = 2113
    PROTO_OA_SYMBOLS_LIST_REQ = 2114
    PROTO_OA_SYMBOLS_LIST_RES = 2115
    PROTO_OA_SYMBOL_BY_ID_REQ = 2116
    PROTO_OA_SYMBOL_BY_ID_RES = 2117
    PROTO_OA_SYMBOLS_FOR_CONVERSION_REQ = 2118
    PROTO_OA_SYMBOLS_FOR_CONVERSION_RES = 2119
    PROTO_OA_SYMBOL_CHANGED_EVENT = 2120
    PROTO_OA_TRADER_REQ = 2121
    PROTO_OA_TRADER_RES = 2122
    PROTO_OA_TRADER_UPDATE_EVENT = 2123
    PROTO_OA_RECONCILE_REQ = 2124
    PROTO_OA_RECONCILE_RES = 2125
    PROTO_OA_EXECUTION_EVENT = 2126
    PROTO_OA_SUBSCRIBE_SPOTS_REQ = 2127
    PROTO_OA_SUBSCRIBE_SPOTS_RES = 2128
    PROTO_OA_UNSUBSCRIBE_SPOTS_REQ = 2129
    PROTO_OA_UNSUBSCRIBE_SPOTS_RES = 2130
    PROTO_OA_SPOT_EVENT = 2131
    PROTO_OA_ORDER_ERROR_EVENT = 2132
    PROTO_OA_ERROR_RES = 2142
    PROTO_OA_GET_ACCOUNTS_BY_ACCESS_TOKEN_REQ = 2149
    PROTO_OA_GET_ACCOUNTS_BY_ACCESS_TOKEN_RES = 2150


class ProtoOATradeSide(IntEnum):
    BUY = 1
    SELL = 2


class ProtoOAOrderType(IntEnum):
    MARKET = 1
    LIMIT = 2
    STOP = 3
    STOP_LOSS_TAKE_PROFIT = 4
    MARKET_RANGE = 5
    STOP_LIMIT = 6


class ProtoOAExecutionType(IntEnum):
    ORDER_ACCEPTED = 1
    ORDER_FILLED = 2
    ORDER_REJECTED = 3
    ORDER_CANCELLED = 4
    ORDER_EXPIRED = 5
    AMENDED = 6
    ORDER_PARTIALLY_FILLED = 7
    BONUS_DEPOSIT = 8
    BONUS_WITHDRAW = 9


# --------------------------------------------------------------------------
# Primitivas de codificación/decodificación Protobuf (Varint, Wire Types)
# --------------------------------------------------------------------------

WIRE_VARINT = 0
WIRE_64BIT = 1
WIRE_LENGTH_DELIMITED = 2
WIRE_32BIT = 5


def encode_varint(value: int) -> bytes:
    """Codifica un entero sin signo como Varint de 7 bits."""
    if value < 0:
        value = (1 << 64) + value
    buf = bytearray()
    while True:
        towrite = value & 0x7F
        value >>= 7
        if value:
            buf.append(towrite | 0x80)
        else:
            buf.append(towrite)
            break
    return bytes(buf)


def decode_varint(stream: io.BytesIO) -> int:
    """Lee un Varint desde un stream de bytes."""
    res = 0
    shift = 0
    while True:
        b = stream.read(1)
        if not b:
            raise EOFError("Fin de stream inesperado leyendo varint")
        val = b[0]
        res |= (val & 0x7F) << shift
        if not (val & 0x80):
            break
        shift += 7
    if res >= (1 << 63):
        res -= (1 << 64)
    return res


def encode_field(field_num: int, wire_type: int, data: bytes) -> bytes:
    tag = (field_num << 3) | wire_type
    return encode_varint(tag) + data


def encode_int32(field_num: int, value: int) -> bytes:
    return encode_field(field_num, WIRE_VARINT, encode_varint(value))


def encode_int64(field_num: int, value: int) -> bytes:
    return encode_field(field_num, WIRE_VARINT, encode_varint(value))


def encode_uint32(field_num: int, value: int) -> bytes:
    return encode_field(field_num, WIRE_VARINT, encode_varint(value))


def encode_uint64(field_num: int, value: int) -> bytes:
    return encode_field(field_num, WIRE_VARINT, encode_varint(value))


def encode_bool(field_num: int, value: bool) -> bytes:
    return encode_field(field_num, WIRE_VARINT, encode_varint(1 if value else 0))


def encode_string(field_num: int, value: str) -> bytes:
    b = value.encode("utf-8")
    return encode_field(field_num, WIRE_LENGTH_DELIMITED, encode_varint(len(b)) + b)


def encode_bytes(field_num: int, value: bytes) -> bytes:
    return encode_field(field_num, WIRE_LENGTH_DELIMITED, encode_varint(len(value)) + value)


def encode_double(field_num: int, value: float) -> bytes:
    return encode_field(field_num, WIRE_64BIT, struct.pack("<d", float(value)))


def encode_float(field_num: int, value: float) -> bytes:
    return encode_field(field_num, WIRE_32BIT, struct.pack("<f", float(value)))


def parse_protobuf_fields(data: bytes) -> Dict[int, List[Tuple[int, Any]]]:
    """
    Parsea un buffer Protobuf genérico y retorna {field_num: [(wire_type, raw_value)]}.
    """
    stream = io.BytesIO(data)
    fields: Dict[int, List[Tuple[int, Any]]] = {}
    
    while True:
        try:
            tag = decode_varint(stream)
        except EOFError:
            break
        
        field_num = tag >> 3
        wire_type = tag & 0x07
        
        if wire_type == WIRE_VARINT:
            val = decode_varint(stream)
        elif wire_type == WIRE_64BIT:
            raw = stream.read(8)
            val = struct.unpack("<d", raw)[0]
        elif wire_type == WIRE_LENGTH_DELIMITED:
            length = decode_varint(stream)
            val = stream.read(length)
        elif wire_type == WIRE_32BIT:
            raw = stream.read(4)
            val = struct.unpack("<f", raw)[0]
        else:
            raise ValueError(f"Wire type desconocido {wire_type} en campo {field_num}")
            
        if field_num not in fields:
            fields[field_num] = []
        fields[field_num].append((wire_type, val))
        
    return fields


# --------------------------------------------------------------------------
# Wrapper ProtoMessage y Framing de Red (4-byte length prefix)
# --------------------------------------------------------------------------

def encode_proto_message(payload_type: int, payload: bytes = b"", client_msg_id: Optional[str] = None) -> bytes:
    """
    Empaqueta el mensaje en la estructura estándar ProtoMessage y le añade
    el prefijo de 4 bytes big-endian requerido por el puerto 5035 de cTrader.
    ProtoMessage:
      1: payloadType (uint32, required)
      2: payload (bytes, optional)
      3: clientMsgId (string, optional)
    """
    msg_body = bytearray()
    msg_body.extend(encode_uint32(1, payload_type))
    if payload:
        msg_body.extend(encode_bytes(2, payload))
    if client_msg_id:
        msg_body.extend(encode_string(3, client_msg_id))
        
    length_prefix = struct.pack(">I", len(msg_body))
    return length_prefix + bytes(msg_body)


def decode_proto_message(data: bytes) -> Tuple[int, bytes, Optional[str]]:
    """Decodifica un ProtoMessage desempaquetado."""
    fields = parse_protobuf_fields(data)
    payload_type = fields.get(1, [(0, 0)])[0][1]
    payload = fields.get(2, [(2, b"")])[0][1] if 2 in fields else b""
    client_msg_id = None
    if 3 in fields:
        raw_id = fields[3][0][1]
        client_msg_id = raw_id.decode("utf-8") if isinstance(raw_id, bytes) else str(raw_id)
    return payload_type, payload, client_msg_id


# --------------------------------------------------------------------------
# Constructores de Solicitudes (Requests)
# En cTrader Open API cada mensaje contiene payloadType en el campo 1
# --------------------------------------------------------------------------

def build_app_auth_req(client_id: str, client_secret: str) -> bytes:
    """Construye ProtoOAApplicationAuthReq (2100)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_APPLICATION_AUTH_REQ))
    buf.extend(encode_string(2, client_id))
    buf.extend(encode_string(3, client_secret))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_APPLICATION_AUTH_REQ, bytes(buf))


def build_account_auth_req(account_id: int, access_token: str) -> bytes:
    """Construye ProtoOAAccountAuthReq (2102)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_ACCOUNT_AUTH_REQ))
    buf.extend(encode_int64(2, account_id))
    buf.extend(encode_string(3, access_token))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_ACCOUNT_AUTH_REQ, bytes(buf))


def build_get_accounts_by_access_token_req(access_token: str) -> bytes:
    """Construye ProtoOAGetAccountsByAccessTokenReq (2149)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_GET_ACCOUNTS_BY_ACCESS_TOKEN_REQ))
    buf.extend(encode_string(2, access_token))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_GET_ACCOUNTS_BY_ACCESS_TOKEN_REQ, bytes(buf))


def parse_accounts_by_access_token_res(payload: bytes) -> List[Dict[str, Any]]:
    """Parsea ProtoOAGetAccountsByAccessTokenRes (2150)."""
    fields = parse_protobuf_fields(payload)
    accounts = []
    acc_list = fields.get(4, []) or fields.get(3, [])
    for wire_type, raw_acc in acc_list:
        if wire_type == WIRE_LENGTH_DELIMITED:
            acc_fields = parse_protobuf_fields(raw_acc)
            ctid_trader_account_id = acc_fields.get(1, [(0, 0)])[0][1]
            is_live = acc_fields.get(2, [(0, 0)])[0][1] == 1
            trader_login = acc_fields.get(3, [(0, 0)])[0][1]
            raw_broker = acc_fields.get(6, [(2, b"")])[0][1] or acc_fields.get(5, [(2, b"")])[0][1]
            broker_name = raw_broker.decode("utf-8") if isinstance(raw_broker, bytes) else str(raw_broker)
            accounts.append({
                "ctid_trader_account_id": ctid_trader_account_id,
                "is_live": is_live,
                "trader_login": trader_login,
                "broker_title": broker_name
            })
    return accounts


def build_symbols_list_req(account_id: int, include_archived: bool = False) -> bytes:
    """Construye ProtoOASymbolsListReq (2114)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SYMBOLS_LIST_REQ))
    buf.extend(encode_int64(2, account_id))
    buf.extend(encode_bool(3, include_archived))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_SYMBOLS_LIST_REQ, bytes(buf))


def build_symbol_by_id_req(account_id: int, symbol_ids: List[int]) -> bytes:
    """Construye ProtoOASymbolByIdReq (2116)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SYMBOL_BY_ID_REQ))
    buf.extend(encode_int64(2, account_id))
    for s_id in symbol_ids:
        buf.extend(encode_int64(3, s_id))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_SYMBOL_BY_ID_REQ, bytes(buf))


def build_subscribe_spots_req(account_id: int, symbol_ids: List[int]) -> bytes:
    """Construye ProtoOASubscribeSpotsReq (2127)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_SUBSCRIBE_SPOTS_REQ))
    buf.extend(encode_int64(2, account_id))
    for s_id in symbol_ids:
        buf.extend(encode_int64(3, s_id))
    buf.extend(encode_bool(4, True))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_SUBSCRIBE_SPOTS_REQ, bytes(buf))


def build_trader_req(account_id: int) -> bytes:
    """Construye ProtoOATraderReq (2121) para consultar balance y apalancamiento."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_TRADER_REQ))
    buf.extend(encode_int64(2, account_id))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_TRADER_REQ, bytes(buf))


def build_reconcile_req(account_id: int) -> bytes:
    """Construye ProtoOAReconcileReq (2124) para sincronizar posiciones abiertas."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_RECONCILE_REQ))
    buf.extend(encode_int64(2, account_id))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_RECONCILE_REQ, bytes(buf))


def build_new_market_order_req(
    account_id: int,
    symbol_id: int,
    trade_side: ProtoOATradeSide,
    volume: int,
    stop_loss: Optional[float] = None,
    take_profit: Optional[float] = None,
    slippage_in_points: Optional[int] = None,
    comment: str = "",
    label: str = "AUTOORO",
    client_order_id: Optional[str] = None
) -> bytes:
    """Construye ProtoOANewOrderReq (2106) para orden a mercado."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_NEW_ORDER_REQ))
    buf.extend(encode_int64(2, account_id))
    buf.extend(encode_int64(3, symbol_id))
    buf.extend(encode_int32(4, ProtoOAOrderType.MARKET))
    buf.extend(encode_int32(5, int(trade_side)))
    buf.extend(encode_int64(6, volume))
    if stop_loss is not None:
        buf.extend(encode_double(11, float(stop_loss)))
    if take_profit is not None:
        buf.extend(encode_double(12, float(take_profit)))
    if comment:
        buf.extend(encode_string(13, comment))
    if slippage_in_points is not None:
        buf.extend(encode_int32(15, slippage_in_points))
    if label:
        buf.extend(encode_string(16, label))
    if client_order_id:
        buf.extend(encode_string(18, client_order_id))
        
    return encode_proto_message(ProtoPayloadType.PROTO_OA_NEW_ORDER_REQ, bytes(buf), client_msg_id=client_order_id)


def build_amend_position_sltp_req(
    account_id: int,
    position_id: int,
    stop_loss: Optional[float] = None,
    take_profit: Optional[float] = None,
    client_msg_id: Optional[str] = None
) -> bytes:
    """Construye ProtoOAAmendPositionSLTPReq (2110)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_AMEND_POSITION_SLTP_REQ))
    buf.extend(encode_int64(2, account_id))
    buf.extend(encode_int64(3, position_id))
    if stop_loss is not None:
        buf.extend(encode_double(4, float(stop_loss)))
    if take_profit is not None:
        buf.extend(encode_double(5, float(take_profit)))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_AMEND_POSITION_SLTP_REQ, bytes(buf), client_msg_id=client_msg_id)


def build_close_position_req(
    account_id: int,
    position_id: int,
    volume: int,
    client_msg_id: Optional[str] = None
) -> bytes:
    """Construye ProtoOAClosePositionReq (2111)."""
    buf = bytearray()
    buf.extend(encode_uint32(1, ProtoPayloadType.PROTO_OA_CLOSE_POSITION_REQ))
    buf.extend(encode_int64(2, account_id))
    buf.extend(encode_int64(3, position_id))
    buf.extend(encode_int64(4, volume))
    return encode_proto_message(ProtoPayloadType.PROTO_OA_CLOSE_POSITION_REQ, bytes(buf), client_msg_id=client_msg_id)


def build_heartbeat_event() -> bytes:
    """Construye mensaje Heartbeat (51)."""
    return encode_proto_message(ProtoPayloadType.HEARTBEAT_EVENT, b"")


# --------------------------------------------------------------------------
# Parsers de Respuestas y Eventos (Responses & Events)
# --------------------------------------------------------------------------

def parse_symbols_list_res(payload: bytes) -> List[Dict[str, Any]]:
    """Parsea ProtoOASymbolsListRes (2115)."""
    fields = parse_protobuf_fields(payload)
    # Campo 3 es lista repetida de ProtoOALightSymbol
    symbols = []
    sym_list = fields.get(3, []) or fields.get(2, [])
    for wire_type, raw_sym in sym_list:
        if wire_type == WIRE_LENGTH_DELIMITED:
            sym_fields = parse_protobuf_fields(raw_sym)
            symbol_id = sym_fields.get(1, [(0, 0)])[0][1]
            raw_name = sym_fields.get(2, [(2, b"")])[0][1]
            symbol_name = raw_name.decode("utf-8") if isinstance(raw_name, bytes) else str(raw_name)
            enabled = sym_fields.get(3, [(0, 1)])[0][1] == 1
            symbols.append({
                "symbol_id": symbol_id,
                "symbol_name": symbol_name,
                "enabled": enabled
            })
    return symbols


def parse_symbol_by_id_res(payload: bytes) -> List[Dict[str, Any]]:
    """Parsea ProtoOASymbolByIdRes (2117)."""
    fields = parse_protobuf_fields(payload)
    symbols = []
    sym_list = fields.get(3, []) or fields.get(2, [])
    for wire_type, raw_sym in sym_list:
        if wire_type == WIRE_LENGTH_DELIMITED:
            sym_fields = parse_protobuf_fields(raw_sym)
            symbol_id = sym_fields.get(1, [(0, 0)])[0][1]
            digits = sym_fields.get(2, [(0, 2)])[0][1]
            pip_position = sym_fields.get(3, [(0, 2)])[0][1]
            max_volume = sym_fields.get(9, [(0, 10000000)])[0][1]
            min_volume = sym_fields.get(10, [(0, 100)])[0][1]
            step_volume = sym_fields.get(11, [(0, 100)])[0][1]
            symbols.append({
                "symbol_id": symbol_id,
                "digits": digits,
                "pip_position": pip_position,
                "max_volume": max_volume,
                "min_volume": min_volume,
                "step_volume": step_volume
            })
    return symbols


def parse_spot_event(payload: bytes, digits: int = 2) -> Dict[str, Any]:
    """
    Parsea ProtoOASpotEvent (2131).
    2: symbolId (int64)
    3: bid (uint64)
    4: ask (uint64)
    7: timestamp (uint64)
    """
    fields = parse_protobuf_fields(payload)
    symbol_id = fields.get(2, [(0, 0)])[0][1] if 2 in fields else fields.get(1, [(0, 0)])[0][1]
    
    bid_raw = fields.get(3, [(0, None)])[0][1] if 3 in fields else fields.get(2, [(0, None)])[0][1]
    ask_raw = fields.get(4, [(0, None)])[0][1] if 4 in fields else fields.get(3, [(0, None)])[0][1]
    timestamp = fields.get(7, [(0, None)])[0][1] if 7 in fields else fields.get(6, [(0, None)])[0][1]
    
    scale_factor = Decimal(10 ** digits)
    bid_price = (Decimal(bid_raw) / scale_factor) if bid_raw is not None else None
    ask_price = (Decimal(ask_raw) / scale_factor) if ask_raw is not None else None
    
    return {
        "symbol_id": symbol_id,
        "bid": bid_price,
        "ask": ask_price,
        "timestamp": timestamp
    }


def parse_trader_res(payload: bytes) -> Dict[str, Any]:
    """Parsea ProtoOATraderRes (2122)."""
    fields = parse_protobuf_fields(payload)
    raw_trader = fields.get(3, [(2, b"")])[0][1] if 3 in fields else fields.get(2, [(2, b"")])[0][1]
    trader_fields = parse_protobuf_fields(raw_trader) if raw_trader else {}
    
    account_id = trader_fields.get(1, [(0, 0)])[0][1]
    balance_cents = trader_fields.get(2, [(0, 0)])[0][1]
    leverage_cents = trader_fields.get(10, [(0, 10000)])[0][1]
    
    balance = Decimal(balance_cents) / Decimal("100.0")
    leverage = Decimal(leverage_cents) / Decimal("100.0")
    
    return {
        "account_id": account_id,
        "balance": balance,
        "leverage": leverage
    }


def parse_position(raw_pos: bytes) -> Dict[str, Any]:
    """Parsea un sub-mensaje ProtoOAPosition."""
    pos_fields = parse_protobuf_fields(raw_pos)
    pos_id = pos_fields.get(1, [(0, 0)])[0][1]
    
    trade_data = pos_fields.get(2, [(2, b"")])[0][1]
    trade_fields = parse_protobuf_fields(trade_data) if trade_data else {}
    
    symbol_id = trade_fields.get(1, [(0, 0)])[0][1]
    volume = trade_fields.get(2, [(0, 0)])[0][1]
    trade_side = trade_fields.get(3, [(0, 1)])[0][1]
    open_time = trade_fields.get(4, [(0, 0)])[0][1]
    
    entry_price = pos_fields.get(3, [(1, 0.0)])[0][1]
    sl = pos_fields.get(4, [(1, None)])[0][1] if 4 in pos_fields else None
    tp = pos_fields.get(5, [(1, None)])[0][1] if 5 in pos_fields else None
    current_price = pos_fields.get(6, [(1, entry_price)])[0][1]
    pnl = pos_fields.get(8, [(0, 0)])[0][1]
    
    return {
        "position_id": pos_id,
        "symbol_id": symbol_id,
        "volume": volume,
        "trade_side": ProtoOATradeSide.BUY if trade_side == 1 else ProtoOATradeSide.SELL,
        "entry_price": Decimal(str(round(entry_price, 2))),
        "current_price": Decimal(str(round(current_price, 2))),
        "sl": Decimal(str(round(sl, 2))) if sl is not None else None,
        "tp": Decimal(str(round(tp, 2))) if tp is not None else None,
        "pnl": Decimal(pnl) / Decimal("100.0"),
        "open_time": open_time
    }


def parse_reconcile_res(payload: bytes) -> List[Dict[str, Any]]:
    """Parsea ProtoOAReconcileRes (2125)."""
    fields = parse_protobuf_fields(payload)
    positions = []
    pos_list = fields.get(3, []) or fields.get(2, [])
    for wire_type, raw_pos in pos_list:
        if wire_type == WIRE_LENGTH_DELIMITED:
            positions.append(parse_position(raw_pos))
    return positions


def parse_execution_event(payload: bytes) -> Dict[str, Any]:
    """Parsea ProtoOAExecutionEvent (2126)."""
    fields = parse_protobuf_fields(payload)
    exec_type = fields.get(2, [(0, 0)])[0][1] if 2 in fields else fields.get(1, [(0, 0)])[0][1]
    
    pos_data = None
    pos_field = fields.get(3, None) or fields.get(2, None)
    if pos_field:
        raw_pos = pos_field[0][1]
        if isinstance(raw_pos, bytes) and raw_pos:
            pos_data = parse_position(raw_pos)
        
    error_code = None
    err_field = fields.get(7, None) or fields.get(6, None)
    if err_field:
        raw_err = err_field[0][1]
        error_code = raw_err.decode("utf-8") if isinstance(raw_err, bytes) else str(raw_err)
        
    return {
        "execution_type": exec_type,
        "position": pos_data,
        "error_code": error_code
    }


def parse_error_res(payload: bytes) -> Dict[str, Any]:
    """Parsea ProtoOAErrorRes (2142)."""
    fields = parse_protobuf_fields(payload)
    err_code = fields.get(2, [(2, b"UNKNOWN_ERROR")])[0][1]
    if isinstance(err_code, bytes):
        err_code = err_code.decode("utf-8")
    desc = fields.get(3, [(2, b"")])[0][1]
    if isinstance(desc, bytes):
        desc = desc.decode("utf-8")
    return {
        "error_code": err_code,
        "description": desc
    }
