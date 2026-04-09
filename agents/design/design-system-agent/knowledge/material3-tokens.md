---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Material 3 Design Tokens

## Token Hierarchy
```
Reference tokens  →  sys.color.primary = #6750A4
System tokens     →  sys.color.primary = ref.palette.primary40
Component tokens  →  comp.filled-button.container-color = sys.color.primary
```
- Flutter maps system tokens to `ColorScheme` roles
- Component tokens map to `ButtonThemeData`, `CardThemeData`, etc.

## Role-Based Color Tokens
| Role | Usage | Flutter accessor |
|------|-------|-----------------|
| primary | Key actions, FAB, active states | `cs.primary` |
| onPrimary | Text/icon on primary | `cs.onPrimary` |
| primaryContainer | Filled cards, chips | `cs.primaryContainer` |
| secondary | Less prominent actions | `cs.secondary` |
| tertiary | Accent, contrast | `cs.tertiary` |
| surface | Page/card background | `cs.surface` |
| surfaceContainerLow | Elevated surfaces | `cs.surfaceContainerLow` |
| error | Error states | `cs.error` |
| outline | Borders, dividers | `cs.outline` |
| outlineVariant | Subtle borders | `cs.outlineVariant` |

## Tonal Palette
- HCT (Hue-Chroma-Tone) generates 13 tones: 0,4,6,10,12,17,20,22,24,30,40,50,60,70,80,87,90,92,94,95,96,98,99,100
- Light theme uses tone40 for primary, dark uses tone80
- Container colors: light=tone90, dark=tone30

## Custom Semantic Tokens
```dart
// VocabApp extends M3 with semantic colors
extension AppSemanticColors on ColorScheme {
  Color get success => brightness == Brightness.dark
      ? Colors.green.shade200 : Colors.green.shade800;
  Color get successContainer => brightness == Brightness.dark
      ? Colors.green.shade900 : Colors.green.shade100;
  Color get xpGold => brightness == Brightness.dark
      ? Colors.amber.shade400 : Colors.amber.shade700;
}
```

## Applying Tokens
- Always use `Theme.of(context).colorScheme.xxx` — never raw colors
- For custom tokens, use extension methods on `ColorScheme`
- Dark mode: all tokens auto-adapt via `fromSeed(brightness: Brightness.dark)`
- Surface tint replaces elevation shadow in M3
