import pytest
from decimal import Decimal
from backend.broker.paper import LocalPaperBroker
from backend.database.models import OrderSide


@pytest.mark.asyncio
async def test_paper_broker_order_lifecycle():
    broker = LocalPaperBroker()
    broker.leverage = Decimal("100.0")
    broker.balance = Decimal("10000.00")
    broker._current_ask = Decimal("2345.20")
    broker._current_bid = Decimal("2345.00")

    # Ejecutar orden BUY de 1.00 lote
    ticket_id = await broker.execute_order(
        symbol="XAUUSD",
        side=OrderSide.BUY,
        lot_size=Decimal("1.00"),
        entry_price=Decimal("2345.20"),
        sl=Decimal("2335.00"),
        tp=Decimal("2360.00")
    )

    assert ticket_id in broker.positions
    pos = broker.positions[ticket_id]
    assert pos.lot_size == Decimal("1.00")
    assert pos.entry_price == Decimal("2345.20")

    # Verificar margen usado
    acc = await broker.get_account_info()
    # Margen = (2345.20 * 1.00 * 100) / 100 = 2345.20 USD
    # Equity = Balance (10000) + PnL Flotante por spread (-20.00 USD) = 9980.00 USD
    # Free Margin = 9980.00 - 2345.20 = 7634.80 USD
    assert acc.margin_used == Decimal("2345.20")
    assert acc.equity == Decimal("9980.00")
    assert acc.free_margin == Decimal("7634.80")

    # Cerrar con beneficio: Precio sube a 2355.20 (+$10.00 x 100 = +$1000.00 USD)
    close_price, pnl = await broker.close_order(ticket_id, close_price=Decimal("2355.20"))
    assert pnl == Decimal("1000.00")
    assert broker.balance == Decimal("11000.00")
    assert ticket_id not in broker.positions
