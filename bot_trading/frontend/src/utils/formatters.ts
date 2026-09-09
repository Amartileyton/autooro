// Utilidades de formateo compartidas por los componentes del dashboard.
// Centraliza los helpers defensivos que antes estaban duplicados en
// SignalFeed.tsx, PositionMatrix.tsx y PositionCardWorkbench.tsx.
// Lógica estrictamente idéntica a la original (Zero-Regression).

/**
 * Convierte un valor a precio con 2 decimales o devuelve un fallback.
 * Tolerante a nulos, undefined, cadenas vacías y comas decimales.
 */
export const safePrice = (val: any, fallback = '---'): string => {
  if (val === null || val === undefined || val === '') return fallback;
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  return isNaN(num) ? fallback : num.toFixed(2);
};

/**
 * Convierte un valor a número o devuelve un fallback (por defecto 0).
 */
export const safeNum = (val: any, fallback = 0): number => {
  if (val === null || val === undefined || val === '') return fallback;
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  return isNaN(num) ? fallback : num;
};

/**
 * Formatea un PnL como cadena con signo explícito: '+9.66 €' o '+$12.34'.
 * Soporta divisa por parámetro (por defecto 'EUR').
 */
export const safePnlStr = (val: any, currency = 'EUR'): string => {
  const isEur = currency === 'EUR' || currency === '€';
  if (val === null || val === undefined || val === '') return isEur ? '0.00 €' : '$0.00';
  const num = typeof val === 'number' ? val : parseFloat(String(val).replace(',', '.'));
  if (isNaN(num)) return isEur ? '0.00 €' : '$0.00';
  const sign = num >= 0 ? '+' : '-';
  const formatted = Math.abs(num).toFixed(2);
  return isEur ? `${sign}${formatted} €` : `${sign}$${formatted}`;
};

/**
 * Formatea una fecha ISO a DD/MM/YYYY HH:mm:ss en la zona horaria local del navegador.
 */
export const formatFullDateTime = (isoString?: string, fallback?: string): string => {
  if (!isoString && fallback) return fallback;
  if (!isoString) return '';
  try {
    const raw = isoString.endsWith('Z') || isoString.includes('+') ? isoString : `${isoString}Z`;
    const d = new Date(raw);
    if (isNaN(d.getTime())) return fallback || isoString;
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
  } catch {
    return fallback || isoString;
  }
};
