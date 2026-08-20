---
name: Institutional Precision
colors:
  surface: '#f9f9ff'
  surface-dim: '#d8d9e3'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3fd'
  surface-container: '#ecedf7'
  surface-container-high: '#e6e7f2'
  surface-container-highest: '#e1e2ec'
  on-surface: '#191b23'
  on-surface-variant: '#424754'
  inverse-surface: '#2e3038'
  inverse-on-surface: '#eff0fa'
  outline: '#727785'
  outline-variant: '#c2c6d6'
  surface-tint: '#005ac2'
  primary: '#0058be'
  on-primary: '#ffffff'
  primary-container: '#2170e4'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#5d5f5b'
  on-secondary: '#ffffff'
  secondary-container: '#e0e0db'
  on-secondary-container: '#62635f'
  tertiary: '#4d5d73'
  on-tertiary: '#ffffff'
  tertiary-container: '#66768d'
  on-tertiary-container: '#fdfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#e3e3de'
  secondary-fixed-dim: '#c6c7c2'
  on-secondary-fixed: '#1a1c19'
  on-secondary-fixed-variant: '#454744'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f9f9ff'
  on-background: '#191b23'
  surface-variant: '#e1e2ec'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  data-lg:
    fontFamily: JetBrains Mono
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  data-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  data-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  data-gap: 8px
  section-margin: 32px
  gutter: 16px
---

## Brand & Style

This design system is engineered for high-stakes institutional trading environments where data density and clarity are paramount. The aesthetic follows a **Modern Corporate** philosophy with a focus on **Precision Minimalism**. By stripping away decorative elements, the system prioritizes the rapid scanning of complex financial instruments. 

The interface evokes a sense of "Architectural Stability"—combining a warm, grounded background with high-performance, clinical data visualization. The emotional response is one of calm authority, reliability, and technical sophistication. High-contrast data points are balanced against a soft, greige foundation to reduce eye strain during long trading sessions.

## Colors

The color palette is strictly functional, separating navigational intent from financial status.

- **Primary Blue (#3b82f6):** Reserved exclusively for structural elements, primary actions (Submit, Login), and active navigation states. It represents the "system" layer.
- **Architectural Greige (#F5F5F0):** Used for the global background to provide a sophisticated, non-clinical warmth that reduces glare.
- **Pure White (#FFFFFF):** Used for interactive surfaces, cards, and data containers to create a clear "work area."
- **Financial Semantics:** Emerald (#10b981) and Crimson (#ef4444) are strictly limited to market direction (Buy/Sell) and P&L indicators. They must never be used for generic buttons or alerts to avoid cognitive interference with market signals.
- **Neutral Slate:** Used for borders and secondary text to maintain a low-contrast hierarchy for non-critical information.

## Typography

This design system utilizes a dual-font strategy to distinguish between UI context and raw data.

- **UI & Labels (Hanken Grotesk):** A sharp, contemporary sans-serif used for all functional labels, headers, and navigation. Its high x-height ensures legibility at small sizes.
- **Financial Data (JetBrains Mono):** A high-performance monospaced font used for all prices, quantities, tickers, and timestamps. Monospacing is critical for tabular alignment, allowing traders to compare vertically stacked numbers instantly.

**Scale Constraints:** 
For mobile, `display-lg` should scale down to `24px` to maintain data density without horizontal scrolling. All `data-` roles must remain monospaced regardless of device.

## Layout & Spacing

The layout utilizes a **12-column Fixed Grid** for desktop (max-width 1440px) to ensure predictable data positioning, transitioning to a fluid layout for mobile. 

A strict **4px baseline grid** governs all spacing. In data-dense areas (like Order Books or Portfolio tables), the spacing is tightened to `4px` or `8px` to maximize information visibility without scrolling. Administrative sections (Settings, Profiles) use a more relaxed `16px` or `24px` rhythm.

**Breakpoints:**
- **Desktop (1280px+):** Full 12-column dashboard.
- **Tablet (768px - 1279px):** Collapsed sidebars, 8-column grid.
- **Mobile (Under 767px):** Single column, stacked data cards, hidden secondary columns in tables.

## Elevation & Depth

To maintain a "High-Performance" feel, the system avoids heavy shadows. 

- **Tonal Layering:** Depth is primarily communicated through color. The global background is Greige (#F5F5F0), while active work surfaces are Pure White (#FFFFFF).
- **Low-Contrast Outlines:** Surfaces are defined by 1px borders in Soft Slate (#E2E8F0). 
- **Interactive State:** Only the most critical overlays (Modals, Context Menus) use a soft, 15% opacity Slate shadow with a 12px blur. 
- **Active State:** In-focus inputs or selected rows use a 2px Primary Blue border rather than a shadow.

## Shapes

The shape language is **Soft (0.25rem)**. This provides a subtle modern touch without sacrificing the "industrial" and "efficient" feel of the interface. 

- **Buttons & Inputs:** Use the standard `rounded` (4px).
- **Data Cards:** Use `rounded-lg` (8px) to softly group complex information.
- **Tabs & Indicators:** Use sharp corners or very minimal `rounded-sm` (2px) to maintain a technical, grid-aligned appearance.

## Components

- **Primary Buttons:** Solid Primary Blue (#3b82f6) with White text. Bold weight. No gradients.
- **Action Buttons (Buy/Sell):** Full-width buttons using Emerald (#10b981) for Buy and Crimson (#ef4444) for Sell. These are the only colored buttons permitted outside of the Primary Blue.
- **Data Tables:** Zebra striping is discouraged. Instead, use 1px bottom borders (#E2E8F0). Hover states should use a 5% Primary Blue tint for the entire row.
- **Input Fields:** White background, 1px Slate border. On focus: 2px Primary Blue border. Labels are always `label-sm` (uppercase) positioned above the field.
- **Chips/Badges:** For status (Filled, Pending, Cancelled), use a subtle background tint of the semantic color with high-contrast text. For example, "Filled" uses 10% Emerald background with 100% Emerald text.
- **Trading Chart:** Background must remain Pure White or the Greige background color. Grid lines in 5% Slate.
- **Portfolio Cards:** Grouped data with a `label-sm` title, a `data-lg` primary value, and a `data-sm` secondary metric (e.g., % change).