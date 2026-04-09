---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Color Accessibility

## WCAG Contrast Requirements
| Level | Normal Text | Large Text | Non-Text UI |
|-------|------------|------------|-------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | — |

- Large text: >= 18pt regular or >= 14pt bold
- VocabApp targets AA minimum, AAA for body text preferred

## Contrast Checking in Flutter
```dart
// Calculate contrast ratio
double contrastRatio(Color fg, Color bg) {
  double lum1 = fg.computeLuminance();
  double lum2 = bg.computeLuminance();
  final lighter = lum1 > lum2 ? lum1 : lum2;
  final darker = lum1 > lum2 ? lum2 : lum1;
  return (lighter + 0.05) / (darker + 0.05);
}

// Verify in tests
expect(contrastRatio(cs.onSurface, cs.surface), greaterThanOrEqualTo(4.5));
```

## Semantic Color Mapping
```dart
// VocabApp AppColors pattern — adaptive semantic colors
static Color successForeground(ColorScheme cs) =>
    cs.brightness == Brightness.dark
        ? Colors.green.shade200   // 7:1 on dark surface
        : Colors.green.shade800;  // 5.1:1 on white

// Extend for quiz feedback
static Color incorrectForeground(ColorScheme cs) =>
    cs.brightness == Brightness.dark
        ? Colors.red.shade200
        : Colors.red.shade800;
```

## Color-Blind Safe Design
- Never use red/green alone to indicate correct/incorrect
- Always pair color with icon (checkmark/X) or text
- VocabApp quiz: green + checkmark for correct, red + X for incorrect
- Leaderboard: use rank numbers, not just color coding

## Dark Mode Considerations
- M3 `fromSeed` auto-adjusts all tones for dark mode
- Custom colors (success, star) must be manually adapted per `AppColors`
- Test: verify all custom colors meet 4.5:1 on both `cs.surface` variants
- Surface tint in dark mode can reduce apparent contrast — verify

## Testing Tools
- Flutter DevTools: layout inspector shows color values
- Golden tests: capture both themes, visual diff
- Manual: macOS Accessibility Inspector, Android accessibility scanner
- Automated: custom test that checks all `AppColors` combinations
