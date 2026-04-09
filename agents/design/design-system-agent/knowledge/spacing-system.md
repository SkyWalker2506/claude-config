---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Spacing System

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

## 4px Base Grid
| Token | Value | Usage |
|-------|-------|-------|
| xs | 4 | Icon-text gap, dense lists |
| sm | 8 | Chip padding, compact spacing |
| md | 12 | List item padding |
| base | 16 | Card padding, section gaps |
| lg | 24 | Section separation |
| xl | 32 | Page margins (compact) |
| 2xl | 48 | Hero section spacing |

## Flutter Implementation
```dart
abstract final class Spacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 12;
  static const double base = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;
}

// Usage
Padding(padding: const EdgeInsets.all(Spacing.base))
SizedBox(height: Spacing.lg)
```

## Responsive Spacing
```dart
EdgeInsets adaptivePadding(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;
  if (width >= 840) return const EdgeInsets.symmetric(horizontal: 48, vertical: 24);
  if (width >= 600) return const EdgeInsets.symmetric(horizontal: 32, vertical: 20);
  return const EdgeInsets.symmetric(horizontal: 16, vertical: 16);
}
```

## M3 Component Spacing
- NavigationBar height: 80dp (includes 12dp top padding for indicator)
- Card internal padding: 16dp
- List item: 16dp horizontal, 8-12dp vertical
- Dialog: 24dp padding
- Bottom sheet: 16dp horizontal, handle area 22dp

## VocabApp Rules
- Page scaffold: `EdgeInsets.all(16)` minimum
- Between sections: `SizedBox(height: 24)`
- Card content: `EdgeInsets.all(16)`
- Quiz answer buttons: 8dp gap between options
- Bottom nav safe area: respect `MediaQuery.padding.bottom`
- Never use arbitrary values (13, 17, 23) — stick to the 4px grid
