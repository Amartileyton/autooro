---
name: Obsidian Terminal
colors:
  surface: '#12131a'
  surface-dim: '#12131a'
  surface-bright: '#383941'
  surface-container-lowest: '#0d0e15'
  surface-container-low: '#1a1b22'
  surface-container: '#1e1f26'
  surface-container-high: '#292931'
  surface-container-highest: '#33343c'
  on-surface: '#e3e1ec'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#e3e1ec'
  inverse-on-surface: '#2f3038'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#ffb3ad'
  on-secondary: '#68000a'
  secondary-container: '#a40217'
  on-secondary-container: '#ffaea8'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e29100'
  on-tertiary-container: '#523200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#ffdad7'
  secondary-fixed-dim: '#ffb3ad'
  on-secondary-fixed: '#410004'
  on-secondary-fixed-variant: '#930013'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#12131a'
  on-background: '#e3e1ec'
  surface-variant: '#33343c'
typography:
  headline-lg:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Geist
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-lg:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  data-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  data-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
spacing:
  unit: 4px
  container-padding: 12px
  gutter: 1px
  cell-padding-x: 8px
  cell-padding-y: 4px
  stack-gap: 8px
---

## Brand & Style

The design system is engineered for institutional-grade financial precision. It evokes a sense of absolute control, high-stakes reliability, and analytical depth. The aesthetic sits at the intersection of **Neo-Brutalism** and **Modern Corporate**, utilizing sharp edges, strict 1px borders, and zero-latency visual cues.

The target audience consists of professional traders and analysts who prioritize information density over aesthetic fluff. The interface is intentionally utilitarian, using a structured grid to manage complex telemetry and real-time market data without cognitive overload.

**Key Stylistic Pillars:**
- **Extreme Density:** Minimized padding and tight leading to maximize data visibility.
- **Functional Color:** Color is never decorative; it is reserved exclusively for indicating market direction, asset classes, or system status.
- **Architectural Rigidity:** A preference for 90-degree angles and visible structural lines.

## Colors

The palette is optimized for long-duration monitor exposure. In **Dark Mode** (default), the "Obsidian" base reduces eye strain, while **Light Mode** uses a "Zinc" scheme for high-glare environments.

- **Action Colors:** Emerald Green is utilized for 'Buy' signals and profitable vectors. Crimson Red is reserved for 'Sell' signals and stop-losses.
- **Utility Colors:** Amber Gold is specifically assigned to XAUUSD (Gold) pairs and high-priority alerts. Cyan is dedicated to technical telemetry and infrastructure status.
- **Surface Logic:** Backgrounds use a tiered zinc/slate scale. Borders are strictly defined at 1px to create a "cell-based" layout reminiscent of classic trading terminals.

## Typography

This design system employs a dual-font strategy. **Geist** provides a clean, neutral sans-serif foundation for navigation, labels, and descriptive text. **JetBrains Mono** is mandated for all numerical data, prices, timestamps, and ticker symbols to ensure character alignment and rapid scanning of fluctuating values.

- **Tabular Figures:** All numerical values must use tabular lining to prevent "jumping" during real-time updates.
- **Hierarchy:** Use `label-sm` for table headers and metadata categories. `data-md` is the primary size for order books and execution logs.
- **Mobile Scaling:** Headlines scale down by 15% on mobile, but data-specific monospaced sizes remain constant to preserve legibility in tight columns.

## Layout & Spacing

The layout philosophy is based on a **Fixed Grid Terminal** model. Content is organized into modular "panes" or "widgets" separated by 1px borders. 

- **Grid:** A 12-column layout is used for the dashboard, but individual widgets utilize internal micro-grids based on 4px increments.
- **Density:** Padding is intentionally constrained. Standard list items use a 4px vertical padding to maximize the number of visible rows on a single screen.
- **Responsive Behavior:** On desktop, the layout is a multi-pane workspace. On mobile, the system collapses into a single-column stack with horizontal "swipeable" panes for charts and order books.

## Elevation & Depth

This design system rejects traditional shadows and soft blurs in favor of **Tonal Layering** and **High-Contrast Outlines**.

- **Level 0 (Floor):** The base terminal background (Zinc-950).
- **Level 1 (Widget):** Primary workspace containers using a subtle lift (Zinc-900) and a 1px border (Zinc-800).
- **Level 2 (Popovers/Menus):** Elevated elements use the same background as Level 1 but add a crisp 1px border in a lighter shade (Zinc-700) to distinguish from the background.
- **Active State:** Selection is indicated via a high-contrast border or a solid color block (Cyan or Emerald), never through a shadow.

## Shapes

The shape language is strictly **Sharp (0px)**. All containers, buttons, input fields, and tags utilize hard 90-degree corners. This reinforces the "terminal" aesthetic and allows 1px borders to align perfectly with the pixel grid, preventing anti-aliasing blur.

- **Exceptions:** Toggle switches and status "pips" may use a 1px radius only to improve affordance, but all structural elements must remain square.

## Components

### Buttons
- **Primary:** Solid Emerald or Crimson for execution. Sharp corners. Label in bold Geist.
- **Kill-Switch:** A high-visibility button with a Crimson background and a secondary white "hazard" border. Requires a long-press or double-tap to activate.
- **Ghost:** Transparent background with 1px Zinc-700 border for secondary actions.

### Data Tables
- **Padding:** 4px top/bottom, 8px left/right. 
- **Borders:** Horizontal 1px Zinc-800 lines only.
- **Interactions:** Row highlight on hover using a subtle Zinc-800/900 fill.

### Status Badges
- **Telemetry:** Cyan text on a transparent background with a 1px Cyan border. 
- **Glow Effect:** Status pips (e.g., "Live Connection") utilize a 4px outer glow in the corresponding accent color to denote activity.

### Input Fields
- **Style:** Inset appearance using a dark background and 1px border.
- **Typography:** JetBrains Mono for all numeric inputs.

### Segmented Controls
- **Style:** A single 1px border frame containing multiple sharp-edged options. The "Active" segment is filled with Zinc-700 or the primary accent color.