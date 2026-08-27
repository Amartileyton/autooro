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
  status: 'OPEN' | 'WIN' | 'LOSS' | 'REJECTED';
  outcome_text: string;
  created_at: string;
  formatted_created_at?: string;
  closed_at?: string | null;
  formatted_closed_at?: string;
  modifications?: string[];
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
              {displayTrades.length} SEÑALES
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
            const isOpen = status === 'OPEN';

            const pnlNum = t.pnl_usd !== null && t.pnl_usd !== undefined ? safeNum(t.pnl_usd) : null;
            const isModified = Boolean((t.modifications && t.modifications.length > 0) || (t.initial_sl && t.sl_price && t.initial_sl !== t.sl_price));
            const fullDateStr = formatFullDateTime(t.created_at, t.formatted_created_at);

            const exitPriceNum = safeNum(t.exit_price, 0);
            const tp3Num = safeNum(t.tp3, 0);
            const tp2Num = safeNum(t.tp2, 0);

            // Identificar qué nivel disparó la orden
            const isTp3Triggered = isWin && exitPriceNum > 0 && tp3Num > 0 && Math.abs(exitPriceNum - tp3Num) < 1.5;
            const isTp2Triggered = isWin && !isTp3Triggered && exitPriceNum > 0 && tp2Num > 0 && Math.abs(exitPriceNum - tp2Num) < 1.5;
            const isTp1Triggered = isWin && !isTp3Triggered && !isTp2Triggered;
            const isSlTriggered = isLoss;
            const isRejected = status === 'REJECTED' || (t.outcome_text && t.outcome_text.toUpperCase().includes('FUERA'));
            const isOpen = status === 'OPEN' && !isRejected;

            const isGreenPipsCard = (t.channel_name || '').toUpperCase().includes('GREEN');

            // Estilos de tarjeta general
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

            return (
              <div
                key={cardKey}
                className={`p-3 border rounded-md relative overflow-hidden transition-all space-y-2.5 ${bgColor} ${borderColor}`}
              >
                {/* Borde lateral indicador de estado */}
                <div
                  className={`absolute top-0 left-0 w-1.5 h-full ${
                    isWin ? 'bg-emerald-green' : isLoss ? 'bg-crimson-red' : isRejected ? 'bg-slate-500' : 'bg-primary'
                  }`}
                />

                {/* Fila 1: Origen + Modo Auditoría + Estado */}
                <div className="flex justify-between items-center pl-1.5 gap-2">
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`text-[10px] font-mono px-2 py-0.5 rounded border flex items-center gap-1 font-semibold ${
                        isGreenPipsCard
                          ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40'
                          : 'bg-blue-500/15 text-blue-300 border-blue-500/40'
                      }`}
                    >
                      <span className="material-symbols-outlined text-[11px]">cell_tower</span>
                      {t.channel_name || 'Chartoro FX'}
                    </span>

                    <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30 font-bold">
                      AUDIT
                    </span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    {pnlNum !== null && (
                      <span className={`text-[11px] font-mono font-bold px-1.5 py-0.5 rounded ${pnlNum >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-crimson-red/20 text-crimson-red'}`}>
                        {safePnlStr(pnlNum)}
                      </span>
                    )}

                    {/* Insignia con SVG Oficial */}
                    {isWin ? (
                      <svg
                        className="w-5 h-5 fill-current text-emerald-400 shrink-0 drop-shadow-[0_0_6px_rgba(16,185,129,0.4)]"
                        viewBox="0 0 24 24"
                        title="Operación Ganada"
                      >
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12ZM15.7071 9.29289C16.0976 9.68342 16.0976 10.3166 15.7071 10.7071L12.0243 14.3899C11.4586 14.9556 10.5414 14.9556 9.97568 14.3899L8.29289 12.7071C7.90237 12.3166 7.90237 11.6834 8.29289 11.2929C8.68342 10.9024 9.31658 10.9024 9.70711 11.2929L11 12.5858L14.2929 9.29289C14.6834 8.90237 15.3166 8.90237 15.7071 9.29289Z"
                        />
                      </svg>
                    ) : isLoss ? (
                      <svg
                        className="w-5 h-5 fill-current text-crimson-red shrink-0 drop-shadow-[0_0_6px_rgba(239,68,68,0.4)]"
                        viewBox="0 0 24 24"
                        title="Operación Perdida"
                      >
                        <path d="M12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm3.71,12.29a1,1,0,0,1,0,1.42,1,1,0,0,1-1.42,0L12,13.42,9.71,15.71a1,1,0,0,1-1.42,0,1,1,0,0,1,0-1.42L10.58,12,8.29,9.71A1,1,0,0,1,9.71,8.29L12,10.58l2.29-2.29a1,1,0,0,1,1.42,1.42L13.42,12Z" />
                      </svg>
                    ) : isRejected ? (
                      <span className="px-2 py-0.5 rounded font-mono text-[10px] font-bold border flex items-center gap-1 bg-slate-500/15 text-slate-400 border-slate-500/40">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                        FUERA PRECIO
                      </span>
                    ) : (
                      <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-bold border flex items-center gap-1 ${statusBadge}`}>
                        <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                        EN CURSO
                      </span>
                    )}
                  </div>
                </div>

                {/* Fila 2: Fecha y Hora Completa */}
                <div className="pl-1.5 flex items-center gap-1 text-[10px] font-mono text-outline">
                  <span className="material-symbols-outlined text-[13px] opacity-70">schedule</span>
                  <span>{fullDateStr || 'Reciente'}</span>
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

                    <span className="text-[11px] text-slate-300 font-semibold">
                      Margen: ${safeNum(t.margin_usd, 250).toFixed(0)} <span className="text-outline font-normal">({safePrice(t.lot_size, '0.09')}L)</span>
                    </span>
                  </div>

                  {/* Precios de Entrada y Salida */}
                  <div className="flex justify-between items-center text-[11px] font-mono pt-1 border-t border-white/5">
                    <div>
                      <span className="text-outline text-[10px] mr-1">ENTRADA:</span>
                      <strong className="text-on-surface font-bold">${safePrice(t.entry_price, '2650.00')}</strong>
                    </div>

                    <div>
                      <span className="text-outline text-[10px] mr-1">SALIDA:</span>
                      {t.exit_price ? (
                        <strong className={`font-bold ${isWin ? 'text-emerald-400' : 'text-crimson-red'}`}>
                          ${safePrice(t.exit_price)}
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
                  <div
                    className={`p-1 rounded flex flex-col transition-all border ${
                      isSlTriggered
                        ? 'bg-crimson-red/30 border-crimson-red shadow-[0_0_10px_rgba(239,68,68,0.35)] ring-1 ring-crimson-red/80'
                        : 'bg-black/30 border-white/5 opacity-80'
                    }`}
                  >
                    <span className="text-[8px] font-mono uppercase flex items-center justify-between">
                      <span className={isSlTriggered ? 'text-crimson-red font-bold' : 'text-outline'}>
                        SL
                      </span>
                      {isModified && <span className="text-amber-400 font-bold text-[7px]">MOD</span>}
                    </span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${isSlTriggered ? 'text-white' : t.sl_price ? 'text-crimson-red' : 'text-outline/40'}`}>
                      {t.sl_price ? `$${safePrice(t.sl_price)}` : '---'}
                    </span>
                  </div>

                  {/* TP1 */}
                  <div
                    className={`p-1 rounded flex flex-col transition-all border ${
                      isTp1Triggered
                        ? 'bg-emerald-500/30 border-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.35)] ring-1 ring-emerald-400/80'
                        : 'bg-black/30 border-white/5 opacity-80'
                    }`}
                  >
                    <span className={`text-[8px] font-mono uppercase ${isTp1Triggered ? 'text-emerald-300 font-bold' : 'text-outline'}`}>
                      TP1
                    </span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${isTp1Triggered ? 'text-white' : t.tp1 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp1 ? `$${safePrice(t.tp1)}` : '---'}
                    </span>
                  </div>

                  {/* TP2 */}
                  <div
                    className={`p-1 rounded flex flex-col transition-all border ${
                      isTp2Triggered
                        ? 'bg-emerald-500/30 border-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.35)] ring-1 ring-emerald-400/80'
                        : 'bg-black/30 border-white/5 opacity-80'
                    }`}
                  >
                    <span className={`text-[8px] font-mono uppercase ${isTp2Triggered ? 'text-emerald-300 font-bold' : 'text-outline'}`}>
                      TP2
                    </span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${isTp2Triggered ? 'text-white' : t.tp2 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp2 ? `$${safePrice(t.tp2)}` : '---'}
                    </span>
                  </div>

                  {/* TP3 */}
                  <div
                    className={`p-1 rounded flex flex-col transition-all border ${
                      isTp3Triggered
                        ? 'bg-emerald-500/30 border-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.35)] ring-1 ring-emerald-400/80'
                        : 'bg-black/30 border-white/5 opacity-80'
                    }`}
                  >
                    <span className={`text-[8px] font-mono uppercase ${isTp3Triggered ? 'text-emerald-300 font-bold' : 'text-outline'}`}>
                      TP3
                    </span>
                    <span className={`text-[10px] font-mono font-bold mt-0.5 ${isTp3Triggered ? 'text-white' : t.tp3 ? 'text-emerald-400' : 'text-outline/40'}`}>
                      {t.tp3 ? `$${safePrice(t.tp3)}` : '---'}
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
