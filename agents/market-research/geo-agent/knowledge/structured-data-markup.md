---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Structured Data Markup

## Quick Reference

| Tür | Schema.org tipi | Yaygın kullanım |
|-----|-----------------|-----------------|
| Kuruluş | Organization, LocalBusiness | Logo, iletişim, adres |
| Ürün | Product, Offer | Fiyat, stok, yorum |
| İçerik | Article, FAQPage, HowTo | zengin sonuç uygunluğu |
| Breadcrumb | BreadcrumbList | navigasyon |

**Format:** JSON-LD önerilir (Google dokümantasyonu); Mikrodata/RDFa eski kod tabanlarında.

## Patterns & Decision Matrix

| Kontrol | Araç |
|---------|------|
| Sözdizimi | Rich Results Test / Schema Validator |
| İçerik uyumu | Sayfada görünen metin ile işaretlenen veri aynı mı |
| Tekil entity | Aynı ürün için çakışan işaretlemeler |

### FAQPage dikkat

- Sadece **gerçekten** SSS olan içerik
- Google yönergeleri: manipülatif SSS spam’i risk

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sahte AggregateRating | Manuel işlem |
| Her sayfaya Organization tekrarı | Gürültü; kritik sayfalarda odaklan |
| Eski fiyat Offer’da | Yanlış zengin sonuç |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google — Structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) — giriş
- [Schema.org](https://schema.org/) — tip sözlüğü
- [Google — Search Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) — uygun türler
- [W3C — JSON-LD](https://www.w3.org/TR/json-ld11/) — syntax
- [validator.schema.org](https://validator.schema.org/) — doğrulama
