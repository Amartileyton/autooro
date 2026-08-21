import React from 'react';

interface ControlModalProps {
  isOpen: boolean;
  onClose: () => void;
  ingestionEnabled: boolean;
  autoExecutionEnabled: boolean;
  onToggleIngestion: () => void;
  onPanicClose: () => void;
  onInjectTestSignal: () => void;
}

export const ControlModal: React.FC<ControlModalProps> = ({
  isOpen,
  onClose,
  ingestionEnabled,
  autoExecutionEnabled,
  onToggleIngestion,
  onPanicClose,
  onInjectTestSignal,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-[#12141c] border border-outline-variant rounded-lg w-full max-w-lg overflow-hidden shadow-2xl flex flex-col">
        {/* Header */}
        <div className="bg-surface-container-highest px-4 py-3 border-b border-outline-variant flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-amber-gold">settings</span>
            <h2 className="text-headline-sm font-bold text-on-surface tracking-tight">
              PANEL DE CONTROL &amp; CONFIGURACIÓN
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-on-surface-variant hover:text-on-surface p-1 rounded hover:bg-surface-container transition-colors"
          >
            <span className="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-6">
          {/* 1. Switches de Control */}
          <div className="space-y-3">
            <h3 className="text-label-sm uppercase tracking-wider text-outline font-bold">
              ESTADO DE EJECUCIÓN
            </h3>

            {/* Ingesta Telegram */}
            <div className="flex items-center justify-between p-3 rounded bg-surface border border-outline-variant">
              <div>
                <div className="text-data-sm font-bold text-on-surface flex items-center gap-2">
                  <span className="material-symbols-outlined text-[18px] text-primary">cell_tower</span>
                  Ingesta de Canales de Telegram
                </div>
                <div className="text-[12px] text-outline mt-0.5">
                  Escucha continua en tiempo real de canales configurados
                </div>
              </div>
              <button
                onClick={onToggleIngestion}
                className={`px-3 py-1.5 rounded font-mono text-label-sm font-bold border transition-colors ${
                  ingestionEnabled
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40 hover:bg-emerald-500/30'
                    : 'bg-error-container/20 text-error border-error/40 hover:bg-error-container/30'
                }`}
              >
                {ingestionEnabled ? 'ACTIVA (ON)' : 'PAUSADA (OFF)'}
              </button>
            </div>

            {/* Auto-Ejecución */}
            <div className="flex items-center justify-between p-3 rounded bg-surface border border-outline-variant">
              <div>
                <div className="text-data-sm font-bold text-on-surface flex items-center gap-2">
                  <span className="material-symbols-outlined text-[18px] text-primary">smart_toy</span>
                  Ejecución Automática de Órdenes
                </div>
                <div className="text-[12px] text-outline mt-0.5">
                  Apertura y gestión automática de slots de capital (25%)
                </div>
              </div>
              <span className="px-3 py-1.5 rounded font-mono text-label-sm font-bold border bg-emerald-500/20 text-emerald-400 border-emerald-500/40">
                HABILITADA
              </span>
            </div>
          </div>

          {/* 2. Diagnóstico y Pruebas */}
          <div className="space-y-3">
            <h3 className="text-label-sm uppercase tracking-wider text-outline font-bold">
              DIAGNÓSTICO Y PRUEBAS
            </h3>
            <button
              onClick={() => {
                onInjectTestSignal();
                onClose();
              }}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-surface hover:bg-surface-container-high border border-outline-variant text-on-surface font-mono text-label-sm font-bold rounded transition-colors"
            >
              <span className="material-symbols-outlined text-[18px] text-amber-gold">send</span>
              Inyectar Señal de Prueba (BUY XAUUSD)
            </button>
          </div>

          {/* 3. Panic Stop / Kill Switch */}
          <div className="space-y-2 pt-2 border-t border-outline-variant">
            <h3 className="text-label-sm uppercase tracking-wider text-error font-bold flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">dangerous</span>
              ZONA DE EMERGENCIA
            </h3>
            <p className="text-[12px] text-outline">
              Cierra inmediatamente todas las posiciones abiertas en el broker y detiene la ingesta de nuevas señales.
            </p>
            <button
              onClick={() => {
                if (window.confirm('¿Confirmas el cierre inmediato de todas las posiciones activas (KILL-SWITCH)?')) {
                  onPanicClose();
                  onClose();
                }
              }}
              className="w-full py-3 px-4 bg-crimson-red hover:bg-crimson-red/80 text-white font-mono font-bold text-data-sm rounded border border-red-400/50 shadow-lg transition-all flex items-center justify-center gap-2"
            >
              <span className="material-symbols-outlined text-[20px]">power_settings_new</span>
              PANIC STOP — KILL SWITCH
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-surface-container-highest px-4 py-2 border-t border-outline-variant flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-surface hover:bg-surface-container border border-outline-variant text-label-sm rounded font-bold text-on-surface transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
