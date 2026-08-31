import { useEffect, useRef, useState } from 'react';

/**
 * Construye la URL del WebSocket de streaming en vivo en función de la
 * ubicación del navegador (misma lógica que el backend en desarrollo).
 */
const getWsUrl = (): string => {
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    if (window.location.port === '4321') {
      return `${protocol}//${window.location.hostname}:8000/ws/live`;
    }
    return `${protocol}//${window.location.host}/ws/live`;
  }
  return 'ws://localhost:8000/ws/live';
};

/**
 * Hook de conexión WebSocket con reconexión automática.
 *
 * Extrae la lógica que antes vivía inline en ``DashboardApp`` (conexión,
 * latencia, reconexión cada 3s y limpieza al desmontar). El callback
 * ``onMessage`` se mantiene siempre actualizado vía ref para evitar cierres
 * obsoletos sobre el estado del dashboard.
 */
export const useTradingWebSocket = (
  authToken: string | null,
  onMessage: (payload: any) => void,
) => {
  const wsRef = useRef<WebSocket | null>(null);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [latencyMs, setLatencyMs] = useState<number>(12);

  // Mantiene siempre la versión más reciente del handler sin re-ejecutar el
  // efecto de conexión (el efecto solo depende de authToken).
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;

  useEffect(() => {
    if (!authToken) return;

    let reconnectTimer: any = null;

    const connectWebSocket = () => {
      const startTime = Date.now();
      const wsUrl = `${getWsUrl()}${authToken ? `?token=${encodeURIComponent(authToken)}` : ''}`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setWsConnected(true);
        setLatencyMs(Math.max(5, Date.now() - startTime));
        console.log('WebSocket conectado a GOLD-EX Live Stream');
      };

      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          onMessageRef.current(payload);
        } catch (e) {
          console.error('Error parseando WebSocket payload:', e);
        }
      };

      ws.onclose = () => {
        setWsConnected(false);
        console.warn('WebSocket desconectado. Reintentando en 3s...');
        reconnectTimer = setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error('Error en WebSocket Live Stream:', err);
        ws.close();
      };
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) wsRef.current.close();
      clearTimeout(reconnectTimer);
    };
  }, [authToken]);

  return { wsRef, wsConnected, latencyMs };
};
