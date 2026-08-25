import React, { useState, useEffect } from 'react';

export interface ChannelPerformanceItem {
  id: number;
  name: string;
  link?: string;
  parser: string;
  mode: 'AUDIT' | 'PRODUCTION';
  enabled: boolean;
  total_messages: number;
  total_signals: number;
  total_trades: number;
  active_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate_pct: number;
  total_gains_usd: number;
  profit_factor: number;
}

interface ChannelAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  apiBaseUrl: string;
  authToken: string | null;
  onSelectChannelFilter?: (channelName: string) => void;
}

export const ChannelAuditModal: React.FC<ChannelAuditModalProps> = ({
  isOpen,
  onClose,
  apiBaseUrl,
  authToken,
  onSelectChannelFilter,
}) => {
  const [channels, setChannels] = useState<ChannelPerformanceItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const fetchChannels = async () => {
    setIsLoading(true);
    try {
      const headers: Record<string, string> = {
        'x-api-key': 'sec_xauusd_trading_key_2026',
      };
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }
      const res = await fetch(`${apiBaseUrl}/api/v1/channels`, { headers });
      if (res.ok) {
        const data = await res.json();
        setChannels(data.channels || []);
      }
    } catch (err) {
      console.error('Error al cargar auditoría de canales:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchChannels();
    }
  }, [isOpen]);

  const toggleChannelMode = async (channelName: string) => {
    try {
      const headers: Record<string, string> = {
        'x-api-key': 'sec_xauusd_trading_key_2026',
      };
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }
      const res = await fetch(
        `${apiBaseUrl}/api/v1/channels/${encodeURIComponent(channelName)}/toggle-mode`,
        { method: 'POST', headers }
      );
      if (res.ok) {
        const data = await res.json();
        setActionMessage(data.message);
        setTimeout(() => setActionMessage(null), 4000);
        fetchChannels();
      }
    } catch (err) {
      console.error('Error al alternar modo del canal:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-fade-in select-none">
      <div className="bg-[#10131c] border border-outline-variant/80 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-hidden shadow-2xl flex flex-col font-sans">
        {/* Header */}
        <div className="bg-surface-container px-5 py-4 border-b border-outline-variant flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-amber-gold text-[24px]">analytics</span>
            <div>
              <h2 className="text-headline-sm font-bold text-white tracking-wide flex items-center gap-2">
                AUDITORÍA Y RENDIMIENTO DE CANALES (GAINS)
              </h2>
              <p className="text-[12px] text-slate-400 font-mono">
                Evaluación segregada de señales, ganancias acumuladas y promoción a producción
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-surface-container-highest transition-colors"
          >
            <span className="material-symbols-outlined text-[22px]">close</span>
          </button>
        </div>

        {/* Banner Informativo */}
        <div className="bg-primary/10 border-b border-primary/20 px-5 py-2.5 flex items-center justify-between gap-3 shrink-0">
          <div className="flex items-center gap-2 text-[12px] text-blue-200">
            <span className="material-symbols-outlined text-[16px] text-primary">info</span>
            <span>
              <strong>Modo Auditoría (Sandbox):</strong> Todos los canales capturan y simulan señales en tiempo real con cotizaciones vivas sin arriesgar capital real.
            </span>
          </div>
          <button
            onClick={fetchChannels}
            disabled={isLoading}
            className="text-[11px] font-mono px-2.5 py-1 rounded bg-primary/20 hover:bg-primary/30 text-blue-300 font-semibold flex items-center gap-1 shrink-0"
          >
            <span className="material-symbols-outlined text-[14px]">refresh</span>
            Refrescar
          </button>
        </div>

        {actionMessage && (
          <div className="bg-emerald-500/15 border-b border-emerald-500/30 px-5 py-2 text-[12px] text-emerald-300 font-mono flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">check_circle</span>
            {actionMessage}
          </div>
        )}

        {/* Body / Lista de Canales */}
        <div className="flex-1 p-5 space-y-4 overflow-y-auto">
          {isLoading && channels.length === 0 ? (
            <div className="text-center py-12 text-slate-400 font-mono text-sm">
              Cargando métricas de canales...
            </div>
          ) : (
            channels.map((ch) => {
              const isAudit = ch.mode === 'AUDIT';
              const isGreenPips = ch.name.toUpperCase().includes('GREEN');
              const gainsPositive = ch.total_gains_usd >= 0;

              return (
                <div
                  key={ch.name}
                  className={`p-4 rounded-lg border transition-all ${
                    isAudit
                      ? 'bg-surface/60 border-outline-variant/60'
                      : 'bg-emerald-950/20 border-emerald-500/50 shadow-[0_0_12px_rgba(16,185,129,0.1)]'
                  }`}
                >
                  {/* Fila Principal */}
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-outline-variant/40">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-9 h-9 rounded-lg flex items-center justify-center font-mono font-bold text-sm ${
                          isGreenPips
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                            : 'bg-blue-500/20 text-blue-400 border border-blue-500/40'
                        }`}
                      >
                        {isGreenPips ? 'GP' : 'CH'}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-base font-bold text-white font-mono">{ch.name}</h3>
                          {ch.link && (
                            <span className="text-[11px] text-slate-400 font-mono bg-surface-container px-1.5 py-0.5 rounded border border-outline-variant/40">
                              {ch.link}
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] text-slate-400 font-mono flex items-center gap-2 mt-0.5">
                          <span>Parser: <strong>{ch.parser.toUpperCase()}</strong></span>
                          <span>•</span>
                          <span>ID Telegram: <strong>{ch.id || 'Dinámico / Auto'}</strong></span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[11px] font-mono font-bold px-2.5 py-1 rounded border flex items-center gap-1.5 ${
                          isAudit
                            ? 'bg-amber-500/15 text-amber-300 border-amber-500/40'
                            : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50'
                        }`}
                      >
                        <span className="material-symbols-outlined text-[14px]">
                          {isAudit ? 'science' : 'verified'}
                        </span>
                        {isAudit ? 'MODO AUDITORÍA (SANDBOX)' : 'MODO PRODUCCIÓN (LIVE)'}
                      </span>

                      <button
                        onClick={() => toggleChannelMode(ch.name)}
                        className={`text-[11px] font-mono font-bold px-3 py-1 rounded border transition-colors ${
                          isAudit
                            ? 'bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border-emerald-500/40'
                            : 'bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border-amber-500/40'
                        }`}
                      >
                        {isAudit ? 'Promover a Producción' : 'Regresar a Auditoría'}
                      </button>
                    </div>
                  </div>

                  {/* Cuadrícula de Métricas de Rentabilidad (Gains) */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 pt-3">
                    {/* Gains Totales */}
                    <div className="bg-surface-container/60 p-2.5 rounded border border-outline-variant/40">
                      <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Gains Totales</div>
                      <div className={`text-base font-mono font-extrabold mt-0.5 ${gainsPositive ? 'text-emerald-400' : 'text-crimson-red'}`}>
                        {gainsPositive ? '+' : ''}${ch.total_gains_usd.toFixed(2)}
                      </div>
                    </div>

                    {/* Win Rate */}
                    <div className="bg-surface-container/60 p-2.5 rounded border border-outline-variant/40">
                      <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Win Rate %</div>
                      <div className="text-base font-mono font-extrabold text-white mt-0.5">
                        {ch.win_rate_pct.toFixed(1)}%
                      </div>
                    </div>

                    {/* Trades Realizados */}
                    <div className="bg-surface-container/60 p-2.5 rounded border border-outline-variant/40">
                      <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Trades Cerrados</div>
                      <div className="text-base font-mono font-extrabold text-white mt-0.5">
                        {ch.total_trades} <span className="text-[10px] text-slate-400 font-normal">({ch.winning_trades}W / {ch.losing_trades}L)</span>
                      </div>
                    </div>

                    {/* Profit Factor */}
                    <div className="bg-surface-container/60 p-2.5 rounded border border-outline-variant/40">
                      <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Profit Factor</div>
                      <div className="text-base font-mono font-extrabold text-amber-gold mt-0.5">
                        {ch.profit_factor.toFixed(2)}
                      </div>
                    </div>

                    {/* Señales Detectadas */}
                    <div className="bg-surface-container/60 p-2.5 rounded border border-outline-variant/40">
                      <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Señales Válidas</div>
                      <div className="text-base font-mono font-extrabold text-blue-300 mt-0.5">
                        {ch.total_signals}
                      </div>
                    </div>

                    {/* Acción / Filtrar */}
                    <div className="bg-surface-container/60 p-2 rounded border border-outline-variant/40 flex items-center justify-center">
                      {onSelectChannelFilter && (
                        <button
                          onClick={() => {
                            onSelectChannelFilter(ch.name);
                            onClose();
                          }}
                          className="w-full h-full text-[11px] font-mono font-bold bg-surface-container-highest hover:bg-primary/30 text-slate-200 hover:text-white rounded border border-outline-variant/60 flex items-center justify-center gap-1 transition-colors"
                        >
                          <span className="material-symbols-outlined text-[14px]">filter_list</span>
                          Ver Feed
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="bg-surface-container px-5 py-3 border-t border-outline-variant flex justify-between items-center shrink-0">
          <div className="text-[11px] text-slate-400 font-mono">
            * Cada canal cuenta con motores y reglas de parsing 100% aislados.
          </div>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-surface-container-highest hover:bg-surface-container-highest/80 text-white font-mono text-xs font-bold border border-outline-variant transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
