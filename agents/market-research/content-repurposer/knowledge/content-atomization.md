---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Content Atomization

## Quick Reference

**Atomization:** Tek “pillar” içeriği (webinar, rapor, uzun makale) **yeniden kullanılabilir atomlara** bölmek — alıntı, grafik, SSS, kısa video.

| Atom türü | Kaynak bölüm |
|-----------|----------------|
| **Pull quote** | Güçlü cümle — görsel kart |
| **Stat** | Tek rakam + kaynak dipnotu |
| **SSS** | Uzun paragraf → soru başlıklı kısa cevap |
| **Checklist** | Prosedür bölümünden madde madde |

**Kural:** Her atom **bağımsız okunabilir** ve **kaynak linki** taşır.

## Patterns & Decision Matrix

| Pillar uzunluğu | Atom sayısı (kılavuz) |
|-----------------|------------------------|
| 2 000 kelime | 8–15 atom |
| 60 dk webinar | 10–20 klip + 5 alıntı |

### Öncelik sırası

1. Mesaj hiyerarşisi (en önemli 3 iddia)
2. Görsel / veri varlığı
3. Kanal uygunluğu (metin vs. video)

## Code Examples

### Örnek: pillar → atom listesi

```markdown
Pillar: "2026 Q1 product webinar"

Atoms:
- [QUOTE] "Ship dashboards in a sprint" — timestamp 12:40
- [STAT] 73% faster time-to-insight (n=120 customers)
- [FAQ] "Does it support Snowflake?" → 3-sentence answer + doc link
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Bağlamı olmayan alıntı | Yanlış yorum |
| Telifsiz görsel kesiti | Hukuk riski |
| Aynı atomu 20 kez yayınlamak | Yorgunluk / spam |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Content Marketing Institute — repurposing](https://contentmarketinginstitute.com/) — metod makaleleri
- [HubSpot — content strategy](https://www.hubspot.com/marketing) — pillar/cluster
- [Wikipedia — fair use](https://en.wikipedia.org/wiki/Fair_use) — telif bağlamı (ABD; bölgeye göre farklı)
- [Creative Commons](https://creativecommons.org/) — lisans türleri
