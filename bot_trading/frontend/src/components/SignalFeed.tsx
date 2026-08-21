import React from 'react';

export interface TradeLifecycleCardItem {
  trade_id: string;
  channel_name: string;
  side: 'BUY' | 'SELL';
  entry_price: number;
  exit_price?: number | null;
  margin_usd?: number;
  lot_size?: number;
  pnl_usd?: number | null;
  sl_price?: number | null;
  initial_sl?: number | null;
  tp1?: number | null;
  tp2?: number | null;
  tp3?: number | null;
  status: 'OPEN' | 'WIN' | 'LOSS';
  outcome_text: string;
  created_at: string;
  formatted_created_at?: string;
  closed_at?: string | null;
  formatted_closed_at?: string;
  modifications?: string[];
}

interface SignalFeedProps {
  trades: TradeLifecycleCardItem[];
}

// Función auxiliar para formatear fecha completa DD/MM/YYYY HH:mm:ss
const formatFullDateTime = (isoString: string, fallback?: string): string => {
  if (fallback) return fallback;
  try {
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return isoString;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
  } catch {
    return isoString;
  }
};

export const SignalFeed: React.FC<SignalFeedProps> = ({ trades }) => {
  const displayTrades = (trades || []).slice(0, 10);

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#12141c]">
      {/* Header del Feed */}
      <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex justify-between items-center shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-amber-gold">history_edu</span>
          <span className="text-label-sm text-on-surface uppercase font-bold tracking-wider">
            Registro de Trades (10 Últimos)
          </span>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-outline-variant text-outline">
          {displayTrades.length} Trades
        </span>
      </div>

      {/* Lista de Tarjetas de Trade Vivas y Vencidas */}
      <div className="flex-1 p-2 space-y-2.5 overflow-y-auto">
        {displayTrades.length === 0 ? (
          <div className="text-outline text-label-sm text-center py-10">
            <span className="material-symbols-outlined text-[28px] opacity-40 mb-1">satellite_alt</span>
            <p>Esperando señales de Telegram...</p>
          </div>
        ) : (
          displayTrades.map((t) => {
            const isBuy = t.side === 'BUY';
            const isWin = t.status === 'WIN';
            const isLoss = t.status === 'LOSS';
            const isOpen = t.status === 'OPEN';

            const isModified = (t.modifications && t.modifications.length > 0) || (t.initial_sl && t.sl_price && t.initial_sl !== t.sl_price);
            const fullDateStr = formatFullDateTime(t.created_at, t.formatted_created_at);

            // Estilos de estado (Verde = Ganada, Rojo = Perdida, Azul = Abierta)
            let borderColor = 'border-outline-variant/50';
            let bgColor = 'bg-surface/60';
            let statusBadge = 'bg-primary/20 text-primary border-primary/40';

            if (isWin) {
              borderColor = 'border-emerald-500/80 shadow-[0_0_10px_rgba(16,185,129,0.18)]';
              bgColor = 'bg-[#0e2019]';
              statusBadge = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
            } else if (isLoss) {
              borderColor = 'border-crimson-red/80 shadow-[0_0_10px_rgba(239,68,68,0.18)]';
              bgColor = 'bg-[#221215]';
              statusBadge = 'bg-crimson-red/20 text-crimson-red border-crimson-red/50';
            } else if (isOpen) {
              borderColor = 'border-primary/80 shadow-[0_0_10px_rgba(59,130,246,0.18)] animate-pulse';
              bgColor = 'bg-[#121c29]';
              statusBadge = 'bg-primary/25 text-primary border-primary/60 font-bold';
            }

            return (
              <div
                key={t.trade_id}
                className={`p-3 border rounded-md relative overflow-hidden transition-all space-y-2.5 ${bgColor} ${borderColor}`}
              >
                {/* Borde lateral indicador de estado */}
                <div
                  className={`absolute top-0 left-0 w-1.5 h-full ${
                    isWin ? 'bg-emerald-green' : isLoss ? 'bg-crimson-red' : 'bg-primary'
                  }`}
                />

                {/* Fila 1: Origen + Estado */}
                <div className="flex justify-between items-center pl-1.5 gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-container-highest text-amber-gold border border-amber-gold/30 flex items-center gap-1 font-bold">
                    <span className="material-symbols-outlined text-[11px]">send</span>
                    {t.channel_name}
                  </span>

                  <div className="flex items-center gap-1.5">
                    {t.pnl_usd !== null && t.pnl_usd !== undefined && (
                      <span className={`text-[11px] font-mono font-bold px-1.5 py-0.5 rounded ${t.pnl_usd >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-crimson-red/20 text-crimson-red'}`}>
                        {t.pnl_usd >= 0 ? `+$${t.pnl_usd.toFixed(2)}` : `-$${Math.abs(t.pnl_usd).toFixed(2)}`}
                      </span>
                    )}
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border ${statusBadge}`}>
                      {isWin ? '✓ GANADA' : isLoss ? '❌ PERDIDA' : '🔵 EN CURSO'}
                    </span>
                  </div>
                </div>

                {/* Fila 2: Fecha y Hora Completa */}
                <div className="pl-1.5 flex items-center gap-1 text-[10px] font-mono text-outline">
                  <span className="material-symbols-outlined text-[13px] opacity-70">schedule</span>
                  <span>{fullDateStr}</span>
                </div>

                {/* Fila 3: Tarjeta de Inversión, Entrada y Salida */}
                <div className="pl-1.5 bg-black/40 p-2 rounded border border-white/5 space-y-1.5">
                  {/* Dirección y Margen */}
                  <div className="flex justify-between items-center text-[12px] font-mono">
                    <span className={`font-bold flex items-center gap-1 ${isBuy ? 'text-emerald-400' : 'text-crimson-red'}`}>
                      <span className="material-symbols-outlined text-[15px]">
                        {isBuy ? 'arrow_upward' : 'arrow_downward'}
                      </span>
                      {isBuy ? 'BUY XAUUSD' : 'SELL XAUUSD'}
                    </span>

                    <span className="text-[11px] text-amber-gold font-bold">
                      Margen: {t.margin_usd ? `$${t.margin_usd.toFixed(0)}` : '$1,000'} <span className="text-outline font-normal">({t.lot_size ? t.lot_size.toFixed(2) : '0.22'}L)</span>
                    </span>
                  </div>

                  {/* Precios de Entrada y Salida */}
                  <div className="flex justify-between items-center text-[11px] font-mono pt-1 border-t border-white/5">
                    <div>
                      <span className="text-outline text-[10px] mr-1">ENTRADA:</span>
                      <strong className="text-on-surface font-bold">${t.entry_price?.toFixed(2)}</strong>
                    </div>

                    <div>
                      <span className="text-outline text-[10px] mr-1">SALIDA:</span>
                      {t.exit_price ? (
                        <strong className={`font-bold ${isWin ? 'text-emerald-400' : 'text-crimson-red'}`}>
                          ${t.exit_price.toFixed(2)}
                        </strong>
                      ) : (
                        <span className="text-primary font-mono text-[10px] italic">En Curso...</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Fila 4: Rejilla de Niveles de SL y Take Profits */}
                <div className="pl-1.5 grid grid-cols-4 gap-1.5">
                  {/* Stop Loss */}
                  <div className="p-1 rounded bg-black/30 border border-white/5 flex flex-col">
                    <span className="text-[8px] font-mono text-outline uppercase flex items-center justify-between">
                      SL
                      {isModified && <span className="text-amber-400 font-bold text-[7px]">MOD</span>}
                    </span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${t.sl_price ? 'text-crimson-red' : 'text-outline/40'}`}>
                      {t.sl_price ? `$${t.sl_price.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP1 */}
                  <div className="p-1 rounded bg-black/30 border border-white/5 flex flex-col">
                    <span className="text-[8px] font-mono text-outline uppercase">TP1</span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${t.tp1 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp1 ? `$${t.tp1.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP2 */}
                  <div className="p-1 rounded bg-black/30 border border-white/5 flex flex-col">
                    <span className="text-[8px] font-mono text-outline uppercase">TP2</span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${t.tp2 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp2 ? `$${t.tp2.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP3 */}
                  <div className="p-1 rounded bg-black/30 border border-white/5 flex flex-col">
                    <span className="text-[8px] font-mono text-outline uppercase">TP3</span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${t.tp3 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp3 ? `$${t.tp3.toFixed(2)}` : '---'}
                    </span>
                  </div>
                </div>

                {/* Modificaciones posteriores si existen */}
                {t.modifications && t.modifications.length > 0 && (
                  <div className="pl-1.5 text-[9px] font-mono text-amber-300 bg-amber-500/10 p-1 rounded border border-amber-500/20 flex items-center gap-1">
                    <span className="material-symbols-outlined text-[12px]">update</span>
                    {t.modifications[t.modifications.length - 1]}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
