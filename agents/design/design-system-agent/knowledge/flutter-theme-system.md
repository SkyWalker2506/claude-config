---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Flutter Theme System

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## ThemeData Structure
```dart
// VocabApp pattern (from app_theme.dart)
abstract final class AppTheme {
  static ThemeData light(Color seedColor) {
    final cs = ColorScheme.fromSeed(seedColor: seedColor);
    return _build(cs);
  }
  static ThemeData dark(Color seedColor) {
    final cs = ColorScheme.fromSeed(
      seedColor: seedColor,
      brightness: Brightness.dark,
    );
    return _build(cs);
  }
}
```

## ColorScheme.fromSeed
- Single seed color generates full M3 palette (primary, secondary, tertiary, error, surface, etc.)
- `brightness` parameter switches light/dark — don't manually override individual roles
- Override specific roles only when brand requires it:
```dart
ColorScheme.fromSeed(
  seedColor: brandBlue,
  primary: brandBlue,        // override only if seed derivation doesn't match
  error: customErrorRed,
)
```

## TextTheme Customization
```dart
ThemeData(
  textTheme: TextTheme(
    displayLarge: GoogleFonts.poppins(fontSize: 57, fontWeight: FontWeight.w400),
    headlineMedium: GoogleFonts.poppins(fontSize: 28, fontWeight: FontWeight.w500),
    bodyLarge: GoogleFonts.inter(fontSize: 16),
    labelLarge: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w500),
  ),
)
```

## Dark Mode Switching
```dart
MaterialApp(
  theme: AppTheme.light(seedColor),
  darkTheme: AppTheme.dark(seedColor),
  themeMode: themeMode,       // ThemeMode.system | .light | .dark
)
```
- Use `Theme.of(context).colorScheme` for colors — never hardcode
- `AppColors` helper for semantic colors not in M3 (success, star)

## Component Theme Overrides
```dart
// VocabApp current overrides
appBarTheme: AppBarTheme(
  backgroundColor: cs.surface,
  scrolledUnderElevation: 2,
  elevation: 0,
),
cardTheme: const CardThemeData(clipBehavior: Clip.antiAlias, elevation: 1),
inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder(), filled: true),
snackBarTheme: const SnackBarThemeData(behavior: SnackBarBehavior.floating, showCloseIcon: true),
```

## Best Practices
- One `AppTheme` class — single source of truth
- Never use `Colors.blue` directly — use `cs.primary`
- Extension methods for custom semantic tokens
- Test both light and dark themes in golden tests
