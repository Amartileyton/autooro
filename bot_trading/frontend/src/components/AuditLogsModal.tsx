import React, { useState } from 'react';

interface AuditLogItem {
  id: number;
  timestamp: string;
  event_type: string;
  severity: string;
  details: string;
}

interface TradeHistoryItem {
  id: number;
  ticket_id: string;
  slot_id: number;
  symbol: string;
  side: string;
  lot_size: number;
  entry_price: number;
  close_price: number | null;
  pnl: number;
  status: string;
  close_reason: string;
  open_time: string;
  close_time: string;
}

interface AuditLogsModalProps {
  isOpen: boolean;
  onClose: () => void;
  logs: AuditLogItem[];
  history: TradeHistoryItem[];
}

export const AuditLogsModal: React.FC<AuditLogsModalProps> = ({
  isOpen,
  onClose,
  logs,
  history,
}) => {
  const [activeTab, setActiveTab] = useState<'history' | 'audit'>('history');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-surface border border-outline w-full max-w-4xl max-h-[85vh] flex flex-col rounded-sm shadow-2xl overflow-hidden">
        {/* Header del Modal */}
        <div className="bg-surface-container-highest px-4 py-2 border-b term-border flex justify-between items-center">
          <div className="flex items-center gap-4">
            <h3 className="text-headline-md font-bold text-primary flex items-center gap-2">
              <span className="material-symbols-outlined text-[20px]">receipt_long</span>
              AUDITORÍA Y REGISTRO INSTITUCIONAL
            </h3>

            <div className="flex gap-1 ml-4">
              <button
                onClick={() => setActiveTab('history')}
                className={`px-3 py-1 text-label-sm font-semibold rounded-sm transition-colors ${
                  activeTab === 'history' ? 'bg-primary text-on-primary' : 'text-outline hover:text-on-surface'
                }`}
              >
                HISTORIAL DE TRADES ({history.length})
              </button>
              <button
                onClick={() => setActiveTab('audit')}
                className={`px-3 py-1 text-label-sm font-semibold rounded-sm transition-colors ${
                  activeTab === 'audit' ? 'bg-primary text-on-primary' : 'text-outline hover:text-on-surface'
                }`}
              >
                LOGS DEL SISTEMA ({logs.length})
              </button>
            </div>
          </div>

          <button
            onClick={onClose}
            className="text-outline hover:text-error transition-colors p-1"
          >
            <span className="material-symbols-outlined text-[24px]">close</span>
          </button>
        </div>

        {/* Contenido */}
        <div className="flex-1 p-4 overflow-y-auto font-mono text-data-sm">
          {activeTab === 'history' ? (
            history.length === 0 ? (
              <div className="text-center py-12 text-outline">No hay trades cerrados registrados aún.</div>
            ) : (
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b term-border text-outline text-[11px] uppercase">
                    <th className="py-2">Ticket</th>
                    <th>Slot</th>
                    <th>Lado</th>
                    <th>Lotes</th>
                    <th>Entrada</th>
                    <th>Cierre</th>
                    <th>PnL</th>
                    <th>Estado</th>
                    <th>Fecha Cierre</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((t) => {
                    const isProfit = t.pnl >= 0;
                    return (
                      <tr key={t.id} className="border-b border-outline-variant/30 hover:bg-surface-container/50">
                        <td className="py-2 text-primary font-semibold">{t.ticket_id}</td>
                        <td>#{t.slot_id}</td>
                        <td className={t.side === 'BUY' ? 'text-emerald-green font-bold' : 'text-crimson-red font-bold'}>
                          {t.side}
                        </td>
                        <td>{t.lot_size.toFixed(2)}</td>
                        <td>${t.entry_price.toFixed(2)}</td>
                        <td>${t.close_price ? t.close_price.toFixed(2) : '-'}</td>
                        <td className={`font-bold ${isProfit ? 'text-profit' : 'text-loss'}`}>
                          {isProfit ? '+' : ''}${t.pnl.toFixed(2)}
                        </td>
                        <td>
                          <span className="text-[10px] px-1 py-0.5 bg-surface-container rounded border border-outline-variant">
                            {t.status}
                          </span>
                        </td>
                        <td className="text-outline text-[10px]">
                          {t.close_time ? new Date(t.close_time).toLocaleString() : '-'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )
          ) : (
            logs.length === 0 ? (
              <div className="text-center py-12 text-outline">No hay logs de auditoría disponibles.</div>
            ) : (
              <div className="space-y-2">
                {logs.map((l) => (
                  <div
                    key={l.id}
                    className="p-2 bg-surface-container border border-outline-variant rounded-sm flex flex-col gap-1 text-[12px]"
                  >
                    <div className="flex justify-between items-center">
                      <span className={`font-bold ${
                        l.severity === 'CRITICAL' ? 'text-error' : l.severity === 'WARNING' ? 'text-amber-gold' : 'text-primary'
                      }`}>
                        [{l.severity}] {l.event_type}
                      </span>
                      <span className="text-outline text-[10px]">{new Date(l.timestamp).toLocaleString()}</span>
                    </div>
                    <div className="text-outline whitespace-pre-wrap">{l.details}</div>
                  </div>
                ))}
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
};
