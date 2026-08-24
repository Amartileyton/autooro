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

export const NewsFeed: React.FC<NewsFeedProps> = ({ className = '', isMobile = false }) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [tick, setTick] = useState<number>(Date.now());
  const [summarizingId, setSummarizingId] = useState<string | null>(null);
  const [expandedSummaries, setExpandedSummaries] = useState<Record<string, any>>({});
  const [filterAsset, setFilterAsset] = useState<string>('ALL');

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
  const fetchNews = async (showRefreshIndicator = false) => {
    if (showRefreshIndicator) setIsRefreshing(true);
    try {
      const res = await fetch(`${getApiBaseUrl()}/api/v1/news`);
      if (res.ok) {
        const data = await res.json();
        if (data.news) {
          setNews(data.news);
          setLastUpdated(new Date());
        }
      }
    } catch {
      // Fallback
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  // Ciclo de refresco periódico y avance dinámico del reloj cada 30 segundos
  useEffect(() => {
    fetchNews();
    const fetchInterval = setInterval(() => fetchNews(false), 60000); // Consulta periódica al backend cada 1 min
    const clockInterval = setInterval(() => setTick(Date.now()), 30000); // Re-renderizado de tiempos relativos cada 30s
    return () => {
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
      }
    } catch {
      // Fallback
      setExpandedSummaries((prev) => ({
        ...prev,
        [item.id]: {
          summary_bullets: [
            `📌 Titular: ${item.title}`,
            `⚡ Impacto en mercado: Atento a la volatilidad en activos correlacionados (${item.asset}).`,
            `🧭 Gestión recomendada: Mantener Stop Loss y gestión estricta de riesgo.`
          ],
          sentiment: 'NEUTRAL',
          key_takeaway: 'Resumen generado en modo de contingencia local.'
        }
      }));
    } finally {
      setSummarizingId(null);
    }
  };

  const filteredNews = filterAsset === 'ALL'
    ? news
    : news.filter((n) => n.asset.toLowerCase().includes(filterAsset.toLowerCase()));

  const categories = ['ALL', 'XAUUSD', 'SPX / NASDAQ', 'EURO STOXX', 'XAGUSD'];

  return (
    <div className={`flex flex-col h-full bg-background border border-outline-variant rounded-md overflow-hidden min-h-0 ${className}`}>
      {/* Cabecera del Feed de Noticias con badge de ciclo horario y botón refrescar */}
      <div className="p-3 border-b border-outline-variant bg-surface flex flex-col gap-2 shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-wider text-text-primary font-mono">
              Radar de Noticias & Macro
            </span>
            <span className="text-[10px] bg-primary/10 text-primary px-1.5 py-0.5 rounded font-mono font-bold">
              {filteredNews.length}
            </span>
          </div>

          <div className="flex items-center gap-2">
            {/* Indicador de última actualización horaria */}
            <div className="flex items-center gap-1.5 text-[10px] text-text-secondary bg-surface-container px-2 py-0.5 rounded border border-outline-variant font-mono">
              <span className="text-primary font-bold">⏱️ Ciclo 1h</span>
              <span className="opacity-70">
                {lastUpdated ? lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'En vivo'}
              </span>
            </div>

            {/* Botón de actualización manual inmediata */}
            <button
              onClick={() => fetchNews(true)}
              disabled={isRefreshing}
              title="Refrescar noticias de APIs externas"
              className="flex items-center justify-center p-1 rounded hover:bg-surface-container text-text-secondary hover:text-primary transition-all border border-outline-variant"
            >
              <span className={`material-symbols-outlined text-[15px] ${isRefreshing ? 'animate-spin text-primary' : ''}`}>
                refresh
              </span>
            </button>
          </div>
        </div>

        {/* Filtros rápidos por activo */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterAsset(cat)}
              className={`text-[10px] px-2.5 py-1 rounded font-mono transition-colors whitespace-nowrap ${
                filterAsset === cat
                  ? 'bg-primary text-black font-bold shadow-sm'
                  : 'bg-surface-container hover:bg-surface-container-high text-text-secondary border border-outline-variant'
              }`}
            >
              {cat === 'ALL' ? 'Todos' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Lista scrolleable de Noticias */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3 min-h-0 divide-y divide-outline-variant/30 scrollbar-thin">
        {loading && news.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-text-secondary gap-2">
            <span className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            <span className="text-xs font-mono">Descargando titulares macro...</span>
          </div>
        ) : filteredNews.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-48 text-text-secondary gap-1 text-center">
            <span className="text-lg">📰</span>
            <span className="text-xs font-medium text-text-primary">No hay noticias en esta categoría</span>
            <span className="text-[10px]">Selecciona otro filtro para ver el radar global.</span>
          </div>
        ) : (
          filteredNews.map((item) => {
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

                {/* Titular interactivo con link externo */}
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => handleFeedback(item, 'click')}
                  className="text-xs font-semibold text-text-primary hover:text-primary leading-snug transition-colors flex items-start gap-1.5 group"
                >
                  <span className="flex-1">{item.title}</span>
                  <svg
                    className="w-3.5 h-3.5 text-text-secondary group-hover:text-primary shrink-0 mt-0.5 opacity-60 group-hover:opacity-100 transition-opacity"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                    />
                  </svg>
                </a>

                {/* Barra de Acciones: Botones SVG de LIKE / DISLIKE corporativos y Botón Resumen IA Más Grande */}
                <div className="flex items-center justify-between pt-1">
                  {/* Botones de Like / Dislike con SVGs corporativos */}
                  <div className="flex items-center gap-2">
                    {/* Botón LIKE corporativo */}
                    <button
                      onClick={() => handleFeedback(item, 'like')}
                      title="Guardar como interesante"
                      className={`flex items-center justify-center w-8 h-8 rounded-md border transition-all ${
                        isLiked
                          ? 'bg-primary/20 text-primary border-primary shadow-[0_0_10px_rgba(229,169,60,0.3)]'
                          : 'bg-surface-container hover:bg-surface-container-high text-text-secondary hover:text-primary border-outline-variant hover:border-primary/50'
                      }`}
                    >
                      <LikeIcon className="w-4 h-4" />
                    </button>

                    {/* Botón DISLIKE (Simétrico invertido) */}
                    <button
                      onClick={() => handleFeedback(item, 'dislike')}
                      title="Descartar / No me interesa"
                      className={`flex items-center justify-center w-8 h-8 rounded-md border transition-all ${
                        isDisliked
                          ? 'bg-error/20 text-error border-error shadow-[0_0_10px_rgba(239,68,68,0.3)]'
                          : 'bg-surface-container hover:bg-surface-container-high text-text-secondary hover:text-error border-outline-variant hover:border-error/50'
                      }`}
                    >
                      <DislikeIcon className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Botón Resumen IA Más Grande, Prominente y Elegante */}
                  <button
                    onClick={() => handleRequestAiSummary(item)}
                    disabled={isSummarizing}
                    className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-mono font-bold border transition-all ${
                      summaryData
                        ? 'bg-primary text-black border-primary shadow-[0_0_14px_rgba(229,169,60,0.4)]'
                        : 'bg-surface-container hover:bg-primary/20 text-primary border-primary/60 hover:border-primary hover:shadow-[0_0_10px_rgba(229,169,60,0.2)]'
                    }`}
                  >
                    {isSummarizing ? (
                      <>
                        <span className="w-3.5 h-3.5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                        <span>Generando Resumen...</span>
                      </>
                    ) : summaryData ? (
                      <>
                        <span>✨ Ocultar Resumen</span>
                      </>
                    ) : (
                      <>
                        <span className="text-sm">✨</span>
                        <span>RESUMEN IA</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Acordeón de Resumen Ejecutivo generado por DeepSeek */}
                {summaryData && (
                  <div className="mt-1 p-3 rounded-md bg-surface-container-high border border-primary/40 flex flex-col gap-2 text-xs animate-in fade-in duration-200 shadow-inner">
                    <div className="flex items-center justify-between border-b border-outline-variant/60 pb-1.5">
                      <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-primary">
                        <span>⚡ Análisis Ejecutivo DeepSeek</span>
                      </div>
                      {summaryData.sentiment && (
                        <span
                          className={`text-[9px] px-2 py-0.5 rounded font-bold font-mono ${
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

                    <div className="space-y-1.5 text-text-primary text-xs leading-relaxed">
                      {(summaryData.summary_bullets || []).map((bullet: string, idx: number) => (
                        <div key={idx} className="flex items-start gap-1">
                          <span className="text-text-primary">{bullet}</span>
                        </div>
                      ))}
                    </div>

                    {summaryData.key_takeaway && (
                      <div className="pt-1.5 text-[11px] text-primary/95 font-mono italic border-t border-outline-variant/40">
                        🎯 {summaryData.key_takeaway}
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
