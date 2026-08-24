# 🚨 ROADMAP & TAREAS PENDIENTES — GOLD-EX TRADING ENGINE (PRIORIDAD TOTAL)

> **ESTADO ACTUAL:** Sistema base desplegado al 100% en producción en GCP (`http://34.175.69.118:4321`).  
> **OBJETIVO CRÍTICO:** Enlace final con la API oficial de cTrader y activación operativa con cuenta real/demo.

---

## 🎯 1. [PRIORIDAD MÁXIMA] Integración Oficial cTrader Open API (Fix & Protobuf)

Cuando se disponga de las credenciales de la Open API de cTrader:

### ⚙️ 1.1 Variables de Entorno (`.env`)
Rellenar en el archivo `.env` del servidor (`/home/adriamartileyton2/app/autooro/bot_trading/.env`):
```env
BROKER_TYPE=ctrader
CTRADER_CLIENT_ID=<TU_CLIENT_ID>
CTRADER_CLIENT_SECRET=<TU_CLIENT_SECRET>
CTRADER_ACCOUNT_ID=<TU_ACCOUNT_ID>
CTRADER_ACCESS_TOKEN=<TU_ACCESS_TOKEN>
CTRADER_HOST=live.ctraderapi.com
CTRADER_PORT=5035
```

### 💱 1.2 Flujo de Ejecución a Mercado
- [ ] **Apertura de Órdenes:** Activar `ProtoOANewOrderReq` para despachar automáticamente la entrada con lotaje dinámico calculado (100x apalancamiento, 1 lote = 100 oz oro).
- [ ] **Gestión de Riesgo (Opción B en Broker):** 
  - Al alcanzar TP1 (+30 pips): Despachar `ProtoOAClosePositionReq` con el 50% del volumen y modificar SL a Break-Even (`ProtoOAAmendPositionSLTPReq`).
  - Al alcanzar TP2: Modificar SL a TP1.
  - Al alcanzar TP3: Cerrar el 50% restante a mercado.

### 💰 1.3 Telemetría de Cuenta y Balance en Vivo
- [ ] Sincronizar eventos `ProtoOASpotEvent` / `ProtoOAAccountAuthRes` para que el campo `BALANCE` en el Header del frontend pase automáticamente de *"No disponible"* a la cifra real en USD de la cuenta.

---

## ⚡ 2. [PRIORIDAD ALTA] Linkado de Botones Interactivos & Diagnósticos

- [ ] **Botón `Cerrar Slot`:** Conectar el callback del frontend con la orden `ProtoOAClosePositionReq` directa al broker para liquidación manual instantánea de cada slot.
- [ ] **Botón `Panic Close / Kill-Switch`:** Conectar con la rutina de cierre masivo de todas las posiciones vivas y cancelación de órdenes activas.
- [ ] **Modal de Diagnóstico (Punto de Humo):**
  - Conectar el botón *"Comprobar Estado"* con un test de ping y autenticación real contra los servidores de cTrader (`live.ctraderapi.com:5035`).

---

## 📲 3. [PRIORIDAD MEDIA] Autenticación Limpia de Telegram MTProto en la VM

- [ ] Ejecutar en la VM el script interactivo para generar la sesión local limpia:
  ```bash
  cd ~/app/autooro/bot_trading && python3 scripts/auth_telegram.py
  ```
  *(Introducir el código de 5 dígitos de Telegram una única vez directamente en el servidor).*

---

## 🤖 4. [PRIORIDAD MEDIA] Notificaciones Push del Bot Administrador (@goldex_AML_bot)

- [ ] Enviar notificaciones en tiempo real al chat privado del Administrador (`ID: 395721207`) ante:
  - Nueva orden ejecutada (Slot #X, BUY/SELL, Precio, TP/SL).
  - Cierre parcial 50% en TP1 y SL movido a Break-Even.
  - Cierre total de posición o activación de Kill-Switch.

---

## ☁️ 5. [FUTURO / FASE 2] Réplica Asíncrona y Copia de Seguridad en Supabase

- [ ] **Configuración de Conector Supabase (`.env`):**
  - `SUPABASE_URL` y `SUPABASE_KEY` (service_role / anon).
- [ ] **Worker de Sincronización Asíncrona (Non-Blocking):**
  - Implementar worker en segundo plano (fire-and-forget) para replicar cada operación cerrada (`Trade`), mensaje de señal (`RawTelegramMessage`) y log de auditoría (`SystemAuditLog`) a PostgreSQL en Supabase.
- [ ] **Data Warehouse & Dashboard Móvil:**
  - Mantener SQLite WAL en local como motor de ultra-baja latencia (<0.1ms) y Supabase como almacén en la nube para consultas, visualización en app móvil y copias de seguridad continuas.

---

*Documento actualizado y sincronizado con el repositorio oficial.*
