import React, { useState } from 'react';
import { safePrice, safeNum } from '@/utils/formatters';

export interface PositionCardState {
  slot_id: number;
  is_active: boolean;
  ticket_id?: string;
  side?: 'BUY' | 'SELL';
  lot_size?: number;
  margin_usd?: number;
  entry_price?: number;
  current_price?: number;
  current_sl?: number;
  initial_sl?: number;
  tp1?: number;
  tp2?: number;
  tp3?: number;
  current_pnl?: number;
  status?: 'OPEN' | 'TP1_HIT' | 'TP2_HIT' | 'CLOSED_TP' | 'CLOSED_SL' | 'AVAILABLE';
  channel_name?: string;
  open_time?: string;
}

// Componente individual de la tarjeta de posición: Fondo Negro con Letras Blancas
export const PositionCard: React.FC<{
  slot: PositionCardState;
  onClose?: (slotId: number) => void;
}> = ({ slot, onClose }) => {
  if (!slot.is_active || !slot.side) {
    return (
      <div className="border border-dashed border-slate-700/80 rounded-md p-4 flex flex-col items-center justify-center bg-[#0c0d12]/70 min-h-[140px] text-white select-none group hover:border-slate-500 transition-all">
        <span className="material-symbols-outlined text-[24px] text-slate-400 mb-1 group-hover:scale-110 transition-transform">
          check_box_outline_blank
        </span>
        <span className="text-data-sm font-mono tracking-wider font-bold text-white">
          SLOT #{slot.slot_id} — DISPONIBLE
        </span>
        <span className="text-[10px] font-mono text-slate-400 mt-0.5">
          Esperando señal para asignación
        </span>
      </div>
    );
  }

  const isBuy = slot.side === 'BUY';
  const pnl = safeNum(slot.current_pnl, 0);
  const isProfit = pnl >= 0;
  const pnlSign = isProfit ? '+' : '';

  const isTp1Hit = slot.status === 'TP1_HIT' || slot.status === 'TP2_HIT' || (slot.status as string) === 'TP3_TRAILING' || slot.status === 'CLOSED_TP';
  const isTp2Hit = slot.status === 'TP2_HIT' || (slot.status as string) === 'TP3_TRAILING' || slot.status === 'CLOSED_TP';
  const isTp3Hit = (slot.status as string) === 'TP3_TRAILING' || slot.status === 'CLOSED_TP';

  return (
    <div className="bg-[#0b0c10] border border-slate-800 rounded-md p-3.5 relative overflow-hidden transition-all space-y-2.5 text-white shadow-sm">
      {/* Borde lateral indicador de dirección (Verde para BUY, Rojo para SELL) */}
      <div
        className={`absolute top-0 left-0 w-1.5 h-full ${
          isBuy ? 'bg-emerald-500' : 'bg-red-500'
        }`}
      />

      {/* Fila 1: Cabecera con Slot #, BUY en verde / SELL en rojo, Lote y PnL */}
      <div className="flex justify-between items-center pl-1.5 gap-2">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-white">
            SLOT #{slot.slot_id}
          </span>
          <span
            className={`text-data-md font-mono font-bold flex items-center gap-1 ${
              isBuy ? 'text-emerald-400' : 'text-red-400'
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">
              {isBuy ? 'arrow_upward' : 'arrow_downward'}
            </span>
            {slot.side} XAUUSD
          </span>
          <span className="text-[11px] font-mono text-white bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700 font-bold">
            {safePrice(slot.lot_size, '0.09')}L
          </span>
        </div>

        {/* PnL en Verde (ganancia) o Rojo (pérdida) */}
        <div className="flex items-center gap-2">
          <span
            className={`text-data-lg font-mono font-bold px-2 py-0.5 rounded ${
              isProfit
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                : 'bg-red-500/20 text-red-400 border border-red-500/40'
            }`}
          >
            {pnlSign}${safePrice(pnl, '0.00')}
          </span>
        </div>
      </div>

      {/* Fila 2: Precios de Entrada y Actual (Fondo negro con letras blancas) */}
      <div className="pl-1.5 bg-[#14151e] p-2 rounded border border-slate-800 grid grid-cols-3 gap-2 text-data-sm font-mono">
        <div>
          <span className="text-slate-400 text-[10px] block font-medium">ENTRADA</span>
          <strong className="text-white font-bold">${safePrice(slot.entry_price, '2650.00')}</strong>
        </div>
        <div>
          <span className="text-slate-400 text-[10px] block font-medium">ACTUAL</span>
          <strong className="text-white font-bold">${safePrice(slot.current_price, '2650.00')}</strong>
        </div>
        <div>
          <span className="text-slate-400 text-[10px] block font-medium">MARGEN</span>
          <strong className="text-slate-200 font-semibold">${safeNum(slot.margin_usd, 250).toFixed(0)}</strong>
        </div>
      </div>

      {/* Fila 3: Niveles de SL y TPs */}
      <div className="pl-1.5 grid grid-cols-4 gap-1.5">
        {/* SL */}
        <div className="p-1 rounded bg-[#14151e] border border-slate-800 flex flex-col">
          <span className="text-[8px] font-mono text-slate-400 uppercase font-bold">SL</span>
          <span className="text-[10px] font-mono font-bold text-red-400 mt-0.5">
            ${safePrice(slot.current_sl, '---')}
          </span>
        </div>

        {/* TP1 */}
        <div
          className={`p-1 rounded flex flex-col transition-all border ${
            isTp1Hit
              ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
              : 'bg-[#14151e] border-slate-800'
          }`}
        >
          <span className={`text-[8px] font-mono uppercase font-bold ${isTp1Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
            TP1
          </span>
          <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
            ${safePrice(slot.tp1, '---')}
          </span>
        </div>

        {/* TP2 */}
        <div
          className={`p-1 rounded flex flex-col transition-all border ${
            isTp2Hit
              ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
              : 'bg-[#14151e] border-slate-800'
          }`}
        >
          <span className={`text-[8px] font-mono uppercase font-bold ${isTp2Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
            TP2
          </span>
          <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
            ${safePrice(slot.tp2, '---')}
          </span>
        </div>

        {/* TP3 */}
        <div
          className={`p-1 rounded flex flex-col transition-all border ${
            isTp3Hit
              ? 'bg-emerald-500/30 border-emerald-400 ring-1 ring-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.3)]'
              : 'bg-[#14151e] border-slate-800'
          }`}
        >
          <span className={`text-[8px] font-mono uppercase font-bold ${isTp3Hit ? 'text-emerald-300' : 'text-slate-400'}`}>
            TP3
          </span>
          <span className="text-[10px] font-mono font-bold text-emerald-400 mt-0.5">
            ${safePrice(slot.tp3, '---')}
          </span>
        </div>
      </div>

      {/* Fila 4: Acciones rápidas (Botón Cerrar Slot en blanco) */}
      <div className="pl-1.5 flex justify-between items-center pt-1 border-t border-slate-800/80">
        <span className="text-[10px] font-mono text-slate-400">
          Ticket: <span className="text-white font-semibold">{slot.ticket_id || 'TCK-88231'}</span>
        </span>
        {onClose && (
          <button
            onClick={() => onClose(slot.slot_id)}
            className="text-[10px] font-mono px-2.5 py-0.5 rounded bg-white hover:bg-slate-200 text-slate-900 border border-white shadow-sm transition-all font-bold flex items-center gap-1"
          >
            <span className="material-symbols-outlined text-[13px] text-slate-900">close</span>
            Cerrar Slot
          </button>
        )}
      </div>
    </div>
  );
};

export const PositionCardWorkbench: React.FC = () => {
  const [mockSlots, setMockSlots] = useState<PositionCardState[]>([
    {
      slot_id: 1,
      is_active: true,
      ticket_id: 'TCK-99412',
      side: 'BUY',
      lot_size: 0.22,
      margin_usd: 1000,
      entry_price: 4580.50,
      current_price: 4585.20,
      current_sl: 4580.50,
      initial_sl: 4575.00,
      tp1: 4583.50,
      tp2: 4588.00,
      tp3: 4595.00,
      current_pnl: 103.40,
      status: 'TP1_HIT',
      channel_name: 'Chartoro FX',
      open_time: '12:45:10'
    },
    {
      slot_id: 2,
      is_active: true,
      ticket_id: 'TCK-99415',
      side: 'SELL',
      lot_size: 0.22,
      margin_usd: 1000,
      entry_price: 4584.00,
      current_price: 4586.80,
      current_sl: 4589.00,
      initial_sl: 4589.00,
      tp1: 4581.00,
      tp2: 4578.00,
      tp3: 4572.00,
      current_pnl: -61.60,
      status: 'OPEN',
      channel_name: 'Gold Signals VIP',
      open_time: '12:51:22'
    },
    {
      slot_id: 3,
      is_active: false
    },
    {
      slot_id: 4,
      is_active: false
    }
  ]);

  const handleCloseSlot = (id: number) => {
    setMockSlots((prev) =>
      prev.map((s) => (s.slot_id === id ? { slot_id: id, is_active: false } : s))
    );
  };

  return (
    <div className="min-h-screen bg-[#0c0d12] text-on-surface p-6 font-sans">
      {/* Header del Workbench */}
      <div className="max-w-5xl mx-auto pb-6 border-b border-outline-variant flex justify-between items-center">
        <div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-amber-gold text-[24px]">view_quilt</span>
            <h1 className="text-xl font-bold text-slate-100 font-mono tracking-tight">
              Mesa de Trabajo / Diseñador de Tarjeta de Posiciones
            </h1>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Espacio aislado: fondo negro con letras blancas y acentos de color.
          </p>
        </div>

        <a
          href="/"
          className="px-3 py-1.5 rounded bg-surface border border-outline-variant hover:border-slate-400 text-slate-300 hover:text-white font-mono text-xs transition-colors flex items-center gap-1.5"
        >
          <span className="material-symbols-outlined text-[16px]">arrow_back</span>
          Volver al Dashboard
        </a>
      </div>

      {/* Galería de Tarjetas */}
      <div className="max-w-5xl mx-auto py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {mockSlots.map((slot) => (
            <div key={slot.slot_id} className="space-y-2">
              <div className="flex justify-between items-center text-xs font-mono text-slate-400 px-1">
                <span>Estado: {slot.is_active ? `ACTIVA (${slot.side})` : 'DISPONIBLE'}</span>
                {slot.status && <span className="text-slate-500 font-bold">{slot.status}</span>}
              </div>
              <PositionCard slot={slot} onClose={handleCloseSlot} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
