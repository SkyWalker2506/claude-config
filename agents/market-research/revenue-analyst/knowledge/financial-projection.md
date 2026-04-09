---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Financial Projection

## Quick Reference

| Bileşen | Tipik girdi | Çıktı |
|---------|-------------|--------|
| **Gelir** | ARPA, müşteri sayısı, expansion | MRR/ARR ramp |
| **COGS** | Hosting, destek, ödeme % | Brüt marj |
| **OpEx** | İşe alım planı, pazarlama bütçesi | Yanma oranı |
| **Nakit** | Tahsilat gecikmesi, capex | Runway |

**Senaryo seti:** Base / Upside / Downside — her biri için **3–5 kritik tahmin** açıkça yazılır.

## Patterns & Decision Matrix

| Yöntem | Kullanım |
|--------|----------|
| **Top-down TAM → pay** | Yatırımcı özeti |
| **Bottom-up pipeline** | Satış tahmini |
| **Monte Carlo** (ileri) | Belirsizlik aralığı — veri yeterliyse |

### Basit 12 aylık şablon (satır)

| Ay | Yeni müşteri | Churn | Net müşteri | ARPA | MRR |
|----|--------------|-------|-------------|------|-----|

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Hockey stick without pipeline | İnanılmaz plan |
| Churn’ü sabit düşük tutmak | Gerçek dışı LTV |
| Opex’i “sonra optimize ederiz” | Sonsuz runway sanrısı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [CFI — Financial modeling](https://corporatefinanceinstitute.com/resources/knowledge/modeling/financial-modeling/) — modelleme prensipleri
- [Frank Rotman — SaaS math](https://twitter.com/rotman) — işaretler (X üzerinde özetler; bağlam için)
- [SEC — MD&A guidance](https://www.sec.gov/) — halka açık şirketlerin ileriye dönük anlatımı
- [PwC — Revenue guide](https://www.pwc.com/) — gelir muhasebesi özeti
- [YC — SAFE / runway](https://www.ycombinator.com/library/) — erken aşama finansal disiplin
