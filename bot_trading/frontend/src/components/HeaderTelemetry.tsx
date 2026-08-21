import React from 'react';

interface TelemetryProps {
  xauusdPrice: number;
  balance: number;
  floatingPnl: number;
  botActive: boolean;
  onOpenSettings?: () => void;
}

export const HeaderTelemetry: React.FC<TelemetryProps> = ({
  xauusdPrice,
  balance,
  floatingPnl,
  botActive,
  onOpenSettings,
}) => {
  const isProfit = floatingPnl >= 0;
  const pnlSign = isProfit ? '+' : '';

  return (
    <header className="flex justify-between items-center w-full px-4 h-12 bg-surface border-b border-outline-variant shrink-0 z-10 relative">
      <div className="flex items-center gap-4">
        <div className="text-headline-md font-bold text-primary tracking-tighter flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">terminal</span>
          GOLD-EX TERMINAL
        </div>

        {/* Telemetría en tiempo real */}
        <div className="hidden lg:flex items-center gap-6 ml-8 pl-8 border-l border-outline-variant">
          <div className="flex items-center gap-2">
            <span className="text-label-sm text-outline">XAUUSD SPOT</span>
            <span className="text-data-md font-mono text-amber-gold pulse-live font-semibold">
              ${xauusdPrice.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-label-sm text-outline">BALANCE</span>
            <span className="text-data-md font-mono font-semibold text-on-surface">
              ${balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-label-sm text-outline">PNL FLOTANTE</span>
            <span className={`text-data-md font-mono font-semibold ${isProfit ? 'text-profit' : 'text-loss'}`}>
              {pnlSign}${floatingPnl.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>

          <div className={`flex items-center gap-2 px-2 py-0.5 rounded border ${
            botActive 
              ? 'bg-emerald-green/20 border-emerald-green/50 glow-green' 
              : 'bg-error-container/20 border-error/50'
          }`}>
            <div className={`w-1.5 h-1.5 rounded-full ${botActive ? 'bg-emerald-green animate-pulse' : 'bg-error'}`} />
            <span className={`text-label-sm font-bold ${botActive ? 'text-emerald-green' : 'text-error'}`}>
              {botActive ? 'BOT ACTIVO' : 'PAUSADO'}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button 
          onClick={onOpenSettings}
          title="Configuración y Controles de Ejecución"
          className="text-on-surface-variant hover:text-primary hover:bg-surface-container-high transition-colors p-1.5 rounded flex items-center gap-1 border border-transparent hover:border-outline-variant"
        >
          <span className="material-symbols-outlined text-[20px]">settings</span>
          <span className="text-label-sm hidden sm:inline">Controles</span>
        </button>
      </div>
    </header>
  );
};
