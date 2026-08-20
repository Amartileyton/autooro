import React from 'react';

export interface SlotTradeData {
  slot_id: number;
  is_active: boolean;
  ticket_id?: string;
  side?: 'BUY' | 'SELL';
  lot_size?: number;
  entry_price?: number;
  current_sl?: number;
  initial_sl?: number;
  tp1?: number;
  tp2?: number;
  tp3?: number;
  current_price?: number;
  current_pnl?: number;
  status?: string;
}

interface PositionMatrixProps {
  slots: SlotTradeData[];
  onCloseSlot: (slotId: number) => Promise<void>;
}

export const PositionMatrix: React.FC<PositionMatrixProps> = ({ slots, onCloseSlot }) => {
  const activeCount = slots.filter((s) => s.is_active).length;

  return (
    <div className="term-panel col-span-1 lg:col-span-1 flex flex-col h-full overflow-hidden">
      <div className="bg-surface-container-highest px-3 py-1.5 border-b term-border flex justify-between items-center">
        <h2 className="text-label-sm text-outline uppercase tracking-widest">Matriz de Posiciones</h2>
        <span className="text-data-sm text-primary font-mono font-bold">
          {activeCount} / 4 ACTIVAS
        </span>
      </div>

      <div className="flex-1 p-2 grid grid-rows-4 gap-2 overflow-y-auto">
        {slots.map((slot) => {
          if (!slot.is_active || !slot.side) {
            return (
              <div
                key={slot.slot_id}
                className="border term-border border-dashed p-2 flex items-center justify-center text-outline opacity-60 bg-surface/50 rounded-sm"
              >
                <span className="text-data-sm font-mono tracking-wide">
                  SLOT #{slot.slot_id} — DISPONIBLE
                </span>
              </div>
            );
          }

          const isBuy = slot.side === 'BUY';
          const pnl = slot.current_pnl || 0;
          const isPnlPositive = pnl >= 0;
          const pnlSign = isPnlPositive ? '+' : '';

          const isTp1Reached = slot.status === 'TP1_HIT' || slot.status === 'TP2_HIT' || slot.status === 'CLOSED_TP';
          const isTp2Reached = slot.status === 'TP2_HIT' || slot.status === 'CLOSED_TP';
          const isTp3Reached = slot.status === 'CLOSED_TP';

          return (
            <div
              key={slot.slot_id}
              className={`border ${
                isBuy ? 'border-profit bg-profit' : 'border-loss bg-loss'
              } p-2 flex flex-col justify-between group relative rounded-sm transition-all`}
            >
              <div className="flex justify-between items-start">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-sm ${isBuy ? 'bg-emerald-green' : 'bg-crimson-red'}`} />
                  <span className={`text-data-md font-bold font-mono ${isBuy ? 'text-emerald-green' : 'text-crimson-red'}`}>
                    {slot.side}
                  </span>
                  <span className="text-data-sm text-on-surface font-mono">
                    {slot.lot_size?.toFixed(2)} L
                  </span>
                  <span className="text-[10px] text-outline font-mono">
                    (Slot #{slot.slot_id})
                  </span>
                </div>
                <span className={`text-data-sm font-bold font-mono ${isPnlPositive ? 'text-profit' : 'text-loss'}`}>
                  {pnlSign}${pnl.toFixed(2)}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-1 mt-1 text-data-sm font-mono">
                <div>
                  <span className="text-outline">ENT:</span> {slot.entry_price?.toFixed(2)}
                </div>
                <div>
                  <span className="text-outline">ACT:</span> {slot.current_price?.toFixed(2)}
                </div>
                <div>
                  <span className="text-outline">SL:</span> {slot.current_sl?.toFixed(2)}
                </div>
                <div className={isTp1Reached ? 'text-emerald-green font-bold' : 'text-outline'}>
                  {isTp2Reached ? 'TP2 ALCANZADO' : isTp1Reached ? 'TP1 (BE ACTIVO)' : `TP: ${slot.tp1?.toFixed(2)}`}
                </div>
              </div>

              {/* Barra de Progreso de Hitos TP1 -> TP2 -> TP3 */}
              <div className="mt-1 flex items-center justify-between text-[9px] font-mono text-outline relative w-full pt-1">
                <div className="absolute h-px bg-outline/30 top-1/2 left-0 right-0 -z-10" />
                <div
                  className={`absolute h-px bg-emerald-green top-1/2 left-0 -z-10 transition-all duration-300 ${
                    isTp3Reached ? 'w-full' : isTp2Reached ? 'w-2/3' : isTp1Reached ? 'w-1/3' : 'w-0'
                  }`}
                />
                
                <div className="flex flex-col items-center gap-0.5 bg-surface-container-highest px-1 rounded-sm">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-green" />
                  <span>Entrada</span>
                </div>
                <div className={`flex flex-col items-center gap-0.5 bg-surface-container-highest px-1 rounded-sm ${
                  isTp1Reached ? 'text-emerald-green font-semibold' : ''
                }`}>
                  <div className={`w-1.5 h-1.5 rounded-full ${isTp1Reached ? 'bg-emerald-green pulse-live' : 'bg-outline/50'}`} />
                  <span>TP1</span>
                </div>
                <div className={`flex flex-col items-center gap-0.5 bg-surface-container-highest px-1 rounded-sm ${
                  isTp2Reached ? 'text-emerald-green font-semibold' : ''
                }`}>
                  <div className={`w-1.5 h-1.5 rounded-full ${isTp2Reached ? 'bg-emerald-green pulse-live' : 'bg-outline/50'}`} />
                  <span>TP2</span>
                </div>
                <div className={`flex flex-col items-center gap-0.5 bg-surface-container-highest px-1 rounded-sm ${
                  isTp3Reached ? 'text-emerald-green font-semibold' : ''
                }`}>
                  <div className={`w-1.5 h-1.5 rounded-full ${isTp3Reached ? 'bg-emerald-green pulse-live' : 'bg-outline/50'}`} />
                  <span>TP3</span>
                </div>
              </div>

              {/* Botón de Cierre Manual en Hover */}
              <div className="absolute inset-0 bg-[#1e1f26]/90 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-sm">
                <button
                  onClick={() => onCloseSlot(slot.slot_id)}
                  className="bg-surface px-4 py-1.5 border border-outline hover:border-primary text-primary text-label-sm font-bold transition-colors shadow-sm"
                >
                  CERRAR A MERCADO
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
