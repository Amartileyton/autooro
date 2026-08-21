import asyncio
import json
import logging
from decimal import Decimal
from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.broker.base import BrokerTick

logger = logging.getLogger("trading_bot.ws")

router = APIRouter(tags=["WebSockets"])

class ConnectionManager:
    """Administrador de conexiones WebSocket activas."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Cliente WebSocket conectado. Total conectados: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Cliente WebSocket desconectado. Restantes: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Difunde un mensaje JSON a todos los clientes WebSocket conectados."""
        if not self.active_connections:
            return

        dead_connections = set()
        msg_str = json.dumps(message)

        for connection in list(self.active_connections):
            try:
                await connection.send_text(msg_str)
            except Exception:
                dead_connections.add(connection)

        for dead in dead_connections:
            self.disconnect(dead)


manager = ConnectionManager()


@router.websocket("/ws/live")
async def websocket_live_stream(websocket: WebSocket):
    """
    Endpoint WebSocket de telemetría en tiempo real:
    Transmite ticks de XAUUSD, estado de los 4 slots, balance y eventos de trading.
    """
    await manager.connect(websocket)
    from backend.main import app_state
    broker = app_state["broker"]
    state_machine = app_state["state_machine"]

    try:
        # Enviar snapshot inicial inmediatamente
        from backend.config import settings
        has_token = bool(
            settings.CTRADER_ACCESS_TOKEN 
            and settings.CTRADER_ACCESS_TOKEN.strip() 
            and settings.CTRADER_ACCESS_TOKEN.lower() != "none" 
            and settings.BROKER_TYPE == "CTRADER"
        )
        acc = await broker.get_account_info()
        tick = await broker.get_current_tick("XAUUSD")
        
        init_payload = {
            "type": "INITIAL_SNAPSHOT",
            "has_ctrader_token": has_token,
            "xauusd_spot": {
                "bid": float(tick.bid),
                "ask": float(tick.ask),
                "timestamp": tick.timestamp
            },
            "account": {
                "balance": float(acc.balance) if has_token else None,
                "equity": float(acc.equity) if has_token else None,
                "margin_used": float(acc.margin_used) if has_token else None,
                "free_margin": float(acc.free_margin) if has_token else None
            },
            "slots": [
                {
                    "slot_id": sid,
                    "is_active": sid in state_machine.active_slots,
                    "trade": {
                        "ticket_id": state_machine.active_slots[sid].ticket_id,
                        "side": state_machine.active_slots[sid].side.value,
                        "lot_size": float(state_machine.active_slots[sid].lot_size),
                        "entry_price": float(state_machine.active_slots[sid].entry_price),
                        "current_sl": float(state_machine.active_slots[sid].current_sl),
                        "tp1": float(state_machine.active_slots[sid].tp1),
                        "tp2": float(state_machine.active_slots[sid].tp2) if state_machine.active_slots[sid].tp2 else None,
                        "tp3": float(state_machine.active_slots[sid].tp3) if state_machine.active_slots[sid].tp3 else None,
                        "current_pnl": float(state_machine.active_slots[sid].current_pnl),
                        "status": state_machine.active_slots[sid].status.value
                    } if sid in state_machine.active_slots else None
                }
                for sid in range(1, 5)
            ]
        }
        await websocket.send_text(json.dumps(init_payload))

        # Mantener conexión viva y escuchar mensajes entrantes (ping/pong)
        while True:
            data = await websocket.receive_text()
            # Si el frontend envía 'ping', responder con 'pong'
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        manager.disconnect(websocket)


async def broadcast_tick_update(tick: BrokerTick, account_info, active_slots):
    """Callback invocado en cada tick para retransmitir a los WebSockets."""
    slots_summary = []
    for sid in range(1, 5):
        if sid in active_slots:
            t = active_slots[sid]
            slots_summary.append({
                "slot_id": sid,
                "is_active": True,
                "ticket_id": t.ticket_id,
                "side": t.side.value,
                "lot_size": float(t.lot_size),
                "entry_price": float(t.entry_price),
                "current_sl": float(t.current_sl),
                "tp1": float(t.tp1),
                "tp2": float(t.tp2) if t.tp2 else None,
                "tp3": float(t.tp3) if t.tp3 else None,
                "current_pnl": float(t.current_pnl),
                "status": t.status.value
            })
        else:
            slots_summary.append({
                "slot_id": sid,
                "is_active": False,
                "ticket_id": None,
                "status": "AVAILABLE"
            })

    payload = {
        "type": "TICK_UPDATE",
        "tick": {
            "symbol": tick.symbol,
            "bid": float(tick.bid),
            "ask": float(tick.ask),
            "timestamp": tick.timestamp
        },
        "account": {
            "balance": float(account_info.balance),
            "equity": float(account_info.equity),
            "free_margin": float(account_info.free_margin),
            "margin_used": float(account_info.margin_used)
        },
        "slots": slots_summary
    }

    await manager.broadcast(payload)
