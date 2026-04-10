---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Unit Economics

## Quick Reference

| Metrik | Formül (yaygın) | Not |
|--------|-----------------|-----|
| **CAC** | Satış+pazarlama gideri / yeni müşteri | Zaman gecikmesi (payback) |
| **LTV** | ARPA × marj × (1/churn) veya NPV akışı | B2B’de genişletme dahil mi netleştir |
| **LTV:CAC** | Oran hedefi tipik 3:1+ (kaynak bağlı) | Segment bazlı |
| **Payback** | CAC / (ARPA × gross margin) | Ay cinsinden |

**Contribution margin:** Gelir − doğrudan değişken maliyet (hosting, destek birimi, ödeme ücreti).

## Patterns & Decision Matrix

| Soru | Eğer kötüyse |
|------|--------------|
| CAC yükseliyor | Kanal verimsizliği veya satış verimliliği |
| Churn yüksek | Ürün-pazar uyumu veya onboarding |
| Marj düşük | Fiyat veya COGS yapısı |

### Basit kontrol listesi

- [ ] Churn **aylık** mi yıllık mı — tutarlı kullan
- [ ] “Müşteri” tanımı — logo mu koltuk mu
- [ ] Serbest nakit vs. muhasebe kârı — yatırım için hangisi

## Code Examples

### Örnek: CAC / LTV kontrol tablosu

```markdown
| Segment | CAC | LTV (36m) | LTV:CAC | Payback |
|---------|-----|-----------|---------|---------|
| SMB PLG | $1.2k | $9k | 7.5x | 11 mo |
| Mid-market | $18k | $96k | 5.3x | 16 mo |
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| LTV’ye hayalî genişleme koymak | Şişirilmiş değerleme |
| Sadece blended CAC | Verimsiz kanalı gizler |
| Viral katsayıyı 1’e yakın varsaymak | Büyüme planı çöker |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [David Skok — SaaS Metrics](https://www.forentrepreneurs.com/saas-metrics/) — klasik tanımlar
- [Bessemer — 10 laws of cloud](https://www.bvp.com/atlas) — birim ekonomi perspektifi
- [McKinsey — Sales & marketing efficiency](https://www.mckinsey.com/capabilities/growth-marketing-and-sales) — GTM verimliliği
- [SaaS Capital — churn benchmarks](https://www.saascapital.com/) — churn veri kültürü
- [Lenny Rachitsky — B2B metrics](https://www.lennysnewsletter.com/) — güncel pratik örnekler
