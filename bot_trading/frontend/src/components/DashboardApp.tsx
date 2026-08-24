import React, { useState, useEffect, useRef } from 'react';
import { HeaderTelemetry } from './HeaderTelemetry';
import { PositionMatrix, type SlotTradeData } from './PositionMatrix';
import { SignalFeed, type TradeLifecycleCardItem } from './SignalFeed';
import { LiveChart } from './LiveChart';
import { NewsFeed } from './NewsFeed';
import { MobileOperatorDashboard } from './MobileOperatorDashboard';
import type { MarketAsset } from './MarketTicker';
import { ControlDropdown } from './ControlDropdown';
import { AuditLogsModal } from './AuditLogsModal';
import { SystemHealthModal } from './SystemHealthModal';
import { LoginScreen } from './LoginScreen';

const GOLD_ASSET: MarketAsset = {
  id: 'xauusd',
  name: 'Oro Spot',
  ticker: 'XAUUSD (Spot)',
  tvSymbol: 'OANDA:XAUUSD',
  market: 'Global',
  type: 'Metal Precioso Spot',
  description: 'Cotización SPOT del oro frente al dólar estadounidense (XAU/USD). Activo refugio físico.',
  price: 4652.60,
  change: 0.65,
  decimals: 2,
};

const getApiBaseUrl = () => {
  if (typeof window !== 'undefined') {
    if (window.location.port === '4321') {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return `${window.location.protocol}//${window.location.host}`;
  }
  return 'http://localhost:8000';
};

const getWsUrl = () => {
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    if (window.location.port === '4321') {
      return `${protocol}//${window.location.hostname}:8000/ws/live`;
    }
    return `${protocol}//${window.location.host}/ws/live`;
  }
  return 'ws://localhost:8000/ws/live';
};

const API_KEY = 'sec_xauusd_trading_key_2026';
const GOOGLE_CLIENT_ID = '844460269390-jdi3not996vcrhvg9uoiucbj6jm7hhdl.apps.googleusercontent.com';

// 4 Slots limpios preparados para recibir señales reales
const EMPTY_SLOTS: SlotTradeData[] = [
  { slot_id: 1, is_active: false },
  { slot_id: 2, is_active: false },
  { slot_id: 3, is_active: false },
  { slot_id: 4, is_active: false },
];

export const DashboardApp: React.FC = () => {
  // Estado de Autenticación con Google OAuth 2.0
  const [authToken, setAuthToken] = useState<string | null>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('goldex_auth_token');
    }
    return null;
  });
  const [authUser, setAuthUser] = useState<any>(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('goldex_auth_user');
      try {
        return stored ? JSON.parse(stored) : null;
      } catch {
        return null;
      }
    }
    return null;
  });
  const [isAuthChecking, setIsAuthChecking] = useState<boolean>(true);

  const [xauusdPrice, setXauusdPrice] = useState<number>(4587.50);
  const [balance, setBalance] = useState<number | null>(null);
  const [hasLiveBalance, setHasLiveBalance] = useState<boolean>(false);
  const [floatingPnl, setFloatingPnl] = useState<number>(0.00);
  const [botActive, setBotActive] = useState<boolean>(true);
  const [ingestionEnabled, setIngestionEnabled] = useState<boolean>(true);
  const [autoExecutionEnabled, setAutoExecutionEnabled] = useState<boolean>(true);
  
  const [slots, setSlots] = useState<SlotTradeData[]>(EMPTY_SLOTS);

  const [trades, setTrades] = useState<TradeLifecycleCardItem[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [tradeHistory, setTradeHistory] = useState<any[]>([]);
  const [isAuditModalOpen, setIsAuditModalOpen] = useState<boolean>(false);
  const [isHealthModalOpen, setIsHealthModalOpen] = useState<boolean>(false);
  const [isControlDropdownOpen, setIsControlDropdownOpen] = useState<boolean>(false);
  const [latencyMs, setLatencyMs] = useState<number>(12);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [selectedAsset, setSelectedAsset] = useState<MarketAsset>(GOLD_ASSET);
  const [desktopRightTab, setDesktopRightTab] = useState<'chart' | 'news'>('chart');

  const wsRef = useRef<WebSocket | null>(null);

  const getAuthHeaders = (extraHeaders: Record<string, string> = {}) => {
    const headers: Record<string, string> = { ...extraHeaders };
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }
    headers['X-API-KEY'] = API_KEY;
    return headers;
  };

  // 0. Verificar validez de la sesión JWT con el backend
  useEffect(() => {
    const verifySession = async () => {
      const token = localStorage.getItem('goldex_auth_token');
      if (!token) {
        setAuthToken(null);
        setAuthUser(null);
        setIsAuthChecking(false);
        return;
      }

      if (token === 'dev_mock_token_2026') {
        const storedUser = localStorage.getItem('goldex_auth_user');
        setAuthUser(storedUser ? JSON.parse(storedUser) : { email: 'adriamartileyton@gmail.com', name: 'Adrià Martí (Dev)' });
        setAuthToken(token);
        setIsAuthChecking(false);
        return;
      }

      try {
        const res = await fetch(`${getApiBaseUrl()}/api/v1/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          setAuthUser(data.user);
          setAuthToken(token);
        } else {
          localStorage.removeItem('goldex_auth_token');
          localStorage.removeItem('goldex_auth_user');
          setAuthToken(null);
          setAuthUser(null);
        }
      } catch (err) {
        console.warn('Backend aún no disponible para verificar sesión auth:', err);
      } finally {
        setIsAuthChecking(false);
      }
    };

    verifySession();
  }, []);

  // 1. Cargar estado inicial y mensajes desde la API REST
  const fetchInitialData = async () => {
    if (!authToken) return;

    try {
      const baseUrl = getApiBaseUrl();
      const stateRes = await fetch(`${baseUrl}/api/v1/state`, {
        headers: getAuthHeaders(),
      });
      if (stateRes.ok) {
        const stateData = await stateRes.json();
        setXauusdPrice(stateData.xauusd_spot?.ask || 4587.50);
        const hasToken = Boolean(stateData.has_ctrader_token);
        setHasLiveBalance(hasToken);
        setBalance(hasToken ? stateData.account?.balance : null);
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
            initial_lot_size: s.initial_lot_size,
            entry_price: s.entry_price,
            current_sl: s.current_sl,
            initial_sl: s.initial_sl,
            tp1: s.tp1,
            tp2: s.tp2,
            tp3: s.tp3,
            current_price: s.current_price,
            current_pnl: s.current_pnl,
            realized_cash_pnl: s.realized_cash_pnl,
            peak_price: s.peak_price,
            is_infinite_trailing: s.is_infinite_trailing,
            status: s.status,
          }));
          setSlots(formattedSlots);
          const totalPnl = formattedSlots.reduce((acc, s) => acc + (s.current_pnl || 0), 0);
          setFloatingPnl(totalPnl);
        }
      }

      // Cargar Tarjetas de Ciclo de Vida de Trades Consolidados
      const tradeRes = await fetch(`${baseUrl}/api/v1/signals/trades?limit=50`, {
        headers: getAuthHeaders(),
      });
      if (tradeRes.ok) {
        const tradeData = await tradeRes.json();
        setTrades(tradeData);
      }
    } catch (err) {
      console.warn('Backend aún no disponible para REST fetch:', err);
    }
  };

  // 2. Conectar WebSocket con Reconexión Automática y Token de Sesión
  useEffect(() => {
    if (!authToken) return;

    fetchInitialData();

    let reconnectTimer: any = null;

    const connectWebSocket = () => {
      const startTime = Date.now();
      const wsUrl = `${getWsUrl()}${authToken ? `?token=${encodeURIComponent(authToken)}` : ''}`;
      const ws = new WebSocket(wsUrl);
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

            if (payload.has_ctrader_token !== undefined) {
              setHasLiveBalance(Boolean(payload.has_ctrader_token));
            }

            if (payload.account) {
              if (payload.account.balance !== undefined && payload.account.balance !== null) {
                setBalance(payload.account.balance);
              }
            }

            if (payload.slots) {
              const updatedSlots: SlotTradeData[] = payload.slots.map((s: any) => ({
                slot_id: s.slot_id,
                is_active: s.is_active,
                ticket_id: s.ticket_id || s.trade?.ticket_id,
                side: s.side || s.trade?.side,
                lot_size: s.lot_size !== undefined ? s.lot_size : s.trade?.lot_size,
                initial_lot_size: s.initial_lot_size !== undefined ? s.initial_lot_size : s.trade?.initial_lot_size,
                entry_price: s.entry_price || s.trade?.entry_price,
                current_sl: s.current_sl || s.trade?.current_sl,
                initial_sl: s.initial_sl || s.trade?.initial_sl,
                tp1: s.tp1 || s.trade?.tp1,
                tp2: s.tp2 || s.trade?.tp2,
                tp3: s.tp3 || s.trade?.tp3,
                current_price: s.current_price || s.trade?.current_price || xauusdPrice,
                current_pnl: s.current_pnl !== undefined ? s.current_pnl : s.trade?.current_pnl || 0,
                realized_cash_pnl: s.realized_cash_pnl !== undefined ? s.realized_cash_pnl : s.trade?.realized_cash_pnl || 0,
                peak_price: s.peak_price !== undefined ? s.peak_price : s.trade?.peak_price,
                is_infinite_trailing: s.is_infinite_trailing !== undefined ? s.is_infinite_trailing : Boolean(s.trade?.is_infinite_trailing),
                status: s.status || s.trade?.status || 'AVAILABLE',
              }));
              setSlots(updatedSlots);
              const totalPnl = updatedSlots.reduce((acc, s) => acc + (s.current_pnl || 0), 0);
              setFloatingPnl(totalPnl);
            }
          }

          // Evento de Trade Recibido / Actualizado
          if (payload.type === 'TRADE_EVENT' || payload.type === 'SIGNAL_PARSED') {
            fetchInitialData();
          }
        } catch (e) {
          console.error('Error parseando WebSocket payload:', e);
        }
      };

      ws.onclose = () => {
        setWsConnected(false);
        console.warn('WebSocket desconectado. Reintentando en 3s...');
        reconnectTimer = setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error('Error en WebSocket Live Stream:', err);
        ws.close();
      };
    };

    connectWebSocket();

    const interval = setInterval(fetchInitialData, 5000);

    return () => {
      if (wsRef.current) wsRef.current.close();
      clearTimeout(reconnectTimer);
      clearInterval(interval);
    };
  }, [authToken]);

  // 3. Handlers para el Menú de Controles
  const handleLogout = () => {
    localStorage.removeItem('goldex_auth_token');
    localStorage.removeItem('goldex_auth_user');
    setAuthToken(null);
    setAuthUser(null);
    if (wsRef.current) wsRef.current.close();
  };

  const handleToggleIngestion = async () => {
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/control/pause`, {
        method: 'POST',
        headers: getAuthHeaders(),
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
        headers: getAuthHeaders(),
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
        headers: getAuthHeaders(),
      });
      if (res.ok) {
        setIngestionEnabled(false);
        setBotActive(false);
        setSlots((prev) => prev.map((s) => ({ slot_id: s.slot_id, is_active: false })));
        setFloatingPnl(0);
        await fetchInitialData();
      }
    } catch (err) {
      console.error('Error al ejecutar Kill-Switch:', err);
    }
  };

  const handleCloseSlot = async (slotId: number) => {
    try {
      setSlots((prev) =>
        prev.map((s) => (s.slot_id === slotId ? { slot_id: slotId, is_active: false } : s))
      );
      const res = await fetch(`${getApiBaseUrl()}/api/v1/control/close-slot/${slotId}`, {
        method: 'POST',
        headers: getAuthHeaders(),
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
      const res = await fetch(`${getApiBaseUrl()}/api/v1/signal/test`, {
        method: 'POST',
        headers: getAuthHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({
          side: 'BUY',
          entry_price: xauusdPrice,
          sl_price: xauusdPrice - 8.50,
          tp1: xauusdPrice + 5.00,
          tp2: xauusdPrice + 10.00,
          tp3: xauusdPrice + 15.00,
        }),
      });
      if (res.ok) {
        await fetchInitialData();
      }
    } catch (err) {
      console.error('Error al inyectar señal de prueba:', err);
    }
  };

  const handleOpenAuditModal = async () => {
    try {
      const baseUrl = getApiBaseUrl();
      const [histRes, auditRes] = await Promise.all([
        fetch(`${baseUrl}/api/v1/history?limit=50`, { headers: getAuthHeaders() }),
        fetch(`${baseUrl}/api/v1/audit?limit=50`, { headers: getAuthHeaders() }),
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

  // Si no está autenticado, mostrar la pantalla de bloqueo Obsidian Terminal Google OAuth
  if (!authToken && !isAuthChecking) {
    return (
      <LoginScreen
        apiBaseUrl={getApiBaseUrl()}
        clientId={GOOGLE_CLIENT_ID}
        onLoginSuccess={(token, user) => {
          setAuthToken(token);
          setAuthUser(user);
        }}
      />
    );
  }

  return (
    <>
      {/* 1. Vista Móvil Especializada con 3 Pantallas Deslizantes (Swipe), Kill Switch y Bottom Nav */}
      <div className="block md:hidden h-screen w-screen overflow-hidden">
        <MobileOperatorDashboard
          balance={balance}
          hasLiveBalance={hasLiveBalance}
          currentPrice={xauusdPrice}
          slots={slots}
          trades={trades}
          isIngestionActive={ingestionEnabled}
          isAutoExecutionActive={autoExecutionEnabled}
          onToggleIngestion={handleToggleIngestion}
          onToggleAutoExecution={handleToggleAutoExecution}
          onEmergencyClose={handlePanicClose}
          onCloseSlot={handleCloseSlot}
          onEmitTestSignal={handleInjectTestSignal}
          userEmail={authUser?.email || null}
          onLogout={handleLogout}
        />
      </div>

      {/* 2. Vista de Escritorio Profesional (3 Columnas con Gráfico / Radar de Noticias Opción C) */}
      <div className="hidden md:flex flex-col h-screen w-full overflow-hidden bg-background">
        {/* Header de Telemetría con botón de controles, usuario autenticado y diagnóstico */}
        <HeaderTelemetry
          xauusdPrice={xauusdPrice}
          balance={balance}
          hasLiveBalance={hasLiveBalance}
          botActive={botActive}
          authUser={authUser}
          selectedTvSymbol={selectedAsset.tvSymbol}
          onSelectAsset={(asset) => {
            setSelectedAsset(asset);
            setDesktopRightTab('chart');
          }}
          onOpenSettings={() => setIsControlDropdownOpen(!isControlDropdownOpen)}
          onOpenDiagnostics={() => setIsHealthModalOpen(true)}
          onLogout={handleLogout}
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
          onOpenAudit={handleOpenAuditModal}
        />

        {/* Cuerpo Principal con 3 Columnas Proporcionales */}
        <div className="flex flex-1 w-full overflow-hidden min-h-0">
          {/* Columna 1 (Izquierda): Registro de Señales en Formato Tarjeta */}
          <aside className="w-[310px] xl:w-[340px] p-2 flex flex-col h-full shrink-0 border-r border-outline-variant/60 bg-background overflow-hidden min-h-0">
            <SignalFeed trades={trades} />
          </aside>

          {/* Columna 2 (Centro): Matriz de Posiciones con Tarjetas Enriquecidas */}
          <section className="w-[330px] xl:w-[360px] p-2 flex flex-col h-full shrink-0 border-r border-outline-variant/60 bg-background overflow-hidden min-h-0">
            <PositionMatrix slots={slots} currentPrice={xauusdPrice} onCloseSlot={handleCloseSlot} />
          </section>

          {/* Columna 3 (Derecha): Pestañas Gráfico TradingView / Radar de Noticias IA (Opción C) */}
          <main className="flex-1 p-2 flex flex-col h-full overflow-hidden bg-background min-h-0">
            {/* Selector de Pestañas Superior */}
            <div className="flex items-center justify-between mb-1.5 px-1 shrink-0">
              <div className="flex items-center gap-1 bg-surface-container p-0.5 rounded border border-outline-variant">
                <button
                  onClick={() => setDesktopRightTab('chart')}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono transition-all ${
                    desktopRightTab === 'chart'
                      ? 'bg-primary text-black font-bold shadow-sm'
                      : 'text-text-secondary hover:text-text-primary'
                  }`}
                >
                  <span>📈</span>
                  <span>Gráfico {selectedAsset.name}</span>
                </button>

                <button
                  onClick={() => setDesktopRightTab('news')}
                  className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono transition-all ${
                    desktopRightTab === 'news'
                      ? 'bg-primary text-black font-bold shadow-sm'
                      : 'text-text-secondary hover:text-text-primary'
                  }`}
                >
                  <span>📰</span>
                  <span>Radar de Noticias IA</span>
                </button>
              </div>

              {desktopRightTab === 'chart' && selectedAsset.id !== 'xauusd' && (
                <button
                  onClick={() => setSelectedAsset(GOLD_ASSET)}
                  className="text-[11px] font-mono text-primary hover:underline flex items-center gap-1"
                >
                  <span>↩ Volver a Oro Spot</span>
                </button>
              )}
            </div>

            {/* Contenedor Activo */}
            <div className="flex-1 min-h-0 overflow-hidden">
              {desktopRightTab === 'chart' ? (
                <LiveChart
                  currentPrice={xauusdPrice}
                  activeSlots={slots}
                  selectedAsset={selectedAsset}
                  onResetToGold={() => setSelectedAsset(GOLD_ASSET)}
                />
              ) : (
                <NewsFeed />
              )}
            </div>
          </main>
        </div>

        {/* Footer Limpio con latencia y estado nominal */}
        <footer className="w-full z-40 flex justify-end items-center px-4 py-1 h-7 bg-surface-container-lowest border-t border-outline-variant shrink-0">
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

        {/* Modales de Auditoría y Diagnóstico */}
        <AuditLogsModal
          isOpen={isAuditModalOpen}
          onClose={() => setIsAuditModalOpen(false)}
          auditLogs={auditLogs}
          tradeHistory={tradeHistory}
        />

        <SystemHealthModal
          isOpen={isHealthModalOpen}
          onClose={() => setIsHealthModalOpen(false)}
          wsConnected={wsConnected}
          latencyMs={latencyMs}
          botActive={botActive}
          hasCtraderToken={hasLiveBalance}
          xauusdPrice={xauusdPrice}
        />
      </div>
    </>
  );
};
