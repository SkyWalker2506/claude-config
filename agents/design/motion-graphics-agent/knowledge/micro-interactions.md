---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Micro-Interactions

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

## Button Feedback
```dart
// Scale down on press, bounce back
GestureDetector(
  onTapDown: (_) => _ctrl.forward(),
  onTapUp: (_) => _ctrl.reverse(),
  onTapCancel: () => _ctrl.reverse(),
  child: ScaleTransition(
    scale: Tween(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut),
    ),
    child: quizAnswerButton,
  ),
)
```
- Duration: 100ms press, 150ms release
- Pair with haptic: `HapticFeedback.lightImpact()`

## 3D Card Flip (VocabApp Flashcard)
```dart
Widget build(BuildContext context) {
  return GestureDetector(
    onTap: () => _showingFront ? _ctrl.forward() : _ctrl.reverse(),
    child: AnimatedBuilder(
      animation: _ctrl,
      builder: (_, __) {
        final angle = _rotation.value;
        final showFront = angle < pi / 2;
        return Transform(
          alignment: Alignment.center,
          transform: Matrix4.identity()
            ..setEntry(3, 2, 0.001)  // perspective
            ..rotateY(angle),
          child: showFront
              ? _frontSide()
              : Transform(
                  alignment: Alignment.center,
                  transform: Matrix4.rotationY(pi),
                  child: _backSide(),
                ),
        );
      },
    ),
  );
}
```
- Duration: 400ms; Curve: easeInOutCubic
- VocabApp has `flash_card_view.dart` — enhance with this pattern

## Swipe Interactions
```dart
Dismissible(
  key: Key(word.id),
  direction: DismissDirection.horizontal,
  onDismissed: (dir) => dir == DismissDirection.endToStart
      ? markIncorrect(word) : markCorrect(word),
  background: _swipeBackground(Colors.green, Icons.check, Alignment.centerLeft),
  secondaryBackground: _swipeBackground(Colors.red, Icons.close, Alignment.centerRight),
  child: WordCard(word: word),
)
```

## Haptic Pairing
| Action | Haptic | Flutter API |
|--------|--------|------------|
| Correct answer | Medium | `HapticFeedback.mediumImpact()` |
| Incorrect answer | Heavy + vibrate | `HapticFeedback.heavyImpact()` |
| Badge unlock | Success pattern | `HapticFeedback.heavyImpact()` × 2 |
| Button tap | Light | `HapticFeedback.lightImpact()` |
| Streak increment | Selection | `HapticFeedback.selectionClick()` |

## XP Counter Animation
```dart
// Animated number that counts up
TweenAnimationBuilder<int>(
  tween: IntTween(begin: oldXP, end: newXP),
  duration: const Duration(milliseconds: 600),
  builder: (_, value, __) => Text(
    '+$value XP',
    style: Theme.of(context).textTheme.headlineSmall,
  ),
)
```

## Principles
- Every tap should have visual + haptic response within 100ms
- Keep micro-interactions under 300ms
- Respect `animDuration()` — skip animation if reduce-motion is on
