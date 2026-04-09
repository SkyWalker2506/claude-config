---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Page Transitions (M3 Motion)

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

## M3 Transition Patterns
| Pattern | When to Use | Duration |
|---------|------------|----------|
| Container Transform | Card → detail page | 300ms |
| Shared Axis | Related pages (tabs, stepper) | 300ms |
| Fade Through | Unrelated pages (bottom nav switch) | 300ms |
| Fade | Overlay, dialog appear | 150ms |

## Container Transform (Card → Detail)
```dart
// Using animations package
OpenContainer(
  transitionDuration: const Duration(milliseconds: 300),
  closedBuilder: (ctx, open) => WordCard(word: word, onTap: open),
  openBuilder: (ctx, close) => WordDetailPage(word: word),
  closedShape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
  closedElevation: 1,
)
```

## Shared Axis (Quiz Steps)
```dart
PageRouteBuilder(
  pageBuilder: (_, __, ___) => QuizStep2Page(),
  transitionsBuilder: (_, anim, secondaryAnim, child) {
    return SharedAxisTransition(
      animation: anim,
      secondaryAnimation: secondaryAnim,
      transitionType: SharedAxisTransitionType.horizontal,
      child: child,
    );
  },
)
```

## Fade Through (Bottom Nav)
```dart
// Switch body content with fade through
AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  transitionBuilder: (child, anim) => FadeTransition(
    opacity: CurvedAnimation(parent: anim, curve: Curves.easeInOut),
    child: child,
  ),
  child: _pages[_currentIndex],
)
```

## VocabApp Transition Map
| From → To | Pattern |
|-----------|---------|
| Word list → Word detail | Container Transform |
| Quiz question → next question | Shared Axis (horizontal) |
| Bottom nav tab → tab | Fade Through |
| Home → Quiz setup | Shared Axis (vertical) |
| Any → Settings | Slide (platform default) |
| Any → Dialog/Sheet | Fade + scale |

## Custom Route Transition
```dart
class FadeThroughRoute<T> extends PageRouteBuilder<T> {
  FadeThroughRoute({required this.page})
      : super(
          pageBuilder: (_, __, ___) => page,
          transitionDuration: const Duration(milliseconds: 300),
          reverseTransitionDuration: const Duration(milliseconds: 300),
          transitionsBuilder: (_, anim, secondaryAnim, child) {
            return FadeThroughTransition(
              animation: anim,
              secondaryAnimation: secondaryAnim,
              child: child,
            );
          },
        );
  final Widget page;
}
```

## Dependencies
- `animations` package (Google) for M3 transitions
- VocabApp `animDuration()` helper respects reduce-motion
