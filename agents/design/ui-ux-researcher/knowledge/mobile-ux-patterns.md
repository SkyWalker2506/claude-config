---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Mobile UX Patterns

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

## Bottom Navigation (M3 NavigationBar)
- Max 5 destinations, min 3
- Always show labels (no icon-only on mobile)
- Active indicator: pill shape with tonal fill
- Badge support for notifications/streaks
- VocabApp targets: Home, Quiz, Review, Profile (4 tabs)

## Gesture Navigation
- Swipe-back: system-level on iOS, predictive back on Android 14+
- Swipe-to-dismiss: cards, notifications, list items
- Pull-to-refresh: data lists, word lists
- Long-press: context menus, word details
- Avoid gesture conflicts with bottom sheets and horizontal scrolling

## Progressive Disclosure
- Show essential info first, details on demand
- Expandable cards for word details (definition → examples → conjugation)
- Bottom sheets for filters/settings (not full pages)
- Stepper for multi-step quiz setup
- VocabApp: quiz options should collapse into "Advanced" section

## Onboarding Flows
- Max 3-4 screens; skip button always visible
- First screen: value prop (not feature list)
- Interactive onboarding > passive carousel
- VocabApp: language select → difficulty → first word pack → done
- Defer sign-up until user has experienced value

## Tab Patterns
- Scrollable tabs for 4+ categories (quiz types)
- Fixed tabs for 2-3 categories
- Tab content should lazy-load

## Empty States
- Illustration + message + primary CTA
- Context-specific (not generic "nothing here")
- VocabApp: "Start your first quiz" with arrow pointing to quiz tab

## Search Patterns
- Persistent search bar on list pages
- Recent searches + suggestions
- Filter chips below search bar
- Debounce input (300ms)
