import React, { useState } from 'react';

export interface SlotTradeData {
  slot_id: number;
  is_active: boolean;
  ticket_id?: string;
  side?: 'BUY' | 'SELL';
  lot_size?: number;
  initial_lot_size?: number;
  margin_usd?: number;
  entry_price?: number;
  current_sl?: number;
  initial_sl?: number;
  tp1?: number;
  tp2?: number;
  tp3?: number;
  current_price?: number;
  current_pnl?: number;
  realized_cash_pnl?: number;
  peak_price?: number;
  is_infinite_trailing?: boolean;
  status?: string;
  channel_name?: string;
}

interface PositionMatrixProps {
  slots: SlotTradeData[];
  currentPrice: number;
  onCloseSlot: (slotId: number) => Promise<void> | void;
}

export const PositionMatrix: React.FC<PositionMatrixProps> = ({ slots = [], currentPrice, onCloseSlot }) => {
  const safeSlots = Array.isArray(slots) ? slots : [];
  const activeCount = safeSlots.filter((s) => s.is_active).length;
  // Estado para controlar qué tarjetas están expandidas (Slot #1 expandido por defecto)
  const [expandedSlots, setExpandedSlots] = useState<Record<number, boolean>>({
    1: true,
  });

  const toggleSlotExpand = (slotId: number) => {
    setExpandedSlots((prev) => ({
      ...prev,
      [slotId]: !prev[slotId],
    }));
  };

  return (
    <div className="flex flex-col h-full w-full overflow-hidden bg-[#12141c] border border-outline-variant rounded-md min-h-0 select-none">
      {/* Cabecera de la Matriz Fija */}
      <div className="bg-surface-container px-3 py-2 border-b border-outline-variant flex justify-between items-center shrink-0">
        <h2 className="text-label-sm text-white font-bold uppercase tracking-widest flex items-center gap-1.5 font-mono">
          <span className="material-symbols-outlined text-[16px] text-slate-400">grid_view</span>
          Matriz de Posiciones
        </h2>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-outline-variant text-white font-bold">
          {activeCount} / 4 ACTIVAS
        </span>
      </div>

      {/* Contenedor con Scroll Fluido y Tarjetas Plegables Suaves */}
      <div className="flex-1 p-2 space-y-2 overflow-y-auto min-h-0 pr-1.5 scrollbar-thin">
        {safeSlots.map((slot) => {
          if (!slot.is_active || !slot.side) {
            return (
              <div
                key={slot.slot_id}
                className="border border-dashed border-slate-700/80 rounded-md p-3 flex flex-col items-center justify-center bg-[#0c0d12]/70 text-white group hover:border-slate-500 transition-all duration-200 shrink-0 cursor-default"
              >
                <span className="material-symbols-outlined text-[18px] text-slate-400 mb-0.5 group-hover:scale-110 transition-transform duration-200">
                  check_box_outline_blank
                </span>
                <span className="text-[11px] font-mono tracking-wider font-bold text-white">
                  SLOT #{slot.slot_id} — DISPONIBLE
                </span>
                <span className="text-[9px] font-mono text-slate-400 mt-0.5">
                  Esperando asignación de señal
                </span>
              </div>
            );
          }

          const isBuy = slot.side === 'BUY';
          const lot = slot.lot_size || 0.22;
          const entryPrice = slot.entry_price || (currentPrice > 0 ? currentPrice : 4580.00);
          const livePrice = currentPrice > 0 ? currentPrice : (slot.current_price || entryPrice);

          // PnL Dinámico en tiempo real ligado a la cotización spot en vivo (1 lote = 100 oz Oro)
          const priceDiff = isBuy ? (livePrice - entryPrice) : (entryPrice - livePrice);
          const pnl = priceDiff * lot * 100;
          const isProfit = pnl >= 0;
          const pnlSign = isProfit ? '+' : '';

          const isExpanded = Boolean(expandedSlots[slot.slot_id]);

          // Determinación Dinámica de Take Profits / Stop Loss alcanzados en base al precio spot actual
          const isTp1Hit = Boolean(
            (isBuy && slot.tp1 && livePrice >= slot.tp1) ||
            (!isBuy && slot.tp1 && livePrice <= slot.tp1) ||
            slot.status === 'TP1_HIT' || slot.status === 'TP2_HIT' || slot.status === 'CLOSED_TP'
          );

          const isTp2Hit = Boolean(
            (isBuy && slot.tp2 && livePrice >= slot.tp2) ||
            (!isBuy && slot.tp2 && livePrice <= slot.tp2) ||
            slot.status === 'TP2_HIT' || slot.status === 'CLOSED_TP'
          );

          const isTp3Hit = Boolean(
            (isBuy && slot.tp3 && livePrice >= slot.tp3) ||
            (!isBuy && slot.tp3 && livePrice <= slot.tp3) ||
            slot.status === 'CLOSED_TP'
          );

          const isSlHit = Boolean(
            (isBuy && slot.current_sl && livePrice <= slot.current_sl) ||
            (!isBuy && slot.current_sl && livePrice >= slot.current_sl) ||
            slot.status === 'CLOSED_SL'
          );

          return (
            <div
              key={slot.slot_id}
              onClick={() => toggleSlotExpand(slot.slot_id)}
              className={`bg-[#0b0c10] border rounded-md p-2.5 relative overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] text-white shadow-sm shrink-0 cursor-pointer group active:scale-[0.995] ${
                isExpanded
                  ? 'border-slate-600 shadow-[0_4px_16px_rgba(0,0,0,0.4)]'
                  : 'border-slate-800 hover:border-slate-700 hover:bg-[#0e0f15]'
              }`}
            >
              {/* Borde lateral indicador de dirección (Verde para BUY, Rojo para SELL) */}
              <div
                className={`absolute top-0 left-0 w-1.5 h-full transition-colors duration-200 ${
                  isBuy ? 'bg-emerald-500' : 'bg-red-500'
                }`}
              />

              {/* Fila 1: Slot #, Dirección (sin etiqueta de lote) y PnL con Chevron con rotación fluida */}
              <div className="flex justify-between items-center pl-1.5 gap-2">
                <div className="flex items-center gap-1.5">
                  <span className="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-white">
                    SLOT #{slot.slot_id}
                  </span>
                  <span
                    className={`text-[12px] font-mono font-bold flex items-center gap-0.5 ${
                      isBuy ? 'text-emerald-400' : 'text-red-400'
                    }`}
                  >
                    <span className="material-symbols-outlined text-[15px]">
                      {isBuy ? 'arrow_upward' : 'arrow_downward'}
                    </span>
                    {slot.side} XAUUSD
                  </span>
                </div>

                {/* PnL en Verde / Rojo + Chevron animado */}
                <div className="flex items-center gap-1.5">
                  <span
                    className={`text-[12px] font-mono font-bold px-2 py-0.5 rounded transition-colors duration-200 ${
                      isProfit
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                        : 'bg-red-500/20 text-red-400 border border-red-500/40'
                    }`}
                  >
                    {pnlSign}${pnl.toFixed(2)}
                  </span>
                  <span
                    className={`material-symbols-outlined text-[18px] transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${
                      isExpanded ? 'rotate-180 text-white' : 'rotate-0 text-slate-400 group-hover:text-slate-200'
                    }`}
                  >
                    expand_more
                  </span>
                </div>
              </div>

              {/* Insignia de Estado y Blindaje de Beneficios (Tier Badges) */}
              <div className="pl-1.5 flex flex-wrap items-center gap-1.5 mt-1.5">
                {(slot.status === 'TP3_TRAILING' || slot.is_infinite_trailing) ? (
                  <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 text-[9px] font-mono font-bold flex items-center gap-1 animate-pulse">
                    <span className="material-symbols-outlined text-[12px]">rocket_launch</span>
                    INFINITE RUNNER (Pico: ${slot.peak_price?.toFixed(2) || livePrice.toFixed(2)})
                  </span>
                ) : slot.status === 'TP2_HIT' ? (
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/50 text-[9px] font-mono font-bold flex items-center gap-1">
                    <span className="material-symbols-outlined text-[12px]">lock</span>
                    TP1 LOCKED (75% Asegurado)
                  </span>
                ) : slot.status === 'TP1_HIT' ? (
                  <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 text-[9px] font-mono font-bold flex items-center gap-1">
                    <span className="material-symbols-outlined text-[12px]">shield</span>
                    BE+ SPREAD (50% en Caja)
                  </span>
                ) : (
                  <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700 text-[9px] font-mono font-semibold">
                    100% Volumen ({lot}L)
                  </span>
                )}

                {Boolean(slot.realized_cash_pnl && slot.realized_cash_pnl > 0) && (
                  <span className="px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-[9px] font-mono font-bold">
                    Caja: +${slot.realized_cash_pnl?.toFixed(2)}
                  </span>
                )}
              </div>

              {/* Fila 2: Precios de Entrada, Actual e Inversión */}
              <div className="pl-1.5 bg-[#14151e] p-1.5 rounded border border-slate-800 grid grid-cols-3 gap-1.5 text-[11px] font-mono mt-1.5">
                <div>
                  <span className="text-slate-400 text-[9px] block font-medium">ENTRADA</span>
                  <strong className="text-white font-bold">${entryPrice.toFixed(2)}</strong>
                </div>
                <div>
                  <span className="text-slate-400 text-[9px] block font-medium">ACTUAL</span>
                  <strong className="text-white font-bold pulse-live">${livePrice.toFixed(2)}</strong>
                </div>
                <div>
                  <span className="text-slate-400 text-[9px] block font-medium">RESTANTE</span>
                  <strong className="text-slate-200 font-semibold">{lot}L <span className="text-[9px] text-slate-400 font-normal">(${slot.margin_usd?.toFixed(0) || '1,000'})</span></strong>
                </div>
              </div>

              {/* CONTENIDO DESPLEGABLE CON ANIMACIÓN FLUIDA Y NATURAL (CSS GRID ACCORDION) */}
              <div
                className={`grid transition-[grid-template-rows,opacity] duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${
                  isExpanded
                    ? 'grid-rows-[1fr] opacity-100 mt-2 pt-2 border-t border-slate-800/80'
                    : 'grid-rows-[0fr] opacity-0 mt-0 pt-0 border-t-0 border-transparent pointer-events-none'
                }`}
              >
                <div className="overflow-hidden min-h-0 space-y-2">
                  {/* Fila 3: Rejilla de Niveles SL, TP1, TP2, TP3 con sombreado dinámico */}
                  <div className="pl-1.5 grid grid-cols-4 gap-1">
                    {/* SL */}
                    <div
                      className={`p-1 rounded flex flex-col transition-all duration-200 border ${
                        isSlHit
                          ? 'bg-red-500/30 border-red-500 ring-1 ring-red-400'
                          : 'bg-[#14151e] border-slate-800'
                      }`}
                    >
                      <span className="text-[8px] font-mono uppercase text-slate-400 font-bold">
                        SL
                      </span>
                      <span className="text-[10px] font-mono font-bold text-red-400 mt-0.5">
                        ${slot.current_sl?.toFixed(2) || '---'}
                      </span>
                    </div>

                    {/* TP1 */}
                    <div
                      className={`p-1 rounded flex flex-col transition-all duration-200 border ${
                        isTp1Hit
                          ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
                          : 'bg-[#14151e] border-slate-800'
                      }`}
                    >
                      <span className={`text-[8px] font-mono uppercase font-bold ${isTp1Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
                        TP1
                      </span>
                      <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
                        ${slot.tp1?.toFixed(2) || '---'}
                      </span>
                    </div>

                    {/* TP2 */}
                    <div
                      className={`p-1 rounded flex flex-col transition-all duration-200 border ${
                        isTp2Hit
                          ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
                          : 'bg-[#14151e] border-slate-800'
                      }`}
                    >
                      <span className={`text-[8px] font-mono uppercase font-bold ${isTp2Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
                        TP2
                      </span>
                      <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
                        ${slot.tp2?.toFixed(2) || '---'}
                      </span>
                    </div>

                    {/* TP3 */}
                    <div
                      className={`p-1 rounded flex flex-col transition-all duration-200 border ${
                        isTp3Hit
                          ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
                          : 'bg-[#14151e] border-slate-800'
                      }`}
                    >
                      <span className={`text-[8px] font-mono uppercase font-bold ${isTp3Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
                        TP3
                      </span>
                      <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
                        ${slot.tp3?.toFixed(2) || '---'}
                      </span>
                    </div>
                  </div>

                  {/* Fila 4: Ticket y Botón Cerrar Slot en blanco */}
                  <div className="pl-1.5 flex justify-between items-center pt-1">
                    <span className="text-[9px] font-mono text-slate-400">
                      Ticket: <span className="text-white font-semibold">{slot.ticket_id || 'TCK-88231'}</span>
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onCloseSlot(slot.slot_id);
                      }}
                      className="text-[9px] font-mono px-2.5 py-0.5 rounded bg-white hover:bg-slate-200 text-slate-900 border border-white shadow-sm transition-all font-bold flex items-center gap-1 active:scale-95"
                    >
                      <span className="material-symbols-outlined text-[11px] text-slate-900">close</span>
                      Cerrar Slot
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
