import React, { useState } from 'react';
import type { SlotTradeData } from './PositionMatrix';

interface LiveChartProps {
  currentPrice: number;
  activeSlots: SlotTradeData[];
}

export const LiveChart: React.FC<LiveChartProps> = ({ currentPrice, activeSlots }) => {
  const [timeframe, setTimeframe] = useState<'1M' | '5M' | '15M' | '1H'>('15M');
  const activeTrade = activeSlots.find((s) => s.is_active && s.side);

  return (
    <div className="term-panel col-span-1 lg:col-span-2 flex flex-col h-full relative overflow-hidden">
      {/* Header del Gráfico */}
      <div className="bg-surface-container-highest px-3 py-1.5 border-b term-border flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <h2 className="text-label-sm text-amber-gold font-bold uppercase tracking-widest flex items-center gap-1">
            <span className="material-symbols-outlined text-[16px]">show_chart</span>
            XAUUSD SPOT
          </h2>

          <div className="flex gap-1">
            {(['1M', '5M', '15M', '1H'] as const).map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-2 py-0.5 border text-label-sm rounded-sm transition-colors ${
                  timeframe === tf
                    ? 'border-primary text-primary bg-primary/10 font-bold'
                    : 'term-border text-outline bg-surface hover:text-on-surface'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-data-sm font-mono text-outline">
            Spread: <strong className="text-primary">15c</strong>
          </span>
        </div>
      </div>

      {/* Canvas del Gráfico con Grid Bloomberg */}
      <div className="flex-1 relative bg-[#131722] w-full h-full chart-grid overflow-hidden">
        {/* Background Overlay */}
        <div 
          className="absolute inset-0 opacity-20 bg-cover bg-center" 
          style={{
            backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBe_LWFSLFPlI2EAYuAEWBsAMFmEZqf3U_yVdXTWB6MKdMINOUz6-7SB3w-6xO6EC7-qP-sVXWsHfq8xaBq52OlzDHZLTfNNWQK_wa4oOx5V8EkGsrHURquzIL2Wn6mFlNJ8jrcQK81JiUrdojrg2p_iXbZEHH-xmCb46XgPnEkZjjOO2QrfdbutHbKx44djJz5ULIDSO5CNEC3P0ZkSDy0NdAY1RNqLx0F-juUJpefBO_vmZvtA-ZhAA')",
            mixBlendMode: 'screen'
          }}
        />

        {/* Líneas de Entrada, SL y TP si hay trade activo */}
        {activeTrade && (
          <>
            {/* Línea de Entrada */}
            <div className="absolute top-[42%] left-0 right-16 border-t border-dashed border-emerald-green/70 z-20 flex items-center">
              <div className="bg-emerald-green/20 text-emerald-green text-[10px] font-mono px-1.5 py-0.5 border border-emerald-green/50 -mt-3 ml-2 rounded-sm backdrop-blur-sm">
                ENT {activeTrade.side} {activeTrade.lot_size?.toFixed(2)}L @ ${activeTrade.entry_price?.toFixed(2)}
              </div>
            </div>

            {/* Línea de Stop Loss */}
            <div className="absolute top-[28%] left-0 right-16 border-t border-dashed border-crimson-red/70 z-20 flex items-center">
              <div className="bg-crimson-red/20 text-crimson-red text-[10px] font-mono px-1.5 py-0.5 border border-crimson-red/50 -mt-3 ml-2 rounded-sm backdrop-blur-sm">
                SL @ ${activeTrade.current_sl?.toFixed(2)}
              </div>
            </div>

            {/* Línea de Take Profit */}
            <div className="absolute top-[65%] left-0 right-16 border-t border-dashed border-profit/70 z-20 flex items-center">
              <div className="bg-profit/20 text-profit text-[10px] font-mono px-1.5 py-0.5 border border-profit/50 -mt-3 ml-2 rounded-sm backdrop-blur-sm">
                TP1 @ ${activeTrade.tp1?.toFixed(2)}
              </div>
            </div>
          </>
        )}

        {/* Price Ladder lateral derecho */}
        <div className="absolute right-0 top-0 bottom-0 w-20 border-l border-[#2a2e39] bg-[#131722] flex flex-col justify-around text-[10px] text-[#787b86] font-mono pr-2 text-right z-30">
          <div>{(currentPrice + 5).toFixed(2)}</div>
          <div>{(currentPrice + 2.5).toFixed(2)}</div>
          <div className="text-profit font-bold border-y border-profit/40 bg-profit/20 py-0.5">
            ${currentPrice.toFixed(2)}
          </div>
          <div>{(currentPrice - 2.5).toFixed(2)}</div>
          <div>{(currentPrice - 5).toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
};
