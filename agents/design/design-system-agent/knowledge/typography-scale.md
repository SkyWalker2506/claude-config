---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Typography Scale

## M3 Type Roles
| Role | Default Size | Weight | Line Height | Usage |
|------|-------------|--------|-------------|-------|
| displayLarge | 57 | 400 | 64 | Hero numbers (XP total) |
| displayMedium | 45 | 400 | 52 | — |
| displaySmall | 36 | 400 | 44 | — |
| headlineLarge | 32 | 400 | 40 | Page titles |
| headlineMedium | 28 | 400 | 36 | Section headers |
| headlineSmall | 24 | 400 | 32 | Card titles |
| titleLarge | 22 | 400 | 28 | AppBar title |
| titleMedium | 16 | 500 | 24 | List item title |
| titleSmall | 14 | 500 | 20 | — |
| bodyLarge | 16 | 400 | 24 | Default body text |
| bodyMedium | 14 | 400 | 20 | Secondary text |
| bodySmall | 12 | 400 | 16 | Captions |
| labelLarge | 14 | 500 | 20 | Button text |
| labelMedium | 12 | 500 | 16 | Chip/badge labels |
| labelSmall | 11 | 500 | 16 | Overline |

## Modular Scale
- M3 uses a 1.2 ratio (minor third) between sizes
- Custom fonts: maintain M3 size roles, only change typeface/weight

## Responsive Font Sizing
```dart
// Scale text for tablet
double responsiveFontSize(BuildContext context, double baseSize) {
  final width = MediaQuery.sizeOf(context).width;
  if (width >= 840) return baseSize * 1.15;  // expanded
  if (width >= 600) return baseSize * 1.08;  // medium
  return baseSize;                            // compact
}
```

## Flutter Usage
```dart
// Always use theme text styles
Text('Quiz Results', style: Theme.of(context).textTheme.headlineMedium)

// Modify weight/color, keep size from theme
Text('Score', style: Theme.of(context).textTheme.titleMedium?.copyWith(
  fontWeight: FontWeight.w700,
  color: cs.primary,
))
```

## VocabApp Guidelines
- Word cards: headlineSmall for the word, bodyMedium for definition
- Quiz questions: titleLarge
- XP counters: displaySmall with tabular figures
- Streak labels: labelLarge
- Never use raw `TextStyle(fontSize: xx)` — always derive from theme
