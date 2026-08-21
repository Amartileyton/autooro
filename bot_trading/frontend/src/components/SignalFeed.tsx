import React from 'react';

export interface TelegramMessageItem {
  id: number;
  message_id?: number;
  channel_id?: number;
  channel_name?: string;
  raw_text: string;
  parsed_success: boolean;
  parser_used: string;
  outcome?: 'WIN' | 'LOSS' | 'ACTIVE' | 'MODIFIED' | 'EXPIRED' | null;
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
  // Filtrar para priorizar señales válidas y limitar a las 10 últimas
  const validSignals = messages.filter((m) => m.parsed_success || m.signal_details);
  const displayItems = (validSignals.length >= 3 ? validSignals : messages).slice(0, 10);

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#12141c]">
      {/* Header del Feed */}
      <div className="px-3 py-2 border-b border-outline-variant bg-surface-container flex justify-between items-center shrink-0">
        <div className="flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px] text-amber-gold">history_edu</span>
          <span className="text-label-sm text-on-surface uppercase font-bold tracking-wider">
            Últimas 10 Señales
          </span>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface border border-outline-variant text-outline">
          {displayItems.length} Registros
        </span>
      </div>

      {/* Lista de Señales (Máximo 10) */}
      <div className="flex-1 p-2 space-y-2 overflow-y-auto">
        {displayItems.length === 0 ? (
          <div className="text-outline text-label-sm text-center py-8">
            <span className="material-symbols-outlined text-[28px] opacity-40 mb-1">satellite_alt</span>
            <p>Esperando señales de Telegram...</p>
          </div>
        ) : (
          displayItems.map((msg) => {
            const isSignal = msg.parsed_success || !!msg.signal_details;
            const details = msg.signal_details;
            const isBuy = details?.side === 'BUY' || msg.raw_text.toUpperCase().includes('BUY');
            const isModifier = details?.type === 'MODIFIER' || msg.raw_text.toUpperCase().includes('MOVE SL');
            const outcome = msg.outcome;
            const channelName = msg.channel_name || 'Chartoro FX';
            const dateObj = new Date(msg.received_at);
            const timeStr = isNaN(dateObj.getTime()) ? '' : dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

            // Colores según resultado (WIN = Verde, LOSS = Rojo, ACTIVE = Azul, MODIFIER = Amarillo)
            let borderColor = 'border-outline-variant/40';
            let bgColor = 'bg-surface/60';
            let badgeColor = 'bg-surface text-outline border-outline-variant/40';
            let outcomeText = 'INFO / AUDITORÍA';

            if (outcome === 'WIN') {
              borderColor = 'border-emerald-500/70 shadow-[0_0_8px_rgba(16,185,129,0.15)]';
              bgColor = 'bg-[#0f1f1a]';
              badgeColor = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50';
              outcomeText = '✅ GANADA (TP HIT)';
            } else if (outcome === 'LOSS') {
              borderColor = 'border-crimson-red/70 shadow-[0_0_8px_rgba(239,68,68,0.15)]';
              bgColor = 'bg-[#221316]';
              badgeColor = 'bg-crimson-red/20 text-crimson-red border-crimson-red/50';
              outcomeText = '❌ PERDIDA (SL HIT)';
            } else if (outcome === 'ACTIVE') {
              borderColor = 'border-primary/70 animate-pulse';
              bgColor = 'bg-[#131b26]';
              badgeColor = 'bg-primary/20 text-primary border-primary/50';
              outcomeText = '🔵 EN CURSO';
            } else if (isModifier || outcome === 'MODIFIED') {
              borderColor = 'border-amber-500/50';
              bgColor = 'bg-[#1a1813]';
              badgeColor = 'bg-amber-500/20 text-amber-400 border-amber-500/50';
              outcomeText = '🟡 MODIFICADOR';
            }

            return (
              <div
                key={msg.id}
                className={`p-2.5 border rounded relative overflow-hidden transition-all ${bgColor} ${borderColor}`}
              >
                {/* Borde indicador lateral */}
                <div
                  className={`absolute top-0 left-0 w-1 h-full ${
                    outcome === 'WIN'
                      ? 'bg-emerald-green'
                      : outcome === 'LOSS'
                      ? 'bg-crimson-red'
                      : isModifier
                      ? 'bg-amber-400'
                      : isSignal
                      ? 'bg-primary'
                      : 'bg-outline/30'
                  }`}
                />

                {/* Cabecera */}
                <div className="flex justify-between items-start pl-1.5 gap-2">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {/* Canal de Origen */}
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-surface-container-highest text-amber-gold border border-amber-gold/30 flex items-center gap-1 font-bold">
                      <span className="material-symbols-outlined text-[12px]">send</span>
                      {channelName}
                    </span>

                    {/* Resultado / Estado */}
                    <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-bold border ${badgeColor}`}>
                      {outcomeText}
                    </span>
                  </div>

                  <span className="text-[10px] font-mono text-outline shrink-0">
                    {timeStr}
                  </span>
                </div>

                {/* Detalles de la Orden */}
                {isSignal && details && details.type === 'ORDER' ? (
                  <div className="mt-2 pl-1.5 bg-black/40 p-2 rounded border border-white/5 space-y-1">
                    <div className="flex justify-between items-center text-[11px] font-mono">
                      <span className={`font-bold ${isBuy ? 'text-emerald-400' : 'text-crimson-red'}`}>
                        {isBuy ? '▲ BUY XAUUSD' : '▼ SELL XAUUSD'}
                      </span>
                      <span>Entrada: <strong className="text-on-surface">${details.entry_price?.toFixed(2)}</strong></span>
                    </div>

                    <div className="flex justify-between items-center text-[10px] font-mono text-outline pt-1 border-t border-white/5">
                      <span>SL: <strong className="text-crimson-red">${details.sl_price ? details.sl_price.toFixed(2) : 'Dinámico'}</strong></span>
                      <div className="flex gap-1.5">
                        {details.tp1 && <span>TP1: <strong className="text-emerald-400">${details.tp1.toFixed(2)}</strong></span>}
                        {details.tp2 && <span>TP2: <strong className="text-emerald-400">${details.tp2.toFixed(2)}</strong></span>}
                        {details.tp3 && <span>TP3: <strong className="text-emerald-400">${details.tp3.toFixed(2)}</strong></span>}
                      </div>
                    </div>
                  </div>
                ) : isSignal && details && details.type === 'MODIFIER' ? (
                  <div className="mt-1.5 pl-1.5 text-[11px] font-mono bg-black/30 p-1.5 rounded border border-white/5 text-amber-300">
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
