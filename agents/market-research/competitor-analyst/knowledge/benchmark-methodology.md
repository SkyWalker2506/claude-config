---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Benchmark Methodology

## Quick Reference

| Adım | Açıklama |
|------|----------|
| **1. Metrik seçimi** | Karşılaştırılabilir KPI (latency, NPS proxy, fiyat/ koltuk) |
| **2. Peer set** | Aynı ICP + benzer ACV; outlier’ları etiketle |
| **3. Veri toplama** | Birincil (ürün) + ikincil (rapor); tarih hizalaması |
| **4. Normalize** | Birim başına, coğrafya, para birimi |
| **5. Güven aralığı** | Veri kalitesi düşükse aralık ver, tek sayı iddia etme |

**Benchmark amacı:** “Kimin lider olduğu” değil — **gap analizi ve iyileştirme önceliği**.

## Patterns & Decision Matrix

| Metrik türü | Örnek | Dikkat |
|-------------|-------|--------|
| Ürün | Özellik var/yok, entegrasyon sayısı | Versiyon tarihi |
| Finansal | Rule of 40, net retention | Halka açık vs. tahmin |
| Operasyonel | SLA, destek süresi | Self-reported bias |

### Rapor yapısı

1. **Yöntem** — kim, ne, ne zaman ölçüldü
2. **Tablo** — normalize değerler
3. **Gap** — biz vs. medyan / hedef
4. **Öneri** — 3 aksiyon, etki/tahmini çaba

## Code Examples

### Örnek: normalize benchmark satırı

```yaml
metric_id: "time_to_first_value_hours"
peer: "Competitor A"
segment: "Mid-market B2B SaaS"
value: 48
currency_normalized: "USD_ACV"
confidence: "medium"
as_of: "2026-01-15"
source_type: "secondary_annual_report"
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Apples-to-oranges (farklı segment) | Yanlış sonuç |
| Cherry-picking tek metrik | Strateji körlüğü |
| Rakip iç verisini ifşa etme | Etik + hukuk riski |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [APQC — benchmarking](https://www.apqc.org/benchmarking) — süreç benchmark metodolojisi
- [SaaS Metrics — OPEXEngine / industry reports](https://www.opengine.com/) — SaaS karşılaştırma kültürü (kaynak notu)
- [ISO 22316 — Organizational resilience](https://www.iso.org/standard/50003.html) — kurumsal dayanıklılık bağlamı
- [NIST — Cybersecurity Framework](https://www.nist.gov/cyberframework) — güvenlik benchmark çerçevesi (B2B tech için)
