import React, { useState, useRef, useEffect } from 'react';
import { PositionMatrix, type SlotTradeData } from './PositionMatrix';
import { SignalFeed, type TradeLifecycleCardItem } from './SignalFeed';
import { NewsFeed } from './NewsFeed';
import { ControlDropdown } from './ControlDropdown';
import { AuditLogsModal } from './AuditLogsModal';
import { SystemHealthModal } from './SystemHealthModal';

interface MobileOperatorDashboardProps {
  balance: number;
  floatingPnl: number;
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
  floatingPnl,
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
  const isProfit = floatingPnl >= 0;

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

        {/* Acciones Rápidas: KILL SWITCH ROJO & Menú */}
        <div className="flex items-center gap-2">
          {/* Botón Kill Switch de Pánico */}
          <button
            onClick={() => setShowKillSwitchConfirm(true)}
            className="flex items-center gap-1 bg-error hover:bg-red-700 text-white font-mono font-bold text-[11px] px-2.5 py-1.5 rounded border border-red-400/50 shadow-sm active:scale-95 transition-transform"
          >
            <span className="w-2 h-2 rounded-full bg-white animate-ping" />
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

      {/* 2. Barra de Estado Resumido (Balance, PnL y Precio XAUUSD) */}
      <div className="bg-surface-container px-3 py-1.5 border-b border-outline-variant flex items-center justify-between font-mono text-xs shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] text-text-secondary">BAL:</span>
          <span className="font-bold text-text-primary">${balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
        </div>

        <div className="flex items-center gap-1.5">
          <span className="text-[10px] text-text-secondary">FLOTANTE:</span>
          <span className={`font-bold ${isProfit ? 'text-primary' : 'text-error'}`}>
            {isProfit ? '+' : ''}${floatingPnl.toFixed(2)}
          </span>
        </div>

        <div className="flex items-center gap-1 text-[10px] text-text-secondary bg-surface px-1.5 py-0.5 rounded border border-outline-variant">
          <span>ORO:</span>
          <span className="text-primary font-bold">${currentPrice > 0 ? currentPrice.toFixed(2) : '4,647.74'}</span>
        </div>
      </div>

      {/* 3. Área de Contenido con Deslizamiento Táctil (Swipe Carousel) */}
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

      {/* 4. Barra de Navegación Táctil Inferior (Bottom Touch Nav) */}
      <nav className="h-14 border-t border-outline-variant bg-surface px-2 grid grid-cols-3 items-center shrink-0 z-30 shadow-lg">
        {/* Pestaña 0: Señales */}
        <button
          onClick={() => setActiveTab(0)}
          className={`flex flex-col items-center justify-center py-1 gap-0.5 transition-colors ${
            activeTab === 0 ? 'text-primary font-bold' : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <span className="text-base">📋</span>
          <span className="text-[10px] font-mono tracking-tight">Señales</span>
        </button>

        {/* Pestaña 1: Posiciones (Home) */}
        <button
          onClick={() => setActiveTab(1)}
          className={`relative flex flex-col items-center justify-center py-1 gap-0.5 transition-colors ${
            activeTab === 1 ? 'text-primary font-bold' : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          {activeSlotsCount > 0 && (
            <span className="absolute top-1 right-6 w-4 h-4 bg-primary text-black font-bold text-[9px] rounded-full flex items-center justify-center font-mono">
              {activeSlotsCount}
            </span>
          )}
          <span className="text-base">🔲</span>
          <span className="text-[10px] font-mono tracking-tight">Posiciones</span>
        </button>

        {/* Pestaña 2: Noticias */}
        <button
          onClick={() => setActiveTab(2)}
          className={`flex flex-col items-center justify-center py-1 gap-0.5 transition-colors ${
            activeTab === 2 ? 'text-primary font-bold' : 'text-text-secondary hover:text-text-primary'
          }`}
        >
          <span className="text-base">📰</span>
          <span className="text-[10px] font-mono tracking-tight">Noticias IA</span>
        </button>
      </nav>

      {/* Modal de Confirmación de Kill Switch Inmediato */}
      {showKillSwitchConfirm && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-surface-container-highest border border-error/50 rounded-lg p-4 max-w-xs w-full shadow-2xl flex flex-col gap-3 font-mono text-center animate-in zoom-in-95">
            <div className="w-12 h-12 rounded-full bg-error/20 border border-error flex items-center justify-center mx-auto text-xl text-error">
              ⚠️
            </div>
            <div className="text-sm font-bold text-text-primary">
              ¿EJECUTAR KILL SWITCH?
            </div>
            <p className="text-[11px] text-text-secondary leading-snug">
              Se enviará una orden de cierre de mercado inmediato a todos los slots activos ({activeSlotsCount}) y se pausará el motor.
            </p>
            <div className="grid grid-cols-2 gap-2 pt-1">
              <button
                onClick={() => setShowKillSwitchConfirm(false)}
                className="px-3 py-2 rounded bg-surface-container text-text-secondary hover:bg-surface-container-high text-xs font-semibold"
              >
                Cancelar
              </button>
              <button
                onClick={() => {
                  onEmergencyClose();
                  setShowKillSwitchConfirm(false);
                }}
                className="px-3 py-2 rounded bg-error hover:bg-red-700 text-white text-xs font-bold shadow-lg"
              >
                CONFIRMAR
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modales de Soporte */}
      <AuditLogsModal isOpen={showAuditModal} onClose={() => setShowAuditModal(false)} />
      <SystemHealthModal isOpen={showHealthModal} onClose={() => setShowHealthModal(false)} />
    </div>
  );
};
