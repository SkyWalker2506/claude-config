---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Accessibility & Motion

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

## Reduce Motion Detection
```dart
// VocabApp already has this helper in anim_duration.dart
Duration animDuration(BuildContext context, Duration normal) =>
    MediaQuery.of(context).disableAnimations ? Duration.zero : normal;

// Usage in AnimationController
_ctrl = AnimationController(
  vsync: this,
  duration: animDuration(context, MotionTokens.medium4),
);
```

## Platform Settings
| Platform | Setting | Flutter API |
|----------|---------|------------|
| iOS | Reduce Motion | `MediaQuery.disableAnimations` |
| Android | Remove animations | `MediaQuery.disableAnimations` |
| Android | Animator duration scale | Reflected in `disableAnimations` when 0 |

## Fallback Strategies

### Strategy 1: Skip Animation (Duration.zero)
```dart
// Best for decorative animations
duration: animDuration(context, const Duration(milliseconds: 300)),
```

### Strategy 2: Instant State Change
```dart
// For essential transitions (card flip)
if (MediaQuery.of(context).disableAnimations) {
  setState(() => _showingFront = !_showingFront);
  return;
}
_ctrl.forward();  // animated flip
```

### Strategy 3: Reduced Motion (Fade Instead of Slide)
```dart
// For page transitions — fade is gentler than slide
Widget transition(Animation<double> anim, Widget child) {
  if (MediaQuery.of(context).disableAnimations) {
    return FadeTransition(opacity: anim, child: child);
  }
  return SlideTransition(
    position: Tween(begin: const Offset(1, 0), end: Offset.zero).animate(anim),
    child: child,
  );
}
```

## What Must Still Animate (Even in Reduce Motion)
- Loading spinners (but use simple rotation, not complex)
- Progress indicators
- Focus ring visibility
- Scroll position changes (but instant, not smooth)

## What Must Stop
- Parallax effects
- Background animations (particle, confetti)
- Auto-playing carousels
- Bouncing/pulsing attention indicators
- Stagger delays (show all items instantly)

## VocabApp Checklist
- [x] `animDuration()` helper exists
- [ ] All `AnimationController` durations use `animDuration()`
- [ ] Page transitions have fade fallback
- [ ] Card flip has instant state change fallback
- [ ] XP/streak animations skip in reduce-motion
- [ ] Confetti/celebration effects disabled in reduce-motion
