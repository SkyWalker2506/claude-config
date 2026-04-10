---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# A/B Test Pricing

## Quick Reference

| Karar | Öneri |
|-------|--------|
| **Metrik** | Birincil: gelir / kullanıcı veya dönüşüm; guardrail: churn, refund |
| **Süre** | Haftalık sezonalite; minimum örnek — power analizi |
| **Katman** | Coğrafya veya kullanıcı % segmenti — kanalıştırma |
| **Etik / hukuk** | Ayrımcı fiyatlandırma ve KVKK — hukuk incelemesi |

**Çok-arm bandit:** Çok varyantta öğrenme hızı — fakat iş yorumu için hâlâ sabır gerekir.

## Patterns & Decision Matrix

| Hipotez şablonu | Örnek |
|-----------------|--------|
| “$X → $Y self-serve checkout’ta dönüşüm Z% değişir” | |
| “Yıllık indirim %A → %B payback’i iyileştirir” | |

### İstatistik

- **Significance:** p-value veya Bayesian posterior — tek başına “%5 lift” yetmez
- **Sipariş etkisi:** Yeni kullanıcılar vs. mevcut — farklı popülasyon

## Code Examples

### Örnek: fiyat A/B test planı

```markdown
Hypothesis: +10% on Pro tier does not reduce conversion >5%
Split: 50/50 by account_id hash (sticky)
Primary metric: net new MRR / visitor
Guardrails: refund rate, sales cycle length
Stop rule: 2 weeks OR 5k exposures per arm
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Peeking (erken durdurma) | False positive |
| Tek gün verisi | Hafta içi/sonu bias |
| Fiyat testini ürün değişikliği ile aynı anda | Hangi etki? |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Evan Miller — sample size](https://www.evanmiller.org/ab-testing/sample-size.html) — örnek büyüklüğü hesaplayıcı mantığı
- [Google — GA4 experiments](https://support.google.com/analytics/) — deney dokümantasyonu
- [Optimizely — Stats engine](https://www.optimizely.com/optimization-glossary/statistical-significance/) — sık kullanılan terimler
- [Harvard — A/B testing pitfalls](https://hbr.org/) — iş bağlamı (arama: A/B testing)
- [Stripe — Billing](https://stripe.com/docs) — fiyat değişimi ve faturalama teknik sınırları
