---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Material 3 in Flutter

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

## Enable M3
```dart
ThemeData(
  useMaterial3: true,                                    // required
  colorScheme: ColorScheme.fromSeed(seedColor: seedColor),
)
```
- `useMaterial3: true` is default since Flutter 3.16
- VocabApp already uses this in `AppTheme._build()`

## ColorScheme.fromSeed
```dart
// Light
final cs = ColorScheme.fromSeed(seedColor: const Color(0xFF4CAF50));

// Dark
final cs = ColorScheme.fromSeed(
  seedColor: const Color(0xFF4CAF50),
  brightness: Brightness.dark,
);

// Access in widgets
final primary = Theme.of(context).colorScheme.primary;
final surface = Theme.of(context).colorScheme.surface;
```

## Adaptive Components
```dart
// Switch adapts to platform
Switch.adaptive(value: v, onChanged: onChanged)

// Slider
Slider.adaptive(value: v, onChanged: onChanged)

// Dialog — use showAdaptiveDialog for iOS-style on Apple
showAdaptiveDialog(
  context: context,
  builder: (ctx) => AlertDialog.adaptive(
    title: const Text('Delete word?'),
    actions: [
      adaptiveAction(context: ctx, onPressed: () {}, child: const Text('Cancel')),
      adaptiveAction(context: ctx, onPressed: onDelete, child: const Text('Delete')),
    ],
  ),
);
```

## M3 NavigationBar (Bottom Nav)
```dart
NavigationBar(
  selectedIndex: _index,
  onDestinationSelected: (i) => setState(() => _index = i),
  destinations: const [
    NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
    NavigationDestination(icon: Icon(Icons.quiz_outlined), selectedIcon: Icon(Icons.quiz), label: 'Quiz'),
    NavigationDestination(icon: Icon(Icons.reviews_outlined), selectedIcon: Icon(Icons.reviews), label: 'Review'),
    NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
  ],
)
```

## M3 Component Checklist for VocabApp
- [x] `useMaterial3: true`
- [x] `ColorScheme.fromSeed()`
- [x] AppBar with surface color
- [x] Cards with M3 theming
- [ ] NavigationBar (bottom nav) — to be added
- [ ] FilledButton / OutlinedButton (replace ElevatedButton)
- [ ] SearchBar (M3 search)
- [ ] SegmentedButton for quiz type selection
- [ ] FilterChip for word filters

## Surface Variants
| Role | Usage | Flutter |
|------|-------|---------|
| surface | Default background | `cs.surface` |
| surfaceContainerLowest | Lowest elevation card | `cs.surfaceContainerLowest` |
| surfaceContainerLow | Card background | `cs.surfaceContainerLow` |
| surfaceContainer | Elevated card | `cs.surfaceContainer` |
| surfaceContainerHigh | Dialog, bottom sheet | `cs.surfaceContainerHigh` |
| surfaceContainerHighest | Highest elevation | `cs.surfaceContainerHighest` |
