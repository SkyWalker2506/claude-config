---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# SEO Audit Checklist

## Quick Reference

| Alan | Kontrol |
|------|---------|
| **Taranabilirlik** | robots.txt, noindex yanlışları, crawl bütçesi |
| **İndeks** | Coverage, canonical zincir, duplicate |
| **On-page** | Title, H1, meta description, iç bağlantı |
| **Performans** | LCP, INP, CLS (Core Web Vitals) |
| **Şema** | JSON-LD doğrulama, zengin sonuç uyumu |

**Öncelik:** Trafik / gelir etkisi × uygulama kolaylığı matrisi.

## Patterns & Decision Matrix

| Sorun | İlk bakılacak |
|-------|----------------|
| Sayfa indekslenmiyor | robots + canonical + iç link |
| Düşüş (tüm site) | manuel işlem / güncelleme / teknik deploy |
| Tek URL düşüşü | intent kayması, SERP özellikleri |

### Mini rapor şablonu

1. Özet (3 madde)
2. Kritik bulgular (P0/P1/P2)
3. Örnek URL’ler
4. Sonraki adımlar ve sahip

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sadece skor aracına güvenmek | Yanlış öncelik |
| Her sayfaya aynı meta | CTR düşer |
| Keyword stuffing | Spam riski |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Search Central — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) — resmi temel
- [Google — Search Quality Rater Guidelines](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) — yararlı içerik
- [Google — Core Web Vitals](https://web.dev/articles/vitals) — performans
- [Bing — Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) — ikinci motor
- [Schema.org — docs](https://schema.org/docs/documents.html) — yapılandırılmış veri
