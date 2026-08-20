# 🏆 GOLD-EX: Motor de Trading Autónomo XAUUSD (Telegram ➔ Broker)

Sistema de trading algorítmico y cuantitativo de alta fidelidad para el par **XAUUSD (Oro)**. Ingesta señales en tiempo real mediante MTProto (Telethon), gestiona el capital con una estricta máquina de estados (4 slots concurrentes de 25% de margen libre con trailing SL por hitos), ejecuta órdenes en broker (Simulación Local Paper / cTrader Open API) y expone una interfaz de monitoreo estilo **Obsidian Terminal** (FastAPI + WebSockets + Astro/React) y un bot de control administrativo en Telegram.

---

## 🏛️ Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph INGESTA["1. Ingesta Telegram (MTProto)"]
        TG[Canal Telegram -1002763662248] -->|Telethon MTProto| TGLISTENER[Telegram Ingestion Client]
        TGLISTENER -->|Regex Parser <0.05ms| PARSER[Parser & Normalizador Decimal]
        PARSER -->|Señales & Modificadores| QUEUE[(Asyncio Queue)]
    end

    subgraph RISK["2. Motor de Riesgo & Máquina de Estados"]
        QUEUE --> WORKER[Signal Consumer Worker]
        WORKER --> DEDUP{¿Existe Orden Previa?}
        DEDUP -->|Sí - Alerta Rápida -> Template| ENRICH[Enriquecer SL y TPs de Orden Activa]
        DEDUP -->|No - Señal Nueva| SLOTEVAL[Evaluar Slots Libres 1..4]
        SLOTEVAL --> LOTCALC[Cálculo de Lote 25% Margen Libre]
        LOTCALC --> SM[Trade State Machine]
    end

    subgraph BROKER["3. Capa de Broker & Mercado"]
        SM --> BROKER_LAYER[LocalPaperBroker / cTrader Adapter]
        BROKER_LAYER -->|Ticks en Vivo Brownian Motion| TICKS[Event Loop de Ticks <100ms]
        TICKS -->|Evaluar SL / TP1 / TP2 / TP3| SM
    end

    subgraph PERSIST["4. Persistencia & Auditoría"]
        SM -->|SQLite WAL Mode| DB[(trading_bot.db)]
        TGLISTENER -->|Auditoría 100% Inmutable| DB
    end

    subgraph INTERFACE["5. Interfaces de Usuario"]
        SM -->|WebSockets Live Stream| WS[FastAPI /ws/live]
        WS --> UI[Obsidian Terminal Dashboard Astro/React :4321]
        SM -->|Alertas Push & Control| TGBOT[Telegram Admin Bot :Aiogram]
    end
```

---

## 📊 Estado Actual del Proyecto y Despliegue en la Nube

- **Estado:** 🟢 **EN PRODUCCIÓN (MODO PAPER TRADING 24/7)**
- **Servidor Cloud:** Google Cloud Platform VM (`europe-southwest1` Madrid)
- **Dashboard Web:** `http://34.175.69.118:4321`
- **Backend API:** `http://34.175.69.118:8000/docs`
- **Canal de Señales:** `-1002763662248` (Chartoro FX)
- **Ingesta:** Calibrada con **1.000 mensajes reales** (Julio 2026 – Agosto 2026) con **0% de falsos positivos**.
- **Normalización Decimal:** `sanitize_price_str` inmune a comas españolas (`4383,69`), miles (`4.383,69`) o puntos estándar (`4383.69`).
- **Enriquecimiento de Órdenes:** Deduplica automáticamente las alertas rápidas (`BUY NOW`) con las plantillas formales (`SIGNAL ALERT`).
- **Tests Automatizados:** **36/36 tests superados** en 0.59s (`pytest tests/ -v`).

---

## 🗺️ Hoja de Ruta (Roadmap)

```mermaid
gantt
    title Plan de Operación y Transición a Real
    dateFormat  YYYY-MM-DD
    section Desarrollo & Despliegue
    Arquitectura & Backend           :done, 2026-08-01, 2026-08-15
    Dashboard Obsidian Terminal      :done, 2026-08-16, 2026-08-18
    Calibración 1000 Mensajes Reales :done, 2026-08-19, 2026-08-20
    Despliegue GCP VM (34.175.69.118):done, 2026-08-20, 2026-08-20
    section Operación & Testeo
    Fase Paper Trading (2-4 semanas) :active, 2026-08-21, 2026-09-15
    Auditoría de PnL y Rendimiento   : 2026-09-10, 2026-09-15
    Transición a cTrader Real        : 2026-09-16, 2026-09-30
```

---

## 🛠️ Estructura del Repositorio

```text
bot_trading/
├── backend/
│   ├── config.py              # Pydantic Settings v2 (.env)
│   ├── main.py                # FastAPI app y Lifecycle Manager
│   ├── api/                   # Rutas REST y WebSocket /ws/live
│   ├── broker/                # LocalPaperBroker y LiveBrokerAdapter (cTrader)
│   ├── database/              # SQLAlchemy 2.0 Async, Modelos y Reconciliación post-reboot
│   ├── ingesta/               # Telethon MTProto client, regex parser, normalizador decimal
│   ├── risk/                  # Motor de 4 Slots, cálculo de lotes y Trailing SL
│   └── telegram_admin/        # Bot privado de control móvil (Aiogram 3.x)
├── frontend/                  # Dashboard Obsidian Terminal (Astro 5 + React 19 + Tailwind)
├── scripts/                   # Scripts de auditoría, scraping histórico y tests
├── tests/                     # 36 tests automatizados de integración y unitarios
├── docker-compose.yml         # Orquestación de Backend + Frontend
├── Dockerfile                 # Contenedor de producción
└── TUTORIAL_SETUP.md          # Guía detallada de instalación
```
