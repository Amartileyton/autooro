import pytest
from decimal import Decimal
from backend.ingesta.parser import parse_signal
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType
)

# 1. Mensajes de Señales Reales de Chartoro FX
def test_parse_chartoro_sell_full_signal():
    text = """
    🚨 SIGNAL ALERT🚨
    📊 #XAUUSD
    Direction: 📈 #SELL
    Entry Point: 4491
    ⛔️ Stop Loss (SL): 4499
    🏆 TP1: 4488
    🏆 TP2: 4483
    🏆 TP3: 4475
    ⚠️ Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.asset == "XAUUSD"
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("4491")
    assert event.sl_price == Decimal("4499")
    assert event.tp_levels == [Decimal("4488"), Decimal("4483"), Decimal("4475")]
    assert event.requires_dynamic_sl is False


def test_parse_chartoro_buy_full_signal():
    text = """
    🚨 SIGNAL ALERT🚨
    📊 #XAUUSD
    Direction: 📉 #BUY
    Entry Point: 4498
    ⛔️ Stop Loss (SL): 4490
    🏆 TP1: 4501
    🏆 TP2: 4506
    🏆 TP3: 4514
    ⚠️ Se recomienda no arriesgar más del 1–2% de tu balance en esta operación — ¡no es asesoramiento financiero!
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.asset == "XAUUSD"
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("4498")
    assert event.sl_price == Decimal("4490")
    assert event.tp_levels == [Decimal("4501"), Decimal("4506"), Decimal("4514")]
    assert event.requires_dynamic_sl is False


def test_parse_chartoro_sell_quick_signal():
    text = """
    XAUUSD SELL NOW 4491
    Set TP1 +30 Pips
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.asset == "XAUUSD"
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("4491")
    assert event.sl_price is None
    assert event.requires_dynamic_sl is True
    # 4491 - (30 * 0.10) = 4488
    assert event.tp_levels == [Decimal("4488.00")]


def test_parse_chartoro_buy_quick_signal():
    text = """
    XAUUSD BUY NOW 4498
    Set TP1 +30 Pips
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.asset == "XAUUSD"
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("4498")
    assert event.sl_price is None
    assert event.requires_dynamic_sl is True
    # 4498 + (30 * 0.10) = 4501
    assert event.tp_levels == [Decimal("4501.00")]


# 2. Modificadores de Chartoro FX
def test_parse_chartoro_move_sl():
    text1 = "Move SL to 4501"
    event1 = parse_signal(text1)
    assert isinstance(event1, ModifierSignalEvent)
    assert event1.signal_type == SignalType.MOVE_SL
    assert event1.target_price == Decimal("4501")

    text2 = "Move SL to 4488"
    event2 = parse_signal(text2)
    assert isinstance(event2, ModifierSignalEvent)
    assert event2.signal_type == SignalType.MOVE_SL
    assert event2.target_price == Decimal("4488")


def test_parse_chartoro_spanish_close_setup():
    text = "**Cerrar el setup de GOLD.**\nEl precio ha vuelto a entrar dentro del canal, invalidando el setup. Cerramos la operación y esperaremos una nueva oportunidad con confirmación."
    event = parse_signal(text, message_id=7618, reply_to_msg_id=7617)
    assert isinstance(event, ModifierSignalEvent)
    assert event.signal_type == SignalType.CLOSE_ORDER
    assert event.reply_to_msg_id == 7617


def test_parse_decimal_prices_signal():
    text = """
    **❗️SIGNAL ALERT❗️**
    📈#XAUUSD📈
    **Direction:📈** **#SELL**
    **Entry Point**: 4383.69
    🏆**TP1**: 4380.69
    🏆**TP2**: 4373.69
    🏆**TP3**: 4363.69
    **⛔️ Stop Loss (SL)**: 4393.69
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.SELL
    assert event.entry_price == Decimal("4383.69")
    assert event.sl_price == Decimal("4393.69")
    assert event.tp_levels == [Decimal("4380.69"), Decimal("4373.69"), Decimal("4363.69")]
    assert event.requires_dynamic_sl is False


def test_parse_comma_decimal_prices_signal():
    # Señal con comas como separador decimal (formato hispano)
    text = """
    🚨 SIGNAL ALERT🚨
    📊 #XAUUSD
    Direction: #BUY
    Entry Point: 4383,69
    ⛔️ Stop Loss (SL): 4375,50
    🏆 TP1: 4386,69
    🏆 TP2: 4392,00
    🏆 TP3: 4400,00
    """
    event = parse_signal(text)
    assert isinstance(event, TradingSignalEvent)
    assert event.side == OrderSide.BUY
    assert event.entry_price == Decimal("4383.69")
    assert event.sl_price == Decimal("4375.50")
    assert event.tp_levels == [Decimal("4386.69"), Decimal("4392.00"), Decimal("4400.00")]
    assert event.requires_dynamic_sl is False


def test_parse_comma_modifier_signal():
    text = "Move SL to 4390,25"
    event = parse_signal(text)
    assert isinstance(event, ModifierSignalEvent)
    assert event.signal_type == SignalType.MOVE_SL
    assert event.target_price == Decimal("4390.25")


# 3. Filtrado del 100% del Spam / Mensajes Informativos de Chartoro FX
@pytest.mark.parametrize("spam_text", [
    "Los miembros VIP ya tienen:\n✅ 4–8 señales premium hoy\n✅ Configuraciones con 80% de efectividad\n✅ Acceso completo al curso\n✅ Soporte 24/7",
    "⚠️ La mitad de la semana se fue.\nLA MITAD DE LAS OPORTUNIDADES TAMBIÉN ‼️\nPero los miembros VIP ya aprovecharon las suyas 📈📈📈",
    "❓ Ya tienes un mentor de trading?",
    "1️⃣ Copiar\n2️⃣ Pegar\n3️⃣ GANAR DINERO 💵💵💵\nDE VERDAD VAS A RECHAZAR ESO??? 🤯🤯",
    "🖼 Muchas gracias ❤️",
    "Copiar las señales dentro del VIP y empezar a ganar de inmediato 💵💵💵\n👑 [HAZ CLIC AQUÍ PARA UNIRTE AHORA]",
    "🔠 SEÑALES VIP GRATIS\n🔠 MATERIAL EDUCATIVO GRATIS\n🔠 MENTORÍA GRATIS\n[RECLAMA AQUÍ]",
    "🖼 TP1 CARGANDO… VAMOS! 🚀",
    "🖼 GANANCIAS TEMPRANAS ASEGURADAS 🔥\n#XAUUSD TP1 HIT, +30 Pips 🏆\nReacción rápida, toma limpia 💰",
    "❌ SL HIT\nDarle más espacio a la operación no ayudó esta vez.\nNo pasa nada — seguiré buscando una nueva configuración clara 🔎",
    "Dónde has visto este nivel de transparencia en un grupo de señales?\nSi encuentras un grupo que afirma tener un 100% de aciertos, mejor sal corriendo... 🏃",
    "[HAZ CLIC AQUÍ PARA UNIRTE AL MÁS REAL DE LOS GRUPOS VIP] 💎"
])
def test_ignore_chartoro_spam_and_info_messages(spam_text):
    event = parse_signal(spam_text)
    assert event is None, f"El mensaje debería haber sido descartado pero retornó: {event}"
