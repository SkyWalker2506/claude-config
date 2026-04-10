---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 5
---

# Game market trends

## Quick Reference

| Sinyal | Tipik kaynak türü |
|--------|-------------------|
| **Genre momentum** | Endüstri raporu + mağaza etiket trendi |
| **Platform shift** | PC vs mobil vs konsol payı |
| **Teknoloji** | AI tooling, cross-play, UGC |
| **Regülasyon** | Çin oyun onayı, AB dijital pazar |

Trend ≠ tek oyun başarısı; **en az iki bağımsız kanıt** veya “hipotez” etiketi.

## Patterns & Decision Matrix

| Erken sinyal | Doğrulama adımı |
|--------------|-----------------|
| Sosyal hype | Steam wishlist / konferans demo |
| Basın özeti | Birincil veri veya ikinci kaynak |
| Tek AAA başarısı | Tür TAM’e genellenmez |

| Çıktı tipi | Güven seviyesi |
|------------|----------------|
| Yatırımcı slaytı | Açık aralık + kaynak dipnotu |
| İç pitch | Senaryo (düşük/orta/yüksek) |

## Code Examples

**Trend kartı (iç not — H16 çıktı):**

```yaml
trend_id: co_op_survival_2026
signals:
  - source: steam_tag_growth
    detail: "Co-op + Survival tag YoY +18% (region=WW)"
    confidence: B
  - source: industry_report_snippet
    detail: "Newzoo 2026 — co-op social engagement"
    confidence: A
conclusion: "Yükselen ilgi; tek başına TAM kanıtı değil"
```

**Steam örnek sorgu (manuel):**

```text
Store search → tag filter → sort by "New & Trending" → export wishlist delta (3rd party tools) — verify ToS
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Tek viral oyunla türü genellemek | Yanlış TAM |
| Eski rapor (2+ yıl) ile “şu an” iddiası | Reddedilen pitch |
| Bölgesiz küresel rakam | Satın alma gücü hatası |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Newzoo](https://newzoo.com/) — pazar özetleri
- [gamesindustry.biz](https://www.gamesindustry.biz/) — haber ve trend
- [Steam Charts / SteamDB](https://steamdb.info/charts/) — oyuncu sayıları
- [IGDA](https://igda.org/) — geliştirici anketleri
- [Unity Gaming Report](https://unity.com/solutions/gaming) — motor ekosistemi
