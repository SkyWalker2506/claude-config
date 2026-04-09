---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Platform Store Analysis

## Quick Reference

| Mağaza | Metrik |
|--------|--------|
| Steam | wishlist, bölge fiyat |
| Mobile | ASO, kategori |
| Console | TRC süreçleri |

## Patterns & Decision Matrix

| Çıkış | Kontrol |
|-------|---------|
| İlk hafta | görünürlük + indirim politikası |

## Code Examples

```text
[STORE] platform=steam | tags=[…] | similar_wishlist_median=… | price_band=$15-25
```

## Anti-Patterns

- Bölge fiyatını kopyala-yapıştır uyumsuz.

## Deep Dive Sources

- Steamworks dokümantasyonu
