import asyncio
import logging
import random
import time
import uuid
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple, Callable, Any
from backend.config import settings
from backend.broker.base import BaseBrokerAdapter, AccountInfo, BrokerTick, BrokerPosition
from backend.database.models import OrderSide

logger = logging.getLogger("trading_bot.paper_broker")


class LocalPaperBroker(BaseBrokerAdapter):
    """
    Simulador local de broker de alta fidelidad para XAUUSD.
    Genera ticks realistas con spread dinámico (10-25 cents),
    mantiene el orderbook en memoria y calcula en tiempo real
    Balance, Equidad, Margen Usado, Margen Libre y PnL Flotante.
    """

    def __init__(self):
        self.balance: Decimal = settings.INITIAL_PAPER_BALANCE
        self.leverage: Decimal = settings.LEVERAGE
        self.contract_size: Decimal = settings.CONTRACT_SIZE
        
        # Precio actual de simulación (sincronizado con mercado real de Oro)
        self._current_mid_price: Decimal = settings.INITIAL_XAUUSD_PRICE
        if self._current_mid_price < Decimal("4000.00"):
            self._current_mid_price = Decimal("4604.83")
        self._current_bid: Decimal = self._current_mid_price - (settings.PAPER_SPREAD_MIN_CENTS / Decimal("2.0"))
        self._current_ask: Decimal = self._current_mid_price + (settings.PAPER_SPREAD_MIN_CENTS / Decimal("2.0"))
        
        # Orderbook de posiciones abiertas: {ticket_id: BrokerPosition}
        self.positions: Dict[str, BrokerPosition] = {}
        
        # Callbacks suscritos al flujo de ticks
        self._tick_callbacks: List[Callable[[BrokerTick], Any]] = []
        
        # Tarea asíncrona del generador de ticks
        self._tick_task: Optional[asyncio.Task] = None
        self._is_running = False

    async def connect(self) -> bool:
        """Inicia el generador de ticks en segundo plano."""
        if not self._is_running:
            self._is_running = True
            self._tick_task = asyncio.create_task(self._tick_generator_loop())
            logger.info(f"LocalPaperBroker conectado. Balance inicial: ${self.balance:.2f} USD. Precio inicial XAUUSD: {self._current_mid_price}")
        return True

    async def disconnect(self) -> None:
        """Detiene el simulador."""
        self._is_running = False
        if self._tick_task:
            self._tick_task.cancel()
            try:
                await self._tick_task
            except asyncio.CancelledError:
                pass
        logger.info("LocalPaperBroker desconectado.")

    async def get_account_info(self) -> AccountInfo:
        """Calcula el estado actual de la cuenta financiera con precisión Decimal."""
        margin_used = Decimal("0.00")
        total_unrealized_pnl = Decimal("0.00")

        for pos in self.positions.values():
            # Margen requerido = (entry_price * lot_size * contract_size) / leverage
            pos_margin = (pos.entry_price * pos.lot_size * self.contract_size) / self.leverage
            margin_used += pos_margin

            # Recalcular PnL flotante
            if pos.side == OrderSide.BUY:
                pos.unrealized_pnl = (self._current_bid - pos.entry_price) * pos.lot_size * self.contract_size
            else:
                pos.unrealized_pnl = (pos.entry_price - self._current_ask) * pos.lot_size * self.contract_size
            
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
        """Retorna el último tick bid/ask."""
        return BrokerTick(
            symbol=symbol,
            bid=self._current_bid.quantize(Decimal("0.01")),
            ask=self._current_ask.quantize(Decimal("0.01")),
            timestamp=time.time()
        )

    async def subscribe_ticks(self, symbol: str, callback: Callable[[BrokerTick], Any]) -> None:
        """Registra un callback que recibirá cada nuevo tick emitido."""
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
        """Ejecuta una orden instantánea en memoria."""
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        
        # En ejecución a mercado, usar entry_price provisto o cotización actual
        if entry_price and entry_price > Decimal("0.00"):
            exec_price = entry_price
        else:
            exec_price = self._current_ask if side == OrderSide.BUY else self._current_bid

        position = BrokerPosition(
            ticket_id=ticket_id,
            symbol=symbol,
            side=side,
            lot_size=lot_size,
            entry_price=exec_price.quantize(Decimal("0.01")),
            current_price=exec_price.quantize(Decimal("0.01")),
            sl=sl.quantize(Decimal("0.01")) if sl else None,
            tp=tp.quantize(Decimal("0.01")) if tp else None,
            unrealized_pnl=Decimal("0.00"),
            open_time=time.time()
        )

        self.positions[ticket_id] = position
        logger.info(f"[PAPER BROKER] Orden Ejecutada: {ticket_id} | {side.value} {lot_size} lotes @ {exec_price:.2f} | SL: {sl} | TP: {tp}")
        return ticket_id

    async def modify_order(
        self,
        ticket_id: str,
        new_sl: Optional[Decimal] = None,
        new_tp: Optional[Decimal] = None
    ) -> bool:
        """Modifica SL/TP en memoria con latencia sub-milisegundo."""
        if ticket_id not in self.positions:
            logger.warning(f"[PAPER BROKER] Intento de modificar orden inexistente {ticket_id}")
            return False

        pos = self.positions[ticket_id]
        if new_sl is not None:
            pos.sl = new_sl.quantize(Decimal("0.01"))
        if new_tp is not None:
            pos.tp = new_tp.quantize(Decimal("0.01"))

        logger.info(f"[PAPER BROKER] Orden Modificada {ticket_id}: Nuevo SL={pos.sl}, Nuevo TP={pos.tp}")
        return True

    async def close_order(
        self,
        ticket_id: str,
        close_price: Optional[Decimal] = None,
        reason: str = "MANUAL_CLOSE"
    ) -> Tuple[Decimal, Decimal]:
        """Cierra la posición, liquida el PnL y actualiza el balance."""
        if ticket_id not in self.positions:
            logger.warning(f"[PAPER BROKER] Posición {ticket_id} no encontrada para cerrar.")
            return Decimal("0.00"), Decimal("0.00")

        pos = self.positions.pop(ticket_id)
        
        if close_price is None:
            close_price = self._current_bid if pos.side == OrderSide.BUY else self._current_ask

        # Calcular PnL realizado
        if pos.side == OrderSide.BUY:
            realized_pnl = (close_price - pos.entry_price) * pos.lot_size * self.contract_size
        else:
            realized_pnl = (pos.entry_price - close_price) * pos.lot_size * self.contract_size

        realized_pnl = realized_pnl.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.balance += realized_pnl

        logger.info(f"[PAPER BROKER] Posición Cerrada: {ticket_id} @ {close_price:.2f} | PnL: ${realized_pnl:+.2f} USD | Motivo: {reason} | Nuevo Balance: ${self.balance:.2f} USD")
        return close_price, realized_pnl

    async def close_partial_order(
        self,
        ticket_id: str,
        lot_size: Decimal,
        close_price: Optional[Decimal] = None
    ) -> Tuple[Decimal, Decimal]:
        """Cierra parcialmente una posición reduciendo su volumen y liquida el PnL parcial al balance."""
        if ticket_id not in self.positions:
            logger.warning(f"[PAPER BROKER] Posición {ticket_id} no encontrada para cierre parcial.")
            return Decimal("0.00"), Decimal("0.00")

        pos = self.positions[ticket_id]
        if close_price is None:
            close_price = self._current_bid if pos.side == OrderSide.BUY else self._current_ask

        # Si el lote a cerrar es mayor o igual al restante, cerrar completa
        if lot_size >= pos.lot_size:
            return await self.close_order(ticket_id, close_price=close_price, reason="FULL_PARTIAL_CLOSE")

        # Calcular PnL de la porción cerrada
        if pos.side == OrderSide.BUY:
            partial_pnl = (close_price - pos.entry_price) * lot_size * self.contract_size
        else:
            partial_pnl = (pos.entry_price - close_price) * lot_size * self.contract_size

        partial_pnl = partial_pnl.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.balance += partial_pnl
        pos.lot_size = (pos.lot_size - lot_size).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        logger.info(f"[PAPER BROKER] Cierre Parcial: {ticket_id} | Cerrados {lot_size}L @ {close_price:.2f} | PnL Parcial Cobrado: +${partial_pnl:.2f} USD | Lote Restante: {pos.lot_size}L | Nuevo Balance: ${self.balance:.2f} USD")
        return close_price, partial_pnl

    async def get_open_positions(self) -> List[BrokerPosition]:
        """Retorna lista de posiciones vivas."""
        return list(self.positions.values())

    async def _tick_generator_loop(self):
        """
        Bucle de generación de ticks en tiempo real para XAUUSD spot.
        """
        while self._is_running:
            try:
                # Micro-fluctuación sub-segundo (+-0.05)
                micro_delta = Decimal(str(round(random.uniform(-0.05, 0.05), 2)))
                mid = self._current_mid_price + micro_delta

                # Spread aleatorio entre 0.10 y 0.20 USD
                spread_cents = random.uniform(
                    float(settings.PAPER_SPREAD_MIN_CENTS),
                    float(settings.PAPER_SPREAD_MAX_CENTS)
                )
                half_spread = Decimal(str(round(spread_cents / 2.0, 2)))

                self._current_bid = (mid - half_spread).quantize(Decimal("0.01"))
                self._current_ask = (mid + half_spread).quantize(Decimal("0.01"))

                tick = BrokerTick(
                    symbol="XAUUSD",
                    bid=self._current_bid,
                    ask=self._current_ask,
                    timestamp=time.time()
                )

                # Actualizar PnL de posiciones abiertas
                for pos in self.positions.values():
                    pos.current_price = self._current_bid if pos.side == OrderSide.BUY else self._current_ask
                    if pos.side == OrderSide.BUY:
                        pos.unrealized_pnl = (self._current_bid - pos.entry_price) * pos.lot_size * self.contract_size
                    else:
                        pos.unrealized_pnl = (pos.entry_price - self._current_ask) * pos.lot_size * self.contract_size

                # Notificar a los suscriptores (State Machine, WebSockets)
                for cb in list(self._tick_callbacks):
                    try:
                        if asyncio.iscoroutinefunction(cb):
                            await cb(tick)
                        else:
                            cb(tick)
                    except Exception as ex:
                        logger.error(f"Error en callback de tick: {ex}")

                # Intervalo de tick (cada 300ms)
                await asyncio.sleep(0.3)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error en tick generator: {e}")
                await asyncio.sleep(1.0)
