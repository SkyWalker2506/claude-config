---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Value-Based Pricing

## Quick Reference

| Adım | Çıktı |
|------|--------|
| **1. Sonuç metrikleri** | Müşterinin ölçtüğü KPI (gelir artışı, maliyet düşüşü, risk) |
| **2. Alternatif maliyet** | Manuel süre, mevcut araç, rakip TCO |
| **3. Pay alma** | Müşteri değerinin % kaçı bizde kalır — adil aralık |
| **4. Kanıt** | Önce-sonra, pilot, müşteri hikayesi |

**Formül fikri:** `Fiyat ≈ (Değer − Alternatif maliyet) × Pay oranı` — sayılar müşteri özelinde kalibre edilir.

## Patterns & Decision Matrix

| B2B satış aşaması | Araç |
|-------------------|------|
| Keşif | Değer mülakatı soruları |
| Teklif | ROI tek sayfa |
| Yenileme | Gerçekleşen değer vs. vaat |

### Risk

| Durum | Strateji |
|-------|----------|
| Değer ölçülemez | Kullanım veya sonuç garantisi ile hizala |
| Uzun ROI | Aşamalı fiyat veya başarı ücreti |

## Code Examples

### Örnek: değer hesabı (basit)

```text
Baseline: manual SQL hours / month per analyst = 40
After: 10 hours (75% reduction)
Loaded cost $80/h → $2,400 saved / analyst / month
Price ask: 20% of savings = $480 seat/month ceiling
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| “%10 tasarruf” iddiası kanıtsız | Satış itirazı |
| Tüm müşterilere aynı pay | Büyük hesapta kayıp |
| Sadece özellik sayısıyla değer | Value-based değil |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [HBR — Value-based pricing](https://hbr.org/) — strateji makaleleri (arama)
- [McKinsey — Pricing solutions](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/how-we-help-clients/pricing) — kurumsal çerçeve
- [Holden Advisors — value selling](https://www.holdenadvisors.com/) — B2B değer satışı
- [Gartner — Total Cost of Ownership](https://www.gartner.com/en/information-technology/glossary/total-cost-of-ownership-tco) — TCO tanımı
- [Challenger — ROI calculator patterns](https://www.challengerco.com/) — müşteri ekonomisi anlatımı
