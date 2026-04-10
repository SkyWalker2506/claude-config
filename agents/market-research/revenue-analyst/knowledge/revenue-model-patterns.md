---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Revenue Model Patterns

## Quick Reference

| Model | Gelir tanımı | Tipik marj baskısı |
|-------|----------------|---------------------|
| **Subscription (SaaS)** | MRR/ARR | Churn, NRR |
| **Usage / consumption** | Birim başına | Fiyat elastikiyeti, tahmin zorluğu |
| **Marketplace** | Komisyon (GMV üzerinden) | İki taraflı denge, dolandırıcılık |
| **Freemium** | Ücretli dönüşüm | Destek maliyeti, dönüşüm hunisi |
| **Hardware + software** | Donanım + recurring | Stok, garanti |

**Net gelir:** Brüt satışlar − iadeler − indirimler (GAAP/IFRS uyumu için raporlama kuralına bak).

## Patterns & Decision Matrix

| Seçim sorusu | Etki |
|--------------|------|
| Kim ödüyor? | B2B proc vs. bireysel kart |
| Sözleşme süresi | Tahsilat ve churn profili |
| Ürün sınırı | Hangi modül ayrı SKU |

### Basit gelir su şeması

`Leads → Trials → Paid → Expansion → Renewal`

Her aşama için **dönüşüm %** ve **ortalama gelir** tanımla; aksi halde projeksiyon spekülatif kalır.

## Code Examples

### Örnek: basit birim ekonomisi

```text
ARPA = $2,400/year
Gross margin = 78%
CAC payback = 14 months (target ≤ 18)
Net retention = 115%
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| GMV’yi gelir sanmak | Marketplace’te komisyon oranı şart |
| “Tüm müşteriler aynı” | Segment bazlı ACV şart |
| Tek senaryo | Yatırımcı / iç plan için yetersiz |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Bessemer — Cloud Index](https://www.bvp.com/cloud-index) — SaaS metrikleri ve kıyaslar
- [OpenView — SaaS benchmarks](https://openviewpartners.com/blog/) — expansion ve PLG
- [Stripe Atlas — Business models](https://stripe.com/atlas/guides) — ödeme ve gelir tanımı
- [IFRS 15 — Revenue recognition](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-15-revenue-from-contracts-with-customers/) — muhasebe çerçevesi
- [a16z — Marketplace guides](https://a16z.com/) — iki taraflı pazar dinamikleri (makale araması)
