---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Responsive Layout

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

## M3 Window Size Classes
| Class | Width | VocabApp Target |
|-------|-------|----------------|
| Compact | <600dp | Phone (primary) |
| Medium | 600-839dp | Tablet portrait |
| Expanded | 840dp+ | Tablet landscape |

## LayoutBuilder Pattern
```dart
class AdaptiveWordGrid extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final columns = constraints.maxWidth >= 840 ? 3
            : constraints.maxWidth >= 600 ? 2
            : 1;
        return GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columns,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
          ),
          itemCount: words.length,
          itemBuilder: (ctx, i) => WordCard(word: words[i]),
        );
      },
    );
  }
}
```

## MediaQuery Usage
```dart
// Screen dimensions
final size = MediaQuery.sizeOf(context);        // preferred over .of(context).size
final padding = MediaQuery.paddingOf(context);  // safe area

// Orientation
final isLandscape = size.width > size.height;

// Text scale
final textScale = MediaQuery.textScaleFactorOf(context);
```

## Adaptive Breakpoints Helper
```dart
enum WindowSize { compact, medium, expanded }

WindowSize windowSize(BuildContext context) {
  final width = MediaQuery.sizeOf(context).width;
  if (width >= 840) return WindowSize.expanded;
  if (width >= 600) return WindowSize.medium;
  return WindowSize.compact;
}
```

## VocabApp Layout Rules
- Phone: single column, bottom nav, full-width cards
- Tablet portrait: 2-column grid for word cards, side panel for detail
- Bottom nav → NavigationRail at medium+
- Quiz: always single column (focus mode)
- Settings: single column with grouped sections

## Safe Area
```dart
// Always wrap scaffold body content
SafeArea(
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: content,
  ),
)
```
- Bottom nav already handles bottom safe area
- AppBar handles top safe area
