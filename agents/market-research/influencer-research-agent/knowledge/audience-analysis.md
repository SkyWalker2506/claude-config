---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 5
---

# Audience analysis (overlap, fraud, fit)

## Quick Reference

| Metrik | Ne ölçer |
|--------|-----------|
| **Demografi** | Yaş, ülke, dil — ICP ile örtüşme |
| **İlgi grafiği** | Niş kategoriler (oyun, dev, lifestyle) |
| **Engagement quality** | Yorum derinliği, kaydetme / paylaşım oranı |
| **Sahte sinyal** | Ani takipçi sıçraması, bot yorumlar, düşük ER |

Mikro-influencer’da **ER** genelde makro’ya göre daha yüksek; mutlak reach değil **hedef kitle örtüşmesi** öncelik.

## Patterns & Decision Matrix

| Uyum | Eşik / not |
|------|------------|
| Marka değerleri | Çelişen sponsor geçmişi → risk |
| Ürün kullanımı | Gerçek kullanım içeriği var mı |
| Coğrafya | Lansman ülkesi ile kitle uyumu |

| Risk | Gösterge |
|------|----------|
| Yüksek | Takipçi/ER oranı anormal, yorumlar şablon |
| Orta | Karışık kitle — daraltılmış demo ile test |
| Düşük | Tutarlı niş + organik etkileşim |

## Code Examples

**Kısa liste skoru (spreadsheet formül mantığı):**

```text
fit_score = 0.4 * icp_overlap + 0.3 * engagement_quality + 0.2 * geo_match + 0.1 * brand_safety
# Her bileşen 0–1 normalize; ağırlıklar kampanyaya göre ayarlanır
```

**YAML brief alanı (H15 çıktı):**

```yaml
creator: "@example_creator"
audience:
  primary_geo: ["TR", "DE"]
  age_band_est: "25-34"
  overlap_icp: 0.71
  fraud_risk: low
  notes: "Yorumlar konuşuyor; bot şüphesi düşük"
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sadece takipçi sayısı | Düşük dönüşüm |
| Satın alınmış takipçi profiline bütçe | ROI sıfır |
| Tek platform metriği ile karar | Örneğin sadece görüntülenme |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Meta — Brand Collabs Manager](https://www.facebook.com/business/creator-colaboration) — bağlam
- [TikTok — Creator Marketplace](https://www.tiktok.com/creators/creator-portal/) — metrikler
- [FTC — Endorsement Guides](https://www.ftc.gov/legal-library/browse/federal-register-notices/guides-concerning-use-endorsements-testimonials-advertising)
- [HypeAuditor / similar tools](https://hypeauditor.com/) — sahte takipçi tarama (üçüncü parti)
- Platform-native analytics (YouTube Studio, IG Insights) — birincil veri
