import React, { useState } from 'react';

interface ControlPanelProps {
  ingestionEnabled: boolean;
  autoExecutionEnabled: boolean;
  onToggleIngestion: () => Promise<void>;
  onPanicClose: () => Promise<void>;
  onInjectTestSignal: () => Promise<void>;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  ingestionEnabled,
  autoExecutionEnabled,
  onToggleIngestion,
  onPanicClose,
  onInjectTestSignal,
}) => {
  const [isConfirmingKill, setIsConfirmingKill] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleKillClick = async () => {
    if (!isConfirmingKill) {
      setIsConfirmingKill(true);
      setTimeout(() => setIsConfirmingKill(false), 4000); // 4 segundos para confirmar
      return;
    }

    setLoading(true);
    try {
      await onPanicClose();
      setIsConfirmingKill(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="term-panel h-full flex flex-col overflow-hidden">
      <div className="bg-surface-container-highest px-3 py-1.5 border-b term-border flex justify-between items-center">
        <h2 className="text-label-sm text-outline uppercase tracking-widest">Controles de Ejecución</h2>
      </div>

      <div className="flex-1 p-3 flex flex-col md:flex-row gap-4 justify-between items-center">
        {/* Toggles de Ingesta y Auto-ejecución */}
        <div className="flex gap-6 border term-border p-3 w-full md:w-auto h-full items-center justify-center bg-surface rounded-sm">
          {/* Switch Ingesta */}
          <div className="flex flex-col items-center gap-1.5">
            <span className="text-label-sm text-outline">INGESTA TELEGRAM</span>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={ingestionEnabled}
                onChange={onToggleIngestion}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-surface-container-highest peer-focus:outline-none border term-border rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-outline after:border-outline after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-green/20 peer-checked:after:bg-emerald-green peer-checked:border-emerald-green" />
            </label>
            <span className={`text-data-sm font-mono font-bold ${ingestionEnabled ? 'text-emerald-green' : 'text-error'}`}>
              {ingestionEnabled ? 'ACTIVA' : 'PAUSADA'}
            </span>
          </div>

          <div className="w-px h-full bg-outline-variant" />

          {/* Switch Auto-Ejecución */}
          <div className="flex flex-col items-center gap-1.5">
            <span className="text-label-sm text-outline">AUTO-EJECUCIÓN</span>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={autoExecutionEnabled}
                readOnly
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-surface-container-highest peer-focus:outline-none border term-border rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-outline after:border-outline after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-green/20 peer-checked:after:bg-emerald-green peer-checked:border-emerald-green" />
            </label>
            <span className={`text-data-sm font-mono font-bold ${autoExecutionEnabled ? 'text-emerald-green' : 'text-error'}`}>
              {autoExecutionEnabled ? 'ACTIVA' : 'PAUSADA'}
            </span>
          </div>

          <div className="w-px h-full bg-outline-variant" />

          {/* Botón de Test Manual */}
          <button
            onClick={onInjectTestSignal}
            className="px-3 py-1.5 border border-primary/40 bg-primary/10 hover:bg-primary/20 text-primary text-label-sm font-bold rounded-sm transition-all"
            title="Inyecta una señal BUY simulada de prueba"
          >
            + SEÑAL TEST
          </button>
        </div>

        {/* Botón de Pánico KILL-SWITCH */}
        <div className="flex-1 flex justify-end h-full w-full md:w-auto">
          <button
            onClick={handleKillClick}
            disabled={loading}
            className={`h-full px-8 bg-[#12131a] border-4 ${
              isConfirmingKill ? 'border-amber-gold bg-amber-gold/20 text-amber-gold animate-pulse' : 'border-crimson-red text-crimson-red'
            } font-bold text-headline-md tracking-wider hover:bg-crimson-red hover:text-white transition-all flex items-center justify-center gap-3 relative overflow-hidden group rounded-sm`}
          >
            <span className="material-symbols-outlined text-[28px] relative z-10">power_settings_new</span>
            <span className="relative z-10">
              {loading
                ? 'CERRANDO POSICIONES...'
                : isConfirmingKill
                ? '¿CONFIRMAR CIERRE TOTAL?'
                : 'CERRAR TODO (KILL-SWITCH)'}
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};
