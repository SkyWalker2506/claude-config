---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Briefing Format Design

## Quick Reference

**Katmanlar:** (1) Executive 3 satır — bugünün kazanımı, en büyük risk, tek odak; (2) Zaman çizelgesi — bloklar; (3) Gelen kutusu / görev özeti; (4) Opsiyonel haberler.

| Bölüm | Hedef uzunluk | Okuma süresi hedefi |
|-------|---------------|---------------------|
| Üst özet | ≤80 kelime | <30 sn |
| Takvim | 5–8 madde | <45 sn |
| Aksiyonlar | 3–7 P0–P2 | <60 sn |

**Tutarlılık:** Her gün aynı sıra; kullanıcı kas is hafızası ile tarar.

```text
Etiketler: [CAL] [MAIL] [TASKS] [NEWS] — her blokta max 1 emoji veya 0
```

## Patterns & Decision Matrix

| Format | Artı | Eksi | Kullan |
|--------|------|------|--------|
| Markdown | Kopyala-yapıştır, Git | Mobil render değişir | Teknik kullanıcı |
| Düz metin | Evrensel | Zayıf vurgu | SMS / Telegram |
| HTML e-posta | Zengin | Spam filtresi | Haftalık özet |

**Kişiselleştirme:** Hafta içi vs hafta sonu şablonu; seyahat günü uçuş bloğu ekle.

## Code Examples

**Sabah brifing iskeleti:**

```markdown
## Daily Briefing — 2026-04-09 (Wed) — Europe/Istanbul

**Focus:** Ship billing hotfix before 14:00.
**Risk:** Vendor API rate limit unknown.
**Win if:** Deploy green + zero S1.

### Calendar (next 12h)
- 09:30 Stand-up — Zoom
- 11:00 Vendor call — **prep: SLA doc**

### Inbox (L1 digest)
- P1: 2 threads need reply (finance, HR)

### Tasks (pulled)
- [ ] Merge PR #442 — blocking release
```

**JSON tüketim şeması (otomasyon):**

```json
{
  "date": "2026-04-09",
  "tz": "Europe/Istanbul",
  "focus_one_liner": "Ship billing hotfix",
  "sections": ["calendar", "mail", "tasks", "news"]
}
```

## Anti-Patterns

- **Wall of text:** Üstte özet yoksa kullanıcı kaybolur.
- **Çift bilgi:** Takvimde olan şeyi görevlerde tekrar etme; `see calendar` ile işaretle.
- **Duygusal dil:** Brifing nötr ve fiil odaklı olmalı.
- **Tarih/saat TZ belirsiz:** Her zaman başlıkta TZ yaz.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Plain Language guidelines](https://www.plainlanguage.gov/) — kısa üst özet yazımı
- [Google Material — communication density](https://m3.material.io/) — bilgi yoğunluğu (UI paraleli)
- [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) — tarih formatı
