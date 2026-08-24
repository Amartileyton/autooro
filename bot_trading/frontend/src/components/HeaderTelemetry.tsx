import React, { useState, useRef, useEffect } from 'react';
import { MarketTicker } from './MarketTicker';

interface HeaderTelemetryProps {
  xauusdPrice: number;
  balance?: number | null;
  hasLiveBalance?: boolean;
  botActive: boolean;
  authUser?: { email: string; name?: string; picture?: string } | null;
  selectedTvSymbol?: string;
  onSelectAsset?: (asset: any) => void;
  onOpenSettings?: () => void;
  onOpenDiagnostics?: () => void;
  onLogout?: () => void;
}

export const HeaderTelemetry: React.FC<HeaderTelemetryProps> = ({
  xauusdPrice,
  balance,
  hasLiveBalance,
  botActive,
  authUser,
  selectedTvSymbol,
  onSelectAsset,
  onOpenSettings,
  onOpenDiagnostics,
  onLogout,
}) => {
  const [isUserMenuOpen, setIsUserMenuOpen] = useState<boolean>(false);
  const userMenuRef = useRef<HTMLDivElement>(null);

  // Cerrar el submenú si se hace clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setIsUserMenuOpen(false);
      }
    };
    if (isUserMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isUserMenuOpen]);

  return (
    <header className="flex items-center w-full px-4 h-12 bg-surface border-b border-outline-variant shrink-0 z-[100] relative">
      {/* 1. Bloque Izquierdo: LOGO */}
      <div className="flex items-center gap-2.5 shrink-0 h-full">
        {/* CASH LOGO.svg en Gris / Plata */}
        <svg className="w-5 h-5 fill-current text-slate-300 shrink-0" viewBox="0 0 32 32">
          <path d="M0 25v-18h32v18h-32zM2 8.938v14.062h28v-14.062h-28zM21 16c0-3.313-2.238-6-5-6h13v12h-13c2.762 0 5-2.687 5-6zM25 18c0.828 0 1.5-0.896 1.5-2s-0.672-2-1.5-2-1.5 0.896-1.5 2 0.672 2 1.5 2zM18.118 13.478c-0.015 0.055-0.036 0.094-0.062 0.119-0.027 0.025-0.063 0.037-0.109 0.037s-0.118-0.028-0.219-0.086c-0.1-0.059-0.223-0.121-0.368-0.189-0.146-0.068-0.314-0.13-0.506-0.187s-0.402-0.083-0.631-0.083c-0.18 0-0.336 0.021-0.469 0.065s-0.245 0.104-0.334 0.18c-0.090 0.077-0.156 0.17-0.2 0.277s-0.065 0.222-0.065 0.342c0 0.18 0.049 0.335 0.147 0.466s0.229 0.248 0.394 0.35c0.165 0.103 0.351 0.198 0.56 0.287 0.207 0.090 0.42 0.185 0.637 0.284 0.217 0.101 0.429 0.214 0.637 0.341s0.395 0.279 0.557 0.456 0.293 0.385 0.394 0.624c0.1 0.24 0.149 0.521 0.149 0.847 0 0.425-0.078 0.797-0.236 1.118s-0.373 0.588-0.645 0.802c-0.271 0.215-0.587 0.376-0.949 0.484-0.046 0.014-0.096 0.020-0.143 0.031v1.092h-0.983v-0.963c-0.013 0-0.024 0.002-0.036 0.002-0.279 0-0.539-0.022-0.778-0.067s-0.451-0.101-0.634-0.164c-0.184-0.064-0.336-0.131-0.459-0.201s-0.211-0.132-0.265-0.186c-0.054-0.054-0.093-0.132-0.116-0.234-0.023-0.103-0.035-0.249-0.035-0.441 0-0.129 0.004-0.237 0.013-0.325s0.022-0.158 0.041-0.213 0.043-0.093 0.075-0.116c0.031-0.022 0.067-0.034 0.109-0.034 0.058 0 0.14 0.034 0.247 0.103s0.243 0.145 0.409 0.228c0.167 0.084 0.365 0.159 0.597 0.229 0.231 0.068 0.499 0.103 0.803 0.103 0.2 0 0.379-0.024 0.537-0.072s0.293-0.115 0.403-0.203 0.194-0.196 0.253-0.325c0.059-0.13 0.088-0.273 0.088-0.433 0-0.183-0.051-0.34-0.15-0.472-0.1-0.131-0.23-0.247-0.391-0.35-0.16-0.102-0.342-0.197-0.546-0.287s-0.414-0.185-0.631-0.284c-0.216-0.1-0.427-0.213-0.631-0.341s-0.386-0.278-0.546-0.455c-0.16-0.177-0.291-0.387-0.39-0.628s-0.15-0.531-0.15-0.868c0-0.388 0.072-0.728 0.215-1.021s0.337-0.537 0.581-0.73 0.531-0.338 0.862-0.434c0.17-0.050 0.346-0.085 0.526-0.109v-1.034h0.983v1.034c0.039 0.005 0.078 0.003 0.117 0.009 0.191 0.029 0.371 0.068 0.537 0.118 0.167 0.049 0.314 0.104 0.444 0.167 0.129 0.062 0.214 0.113 0.256 0.155s0.069 0.076 0.085 0.105c0.014 0.029 0.026 0.068 0.037 0.116s0.018 0.108 0.021 0.182c0.004 0.072 0.006 0.163 0.006 0.271 0 0.121-0.003 0.224-0.009 0.308-0.009 0.079-0.019 0.149-0.034 0.203zM11 16c0 3.313 2.238 6 5 6h-13v-12h13c-2.762 0-5 2.687-5 6zM7 14c-0.829 0-1.5 0.896-1.5 2s0.671 2 1.5 2c0.828 0 1.5-0.896 1.5-2s-0.672-2-1.5-2z"/>
        </svg>
        <span className="text-headline-md font-bold text-slate-200 tracking-tight whitespace-nowrap leading-none">
          GOLD-EX TERMINAL
        </span>

        {/* Indicador de Punto con Dispersión de Humo */}
        <button
          onClick={onOpenDiagnostics}
          title={botActive ? "Bot Activo (24/7) — Clic para abrir Diagnóstico de APIs" : "Bot Pausado — Clic para abrir Diagnóstico de APIs"}
          className="relative flex items-center justify-center p-1 rounded-full hover:scale-125 transition-transform duration-200 cursor-pointer focus:outline-none"
        >
          <div
            className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${
              botActive
                ? 'bg-emerald-400 smoke-pulse-green'
                : 'bg-red-500 smoke-pulse-red'
            }`}
          />
        </button>
      </div>

      {/* Separador 1 */}
      <div className="h-4 w-px bg-outline-variant mx-3 shrink-0 self-center" />

      {/* 2. Bloque Balance */}
      <div className="hidden sm:flex items-center gap-2 shrink-0 h-full leading-none">
        <span className="text-label-sm text-slate-400 font-semibold tracking-wider leading-none">BALANCE</span>
        {balance !== null && balance !== undefined && hasLiveBalance ? (
          <span className="text-data-md font-mono font-bold text-slate-100 whitespace-nowrap leading-none">
            ${balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
        ) : (
          <span className="text-data-sm font-mono text-slate-400/80 italic tracking-tight whitespace-nowrap leading-none">
            No disponible
          </span>
        )}
      </div>

      {/* Separador 2 */}
      <div className="h-4 w-px bg-outline-variant mx-3 shrink-0 self-center" />

      {/* 3. Bloque Central: TICKER AMERICANO */}
      <div className="flex-1 min-w-0 h-full flex items-center overflow-hidden">
        <MarketTicker
          liveXauusdPrice={xauusdPrice}
          selectedTvSymbol={selectedTvSymbol}
          onSelectAsset={onSelectAsset}
        />
      </div>

      {/* Separador 3 */}
      <div className="h-4 w-px bg-outline-variant mx-3 shrink-0 self-center" />

      {/* 4. Bloque Derecho: OPERADOR Y CONTROLES */}
      <div className="flex items-center gap-3 shrink-0 h-full">
        {/* Burbuja de Perfil (Sin Nombre) */}
        <div className="relative flex items-center" ref={userMenuRef}>
          <button
            onClick={() => setIsUserMenuOpen((prev) => !prev)}
            title="Cuenta de Operador — Clic para opciones"
            className="relative w-8 h-8 rounded-full bg-[#1b1d28] border border-[#3a3d52] hover:border-amber-400 hover:ring-2 hover:ring-amber-500/30 active:scale-95 transition-all flex items-center justify-center overflow-hidden cursor-pointer shadow-md focus:outline-none"
          >
            {authUser?.picture ? (
              <img
                src={authUser.picture}
                alt="Avatar"
                className="w-full h-full object-cover rounded-full"
              />
            ) : (
              <span className="material-symbols-outlined text-[18px] text-amber-400">person</span>
            )}
          </button>

          {/* Submenú desplegable flotante */}
          {isUserMenuOpen && (
            <div className="absolute right-0 top-full mt-2 w-48 py-1.5 px-1.5 rounded-xl bg-[#14151e] border border-[#3b3d4f] shadow-[0_15px_35px_rgba(0,0,0,0.85)] backdrop-blur-2xl z-[9999] animate-fadeIn">
              <button
                onClick={() => {
                  setIsUserMenuOpen(false);
                  onLogout?.();
                }}
                className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-mono text-slate-200 hover:text-red-300 hover:bg-red-500/15 transition-all text-left group"
              >
                {/* Burbuja en rojo */}
                <span className="w-4 h-4 rounded-full bg-red-500/20 border border-red-500/50 flex items-center justify-center shrink-0 group-hover:bg-red-500/30 group-hover:border-red-500/80 transition-colors">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-500 shadow-sm shadow-red-500" />
                </span>
                <span className="font-semibold tracking-tight">Cerrar sesión</span>
              </button>
            </div>
          )}
        </div>

        <button 
          onClick={onOpenSettings}
          title="Configuración y Controles de Ejecución"
          className="text-slate-300 bg-surface-container hover:bg-surface-container-high hover:text-white border border-outline-variant transition-all px-2.5 py-1.5 rounded flex items-center gap-1.5 font-medium shadow-sm leading-none h-8"
        >
          <span className="material-symbols-outlined text-[18px]">settings</span>
          <span className="text-label-sm hidden sm:inline uppercase tracking-wider leading-none">Controles</span>
        </button>
      </div>
    </header>
  );
};



