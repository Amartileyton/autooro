import React from 'react';

export interface TradeLifecycleCardItem {
  trade_id: string;
  channel_name: string;
  side: 'BUY' | 'SELL';
  entry_price: number;
  sl_price?: number | null;
  initial_sl?: number | null;
  tp1?: number | null;
  tp2?: number | null;
  tp3?: number | null;
  status: 'OPEN' | 'WIN' | 'LOSS';
  outcome_text: string;
  created_at: string;
  closed_at?: string | null;
  modifications?: string[];
}

interface SignalFeedProps {
  trades: TradeLifecycleCardItem[];
}

export const SignalFeed: React.FC<SignalFeedProps> = ({ trades }) => {
  const displayTrades = (trades || []).slice(0, 10);

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#12141c]">
      {/* Header del Feed */}
      <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex justify-between items-center shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-amber-gold">stacked_line_chart</span>
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

            const dateObj = new Date(t.created_at);
            const timeStr = isNaN(dateObj.getTime())
              ? ''
              : dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

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
                className={`p-3 border rounded-md relative overflow-hidden transition-all space-y-2 ${bgColor} ${borderColor}`}
              >
                {/* Borde lateral indicador de estado */}
                <div
                  className={`absolute top-0 left-0 w-1.5 h-full ${
                    isWin ? 'bg-emerald-green' : isLoss ? 'bg-crimson-red' : 'bg-primary'
                  }`}
                />

                {/* Fila 1: Origen + Estado + Hora */}
                <div className="flex justify-between items-center pl-1.5 gap-2">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {/* Canal de Origen */}
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-container-highest text-amber-gold border border-amber-gold/30 flex items-center gap-1 font-bold">
                      <span className="material-symbols-outlined text-[11px]">send</span>
                      {t.channel_name}
                    </span>

                    {/* Badge de Estado del Trade */}
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border ${statusBadge}`}>
                      {isWin ? `✅ ${t.outcome_text}` : isLoss ? `❌ ${t.outcome_text}` : '🔵 ACTIVO (EN CURSO)'}
                    </span>
                  </div>

                  <span className="text-[10px] font-mono text-outline shrink-0">
                    {timeStr}
                  </span>
                </div>

                {/* Fila 2: Dirección y Precio de Entrada */}
                <div className="pl-1.5 flex justify-between items-center border-t border-white/5 pt-1.5">
                  <div className="flex items-center gap-2">
                    <span className={`text-[13px] font-mono font-bold flex items-center gap-1 ${isBuy ? 'text-emerald-400' : 'text-crimson-red'}`}>
                      <span className="material-symbols-outlined text-[16px]">
                        {isBuy ? 'arrow_upward' : 'arrow_downward'}
                      </span>
                      {isBuy ? 'BUY XAUUSD' : 'SELL XAUUSD'}
                    </span>
                  </div>

                  <div className="text-[12px] font-mono">
                    <span className="text-outline text-[10px] mr-1.5">ENTRADA:</span>
                    <strong className="text-on-surface font-bold text-[13px]">${t.entry_price?.toFixed(2)}</strong>
                  </div>
                </div>

                {/* Fila 3: Rejilla de Niveles de SL y Take Profits */}
                <div className="pl-1.5 grid grid-cols-4 gap-1.5 pt-1">
                  {/* Stop Loss */}
                  <div className="p-1.5 rounded bg-black/40 border border-white/5 flex flex-col">
                    <span className="text-[9px] font-mono text-outline uppercase flex items-center justify-between">
                      SL
                      {isModified && <span className="text-amber-400 font-bold text-[8px]">MOD</span>}
                    </span>
                    <span className={`text-[11px] font-mono font-bold mt-0.5 ${t.sl_price ? 'text-crimson-red' : 'text-outline/40'}`}>
                      {t.sl_price ? `$${t.sl_price.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP1 */}
                  <div className="p-1.5 rounded bg-black/40 border border-white/5 flex flex-col">
                    <span className="text-[9px] font-mono text-outline uppercase">TP1</span>
                    <span className={`text-[11px] font-mono font-bold mt-0.5 ${t.tp1 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp1 ? `$${t.tp1.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP2 */}
                  <div className="p-1.5 rounded bg-black/40 border border-white/5 flex flex-col">
                    <span className="text-[9px] font-mono text-outline uppercase">TP2</span>
                    <span className={`text-[11px] font-mono font-bold mt-0.5 ${t.tp2 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp2 ? `$${t.tp2.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP3 */}
                  <div className="p-1.5 rounded bg-black/40 border border-white/5 flex flex-col">
                    <span className="text-[9px] font-mono text-outline uppercase">TP3</span>
                    <span className={`text-[11px] font-mono font-bold mt-0.5 ${t.tp3 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp3 ? `$${t.tp3.toFixed(2)}` : '---'}
                    </span>
                  </div>
                </div>

                {/* Modificaciones posteriores si existen */}
                {t.modifications && t.modifications.length > 0 && (
                  <div className="pl-1.5 text-[10px] font-mono text-amber-300 bg-amber-500/10 p-1 rounded border border-amber-500/20 flex items-center gap-1">
                    <span className="material-symbols-outlined text-[13px]">update</span>
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
