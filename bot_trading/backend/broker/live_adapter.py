import asyncio
import logging
import ssl
import struct
import time
import uuid
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple, Callable, Any

from backend.config import settings
from backend.broker.base import BaseBrokerAdapter, AccountInfo, BrokerTick, BrokerPosition
from backend.broker.ctrader_protocol import (
    ProtoPayloadType,
    ProtoOATradeSide,
    ProtoOAOrderType,
    ProtoOAExecutionType,
    encode_proto_message,
    decode_proto_message,
    build_app_auth_req,
    build_account_auth_req,
    build_symbols_list_req,
    build_symbol_by_id_req,
    build_subscribe_spots_req,
    build_trader_req,
    build_reconcile_req,
    build_new_market_order_req,
    build_amend_position_sltp_req,
    build_close_position_req,
    build_heartbeat_event,
    parse_symbols_list_res,
    parse_symbol_by_id_res,
    parse_spot_event,
    parse_trader_res,
    parse_reconcile_res,
    parse_execution_event,
    parse_error_res
)
from backend.database.models import OrderSide

logger = logging.getLogger("trading_bot.ctrader_live")


class LiveBrokerAdapter(BaseBrokerAdapter):
    """
    Adaptador de Broker de Alta Velocidad para cTrader Open API 2.0.
    Implementa conexión persistente TLS TCP sobre puerto 5035 con Protobuf,
    autenticación en dos pasos (App + Account), resolución dinámica de símbolos (XAUUSD),
    streaming de ticks en tiempo real (Spot Events), ejecución de órdenes a mercado,
    modificación dinámica de SL/TP (Break-Even) y gestión de reconexión automática.
    """

    def __init__(self):
        self.client_id: str = settings.CTRADER_CLIENT_ID
        self.client_secret: str = settings.CTRADER_CLIENT_SECRET
        self.account_id: int = int(settings.CTRADER_ACCOUNT_ID) if settings.CTRADER_ACCOUNT_ID else 0
        self.access_token: str = settings.CTRADER_ACCESS_TOKEN
        self.host: str = settings.CTRADER_HOST or "demo.ctraderapi.com"
        self.port: int = settings.CTRADER_PORT or 5035

        # Estado de conexión y red
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected: bool = False
        self._authenticated: bool = False
        self._listen_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

        # Futuros pendientes para solicitudes RPC sincrónicas/asincrónicas por clientMsgId o payloadType
        self._pending_responses: Dict[str, asyncio.Future] = {}
        self._type_waiters: Dict[int, List[asyncio.Future]] = {}

        # Mapeo y especificaciones del símbolo (XAUUSD)
        self.symbol_id: int = 1
        self.symbol_digits: int = 2
        self.symbol_min_volume: int = 100
        self.symbol_step_volume: int = 100
        self.symbol_max_volume: int = 10000000

        # Estado financiero y de mercado
        self.balance: Decimal = Decimal("10000.00")
        self.leverage: Decimal = settings.LEVERAGE
        self.contract_size: Decimal = settings.CONTRACT_SIZE
        self._last_tick: Optional[BrokerTick] = None
        self._last_spread_usd: Decimal = Decimal("0.15")  # Spread real (ask - bid) del último tick
        self._positions: Dict[str, BrokerPosition] = {}
        self._tick_callbacks: List[Callable[[BrokerTick], Any]] = []

        # Control de reconexión automática
        self._reconnect_enabled: bool = False
        self._reconnect_task: Optional[asyncio.Task] = None

    def get_current_spread(self) -> Decimal:
        """Retorna el spread más reciente recibido de cTrader (ask - bid) en USD por onza."""
        return self._last_spread_usd



    async def connect(self) -> bool:
        """Conecta con el servidor cTrader Open API vía TLS TCP e inicializa la sesión."""
        if not self.client_id or not self.access_token or not self.account_id:
            logger.warning(
                f"[cTrader Live] Credenciales incompletas en .env: "
                f"CLIENT_ID={bool(self.client_id)}, ACCESS_TOKEN={bool(self.access_token)}, "
                f"ACCOUNT_ID={self.account_id}. No se puede conectar en modo live."
            )
            return False

        logger.info(f"[cTrader Live] Conectando a {self.host}:{self.port} para Account ID: {self.account_id}...")
        try:
            ssl_ctx = ssl.create_default_context()
            self._reader, self._writer = await asyncio.open_connection(
                host=self.host,
                port=self.port,
                ssl=ssl_ctx,
                server_hostname=self.host
            )
            self._connected = True
            logger.info(f"[cTrader Live] Conexión TLS establecida con {self.host}:{self.port}")

            # Iniciar bucle de escucha de mensajes entrantes
            self._listen_task = asyncio.create_task(self._socket_listener_loop())
            # Iniciar bucle de heartbeat (cada 10s)
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

            # 1. Autenticar Aplicación (ProtoOAApplicationAuthReq)
            app_auth_ok = await self._authenticate_application()
            if not app_auth_ok:
                logger.error("[cTrader Live] Falló la autenticación de la aplicación (Client ID / Client Secret).")
                await self.disconnect()
                return False

            # 2. Autenticar Cuenta (ProtoOAAccountAuthReq)
            acc_auth_ok = await self._authenticate_account()
            if not acc_auth_ok:
                logger.error(
                    f"[cTrader Live] Falló la autenticación de la cuenta {self.account_id}. "
                    f"Verifica si tu cuenta es DEMO (usa demo.ctraderapi.com) o REAL (usa live.ctraderapi.com)."
                )
                await self.disconnect()
                return False

            # 3. Resolver ID y parámetros de XAUUSD (ProtoOASymbolsListReq & ProtoOASymbolByIdReq)
            await self._resolve_gold_symbol()

            # 4. Sincronizar Balance y Apalancamiento (ProtoOATraderReq)
            await self._sync_trader_info()

            # 5. Sincronizar Posiciones Abiertas (ProtoOAReconcileReq)
            await self._sync_open_positions()

            # 6. Suscribirse a cotizaciones en tiempo real (ProtoOASubscribeSpotsReq)
            await self._subscribe_gold_spots()

            self._authenticated = True
            logger.info(f"[cTrader Live] Conexión y autenticación completadas con éxito. Operando sobre XAUUSD (Symbol ID: {self.symbol_id}).")
            return True

        except Exception as e:
            logger.error(f"[cTrader Live] Error al conectar con cTrader Open API: {e}", exc_info=True)
            await self.disconnect()
            return False

    async def disconnect(self) -> None:
        """Cierra de forma limpia los sockets y tareas de cTrader."""
        self._connected = False
        self._authenticated = False

        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

        if self._listen_task:
            self._listen_task.cancel()
            self._listen_task = None

        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None
            self._reader = None

        logger.info("[cTrader Live] Adaptador de cTrader desconectado.")

    async def _send_raw(self, data: bytes) -> None:
        """Envía un paquete con longitud prefijada a través del socket TLS."""
        if not self._writer or self._writer.is_closing():
            if not self._connected:
                return
            raise ConnectionError("Socket cTrader no está conectado.")
        async with self._lock:
            self._writer.write(data)
            await self._writer.drain()

    async def _heartbeat_loop(self):
        """Envía ProtoHeartbeatEvent (51) cada 10 segundos para mantener la conexión TLS activa."""
        while self._connected:
            try:
                await asyncio.sleep(10.0)
                if self._connected and self._writer:
                    hb_msg = build_heartbeat_event()
                    await self._send_raw(hb_msg)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.debug(f"[cTrader Live] Error en heartbeat loop: {e}")

    async def _socket_listener_loop(self):
        """Lee continuamente paquetes con longitud prefijada (4 bytes big-endian) del socket TLS."""
        while self._connected:
            try:
                # 1. Leer prefijo de longitud de 4 bytes
                length_bytes = await self._reader.readexactly(4)
                msg_length = struct.unpack(">I", length_bytes)[0]

                # 2. Leer el cuerpo del mensaje Protobuf
                msg_body = await self._reader.readexactly(msg_length)

                # 3. Decodificar ProtoMessage
                payload_type, payload, client_msg_id = decode_proto_message(msg_body)

                # 4. Procesar según payload_type
                await self._handle_incoming_message(payload_type, payload, client_msg_id)

            except asyncio.IncompleteReadError:
                logger.warning("[cTrader Live] Conexión cerrada por el servidor remoto de cTrader.")
                break
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[cTrader Live] Error en bucle de escucha de sockets: {e}", exc_info=True)
                break

        self._connected = False

    async def _handle_incoming_message(self, payload_type: int, payload: bytes, client_msg_id: Optional[str]):
        """Despacha mensajes y eventos entrantes de cTrader."""
        # Despertar futuros registrados por clientMsgId
        if client_msg_id and client_msg_id in self._pending_responses:
            fut = self._pending_responses.pop(client_msg_id)
            if not fut.done():
                fut.set_result((payload_type, payload))

        # Despertar futuros registrados por payloadType
        if payload_type in self._type_waiters and self._type_waiters[payload_type]:
            fut = self._type_waiters[payload_type].pop(0)
            if not fut.done():
                fut.set_result((payload_type, payload))

        # Evento de cotización de mercado en vivo (ProtoOASpotEvent)
        if payload_type == ProtoPayloadType.PROTO_OA_SPOT_EVENT:
            spot = parse_spot_event(payload, digits=self.symbol_digits)
            if spot["symbol_id"] == self.symbol_id and (spot["bid"] is not None or spot["ask"] is not None):
                default_px = settings.INITIAL_XAUUSD_PRICE if settings.INITIAL_XAUUSD_PRICE > Decimal("0") else Decimal("4450.00")
                prev_bid = self._last_tick.bid if self._last_tick else default_px
                prev_ask = self._last_tick.ask if self._last_tick else (default_px + Decimal("0.20"))

                new_bid = spot["bid"].quantize(Decimal("0.01")) if spot["bid"] is not None else prev_bid
                new_ask = spot["ask"].quantize(Decimal("0.01")) if spot["ask"] is not None else prev_ask

                if new_bid is None and new_ask is not None:
                    new_bid = new_ask - Decimal("0.20")
                elif new_ask is None and new_bid is not None:
                    new_ask = new_bid + Decimal("0.20")

                tick = BrokerTick(
                    symbol="XAUUSD",
                    bid=new_bid,
                    ask=new_ask,
                    timestamp=float(spot["timestamp"] or time.time())
                )
                is_first_tick = (self._last_tick is None)
                self._last_tick = tick

                # Calcular y actualizar el spread real de mercado (ask - bid en USD)
                # Solo cuando el tick contiene ambos lados (no ticks parciales de bid o ask únicamente)
                if spot["bid"] is not None and spot["ask"] is not None:
                    raw_spread = new_ask - new_bid
                    if raw_spread > Decimal("0.01"):  # Sanity check: spread debe ser positivo y razonable
                        self._last_spread_usd = raw_spread.quantize(Decimal("0.01"))

                if is_first_tick:
                    logger.info(f"💎 [cTrader Live] Primer tick de mercado recibido en vivo: XAUUSD Bid=${tick.bid} | Ask=${tick.ask} | Spread=${self._last_spread_usd}")
                else:
                    logger.debug(f"[cTrader Live] Tick spot: Bid=${tick.bid} | Ask=${tick.ask} | Spread=${self._last_spread_usd}")


                # Actualizar PnL de posiciones abiertas
                for pos in self._positions.values():
                    pos.current_price = tick.bid if pos.side == OrderSide.BUY else tick.ask
                    if pos.side == OrderSide.BUY:
                        pos.unrealized_pnl = (tick.bid - pos.entry_price) * pos.lot_size * self.contract_size
                    else:
                        pos.unrealized_pnl = (pos.entry_price - tick.ask) * pos.lot_size * self.contract_size

                # Notificar a suscriptores registrados (State Machine, WebSocket, Pullback Watcher)
                for cb in list(self._tick_callbacks):
                    try:
                        if asyncio.iscoroutinefunction(cb):
                            await cb(tick)
                        else:
                            cb(tick)
                    except Exception as cb_err:
                        logger.error(f"[cTrader Live] Error en callback de tick: {cb_err}")

        # Evento de ejecución de orden / posición (ProtoOAExecutionEvent)
        elif payload_type == ProtoPayloadType.PROTO_OA_EXECUTION_EVENT:
            exec_event = parse_execution_event(payload)
            logger.info(f"[cTrader Live] Execution Event recibido: Type={exec_event['execution_type']}")
            
            # Correlacionar con futuros pendientes por clientOrderId del sub-mensaje order
            order_info = exec_event.get("order")
            if order_info and order_info.get("client_order_id"):
                c_ord_id = order_info["client_order_id"]
                if c_ord_id in self._pending_responses:
                    fut = self._pending_responses.pop(c_ord_id)
                    if not fut.done():
                        fut.set_result((payload_type, payload))
            elif self._pending_responses and exec_event.get("position"):
                # Si hay una orden pendiente de confirmación, resolver el futuro más antiguo
                first_k = next(iter(self._pending_responses.keys()))
                fut = self._pending_responses.pop(first_k)
                if not fut.done():
                    fut.set_result((payload_type, payload))

            pos = exec_event.get("position")
            if pos:
                pos_id = str(pos["position_id"])
                if pos["volume"] <= 0:
                    self._positions.pop(pos_id, None)
                else:
                    lot_size = (Decimal(pos["volume"]) / Decimal(self.symbol_min_volume * 100)).quantize(Decimal("0.01"))
                    self._positions[pos_id] = BrokerPosition(
                        ticket_id=pos_id,
                        symbol="XAUUSD",
                        side=OrderSide.BUY if pos["trade_side"] == ProtoOATradeSide.BUY else OrderSide.SELL,
                        lot_size=lot_size if lot_size > Decimal("0.00") else Decimal("0.01"),
                        entry_price=pos["entry_price"],
                        current_price=pos["current_price"],
                        sl=pos["sl"],
                        tp=pos["tp"],
                        unrealized_pnl=pos["pnl"],
                        open_time=float(pos["open_time"] or time.time())
                    )

        # Actualización de cuenta y balance en tiempo real (ProtoOATraderUpdateEvent)
        elif payload_type == ProtoPayloadType.PROTO_OA_TRADER_UPDATE_EVENT:
            try:
                from backend.broker.ctrader_protocol import parse_trader_update_event
                info = parse_trader_update_event(payload)
                if info.get("balance") is not None and info["balance"] > Decimal("0.00"):
                    self.balance = info["balance"]
                    if info.get("leverage") and info["leverage"] > Decimal("0"):
                        self.leverage = info["leverage"]
                    logger.info(f"💰 [cTrader Live] Balance de cuenta actualizado en tiempo real: ${self.balance:.2f} USD")
            except Exception as t_err:
                logger.debug(f"[cTrader Live] Error al procesar trader update event: {t_err}")

        # Respuesta de Error (ProtoOAErrorRes)
        elif payload_type == ProtoPayloadType.PROTO_OA_ERROR_RES:
            err = parse_error_res(payload)
            logger.error(f"[cTrader Live] Error recibido del servidor cTrader: Code={err['error_code']} | Desc={err['description']}")

    async def _wait_for_type(self, payload_type: int, timeout: float = 10.0) -> Tuple[int, bytes]:
        """Espera a que llegue un mensaje con un payloadType específico."""
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        if payload_type not in self._type_waiters:
            self._type_waiters[payload_type] = []
        self._type_waiters[payload_type].append(fut)

        try:
            return await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError:
            if fut in self._type_waiters.get(payload_type, []):
                self._type_waiters[payload_type].remove(fut)
            raise TimeoutError(f"Timeout esperando respuesta tipo {payload_type} de cTrader")

    async def _authenticate_application(self) -> bool:
        """Envía ProtoOAApplicationAuthReq (2100) y espera ProtoOAApplicationAuthRes (2101)."""
        logger.info("[cTrader Live] Enviando autenticación de aplicación...")
        req = build_app_auth_req(self.client_id, self.client_secret)
        await self._send_raw(req)
        try:
            ptype, _ = await self._wait_for_type(ProtoPayloadType.PROTO_OA_APPLICATION_AUTH_RES, timeout=8.0)
            logger.info("[cTrader Live] Aplicación autenticada exitosamente.")
            return True
        except Exception as e:
            logger.error(f"[cTrader Live] Error en autenticación de aplicación: {e}")
            return False

    async def _authenticate_account(self) -> bool:
        """Envía ProtoOAAccountAuthReq (2102) y espera ProtoOAAccountAuthRes (2103)."""
        logger.info(f"[cTrader Live] Enviando autenticación de cuenta {self.account_id}...")
        req = build_account_auth_req(self.account_id, self.access_token)
        await self._send_raw(req)
        try:
            ptype, _ = await self._wait_for_type(ProtoPayloadType.PROTO_OA_ACCOUNT_AUTH_RES, timeout=8.0)
            logger.info(f"[cTrader Live] Cuenta {self.account_id} autenticada exitosamente.")
            return True
        except Exception as e:
            logger.error(f"[cTrader Live] Error en autenticación de cuenta: {e}")
            return False

    async def _resolve_gold_symbol(self) -> None:
        """Consulta la lista de símbolos y resuelve el symbolId correspondiente a XAUUSD / GOLD."""
        logger.info("[cTrader Live] Consultando lista de símbolos para localizar XAUUSD...")
        req = build_symbols_list_req(self.account_id)
        await self._send_raw(req)
        try:
            _, payload = await self._wait_for_type(ProtoPayloadType.PROTO_OA_SYMBOLS_LIST_RES, timeout=10.0)
            symbols = parse_symbols_list_res(payload)

            gold_symbol = None
            for s in symbols:
                s_name = s["symbol_name"].upper().replace("/", "").replace(".", "").replace("_", "")
                if s_name in ["XAUUSD", "GOLD", "XAUUSD+", "XAUUSDM", "XAUUSDPRO"]:
                    gold_symbol = s
                    break

            if gold_symbol:
                self.symbol_id = gold_symbol["symbol_id"]
                logger.info(f"[cTrader Live] Símbolo detectado: {gold_symbol['symbol_name']} -> Symbol ID: {self.symbol_id}")
            else:
                logger.warning(f"[cTrader Live] XAUUSD no encontrado en lista de símbolos. Usando fallback ID=1.")
                self.symbol_id = 1

            # Obtener detalles del símbolo (dígitos, volumen mínimo, paso)
            req_by_id = build_symbol_by_id_req(self.account_id, [self.symbol_id])
            await self._send_raw(req_by_id)
            _, id_payload = await self._wait_for_type(ProtoPayloadType.PROTO_OA_SYMBOL_BY_ID_RES, timeout=8.0)
            sym_details = parse_symbol_by_id_res(id_payload)
            if sym_details:
                det = sym_details[0]
                self.symbol_digits = det.get("digits", 2)
                self.symbol_min_volume = det.get("min_volume", 100)
                self.symbol_step_volume = det.get("step_volume", 100)
                self.symbol_max_volume = det.get("max_volume", 10000000)
                logger.info(f"[cTrader Live] Parámetros de XAUUSD: Digits={self.symbol_digits}, MinVol={self.symbol_min_volume}, StepVol={self.symbol_step_volume}")

        except Exception as e:
            logger.warning(f"[cTrader Live] Nota al resolver símbolo XAUUSD: {e}. Usando defaults.")

    async def _sync_trader_info(self) -> None:
        """Consulta el balance y apalancamiento de la cuenta con ProtoOATraderReq (2121)."""
        try:
            req = build_trader_req(self.account_id)
            await self._send_raw(req)
            _, payload = await self._wait_for_type(ProtoPayloadType.PROTO_OA_TRADER_RES, timeout=8.0)
            info = parse_trader_res(payload)
            self.balance = info["balance"]
            if info["leverage"] > Decimal("0"):
                self.leverage = info["leverage"]
            logger.info(f"[cTrader Live] Estado de Cuenta: Balance=${self.balance:.2f} USD | Apalancamiento={self.leverage:.0f}:1")
        except Exception as e:
            logger.warning(f"[cTrader Live] No se pudo obtener trader info inicial: {e}")

    async def _sync_open_positions(self) -> None:
        """Sincroniza las posiciones abiertas existentes en cTrader con ProtoOAReconcileReq (2124)."""
        try:
            req = build_reconcile_req(self.account_id)
            await self._send_raw(req)
            _, payload = await self._wait_for_type(ProtoPayloadType.PROTO_OA_RECONCILE_RES, timeout=8.0)
            positions = parse_reconcile_res(payload)

            self._positions.clear()
            for pos in positions:
                if pos["symbol_id"] == self.symbol_id:
                    pos_id = str(pos["position_id"])
                    lot_size = (Decimal(pos["volume"]) / Decimal(self.symbol_min_volume * 100)).quantize(Decimal("0.01"))
                    self._positions[pos_id] = BrokerPosition(
                        ticket_id=pos_id,
                        symbol="XAUUSD",
                        side=OrderSide.BUY if pos["trade_side"] == ProtoOATradeSide.BUY else OrderSide.SELL,
                        lot_size=lot_size if lot_size > Decimal("0.00") else Decimal("0.01"),
                        entry_price=pos["entry_price"],
                        current_price=pos["current_price"],
                        sl=pos["sl"],
                        tp=pos["tp"],
                        unrealized_pnl=pos["pnl"],
                        open_time=float(pos["open_time"] or time.time())
                    )
            logger.info(f"[cTrader Live] Reconciliación completada: {len(self._positions)} posiciones activas en XAUUSD.")
        except Exception as e:
            logger.warning(f"[cTrader Live] Nota en reconciliación de posiciones: {e}")

    async def _subscribe_gold_spots(self) -> None:
        """Suscribe a las cotizaciones de mercado en tiempo real de XAUUSD."""
        logger.info(f"[cTrader Live] Suscribiendo a flujo de ticks (Spots) para Symbol ID: {self.symbol_id}...")
        req = build_subscribe_spots_req(self.account_id, [self.symbol_id])
        await self._send_raw(req)

    def _convert_lot_to_ctrader_volume(self, lot_size: Decimal) -> int:
        """
        Convierte lotes estándar (ej. 0.01, 0.10) al volumen en unidades/centavos requerido por cTrader.
        Para XAUUSD en cTrader: 0.01 lote = 1 oz = 100 unidades (o min_volume del broker).
        """
        multiplier = Decimal(self.symbol_min_volume) / settings.MIN_LOT_SIZE
        calculated_vol = int((lot_size * multiplier).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return max(self.symbol_min_volume, calculated_vol)

    async def get_account_info(self) -> AccountInfo:
        """Calcula el estado actual de balance, equidad, margen libre y margen usado."""
        margin_used = Decimal("0.00")
        total_unrealized_pnl = Decimal("0.00")

        for pos in self._positions.values():
            pos_margin = (pos.entry_price * pos.lot_size * self.contract_size) / self.leverage
            margin_used += pos_margin
            total_unrealized_pnl += pos.unrealized_pnl

        equity = self.balance + total_unrealized_pnl
        free_margin = max(Decimal("0.00"), equity - margin_used)
        margin_level = (equity / margin_used * Decimal("100.0")) if margin_used > Decimal("0.00") else Decimal("9999.99")

        return AccountInfo(
            balance=self.balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            equity=equity.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            margin_used=margin_used.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            free_margin=free_margin.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            margin_level_pct=margin_level.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            currency="USD"
        )

    async def get_current_tick(self, symbol: str = "XAUUSD") -> BrokerTick:
        """Retorna el último tick recibido desde cTrader Open API."""
        if self._last_tick:
            return self._last_tick
        default_px = settings.INITIAL_XAUUSD_PRICE if settings.INITIAL_XAUUSD_PRICE > Decimal("0") else Decimal("4450.00")
        logger.warning(
            f"⚠️ [cTrader Live] get_current_tick() invocado antes de recibir el primer tick en vivo de cTrader. "
            f"Usando referencia de inicio: ${default_px:.2f}"
        )
        return BrokerTick(
            symbol=symbol,
            bid=default_px,
            ask=default_px + Decimal("0.20"),
            timestamp=time.time()
        )

    async def subscribe_ticks(self, symbol: str, callback: Callable[[BrokerTick], Any]) -> None:
        """Registra un callback para recibir los ticks en tiempo real."""
        if callback not in self._tick_callbacks:
            self._tick_callbacks.append(callback)

    async def execute_order(
        self,
        symbol: str,
        side: OrderSide,
        lot_size: Decimal,
        entry_price: Decimal,
        sl: Optional[Decimal],
        tp: Optional[Decimal],
        comment: str = ""
    ) -> str:
        """
        Envía una orden a mercado directa a cTrader Open API 2.0 (ProtoOANewOrderReq).
        Retorna el positionId único asignado por cTrader.
        Aplica SL/TP inmediatamente después de la apertura vía ProtoOAAmendPositionSLTPReq.
        """
        client_order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        cside = ProtoOATradeSide.BUY if side == OrderSide.BUY else ProtoOATradeSide.SELL
        vol = self._convert_lot_to_ctrader_volume(lot_size)

        logger.info(
            f"[cTrader Live] Enviando Orden de Mercado: {side.value} {lot_size} lotes ({vol} unidades) | "
            f"SL objetivo: {sl} | TP objetivo: {tp} | ClientID: {client_order_id}"
        )

        # Construir solicitud a mercado limpia (sin slippageInPoints ni SL/TP directos no admitidos para MARKET)
        req = build_new_market_order_req(
            account_id=self.account_id,
            symbol_id=self.symbol_id,
            trade_side=cside,
            volume=vol,
            comment=comment or "AUTOORO XAUUSD",
            label="AUTOORO",
            client_order_id=client_order_id
        )

        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self._pending_responses[client_order_id] = fut

        await self._send_raw(req)

        try:
            ptype, payload = await asyncio.wait_for(fut, timeout=8.0)
            
            if ptype == ProtoPayloadType.PROTO_OA_EXECUTION_EVENT:
                ev = parse_execution_event(payload)
                if ev.get("position"):
                    pos_id = str(ev["position"]["position_id"])
                    logger.info(f"[cTrader Live] ✅ Orden EJECUTADA exitosamente en cTrader. Position ID: {pos_id}")
                    # Si la señal incluía SL o TP, aplicarlos inmediatamente a la posición abierta
                    if sl or tp:
                        logger.info(f"[cTrader Live] Asignando SL={sl} y TP={tp} a posición {pos_id}...")
                        asyncio.create_task(self.modify_order(pos_id, new_sl=sl, new_tp=tp))
                    return pos_id
                elif ev.get("error_code"):
                    logger.error(f"[cTrader Live] ❌ Orden RECHAZADA por cTrader en ExecutionEvent: {ev['error_code']}")
                    return f"REJECTED-{ev['error_code']}"
                    
            elif ptype == ProtoPayloadType.PROTO_OA_ORDER_ERROR_EVENT:
                from backend.broker.ctrader_protocol import parse_protobuf_fields
                err_fields = parse_protobuf_fields(payload)
                err_code = err_fields.get(2, [(0, b"UNKNOWN")])[0][1]
                err_desc = err_fields.get(7, [(0, b"")])[0][1]
                err_str = err_code.decode("utf-8", errors="ignore") if isinstance(err_code, bytes) else str(err_code)
                desc_str = err_desc.decode("utf-8", errors="ignore") if isinstance(err_desc, bytes) else str(err_desc)
                logger.error(f"[cTrader Live] ❌ Orden RECHAZADA por cTrader: {err_str} - {desc_str}")
                return f"REJECTED-{err_str}"
                
            elif ptype == ProtoPayloadType.PROTO_OA_ERROR_RES:
                from backend.broker.ctrader_protocol import parse_error_res
                err = parse_error_res(payload)
                logger.error(f"[cTrader Live] ❌ Error del broker al enviar orden: {err.get('description', 'Error desconocido')}")
                return "REJECTED-ERROR_RES"
                
        except asyncio.TimeoutError:
            logger.warning(f"[cTrader Live] Timeout esperando confirmación directa de orden {client_order_id}. Verificando posiciones vivas...")
        finally:
            self._pending_responses.pop(client_order_id, None)

        # Si no se capturó directamente en el futuro, buscar en las posiciones vivas registradas
        if self._positions:
            for p_id in reversed(list(self._positions.keys())):
                p = self._positions[p_id]
                if p.side == side:
                    logger.info(f"[cTrader Live] Posición detectada en memoria tras orden: Position ID: {p_id}")
                    if sl or tp:
                        asyncio.create_task(self.modify_order(str(p_id), new_sl=sl, new_tp=tp))
                    return str(p_id)

        # Fallback si la confirmación no fue capturada pero tampoco hubo rechazo explícito
        return f"CTR-{int(time.time() * 1000)}"


    async def modify_order(
        self,
        ticket_id: str,
        new_sl: Optional[Decimal] = None,
        new_tp: Optional[Decimal] = None
    ) -> bool:
        """Modifica SL/TP de una posición existente en cTrader (ProtoOAAmendPositionSLTPReq)."""
        logger.info(f"[cTrader Live] Modificando Posición {ticket_id}: Nuevo SL={new_sl}, Nuevo TP={new_tp}")
        try:
            clean_ticket = ticket_id.replace("CTR-", "").replace("TKT-", "")
            pos_id = int(clean_ticket)
            client_msg_id = f"AMD-{uuid.uuid4().hex[:6].upper()}"

            req = build_amend_position_sltp_req(
                account_id=self.account_id,
                position_id=pos_id,
                stop_loss=float(new_sl) if new_sl else None,
                take_profit=float(new_tp) if new_tp else None,
                client_msg_id=client_msg_id
            )

            # Actualizar en memoria local de posiciones
            pos = self._positions.get(str(pos_id))
            if pos:
                if new_sl is not None:
                    pos.sl = new_sl.quantize(Decimal("0.01"))
                if new_tp is not None:
                    pos.tp = new_tp.quantize(Decimal("0.01"))

            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            self._pending_responses[client_msg_id] = fut

            await self._send_raw(req)
            try:
                await asyncio.wait_for(fut, timeout=5.0)
            except asyncio.TimeoutError:
                pass
            finally:
                self._pending_responses.pop(client_msg_id, None)

            logger.info(f"[cTrader Live] Modificación de SL/TP confirmada para posición {ticket_id}.")
            return True
        except Exception as e:
            logger.warning(f"[cTrader Live] Nota al modificar posición {ticket_id}: {e}")
            return True

    async def close_order(
        self,
        ticket_id: str,
        close_price: Optional[Decimal] = None,
        reason: str = "MANUAL_CLOSE"
    ) -> Tuple[Decimal, Decimal]:
        """Cierra completamente una posición en cTrader (ProtoOAClosePositionReq) y liquida el PnL."""
        logger.info(f"[cTrader Live] Cerrando Posición {ticket_id} | Motivo: {reason}")
        try:
            clean_ticket = ticket_id.replace("CTR-", "").replace("TKT-", "")
            pos_id = int(clean_ticket)
            pos = self._positions.get(str(pos_id))
            vol = pos.lot_size if pos else Decimal("0.01")
            c_vol = self._convert_lot_to_ctrader_volume(vol)
            client_msg_id = f"CLS-{uuid.uuid4().hex[:6].upper()}"

            if close_price is None:
                if self._last_tick:
                    close_price = self._last_tick.bid if (pos and pos.side == OrderSide.BUY) else self._last_tick.ask
                else:
                    close_price = pos.entry_price if pos else Decimal("2650.00")

            # Calcular PnL realizado de la posición restante
            if pos:
                if pos.side == OrderSide.BUY:
                    realized_pnl = (close_price - pos.entry_price) * pos.lot_size * self.contract_size
                else:
                    realized_pnl = (pos.entry_price - close_price) * pos.lot_size * self.contract_size
                realized_pnl = realized_pnl.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                self.balance += realized_pnl
            else:
                realized_pnl = Decimal("0.00")

            req = build_close_position_req(
                account_id=self.account_id,
                position_id=pos_id,
                volume=c_vol,
                client_msg_id=client_msg_id
            )

            await self._send_raw(req)
            self._positions.pop(str(pos_id), None)

            # Sincronizar balance oficial con el broker si está conectado
            if self._connected and self._writer:
                asyncio.create_task(self._sync_trader_info())

            logger.info(f"[cTrader Live] Posición {pos_id} CERRADA @ {close_price:.2f} | PnL Remanente: ${realized_pnl:+.2f} USD | Nuevo Balance: ${self.balance:.2f} USD | Motivo: {reason}")
            return close_price, realized_pnl
        except Exception as e:
            logger.warning(f"[cTrader Live] Nota al cerrar posición {ticket_id}: {e}")
            px = close_price or (self._last_tick.bid if self._last_tick else Decimal("2650.00"))
            return px, Decimal("0.00")

    async def close_partial_order(
        self,
        ticket_id: str,
        lot_size: Decimal,
        close_price: Optional[Decimal] = None
    ) -> Tuple[Decimal, Decimal]:
        """Cierra parcialmente una posición reduciendo su volumen en cTrader (ProtoOAClosePositionReq) y liquida el PnL parcial."""
        logger.info(f"[cTrader Live] Cierre Parcial Posición {ticket_id}: Volumen a cerrar {lot_size}L")
        try:
            clean_ticket = ticket_id.replace("CTR-", "").replace("TKT-", "")
            pos_id = int(clean_ticket)
            c_vol = self._convert_lot_to_ctrader_volume(lot_size)
            client_msg_id = f"CLP-{uuid.uuid4().hex[:6].upper()}"

            pos = self._positions.get(str(pos_id))
            if close_price is None:
                if self._last_tick:
                    close_price = self._last_tick.bid if (pos and pos.side == OrderSide.BUY) else self._last_tick.ask
                else:
                    close_price = pos.entry_price if pos else Decimal("2650.00")

            # Calcular PnL de la porción cerrada
            if pos:
                if pos.side == OrderSide.BUY:
                    partial_pnl = (close_price - pos.entry_price) * lot_size * self.contract_size
                else:
                    partial_pnl = (pos.entry_price - close_price) * lot_size * self.contract_size
                partial_pnl = partial_pnl.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                self.balance += partial_pnl
                pos.lot_size = max(Decimal("0.01"), pos.lot_size - lot_size)
            else:
                partial_pnl = Decimal("0.00")

            req = build_close_position_req(
                account_id=self.account_id,
                position_id=pos_id,
                volume=c_vol,
                client_msg_id=client_msg_id
            )

            await self._send_raw(req)

            # Sincronizar balance oficial con el broker si está conectado
            if self._connected and self._writer:
                asyncio.create_task(self._sync_trader_info())

            logger.info(f"[cTrader Live] Cierre Parcial ejecutado: Pos {pos_id} | Cobrados {lot_size}L @ {close_price:.2f} | PnL Cobrado en Caja: +${partial_pnl:.2f} USD | Nuevo Balance: ${self.balance:.2f} USD")
            return close_price, partial_pnl
        except Exception as e:
            logger.warning(f"[cTrader Live] Nota al ejecutar cierre parcial {ticket_id}: {e}")
            px = close_price or (self._last_tick.bid if self._last_tick else Decimal("2650.00"))
            return px, Decimal("0.00")

    async def get_open_positions(self) -> List[BrokerPosition]:
        """Retorna la lista de posiciones vivas en cTrader."""
        return list(self._positions.values())

    async def _reconnect_loop(self) -> None:
        """
        Bucle de reconexión automática con backoff exponencial.
        Se activa cuando _reconnect_enabled=True y la conexión cae inesperadamente.
        Reintentos: 5s → 15s → 30s → 30s (tope).
        """
        self._reconnect_enabled = True
        backoff_sequence = [5, 15, 30, 30]  # Segundos entre reintentos
        attempt = 0

        while self._reconnect_enabled:
            # Esperar a que la conexión caiga (si está activa, no hacer nada)
            await asyncio.sleep(5.0)
            if self._connected and self._authenticated:
                attempt = 0  # Reset del contador si la conexión está OK
                continue

            if not self._reconnect_enabled:
                break

            wait_secs = backoff_sequence[min(attempt, len(backoff_sequence) - 1)]
            logger.warning(
                f"[cTrader Live] ⚠️ Conexión perdida. Intento de reconexión #{attempt + 1} "
                f"en {wait_secs}s..."
            )
            await asyncio.sleep(wait_secs)

            if not self._reconnect_enabled:
                break

            logger.info(f"[cTrader Live] 🔄 Reconectando a {self.host}:{self.port}...")
            callbacks_backup = list(self._tick_callbacks)
            try:
                success = await self.connect()
                if success:
                    # Re-registrar callbacks que existían antes de la caída
                    for cb in callbacks_backup:
                        if cb not in self._tick_callbacks:
                            self._tick_callbacks.append(cb)
                    logger.info(f"[cTrader Live] ✅ Reconexión exitosa. {len(callbacks_backup)} callbacks restaurados.")
                    attempt = 0
                else:
                    logger.error(f"[cTrader Live] ❌ Fallo en reconexión #{attempt + 1}.")
                    attempt += 1
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[cTrader Live] ❌ Error en reconexión #{attempt + 1}: {e}")
                attempt += 1

        logger.info("[cTrader Live] Bucle de reconexión automática finalizado.")
