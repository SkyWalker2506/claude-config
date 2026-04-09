---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Source Credibility

## Quick Reference

| Tier | Örnek | Güven skoru (başlangıç) |
|------|-------|-------------------------|
| **T0 — Birincil** | RFC, resmi doküman, mahkeme kararı, peer-reviewed | 0.9–1.0 |
| **T1 — İkincil güçlü** | Büyük yayınevleri, standart kuruluş blogları | 0.7–0.85 |
| **T2 — Uzman içerik** | Bilinen maintainer, şirket teknik blogu | 0.55–0.75 |
| **T3 — Dikkat** | Forum, Reddit, anonim wiki | 0.3–0.5 (doğrulama şart) |

```text
Hızlı kontrol: Yazar adı? Tarih? Editör / peer review? Çıkar çatışması?
```

## Patterns & Decision Matrix

| Sinyal | Pozitif | Negatif |
|--------|---------|---------|
| Domain | `.gov`, `.edu`, bilinen org | Yeni kayıt, typo-squat |
| Yazar | Doğrulanabilir profil | Yok veya sahte |
| Atıf | Kaynakça var | “Studies show” kaynaksız |
| Güncellik | Versiyon notu | “2020” sabit kalmış API sayfası |

**Karar:** T3 kaynak yalnızca hipotez üretir; iddia T0/T1 ile çaprazlanmadan rapora “unverified” yaz.

## Code Examples

**Kaynak kartı şablonu:**

```text
[SOURCE]
url: …
tier: T2
author: … | published: … | updated: …
conflict_of_interest: none | unknown | yes (detail)
claim_supported: primary | secondary | anecdotal
```

## Anti-Patterns

- **Domain otoritesine tek başına güvenmek:** Eski `.edu` sayfası güncel olmayabilir.
- **Yıldız / upvote saymak:** Popülerlik ≠ doğruluk.
- **Çeviri zincirini kaynak saymak:** Orijinal dili bul veya “translated summary” işaretle.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [CRAAP test (California State University overview)](https://libguides.csuchico.edu/c.php?g=414307) — Currency, Relevance, Authority, Accuracy, Purpose
- [IFLA How to Spot Fake News](https://www.ifla.org/publications/node/11174) — hızlı kontrol listesi
