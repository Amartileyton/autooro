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
      {/* Header del Feed en Gris Institucional */}
      <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex justify-between items-center shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-slate-400">history_edu</span>
          <span className="text-label-sm text-slate-200 uppercase font-bold tracking-wider">
            Registro de Trades (10 Últimos)
          </span>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-outline-variant text-slate-400 font-bold">
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

            // Identificar qué nivel disparó la orden
            const isTp3Triggered = isWin && t.exit_price && t.tp3 && Math.abs(t.exit_price - t.tp3) < 1.0;
            const isTp2Triggered = isWin && !isTp3Triggered && t.exit_price && t.tp2 && Math.abs(t.exit_price - t.tp2) < 1.0;
            const isTp1Triggered = isWin && !isTp3Triggered && !isTp2Triggered; // Default a TP1 en operaciones ganadas
            const isSlTriggered = isLoss; // Disparo de SL en operaciones perdidas

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

                {/* Fila 1: Origen + Estado (Solo SVG sin texto GANADA/PERDIDA) */}
                <div className="flex justify-between items-center pl-1.5 gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-container-highest text-slate-300 border border-outline-variant/60 flex items-center gap-1 font-semibold">
                    <span className="material-symbols-outlined text-[11px] text-slate-400">send</span>
                    {t.channel_name}
                  </span>

                  <div className="flex items-center gap-1.5">
                    {t.pnl_usd !== null && t.pnl_usd !== undefined && (
                      <span className={`text-[11px] font-mono font-bold px-1.5 py-0.5 rounded ${t.pnl_usd >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-crimson-red/20 text-crimson-red'}`}>
                        {t.pnl_usd >= 0 ? `+$${t.pnl_usd.toFixed(2)}` : `-$${Math.abs(t.pnl_usd).toFixed(2)}`}
                      </span>
                    )}

                    {/* Insignia con SVG Oficial Puro Flotante (sin recuadro exterior) */}
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

                    <span className="text-[11px] text-slate-300 font-semibold">
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

                {/* Fila 4: Rejilla de Niveles de SL y Take Profits con Sombreado Puro (sin marcadores de texto) */}
                <div className="pl-1.5 grid grid-cols-4 gap-1.5">
                  {/* Stop Loss (Sombreado en rojo si disparó pérdida) */}
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
                      {t.sl_price ? `$${t.sl_price.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP1 (Sombreado en verde si disparó ganancia) */}
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
                      {t.tp1 ? `$${t.tp1.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP2 (Sombreado en verde si disparó ganancia) */}
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
                      {t.tp2 ? `$${t.tp2.toFixed(2)}` : '---'}
                    </span>
                  </div>

                  {/* TP3 (Sombreado en verde si disparó ganancia) */}
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
