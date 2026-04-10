---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 5
---

# Pricing Psychology

## Quick Reference

| İlke | Örnek | Risk |
|------|-------|------|
| **Anchoring** | Önce yüksek paket göster | Güven — desteklenmeli |
| **Charm pricing** | $9.99 | B2B’de bazen düşük algı |
| **Decoy** | Orta tier’ı “sweet spot” yap | Etik — manipülasyon algısı |
| **Loss aversion** | “Kaybetme” çerçevesi | A/B ile ölç |
| **Default effect** | Yıllık varsayılan | İptal sürtünmesi (regülasyon) |

**B2B:** Psikoloji + ROI hesabı; satın alma komitesi rasyonel kanıt ister.

## Patterns & Decision Matrix

| Segment | Ton |
|---------|-----|
| Self-serve | Net fiyat, şeffaf karşılaştırma |
| Enterprise | Özel teklif + değer tablosu |
| Global | Yerel referans fiyat (anchor) farklı olabilir |

### Deney tasarımı notu

- Kontrol ve varyant **tek değişken** (fiyat veya sunum, ikisi birden değil — başlangıç için)
- Örnek gücü — dönüşüm oranı düşükse süre uzar

## Code Examples

### Örnek: fiyat sunumu (Good / Better / Best)

```markdown
| Tier | Price | Anchor copy |
|------|-------|-------------|
| Starter | $29 | "For individuals" |
| Team | $99 | **Most popular** — "Everything in Starter + SSO" |
| Business | $299 | "SOC2 + audit logs" |
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Gizli ücret | Güven ve chargeback |
| Sınırsız “son fırsat” | Mesaj tükenmesi |
| Psikoloji jargonu ile iç ekip aldatmak | Yanlış ürün önceliği |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Kahneman — Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow) — önyargı çerçevesi (özet)
- [Behavioral Economics — OECD](https://www.oecd.org/) — politika ve tüketici (arama: behavioral)
- [Nielsen Norman — UX & pricing](https://www.nngroup.com/) — fiyat sayfası kullanılabilirliği
- [Cialdini — Influence](https://www.influenceatwork.com/) — ikna ilkeleri (resmi kaynak)
- [Google Optimize sunset](https://support.google.com/optimize) — A/B araç geçişi (2023 sonrası alternatifler ara)
