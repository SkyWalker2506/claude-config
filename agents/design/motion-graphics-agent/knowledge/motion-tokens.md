---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Motion Tokens

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

## Duration Scale (M3)
| Token | Duration | Usage |
|-------|----------|-------|
| short1 | 50ms | Ripple, state change |
| short2 | 100ms | Button press feedback |
| short3 | 150ms | Fade in/out, icon change |
| short4 | 200ms | Small element transition |
| medium1 | 250ms | Card expand, chip select |
| medium2 | 300ms | Page transition, container transform |
| medium3 | 350ms | Complex layout shift |
| medium4 | 400ms | Card flip, shared axis |
| long1 | 450ms | Large surface change |
| long2 | 500ms | Full-screen transition |
| extraLong1 | 700ms | Staggered list entrance |

## Flutter Implementation
```dart
abstract final class MotionTokens {
  static const short1 = Duration(milliseconds: 50);
  static const short2 = Duration(milliseconds: 100);
  static const short3 = Duration(milliseconds: 150);
  static const short4 = Duration(milliseconds: 200);
  static const medium1 = Duration(milliseconds: 250);
  static const medium2 = Duration(milliseconds: 300);
  static const medium3 = Duration(milliseconds: 350);
  static const medium4 = Duration(milliseconds: 400);
  static const long1 = Duration(milliseconds: 450);
  static const long2 = Duration(milliseconds: 500);
}
```

## Easing Curves (M3)
| Token | Flutter Curve | Usage |
|-------|--------------|-------|
| emphasized | Curves.easeInOutCubicEmphasized | Primary transitions |
| emphasizedDecelerate | Curves.easeOutCubic | Enter screen |
| emphasizedAccelerate | Curves.easeInCubic | Exit screen |
| standard | Curves.easeInOutCubic | Property changes |
| standardDecelerate | Curves.easeOut | Appear/fade in |
| standardAccelerate | Curves.easeIn | Disappear/fade out |

## Stagger Patterns
```dart
// List item stagger: each item delayed by 50ms
for (int i = 0; i < items.length; i++) {
  final delay = Duration(milliseconds: i * 50);
  Future.delayed(delay, () => _itemControllers[i].forward());
}
```
- Max stagger offset: 700ms total (don't delay last item too long)
- Cap visible staggered items at 8-10

## VocabApp Motion Map
| Widget | Duration | Curve |
|--------|----------|-------|
| Flash card flip | medium4 (400ms) | easeInOutCubic |
| Quiz answer feedback | short3 (150ms) | easeOut |
| Page transition | medium2 (300ms) | easeInOutCubicEmphasized |
| XP counter | medium2-long2 | easeOut |
| Streak animation | medium1 (250ms) | easeOutBack |
| Word list stagger | 50ms per item | easeOut |
