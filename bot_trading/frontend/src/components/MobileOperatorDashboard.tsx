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
  onEmergencyClose: () => void;
  onCloseSlot: (slotId: number) => void;
  onEmitTestSignal: () => void;
  userEmail: string | null;
  onLogout: () => void;
}

// Logo CASH LOGO.svg en color corporativo
const CashLogoIcon: React.FC<{ className?: string }> = ({ className = "w-6 h-6" }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <g id="cash">
      <path d="M21,10.77V6c0-1.37-2.85-2-5.5-2a15,15,0,0,0-2.5.2V4c0-1.37-2.85-2-5.5-2S2,2.63,2,4V19c0,1.37,2.85,2,5.5,2a14.7,14.7,0,0,0,2.83-.27A7.49,7.49,0,0,0,21,10.77ZM17.89,7.82A7.34,7.34,0,0,0,20,7.21V9.42A7.55,7.55,0,0,0,17.89,7.82ZM7.5,6A10.93,10.93,0,0,0,12,5.21V7c-.08.28-1.58,1-4.5,1S3.08,7.27,3,7V5.21A10.93,10.93,0,0,0,7.5,6Zm-.06,6A6.91,6.91,0,0,0,7,14c-2.6-.08-3.95-.73-4-1V11.21A11,11,0,0,0,7.44,12ZM3,16V14.21A10.22,10.22,0,0,0,7,15a7.49,7.49,0,0,0,.42,2C4.56,17,3.08,16.27,3,16Zm4.88-5H7.5c-2.92,0-4.42-.73-4.5-1V8.21A10.93,10.93,0,0,0,7.5,9a15.5,15.5,0,0,0,2.06-.13A7.53,7.53,0,0,0,7.88,11ZM15.5,5c2.93,0,4.43.73,4.5,1s-1.57,1-4.5,1A14.59,14.59,0,0,1,13,6.79V5.21A14.59,14.59,0,0,1,15.5,5Zm-8-2c2.9,0,4.4.72,4.5,1-.1.27-1.5.94-4.19,1H7.5C4.58,5,3.08,4.27,3,4H3C3.08,3.73,4.58,3,7.5,3Zm0,17c-2.92,0-4.42-.73-4.5-1V17.21A10.93,10.93,0,0,0,7.5,18h.37a7.5,7.5,0,0,0,1.42,1.89A14.67,14.67,0,0,1,7.5,20Zm7,1A6.5,6.5,0,1,1,21,14.5,6.51,6.51,0,0,1,14.5,21Z"/>
      <path d="M15,14v-2.3a1.29,1.29,0,0,1,1,.88.5.5,0,0,0,1-.24A2.38,2.38,0,0,0,15,10.72V10.5a.5.5,0,0,0-1,0v.21a2.27,2.27,0,0,0-2,2.12,2.31,2.31,0,0,0,.05.46A2.39,2.39,0,0,0,14,15v2.31a1.29,1.29,0,0,1-1-.88.5.5,0,1,0-1,.24A2.36,2.36,0,0,0,14,18.28v.22a.5.5,0,0,0,1,0v-.22A2.36,2.36,0,0,0,17,16.61a2.28,2.28,0,0,0,.05-.44A2.28,2.28,0,0,0,15,14Zm-2-1a.78.78,0,0,1,0-.22,1.23,1.23,0,0,1,1-1.09v2.19A1.3,1.3,0,0,1,13,13.05ZM16,16.38a1.29,1.29,0,0,1-1,.88V15.07a1.23,1.23,0,0,1,1,1.1A.82.82,0,0,1,16,16.38Z"/>
    </g>
  </svg>
);

// KILL SWITCH.svg dinámico estilo interruptor mecánico deslizante
const KillSwitchToggle: React.FC<{
  isOn: boolean;
  onClick: () => void;
}> = ({ isOn, onClick }) => {
  return (
    <button
      onClick={onClick}
      title={isOn ? "KILL SWITCH: Pulsa para apagar bot y cerrar todas las posiciones" : "Bot Apagado / Modo Emergencia Activo"}
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
              <span className={`w-1.5 h-1.5 rounded-full ${isIngestionActive ? 'bg-primary animate-pulse' : 'bg-error'}`} />
              <span className="text-[9px] font-mono text-text-secondary">
                {isIngestionActive ? 'EN VIVO' : 'PAUSADO'}
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

          {/* Interruptor Dinámico KILL SWITCH con KILL SWITCH.svg */}
          <KillSwitchToggle
            isOn={isIngestionActive && isAutoExecutionActive}
            onClick={() => setShowKillSwitchConfirm(true)}
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
        auditLogs={[]}
        tradeHistory={[]}
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
