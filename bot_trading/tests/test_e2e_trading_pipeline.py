import pytest
import asyncio
import time
from decimal import Decimal
from backend.config import settings
from backend.broker.paper import LocalPaperBroker
from backend.broker.base import BrokerTick
from backend.ingesta.parser import parse_signal
from backend.ingesta.schemas import TradingSignalEvent, ModifierSignalEvent, SignalType
from backend.risk.engine import RiskEngine
from backend.risk.state_machine import TradeStateMachine
from backend.database.models import Base, OrderSide, TradeStatus
from backend.database.session import engine, AsyncSessionLocal


@pytest.mark.asyncio
async def test_full_e2e_telegram_signal_to_trade_and_trailing():
    """
    Test E2E integral que valida todo el circuito:
    1. Mensaje de Telegram real entrante.
    2. Parseo y extracción de parámetros.
    3. Asignación de slot y cálculo de lote por el motor de riesgo.
    4. Ejecución en broker.
    5. Evaluación de ticks en vivo: TP1 (+50% caja + BE), TP2 (+25% caja + TP1), TP3 Trailing Runner.
    6. Cierre con PnL acumulado positivo en base de datos.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    broker = LocalPaperBroker()
    risk_engine = RiskEngine(broker=broker)
    state_machine = TradeStateMachine(broker=broker)

    # 1. Simular mensaje real de Telegram de Chartoro FX
    raw_telegram_text = """
❗️SIGNAL ALERT❗️
📊#XAUUSD📊
Direction:📈 #BUY
Entry Point: 4615.00
🏆TP1: 4618.00
🏆TP2: 4625.00
🏆TP3: 4635.00
⛔️ Stop Loss (SL): 4605.00
⚠️ Se recomienda no arriesgar más del 1–2% de tu balance
"""
    parsed_event = parse_signal(raw_telegram_text, message_id=888100, channel_id=-1002763662248)
    assert parsed_event is not None
    assert isinstance(parsed_event, TradingSignalEvent)
    assert parsed_event.side == OrderSide.BUY
    assert parsed_event.entry_price == Decimal("4615.00")
    assert parsed_event.tp_levels == [Decimal("4618.00"), Decimal("4625.00"), Decimal("4635.00")]
    assert parsed_event.sl_price == Decimal("4605.00")

    # 2. Motor de Riesgo evalúa disponibilidad de slots y lot sizing
    can_execute, slot_id, reason = risk_engine.evaluate_signal_for_slot(parsed_event, state_machine.active_slots)
    assert can_execute is True
    assert slot_id == 1

    acc_info = await broker.get_account_info()
    lot_size = await risk_engine.calculate_lot_size(parsed_event.entry_price, acc_info)
    assert lot_size >= Decimal("0.01")

    # 3. Apertura de Trade en el Slot 1
    trade = await state_machine.open_new_trade(
        slot_id=slot_id,
        side=parsed_event.side,
        lot_size=lot_size,
        entry_price=parsed_event.entry_price,
        sl=parsed_event.sl_price,
        tp_levels=parsed_event.tp_levels,
        raw_signal_id=parsed_event.message_id
    )

    assert trade is not None
    assert 1 in state_machine.active_slots
    assert state_machine.active_slots[1].status == TradeStatus.OPEN
    assert state_machine.active_slots[1].current_sl == Decimal("4605.00")

    # 4. Simular Tick de mercado alcanzando TP1 (4618.20 >= 4618.00)
    tick_tp1 = BrokerTick(symbol="XAUUSD", bid=Decimal("4618.20"), ask=Decimal("4618.40"), timestamp=time.time())
    await state_machine.on_market_tick(tick_tp1)

    assert state_machine.active_slots[1].status == TradeStatus.TP1_HIT
    from backend.config import settings
    be_buf = getattr(settings, 'DEFAULT_BE_BUFFER_USD', Decimal("0.80"))
    assert state_machine.active_slots[1].current_sl == (Decimal("4615.00") + be_buf)
    assert state_machine.active_slots[1].realized_cash_pnl > Decimal("0.00")

    # 5. Simular Tick alcanzando TP2 (4625.50 >= 4625.00)
    tick_tp2 = BrokerTick(symbol="XAUUSD", bid=Decimal("4625.50"), ask=Decimal("4625.70"), timestamp=time.time())
    await state_machine.on_market_tick(tick_tp2)

    assert state_machine.active_slots[1].status == TradeStatus.TP2_HIT
    # Stop Loss del Runner debe asegurarse en TP1 (4618.00)
    assert state_machine.active_slots[1].current_sl == Decimal("4618.00")

    # 6. Simular Tick alcanzando TP3 (4635.50 >= 4635.00) ➔ Activación de Infinite Runner
    tick_tp3 = BrokerTick(symbol="XAUUSD", bid=Decimal("4635.50"), ask=Decimal("4635.70"), timestamp=time.time())
    await state_machine.on_market_tick(tick_tp3)

    assert state_machine.active_slots[1].status == TradeStatus.TP3_TRAILING
    assert state_machine.active_slots[1].is_infinite_trailing is True
    assert state_machine.active_slots[1].current_sl == Decimal("4635.00")

    # 7. El oro sigue subiendo a 4645.00 (Nuevo Pico) ➔ Trailing Stop dinámico a 30 pips (4642.00)
    tick_peak = BrokerTick(symbol="XAUUSD", bid=Decimal("4645.00"), ask=Decimal("4645.20"), timestamp=time.time())
    await state_machine.on_market_tick(tick_peak)

    assert state_machine.active_slots[1].peak_price == Decimal("4645.00")
    assert state_machine.active_slots[1].current_sl == Decimal("4642.00")

    # 8. Retroceso del mercado que toca el Trailing Stop (4641.80 <= 4642.00)
    tick_exit = BrokerTick(symbol="XAUUSD", bid=Decimal("4641.80"), ask=Decimal("4642.00"), timestamp=time.time())
    await state_machine.on_market_tick(tick_exit)

    # El slot debe quedar completamente cerrado con beneficio acumulado
    assert 1 not in state_machine.active_slots
    final_acc = await broker.get_account_info()
    assert final_acc.balance > acc_info.balance
