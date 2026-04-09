---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Material 3 Guidelines

## Color System
- M3 uses **tonal palettes** generated from a single seed color via HCT color space
- 5 key colors: primary, secondary, tertiary, error, neutral
- Each generates 13 tones (0-100) mapped to roles: onPrimary, primaryContainer, etc.
- VocabApp uses `ColorScheme.fromSeed()` — all roles auto-derived

## Component Specs (Key for Audit)
| Component | Min Height | Touch Target | Corner Radius |
|-----------|-----------|--------------|---------------|
| FAB | 56dp | 48dp | 16dp |
| Button (filled) | 40dp | 48dp | 20dp (full) |
| Card (filled) | — | — | 12dp |
| NavigationBar | 80dp | 48dp | — |
| Chip | 32dp | 48dp | 8dp |

## Typography Scale (M3)
- displayLarge → displaySmall (3 sizes)
- headlineLarge → headlineSmall (3 sizes)
- titleLarge → titleSmall (3 sizes)
- bodyLarge → bodySmall (3 sizes)
- labelLarge → labelSmall (3 sizes)
- Default typeface: Roboto; weight 400/500/700

## Adaptive Layouts
- Compact: <600dp (phone) — single pane, bottom nav
- Medium: 600-839dp (tablet portrait) — rail or dual pane
- Expanded: 840dp+ (tablet landscape/desktop) — persistent nav, multi-pane
- VocabApp target: compact-first, medium adaptive

## Elevation System
- M3 uses **tonal elevation** (surface tint) not shadow elevation
- Levels: 0, 1, 3, 6, 8, 12 — each adds surface tint opacity
- Cards: level 1; Dialogs: level 3; FAB: level 3

## Audit Checklist
- [ ] All components use M3 specs (not MD2 overrides)
- [ ] Color roles used semantically (not hardcoded hex)
- [ ] Touch targets >= 48dp
- [ ] Typography uses M3 scale roles
- [ ] Navigation pattern matches screen width class
