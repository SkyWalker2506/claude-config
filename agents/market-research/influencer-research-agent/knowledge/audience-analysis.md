---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Audience Analysis

## Quick Reference

| Metrik | Anlam |
|--------|-------|
| Demografi | yaş, ülke |
| İlgi grafiği | kategori örtüşmesi |
| Sahte etkileşim | yorum kalitesi |

## Patterns & Decision Matrix

| Uyum | Eşik |
|------|------|
| Marka | ton + değerler |
| Ürün | kullanım senaryosu örtüşmesi |

## Code Examples

```text
[AUDIENCE] overlap_with_icp=72% | geo_match=primary_markets | risk=fake_followers_low
```

## Anti-Patterns

- Sadece takipçi sayısı ile seçim.

## Deep Dive Sources

- Audience analytics tool dokümantasyonları
