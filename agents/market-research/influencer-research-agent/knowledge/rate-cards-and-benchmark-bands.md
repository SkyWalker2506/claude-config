---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Rate cards, CPM/CPE bands, and negotiation bands

## Quick Reference

| Terim | Anlam |
|-------|--------|
| **CPM** | 1000 gösterim başına maliyet (paid) |
| **CPE** | Etkileşim başına (etkileşim tanımı platforma göre) |
| **Deliverable set** | 1 Reels + 1 Story + usage 30 gün |
| **Exclusivity** | Rakip yasağı — süreye göre prim |

H15 **bant** verir; kesin fiyat avukat / satın alma işi değildir. Bölge ve nişe göre 10x fark normaldir.

## Patterns & Decision Matrix

| Takipçi bandı | Tipik not (2025–2026, göreli) |
|---------------|-------------------------------|
| Mikro (<50k) | Yüksek ER, düşük tek başına ücret |
| Orta (50k–500k) | Story + feed paketi |
| Makro (500k+) | Ajans üzerinden, uzun sözleşme |

## Code Examples

**Brief’te ücret bandı (aralık):**

```yaml
creator: "@indie_dev_tr"
metrics:
  followers: 82000
  median_views_reel: 45000
  er_last_30d: 0.031
fee_band_usd: [1200, 2200]
deliverables:
  - 1x 45s Reels + hook A/B
  - 2x Story with swipe
usage_rights: organic_social_90d
exclusivity: none
```

**Rakip benchmark tablosu (iç analiz):**

```markdown
| Kampanya | Creator tier | Est. CPM band | Kaynak |
|----------|--------------|---------------|--------|
| A — mobil oyun | mid | $8–$15 | influencer platform quote |
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Tek veri noktasıyla “adil fiyat” | Pazar dışı kalır |
| Ücreti DM’de açıkça garanti etmek | Sözleşme öncesi risk |
| Sadece takipçi ile tier | Bot şişirmesi |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [IAB — influencer guidelines](https://www.iab.com/) — endüstri çerçevesi
- [ASA (UK) — influencer ad disclosure](https://www.asa.org.uk/) — şeffaflık
- Platform creator marketplace şeffaf bantları (Instagram, TikTok) — güncel dokümantasyon
