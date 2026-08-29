import React from 'react';

export interface TradeLifecycleCardItem {
  trade_id: string;
  message_id?: number | null;
  ticket_id?: string | null;
  channel_name: string;
  side: 'BUY' | 'SELL';
  entry_price: number;
  exit_price?: number | null;
  margin_usd?: number;
  lot_size?: number;
  pnl_usd?: number | null;
  gross_pnl_usd?: number | null;
  spread_cost_usd?: number;
  commission_usd?: number;
  net_pnl_usd?: number | null;
  sl_price?: number | null;
  initial_sl?: number | null;
  tp1?: number | null;
  tp2?: number | null;
  tp3?: number | null;
  tp1_hit?: boolean;
  tp2_hit?: boolean;
  tp3_hit?: boolean;
  highest_tp?: number;
  status: 'OPEN' | 'WIN' | 'LOSS' | 'PENDING_PULLBACK' | 'REJECTED';
  outcome_text: string;
  created_at: string;
  formatted_created_at?: string;
  closed_at?: string | null;
  formatted_closed_at?: string;
  modifications?: string[];
  error_reason?: string | null;
}

interface SignalFeedProps {
  trades: TradeLifecycleCardItem[];
  selectedChannel?: string;
  onSelectChannel?: (channel: string) => void;
  onOpenAuditModal?: () => void;
}

// Helpers defensivos ultra-seguros contra valores nulos o tipos inesperados
const safePrice = (val: any, fallback = '---'): string => {
  if (val === null || val === undefined || val === '') return fallback;
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  return isNaN(num) ? fallback : num.toFixed(2);
};

const safeNum = (val: any, fallback = 0): number => {
  if (val === null || val === undefined || val === '') return fallback;
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  return isNaN(num) ? fallback : num;
};

const safePnlStr = (val: any): string => {
  if (val === null || val === undefined || val === '') return '$0.00';
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  if (isNaN(num)) return '$0.00';
  const sign = num >= 0 ? '+' : '-';
  return `${sign}$${Math.abs(num).toFixed(2)}`;
};

// Función auxiliar para formatear fecha completa DD/MM/YYYY HH:mm:ss en la zona horaria local del navegador
const formatFullDateTime = (isoString?: string, fallback?: string): string => {
  if (!isoString && fallback) return fallback;
  if (!isoString) return '';
  try {
    const raw = isoString.endsWith('Z') || isoString.includes('+') ? isoString : `${isoString}Z`;
    const d = new Date(raw);
    if (isNaN(d.getTime())) return fallback || isoString;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
  } catch {
    return fallback || isoString;
  }
};

export const SignalFeed: React.FC<SignalFeedProps> = ({
  trades,
  selectedChannel = 'ALL',
  onSelectChannel,
  onOpenAuditModal,
}) => {
  const [localChannelFilter, setLocalChannelFilter] = React.useState<string>(selectedChannel);
  const [expandedCards, setExpandedCards] = React.useState<Record<string, boolean>>({});

  const toggleCardExpand = (cardKey: string) => {
    setExpandedCards(prev => ({ ...prev, [cardKey]: !prev[cardKey] }));
  };

  const activeFilter = onSelectChannel ? selectedChannel : localChannelFilter;
  const setFilter = onSelectChannel || setLocalChannelFilter;

  const safeTradesList = Array.isArray(trades) ? trades : [];
  const filteredTrades = activeFilter === 'ALL'
    ? safeTradesList
    : safeTradesList.filter(t => (t.channel_name || '').toUpperCase().includes(activeFilter.toUpperCase()));

  const displayTrades = filteredTrades.slice(0, 10);

  return (
    <div className="flex flex-col h-full w-full overflow-hidden bg-[#12141c] border border-outline-variant rounded-md min-h-0 select-none">
      {/* Header del Feed con Selector de Canales */}
      <div className="bg-surface-container px-3 py-2 border-b border-outline-variant flex flex-col gap-2 shrink-0">
        <div className="flex justify-between items-center">
          <h2 className="text-label-sm text-white font-bold uppercase tracking-widest flex items-center gap-1.5 font-mono">
            <span className="material-symbols-outlined text-[16px] text-slate-400">history_edu</span>
            Registro de Señales
          </h2>
          <div className="flex items-center gap-1.5">
            {onOpenAuditModal && (
              <button
                onClick={onOpenAuditModal}
                className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 font-bold flex items-center gap-1 transition-colors"
                title="Auditoría de ganancias por canal"
              >
                <span className="material-symbols-outlined text-[12px]">analytics</span>
                Gains
              </button>
            )}
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-outline-variant text-white font-bold">
              {displayTrades.length} TRADES
            </span>
          </div>
        </div>

        {/* Pestañas / Filtros de Canales */}
        <div className="flex items-center gap-1 bg-[#0b0e14] p-1 rounded border border-outline-variant/50 text-[11px] font-mono">
          <button
            onClick={() => setFilter('ALL')}
            className={`flex-1 py-1 rounded text-center font-semibold transition-all ${
              activeFilter === 'ALL'
                ? 'bg-surface-container-highest text-white border border-outline-variant/60 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Todos
          </button>
          <button
            onClick={() => setFilter('Chartoro')}
            className={`flex-1 py-1 rounded text-center font-semibold transition-all ${
              activeFilter.includes('Chartoro')
                ? 'bg-blue-600/30 text-blue-300 border border-blue-500/50 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Chartoro FX
          </button>
          <button
            onClick={() => setFilter('GREEN')}
            className={`flex-1 py-1 rounded text-center font-semibold transition-all ${
              activeFilter.includes('GREEN')
                ? 'bg-emerald-600/30 text-emerald-300 border border-emerald-500/50 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            GREEN PIPS
          </button>
        </div>
      </div>

      {/* Lista de Tarjetas de Trade Vivas y Vencidas */}
      <div className="flex-1 p-2 space-y-2.5 overflow-y-auto">
        {displayTrades.length === 0 ? (
          <div className="text-outline text-label-sm text-center py-10">
            <span className="material-symbols-outlined text-[28px] opacity-40 mb-1">satellite_alt</span>
            <p>No hay señales para el canal seleccionado...</p>
          </div>
        ) : (
          displayTrades.map((t, idx) => {
            const side = t.side || 'BUY';
            const isBuy = side === 'BUY';
            const status = t.status || 'OPEN';
            const isWin = status === 'WIN';
            const isLoss = status === 'LOSS';

            const pnlNum = t.pnl_usd !== null && t.pnl_usd !== undefined ? safeNum(t.pnl_usd) : null;
            const netPnlVal = t.net_pnl_usd !== undefined && t.net_pnl_usd !== null
              ? t.net_pnl_usd
              : (pnlNum !== null ? (pnlNum - safeNum(t.commission_usd, 0.16) - safeNum(t.spread_cost_usd, 0.15)) : null);
            const isModified = Boolean((t.modifications && t.modifications.length > 0) || (t.initial_sl && t.sl_price && t.initial_sl !== t.sl_price));
            const fullDateStr = formatFullDateTime(t.created_at, t.formatted_created_at);

            const exitPriceNum = safeNum(t.exit_price, 0);
            const tp1Num = safeNum(t.tp1, 0);
            const tp2Num = safeNum(t.tp2, 0);
            const tp3Num = safeNum(t.tp3, 0);

            // Identificar con precisión institucional qué niveles de Take Profit se alcanzaron
            const isTp3Triggered = Boolean(
              t.tp3_hit ||
              (t.highest_tp && t.highest_tp >= 3) ||
              (t.modifications && t.modifications.some(m => m.includes('TP3') || m.includes('Infinite Runner'))) ||
              (isWin && tp3Num > 0 && ((isBuy && exitPriceNum >= tp3Num - 1.0) || (!isBuy && exitPriceNum <= tp3Num + 1.0)))
            );

            const isTp2Triggered = Boolean(
              isTp3Triggered ||
              t.tp2_hit ||
              (t.highest_tp && t.highest_tp >= 2) ||
              (t.modifications && t.modifications.some(m => m.includes('TP2') || m.includes('Runner') || m.includes('75%'))) ||
              (isWin && tp2Num > 0 && ((isBuy && exitPriceNum >= tp2Num - 1.0) || (!isBuy && exitPriceNum <= tp2Num + 1.0)))
            );

            const isTp1Triggered = Boolean(
              isTp2Triggered ||
              t.tp1_hit ||
              (t.highest_tp && t.highest_tp >= 1) ||
              (t.modifications && t.modifications.some(m => m.includes('TP1') || m.includes('TP2') || m.includes('TP3') || m.includes('Cobro parcial') || m.includes('50%'))) ||
              (isWin && tp1Num > 0 && ((isBuy && exitPriceNum >= tp1Num - 1.0) || (!isBuy && exitPriceNum <= tp1Num + 1.0)))
            );
            
            const isSlTriggered = isLoss;
            const isPendingPullback = status === 'PENDING_PULLBACK' || (t.outcome_text && t.outcome_text.toUpperCase().includes('PULLBACK') && !t.outcome_text.toUpperCase().includes('TIMEOUT') && !t.outcome_text.toUpperCase().includes('ALCANZADO'));
            const isRejected = (status === 'REJECTED' || (t.outcome_text && t.outcome_text.toUpperCase().includes('FUERA'))) && !isPendingPullback;
            const isOpen = status === 'OPEN' && !isRejected && !isPendingPullback;

            const isGreenPipsCard = (t.channel_name || '').toUpperCase().includes('GREEN');

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
            } else if (isPendingPullback) {
              borderColor = 'border-amber-500/70 shadow-[0_0_10px_rgba(245,158,11,0.2)]';
              bgColor = 'bg-[#1c1810]';
              statusBadge = 'bg-amber-500/20 text-amber-300 border-amber-500/50 font-bold';
            } else if (isRejected) {
              borderColor = 'border-slate-700/60';
              bgColor = 'bg-[#15171e]';
              statusBadge = 'bg-slate-500/15 text-slate-400 border-slate-500/40';
            } else if (isOpen) {
              borderColor = 'border-primary/80 shadow-[0_0_10px_rgba(59,130,246,0.18)] animate-pulse';
              bgColor = 'bg-[#121c29]';
              statusBadge = 'bg-primary/25 text-primary border-primary/60 font-bold';
            }

            const cardKey = t.trade_id || `signal-card-${idx}`;
            const isExpanded = Boolean(expandedCards[cardKey]);

            return (
              <div key={cardKey} className={`p-3 border rounded-md relative overflow-hidden transition-all space-y-2.5 ${bgColor} ${borderColor}`}>
                <div className={`absolute top-0 left-0 w-1.5 h-full ${isWin ? 'bg-emerald-green' : isLoss ? 'bg-crimson-red' : isPendingPullback ? 'bg-amber-400' : isRejected ? 'bg-slate-500' : 'bg-primary'}`} />

                <div className="flex justify-between items-center pl-1.5 gap-2">
                  <div className="flex items-center gap-1.5">
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded border flex items-center gap-1 font-semibold ${isGreenPipsCard ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40' : 'bg-blue-500/15 text-blue-300 border-blue-500/40'}`}>
                      <span className="material-symbols-outlined text-[11px]">cell_tower</span>
                      {t.channel_name || 'Chartoro FX'}
                    </span>
                    <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30 font-bold">AUDIT</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    {netPnlVal !== null && (
                      <span className={`text-[11px] font-mono font-bold px-1.5 py-0.5 rounded ${netPnlVal >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-crimson-red/20 text-crimson-red'}`}>
                        {safePnlStr(netPnlVal)}
                      </span>
                    )}
                  </div>
                </div>

                <div className="pl-1.5 flex items-center gap-1 text-[10px] font-mono text-outline">
                  <span className="material-symbols-outlined text-[13px] opacity-70">schedule</span>
                  <span>{fullDateStr || 'Reciente'}</span>
                </div>

                <div className="pl-1.5 bg-black/40 p-2 rounded border border-white/5 space-y-1.5">
                  <div className="flex justify-between items-center text-[12px] font-mono">
                    <span className={`font-bold flex items-center gap-1 ${isBuy ? 'text-emerald-400' : 'text-crimson-red'}`}>
                      <span className="material-symbols-outlined text-[15px]">{isBuy ? 'arrow_upward' : 'arrow_downward'}</span>
                      {isBuy ? 'BUY XAUUSD' : 'SELL XAUUSD'}
                    </span>
                    <span className="text-[11px] text-slate-300 font-semibold">
                      Margen: ${safeNum(t.margin_usd, 250).toFixed(0)} <span className="text-outline font-normal">({safePrice(t.lot_size, '0.09')}L)</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-[11px] font-mono pt-1 border-t border-white/5">
                    <div>
                      <span className="text-outline text-[10px] mr-1">ENTRADA:</span>
                      <strong className="text-on-surface font-bold">${safePrice(t.entry_price, '2650.00')}</strong>
                    </div>
                    <div>
                      <span className="text-outline text-[10px] mr-1">SALIDA:</span>
                      {t.exit_price ? <strong className={`font-bold ${isWin ? 'text-emerald-400' : 'text-crimson-red'}`}>${safePrice(t.exit_price)}</strong> : <span className="text-primary font-mono text-[10px] italic">En Curso...</span>}
                    </div>
                  </div>
                </div>

                <div className="pl-1.5 grid grid-cols-4 gap-1.5">
                  <div className={`p-1 rounded flex flex-col transition-all border ${isSlTriggered ? 'bg-crimson-red/30 border-crimson-red' : 'bg-black/30 border-white/5'}`}>
                    <span className="text-[8px] font-mono uppercase text-outline">SL</span>
                    <span className={`text-[10px] font-mono font-bold ${isSlTriggered ? 'text-white' : 'text-crimson-red'}`}>{t.sl_price ? `$${safePrice(t.sl_price)}` : '---'}</span>
                  </div>
                  <div className={`p-1 rounded flex flex-col transition-all border ${isTp1Triggered ? 'bg-emerald-500/30 border-emerald-400' : 'bg-black/30 border-white/5'}`}>
                    <span className="text-[8px] font-mono uppercase text-outline">TP1</span>
                    <span className={`text-[10px] font-mono font-bold ${isTp1Triggered ? 'text-white' : 'text-emerald-400'}`}>{t.tp1 ? `$${safePrice(t.tp1)}` : '---'}</span>
                  </div>
                  <div className={`p-1 rounded flex flex-col transition-all border ${isTp2Triggered ? 'bg-emerald-500/30 border-emerald-400' : 'bg-black/30 border-white/5'}`}>
                    <span className="text-[8px] font-mono uppercase text-outline">TP2</span>
                    <span className={`text-[10px] font-mono font-bold ${isTp2Triggered ? 'text-white' : 'text-emerald-400'}`}>{t.tp2 ? `$${safePrice(t.tp2)}` : '---'}</span>
                  </div>
                  <div className={`p-1 rounded flex flex-col transition-all border ${isTp3Triggered ? 'bg-emerald-500/30 border-emerald-400' : 'bg-black/30 border-white/5'}`}>
                    <span className="text-[8px] font-mono uppercase text-outline">TP3</span>
                    <span className={`text-[10px] font-mono font-bold ${isTp3Triggered ? 'text-white' : 'text-emerald-400'}`}>{t.tp3 ? `$${safePrice(t.tp3)}` : '---'}</span>
                  </div>
                </div>

                {(t.status === 'WIN' || t.status === 'LOSS' || pnlNum !== null || t.exit_price) && (
                  <div className="pt-1 border-t border-white/5 pl-1.5">
                    <button type="button" onClick={() => toggleCardExpand(cardKey)} className="w-full py-1 px-2 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-[9.5px] font-mono text-slate-300 flex items-center justify-between transition-colors">
                      <span className="flex items-center gap-1.5 font-semibold text-slate-200">
                        <span className="material-symbols-outlined text-[12px] text-amber-400">receipt_long</span>
                        {isExpanded ? 'Ocultar desglose' : 'Ver desglose financiero'}
                      </span>
                      <span className="material-symbols-outlined text-[14px] text-slate-400">{isExpanded ? 'expand_less' : 'expand_more'}</span>
                    </button>
                    {isExpanded && (
                      <div className="mt-1.5 p-2 rounded bg-black/50 border border-white/10 flex flex-col gap-1 text-[9.5px] font-mono animate-fadeIn">
                        <div className="flex justify-between items-center text-slate-400 border-b border-white/5 pb-1">
                          <span>Movimiento Bruto:</span>
                          <span className={pnlNum !== null && pnlNum >= 0 ? 'text-emerald-400' : 'text-crimson-red'}>{safePnlStr(pnlNum)}</span>
                        </div>
                        <div className="flex justify-between items-center text-slate-400">
                          <span>Spread cTrader:</span>
                          <span className="text-amber-300">-${safePrice(t.spread_cost_usd, '0.15')}</span>
                        </div>
                        <div className="flex justify-between items-center text-slate-400">
                          <span>Comisión IC Markets:</span>
                          <span className="text-blue-300">-${safePrice(t.commission_usd, '0.16')}</span>
                        </div>
                        <div className="flex justify-between items-center pt-1 border-t border-white/10 font-bold text-[10.5px]">
                          <span>NETO FINAL:</span>
                          <span className={netPnlVal !== null && netPnlVal >= 0 ? 'text-emerald-400' : 'text-crimson-red'}>{safePnlStr(netPnlVal)}</span>
                        </div>
                      </div>
                    )}
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
