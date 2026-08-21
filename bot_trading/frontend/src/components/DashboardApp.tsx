import React, { useState, useEffect, useRef } from 'react';
import { HeaderTelemetry } from './HeaderTelemetry';
import { PositionMatrix, type SlotTradeData } from './PositionMatrix';
import { SignalFeed, type TradeLifecycleCardItem } from './SignalFeed';
import { LiveChart } from './LiveChart';
import { ControlDropdown } from './ControlDropdown';
import { AuditLogsModal } from './AuditLogsModal';

const getApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.location.hostname) {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }
  return 'http://localhost:8000';
};

const getWsUrl = () => {
  if (typeof window !== 'undefined' && window.location.hostname) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.hostname}:8000/ws/live`;
  }
  return 'ws://localhost:8000/ws/live';
};

const API_KEY = 'sec_xauusd_trading_key_2026';

export const DashboardApp: React.FC = () => {
  const [xauusdPrice, setXauusdPrice] = useState<number>(2345.50);
  const [balance, setBalance] = useState<number>(10000.00);
  const [floatingPnl, setFloatingPnl] = useState<number>(0.00);
  const [botActive, setBotActive] = useState<boolean>(true);
  const [ingestionEnabled, setIngestionEnabled] = useState<boolean>(true);
  const [autoExecutionEnabled, setAutoExecutionEnabled] = useState<boolean>(true);
  
  const [slots, setSlots] = useState<SlotTradeData[]>([
    { slot_id: 1, is_active: false },
    { slot_id: 2, is_active: false },
    { slot_id: 3, is_active: false },
    { slot_id: 4, is_active: false },
  ]);

  const [trades, setTrades] = useState<TradeLifecycleCardItem[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [tradeHistory, setTradeHistory] = useState<any[]>([]);
  const [isAuditModalOpen, setIsAuditModalOpen] = useState<boolean>(false);
  const [isControlDropdownOpen, setIsControlDropdownOpen] = useState<boolean>(false);
  const [latencyMs, setLatencyMs] = useState<number>(12);
  const [wsConnected, setWsConnected] = useState<boolean>(false);

  const wsRef = useRef<WebSocket | null>(null);

  // 1. Cargar estado inicial y mensajes desde la API REST
  const fetchInitialData = async () => {
    try {
      const baseUrl = getApiBaseUrl();
      const stateRes = await fetch(`${baseUrl}/api/v1/state`);
      if (stateRes.ok) {
        const stateData = await stateRes.json();
        setXauusdPrice(stateData.xauusd_spot?.ask || 2345.50);
        setBalance(stateData.account?.balance || 10000.00);
        setIngestionEnabled(stateData.ingestion_enabled);
        setAutoExecutionEnabled(stateData.auto_execution_enabled);
        setBotActive(stateData.ingestion_enabled);

        if (stateData.slots) {
          const formattedSlots: SlotTradeData[] = stateData.slots.map((s: any) => ({
            slot_id: s.slot_id,
            is_active: s.is_active,
            ticket_id: s.ticket_id,
            side: s.side,
            lot_size: s.lot_size,
            entry_price: s.entry_price,
            current_sl: s.current_sl,
            initial_sl: s.initial_sl,
            tp1: s.tp1,
            tp2: s.tp2,
            tp3: s.tp3,
            current_price: s.current_price,
            current_pnl: s.current_pnl,
            status: s.status,
          }));
          setSlots(formattedSlots);
          const totalPnl = formattedSlots.reduce((acc, s) => acc + (s.current_pnl || 0), 0);
          setFloatingPnl(totalPnl);
        }
      }

      // Cargar Tarjetas de Ciclo de Vida de Trades Consolidados
      const tradeRes = await fetch(`${baseUrl}/api/v1/signals/trades?limit=50`);
      if (tradeRes.ok) {
        const tradeData = await tradeRes.json();
        setTrades(tradeData);
      }
    } catch (err) {
      console.warn('Backend aún no disponible para REST fetch:', err);
    }
  };

  // 2. Conectar WebSocket con Reconexión Automática
  useEffect(() => {
    fetchInitialData();

    let reconnectTimer: any = null;

    const connectWebSocket = () => {
      const startTime = Date.now();
      const ws = new WebSocket(getWsUrl());
      wsRef.current = ws;

      ws.onopen = () => {
        setWsConnected(true);
        setLatencyMs(Math.max(5, Date.now() - startTime));
        console.log('WebSocket conectado a GOLD-EX Live Stream');
      };

      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);

          if (payload.type === 'TICK_UPDATE' || payload.type === 'INITIAL_SNAPSHOT') {
            if (payload.tick) {
              setXauusdPrice(payload.tick.ask);
            } else if (payload.xauusd_spot) {
              setXauusdPrice(payload.xauusd_spot.ask);
            }

            if (payload.account) {
              setBalance(payload.account.balance);
            }

            if (payload.slots) {
              const updatedSlots: SlotTradeData[] = payload.slots.map((s: any) => ({
                slot_id: s.slot_id,
                is_active: s.is_active,
                ticket_id: s.ticket_id || s.trade?.ticket_id,
                side: s.side || s.trade?.side,
                lot_size: s.lot_size || s.trade?.lot_size,
                entry_price: s.entry_price || s.trade?.entry_price,
                current_sl: s.current_sl || s.trade?.current_sl,
                initial_sl: s.initial_sl || s.trade?.initial_sl,
                tp1: s.tp1 || s.trade?.tp1,
                tp2: s.tp2 || s.trade?.tp2,
                tp3: s.tp3 || s.trade?.tp3,
                current_price: s.current_price || s.trade?.current_price || xauusdPrice,
                current_pnl: s.current_pnl !== undefined ? s.current_pnl : s.trade?.current_pnl || 0,
                status: s.status || s.trade?.status || 'AVAILABLE',
              }));
              setSlots(updatedSlots);
              const totalPnl = updatedSlots.reduce((acc, s) => acc + (s.current_pnl || 0), 0);
              setFloatingPnl(totalPnl);
            }
          }
        } catch (e) {
          console.error('Error parseando WebSocket payload:', e);
        }
      };

      ws.onclose = () => {
        setWsConnected(false);
        console.warn('WebSocket cerrado. Reintentando en 3s...');
        reconnectTimer = setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.warn('Error en WebSocket:', err);
        ws.close();
      };
    };

    connectWebSocket();

    const interval = setInterval(fetchInitialData, 10000);

    return () => {
      if (wsRef.current) wsRef.current.close();
      clearTimeout(reconnectTimer);
      clearInterval(interval);
    };
  }, []);

  // Handlers de Control
  const handleToggleIngestion = async () => {
    const endpoint = ingestionEnabled ? '/api/v1/control/pause' : '/api/v1/control/resume';
    try {
      const res = await fetch(`${getApiBaseUrl()}${endpoint}`, {
        method: 'POST',
        headers: { 'X-API-KEY': API_KEY },
      });
      if (res.ok) {
        const data = await res.json();
        setIngestionEnabled(data.ingestion_enabled);
        setBotActive(data.ingestion_enabled);
      }
    } catch (err) {
      console.error('Error al cambiar estado de ingesta:', err);
    }
  };

  const handleToggleAutoExecution = async () => {
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/control/auto-execution/toggle`, {
        method: 'POST',
        headers: { 'X-API-KEY': API_KEY },
      });
      if (res.ok) {
        const data = await res.json();
        setAutoExecutionEnabled(data.auto_execution_enabled);
      }
    } catch (err) {
      console.error('Error al alternar auto-ejecución:', err);
    }
  };

  const handlePanicClose = async () => {
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/control/panic-close`, {
        method: 'POST',
        headers: { 'X-API-KEY': API_KEY },
      });
      if (res.ok) {
        setIngestionEnabled(false);
        setBotActive(false);
        await fetchInitialData();
      }
    } catch (err) {
      console.error('Error al ejecutar Kill-Switch:', err);
    }
  };

  const handleCloseSlot = async (slotId: number) => {
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/control/close-slot/${slotId}`, {
        method: 'POST',
        headers: { 'X-API-KEY': API_KEY },
      });
      if (res.ok) {
        await fetchInitialData();
      }
    } catch (err) {
      console.error(`Error al cerrar slot ${slotId}:`, err);
    }
  };

  const handleInjectTestSignal = async () => {
    try {
      await fetch(`${getApiBaseUrl()}/api/v1/signal/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-KEY': API_KEY,
        },
        body: JSON.stringify({
          side: 'BUY',
          entry_price: xauusdPrice,
          sl_price: xauusdPrice - 8.50,
          tp1: xauusdPrice + 5.00,
          tp2: xauusdPrice + 10.00,
          tp3: xauusdPrice + 15.00,
        }),
      });
      await fetchInitialData();
    } catch (err) {
      console.error('Error al inyectar señal de prueba:', err);
    }
  };

  const handleOpenAuditModal = async () => {
    try {
      const baseUrl = getApiBaseUrl();
      const [histRes, auditRes] = await Promise.all([
        fetch(`${baseUrl}/api/v1/history?limit=50`),
        fetch(`${baseUrl}/api/v1/audit?limit=50`),
      ]);
      if (histRes.ok) {
        const histData = await histRes.json();
        setTradeHistory(histData.history || []);
      }
      if (auditRes.ok) {
        const auditData = await auditRes.json();
        setAuditLogs(auditData || []);
      }
    } catch (e) {
      console.error('Error cargando auditoría:', e);
    }
    setIsAuditModalOpen(true);
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-background">
      {/* 1. Header de Telemetría con botón de controles */}
      <HeaderTelemetry
        xauusdPrice={xauusdPrice}
        balance={balance}
        floatingPnl={floatingPnl}
        botActive={botActive}
        onOpenSettings={() => setIsControlDropdownOpen(!isControlDropdownOpen)}
      />

      {/* Desplegable de Control y Kill Switch anclado al Header */}
      <ControlDropdown
        isOpen={isControlDropdownOpen}
        onClose={() => setIsControlDropdownOpen(false)}
        ingestionEnabled={ingestionEnabled}
        autoExecutionEnabled={autoExecutionEnabled}
        onToggleIngestion={handleToggleIngestion}
        onToggleAutoExecution={handleToggleAutoExecution}
        onPanicClose={handlePanicClose}
        onInjectTestSignal={handleInjectTestSignal}
      />

      {/* 2. Cuerpo Principal */}
      <div className="flex flex-1 overflow-hidden">
        {/* Barra Lateral de Navegación y Feed de Señales */}
        <nav className="hidden md:flex flex-col h-full w-84 bg-surface-container border-r border-outline-variant shrink-0" style={{ width: '340px' }}>
          <div className="p-3 border-b border-outline-variant flex justify-between items-center">
            <div>
              <div className="text-label-md font-bold text-primary truncate">XAUUSD-CORE-01</div>
              <div className="text-[11px] text-outline flex items-center gap-1.5 mt-0.5 font-mono">
                <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-primary pulse-live' : 'bg-error'}`} />
                {wsConnected ? 'Protobuf/WS Live' : 'Reconectando WS...'}
              </div>
            </div>
            <button
              onClick={handleOpenAuditModal}
              title="Ver Auditoría y Logs"
              className="p-1.5 rounded hover:bg-surface-container-highest text-outline hover:text-primary transition-colors flex items-center gap-1 border border-outline-variant/40"
            >
              <span className="material-symbols-outlined text-[16px]">receipt_long</span>
              <span className="text-[10px] font-mono">Auditoría</span>
            </button>
          </div>

          {/* Feed de Señales de Telegram en Vivo */}
          <div className="flex-1 overflow-hidden">
            <SignalFeed trades={trades} />
          </div>
        </nav>

        {/* Workspace Central Ampliado */}
        <main className="flex-1 p-2 flex flex-col gap-2 overflow-hidden bg-background">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 h-full">
            <PositionMatrix slots={slots} onCloseSlot={handleCloseSlot} />
            <LiveChart currentPrice={xauusdPrice} activeSlots={slots} />
          </div>
        </main>
      </div>

      {/* 3. Footer */}
      <footer className="w-full z-40 flex justify-between items-center px-4 py-1 h-7 bg-surface-container-lowest border-t border-outline-variant shrink-0">
        <div className="text-label-sm font-bold text-outline">
          © 2026 QUANTUM GOLD SYSTEMS — XAUUSD AUTONOMOUS ENGINE
        </div>
        <div className="flex gap-6 font-mono text-[11px] text-outline">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-green" /> Status: Nominal
          </span>
          <span>Latencia: {latencyMs}ms</span>
          <span className={wsConnected ? 'text-primary' : 'text-error'}>
            WS: {wsConnected ? 'Connected' : 'Offline'}
          </span>
        </div>
      </footer>

      {/* Modal de Auditoría */}
      <AuditLogsModal
        isOpen={isAuditModalOpen}
        onClose={() => setIsAuditModalOpen(false)}
        logs={auditLogs}
        history={tradeHistory}
      />
    </div>
  );
};
