---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Meta Tag Optimization

## Quick Reference

| Etiket | Rol | Uzunlık kuralı (kılavuz) |
|--------|-----|-------------------------|
| `<title>` | SERP başlığı — birincil sıralama sinyali | ~50–60 karakter (kesilme mobilde) |
| `meta name="description"` | Snippet — CTR | ~120–160 karakter |
| `meta robots` | index/noindex, follow | Dikkatli kullan |
| Open Graph / Twitter Card | Sosyal önizleme — doğrudan klasik sıralama değil | Görsel + başlık tutarlılığı |

**Google:** Meta description sıralama için doğrudan “sıra garantisi” değil; **snippet kaynağı** ve CTR etkisi önemli.

## Patterns & Decision Matrix

| Sayfa tipi | Title formülü örneği |
|------------|----------------------|
| Ürün | `{Ürün adı} — {ana fayda} \| {Marka}` |
| Blog | `{Konu}: {çıkarım} \| {Marka}` |
| Yerel | `{Hizmet} in {Şehir} \| {Marka}` |

### Snippet iyileştirme

- Anahtar kelimeyi doğal yerleştir
- Tekrarlayan şablonları azalt (Search Console’da düşük CTR’lı URL’ler)
- Structured data ile uyumlu iddia (ör. fiyat, stok — doğru olmalı)

## Code Examples

### Örnek: title + meta şablonu

```html
<title>Embedded Analytics SDK for SaaS | AnalyticsBoard</title>
<meta name="description" content="Ship customer-facing dashboards in days. Row-level security, SSO, &lt;200 KB SDK. SOC2-ready.">
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Her sayfada aynı title | Cannibalization + düşük CTR |
| Clickbait ile içerik uyumsuz | Core update’te risk |
| Keywords meta’ya güvenmek | Çoğu motor yok sayar |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google — Snippet kontrolü](https://developers.google.com/search/docs/appearance/snippet) — resmi rehber
- [Google — Title links](https://developers.google.com/search/docs/appearance/title-link) — başlık yeniden yazımı
- [Open Graph protocol](https://ogp.me/) — sosyal meta
- [Twitter — Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards) — kart türleri
