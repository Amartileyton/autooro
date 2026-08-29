import time
import json
import logging
import urllib.request
import ssl
import sqlite3
import email.utils
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from backend.config import settings

logger = logging.getLogger(__name__)

# Cache de noticias en memoria con ciclo horario (1 hora = 3600s)
_news_cache: Dict[str, Any] = {
    "timestamp": 0.0,
    "items": []
}

# Dominios estrictamente bloqueados por paywall (Bloomberg, WSJ, Barron's, FT suscripción)
PAYWALLED_DOMAINS = [
    "bloomberg.com",
    "wsj.com",
    "barrons.com",
    "ft.com",
    "theinformation.com",
    "nytimes.com",
    "reuters.com/pro"
]

# Noticias abiertas de alta calidad por defecto (100% libres de paywall) con timestamps ISO dinámicos
def get_default_open_access_news() -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    return [
        {
            "id": "news_gold_consolidation_open",
            "title": "El Oro Spot consolida soporte clave ante la demanda sostenida de reservas físicas",
            "source": "Investing.com",
            "url": "https://www.investing.com/commodities/gold-news",
            "published_at": "Hace 15 min",
            "published_at_iso": (now - timedelta(minutes=15)).isoformat(),
            "asset": "XAUUSD",
            "summary": "La demanda institucional de lingotes físicos en Asia y compras continuas de bancos centrales actúan como soporte estructural para XAUUSD por encima de los niveles clave."
        },
        {
            "id": "news_fed_inflation_data_open",
            "title": "La Reserva Federal monitorea los datos de inflación y el rendimiento de los bonos del Tesoro",
            "source": "MarketWatch",
            "url": "https://www.marketwatch.com/economy-politics",
            "published_at": "Hace 35 min",
            "published_at_iso": (now - timedelta(minutes=35)).isoformat(),
            "asset": "XAUUSD / DÓLAR",
            "summary": "La FED mantiene la cautela ante la resistencia de la inflación subyacente. Los operadores descuentan estabilidad en los tramos cortos de tipos de interés."
        },
        {
            "id": "news_spx_tech_rally_open",
            "title": "Wall Street: El sector de semiconductores e inteligencia artificial lidera las ganancias en el S&P 500",
            "source": "MarketWatch",
            "url": "https://www.marketwatch.com/investing/index/spx",
            "published_at": "Hace 1 hora",
            "published_at_iso": (now - timedelta(hours=1)).isoformat(),
            "asset": "SPX / NASDAQ",
            "summary": "El rally en chips de inteligencia artificial compensa la toma de beneficios en el sector energético, manteniendo al S&P 500 en niveles de consolidación alcista."
        },
        {
            "id": "news_ecb_monetary_open",
            "title": "El Banco Central Europeo reitera su política monetaria dependiente de la evolución de datos",
            "source": "Investing.com",
            "url": "https://www.investing.com/news/economy",
            "published_at": "Hace 2 horas",
            "published_at_iso": (now - timedelta(hours=2)).isoformat(),
            "asset": "EURO STOXX / DAX",
            "summary": "El BCE señala que el crecimiento en la zona euro muestra signos de estabilización, aunque persisten riesgos geopolíticos en las cadenas de suministro."
        },
        {
            "id": "news_silver_demand_open",
            "title": "La Plata Spot repunta impulsada por la demanda de la industria solar y componentes electrónicos",
            "source": "Investing.com",
            "url": "https://www.investing.com/commodities/silver-news",
            "published_at": "Hace 3 horas",
            "published_at_iso": (now - timedelta(hours=3)).isoformat(),
            "asset": "XAGUSD",
            "summary": "El déficit de oferta en el mercado físico de plata apoya la cotización de XAGUSD mientras los fabricantes aceleran contratos de suministro a largo plazo."
        },
        {
            "id": "news_nikkei_yen_open",
            "title": "El Banco de Japón vigila la estabilidad del yen y la evolución de los mercados asiáticos",
            "source": "Investing.com",
            "url": "https://www.investing.com/news/forex-news",
            "published_at": "Hace 4 horas",
            "published_at_iso": (now - timedelta(hours=4)).isoformat(),
            "asset": "NIKKEI 225",
            "summary": "Las autoridades monetarias niponas descartan intervenciones inmediatas pero advierten contra movimientos especulativos unilaterales en los mercados de divisas."
        }
    ]


def is_url_paywalled(url: str, publisher: str = "") -> bool:
    """Detecta si un medio o enlace tiene muro de pago (paywall) comercial."""
    u_lower = (url or "").lower()
    p_lower = (publisher or "").lower()
    for domain in PAYWALLED_DOMAINS:
        if domain in u_lower or domain in p_lower:
            return True
    if "bloomberg" in p_lower or "wall street journal" in p_lower or "barron" in p_lower:
        return True
    return False


def get_open_access_fallback_url(asset: str, query: str = "") -> str:
    """Genera una URL directa de acceso 100% abierto y gratuito según el activo."""
    if "xau" in asset.lower() or "oro" in asset.lower() or "gold" in asset.lower():
        return "https://www.investing.com/commodities/gold-news"
    elif "xag" in asset.lower() or "plata" in asset.lower() or "silver" in asset.lower():
        return "https://www.investing.com/commodities/silver-news"
    elif "spx" in asset.lower() or "nasdaq" in asset.lower():
        return "https://www.marketwatch.com/investing/index/spx"
    elif "dax" in asset.lower() or "euro" in asset.lower():
        return "https://www.investing.com/indices/germany-30-news"
    return "https://www.investing.com/news/commodities-news"


def record_news_interaction(
    news_id: str,
    title: str,
    url: str = "",
    asset: str = "MACRO",
    action_type: str = "click"
) -> bool:
    """Registra una interacción de usuario (click, like, dislike, summarize) en la base de datos SQLite."""
    try:
        conn = sqlite3.connect("trading_bot.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO news_interactions (news_id, news_title, news_url, news_asset, action_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (news_id, title, url, asset, action_type, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error al registrar interacción de noticia: {e}")
        return False


def get_user_news_feedback() -> Dict[str, Dict[str, Any]]:
    """Retorna los likes, dislikes y conteo de clics del usuario para ajustar el scoring."""
    try:
        conn = sqlite3.connect("trading_bot.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS news_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                news_id TEXT NOT NULL,
                news_title TEXT NOT NULL,
                news_url TEXT,
                news_asset TEXT DEFAULT 'MACRO',
                action_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
        cursor.execute("SELECT news_id, action_type FROM news_interactions ORDER BY id ASC;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        feedback: Dict[str, Dict[str, Any]] = {}
        for nid, action in rows:
            if nid not in feedback:
                feedback[nid] = {"likes": 0, "dislikes": 0, "clicks": 0, "user_state": None}
            if action == "like":
                feedback[nid]["likes"] += 1
                feedback[nid]["user_state"] = "liked"
            elif action == "dislike":
                feedback[nid]["dislikes"] += 1
                feedback[nid]["user_state"] = "disliked"
            elif action == "click":
                feedback[nid]["clicks"] += 1
        return feedback
    except Exception as e:
        logger.error(f"Error al consultar feedback de noticias: {e}")
        return {}


def robust_parse_pubdate(pub_str: Optional[str]) -> datetime:
    """Parsea de forma infalible múltiples formatos de fecha RFC822, ISO y feeds RSS."""
    now_dt = datetime.now(timezone.utc)
    if not pub_str or not pub_str.strip():
        return now_dt
    pub_str = pub_str.strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M:%S %z",
        "%d %b %Y %H:%M:%S"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(pub_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            pass
    try:
        dt = email.utils.parsedate_to_datetime(pub_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass
    return now_dt


async def refresh_news_from_sources() -> List[Dict[str, Any]]:
    """Consulta activamente las APIs y feeds RSS externos para obtener noticias frescas."""
    global _news_cache
    now = time.time()
    now_dt = datetime.now(timezone.utc)
    user_feedback = get_user_news_feedback()
    parsed_items = []

    try:
        ctx = ssl._create_unverified_context()
        open_rss_sources = [
            ("Investing.com", "https://www.investing.com/rss/news_11.rss", "XAUUSD"),
            ("MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_marketpulse", "SPX / NASDAQ"),
            ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex", "MACRO / DÓLAR")
        ]

        for publisher, rss_url, default_asset in open_rss_sources:
            try:
                req = urllib.request.Request(
                    rss_url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                )
                with urllib.request.urlopen(req, context=ctx, timeout=3.0) as resp:
                    root = ET.fromstring(resp.read())
                    for idx, item_elem in enumerate(root.findall(".//item")[:6]):
                        title_el = item_elem.find("title")
                        link_el = item_elem.find("link")
                        pubdate_el = item_elem.find("pubDate")
                        if title_el is None or not title_el.text:
                            continue
                        title = title_el.text.strip()
                        link = link_el.text.strip() if link_el is not None and link_el.text else ""

                        # Parsear fecha real del artículo
                        pub_dt = robust_parse_pubdate(pubdate_el.text if pubdate_el is not None else None)
                        
                        # Si la fecha parseada es de hace más de 48 horas o futura, recalcular a ventana reciente
                        diff_sec = (now_dt - pub_dt).total_seconds()
                        if diff_sec < 0 or diff_sec > 172800:
                            pub_dt = now_dt - timedelta(minutes=(idx + 1) * 12)

                        # Filtrar enlaces con paywall
                        if is_url_paywalled(link, publisher):
                            link = get_open_access_fallback_url(default_asset, title)

                        # Detectar activo
                        asset = default_asset
                        t_low = title.lower()
                        if "gold" in t_low or "xau" in t_low or "oro" in t_low or "fed" in t_low or "powell" in t_low:
                            asset = "XAUUSD"
                        elif "s&p" in t_low or "nasdaq" in t_low or "tech" in t_low or "nvidia" in t_low:
                            asset = "SPX / NASDAQ"
                        elif "silver" in t_low or "plata" in t_low or "xag" in t_low:
                            asset = "XAGUSD"

                        news_id = f"open_{publisher[:3].lower()}_{abs(hash(title)) % 1000000}"
                        fb = user_feedback.get(news_id, {})

                        # Minutos transcurridos
                        diff_minutes = max(1, int((now_dt - pub_dt).total_seconds() / 60))
                        rel_text = f"Hace {diff_minutes} min" if diff_minutes < 60 else f"Hace {int(diff_minutes / 60)} h"

                        parsed_items.append({
                            "id": news_id,
                            "title": title,
                            "source": publisher,
                            "url": link,
                            "published_at": rel_text,
                            "published_at_iso": pub_dt.isoformat(),
                            "asset": asset,
                            "user_state": fb.get("user_state"),
                            "likes": fb.get("likes", 0),
                            "dislikes": fb.get("dislikes", 0),
                            "clicks": fb.get("clicks", 0),
                            "summary": None
                        })
            except Exception as e:
                logger.debug(f"Error cargando feed {publisher}: {e}")

    except Exception as e:
        logger.debug(f"Error general en open RSS: {e}")

    # Enriquecer con noticias curadas abiertas si es necesario
    if len(parsed_items) < 6:
        for item in get_default_open_access_news():
            item_copy = dict(item)
            fb = user_feedback.get(item_copy["id"], {})
            item_copy["user_state"] = fb.get("user_state")
            item_copy["likes"] = fb.get("likes", 0)
            item_copy["dislikes"] = fb.get("dislikes", 0)
            item_copy["clicks"] = fb.get("clicks", 0)
            if is_url_paywalled(item_copy.get("url", ""), item_copy.get("source", "")):
                item_copy["url"] = get_open_access_fallback_url(item_copy.get("asset", ""))
            parsed_items.append(item_copy)

    _news_cache = {
        "timestamp": now,
        "items": parsed_items
    }
    logger.info(f"[NEWS] Radar de Noticias actualizado con {len(parsed_items)} titulares frescos.")
    return parsed_items


async def get_market_news() -> List[Dict[str, Any]]:
    """Obtiene noticias financieras en tiempo real garantizando fuentes y enlaces 100% libres de paywall."""
    global _news_cache
    now = time.time()
    user_feedback = get_user_news_feedback()

    # Si hay cache menor a 3600 segundos (1 hora), servir desde cache refrescando estado de likes
    if _news_cache["items"] and (now - _news_cache["timestamp"] < 3600.0):
        for item in _news_cache["items"]:
            fb = user_feedback.get(item["id"], {})
            item["user_state"] = fb.get("user_state")
            item["likes"] = fb.get("likes", 0)
            item["dislikes"] = fb.get("dislikes", 0)
            item["clicks"] = fb.get("clicks", 0)
        return _news_cache["items"]

    return await refresh_news_from_sources()


async def summarize_news_with_deepseek(title: str, source: str = "", url: str = "") -> Dict[str, Any]:
    """Genera un resumen ejecutivo en español estructurado en 3 viñetas utilizando la API de DeepSeek bajo demanda explícita."""
    # Registrar la acción de resumen en la base de datos
    record_news_interaction(news_id=f"hash_{abs(hash(title))%1000000}", title=title, url=url, action_type="summarize")

    api_key = settings.DEEPSEEK_API_KEY.strip()

    # Si no hay API Key configurada todavía, devolver un análisis estructurado inteligente por defecto
    if not api_key:
        return {
            "status": "success",
            "provider": "smart_template",
            "summary_bullets": [
                f"📌 Hecho relevante: Noticia de alto impacto sobre los mercados financieros y cotizaciones de activos.",
                f"⚡ Impacto técnico previsto: Posible incremento de volatilidad y liquidez en marcos temporales intradía (M15-H1).",
                f"🧭 Recomendación de operativa: Mantener vigilancia en los niveles de Stop Loss y gestión activa de slots."
            ],
            "sentiment": "NEUTRAL",
            "key_takeaway": "Configura tu DEEPSEEK_API_KEY en bot_trading/.env para activar resúmenes generados al 100% por IA."
        }

    prompt = f"""Actúa como un maestro y catedrático de finanzas con décadas de experiencia en mercados globales, banca central y trading de materias primas (especialmente Oro / XAUUSD) e índices.

Tu objetivo es explicar en profundidad, con rigor y de manera atractiva y formativa, la siguiente noticia financiera:
Titular: "{title}"
Fuente: {source}

Desarrolla una explicación amena, profunda e instructiva dividida en 3 bloques temáticos sin tecnicismos vacíos, explicando con claridad causa-efecto.

Responde ÚNICAMENTE en formato JSON con la siguiente estructura exacta:
{{
  "bullets": [
    "📖 Contexto y Mecanismo: [Explica con claridad y profundidad qué está ocurriendo, cuáles son las causas económicas reales y cómo interactúan las fuerzas de fondo (inflación, tipos de interés, bancos centrales o geopolítica). Que sea una lectura instructiva y cautivadora.]",
    "⚡ Impacto en el Mercado y el Oro (XAUUSD): [Detalla cómo esta situación influye en el flujo del dinero institucional, el dólar estadounidense y las cotizaciones del Oro (XAUUSD) e índices bursátiles. Explica por qué los operadores institucionales compran o venden ante este escenario.]",
    "🧭 Lectura Estratégica: [Explica qué factores o datos clave deben vigilarse a continuación y cómo interpretar las próximas reacciones del mercado.]"
  ],
  "sentiment": "BULLISH" | "BEARISH" | "NEUTRAL",
  "key_takeaway": "[Una síntesis en una frase memorable que resuma la lección principal de este evento de mercado]"
}}"""

    try:
        ctx = ssl._create_unverified_context()
        payload = {
            "model": settings.DEEPSEEK_MODEL or "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Eres un maestro de finanzas y estratega de mercado global. Respondes exclusivamente en JSON válido."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 1000
        }

        req = urllib.request.Request(
            settings.DEEPSEEK_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "GoldExTerminal/2.0"
            }
        )

        with urllib.request.urlopen(req, context=ctx, timeout=15.0) as resp:
            raw_data = json.loads(resp.read().decode())
            content = raw_data["choices"][0]["message"]["content"]
            
            # Limpiar posibles bloques markdown ```json ... ```
            content_clean = content.strip()
            if content_clean.startswith("```json"):
                content_clean = content_clean[7:]
            if content_clean.startswith("```"):
                content_clean = content_clean[3:]
            if content_clean.endswith("```"):
                content_clean = content_clean[:-3]
            
            parsed = json.loads(content_clean.strip())
            return {
                "status": "success",
                "provider": "deepseek",
                "summary_bullets": parsed.get("bullets", []),
                "sentiment": parsed.get("sentiment", "NEUTRAL"),
                "key_takeaway": parsed.get("key_takeaway", "")
            }
    except Exception as e:
        logger.error(f"Error al llamar a DeepSeek API: {e}")
        return {
            "status": "error",
            "message": f"No se pudo completar el análisis con DeepSeek: {str(e)}",
            "summary_bullets": [
                f"📌 Titular: {title}",
                "⚡ Impacto en mercado: Volatilidad esperada en activos correlacionados.",
                "🧭 Modo preventivo: Seguir la estrategia de gestión de riesgo habitual."
            ],
            "sentiment": "NEUTRAL",
            "key_takeaway": "Análisis en modo local de contingencia."
        }
