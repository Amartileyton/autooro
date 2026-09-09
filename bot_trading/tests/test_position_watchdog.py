import pytest
import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock, patch

from backend.broker.base import BrokerPosition, OrderSide, BrokerTick
from backend.broker.paper import LocalPaperBroker
from backend.risk.state_machine import TradeStateMachine, ActiveSlotTrade, TradeStatus
from backend.risk.position_watchdog import PositionWatchdog


@pytest.mark.asyncio
async def test_watchdog_restores_missing_sl():
    """Verifica que el Watchdog detecta una posición en cTrader sin SL y le asigna el SL inmediatamente."""
    broker = LocalPaperBroker()
    state_machine = TradeStateMachine(broker=broker)

    # Slot en el bot con SL en 4376.00
    state_machine.active_slots[1] = ActiveSlotTrade(
        slot_id=1,
        ticket_id="286937833",
        db_trade_id=11,
        symbol="XAUUSD",
        side=OrderSide.BUY,
        status=TradeStatus.OPEN,
        lot_size=Decimal("0.03"),
        initial_lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_sl=Decimal("4376.00"),
        initial_sl=Decimal("4376.00"),
        open_time=1.0,
        tp1=Decimal("4390.00"),
        tp2=Decimal("4396.00"),
        tp3=None
    )

    # Posición en cTrader pero con SL=None (desprotegida)
    broker.positions["286937833"] = BrokerPosition(
        ticket_id="286937833",
        symbol="XAUUSD",
        side=OrderSide.BUY,
        lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_price=Decimal("4386.00"),
        sl=None,  # ¡DESPROTEGIDA!
        tp=Decimal("4396.00"),
        unrealized_pnl=Decimal("2.00"),
        open_time=1.0
    )

    broker.modify_order = AsyncMock(return_value=True)

    watchdog = PositionWatchdog(broker=broker, state_machine=state_machine)
    with patch("backend.risk.position_watchdog.dispatch_telegram_alert", new_callable=AsyncMock) as mock_alert:
        await watchdog.audit_positions()

    # Debe haber llamado a modify_order para poner el SL de 4376.00
    broker.modify_order.assert_called_once_with("286937833", new_sl=Decimal("4376.00"))


@pytest.mark.asyncio
async def test_watchdog_cleans_slot_when_broker_closed():
    """Verifica que si cTrader cerró la posición (ej. SL hit en broker), el bot libera el slot inmediatamente."""
    broker = LocalPaperBroker()
    state_machine = TradeStateMachine(broker=broker)

    # Slot activo en bot
    state_machine.active_slots[1] = ActiveSlotTrade(
        slot_id=1,
        ticket_id="286937833",
        db_trade_id=11,
        symbol="XAUUSD",
        side=OrderSide.BUY,
        status=TradeStatus.OPEN,
        lot_size=Decimal("0.03"),
        initial_lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_sl=Decimal("4376.00"),
        initial_sl=Decimal("4376.00"),
        open_time=1.0,
        tp1=Decimal("4390.00"),
        tp2=Decimal("4396.00"),
        tp3=None
    )

    # En el broker NO hay posiciones abiertas (lista vacía)
    broker.positions.clear()

    state_machine._close_slot = AsyncMock()

    watchdog = PositionWatchdog(broker=broker, state_machine=state_machine)
    with patch("backend.risk.position_watchdog.dispatch_telegram_alert", new_callable=AsyncMock):
        await watchdog.audit_positions()

    # Debe haber cerrado el slot huérfano
    state_machine._close_slot.assert_called_once()
    args, kwargs = state_machine._close_slot.call_args
    assert args[0] == 1  # slot_id 1
    assert kwargs.get("reason") == "BROKER_RECONCILE_CLOSED"


@pytest.mark.asyncio
async def test_watchdog_repairs_synthetic_ticket():
    """Verifica que si el bot tenía un ticket CTR-..., el watchdog lo repara al ID numérico del broker."""
    broker = LocalPaperBroker()
    state_machine = TradeStateMachine(broker=broker)

    # Bot tiene CTR-1788931807550
    state_machine.active_slots[1] = ActiveSlotTrade(
        slot_id=1,
        ticket_id="CTR-1788931807550",
        db_trade_id=11,
        symbol="XAUUSD",
        side=OrderSide.BUY,
        status=TradeStatus.OPEN,
        lot_size=Decimal("0.03"),
        initial_lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_sl=Decimal("4376.00"),
        initial_sl=Decimal("4376.00"),
        open_time=1.0,
        tp1=Decimal("4390.00"),
        tp2=Decimal("4396.00"),
        tp3=None
    )

    # Broker tiene 286937833
    broker.positions["286937833"] = BrokerPosition(
        ticket_id="286937833",
        symbol="XAUUSD",
        side=OrderSide.BUY,
        lot_size=Decimal("0.03"),
        entry_price=Decimal("4385.33"),
        current_price=Decimal("4386.00"),
        sl=Decimal("4376.00"),
        tp=Decimal("4396.00"),
        unrealized_pnl=Decimal("2.00"),
        open_time=1.0
    )

    watchdog = PositionWatchdog(broker=broker, state_machine=state_machine)
    await watchdog.audit_positions()

    # El ticket en el slot debe haber sido corregido al real del broker
    assert state_machine.active_slots[1].ticket_id == "286937833"
