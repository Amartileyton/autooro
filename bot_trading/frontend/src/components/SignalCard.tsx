import React from 'react';
import { safePrice, safeNum, safePnlStr, formatFullDateTime } from '@/utils/formatters';
import type { TradeLifecycleCardItem } from './SignalFeed';

interface SignalCardProps {
  trade: TradeLifecycleCardItem;
  index: number;
  isExpanded: boolean;
  onToggleExpand: (cardKey: string) => void;
}

/**
 * Tarjeta atómica de ciclo de vida de un trade. Extraída de SignalFeed para
 * mejorar legibilidad y permitir memoización por tarjeta (React.memo).
 */
export const SignalCard: React.FC<SignalCardProps> = React.memo(
  ({ trade: t, index: idx, isExpanded, onToggleExpand }) => {
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

    // Identificar con precisión institucional qué niveles de Take Profit se alcanzaron EN CUENTA
    const isTp3Triggered = Boolean(
      t.account_tp3_hit ||
      (!t.security_exit_before_tp && t.tp3_hit) ||
      (!t.security_exit_before_tp && t.highest_tp && t.highest_tp >= 3) ||
      (isWin && tp3Num > 0 && ((isBuy && exitPriceNum >= tp3Num - 1.0) || (!isBuy && exitPriceNum <= tp3Num + 1.0)))
    );

    const isTp2Triggered = Boolean(
      isTp3Triggered ||
      t.account_tp2_hit ||
      (!t.security_exit_before_tp && t.tp2_hit) ||
      (!t.security_exit_before_tp && t.highest_tp && t.highest_tp >= 2) ||
      (isWin && tp2Num > 0 && ((isBuy && exitPriceNum >= tp2Num - 1.0) || (!isBuy && exitPriceNum <= tp2Num + 1.0)))
    );

    const isTp1Triggered = Boolean(
      isTp2Triggered ||
      t.account_tp1_hit ||
      t.tp1_hit ||
      (t.highest_tp && t.highest_tp >= 1) ||
      (isWin && tp1Num > 0 && ((isBuy && exitPriceNum >= tp1Num - 1.0) || (!isBuy && exitPriceNum <= tp1Num + 1.0)))
    );

    // Hitos alcanzados únicamente por el canal de Telegram tras la salida defensiva de la cuenta
    const isChannelOnlyTp3 = Boolean(
      !isTp3Triggered && (t.channel_tp3_hit || (t.highest_channel_tp && t.highest_channel_tp >= 3) || (t.security_exit_before_tp && (t.highest_channel_tp || 0) >= 3))
    );
    const isChannelOnlyTp2 = Boolean(
      !isTp2Triggered && (t.channel_tp2_hit || (t.highest_channel_tp && t.highest_channel_tp >= 2) || (t.security_exit_before_tp && (t.highest_channel_tp || 0) >= 2))
    );
    
    const isSlTriggered = isLoss;
    const isRejected = (status === 'REJECTED' || (t.outcome_text && (t.outcome_text.toUpperCase().includes('FUERA') || t.outcome_text.toUpperCase().includes('TIMEOUT') || t.outcome_text.toUpperCase().includes('ALCANZADO'))));
    const isPendingPullback = !isRejected && (status === 'PENDING_PULLBACK' || (t.outcome_text && t.outcome_text.toUpperCase().includes('PULLBACK')));
    const isOpen = status === 'OPEN' && !isRejected && !isPendingPullback;

    const isGreenPipsCard = (t.channel_name || '').toUpperCase().includes('GREEN');
    const cleanChannelName = (t.channel_name || 'Chartoro FX')
      .replace(/XAU\(USD\)\s*/i, '')
      .replace(/XAUUSD\s*/i, '')
      .trim() || 'Chartoro FX';

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

    return (
      <div className={`p-3 border rounded-md relative overflow-hidden transition-all space-y-2.5 ${bgColor} ${borderColor}`}>
        <div className={`absolute top-0 left-0 w-1.5 h-full ${isWin ? 'bg-emerald-green' : isLoss ? 'bg-crimson-red' : isPendingPullback ? 'bg-amber-400' : isRejected ? 'bg-slate-500' : 'bg-primary'}`} />

        {/* Fila 1: Cabecera normalizada y alineada en una sola línea */}
        <div className="flex justify-between items-center pl-1.5 gap-2 min-h-[24px]">
          <div className="flex items-center gap-1.5 shrink-0">
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded border flex items-center gap-1 font-semibold whitespace-nowrap ${isGreenPipsCard ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/40' : 'bg-blue-500/15 text-blue-300 border-blue-500/40'}`}>
              <span className="material-symbols-outlined text-[11px]">cell_tower</span>
              {cleanChannelName}
            </span>
            <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/30 font-bold whitespace-nowrap">AUDIT</span>
          </div>

          <div className="flex items-center gap-1.5 shrink-0">
            {isRejected ? (
              <span className="text-[9.5px] font-mono font-bold px-2 py-0.5 rounded bg-slate-700/60 text-slate-200 border border-slate-500/60 flex items-center gap-1 whitespace-nowrap">
                <span className="material-symbols-outlined text-[12px] text-amber-400">block</span>
                FUERA PRECIO
              </span>
            ) : isPendingPullback ? (
              <span className="text-[9.5px] font-mono font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center gap-1 whitespace-nowrap">
                <span className="material-symbols-outlined text-[12px] text-amber-400">hourglass_top</span>
                EN ESPERA
              </span>
            ) : netPnlVal !== null ? (
              <span className={`text-[11px] font-mono font-bold px-1.5 py-0.5 rounded whitespace-nowrap ${netPnlVal >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-crimson-red/20 text-crimson-red'}`}>
                {safePnlStr(netPnlVal)}
              </span>
            ) : isOpen ? (
              <span className="text-[9.5px] font-mono font-bold px-1.5 py-0.5 rounded bg-primary/20 text-primary border border-primary/40 flex items-center gap-1 animate-pulse whitespace-nowrap">
                <span className="material-symbols-outlined text-[11px]">radio_button_checked</span>
                EN CURSO
              </span>
            ) : null}
          </div>
        </div>

        {/* Fila 2: Timestamp */}
        <div className="pl-1.5 flex items-center gap-1 text-[10px] font-mono text-outline">
          <span className="material-symbols-outlined text-[13px] opacity-70">schedule</span>
          <span>{fullDateStr || 'Reciente'}</span>
        </div>

        {/* Fila 3: Caja de Ejecución (Sintaxis y alturas fijas) */}
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
            <div className="flex items-center">
              <span className="text-outline text-[10px] mr-1">ENTRADA:</span>
              <strong className="text-on-surface font-bold">${safePrice(t.entry_price, '2650.00')}</strong>
            </div>
            <div className="flex items-center">
              <span className="text-outline text-[10px] mr-1">SALIDA:</span>
              {isRejected ? (
                <span className="text-slate-400 font-mono text-[10px] font-semibold">---</span>
              ) : isPendingPullback ? (
                <span className="text-amber-400 font-mono text-[10px] font-semibold italic">En espera...</span>
              ) : t.exit_price ? (
                <strong className={`font-bold ${isWin ? 'text-emerald-400' : 'text-crimson-red'}`}>${safePrice(t.exit_price)}</strong>
              ) : (
                <span className="text-primary font-mono text-[10px] italic">En Curso...</span>
              )}
            </div>
          </div>
        </div>

        {/* Fila 4: Banner de estado fuera de precio (si aplica) */}
        {isRejected && (
          <div className="pl-1.5 py-1 px-2 rounded bg-slate-800/60 border border-slate-700/60 flex items-center justify-between text-[9.5px] font-mono text-slate-300 gap-2">
            <span className="flex items-center gap-1 text-amber-400 font-semibold shrink-0">
              <span className="material-symbols-outlined text-[12px]">shield</span>
              FUERA PRECIO:
            </span>
            <span className="text-slate-300 text-right truncate text-[9px]" title={t.outcome_text || 'Orden no ejecutada por deslizamiento'}>
              {t.outcome_text && t.outcome_text !== 'FUERA PRECIO' ? t.outcome_text : 'Entrada cancelada por protección de Slippage'}
            </span>
          </div>
        )}

        {/* Banner de Salida de Seguridad antes de TPs del Canal */}
        {t.security_exit_before_tp && (
          <div className="pl-1.5 py-1 px-2 rounded bg-amber-950/40 border border-amber-500/40 flex items-center justify-between text-[9px] font-mono text-amber-200 gap-1.5">
            <span className="flex items-center gap-1 font-semibold text-amber-400 shrink-0">
              <span className="material-symbols-outlined text-[12px]">security</span>
              BLINDAJE BE:
            </span>
            <span className="text-right truncate text-[8.5px]">
              {t.security_exit_reason || `Posición cerrada en BE ($${safePrice(t.exit_price)}). El canal continuó hacia TP.`}
            </span>
          </div>
        )}

        <div className="pl-1.5 grid grid-cols-4 gap-1.5">
          <div className={`p-1 rounded flex flex-col transition-all border ${isSlTriggered ? 'bg-crimson-red/30 border-crimson-red' : 'bg-black/30 border-white/5'}`}>
            <span className="text-[8px] font-mono uppercase text-outline">SL</span>
            <span className={`text-[10px] font-mono font-bold ${isSlTriggered ? 'text-white' : 'text-crimson-red'}`}>{t.sl_price ? `$${safePrice(t.sl_price)}` : '---'}</span>
          </div>
          <div className={`p-1 rounded flex flex-col transition-all border ${isTp1Triggered ? 'bg-emerald-500/30 border-emerald-400' : 'bg-black/30 border-white/5'}`}>
            <span className="text-[8px] font-mono uppercase text-outline">TP1</span>
            <span className={`text-[10px] font-mono font-bold ${isTp1Triggered ? 'text-white' : 'text-emerald-400'}`}>{t.tp1 ? `$${safePrice(t.tp1)}` : '---'}</span>
          </div>
          <div className={`p-1 rounded flex flex-col transition-all border ${
            isTp2Triggered
              ? 'bg-emerald-500/30 border-emerald-400'
              : isChannelOnlyTp2
              ? 'bg-amber-500/15 border-dashed border-amber-400/60'
              : 'bg-black/30 border-white/5'
          }`}>
            <span className="text-[8px] font-mono uppercase text-outline flex items-center justify-between">
              TP2 {isChannelOnlyTp2 && <span className="text-[7px] text-amber-400 font-bold ml-0.5">CANAL</span>}
            </span>
            <span className={`text-[10px] font-mono font-bold ${
              isTp2Triggered
                ? 'text-white'
                : isChannelOnlyTp2
                ? 'text-amber-300'
                : 'text-emerald-400'
            }`}>{t.tp2 ? `$${safePrice(t.tp2)}` : '---'}</span>
          </div>
          <div className={`p-1 rounded flex flex-col transition-all border ${
            isTp3Triggered
              ? 'bg-emerald-500/30 border-emerald-400'
              : isChannelOnlyTp3
              ? 'bg-amber-500/15 border-dashed border-amber-400/60'
              : 'bg-black/30 border-white/5'
          }`}>
            <span className="text-[8px] font-mono uppercase text-outline flex items-center justify-between">
              TP3 {isChannelOnlyTp3 && <span className="text-[7px] text-amber-400 font-bold ml-0.5">CANAL</span>}
            </span>
            <span className={`text-[10px] font-mono font-bold ${
              isTp3Triggered
                ? 'text-white'
                : isChannelOnlyTp3
                ? 'text-amber-300'
                : 'text-emerald-400'
            }`}>{t.tp3 ? `$${safePrice(t.tp3)}` : '---'}</span>
          </div>
        </div>

        {!isRejected && !isPendingPullback && (t.status === 'WIN' || t.status === 'LOSS' || pnlNum !== null || t.exit_price) && (
          <div className="pt-1 border-t border-white/5 pl-1.5">
            <button type="button" onClick={() => onToggleExpand(cardKey)} className="w-full py-1 px-2 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-[9.5px] font-mono text-slate-300 flex items-center justify-between transition-colors">
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
  },
);
SignalCard.displayName = "SignalCard";
