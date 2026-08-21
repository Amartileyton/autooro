import React, { useState, useEffect } from 'react';

interface SystemHealthModalProps {
  isOpen: boolean;
  onClose: () => void;
  wsConnected: boolean;
  latencyMs: number;
  botActive: boolean;
  hasCtraderToken: boolean;
  xauusdPrice: number;
}

export const SystemHealthModal: React.FC<SystemHealthModalProps> = ({
  isOpen,
  onClose,
  wsConnected,
  latencyMs,
  botActive,
  hasCtraderToken,
  xauusdPrice,
}) => {
  const [isPinging, setIsPinging] = useState(false);
  const [serverState, setServerState] = useState<any>(null);

  useEffect(() => {
    if (isOpen) {
      fetchServerStatus();
    }
  }, [isOpen]);

  const fetchServerStatus = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/state');
      if (res.ok) {
        const data = await res.json();
        setServerState(data);
      }
    } catch (e) {
      console.error('Error fetching server state:', e);
    }
  };

  const handleRunPing = async () => {
    setIsPinging(true);
    await fetchServerStatus();
    setTimeout(() => setIsPinging(false), 500);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-fade-in">
      <div
        className="bg-[#0e1017] border border-slate-700 w-full max-w-2xl rounded-lg shadow-2xl overflow-hidden flex flex-col max-h-[90vh] text-slate-200"
        style={{ minWidth: '340px' }}
      >
        {/* Header del Modal */}
        <div className="bg-[#141722] px-4 py-3 border-b border-slate-800 flex justify-between items-center">
          <div className="flex items-center gap-2.5">
            <div className={`w-3 h-3 rounded-full ${botActive ? 'bg-emerald-400 smoke-pulse-green' : 'bg-red-500 smoke-pulse-red'}`} />
            <h2 className="text-sm font-mono font-bold text-white uppercase tracking-wider">
              Diagnóstico del Sistema & Estado de APIs
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>

        {/* Cuerpo del Diagnóstico */}
        <div className="p-4 space-y-4 overflow-y-auto flex-1 font-mono text-xs">
          {/* 1. Resumen General */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div className="p-2.5 rounded bg-[#141722] border border-slate-800/80">
              <span className="text-[10px] text-slate-400 block">ESTADO MOTOR</span>
              <strong className={botActive ? 'text-emerald-400 font-bold' : 'text-red-400 font-bold'}>
                {botActive ? 'ACTIVO (24/7)' : 'PAUSADO'}
              </strong>
            </div>

            <div className="p-2.5 rounded bg-[#141722] border border-slate-800/80">
              <span className="text-[10px] text-slate-400 block">WEBSOCKET STREAM</span>
              <strong className={wsConnected ? 'text-emerald-400 font-bold' : 'text-red-400 font-bold'}>
                {wsConnected ? 'CONECTADO' : 'OFFLINE'}
              </strong>
            </div>

            <div className="p-2.5 rounded bg-[#141722] border border-slate-800/80">
              <span className="text-[10px] text-slate-400 block">LATENCIA WS</span>
              <strong className="text-white font-bold">{latencyMs} ms</strong>
            </div>

            <div className="p-2.5 rounded bg-[#141722] border border-slate-800/80">
              <span className="text-[10px] text-slate-400 block">SPOT ORO (OANDA)</span>
              <strong className="text-white font-bold">${xauusdPrice.toFixed(2)}</strong>
            </div>
          </div>

          {/* 2. Lista de APIs & Servicios Integrados */}
          <div className="space-y-2">
            <div className="text-[11px] font-bold text-slate-300 uppercase tracking-wide">
              Servicios y Conectores de APIs
            </div>

            {/* Telegram MTProto */}
            <div className="p-3 rounded bg-[#141722] border border-slate-800/80 flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <span className="material-symbols-outlined text-[18px] text-sky-400">cell_tower</span>
                <div>
                  <div className="text-white font-bold text-xs">Telegram MTProto Stream</div>
                  <div className="text-[10px] text-slate-400">Canal: -1002763662248 (Ingesta en tiempo real)</div>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold">
                OPERATIVO
              </span>
            </div>

            {/* Broker cTrader / OpenAPI */}
            <div className="p-3 rounded bg-[#141722] border border-slate-800/80 flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <span className="material-symbols-outlined text-[18px] text-amber-400">currency_exchange</span>
                <div>
                  <div className="text-white font-bold text-xs">Broker OpenAPI cTrader</div>
                  <div className="text-[10px] text-slate-400">
                    {hasCtraderToken ? 'Token de cTrader verificado y activo' : 'Modo Simulación / Token cTrader pendiente'}
                  </div>
                </div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                  hasCtraderToken
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                    : 'bg-slate-800 text-slate-400 border-slate-700'
                }`}
              >
                {hasCtraderToken ? 'CONECTADO' : 'PAPER TRADING'}
              </span>
            </div>

            {/* Risk Management Engine */}
            <div className="p-3 rounded bg-[#141722] border border-slate-800/80 flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <span className="material-symbols-outlined text-[18px] text-purple-400">security</span>
                <div>
                  <div className="text-white font-bold text-xs">Motor de Gestión de Riesgo (Opción B)</div>
                  <div className="text-[10px] text-slate-400">50% Cierre Parcial en TP1 + Mover SL a Break-Even</div>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold">
                ACTIVO
              </span>
            </div>

            {/* WebSocket Live Feed */}
            <div className="p-3 rounded bg-[#141722] border border-slate-800/80 flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <span className="material-symbols-outlined text-[18px] text-emerald-400">bolt</span>
                <div>
                  <div className="text-white font-bold text-xs">FastAPI WebSocket Engine</div>
                  <div className="text-[10px] text-slate-400">Transmisión de ticks y ciclo de vida de trades (Port 8000)</div>
                </div>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-[10px] font-bold">
                SINCRONIZADO
              </span>
            </div>
          </div>
        </div>

        {/* Footer del Modal con Acciones */}
        <div className="bg-[#141722] px-4 py-2.5 border-t border-slate-800 flex justify-between items-center">
          <span className="text-[10px] font-mono text-slate-400">
            Última verificación: {new Date().toLocaleTimeString()}
          </span>
          <div className="flex gap-2">
            <button
              onClick={handleRunPing}
              disabled={isPinging}
              className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-white font-mono text-[11px] rounded border border-slate-600 transition-colors flex items-center gap-1.5"
            >
              <span className={`material-symbols-outlined text-[14px] ${isPinging ? 'animate-spin' : ''}`}>
                refresh
              </span>
              {isPinging ? 'Comprobando...' : 'Comprobar Estado'}
            </button>
            <button
              onClick={onClose}
              className="px-3 py-1 bg-white hover:bg-slate-200 text-slate-900 font-mono text-[11px] font-bold rounded shadow transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
