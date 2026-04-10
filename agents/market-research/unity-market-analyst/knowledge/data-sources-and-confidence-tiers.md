---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Data sources and confidence tiers for game market analysis

## Quick Reference

| Tier | Kaynak örnekleri | Kullanım |
|------|------------------|----------|
| **A — Yüksek** | Steam Charts (oyuncu sayısı), resmi Unity/Unreal blog, düzenleyici raporlar | Slayt’ta doğrudan alıntı |
| **B — Orta** | Newzoo / Data.ai özetleri, güvenilir basın, GDC özetleri | Trend yönü — mutlak sayı şart değil |
| **C — Düşük** | Reddit anket, tek başarılı oyun hikayesi | “Sinyal” olarak etiketle |

H16 her sayıda **tarih + kaynak** veya “tahmin” etiketi ister.

## Patterns & Decision Matrix

| İddia | Gereken kanıt |
|-------|-----------------|
| “Tür X büyüyor” | En az 2 bağımsız kaynak veya aralık |
| “Unity şu segmentte önde” | Motor + hedef platform + ekip becerisi üçlüsü |
| Gelir tahmini | Düşük / orta / yüksek senaryo |

## Code Examples

**Rapor üst bilgi (YAML — H16 çıktı meta):**

```yaml
analysis_id: pitch_deck_q2_2026
confidence_policy:
  tier_A_sources: ["steamdb.info", "unity.com/releases"]
  tier_B_sources: ["gamesindustry.biz"]
  assumptions:
    - arppu_midcore: { low: 12, mid: 22, high: 40, unit: USD }
```

**Slayt dipnotu (Markdown):**

```markdown
> Oyuncu sayıları: Steam Charts, çekim 2026-04-01. Tahmin aralığı: ekip varsayımı — finansal tavsiye değildir.
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Tek viral oyunla TAM | Yatırımcı reddi |
| 3 yıllık motor tablosu | Güncel özellik seti yanlış |
| Bölgesiz fiyat | Satın alma gücü hatası |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [SteamDB](https://steamdb.info/) — istatistikler
- [Unity — gaming reports](https://unity.com/solutions/gaming)
- [Unreal — industry](https://www.unrealengine.com/en-US/solutions)
- [IGDA — surveys](https://igda.org/) — geliştirici anketleri
