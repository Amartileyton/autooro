import React, { useEffect, useRef } from 'react';
import type { SlotTradeData } from './PositionMatrix';

interface LiveChartProps {
  currentPrice: number;
  activeSlots: SlotTradeData[];
}

export const LiveChart: React.FC<LiveChartProps> = ({ currentPrice, activeSlots }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const activeTrade = activeSlots.find((s) => s.is_active && s.side);

  useEffect(() => {
    if (!containerRef.current) return;
    containerRef.current.innerHTML = '';

    const widgetDiv = document.createElement('div');
    widgetDiv.className = 'tradingview-widget-container__widget';
    widgetDiv.style.height = '100%';
    widgetDiv.style.width = '100%';

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
    script.type = 'text/javascript';
    script.async = true;
    script.innerHTML = JSON.stringify({
      autosize: true,
      symbol: 'OANDA:XAUUSD',
      interval: '60', // 1 Hora por defecto
      timezone: 'Etc/UTC',
      theme: 'dark',
      style: '1',
      locale: 'es',
      enable_publishing: false,
      hide_top_toolbar: false, // Controles NATIVOS de TradingView (temporalidades, indicadores, velas)
      hide_side_toolbar: true, // Ocultar herramientas de dibujo laterales
      hide_volume: true, // Ocultar subpanel inferior de volumen
      allow_symbol_change: false,
      save_image: false,
      calendar: false,
      withdateranges: false,
      support_host: 'https://www.tradingview.com',
      backgroundColor: '#0a0d14',
      gridColor: 'rgba(42, 46, 57, 0.15)',
      studies: [
        'MASimple@tv-basicstudies',
        'EMA@tv-basicstudies'
      ],
      studies_overrides: {
        'moving average.length': 50,
        'moving average.color': '#818cf8',
        'moving average.linewidth': 2,
        'moving average exponential.length': 20,
        'moving average exponential.color': '#f59e0b',
        'moving average exponential.linewidth': 2
      },
      overrides: {
        'paneProperties.background': '#0a0d14',
        'paneProperties.backgroundType': 'solid',
        'paneProperties.vertGridProperties.color': 'rgba(42, 46, 57, 0.10)',
        'paneProperties.horzGridProperties.color': 'rgba(42, 46, 57, 0.10)',
        'mainSeriesProperties.candleStyle.upColor': '#10b981',
        'mainSeriesProperties.candleStyle.downColor': '#ef4444',
        'mainSeriesProperties.candleStyle.wickUpColor': '#10b981',
        'mainSeriesProperties.candleStyle.wickDownColor': '#ef4444',
        'mainSeriesProperties.candleStyle.borderUpColor': '#10b981',
        'mainSeriesProperties.candleStyle.borderDownColor': '#ef4444',
        'scalesProperties.textColor': '#94a3b8',
        'scalesProperties.lineColor': '#1e293b'
      }
    });

    const wrapper = document.createElement('div');
    wrapper.className = 'tradingview-widget-container';
    wrapper.style.height = '100%';
    wrapper.style.width = '100%';
    wrapper.appendChild(widgetDiv);
    wrapper.appendChild(script);

    containerRef.current.appendChild(wrapper);
  }, []);

  return (
    <div className="term-panel col-span-1 lg:col-span-2 flex flex-col h-full relative overflow-hidden bg-[#0a0d14]">
      {/* Header del Gráfico con Indicación de Slot Activo y Feed */}
      <div className="bg-surface-container-highest px-3 py-1 border-b term-border flex justify-between items-center z-10">
        <div className="flex items-center gap-3">
          <h2 className="text-label-sm text-amber-gold font-bold uppercase tracking-widest flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[16px]">show_chart</span>
            XAUUSD SPOT &bull; FEED OFICIAL TRADINGVIEW
          </h2>
          <div className="hidden sm:flex items-center gap-2 text-[11px] font-mono">
            <span className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
              EMA 20
            </span>
            <span className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
              SMA 50
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {activeTrade && (
            <span className="text-label-sm font-mono px-2 py-0.5 rounded bg-primary/20 text-primary border border-primary/30 animate-pulse">
              Slot Activo: {activeTrade.side} {activeTrade.lot_size?.toFixed(2)}L @ ${activeTrade.entry_price?.toFixed(2)}
            </span>
          )}
          <span className="text-data-sm font-mono text-outline">
            Precio: <strong className="text-amber-gold font-bold">${currentPrice > 0 ? currentPrice.toFixed(2) : '---'}</strong>
          </span>
        </div>
      </div>

      {/* Contenedor del Gráfico con Controles Nativos de TradingView */}
      <div className="flex-1 relative w-full h-[450px] lg:h-full overflow-hidden" ref={containerRef}>
        <div className="w-full h-full flex items-center justify-center text-outline text-label-sm">
          Cargando feed de TradingView...
        </div>
      </div>
    </div>
  );
};
