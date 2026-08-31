import React, { useState, useRef } from 'react';
import { PositionMatrix, type SlotTradeData } from './PositionMatrix';
import { SignalFeed, type TradeLifecycleCardItem } from './SignalFeed';
import { NewsFeed } from './NewsFeed';
import { AuditLogsModal } from './AuditLogsModal';
import { SystemHealthModal } from './SystemHealthModal';

interface MobileOperatorDashboardProps {
  balance?: number | null;
  hasLiveBalance?: boolean;
  currentPrice: number;
  slots: SlotTradeData[];
  trades: TradeLifecycleCardItem[];
  isIngestionActive: boolean;
  isAutoExecutionActive: boolean;
  onToggleIngestion: () => void;
  onToggleAutoExecution: () => void;
  onRearmBot?: () => void;
  onEmergencyClose: () => void;
  onCloseSlot: (slotId: number) => void;
  onEmitTestSignal: () => void;
  userEmail: string | null;
  onLogout: () => void;
}

// Logo CASH_LOGO.svg según dist/svg/CASH_LOGO.svg
const CashLogoIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 32 32" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M0 25v-18h32v18h-32zM2 8.938v14.062h28v-14.062h-28zM21 16c0-3.313-2.238-6-5-6h13v12h-13c2.762 0 5-2.687 5-6zM25 18c0.828 0 1.5-0.896 1.5-2s-0.672-2-1.5-2-1.5 0.896-1.5 2 0.672 2 1.5 2zM18.118 13.478c-0.015 0.055-0.036 0.094-0.062 0.119-0.027 0.025-0.063 0.037-0.109 0.037s-0.118-0.028-0.219-0.086c-0.1-0.059-0.223-0.121-0.368-0.189-0.146-0.068-0.314-0.13-0.506-0.187s-0.402-0.083-0.631-0.083c-0.18 0-0.336 0.021-0.469 0.065s-0.245 0.104-0.334 0.18c-0.090 0.077-0.156 0.17-0.2 0.277s-0.065 0.222-0.065 0.342c0 0.18 0.049 0.335 0.147 0.466s0.229 0.248 0.394 0.35c0.165 0.103 0.351 0.198 0.56 0.287 0.207 0.090 0.42 0.185 0.637 0.284 0.217 0.101 0.429 0.214 0.637 0.341s0.395 0.279 0.557 0.456 0.293 0.385 0.394 0.624c0.1 0.24 0.149 0.521 0.149 0.847 0 0.425-0.078 0.797-0.236 1.118s-0.373 0.588-0.645 0.802c-0.271 0.215-0.587 0.376-0.949 0.484-0.046 0.014-0.096 0.020-0.143 0.031v1.092h-0.983v-0.963c-0.013 0-0.024 0.002-0.036 0.002-0.279 0-0.539-0.022-0.778-0.067s-0.451-0.101-0.634-0.164c-0.184-0.064-0.336-0.131-0.459-0.201s-0.211-0.132-0.265-0.186c-0.054-0.054-0.093-0.132-0.116-0.234-0.023-0.103-0.035-0.249-0.035-0.441 0-0.129 0.004-0.237 0.013-0.325s0.022-0.158 0.041-0.213 0.043-0.093 0.075-0.116c0.031-0.022 0.067-0.034 0.109-0.034 0.058 0 0.14 0.034 0.247 0.103s0.243 0.145 0.409 0.228c0.167 0.084 0.365 0.159 0.597 0.229 0.231 0.068 0.499 0.103 0.803 0.103 0.2 0 0.379-0.024 0.537-0.072s0.293-0.115 0.403-0.203 0.194-0.196 0.253-0.325c0.059-0.13 0.088-0.273 0.088-0.433 0-0.183-0.051-0.34-0.15-0.472-0.1-0.131-0.23-0.247-0.391-0.35-0.16-0.102-0.342-0.197-0.546-0.287s-0.414-0.185-0.631-0.284c-0.216-0.1-0.427-0.213-0.631-0.341s-0.386-0.278-0.546-0.455c-0.16-0.177-0.291-0.387-0.39-0.628s-0.15-0.531-0.15-0.868c0-0.388 0.072-0.728 0.215-1.021s0.337-0.537 0.581-0.73 0.531-0.338 0.862-0.434c0.17-0.050 0.346-0.085 0.526-0.109v-1.034h0.983v1.034c0.039 0.005 0.078 0.003 0.117 0.009 0.191 0.029 0.371 0.068 0.537 0.118 0.167 0.049 0.314 0.104 0.444 0.167 0.129 0.062 0.214 0.113 0.256 0.155s0.069 0.076 0.085 0.105c0.014 0.029 0.026 0.068 0.037 0.116s0.018 0.108 0.021 0.182c0.004 0.072 0.006 0.163 0.006 0.271 0 0.121-0.003 0.224-0.009 0.308-0.009 0.079-0.019 0.149-0.034 0.203zM11 16c0 3.313 2.238 6 5 6h-13v-12h13c-2.762 0-5 2.687-5 6zM7 14c-0.829 0-1.5 0.896-1.5 2s0.671 2 1.5 2c0.828 0 1.5-0.896 1.5-2s-0.672-2-1.5-2z"/>
  </svg>
);

// KILL SWITCH.svg dinámico estilo interruptor mecánico deslizante con soporte ON y OFF
const KillSwitchToggle: React.FC<{
  isOn: boolean;
  onClick: () => void;
}> = ({ isOn, onClick }) => {
  return (
    <button
      onClick={onClick}
      title={isOn ? "KILL SWITCH ACTIVO: Pulsa para apagar bot y cerrar todas las posiciones" : "BOT DETENIDO (OFF): Pulsa para reactivar operativa y reanudar escucha"}
      className="flex items-center gap-1.5 p-1 rounded hover:bg-surface-container active:scale-95 transition-all cursor-pointer select-none group shrink-0"
    >
      <div className="w-10 h-5 relative shrink-0">
        <svg
          viewBox="0 0 117 63"
          className="w-full h-full overflow-visible"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Track / Marco del Interruptor según dist/svg/KILL SWITCH.svg */}
          <path
            d="M31.5,62.6 L85.5,62.6 C102.6,62.6 116.6,48.7 116.6,31.5 C116.6,14.3 102.7,0.4 85.5,0.4 L31.5,0.4 C14.4,0.4 0.4,14.3 0.4,31.5 C0.4,48.7 14.4,62.6 31.5,62.6 Z M31.5,8.6 L85.5,8.6 C98.1,8.6 108.4,18.9 108.4,31.5 C108.4,44.1 98.1,54.4 85.5,54.4 L31.5,54.4 C18.9,54.4 8.6,44.1 8.6,31.5 C8.6,18.9 18.9,8.6 31.5,8.6 Z"
            fill={isOn ? "#1c202d" : "#3b0c0c"}
            stroke={isOn ? "#17AB13" : "#ef4444"}
            strokeWidth="2"
          />

          {/* Knob deslizante dinámico */}
          <g
            className="transition-transform duration-300 ease-out"
            style={{
              transform: isOn ? "translateX(54px)" : "translateX(0px)",
            }}
          >
            <path
              d="M31.5,48.8 C41,48.8 48.8,41 48.8,31.5 C48.8,22 41,14.2 31.5,14.2 C22,14.2 14.2,22 14.2,31.5 C14.2,41 22,48.8 31.5,48.8 Z M31.5,22.4 C36.5,22.4 40.6,26.5 40.6,31.5 C40.6,36.5 36.5,40.6 31.5,40.6 C26.5,40.6 22.4,36.5 22.4,31.5 C22.4,26.5 26.5,22.4 31.5,22.4 Z"
              fill={isOn ? "#17AB13" : "#ef4444"}
              filter={isOn ? "drop-shadow(0 0 5px rgba(23,171,19,0.9))" : "drop-shadow(0 0 5px rgba(239,68,68,0.9))"}
            />
          </g>
        </svg>
      </div>
      <span className={`text-[10px] font-mono font-bold tracking-tight ${isOn ? 'text-emerald-400' : 'text-error'}`}>
        {isOn ? 'KILL' : 'OFF'}
      </span>
    </button>
  );
};

export const MobileOperatorDashboard: React.FC<MobileOperatorDashboardProps> = ({
  balance,
  hasLiveBalance = false,
  currentPrice,
  slots = [],
  trades = [],
  isIngestionActive,
  isAutoExecutionActive,
  onToggleIngestion,
  onToggleAutoExecution,
  onRearmBot,
  onEmergencyClose,
  onCloseSlot,
  onEmitTestSignal,
  userEmail,
  onLogout,
}) => {
  // Pestañas: 0 = Señales, 1 = Posiciones (Home por defecto), 2 = Noticias
  const [activeTab, setActiveTab] = useState<number>(1);
  const [showKillSwitchConfirm, setShowKillSwitchConfirm] = useState<boolean>(false);
  const [showAuditModal, setShowAuditModal] = useState<boolean>(false);
  const [showHealthModal, setShowHealthModal] = useState<boolean>(false);
  const [showUserMenu, setShowUserMenu] = useState<boolean>(false);

  const isBotFullyActive = isIngestionActive && isAutoExecutionActive;

  // Manejador interactivo para alternar el Kill Switch en ambas direcciones
  const handleKillSwitchClick = () => {
    if (isBotFullyActive) {
      // Si está activo -> solicitar confirmación de parada de emergencia
      setShowKillSwitchConfirm(true);
    } else {
      // Si está detenido -> reactivar de inmediato
      if (onRearmBot) {
        onRearmBot();
      } else {
        if (!isIngestionActive) onToggleIngestion();
        if (!isAutoExecutionActive) onToggleAutoExecution();
      }
    }
  };

  // Control táctil para gestos de Swipe
  const touchStartX = useRef<number | null>(null);
  const touchEndX = useRef<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    touchEndX.current = null;
    touchStartX.current = e.targetTouches[0].clientX;
  };

  const onTouchMove = (e: React.TouchEvent) => {
    touchEndX.current = e.targetTouches[0].clientX;
  };

  const onTouchEnd = () => {
    if (!touchStartX.current || !touchEndX.current) return;
    const distance = touchStartX.current - touchEndX.current;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe && activeTab < 2) {
      setActiveTab((prev) => prev + 1);
    } else if (isRightSwipe && activeTab > 0) {
      setActiveTab((prev) => prev - 1);
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-background text-text-primary overflow-hidden select-none">
      {/* 1. Header Táctil Móvil */}
      <header className="h-14 border-b border-outline-variant bg-surface px-3 flex items-center justify-between shrink-0 z-30 shadow-md">
        {/* Logo CASH LOGO.svg en Color Corporativo & Estado del Motor */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 flex items-center justify-center text-primary shrink-0">
            <CashLogoIcon className="w-6 h-6 fill-current text-primary" />
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-bold text-xs tracking-wider text-text-primary">GOLD-EX</span>
            <div className="flex items-center gap-1">
              <span className={`w-1.5 h-1.5 rounded-full ${isBotFullyActive ? 'bg-primary animate-pulse' : 'bg-error'}`} />
              <span className="text-[9px] font-mono text-text-secondary">
                {isBotFullyActive ? 'EN VIVO' : 'PAUSADO'}
              </span>
            </div>
          </div>
        </div>

        {/* Acciones Rápidas: BALANCE a la izquierda del KILL SWITCH & Menú */}
        <div className="flex items-center gap-2 sm:gap-2.5">
          {/* Bloque Balance cTrader (Muestra 'No disponible' si no hay token) */}
          <div className="flex items-center gap-1 font-mono text-xs">
            <span className="text-[9px] text-text-secondary font-semibold tracking-tight">BAL:</span>
            {hasLiveBalance && balance !== null && balance !== undefined ? (
              <span className="font-bold text-text-primary text-[11px] font-mono whitespace-nowrap">
                ${balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            ) : (
              <span className="text-[10px] text-text-secondary/75 italic font-mono whitespace-nowrap">
                No disponible
              </span>
            )}
          </div>

          {/* Interruptor Dinámico KILL SWITCH con soporte bidireccional ON/OFF */}
          <KillSwitchToggle
            isOn={isBotFullyActive}
            onClick={handleKillSwitchClick}
          />

          {/* Menú de Controles y Perfil */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="w-8 h-8 rounded bg-surface-container hover:bg-surface-container-high border border-outline-variant flex items-center justify-center text-text-secondary text-sm"
            >
              ⚙️
            </button>

            {showUserMenu && (
              <div className="absolute right-0 top-10 w-52 bg-surface-container-highest border border-outline-variant rounded-md shadow-2xl p-2 z-50 flex flex-col gap-1.5 font-mono text-xs">
                <div className="p-1 border-b border-outline-variant/50 text-[10px] text-text-secondary truncate">
                  {userEmail || 'Operador Autorizado'}
                </div>

                {!isBotFullyActive && (
                  <button
                    onClick={() => {
                      if (onRearmBot) onRearmBot();
                      setShowUserMenu(false);
                    }}
                    className="flex items-center justify-center p-2 rounded bg-primary/20 text-primary border border-primary/40 font-bold text-center hover:bg-primary/30"
                  >
                    🟢 REARMAR Y ACTIVAR BOT
                  </button>
                )}

                <button
                  onClick={() => {
                    onToggleIngestion();
                    setShowUserMenu(false);
                  }}
                  className="flex items-center justify-between p-1.5 rounded hover:bg-surface-container text-left"
                >
                  <span>Ingesta Telegram:</span>
                  <span className={isIngestionActive ? 'text-primary font-bold' : 'text-error'}>
                    {isIngestionActive ? 'ON' : 'OFF'}
                  </span>
                </button>
                <button
                  onClick={() => {
                    onToggleAutoExecution();
                    setShowUserMenu(false);
                  }}
                  className="flex items-center justify-between p-1.5 rounded hover:bg-surface-container text-left"
                >
                  <span>Auto-Ejecución:</span>
                  <span className={isAutoExecutionActive ? 'text-primary font-bold' : 'text-error'}>
                    {isAutoExecutionActive ? 'ON' : 'OFF'}
                  </span>
                </button>
                <button
                  onClick={() => {
                    onEmitTestSignal();
                    setShowUserMenu(false);
                  }}
                  className="p-1.5 rounded hover:bg-surface-container text-left text-primary"
                >
                  ⚡ Emitir Señal Test
                </button>
                <button
                  onClick={() => {
                    setShowAuditModal(true);
                    setShowUserMenu(false);
                  }}
                  className="p-1.5 rounded hover:bg-surface-container text-left"
                >
                  📜 Logs de Auditoría
                </button>
                <button
                  onClick={() => {
                    setShowHealthModal(true);
                    setShowUserMenu(false);
                  }}
                  className="p-1.5 rounded hover:bg-surface-container text-left"
                >
                  🩺 Estado de Salud
                </button>
                <button
                  onClick={() => {
                    onLogout();
                    setShowUserMenu(false);
                  }}
                  className="p-1.5 rounded hover:bg-error/20 text-left text-error border-t border-outline-variant/50"
                >
                  🚪 Cerrar Sesión
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* 2. Área de Contenido con Deslizamiento Táctil (Swipe Carousel) */}
      <main
        className="flex-1 relative overflow-hidden min-h-0"
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        <div
          className="flex h-full w-[300%] transition-transform duration-300 ease-out"
          style={{ transform: `translateX(-${activeTab * (100 / 3)}%)` }}
        >
          {/* Pantalla 0: Registro de Señales */}
          <div className="w-1/3 h-full p-2 overflow-hidden">
            <SignalFeed trades={trades} />
          </div>

          {/* Pantalla 1: Matriz de Posiciones (Pantalla Principal) */}
          <div className="w-1/3 h-full p-2 overflow-hidden">
            <PositionMatrix
              slots={slots}
              currentPrice={currentPrice}
              onCloseSlot={onCloseSlot}
            />
          </div>

          {/* Pantalla 2: Feed de Noticias & Radar IA */}
          <div className="w-1/3 h-full p-2 overflow-hidden">
            <NewsFeed isMobile={true} />
          </div>
        </div>
      </main>

      {/* 3. Indicador Discreto de Pantalla Deslizable (Paginación Minimalista) */}
      <div className="h-3 flex items-center justify-center gap-1.5 pb-1 shrink-0 bg-background">
        <button
          onClick={() => setActiveTab(0)}
          className={`h-1 rounded-full transition-all ${
            activeTab === 0 ? 'bg-primary w-4' : 'bg-outline-variant w-1.5'
          }`}
          title="Señales"
        />
        <button
          onClick={() => setActiveTab(1)}
          className={`h-1 rounded-full transition-all ${
            activeTab === 1 ? 'bg-primary w-4' : 'bg-outline-variant w-1.5'
          }`}
          title="Posiciones"
        />
        <button
          onClick={() => setActiveTab(2)}
          className={`h-1 rounded-full transition-all ${
            activeTab === 2 ? 'bg-primary w-4' : 'bg-outline-variant w-1.5'
          }`}
          title="Noticias"
        />
      </div>

      {/* Modal de Confirmación de Kill Switch Móvil */}
      {showKillSwitchConfirm && (
        <div className="fixed inset-0 z-50 bg-black/85 flex items-center justify-center p-4">
          <div className="bg-surface-container-highest border-2 border-error rounded-lg p-5 max-w-sm w-full shadow-2xl flex flex-col gap-4 font-mono">
            <div className="flex items-center gap-2 text-error">
              <span className="text-2xl">⚠️</span>
              <h3 className="font-bold text-sm uppercase">EMERGENCIA KILL SWITCH</h3>
            </div>
            <p className="text-xs text-text-primary leading-relaxed">
              ¿Estás seguro de que deseas cerrar <strong>TODAS LAS POSICIONES ABIERTAS</strong> inmediatamente y detener el bot?
            </p>
            <div className="flex gap-2 justify-end pt-2">
              <button
                onClick={() => setShowKillSwitchConfirm(false)}
                className="px-3 py-1.5 rounded bg-surface hover:bg-surface-container text-text-secondary text-xs font-bold border border-outline-variant"
              >
                Cancelar
              </button>
              <button
                onClick={() => {
                  onEmergencyClose();
                  setShowKillSwitchConfirm(false);
                }}
                className="px-4 py-1.5 rounded bg-error hover:bg-red-700 text-white text-xs font-bold shadow-lg"
              >
                CONFIRMAR CIERRE TOTAL
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modales de Diagnóstico y Auditoría */}
      <AuditLogsModal
        isOpen={showAuditModal}
        onClose={() => setShowAuditModal(false)}
        logs={[]}
        history={[]}
      />

      <SystemHealthModal
        isOpen={showHealthModal}
        onClose={() => setShowHealthModal(false)}
        wsConnected={true}
        latencyMs={12}
        botActive={isIngestionActive}
        hasCtraderToken={hasLiveBalance}
        xauusdPrice={currentPrice}
      />
    </div>
  );
};
