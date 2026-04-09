---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Market Timing

## Quick Reference

| Zamanlama sorusu | Veri | Çıktı |
|------------------|------|-------|
| Şimdi mi bekle mi? | TCO, ekip becerisi, risk | Karar penceresi |
| Rakip hamlesi | Release / fiyat | Tepki senaryosu |
| Regülasyon | Yürürlük tarihi | Uyum milestone |

```text
Öneri etiketi: NOW | WAIT( koşul ) | NO-GO ( gerekçe )
```

## Patterns & Decision Matrix

| Faktör | Erken | Geç |
|--------|-------|-----|
| First-mover | Pazar payı | Ölçek riski |
| Fast-follow | Öğrenilmiş dersler | Kaçırılan segment |
| Regülasyon | Belirsizlik | Uyum maliyeti |

**Karar:** “NOW” için en az iki risk azaltıcı (ör. feature flag, geri dönüş planı).

## Code Examples

**Zamanlama özeti:**

```text
[TIMING] decision=WAIT | until: stable LTS + team training done | risks: […] | review_date: …
```

## Anti-Patterns

- **Roadmap’e körü körüne güvenmek:** Tarih kayması varsayılanı koy.
- **Sunk cost:** Geçmiş yatırım “şimdi”yi zorlamamalı.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Crossing the Chasm (Moore) — özet kaynaklar](https://en.wikipedia.org/wiki/Crossing_the_Chasm) — erken çoğunluk geçişi
- Şirket içi portföy / OKR dokümanları — öncelik hizalaması
