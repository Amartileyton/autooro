import React, { useEffect, useRef } from 'react';

interface ControlDropdownProps {
  isOpen: boolean;
  onClose: () => void;
  ingestionEnabled: boolean;
  autoExecutionEnabled: boolean;
  onToggleIngestion: () => void;
  onToggleAutoExecution: () => void;
  onPanicClose: () => void;
  onInjectTestSignal: () => void;
  onOpenAudit?: () => void;
}

export const ControlDropdown: React.FC<ControlDropdownProps> = ({
  isOpen,
  onClose,
  ingestionEnabled,
  autoExecutionEnabled,
  onToggleIngestion,
  onToggleAutoExecution,
  onPanicClose,
  onInjectTestSignal,
  onOpenAudit,
}) => {
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={dropdownRef}
      className="absolute right-4 top-12 w-88 bg-[#12141c] border border-outline-variant rounded-md shadow-2xl z-50 p-3.5 space-y-3 animate-fade-in text-on-surface"
      style={{ minWidth: '320px' }}
    >
      {/* Header del Dropdown */}
      <div className="flex justify-between items-center pb-2 border-b border-outline-variant/60">
        <span className="text-label-sm font-bold uppercase tracking-wider text-slate-200 flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-slate-400">tune</span>
          Controles del Sistema
        </span>
        <button
          onClick={onClose}
          className="text-outline hover:text-on-surface p-0.5 rounded transition-colors"
        >
          <span className="material-symbols-outlined text-[16px]">close</span>
        </button>
      </div>

      {/* 1. Ingestión de Señales Telegram */}
      <div className="flex justify-between items-center p-2 rounded bg-surface border border-outline-variant/40">
        <div>
          <div className="text-[11px] font-bold text-on-surface">Escucha Telegram</div>
          <div className="text-[10px] text-outline">Recepción MTProto de canales</div>
        </div>
        <button
          onClick={onToggleIngestion}
          className={`px-2.5 py-1 rounded text-[10px] font-mono font-bold transition-all border ${
            ingestionEnabled
              ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
              : 'bg-error-container/20 text-error border-error/40'
          }`}
        >
          {ingestionEnabled ? 'ACTIVA (ON)' : 'PAUSADA (OFF)'}
        </button>
      </div>

      {/* 2. Auto-Ejecución */}
      <div className="flex justify-between items-center p-2 rounded bg-surface border border-outline-variant/40">
        <div>
          <div className="text-[11px] font-bold text-on-surface">Auto-Ejecución</div>
          <div className="text-[10px] text-outline">Apertura automática de órdenes</div>
        </div>
        <button
          onClick={onToggleAutoExecution}
          className={`px-2.5 py-1 rounded text-[10px] font-mono font-bold transition-all border ${
            autoExecutionEnabled
              ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
              : 'bg-error-container/20 text-error border-error/40'
          }`}
        >
          {autoExecutionEnabled ? 'ACTIVA (ON)' : 'PAUSADA (OFF)'}
        </button>
      </div>

      {/* 3. Inyección de Prueba y Auditoría */}
      <div className="space-y-1.5">
        <button
          onClick={() => {
            onInjectTestSignal();
            onClose();
          }}
          className="w-full flex items-center justify-center gap-2 py-1.5 px-3 bg-surface hover:bg-surface-container-high border border-outline-variant text-[11px] font-mono font-bold rounded text-slate-200 transition-colors"
        >
          <span className="material-symbols-outlined text-[15px] text-slate-400">send</span>
          Inyectar Señal de Test (BUY XAUUSD)
        </button>

        {onOpenAudit && (
          <button
            onClick={() => {
              onOpenAudit();
              onClose();
            }}
            className="w-full flex items-center justify-center gap-2 py-1.5 px-3 bg-surface hover:bg-surface-container-high border border-outline-variant text-[11px] font-mono font-medium rounded text-slate-300 transition-colors"
          >
            <span className="material-symbols-outlined text-[15px] text-slate-400">receipt_long</span>
            Ver Registro de Auditoría y Logs
          </button>
        )}
      </div>

      {/* 4. Kill Switch Panic Stop */}
      <div className="pt-2 border-t border-outline-variant/60">
        <button
          onClick={() => {
            if (window.confirm('¿Confirmas el cierre inmediato de todas las posiciones (KILL-SWITCH)?')) {
              onPanicClose();
              onClose();
            }
          }}
          className="w-full py-2.5 px-3 bg-crimson-red hover:bg-crimson-red/80 text-white font-mono font-bold text-[11px] rounded border border-red-400/50 shadow transition-all flex items-center justify-center gap-2"
        >
          <span className="material-symbols-outlined text-[16px]">power_settings_new</span>
          PANIC STOP (KILL SWITCH)
        </button>
      </div>
    </div>
  );
};
