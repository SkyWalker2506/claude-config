---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Flutter Best Practices

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

## Const Widgets
```dart
// const prevents unnecessary rebuilds
const SizedBox(height: 16)           // good
SizedBox(height: 16)                 // bad — new instance every build

// const constructor requirement: all fields must be compile-time constants
class StreakChip extends StatelessWidget {
  const StreakChip({required this.count, super.key});
  final int count;
}
```

## Key Usage
- `ValueKey` for list items with stable IDs: `ValueKey(word.id)`
- `UniqueKey` to force rebuild on reorder
- `GlobalKey` for form state, scaffold messenger — use sparingly
- Never use index as key in reorderable lists

## Build Optimization
```dart
// Split rebuild scope
class QuizPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const QuizHeader(),               // never rebuilds
        const QuizProgressBar(),          // never rebuilds
        QuizQuestionCard(question: q),    // rebuilds on question change
      ],
    );
  }
}

// Use RepaintBoundary for animated widgets
RepaintBoundary(child: AnimatedStreakCounter())
```

## Widget Lifecycle
| Method | When | Use For |
|--------|------|---------|
| initState | Once, on insert | Controller init, subscriptions |
| didChangeDependencies | After initState + on dependency change | InheritedWidget reads |
| build | Every setState/rebuild | UI tree |
| didUpdateWidget | Parent rebuilt with new config | Compare old/new props |
| deactivate | Removed from tree (may reinsert) | Pause subscriptions |
| dispose | Permanently removed | Cancel controllers, streams |

## Performance Checklist
- [ ] `const` on all stateless literals
- [ ] `ListView.builder` for 20+ items (not `Column + map`)
- [ ] `RepaintBoundary` around animations
- [ ] No heavy computation in `build` — move to provider/isolate
- [ ] `MediaQuery.sizeOf(context)` not `MediaQuery.of(context).size`
- [ ] `AutomaticKeepAliveClientMixin` for tab content preservation
- [ ] Image caching with `cached_network_image`
