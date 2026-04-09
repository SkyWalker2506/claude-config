---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Flutter Animations

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

## Implicit vs Explicit
| Type | When to Use | Examples |
|------|------------|---------|
| Implicit | Simple property changes | AnimatedContainer, AnimatedOpacity, AnimatedScale |
| Explicit | Complex sequences, loops, control | AnimationController + Tween |
| Hero | Shared element transitions | Hero widget across routes |

## AnimationController Pattern
```dart
class _FlipCardState extends State<FlipCard> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _rotation;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: animDuration(context, const Duration(milliseconds: 400)),
    );
    _rotation = Tween<double>(begin: 0, end: pi).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeInOutCubic),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }
}
```

## Tween Types
- `Tween<double>` — opacity, scale, rotation
- `ColorTween` — color transitions
- `AlignmentTween` — position shifts
- `BorderRadiusTween` — corner radius animation
- Chain with `TweenSequence` for multi-step

## Hero Transitions
```dart
// Source
Hero(tag: 'word-${word.id}', child: WordCard(word: word))

// Destination
Hero(tag: 'word-${word.id}', child: WordDetailHeader(word: word))
```
- Use `flightShuttleBuilder` for custom in-flight widget
- VocabApp: word card → word detail page

## Staggered Animations
```dart
// Offset each item's start by index * delay
Animation<double> _stagger(int index) {
  final start = index * 0.1;
  final end = (start + 0.4).clamp(0.0, 1.0);
  return CurvedAnimation(
    parent: _ctrl,
    curve: Interval(start, end, curve: Curves.easeOut),
  );
}
```

## Performance
- Use `AnimatedBuilder` or `AnimatedWidget` — avoid `setState` in animation tick
- Prefer `Transform` (non-relayout) over changing size/padding
- `RepaintBoundary` around animated widgets to isolate repaints
