import json
import logging
import httpx
from decimal import Decimal, InvalidOperation
from typing import Optional, Union
from backend.config import settings
from backend.ingesta.schemas import (
    TradingSignalEvent, ModifierSignalEvent, OrderSide, SignalType, ParserType
)

logger = logging.getLogger("trading_bot.ai_fallback")

AI_SYSTEM_PROMPT = """Eres un parser experto de señales de trading para XAUUSD (Gold).
Tu tarea es extraer los datos estructurados del mensaje de Telegram en formato JSON estricto.

Si es una nueva señal de compra o venta:
{
  "type": "NEW_ORDER",
  "asset": "XAUUSD",
  "side": "BUY" o "SELL",
  "entry_price": 2345.50,
  "sl_price": 2335.00 (o null si falta),
  "tp_levels": [2350.00, 2355.00, 2365.00],
  "requires_dynamic_sl": false o true
}

Si es un modificador de orden:
{
  "type": "MOVE_SL" | "MOVE_BE" | "CLOSE_ORDER",
  "target_price": 2345.50 (o null),
  "close_percentage": 100.0 (o null)
}

Si el mensaje NO es una señal de trading válida (es chat o análisis genérico sin precios):
{
  "type": "INVALID"
}

Responde ÚNICAMENTE con el objeto JSON."""


async def parse_with_ai(
    raw_text: str,
    message_id: Optional[int] = None,
    channel_id: Optional[int] = None
) -> Optional[Union[TradingSignalEvent, ModifierSignalEvent]]:
    """
    Parser asíncrono secundario mediante IA para señales en lenguaje natural complejo.
    Se invoca solo si el parser Regex no pudo estructurar el mensaje.
    """
    if not settings.AI_FALLBACK_ENABLED or not settings.AI_API_KEY:
        return None

    try:
        response_json = None
        if settings.AI_PROVIDER.lower() == "gemini":
            response_json = await _call_gemini_api(raw_text)
        else:
            response_json = await _call_openai_api(raw_text)

        if not response_json or response_json.get("type") == "INVALID":
            return None

        msg_type = response_json.get("type")

        if msg_type == "NEW_ORDER":
            side_str = response_json.get("side", "").upper()
            if side_str not in ("BUY", "SELL"):
                return None
            side = OrderSide.BUY if side_str == "BUY" else OrderSide.SELL

            entry_price = Decimal(str(response_json.get("entry_price")))
            sl_val = response_json.get("sl_price")
            sl_price = Decimal(str(sl_val)) if sl_val is not None else None
            tp_list = [Decimal(str(tp)) for tp in response_json.get("tp_levels", [])]

            if not tp_list:
                return None

            return TradingSignalEvent(
                asset="XAUUSD",
                side=side,
                entry_price=entry_price,
                sl_price=sl_price,
                tp_levels=tp_list,
                requires_dynamic_sl=response_json.get("requires_dynamic_sl", sl_price is None),
                parser_type=ParserType.AI_FALLBACK,
                raw_text=raw_text,
                message_id=message_id,
                channel_id=channel_id
            )

        elif msg_type in ("MOVE_SL", "MOVE_BE", "CLOSE_ORDER"):
            sig_type = SignalType[msg_type]
            target_p = None
            if response_json.get("target_price"):
                target_p = Decimal(str(response_json.get("target_price")))
            close_pct = Decimal(str(response_json.get("close_percentage", "100.0")))

            return ModifierSignalEvent(
                signal_type=sig_type,
                target_price=target_p,
                close_percentage=close_pct,
                raw_text=raw_text,
                message_id=message_id,
                channel_id=channel_id
            )

    except Exception as e:
        logger.warning(f"Error en AI Fallback parser: {e}")
        return None

    return None


async def _call_gemini_api(text: str) -> Optional[dict]:
    """Llamada directa de alta velocidad a Google Gemini 2.0 Flash / 1.5 Flash."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.AI_MODEL}:generateContent?key={settings.AI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{AI_SYSTEM_PROMPT}\n\nMensaje a parsear:\n{text}"}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.0
        }
    }
    async with httpx.AsyncClient(timeout=3.0) as client:
        resp = await client.post(url, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            raw_content = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_content)
    return None


async def _call_openai_api(text: str) -> Optional[dict]:
    """Llamada a OpenAI API."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {settings.AI_API_KEY}"}
    payload = {
        "model": settings.AI_MODEL if settings.AI_MODEL.startswith("gpt") else "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": AI_SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.0
    }
    async with httpx.AsyncClient(timeout=3.0) as client:
        resp = await client.post(url, headers=headers, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            raw_content = data["choices"][0]["message"]["content"]
            return json.loads(raw_content)
    return None
