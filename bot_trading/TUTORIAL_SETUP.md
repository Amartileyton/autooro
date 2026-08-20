# 📘 GUÍA DE PUESTA EN MARCHA: MOTOR DE TRADING AUTÓNOMO XAUUSD
### (TELEGRAM MTPROTO ➔ RISK ENGINE 4 SLOTS ➔ BROKER ➔ DASHBOARD & BOT ADMIN)

Esta guía paso a paso te explica de forma clara y detallada cómo obtener todas las credenciales necesarias (Telegram API, BotFather, IDs de canales y cuentas de broker), configurar el entorno y poner a funcionar el sistema tanto en **modo local** como en **Docker**.

---

## 📑 ÍNDICE
1. [Paso 1: Obtener credenciales de Telegram API (Telethon MTProto)](#paso-1-obtener-credenciales-de-telegram-api-telethon-mtproto)
2. [Paso 2: Crear el Bot Privado de Administración con @BotFather](#paso-2-crear-el-bot-privado-de-administración-con-botfather)
3. [Paso 3: Obtener tu Telegram User ID y el ID del Canal de Señales](#paso-3-obtener-tu-telegram-user-id-y-el-id-del-canal-de-señales)
4. [Paso 4: Configuración de Broker (Paper Trading vs cTrader Open API)](#paso-4-configuración-de-broker-paper-trading-vs-ctrader-open-api)
5. [Paso 5: Configurar el archivo `.env`](#paso-5-configurar-el-archivo-env)
6. [Paso 6: Ejecución del Sistema](#paso-6-ejecución-del-sistema)
   - [Opción A: Un solo comando con Docker Compose (Recomendado)](#opción-a-un-solo-comando-con-docker-compose-recomendado)
   - [Opción B: Ejecución en Entorno Local (Python + Astro)](#opción-b-ejecución-en-entorno-local-python--astro)
7. [Paso 7: Verificación, Comandos del Bot y Dashboard](#paso-7-verificación-comandos-del-bot-y-dashboard)

---

## PASO 1: Obtener credenciales de Telegram API (Telethon MTProto)
Para que el bot pueda leer las señales de cualquier canal de Telegram (público o privado) en tiempo real con latencia sub-milisegundo, se utiliza el protocolo **MTProto** mediante Telethon.

1. Abre tu navegador e ingresa a: **[https://my.telegram.org](https://my.telegram.org)**.
2. Introduce tu número de teléfono con el código de país (ej. `+34600000000`).
3. Recibirás un código de confirmación dentro de la aplicación de Telegram en tu móvil u ordenador. Introdúcelo.
4. Haz clic en la opción **"API development tools"**.
5. Rellena el formulario:
   - **App title:** `XAUUSD-Trading-Engine` (o el nombre que prefieras).
   - **Short name:** `xauusd_bot` (sin espacios ni caracteres especiales).
   - **Platform:** `Desktop` u `Other`.
6. Haz clic en **"Create application"**.
7. Verás en pantalla dos datos fundamentales:
   - `api_id` (un número, ej: `12345678`) ➔ Este es tu `TG_API_ID`.
   - `api_hash` (una cadena alfanumérica, ej: `abcdef0123456789abcdef0123456789`) ➔ Este es tu `TG_API_HASH`.

> ⚠️ **Nota:** Guarda estos datos de forma privada. La primera vez que arranques Telethon en la consola, te pedirá que introduzcas el código SMS/Telegram una sola vez para generar el archivo de sesión `bot_session.session`. Luego no volverá a pedirlo.

---

## PASO 2: Crear el Bot Privado de Administración con @BotFather
Este bot es tu canal de mando privado para recibir alertas instantáneas (aperturas de slots, trailing SL asegurado en TP1/TP2, cierres con PnL) y ejecutar comandos (`/status`, `/pause`, `/kill`).

1. Abre Telegram y busca al usuario oficial: **`@BotFather`** (verás la insignia de verificación azul).
2. Pulsa en **Iniciar** y envía el comando:
   ```text
   /newbot
   ```
3. Te pedirá un nombre público para el bot (ej: `GoldEx Admin Bot`).
4. Te pedirá un nombre de usuario único que termine en `bot` (ej: `gold_ex_admin_99_bot`).
5. BotFather te responderá con el token de acceso HTTP:
   ```text
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. Copia ese token ➔ Este es tu `TELEGRAM_BOT_TOKEN`.

---

## PASO 3: Obtener tu Telegram User ID y el ID del Canal de Señales

### 3.1 Obtener tu `ADMIN_TELEGRAM_USER_ID` (Seguridad)
Para que nadie más pueda controlar tu bot ni ejecutar el Kill-Switch, restringimos el acceso exclusivamente a tu ID numérico de Telegram.

1. En Telegram, busca el bot: **`@userinfobot`**.
2. Pulsa **Iniciar**.
3. Te devolverá un mensaje como este:
   ```text
   Id: 987654321
   First: Juan
   Lang: es
   ```
4. El número en `Id:` (ej. `987654321`) ➔ Este es tu `ADMIN_TELEGRAM_USER_ID`.

---

### 3.2 Obtener el ID del Canal de Señales (`TARGET_CHANNEL_ID`)
1. **Opción A (Telegram Web):**
   - Entra a [web.telegram.org](https://web.telegram.org) y haz clic sobre el canal VIP de señales.
   - Mira la URL en la barra de direcciones del navegador: `https://web.telegram.org/a/#-1001987654321`.
   - El ID completo es el número que empieza por `-100...` (ej. `-1001987654321`).
2. **Opción B (Reenviar mensaje):**
   - Reenvía cualquier mensaje del canal al bot **`@JsonDumpBot`** o **`@username_to_id_bot`** y te indicará el `chat_id`.

---

## PASO 4: Configuración de Broker (Paper Trading vs cTrader Open API)

### 4.1 Modo Paper Trading (Recomendado para las primeras semanas)
- Viene activado por defecto con `BROKER_TYPE=paper`.
- No requiere abrir ninguna cuenta de broker externa ni arriesgar dinero.
- Simula ticks en tiempo real de XAUUSD, spread dinámico (10–25 cents), balance inicial ($10,000 USD), cálculo de apalancamiento (100:1), margen por slot (25%) y liquidación de PnL.

---

### 4.2 Modo cTrader Open API (Para operar en cuenta real con bajas comisiones)
Cuando decidas pasar a cuenta real con cTrader:
1. Abre una cuenta con un broker ECN que soporte cTrader (como **IC Markets**, **Pepperstone** o **FxPro**).
2. Ve al portal de desarrolladores de Spotware: **[https://openapi.ctrader.com](https://openapi.ctrader.com)**.
3. Inicia sesión con tu cTrader ID y crea una nueva aplicación ("Create Application").
4. Obtendrás:
   - `Client ID` ➔ `CTRADER_CLIENT_ID`
   - `Client Secret` ➔ `CTRADER_CLIENT_SECRET`
5. En la sección de cuentas, autoriza tu cuenta de trading y genera un **Access Token**.
6. Configura en el `.env`: `BROKER_TYPE=ctrader`.

---

## PASO 5: Configurar el archivo `.env`
Copia el archivo `.env.example` y crea tu archivo `.env`:

```bash
cd bot_trading
cp .env.example .env
```

Edita `.env` con tus credenciales:

```ini
# ==============================================================================
# CONFIGURACIÓN DEL MOTOR DE TRADING AUTÓNOMO XAUUSD
# ==============================================================================

ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
API_KEY=sec_xauusd_trading_key_2026
DATABASE_URL=sqlite+aiosqlite:///./trading_bot.db

# Credenciales de Telegram MTProto (Paso 1)
TG_API_ID=12345678
TG_API_HASH=abcdef0123456789abcdef0123456789
TG_PHONE=+34600000000
TG_SESSION_NAME=bot_session
TARGET_CHANNEL_ID=-1001234567890
INGESTION_ENABLED=true

# Bot Admin de Telegram (Paso 2 y 3)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_TELEGRAM_USER_ID=987654321

# Motor de Riesgo
MAX_CONCURRENT_SLOTS=4
SLOT_MARGIN_PERCENT=0.25
LEVERAGE=100.0
CONTRACT_SIZE=100.0
MIN_LOT_SIZE=0.01
LOT_STEP=0.01
SLIPPAGE_TOLERANCE_USD=0.00
DEFAULT_DYNAMIC_SL_DELTA_USD=8.50
AUTO_EXECUTION_ENABLED=true

# Broker
BROKER_TYPE=paper
INITIAL_PAPER_BALANCE=10000.00
PAPER_SPREAD_MIN_CENTS=0.10
PAPER_SPREAD_MAX_CENTS=0.25
INITIAL_XAUUSD_PRICE=2345.50
```

---

## PASO 6: Ejecución del Sistema

### Opción A: Un solo comando con Docker Compose (Recomendado)
Para arrancar todo el ecosistema (Backend FastAPI, SQLite WAL, WebSockets y Dashboard Astro):

```bash
# 1. Situarse en la carpeta del proyecto
cd bot_trading

# 2. Levantar los contenedores
docker-compose up --build -d

# 3. Ver logs en tiempo real
docker-compose logs -f
```

---

### Opción B: Ejecución en Entorno Local (Python + Astro)

#### 1. Backend (Python 3.11+)
```bash
cd bot_trading

# Crear y activar entorno virtual
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend (Node.js 18+)
En una segunda terminal:
```bash
cd bot_trading/frontend

# Instalar paquetes
npm install

# Iniciar dashboard
npm run dev
```

---

## PASO 7: Verificación, Comandos del Bot y Dashboard

### 1. Acceso al Dashboard de Trading
- Abre en tu navegador: **`http://localhost:4321`** (o `http://localhost:8000/docs` para la API OpenAPI).
- Verás la interfaz **Obsidian Terminal**:
  - **Header de Telemetría:** Ticker XAUUSD Spot en tiempo real con animación de pulso, Balance, Equidad y PnL Flotante.
  - **Matriz de 4 Slots:** Visualización del estado de cada slot con la barra de progreso de hitos (Entrada ➔ TP1 ➔ TP2 ➔ TP3) y botón de cierre en hover.
  - **Gráfico en Vivo:** Grid Bloomberg con cotización en tiempo real y niveles dinámicos de entrada, SL y TP.
  - **Panel de Controles:** Toggles de Ingesta, Auto-ejecución, botón "+ SEÑAL TEST" y el botón de pánico **CERRAR TODO (KILL-SWITCH)**.
  - **Historial & Auditoría:** Modal con registro detallado de cada trade y logs SQLite WAL.

---

### 2. Comandos en el Bot Privado de Telegram
Abre Telegram y chatea con tu bot privado:
- `/status` ➔ Muestra la cotización actual de XAUUSD, el balance, equidad y el estado de los 4 slots.
- `/slots` ➔ Muestra el detalle milimétrico de las posiciones vivas (SL actual, TP1/2/3, PnL flotante).
- `/pause` ➔ Pausa la ingesta de nuevas señales de Telegram.
- `/resume` ➔ Reanuda la ingesta de señales.
- `/kill` ➔ Ejecuta el cierre de pánico inmediato de todas las posiciones a mercado y pausa la ingesta.

---

### 3. Prueba Rápida de Ejecución (Señal Simulada)
Puedes enviar una señal de prueba desde el Dashboard pulsando el botón **"+ SEÑAL TEST"** o mediante cURL:

```bash
curl -X POST http://localhost:8000/api/v1/signal/test \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: sec_xauusd_trading_key_2026" \
  -d '{
    "side": "BUY",
    "entry_price": 2345.50,
    "sl_price": 2335.00,
    "tp1": 2350.00,
    "tp2": 2355.00,
    "tp3": 2365.00
  }'
```

¡El Slot #1 se activará de inmediato, recibirás la alerta en tu bot de Telegram y verás cómo el Trailing SL sube automáticamente a TP1 y TP2 a medida que el precio fluctúa!
