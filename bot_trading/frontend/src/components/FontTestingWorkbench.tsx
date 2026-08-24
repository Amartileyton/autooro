import React, { useState } from 'react';

export interface FontPreset {
  id: string;
  name: string;
  badge: string;
  description: string;
  sansFont: string;
  monoFont: string;
  sansClass: string;
  monoClass: string;
  googleFontsImport: string;
}

export const FONT_PRESETS: FontPreset[] = [
  {
    id: 'inter_roboto',
    name: '1. Institutional Pro (Recomendada)',
    badge: 'ESTILO BLOOMBERG / TRADINGVIEW',
    description: 'La combinación estándar en plataformas institucionales y fondos. Máxima nitidez en pantallas de trading, legibilidad impecable en números compactos y gráficos.',
    sansFont: "'Inter', sans-serif",
    monoFont: "'Roboto Mono', monospace",
    sansClass: 'font-inter',
    monoClass: 'font-roboto-mono',
    googleFontsImport: 'family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;600;700',
  },
  {
    id: 'ibm_plex',
    name: '2. Wall Street & Banking Terminal',
    badge: 'ESTILO IBM TERMINAL / BANCA PRIVADA',
    description: 'Diseñada específicamente para interfaces financieras densas. Caracteres técnicos robustos, gran distinción entre ceros y letras O, sobria y de alta autoridad.',
    sansFont: "'IBM Plex Sans', sans-serif",
    monoFont: "'IBM Plex Mono', monospace",
    sansClass: 'font-ibm-sans',
    monoClass: 'font-ibm-mono',
    googleFontsImport: 'family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700',
  },
  {
    id: 'jakarta_dm',
    name: '3. Swiss Fintech & Modern Quant',
    badge: 'ESTILO REVOLUT PRO / KRAKEN',
    description: 'Geometría moderna, elegante y limpia. Reduce la fatiga visual en sesiones prolongadas manteniendo un contraste excelente en números.',
    sansFont: "'Plus Jakarta Sans', sans-serif",
    monoFont: "'DM Mono', monospace",
    sansClass: 'font-jakarta',
    monoClass: 'font-dm-mono',
    googleFontsImport: 'family=Plus+Jakarta+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500',
  },
  {
    id: 'space_grotesk',
    name: '4. High-Tech AI & Hedge Fund',
    badge: 'ESTILO CUANTITATIVO / DEEPSEEK',
    description: 'Estética futurista y tecnológica. Brinda una personalidad distintiva de sistema autónomo con IA y terminal de alta frecuencia.',
    sansFont: "'Space Grotesk', sans-serif",
    monoFont: "'Space Mono', monospace",
    sansClass: 'font-space-sans',
    monoClass: 'font-space-mono',
    googleFontsImport: 'family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700',
  },
  {
    id: 'rajdhani_share',
    name: '5. Tactical Obsidian Cyber',
    badge: 'ESTILO RADAR MILITAR / CYBERPUNK',
    description: 'Tipografía condensada y agresiva, optimizada para aprovechar al máximo el espacio horizontal de los paneles.',
    sansFont: "'Rajdhani', sans-serif",
    monoFont: "'Share Tech Mono', monospace",
    sansClass: 'font-rajdhani',
    monoClass: 'font-share-mono',
    googleFontsImport: 'family=Rajdhani:wght@500;600;700&family=Share+Tech+Mono',
  },
  {
    id: 'current_geist',
    name: '6. Actual (Geist + JetBrains Mono)',
    badge: 'CONFIGURACIÓN ACTUAL',
    description: 'La tipografía por defecto actual del dashboard.',
    sansFont: "'Geist', sans-serif",
    monoFont: "'JetBrains Mono', monospace",
    sansClass: 'font-geist',
    monoClass: 'font-jetbrains',
    googleFontsImport: 'family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700',
  },
];

// Icono LIKE corporativo según dist/svg/LIKE.svg
const LikeIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg viewBox="0 0 512 512" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M83.578,167.256H16.716C7.524,167.256,0,174.742,0,183.971v300.881c0,9.225,7.491,16.713,16.716,16.713h66.862 c9.225,0,16.716-7.489,16.716-16.713V183.971C100.294,174.742,92.769,167.256,83.578,167.256z"/>
    <path d="M470.266,167.256c-2.692-0.456-128.739,0-128.739,0l17.606-48.032c12.148-33.174,4.283-83.827-29.424-101.835 c-10.975-5.864-26.309-8.809-38.672-5.697c-7.09,1.784-13.321,6.478-17.035,12.767c-4.271,7.233-3.83,15.676-5.351,23.696 c-3.857,20.342-13.469,39.683-28.354,54.2c-25.952,25.311-106.571,98.331-106.571,98.331v267.45h278.593 c37.592,0.022,62.228-41.958,43.687-74.749c22.101-14.155,29.66-43.97,16.716-66.862c22.102-14.155,29.66-43.97,16.716-66.862 C527.572,235.24,514.823,174.792,470.266,167.256z"/>
  </svg>
);

const DislikeIcon: React.FC<{ className?: string }> = ({ className = "w-4 h-4" }) => (
  <svg viewBox="0 0 512 512" fill="currentColor" className={`transform rotate-180 ${className}`} xmlns="http://www.w3.org/2000/svg">
    <path d="M83.578,167.256H16.716C7.524,167.256,0,174.742,0,183.971v300.881c0,9.225,7.491,16.713,16.716,16.713h66.862 c9.225,0,16.716-7.489,16.716-16.713V183.971C100.294,174.742,92.769,167.256,83.578,167.256z"/>
    <path d="M470.266,167.256c-2.692-0.456-128.739,0-128.739,0l17.606-48.032c12.148-33.174,4.283-83.827-29.424-101.835 c-10.975-5.864-26.309-8.809-38.672-5.697c-7.09,1.784-13.321,6.478-17.035,12.767c-4.271,7.233-3.83,15.676-5.351,23.696 c-3.857,20.342-13.469,39.683-28.354,54.2c-25.952,25.311-106.571,98.331-106.571,98.331v267.45h278.593 c37.592,0.022,62.228-41.958,43.687-74.749c22.101-14.155,29.66-43.97,16.716-66.862c22.102-14.155,29.66-43.97,16.716-66.862 C527.572,235.24,514.823,174.792,470.266,167.256z"/>
  </svg>
);

export const FontTestingWorkbench: React.FC = () => {
  const [selectedPreset, setSelectedPreset] = useState<FontPreset>(FONT_PRESETS[0]);
  const [appliedFeedback, setAppliedFeedback] = useState<boolean>(false);

  const applyToDashboard = () => {
    // Almacenar en localStorage para que el usuario pueda probarla de inmediato en el dashboard real
    localStorage.setItem('goldex_custom_font_preset', JSON.stringify(selectedPreset));
    setAppliedFeedback(true);
    setTimeout(() => setAppliedFeedback(false), 3000);
  };

  return (
    <div
      className="min-h-screen w-full bg-[#0b0c10] text-text-primary flex flex-col p-4 md:p-6 overflow-y-auto"
      style={{ fontFamily: selectedPreset.sansFont }}
    >
      {/* 1. Barra de Control Superior de Tipografías */}
      <div className="max-w-7xl w-full mx-auto mb-6 bg-surface border border-outline-variant rounded-lg p-4 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-primary font-bold text-lg">🔤 Estudio de Tipografías</span>
            <span className="text-[10px] font-mono bg-primary/20 text-primary px-2 py-0.5 rounded border border-primary/30 font-bold uppercase">
              Laboratorio Visual
            </span>
          </div>
          <p className="text-xs text-text-secondary mt-1">
            Selecciona una propuesta de fuentes para ver cómo transforma en tiempo real la nitidez, los números y las tarjetas del terminal.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            onClick={applyToDashboard}
            className="flex-1 md:flex-none px-4 py-2 rounded bg-primary hover:bg-amber-400 text-black font-bold text-xs font-mono shadow-lg transition-all flex items-center justify-center gap-1.5 active:scale-95"
          >
            <span>{appliedFeedback ? '✅ ¡Guardado para tu sesión!' : '⚡ Probar esta fuente en el Dashboard'}</span>
          </button>
          <a
            href="/"
            className="px-3 py-2 rounded bg-surface-container hover:bg-surface-container-high border border-outline-variant text-xs font-mono text-text-secondary hover:text-text-primary transition-colors whitespace-nowrap"
          >
            ← Volver al Dashboard
          </a>
        </div>
      </div>

      {/* 2. Selector de Propuestas de Tipografía */}
      <div className="max-w-7xl w-full mx-auto grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-2.5 mb-6">
        {FONT_PRESETS.map((preset) => {
          const isSelected = preset.id === selectedPreset.id;
          return (
            <button
              key={preset.id}
              onClick={() => setSelectedPreset(preset)}
              className={`p-3 rounded-lg border text-left flex flex-col justify-between transition-all ${
                isSelected
                  ? 'bg-surface-container-highest border-primary shadow-[0_0_15px_rgba(229,169,60,0.25)] ring-1 ring-primary'
                  : 'bg-surface border-outline-variant hover:border-outline hover:bg-surface-container'
              }`}
            >
              <div>
                <span className={`text-[9px] font-mono font-bold block mb-1 uppercase tracking-tight ${isSelected ? 'text-primary' : 'text-text-secondary'}`}>
                  {preset.badge}
                </span>
                <span className="text-xs font-bold block text-text-primary leading-tight">
                  {preset.name}
                </span>
              </div>

              <div className="mt-2 pt-2 border-t border-outline-variant/40 text-[10px] text-text-secondary font-mono flex justify-between items-center">
                <span>UI: {preset.sansFont.split(',')[0].replace(/'/g, '')}</span>
                <span className="text-primary font-bold">{isSelected ? 'ACTIVA' : ''}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* 3. Ficha de la Propuesta Seleccionada */}
      <div className="max-w-7xl w-full mx-auto bg-surface-container p-3.5 rounded-md border border-outline-variant mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-2 font-mono text-xs">
        <div>
          <span className="text-text-secondary">Fuente de Textos / UI: </span>
          <span className="text-primary font-bold">{selectedPreset.sansFont}</span>
          <span className="text-text-secondary ml-3">Fuente Numérica / Telemetría: </span>
          <span className="text-primary font-bold">{selectedPreset.monoFont}</span>
        </div>
        <div className="text-[11px] text-text-secondary italic">
          {selectedPreset.description}
        </div>
      </div>

      {/* 4. Maqueta en Vivo del Terminal con la Tipografía Seleccionada */}
      <div className="max-w-7xl w-full mx-auto flex-1 flex flex-col gap-4">
        {/* A. Simulación de Header & Telemétrico */}
        <div className="bg-surface border border-outline-variant rounded-md p-3 flex flex-wrap items-center justify-between gap-3 shadow-md">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse" />
              <span className="font-bold text-sm tracking-wider text-text-primary">GOLD-EX TERMINAL</span>
            </div>
            <div className="h-4 w-px bg-outline-variant" />
            <div className="flex items-center gap-2" style={{ fontFamily: selectedPreset.monoFont }}>
              <span className="text-[11px] text-text-secondary">BALANCE:</span>
              <span className="text-sm font-bold text-text-primary">$10,482.50 USD</span>
            </div>
          </div>

          {/* Ticker de Activos */}
          <div className="flex items-center gap-4 text-xs overflow-x-auto py-1" style={{ fontFamily: selectedPreset.monoFont }}>
            <div className="flex items-center gap-1.5">
              <span className="text-text-secondary font-bold">XAUUSD:</span>
              <span className="text-primary font-bold">$4,647.74</span>
              <span className="text-emerald-400 text-[10px] font-bold">(+0.97%)</span>
            </div>
            <div className="h-3 w-px bg-outline-variant" />
            <div className="flex items-center gap-1.5">
              <span className="text-text-secondary font-bold">S&P 500:</span>
              <span className="text-text-primary font-bold">7,661.40</span>
              <span className="text-error text-[10px] font-bold">(-0.20%)</span>
            </div>
            <div className="h-3 w-px bg-outline-variant" />
            <div className="flex items-center gap-1.5">
              <span className="text-text-secondary font-bold">NASDAQ 100:</span>
              <span className="text-text-primary font-bold">29,182.75</span>
              <span className="text-error text-[10px] font-bold">(-0.70%)</span>
            </div>
          </div>
        </div>

        {/* B. Simulación de las 3 Columnas Reales */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-1">
          {/* Columna 1: Registro de Señales */}
          <div className="bg-surface border border-outline-variant rounded-md p-3 flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-outline-variant pb-2">
              <span className="font-bold text-xs uppercase tracking-wider text-text-primary">
                Registro de Señales
              </span>
              <span className="text-[10px] bg-primary/20 text-primary px-2 py-0.5 rounded font-mono font-bold">
                10 SEÑALES
              </span>
            </div>

            {/* Tarjeta de Señal */}
            <div className="bg-[#0b0c10] border border-slate-700 rounded-md p-3 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-text-primary">Chartoro FX</span>
                <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold text-[10px]">
                  WIN (TP1)
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs font-mono" style={{ fontFamily: selectedPreset.monoFont }}>
                <div>
                  <span className="text-[10px] text-text-secondary block">ENTRADA:</span>
                  <span className="font-bold text-text-primary">BUY @ $4,635.20</span>
                </div>
                <div>
                  <span className="text-[10px] text-text-secondary block">TP1 ALCANZADO:</span>
                  <span className="font-bold text-emerald-400">$4,642.00 (+68 pips)</span>
                </div>
              </div>

              <div className="text-[10px] text-text-secondary font-mono border-t border-outline-variant/50 pt-1.5 flex justify-between">
                <span>SL Dinámico: $4,635.20 (BE)</span>
                <span>24/08/2026 09:15:22</span>
              </div>
            </div>
          </div>

          {/* Columna 2: Matriz de Posiciones */}
          <div className="bg-surface border border-outline-variant rounded-md p-3 flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-outline-variant pb-2">
              <span className="font-bold text-xs uppercase tracking-wider text-text-primary">
                Matriz de Posiciones
              </span>
              <span className="text-[10px] bg-primary text-black font-mono font-bold px-2 py-0.5 rounded">
                1 / 4 ACTIVAS
              </span>
            </div>

            {/* Tarjeta de Slot #1 Activo */}
            <div className="bg-[#0b0c10] border border-primary/60 rounded-md p-3 flex flex-col gap-2.5 shadow-lg relative overflow-hidden">
              <div className="absolute top-0 left-0 bottom-0 w-1 bg-emerald-500" />
              <div className="flex items-center justify-between pl-1">
                <div className="flex items-center gap-1.5 font-mono" style={{ fontFamily: selectedPreset.monoFont }}>
                  <span className="text-xs font-bold text-primary">SLOT #1</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">BUY</span>
                  <span className="text-xs text-text-secondary">0.22 lot</span>
                </div>
                <span className="text-sm font-bold text-emerald-400 font-mono" style={{ fontFamily: selectedPreset.monoFont }}>
                  +$385.40 USD
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs font-mono pl-1" style={{ fontFamily: selectedPreset.monoFont }}>
                <div>
                  <span className="text-[9px] text-text-secondary block">ENTRADA</span>
                  <span className="font-bold text-text-primary">$4,635.20</span>
                </div>
                <div>
                  <span className="text-[9px] text-text-secondary block">ACTUAL</span>
                  <span className="font-bold text-primary">$4,647.74</span>
                </div>
                <div>
                  <span className="text-[9px] text-text-secondary block">STOP LOSS</span>
                  <span className="font-bold text-amber-400">$4,640.00</span>
                </div>
              </div>

              <button className="w-full py-1.5 rounded bg-error/20 hover:bg-error/30 text-error border border-error/40 font-mono font-bold text-[11px] transition-colors mt-1">
                Cerrar Slot #1 a Mercado
              </button>
            </div>

            {/* Slot #2 Disponible */}
            <div className="border border-dashed border-slate-700 rounded-md p-3 text-center text-text-secondary font-mono text-xs">
              SLOT #2 — DISPONIBLE
            </div>
          </div>

          {/* Columna 3: Radar de Noticias & Resumen IA */}
          <div className="bg-surface border border-outline-variant rounded-md p-3 flex flex-col gap-3">
            <div className="flex items-center justify-between border-b border-outline-variant pb-2">
              <span className="font-bold text-xs uppercase tracking-wider text-text-primary">
                Radar de Noticias IA
              </span>
              <span className="text-[10px] text-primary font-mono font-bold">
                ✨ DeepSeek On-Demand
              </span>
            </div>

            {/* Tarjeta de Noticia */}
            <div className="bg-[#0b0c10] border border-outline-variant rounded-md p-3 flex flex-col gap-2.5">
              <div className="flex items-center justify-between text-[10px] font-mono">
                <span className="px-1.5 py-0.5 bg-surface-container text-primary font-bold rounded">
                  XAUUSD
                </span>
                <span className="text-text-secondary">Investing.com • Hace 15 min</span>
              </div>

              <a href="#" className="text-xs font-semibold text-text-primary hover:text-primary leading-snug">
                El Oro Spot consolida soporte clave ante la demanda sostenida de reservas físicas
              </a>

              {/* Botones de Like, Dislike y Resumen IA */}
              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 rounded-md bg-primary/20 text-primary border border-primary shadow-sm" title="LIKE">
                    <LikeIcon className="w-3.5 h-3.5" />
                  </button>
                  <button className="p-1.5 rounded-md bg-surface-container hover:bg-surface-container-high text-text-secondary hover:text-error border border-outline-variant" title="DISLIKE">
                    <DislikeIcon className="w-3.5 h-3.5" />
                  </button>
                </div>

                <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-mono font-bold bg-surface-container hover:bg-primary/20 text-primary border border-primary/60 shadow-sm">
                  <span>✨</span>
                  <span>RESUMEN IA</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
