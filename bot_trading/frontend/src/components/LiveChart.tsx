import React, { useEffect, useRef } from 'react';
import type { SlotTradeData } from './PositionMatrix';

declare global {
  interface Window {
    TradingView?: any;
  }
}

export interface ChartAssetInfo {
  name: string;
  ticker: string;
  tvSymbol: string;
  price: number;
  decimals?: number;
  change?: number;
}

interface LiveChartProps {
  currentPrice: number;
  activeSlots: SlotTradeData[];
  selectedAsset?: ChartAssetInfo;
  onResetToGold?: () => void;
}

export const LiveChart: React.FC<LiveChartProps> = ({
  currentPrice,
  activeSlots,
  selectedAsset = {
    name: 'Oro Spot',
    ticker: 'XAUUSD (Spot)',
    tvSymbol: 'OANDA:XAUUSD',
    price: currentPrice || 4652.60,
    decimals: 2,
    change: 0.65,
  },
  onResetToGold,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const activeTvSymbol = selectedAsset?.tvSymbol || 'OANDA:XAUUSD';
  const isGold = activeTvSymbol === 'OANDA:XAUUSD';

  // Mostrar precio del activo actual (si es Oro usar el precio de telemetría en vivo, si no el precio del activo)
  const displayPrice = isGold
    ? (currentPrice > 0 ? currentPrice : selectedAsset.price)
    : selectedAsset.price;
  const decimals = selectedAsset.decimals ?? 2;

  useEffect(() => {
    const renderWidget = () => {
      if (!containerRef.current) return;
      containerRef.current.innerHTML = '';

      const widgetContainerId = 'tradingview_native_chart';
      const chartDiv = document.createElement('div');
      chartDiv.id = widgetContainerId;
      chartDiv.style.width = '100%';
      chartDiv.style.height = '100%';
      chartDiv.style.backgroundColor = '#000000';
      containerRef.current.appendChild(chartDiv);

      if (window.TradingView) {
        new window.TradingView.widget({
          autosize: true,
          symbol: activeTvSymbol,
          interval: '60', // 1h por defecto
          timezone: 'Europe/Madrid',
          theme: 'dark',
          style: '1',
          locale: 'es',
          toolbar_bg: '#000000',
          enable_publishing: false,
          hide_top_toolbar: false, // BARRA NATIVA DE TRADINGVIEW
          hide_side_toolbar: true, // OCULTAR panel lateral de dibujo
          withdateranges: false, // OCULTAR barra inferior de rangos
          hide_volume: false, // MOSTRAR volumen nativo en las velas
          allow_symbol_change: false,
          save_image: false,
          calendar: false,
          container_id: widgetContainerId,
          backgroundColor: '#000000',
          gridColor: '#141414',
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
            'moving average exponential.linewidth': 2,
            'volume.volume.color.0': '#ef4444',
            'volume.volume.color.1': '#10b981'
          },
          overrides: {
            'paneProperties.background': '#000000',
            'paneProperties.backgroundType': 'solid',
            'paneProperties.vertGridProperties.color': '#141414',
            'paneProperties.horzGridProperties.color': '#141414',
            'scalesProperties.textColor': '#94a3b8',
            'scalesProperties.lineColor': '#222222',
            'mainSeriesProperties.candleStyle.upColor': '#10b981',
            'mainSeriesProperties.candleStyle.downColor': '#ef4444',
            'mainSeriesProperties.candleStyle.wickUpColor': '#10b981',
            'mainSeriesProperties.candleStyle.wickDownColor': '#ef4444',
            'mainSeriesProperties.candleStyle.borderUpColor': '#10b981',
            'mainSeriesProperties.candleStyle.borderDownColor': '#ef4444'
          }
        });
      } else {
        const script = document.createElement('script');
        script.src = 'https://s3.tradingview.com/tv.js';
        script.type = 'text/javascript';
        script.async = true;
        script.onload = () => {
          renderWidget();
        };
        document.head.appendChild(script);
      }
    };

    renderWidget();
  }, [activeTvSymbol]);

  return (
    <div className="flex flex-col h-full w-full relative overflow-hidden bg-black border border-outline-variant rounded-md min-h-0 select-none">
      {/* Barra de Estado de la Tarjeta del Gráfico */}
      <div className="bg-[#080808] px-3 py-1.5 border-b border-outline-variant/60 flex justify-between items-center z-10 shrink-0">
        <div className="flex items-center gap-2">
          <h2 className="text-label-sm text-slate-200 font-bold uppercase tracking-widest flex items-center gap-1.5 font-mono">
            <span className="material-symbols-outlined text-[16px] text-slate-400">show_chart</span>
            <span>{selectedAsset.name}</span>
            <span className="text-slate-500 text-[11px] font-normal font-mono">({activeTvSymbol})</span>
          </h2>

          {/* Botón para volver a XAUUSD si se está viendo otro activo */}
          {!isGold && (
            <button
              onClick={onResetToGold}
              title="Volver a la vista principal de Oro (XAUUSD)"
              className="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/15 border border-amber-500/40 text-amber-300 hover:bg-amber-500/25 transition-all cursor-pointer ml-1"
            >
              <span className="material-symbols-outlined text-[12px]">replay</span>
              <span>Volver a Oro</span>
            </button>
          )}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-data-sm font-mono text-slate-400">
            PRECIO SPOT:{' '}
            <strong className="text-slate-100 font-bold">
              ${displayPrice > 0 ? displayPrice.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) : '---'}
            </strong>
          </span>
        </div>
      </div>

      {/* Contenedor del Gráfico de TradingView Nativo */}
      <div
        className="flex-1 relative w-full h-full overflow-hidden bg-black"
        ref={containerRef}
        style={{ minHeight: '450px', backgroundColor: '#000000' }}
      >
        <div className="w-full h-full flex items-center justify-center text-outline text-label-sm bg-black">
          Cargando gráfico interactivo de {selectedAsset.name}...
        </div>
      </div>
    </div>
  );
};
