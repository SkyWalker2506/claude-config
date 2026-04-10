---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Technical SEO Guide

## Quick Reference

| Konu | Kontrol |
|------|---------|
| **Crawl** | XML sitemap, internal link derinliği, log analizi |
| **Rendering** | JS SSR/CSR — Google’nin render ettiği HTML |
| **HTTPS** | Mixed content, HSTS |
| **Hreflang** | Çok dilli duplicate yönetimi |
| **Pagination** | rel=prev/next kullanımı (sayfa yapısına göre) |
| **404/410** | Kırık link, soft 404 |

**Hreflang:** Her dil sürümü karşılıklı işaret etmeli; yoksa yanlış ülke sürümü gösterilebilir.

## Patterns & Decision Matrix

| Site tipi | Ekstra |
|-----------|--------|
| Büyük e-ticaret | Faceted navigation parametreleri — canonical |
| SPA (React/Vue) | hydration hataları, boş ilk HTML |
| Çok dil | URL yapısı + hreflang + çeviri kalitesi |

### Araç zinciri (örnek)

Search Console → Crawl stats → URL Inspection → Lighthouse (CWV) → log (Bulutflare/Akamai) 

## Code Examples

### Örnek: Core Web Vitals field verisi (CrUX benzeri)

```json
{
  "origin": "https://example.com",
  "LCP": { "p75_ms": 2100 },
  "INP": { "p75_ms": 180 },
  "CLS": { "p75": 0.08 }
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sonsuz parametre URL’leri | Crawl bütçesi israfı |
| Mobil ve desktop farklı içerik | Mobile-first uyumsuzluğu |
| Staging’i indexlettirmek | Duplicate / düşük kalite |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google — JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) — render
- [Google — Site structure](https://developers.google.com/search/docs/specialty/ecommerce/help-google-understand-your-ecommerce-site-structure) — e-ticaret yapı
- [Mozilla — HTTP status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — kod anlamları
- [web.dev — Learn performance](https://web.dev/learn/performance/) — teknik performans
- [Bing — SEO](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) — ikinci motor teknik
