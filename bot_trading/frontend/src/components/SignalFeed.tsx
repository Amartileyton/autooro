import React from 'react';
import { safePrice, safeNum, safePnlStr, formatFullDateTime } from '@/utils/formatters';
import { SignalCard } from './SignalCard';

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

export const SignalFeed: React.FC<SignalFeedProps> = ({
  trades,
  selectedChannel = 'ALL',
  onSelectChannel,
  onOpenAuditModal,
}) => {
  const [localChannelFilter, setLocalChannelFilter] = React.useState<string>(selectedChannel);
  const [expandedCards, setExpandedCards] = React.useState<Record<string, boolean>>({});

  const toggleCardExpand = React.useCallback((cardKey: string) => {
    setExpandedCards(prev => ({ ...prev, [cardKey]: !prev[cardKey] }));
  }, []);

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
            const cardKey = t.trade_id || `signal-card-${idx}`;
            return (
              <SignalCard
                key={cardKey}
                trade={t}
                index={idx}
                isExpanded={Boolean(expandedCards[cardKey])}
                onToggleExpand={toggleCardExpand}
              />
            );
          })
        )}
      </div>
    </div>
  );
};
