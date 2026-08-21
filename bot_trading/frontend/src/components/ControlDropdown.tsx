import React, { useEffect, useRef } from 'react';

interface ControlDropdownProps {
  isOpen: boolean;
  onClose: () => void;
  ingestionEnabled: boolean;
  autoExecutionEnabled: boolean;
  onToggleIngestion: () => void;
  onPanicClose: () => void;
  onInjectTestSignal: () => void;
}

export const ControlDropdown: React.FC<ControlDropdownProps> = ({
  isOpen,
  onClose,
  ingestionEnabled,
  autoExecutionEnabled,
  onToggleIngestion,
  onPanicClose,
  onInjectTestSignal,
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
      className="absolute right-3 top-12 w-80 bg-[#12141c] border border-outline-variant rounded-md shadow-2xl z-50 p-3 space-y-3 animate-fade-in text-on-surface"
    >
      {/* Header del Dropdown */}
      <div className="flex justify-between items-center pb-2 border-b border-outline-variant/60">
        <span className="text-label-sm font-bold uppercase tracking-wider text-amber-gold flex items-center gap-1">
          <span className="material-symbols-outlined text-[16px]">tune</span>
          Controles Rápidos
        </span>
        <button
          onClick={onClose}
          className="text-outline hover:text-on-surface p-0.5 rounded transition-colors"
        >
          <span className="material-symbols-outlined text-[16px]">close</span>
        </button>
      </div>

      {/* Switch Ingesta */}
      <div className="flex items-center justify-between p-2 rounded bg-surface border border-outline-variant/50">
        <div>
          <div className="text-[12px] font-bold">Ingesta Telegram</div>
          <div className="text-[10px] text-outline">Captura de canales</div>
        </div>
        <button
          onClick={onToggleIngestion}
          className={`px-2.5 py-1 text-[11px] font-mono font-bold rounded border transition-colors ${
            ingestionEnabled
              ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40 hover:bg-emerald-500/30'
              : 'bg-error-container/20 text-error border-error/40 hover:bg-error-container/30'
          }`}
        >
          {ingestionEnabled ? 'ACTIVA' : 'PAUSADA'}
        </button>
      </div>

      {/* Inyección de Prueba */}
      <button
        onClick={() => {
          onInjectTestSignal();
          onClose();
        }}
        className="w-full flex items-center justify-center gap-1.5 py-2 px-3 bg-surface hover:bg-surface-container-high border border-outline-variant text-[11px] font-mono rounded text-on-surface transition-colors"
      >
        <span className="material-symbols-outlined text-[16px] text-amber-gold">send</span>
        Inyectar Señal de Prueba
      </button>

      {/* Kill Switch Panic Stop */}
      <div className="pt-2 border-t border-outline-variant/60">
        <button
          onClick={() => {
            if (window.confirm('¿Confirmas el cierre inmediato de todas las posiciones (KILL-SWITCH)?')) {
              onPanicClose();
              onClose();
            }
          }}
          className="w-full py-2 px-3 bg-crimson-red hover:bg-crimson-red/80 text-white font-mono font-bold text-[11px] rounded border border-red-400/50 shadow transition-all flex items-center justify-center gap-1.5"
        >
          <span className="material-symbols-outlined text-[16px]">power_settings_new</span>
          PANIC STOP (KILL SWITCH)
        </button>
      </div>
    </div>
  );
};
