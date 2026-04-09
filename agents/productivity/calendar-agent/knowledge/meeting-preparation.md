---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Meeting Preparation

## Quick Reference

**Hazırlık checklist (toplantı öncesi T-24h / T-1h):** amaç, gündem (≤5 madde), karar beklenen sorular, ön okuma linkleri, not alan kişi, zaman sınırı.

| Toplantı türü | Süre önerisi | Ön koşul |
|---------------|--------------|----------|
| 1:1 | 25–30 dk | Haftalık durum özeti |
| Karar toplantısı | ≤45 dk | Ön doküman 24h önce |
| Beyin fırtınası | 45–60 dk | problem tanımı tek paragraf |

```text
Çıktı: agenda.md veya takvim açıklama alanına yapıştırılabilir blok + OKR bağlantısı
```

## Patterns & Decision Matrix

| Kalıp | Artı | Eksi |
|-------|------|------|
| DACI / RACI | Net karar sahibi | Kurumsal ağırlık |
| Lean agenda (3 madde) | Odak | Geniş konu sığmaz |
| Pre-read zorunlu | Kaliteli tartışma | Katılım düşebilir |

**L2 → L6 köprüsü:** Hazırlık maddeleri toplantı notları şablonunun `Context` bölümüne gider.

## Code Examples

**Markdown gündem şablonu:**

```markdown
# Decision: API versioning — 2026-04-10

## Goal
Pick v1 sunset date for mobile clients.

## Agenda (30m)
1. Metrics review (5m) — @alice
2. Options A/B/C (15m) — open discussion
3. Decision & next steps (10m) — @bob decides

## Pre-read
- [doc] /docs/api-versioning.md
- [dashboard] error rates Q1

## Decisions needed
- Sunset date: ? 
- Comms owner: ?
```

**Takvim açıklama alanı (kısa):**

```text
AGENDA: (1) Metrics (2) Options (3) Decision | PRE-READ: link in invite | NOTE-TAKER: @alice
```

**L3 brifing entegrasyonu (satır):**

```text
NEXT_MEETING[10:00 ET]: API versioning — bring: error rate screenshot | decision owner: @bob
```

## Anti-Patterns

- **Gündemsiz "sync":** Amaç yoksa toplantıyı e-posta veya dokümana çevir.
- **Herkese aynı ön okuma:** Rol bazlı "required" vs "optional" ayır.
- **Not alan atamadan başlama:** Sonuç L6'da aksiyon çıkmaz.
- **Süre aşımı:** Her madde için zaman kutusu; taşanı ertesi toplantıya taşı.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Atlassian — meeting agenda tips](https://www.atlassian.com/work-management/project-management/meeting-agenda) — yapı ve örnekler
- [MIT — effective meetings](https://hr.mit.edu/learning-topics/teams/articles/effective-meetings) — hazırlık ve roller
- [Minto Pyramid — SCQA](https://www.amazon.com/Minto-Pyramid-Principle-Logic-Writing/dp/0273710516) — net problem çerçevesi (kitap referansı)
