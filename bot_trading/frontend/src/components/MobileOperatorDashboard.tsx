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

  const activeSlotsCount = slots.filter((s) => s.is_active).length;

  return (
    <div className="flex flex-col h-screen w-screen bg-background text-text-primary overflow-hidden select-none">
      {/* 1. Header Táctil Móvil */}
      <header className="h-14 border-b border-outline-variant bg-surface px-3 flex items-center justify-between shrink-0 z-30 shadow-md">
        {/* Logo & Estado del Motor */}
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded bg-primary/10 border border-primary/30 flex items-center justify-center font-mono font-bold text-primary text-xs">
            GX
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

          {/* Botón Kill Switch de Pánico */}
          <button
            onClick={() => setShowKillSwitchConfirm(true)}
            className="flex items-center gap-1 bg-error hover:bg-red-700 text-white font-mono font-bold text-[11px] px-2.5 py-1.5 rounded border border-red-400/50 shadow-sm active:scale-95 transition-transform"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-white animate-ping" />
            <span>KILL SWITCH</span>
          </button>

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
