import React, { useState } from 'react';

export interface TelegramMessageItem {
  id: number;
  message_id?: number;
  channel_id?: number;
  channel_name?: string;
  raw_text: string;
  parsed_success: boolean;
  parser_used: string;
  signal_details?: {
    type: 'ORDER' | 'MODIFIER';
    side?: 'BUY' | 'SELL';
    entry_price?: number;
    sl_price?: number;
    tp1?: number;
    tp2?: number;
    tp3?: number;
    action?: string;
    target_price?: number;
  } | null;
  error_reason?: string;
  received_at: string;
}

interface SignalFeedProps {
  messages: TelegramMessageItem[];
}

export const SignalFeed: React.FC<SignalFeedProps> = ({ messages }) => {
  const [filterOnlySignals, setFilterOnlySignals] = useState<boolean>(false);

  const filteredMessages = filterOnlySignals
    ? messages.filter((m) => m.parsed_success || m.signal_details)
    : messages;

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#12141c]">
      {/* Header del Feed */}
      <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex justify-between items-center shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-amber-gold">history_edu</span>
          <span className="text-label-sm text-on-surface uppercase font-bold tracking-wider">
            Historial de Señales
          </span>
        </div>

        {/* Toggle Filtro */}
        <button
          onClick={() => setFilterOnlySignals(!filterOnlySignals)}
          className={`px-2 py-0.5 text-[10px] font-mono rounded border transition-colors ${
            filterOnlySignals
              ? 'bg-primary/20 text-primary border-primary/50 font-bold'
              : 'bg-surface text-outline border-outline-variant hover:text-on-surface'
          }`}
        >
          {filterOnlySignals ? 'Solo Señales' : 'Todos'}
        </button>
      </div>

      {/* Lista de Señales */}
      <div className="flex-1 p-2 space-y-2 overflow-y-auto">
        {filteredMessages.length === 0 ? (
          <div className="text-outline text-label-sm text-center py-8">
            <span className="material-symbols-outlined text-[28px] opacity-40 mb-1">satellite_alt</span>
            <p>Esperando nuevas señales de Telegram...</p>
          </div>
        ) : (
          filteredMessages.map((msg) => {
            const isSignal = msg.parsed_success || !!msg.signal_details;
            const details = msg.signal_details;
            const isBuy = details?.side === 'BUY' || msg.raw_text.toUpperCase().includes('BUY');
            const isModifier = details?.type === 'MODIFIER' || msg.raw_text.toUpperCase().includes('MOVE SL') || msg.raw_text.toUpperCase().includes('SL TO');
            const channelName = msg.channel_name || 'Chartoro FX';
            const dateObj = new Date(msg.received_at);
            const timeStr = isNaN(dateObj.getTime()) ? '' : dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

            return (
              <div
                key={msg.id}
                className={`p-2.5 border rounded relative overflow-hidden transition-all ${
                  isSignal
                    ? isModifier
                      ? 'bg-[#181b26] border-amber-500/40 hover:border-amber-400'
                      : isBuy
                      ? 'bg-[#131d1a] border-emerald-500/40 hover:border-emerald-400'
                      : 'bg-[#1f1519] border-crimson-red/40 hover:border-crimson-red'
                    : 'bg-surface/60 border-outline-variant/40 opacity-70 hover:opacity-100'
                }`}
              >
                {/* Indicador de Borde Lateral */}
                <div
                  className={`absolute top-0 left-0 w-1 h-full ${
                    isSignal
                      ? isModifier
                        ? 'bg-amber-400'
                        : isBuy
                        ? 'bg-emerald-green'
                        : 'bg-crimson-red'
                      : 'bg-outline/30'
                  }`}
                />

                {/* Cabecera del Item */}
                <div className="flex justify-between items-start pl-1.5 gap-2">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {/* Canal de Origen */}
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-surface-container-highest text-outline-variant border border-outline-variant/50 flex items-center gap-1">
                      <span className="material-symbols-outlined text-[12px] text-primary">send</span>
                      {channelName}
                    </span>

                    {/* Tipo / Badge de Señal */}
                    {isSignal ? (
                      isModifier ? (
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 font-bold border border-amber-500/30">
                          MODIFICADOR
                        </span>
                      ) : (
                        <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold border ${
                          isBuy 
                            ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' 
                            : 'bg-crimson-red/20 text-crimson-red border-crimson-red/30'
                        }`}>
                          {isBuy ? 'BUY' : 'SELL'}
                        </span>
                      )
                    ) : (
                      <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-surface text-outline border border-outline-variant/40">
                        INFO / SPAM
                      </span>
                    )}
                  </div>

                  <span className="text-[10px] font-mono text-outline shrink-0">
                    {timeStr}
                  </span>
                </div>

                {/* Resumen Estructurado de la Señal */}
                {isSignal && details && details.type === 'ORDER' ? (
                  <div className="mt-2 pl-1.5 grid grid-cols-2 gap-1 text-[11px] font-mono bg-black/30 p-1.5 rounded border border-white/5">
                    <div>
                      <span className="text-outline">Entrada: </span>
                      <strong className="text-on-surface">${details.entry_price?.toFixed(2)}</strong>
                    </div>
                    <div>
                      <span className="text-outline">Stop Loss: </span>
                      <strong className="text-crimson-red">${details.sl_price ? details.sl_price.toFixed(2) : 'Dinámico'}</strong>
                    </div>
                    <div className="col-span-2 flex gap-2 pt-0.5 border-t border-white/5 text-[10px]">
                      {details.tp1 && <span>TP1: <strong className="text-profit">${details.tp1.toFixed(2)}</strong></span>}
                      {details.tp2 && <span>TP2: <strong className="text-profit">${details.tp2.toFixed(2)}</strong></span>}
                      {details.tp3 && <span>TP3: <strong className="text-profit">${details.tp3.toFixed(2)}</strong></span>}
                    </div>
                  </div>
                ) : isSignal && details && details.type === 'MODIFIER' ? (
                  <div className="mt-2 pl-1.5 text-[11px] font-mono bg-black/30 p-1.5 rounded border border-white/5 text-amber-300">
                    {details.action} {details.target_price ? `-> $${details.target_price.toFixed(2)}` : ''}
                  </div>
                ) : (
                  <div className="mt-1.5 pl-1.5 text-[10px] font-mono text-outline line-clamp-2 bg-black/20 p-1 rounded">
                    {msg.raw_text}
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
