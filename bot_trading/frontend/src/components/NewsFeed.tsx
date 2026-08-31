import React, { useState, useEffect } from 'react';

export interface NewsItem {
  id: string;
  title: string;
  source: string;
  url: string;
  published_at: string;
  published_at_iso?: string;
  asset: string;
  user_state?: 'liked' | 'disliked' | null;
  likes?: number;
  dislikes?: number;
  clicks?: number;
  summary?: {
    bullets: string[];
    sentiment: string;
    key_takeaway: string;
    provider: string;
  } | null;
}

interface NewsFeedProps {
  className?: string;
  isMobile?: boolean;
}

// Icono LIKE corporativo según dist/svg/LIKE.svg
const LikeIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg viewBox="0 0 512 512" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M83.578,167.256H16.716C7.524,167.256,0,174.742,0,183.971v300.881c0,9.225,7.491,16.713,16.716,16.713h66.862 c9.225,0,16.716-7.489,16.716-16.713V183.971C100.294,174.742,92.769,167.256,83.578,167.256z"/>
    <path d="M470.266,167.256c-2.692-0.456-128.739,0-128.739,0l17.606-48.032c12.148-33.174,4.283-83.827-29.424-101.835 c-10.975-5.864-26.309-8.809-38.672-5.697c-7.09,1.784-13.321,6.478-17.035,12.767c-4.271,7.233-3.83,15.676-5.351,23.696 c-3.857,20.342-13.469,39.683-28.354,54.2c-25.952,25.311-106.571,98.331-106.571,98.331v267.45h278.593 c37.592,0.022,62.228-41.958,43.687-74.749c22.101-14.155,29.66-43.97,16.716-66.862c22.102-14.155,29.66-43.97,16.716-66.862 C527.572,235.24,514.823,174.792,470.266,167.256z"/>
  </svg>
);

// Icono DISLIKE (Simétrico inverso de LIKE.svg rotado 180 grados)
const DislikeIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg viewBox="0 0 512 512" fill="currentColor" className={`transform rotate-180 ${className}`} xmlns="http://www.w3.org/2000/svg">
    <path d="M83.578,167.256H16.716C7.524,167.256,0,174.742,0,183.971v300.881c0,9.225,7.491,16.713,16.716,16.713h66.862 c9.225,0,16.716-7.489,16.716-16.713V183.971C100.294,174.742,92.769,167.256,83.578,167.256z"/>
    <path d="M470.266,167.256c-2.692-0.456-128.739,0-128.739,0l17.606-48.032c12.148-33.174,4.283-83.827-29.424-101.835 c-10.975-5.864-26.309-8.809-38.672-5.697c-7.09,1.784-13.321,6.478-17.035,12.767c-4.271,7.233-3.83,15.676-5.351,23.696 c-3.857,20.342-13.469,39.683-28.354,54.2c-25.952,25.311-106.571,98.331-106.571,98.331v267.45h278.593 c37.592,0.022,62.228-41.958,43.687-74.749c22.101-14.155,29.66-43.97,16.716-66.862c22.102-14.155,29.66-43.97,16.716-66.862 C527.572,235.24,514.823,174.792,470.266,167.256z"/>
  </svg>
);

// Icono IA corporativo según dist/svg/IA.svg
const IaIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg viewBox="0 0 512 512" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(64.000000, 64.000000)">
      <path d="M320,64 L320,320 L64,320 L64,64 L320,64 Z M171.749388,128 L146.817842,128 L99.4840387,256 L121.976629,256 L130.913039,230.977 L187.575039,230.977 L196.319607,256 L220.167172,256 L171.749388,128 Z M260.093778,128 L237.691519,128 L237.691519,256 L260.093778,256 L260.093778,128 Z M159.094727,149.47526 L181.409039,213.333 L137.135039,213.333 L159.094727,149.47526 Z M341.333333,256 L384,256 L384,298.666667 L341.333333,298.666667 L341.333333,256 Z M85.3333333,341.333333 L128,341.333333 L128,384 L85.3333333,384 L85.3333333,341.333333 Z M170.666667,341.333333 L213.333333,341.333333 L213.333333,384 L170.666667,384 L170.666667,341.333333 Z M85.3333333,0 L128,0 L128,42.6666667 L85.3333333,42.6666667 L85.3333333,0 Z M256,341.333333 L298.666667,341.333333 L298.666667,384 L256,384 L256,341.333333 Z M170.666667,0 L213.333333,0 L213.333333,42.6666667 L170.666667,42.6666667 L170.666667,0 Z M256,0 L298.666667,0 L298.666667,42.6666667 L256,42.6666667 L256,0 Z M341.333333,170.666667 L384,170.666667 L384,213.333333 L341.333333,213.333333 L341.333333,170.666667 Z M0,256 L42.6666667,256 L42.6666667,298.666667 L0,298.666667 L0,256 Z M341.333333,85.3333333 L384,85.3333333 L384,128 L341.333333,128 L341.333333,85.3333333 Z M0,170.666667 L42.6666667,170.666667 L42.6666667,213.333333 L0,213.333333 L0,170.666667 Z M0,85.3333333 L42.6666667,85.3333333 L42.6666667,128 L0,128 L0,85.3333333 Z" />
    </g>
  </svg>
);

// Formateador de tiempo relativo dinámico que avanza en tiempo real en el navegador
const formatRelativeTime = (isoString?: string, fallback?: string): string => {
  if (!isoString) return fallback || 'Reciente';
  try {
    const raw = isoString.endsWith('Z') || isoString.includes('+') ? isoString : `${isoString}Z`;
    const d = new Date(raw);
    if (isNaN(d.getTime())) return fallback || 'Reciente';
    const now = Date.now();
    const diffSec = Math.max(0, Math.floor((now - d.getTime()) / 1000));

    if (diffSec < 60) return 'Hace un momento';
    const mins = Math.floor(diffSec / 60);
    if (mins < 60) return `Hace ${mins} min`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `Hace ${hours} h ${mins % 60 > 0 ? `${mins % 60}m` : ''}`;
    const days = Math.floor(hours / 24);
    return `Hace ${days} d`;
  } catch {
    return fallback || 'Reciente';
  }
};

const MOCK_NEWS_DATA: NewsItem[] = [
  {
    id: "mock-1",
    title: "Gold hits fresh record high above $2,500 amid escalating Middle East tensions & Fed rate cut expectations",
    source: "Investing.com",
    url: "https://www.investing.com/news/commodities-news/gold-price-hits-record-high-3569123",
    published_at: "Hace 6 min",
    published_at_iso: new Date(Date.now() - 6 * 60 * 1000).toISOString(),
    asset: "XAUUSD",
    user_state: null,
    likes: 14,
    dislikes: 1,
    clicks: 85,
    summary: {
      sentiment: "ALCISTA (BULLISH)",
      key_takeaway: "El oro mantiene fuerte soporte por flujos de refugio seguro y flexibilización monetaria de la Fed.",
      bullets: [
        "Demanda institucional masiva impulsada por compras sostenidas de bancos centrales.",
        "Riesgo geopolítico incrementa las primas de cobertura en metales preciosos.",
        "Resistencia clave identificada en $2,540.00 con soporte en $2,480.00."
      ],
      provider: "DeepSeek Quant AI"
    }
  },
  {
    id: "mock-2",
    title: "Federal Reserve signals potential 50 bps rate cut in September as labor market cools",
    source: "MarketWatch",
    url: "https://www.marketwatch.com/story/fed-signals-september-cut-2026",
    published_at: "Hace 24 min",
    published_at_iso: new Date(Date.now() - 24 * 60 * 1000).toISOString(),
    asset: "MACRO",
    user_state: null,
    likes: 8,
    dislikes: 0,
    clicks: 42
  },
  {
    id: "mock-3",
    title: "US Dollar Index (DXY) sinks to 7-month low following Powell Jackson Hole remarks",
    source: "FXStreet",
    url: "https://www.fxstreet.com/news/dxy-falls-to-multi-month-low",
    published_at: "Hace 52 min",
    published_at_iso: new Date(Date.now() - 52 * 60 * 1000).toISOString(),
    asset: "DXY",
    user_state: null,
    likes: 5,
    dislikes: 2,
    clicks: 31
  },
  {
    id: "mock-4",
    title: "Global central banks accelerate physical gold reserve diversification in Q3",
    source: "Investing.com",
    url: "https://www.investing.com/news/commodities-news/central-banks-gold-reserves-3569145",
    published_at: "Hace 2 h",
    published_at_iso: new Date(Date.now() - 120 * 60 * 1000).toISOString(),
    asset: "XAUUSD",
    user_state: null,
    likes: 19,
    dislikes: 0,
    clicks: 97
  }
];

export const NewsFeed: React.FC<NewsFeedProps> = ({ className = '', isMobile = false }) => {
  const [news, setNews] = useState<NewsItem[]>(MOCK_NEWS_DATA);
  const [loading, setLoading] = useState<boolean>(false);
  const [tick, setTick] = useState<number>(Date.now());
  const [summarizingId, setSummarizingId] = useState<string | null>(null);
  const [expandedSummaries, setExpandedSummaries] = useState<Record<string, any>>({});

  const getApiBaseUrl = () => {
    if (typeof window !== 'undefined') {
      if (window.location.port === '4321') {
        return `${window.location.protocol}//${window.location.hostname}:8000`;
      }
      return `${window.location.protocol}//${window.location.host}`;
    }
    return '';
  };

  // Cargar noticias del backend
  const fetchNews = async () => {
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/news`);
      if (res.ok) {
        const data = await res.json();
        if (data.news && data.news.length > 0) {
          setNews(data.news);
        }
      }
    } catch {
      if (news.length === 0) {
        setNews(MOCK_NEWS_DATA);
      }
    } finally {
      setLoading(false);
    }
  };

  // Ciclo de refresco periódico y avance dinámico del reloj cada 30 segundos
  useEffect(() => {
    fetchNews();
    const handleNewsRefreshed = () => fetchNews();
    window.addEventListener('news_refreshed', handleNewsRefreshed);
    const fetchInterval = setInterval(() => fetchNews(), 60000); // Consulta periódica al backend cada 1 min
    const clockInterval = setInterval(() => setTick(Date.now()), 30000); // Re-renderizado de tiempos relativos cada 30s
    return () => {
      window.removeEventListener('news_refreshed', handleNewsRefreshed);
      clearInterval(fetchInterval);
      clearInterval(clockInterval);
    };
  }, []);

  // Registrar feedback de usuario (Like, Dislike, Click)
  const handleFeedback = async (item: NewsItem, actionType: 'like' | 'dislike' | 'click') => {
    // Actualización optimista de UI
    if (actionType === 'like' || actionType === 'dislike') {
      setNews((prev) =>
        prev.map((n) => {
          if (n.id === item.id) {
            const newState = n.user_state === (actionType === 'like' ? 'liked' : 'disliked') ? null : (actionType === 'like' ? 'liked' : 'disliked');
            return {
              ...n,
              user_state: newState,
            };
          }
          return n;
        })
      );
    }

    try {
      await fetch(`${getApiBaseUrl()}/api/v1/news/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'sec_xauusd_trading_key_2026',
        },
        body: JSON.stringify({
          news_id: item.id,
          news_title: item.title,
          news_url: item.url,
          news_asset: item.asset,
          action_type: actionType,
        }),
      });
    } catch {
      // Fallback silencioso
    }
  };

  // Solicitar resumen inteligente con DeepSeek bajo demanda
  const handleSummarize = async (item: NewsItem) => {
    if (expandedSummaries[item.id]) {
      // Toggle off
      setExpandedSummaries((prev) => {
        const next = { ...prev };
        delete next[item.id];
        return next;
      });
      return;
    }

    setSummarizingId(item.id);
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/news/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'sec_xauusd_trading_key_2026',
        },
        body: JSON.stringify({
          title: item.title,
          source: item.source,
          url: item.url,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setExpandedSummaries((prev) => ({
          ...prev,
          [item.id]: data,
        }));
      } else {
        throw new Error('Resumen no disponible');
      }
    } catch {
      // Fallback con datos de contingencia
      setExpandedSummaries((prev) => ({
        ...prev,
        [item.id]: {
          summary_bullets: [
            `📌 Titular: ${item.title}`,
            `⚡ Impacto en mercado: Atento a la volatilidad en activos correlacionados (${item.asset}).`,
            `🧭 Gestión recomendada: Mantener Stop Loss y gestión estricta de riesgo.`
          ],
          sentiment: 'NEUTRAL',
          key_takeaway: 'Resumen ejecutivo generado para el activo.'
        }
      }));
    } finally {
      setSummarizingId(null);
    }
  };

  return (
    <div className={`flex flex-col h-full bg-background border border-outline-variant rounded-md overflow-hidden min-h-0 ${className}`}>
      {/* Cabecera limpia del Feed de Noticias */}
      <div className="p-3 border-b border-outline-variant bg-surface flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
          <span className="text-xs font-bold uppercase tracking-wider text-text-primary font-mono">
            Radar de Noticias & Macro
          </span>
          <span className="text-[10px] bg-primary/10 text-primary px-1.5 py-0.5 rounded font-mono font-bold">
            {news.length}
          </span>
        </div>
      </div>

      {/* Lista scrolleable de Noticias */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3 min-h-0 divide-y divide-outline-variant/30 scrollbar-thin">
        {loading && news.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-text-secondary gap-2">
            <span className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <span className="text-xs font-mono">Descargando titulares macro...</span>
          </div>
        ) : news.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-text-secondary gap-1 text-center">
            <span className="text-lg">📰</span>
            <span className="text-xs font-medium text-text-primary">No hay noticias disponibles</span>
          </div>
        ) : (
          news.map((item) => {
            const isLiked = item.user_state === 'liked';
            const isDisliked = item.user_state === 'disliked';
            const isSummarizing = summarizingId === item.id;
            const summaryData = expandedSummaries[item.id];

            return (
              <div
                key={item.id}
                className={`pt-3 first:pt-0 flex flex-col gap-2.5 transition-opacity ${
                  isDisliked ? 'opacity-35 hover:opacity-100' : ''
                }`}
              >
                {/* Metadatos superiores: Activo, Medio y Fecha */}
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="px-1.5 py-0.5 bg-surface-container text-primary font-bold rounded border border-outline-variant">
                      {item.asset}
                    </span>
                    <span className="text-text-secondary truncate max-w-[140px] font-medium">{item.source}</span>
                    <span className="text-text-secondary/60">•</span>
                    <span className="text-text-secondary/75">{formatRelativeTime(item.published_at_iso, item.published_at)}</span>
                  </div>
                </div>

                {/* Titular interactivo directo (sin icono de enlace externo) */}
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => handleFeedback(item, 'click')}
                  className="text-xs font-semibold text-text-primary hover:text-primary leading-snug transition-colors block group cursor-pointer"
                >
                  {item.title}
                </a>

                {/* Barra de Acciones: Botones de Like/Dislike y Botón RESUMEN a la derecha */}
                <div className="flex items-center justify-between pt-1">
                  {/* Botones de Like / Dislike con SVGs corporativos */}
                  <div className="flex items-center gap-1.5">
                    {/* Botón LIKE corporativo */}
                    <button
                      onClick={() => handleFeedback(item, 'like')}
                      title="Guardar como interesante"
                      className={`flex items-center justify-center w-7 h-7 rounded-md border transition-all ${
                        isLiked
                          ? 'bg-primary/20 text-primary border-primary shadow-[0_0_10px_rgba(229,169,60,0.3)]'
                          : 'bg-surface-container hover:bg-surface-container-high text-text-secondary hover:text-primary border-outline-variant hover:border-primary/50'
                      }`}
                    >
                      <LikeIcon className="w-3.5 h-3.5" />
                    </button>

                    {/* Botón DISLIKE (Simétrico invertido) */}
                    <button
                      onClick={() => handleFeedback(item, 'dislike')}
                      title="Descartar / No me interesa"
                      className={`flex items-center justify-center w-7 h-7 rounded-md border transition-all ${
                        isDisliked
                          ? 'bg-error/20 text-error border-error shadow-[0_0_10px_rgba(239,68,68,0.3)]'
                          : 'bg-surface-container hover:bg-surface-container-high text-text-secondary hover:text-error border-outline-variant hover:border-error/50'
                      }`}
                    >
                      <DislikeIcon className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Botón RESUMEN a la derecha con IA.svg en color corporativo */}
                  <button
                    onClick={() => handleSummarize(item)}
                    disabled={isSummarizing}
                    className={`flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-md text-[11px] font-mono font-bold border transition-all ${
                      summaryData
                        ? 'bg-primary text-black border-primary shadow-[0_0_14px_rgba(229,169,60,0.4)]'
                        : 'bg-surface-container hover:bg-primary/15 text-primary border-primary/50 hover:border-primary hover:shadow-[0_0_10px_rgba(229,169,60,0.2)]'
                    }`}
                  >
                    {isSummarizing ? (
                      <>
                        <span className="w-3.5 h-3.5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                        <span>Generando...</span>
                      </>
                    ) : summaryData ? (
                      <>
                        <IaIcon className="w-3.5 h-3.5 text-black shrink-0" />
                        <span>OCULTAR RESUMEN</span>
                      </>
                    ) : (
                      <>
                        <IaIcon className="w-3.5 h-3.5 text-primary shrink-0" />
                        <span>RESUMEN</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Acordeón de Lección Magistral / Masterclass Macroeconómica */}
                {summaryData && (
                  <div className="mt-2 p-3.5 rounded-lg bg-surface-container border border-primary/40 flex flex-col gap-3 text-xs animate-in fade-in duration-200 shadow-lg">
                    <div className="flex items-center justify-between border-b border-outline-variant/60 pb-2">
                      <div className="flex items-center gap-2 text-xs font-mono font-bold text-primary">
                        <IaIcon className="w-4 h-4 text-primary shrink-0" />
                        <span>🎓 MASTERCLASS MACROECONÓMICA</span>
                      </div>
                      {summaryData.sentiment && (
                        <span
                          className={`text-[9px] px-2.5 py-0.5 rounded font-bold font-mono uppercase tracking-wider ${
                            summaryData.sentiment === 'BULLISH'
                              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                              : summaryData.sentiment === 'BEARISH'
                              ? 'bg-error/20 text-error border border-error/30'
                              : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          }`}
                        >
                          {summaryData.sentiment === 'BULLISH'
                            ? 'ALCISTA 🟢'
                            : summaryData.sentiment === 'BEARISH'
                            ? 'BAJISTA 🔴'
                            : 'NEUTRAL 🟡'}
                        </span>
                      )}
                    </div>

                    {summaryData.translated_title && (
                      <div className="text-[11px] font-semibold text-text-primary/90 italic bg-surface-container-high/60 px-2.5 py-1.5 rounded border border-outline-variant/30">
                        📌 {summaryData.translated_title}
                      </div>
                    )}

                    <div className="space-y-2.5 text-text-primary text-xs leading-relaxed">
                      {(summaryData.summary_bullets || []).map((bullet: string, idx: number) => {
                        const parts = bullet.split(': ');
                        const hasPrefix = parts.length > 1;
                        const prefix = hasPrefix ? parts[0] : '';
                        const content = hasPrefix ? parts.slice(1).join(': ') : bullet;

                        return (
                          <div
                            key={idx}
                            className="p-2.5 rounded bg-surface-container-high/40 border-l-2 border-primary/70 text-[11.5px] leading-relaxed flex flex-col gap-1"
                          >
                            {hasPrefix && (
                              <span className="font-bold text-primary font-mono text-[11px]">
                                {prefix}:
                              </span>
                            )}
                            <span className="text-text-primary/95 text-[11px]">
                              {content}
                            </span>
                          </div>
                        );
                      })}
                    </div>

                    {summaryData.key_takeaway && (
                      <div className="p-2.5 rounded bg-primary/10 border border-primary/30 text-[11.5px] text-primary font-mono font-medium leading-normal">
                        {summaryData.key_takeaway}
                      </div>
                    )}
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
