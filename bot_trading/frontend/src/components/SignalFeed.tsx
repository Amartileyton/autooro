import React from 'react';

export interface TelegramMessageItem {
  id: number;
  message_id?: number;
  raw_text: string;
  parsed_success: boolean;
  parser_used: string;
  error_reason?: string;
  received_at: string;
}

interface SignalFeedProps {
  messages: TelegramMessageItem[];
}

export const SignalFeed: React.FC<SignalFeedProps> = ({ messages }) => {
  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-4 py-2 border-b border-outline-variant">
        <span className="text-label-sm text-outline uppercase font-semibold">Registro de Señales</span>
      </div>

      <div className="flex-1 p-2 space-y-2 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="text-outline text-label-sm text-center py-6">
            Esperando señales de Telegram...
          </div>
        ) : (
          messages.map((msg) => {
            const isBuy = msg.raw_text.toUpperCase().includes('BUY') || msg.raw_text.toUpperCase().includes('COMPRA');
            const dateStr = new Date(msg.received_at).toLocaleTimeString();

            return (
              <div
                key={msg.id}
                className="bg-surface p-2 border border-outline-variant rounded relative overflow-hidden group hover:border-primary/50 transition-colors"
              >
                <div
                  className={`absolute top-0 left-0 w-1 h-full ${
                    msg.parsed_success ? (isBuy ? 'bg-emerald-green' : 'bg-crimson-red') : 'bg-outline/40'
                  }`}
                />

                <div className="flex justify-between items-start pl-2">
                  <div>
                    <div className={`text-data-sm font-bold font-mono ${
                      msg.parsed_success ? (isBuy ? 'text-emerald-green' : 'text-crimson-red') : 'text-outline'
                    }`}>
                      {msg.parsed_success ? (isBuy ? 'COMPRA XAUUSD' : 'VENTA XAUUSD') : 'MENSAJE DESCARTADO'}
                    </div>
                    <div className="text-label-sm text-outline mt-0.5">
                      Via Telegram {msg.parser_used !== 'NONE' && `(${msg.parser_used})`}
                    </div>
                  </div>

                  <span className={`text-[9px] px-1 py-0.5 rounded uppercase tracking-wider font-mono border ${
                    msg.parsed_success
                      ? 'bg-primary-container/20 text-primary border-primary/30'
                      : 'bg-error-container/20 text-error border-error/30'
                  }`}>
                    {msg.parsed_success ? 'Procesado' : 'Ignorado'}
                  </span>
                </div>

                <div className="mt-2 pl-2 text-[11px] font-mono text-outline line-clamp-3 whitespace-pre-line bg-surface-container-lowest/50 p-1 rounded border border-outline-variant/30">
                  {msg.raw_text}
                </div>

                <div className="text-[9px] text-outline mt-1 pl-2 text-right font-mono">
                  {dateStr}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
