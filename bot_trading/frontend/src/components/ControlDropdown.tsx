import React, { useEffect, useRef } from 'react';

interface ControlDropdownProps {
  isOpen: boolean;
  onClose: () => void;
  ingestionEnabled: boolean;
  autoExecutionEnabled: boolean;
  onToggleIngestion: () => void;
  onToggleAutoExecution: () => void;
  onRearmBot?: () => void;
  onPanicClose: () => void;
  onInjectTestSignal: () => void;
  onOpenAudit?: () => void;
}

// KILL SWITCH.svg dinámico estilo interruptor mecánico deslizante con soporte ON y OFF
const KillSwitchToggle: React.FC<{
  isOn: boolean;
  onClick: () => void;
}> = ({ isOn, onClick }) => {
  return (
    <button
      onClick={onClick}
      title={isOn ? "KILL SWITCH ACTIVO: Pulsa para apagar bot y cerrar todas las posiciones" : "BOT DETENIDO (OFF): Pulsa para reactivar operativa y reanudar escucha"}
      className="w-full flex items-center justify-between p-2.5 rounded-md bg-surface border border-outline-variant/60 hover:border-outline-variant transition-all cursor-pointer select-none group"
    >
      <div className="flex flex-col text-left leading-tight">
        <span className={`text-xs font-mono font-bold tracking-wider ${isOn ? 'text-emerald-400' : 'text-error'}`}>
          {isOn ? 'KILL SWITCH (EN VIVO)' : 'BOT PARADO (OFF)'}
        </span>
        <span className="text-[10px] font-mono text-outline opacity-80">
          {isOn ? 'Pulsa para parada de emergencia' : 'Pulsa para rearmar y encender'}
        </span>
      </div>

      <div className="w-12 h-6 relative shrink-0">
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
              filter={isOn ? "drop-shadow(0 0 6px rgba(23,171,19,0.9))" : "drop-shadow(0 0 6px rgba(239,68,68,0.9))"}
            />
          </g>
        </svg>
      </div>
    </button>
  );
};

export const ControlDropdown: React.FC<ControlDropdownProps> = ({
  isOpen,
  onClose,
  ingestionEnabled,
  autoExecutionEnabled,
  onToggleIngestion,
  onToggleAutoExecution,
  onRearmBot,
  onPanicClose,
  onInjectTestSignal,
  onOpenAudit,
}) => {
  const dropdownRef = useRef<HTMLDivElement>(null);
  const isBotFullyActive = ingestionEnabled && autoExecutionEnabled;

  const handleKillSwitchClick = () => {
    if (isBotFullyActive) {
      if (window.confirm('🚨 ¿Confirmas el cierre inmediato de todas las posiciones abiertas y el apagado general (KILL SWITCH)?')) {
        onPanicClose();
        onClose();
      }
    } else {
      if (onRearmBot) {
        onRearmBot();
      } else {
        if (!ingestionEnabled) onToggleIngestion();
        if (!autoExecutionEnabled) onToggleAutoExecution();
      }
      onClose();
    }
  };

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
      style={{ minWidth: '340px' }}
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

      {/* 1. Interruptor Maestro Kill Switch (ON / OFF) con SVG Corporativo */}
      <div className="p-1 rounded bg-surface-container border border-outline-variant/50">
        <KillSwitchToggle
          isOn={isBotFullyActive}
          onClick={handleKillSwitchClick}
        />
      </div>

      {/* 2. Ingestión de Señales Telegram */}
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

      {/* 3. Auto-Ejecución */}
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

      {/* 4. Radar de Noticias Macroeconómicas (Worker Horario 1h) */}
      <div className="flex justify-between items-center p-2 rounded bg-surface border border-outline-variant/40">
        <div>
          <div className="text-[11px] font-bold text-on-surface flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
            <span>Radar de Noticias Macro</span>
          </div>
          <div className="text-[10px] text-outline">Ciclo horario automático (3600s)</div>
        </div>
        <button
          onClick={async () => {
            try {
              const base = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1') ? 'http://127.0.0.1:8000' : window.location.origin;
              await fetch(`${base}/api/v1/news/refresh`, { method: 'POST' });
              window.dispatchEvent(new CustomEvent('news_refreshed'));
            } catch (e) {
              console.error(e);
            }
          }}
          title="Forzar actualización de titulares ahora"
          className="px-2 py-1 rounded text-[10px] font-mono font-bold bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 flex items-center gap-1 transition-colors"
        >
          <span className="material-symbols-outlined text-[13px]">refresh</span>
          ACTUALIZAR
        </button>
      </div>

      {/* 5. Inyección de Prueba y Auditoría */}
      <div className="space-y-1.5 pt-1">
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
    </div>
  );
};
