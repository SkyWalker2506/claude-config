---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Reporting and experimentation rhythm

## Quick Reference

| Ritim | Çıktı |
|-------|--------|
| **Haftalık** | Kanal bazlı özet — reach, engagement rate, link tıklaması |
| **Aylık** | Sütun performansı, kazanan format, öğrenme notu |
| **Çeyrek** | OKR hizası — takipçi değil iş sonucu (lead, trial) |

Her deney için **tek değişken** hipotezi; kontrol haftası ile kıyas.

## Patterns & Decision Matrix

| KPI | Ne zaman kullan |
|-----|------------------|
| ER (engagement rate) | Organik kalite |
| CTR | Trafik hedefi |
| Saves / shares | Üst huni farkındalık |
| CPL (paid) | M4 ile birlikte |

## Code Examples

**Haftalık tablo (Markdown — yönetici özeti):**

```markdown
| Kanal | Gönderi | Reach | ER% | Not |
|-------|---------|-------|-----|-----|
| IG | Reels x3 | 42k | 4.2 | Hook A kazandı |
| LI | Doküman x1 | 12k | 2.1 | CTA LinkedIn Learning |
```

**UTM disiplini (kampanya bazlı):**

```
https://example.com/signup?utm_source=instagram&utm_medium=organic&utm_campaign=q2_launch&utm_content=reel_hookA
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Vanity metrik (sadece takipçi) | Bütçe yanlış yere |
| Aynı hafta 5 değişken | Sonuç yorumlanamaz |
| UTM’siz link | Attribution kaybı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Analytics 4 — traffic acquisition](https://support.google.com/analytics/)
- [North Star Framework](https://amplitude.com/blog/north-star-metric) — ürün metrikleri
- [Meta Business — insights](https://www.facebook.com/business/insights)
