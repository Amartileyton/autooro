import React, { useState, useEffect } from 'react';

export interface MarketAsset {
  id: string;
  name: string;
  ticker: string;
  tvSymbol: string;
  market: string;
  type: string;
  description: string;
  price: number;
  change: number;
  decimals: number;
}

const INITIAL_MARKET_ASSETS: MarketAsset[] = [
  {
    id: 'spx',
    name: 'S&P 500',
    ticker: 'SPX / ^GSPC',
    tvSymbol: 'OANDA:SPX500USD',
    market: 'Estados Unidos',
    type: 'Renta Variable',
    description: '500 mayores empresas cotizadas en EE. UU.; referencia macroeconómica mundial. ISIN: US78378X1072',
    price: 7661.40,
    change: -0.20,
    decimals: 2,
  },
  {
    id: 'ndx',
    name: 'Nasdaq 100',
    ticker: 'NDX / ^NDX',
    tvSymbol: 'OANDA:NAS100USD',
    market: 'Estados Unidos',
    type: 'Renta Variable',
    description: '100 mayores empresas no financieras del Nasdaq. ISIN: US6311011026',
    price: 29182.75,
    change: -0.70,
    decimals: 2,
  },
  {
    id: 'dji',
    name: 'Dow Jones',
    ticker: 'DJI / ^DJI',
    tvSymbol: 'OANDA:US30USD',
    market: 'Estados Unidos',
    type: 'Renta Variable',
    description: '30 empresas industriales líderes de EE. UU. ISIN: US2605661048',
    price: 53336.00,
    change: -0.03,
    decimals: 2,
  },
  {
    id: 'sx5e',
    name: 'Euro Stoxx 50',
    ticker: 'SX5E / ^STOXX50E',
    tvSymbol: 'OANDA:EU50EUR',
    market: 'Eurozona',
    type: 'Renta Variable',
    description: '50 mayores empresas de la zona euro. ISIN: EU0009658145',
    price: 6441.79,
    change: -0.32,
    decimals: 2,
  },
  {
    id: 'dax',
    name: 'DAX 40',
    ticker: 'DAX / ^GDAXI',
    tvSymbol: 'OANDA:DE40EUR',
    market: 'Alemania',
    type: 'Renta Variable',
    description: '40 principales cotizadas de la Bolsa de Fráncfort. ISIN: DE0008469008',
    price: 26066.58,
    change: -0.27,
    decimals: 2,
  },
  {
    id: 'ukx',
    name: 'FTSE 100',
    ticker: 'UKX / ^FTSE',
    tvSymbol: 'OANDA:UK100GBP',
    market: 'Reino Unido',
    type: 'Renta Variable',
    description: '100 principales empresas de la Bolsa de Londres. ISIN: GB0001383545',
    price: 10816.97,
    change: +0.00,
    decimals: 2,
  },
  {
    id: 'n225',
    name: 'Nikkei 225',
    ticker: 'N225 / ^N225',
    tvSymbol: 'OANDA:JP225USD',
    market: 'Japón',
    type: 'Renta Variable',
    description: '225 mayores valores de la Bolsa de Tokio. ISIN: JP9010C00002',
    price: 65528.09,
    change: -0.74,
    decimals: 2,
  },
  {
    id: 'hsi',
    name: 'Hang Seng',
    ticker: 'HSI / ^HSI',
    tvSymbol: 'OANDA:HK33HKD',
    market: 'Hong Kong / China',
    type: 'Renta Variable',
    description: 'Principales empresas cotizadas en Hong Kong. ISIN: HK0000004322',
    price: 25563.99,
    change: -1.71,
    decimals: 2,
  },
  {
    id: 'xauusd',
    name: 'Oro Spot',
    ticker: 'XAUUSD (Spot)',
    tvSymbol: 'OANDA:XAUUSD',
    market: 'Global',
    type: 'Metal Precioso Spot',
    description: 'Cotización SPOT del oro frente al dólar (XAU/USD). Activo refugio físico.',
    price: 4647.74,
    change: +0.97,
    decimals: 2,
  },
  {
    id: 'xagusd',
    name: 'Plata Spot',
    ticker: 'XAGUSD (Spot)',
    tvSymbol: 'OANDA:XAGUSD',
    market: 'Global',
    type: 'Metal Precioso Spot',
    description: 'Cotización SPOT de la plata frente al dólar (XAG/USD). Demanda física e industrial.',
    price: 69.17,
    change: +0.33,
    decimals: 2,
  },
];

interface MarketTickerProps {
  liveXauusdPrice?: number;
  selectedTvSymbol?: string;
  onSelectAsset?: (asset: MarketAsset) => void;
}

export const MarketTicker: React.FC<MarketTickerProps> = ({
  liveXauusdPrice,
  selectedTvSymbol = 'OANDA:XAUUSD',
  onSelectAsset,
}) => {
  const [assets, setAssets] = useState<MarketAsset[]>(INITIAL_MARKET_ASSETS);

  // Sincronizar precio real de XAUUSD si viene por WebSocket / REST
  useEffect(() => {
    if (liveXauusdPrice && liveXauusdPrice > 0) {
      setAssets((prev) =>
        prev.map((item) =>
          item.id === 'xauusd'
            ? { ...item, price: liveXauusdPrice }
            : item
        )
      );
    }
  }, [liveXauusdPrice]);

  // Sincronización continua de cotizaciones de mercado en vivo
  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        const baseUrl =
          typeof window !== 'undefined' && window.location.port === '4321'
            ? `${window.location.protocol}//${window.location.hostname}:8000`
            : '';
        const res = await fetch(`${baseUrl}/api/v1/market-quotes`);
        if (res.ok) {
          const json = await res.json();
          if (json.quotes) {
            setAssets((prev) =>
              prev.map((asset) => {
                const q = json.quotes[asset.id];
                if (q && q.price && (asset.id !== 'xauusd' || !liveXauusdPrice)) {
                  return {
                    ...asset,
                    price: q.price,
                    change: q.change !== undefined ? q.change : asset.change,
                  };
                }
                return asset;
              })
            );
          }
        }
      } catch {
        // Fallback suave
      }
    };

    fetchQuotes();
    const interval = setInterval(fetchQuotes, 5000);
    return () => clearInterval(interval);
  }, [liveXauusdPrice]);

  // Duplicamos los elementos para el loop infinito continuo sin saltos visuales
  const tickerItems = [...assets, ...assets];

  return (
    <div className="relative flex-1 overflow-hidden h-full flex items-center select-none group min-w-0">
      {/* Gradientes sutiles de borde para efecto de desvanecimiento continuo */}
      <div className="absolute left-0 top-0 bottom-0 w-4 bg-gradient-to-r from-surface to-transparent z-10 pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-4 bg-gradient-to-l from-surface to-transparent z-10 pointer-events-none" />

      {/* Cinta móvil estilo Wall Street / Ticker Americano */}
      <div className="ticker-track flex items-center h-full whitespace-nowrap will-change-transform group-hover:[animation-play-state:paused]">
        {tickerItems.map((asset, index) => {
          const isPositive = asset.change >= 0;
          const isSelected = asset.tvSymbol === selectedTvSymbol;

          return (
            <div
              key={`${asset.id}-${index}`}
              onClick={() => onSelectAsset?.(asset)}
              className={`inline-flex items-center gap-2 h-7 px-2 rounded transition-all cursor-pointer group/item ${
                isSelected
                  ? 'bg-amber-500/15 ring-1 ring-amber-400/50 shadow-sm shadow-amber-500/10'
                  : 'hover:bg-[#1a1c26] active:scale-95'
              }`}
              title={`Clic para ver gráfico de ${asset.name} (${asset.tvSymbol})\n${asset.market} • ${asset.type}\n${asset.description}`}
            >
              {/* Nombre del Índice o Activo con su Ticker */}
              <div className="flex items-center gap-1 leading-none">
                <span className={`text-[11px] font-semibold tracking-tight whitespace-nowrap leading-none transition-colors ${
                  isSelected ? 'text-amber-300 font-bold' : 'text-slate-200 group-hover/item:text-white'
                }`}>
                  {asset.name}
                </span>
                <span className={`font-mono text-[10px] font-normal leading-none ${
                  isSelected ? 'text-amber-400/80' : 'text-slate-400'
                }`}>
                  ({asset.ticker.split('/')[0].trim()})
                </span>
              </div>

              {/* Precio en tiempo real */}
              <span className="text-[11px] font-mono font-semibold text-slate-100 leading-none">
                ${asset.price.toLocaleString('en-US', {
                  minimumFractionDigits: asset.decimals,
                  maximumFractionDigits: asset.decimals,
                })}
              </span>

              {/* Variación % con flecha y color verde/rojo */}
              <span
                className={`text-[10px] font-mono font-bold flex items-center gap-0.5 px-1 py-0.5 rounded leading-none ${
                  isPositive
                    ? 'text-emerald-400 bg-emerald-500/10'
                    : 'text-red-400 bg-red-500/10'
                }`}
              >
                {isPositive ? '▲' : '▼'}
                {isPositive ? `+${asset.change.toFixed(2)}%` : `${asset.change.toFixed(2)}%`}
              </span>

              {/* Separador vertical idéntico a todos los divisores de cabecera */}
              <span className="h-4 w-px bg-outline-variant mx-3 shrink-0 select-none self-center" />
            </div>
          );
        })}
      </div>
    </div>
  );
};

