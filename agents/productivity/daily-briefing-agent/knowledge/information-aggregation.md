---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Information Aggregation

## Quick Reference

**Kaynaklar:** L1 (e-posta), L2 (takvim), görev listesi (Jira/Linear/Apple Reminders), opsiyonel RSS/haber MCP. Birleştirme = tek zaman damgası ekseninde sıralama + çakışma tespiti.

| Kaynak | Çekirdek alan | Tazelik SLA |
|--------|---------------|-------------|
| Gmail | `internalDate`, thread | <15 dk |
| Calendar | `updated`, `start` | Canlı |
| Jira | `updated` | Pull sırasında |

**Çakışma:** Aynı slot’ta iki hard meeting → üstte uyarı kutusu.

```text
merge_policy: email_threads_dedupe_by_threadId | calendar_wins_on_time_conflict_display
```

## Patterns & Decision Matrix

| Birleştirme | Artı | Eksi |
|-------------|------|------|
| Zaman çizelgesi önce | Gün planı net | E-posta ikinci planda kalabilir |
| Risk önce (P0) | Acil görünür | Takvim kaçabilir |
| Hibrit skor | Dengeli | Ayar gerekir |

**Idempotent:** Aynı brifing penceresi iki kez çalışırsa aynı hash (`sha256(sorted source ids)`) ile dedup.

## Code Examples

**Birleştirilmiş zaman çizelgesi satırları:**

```text
08:00  [CAL] Focus block
09:30  [CAL] Team sync
10:00  [MAIL] P1 — Vendor invoice (thread 18ab…)
10:30  [TASK] CRITICAL JIRA-441 — assigned you
```

**Pseudo-merge (Python):**

```python
def merge_events(cal, mail_actions, tasks):
    items = []
    for e in cal: items.append(("ts", e.start, "CAL", e))
    for m in mail_actions: items.append(("ts", m.due or m.received, "MAIL", m))
    for t in tasks: items.append(("ts", t.due, "TASK", t))
    return sorted(items, key=lambda x: x[1])
```

**Veri çizgisi uyumu (log):**

```json
{"briefing_id":"bf-20260409","sources":{"gmail":42,"calendar":6,"jira":3},"merged":51,"deduped":2}
```

## Anti-Patterns

- **Eski önbelleği sessizce kullanmak:** Kaynak hata verdiyse "STALE" etiketi göster.
- **Gizli kaynak karıştırma:** Kişisel Gmail + iş takvimi politikasına aykırı olabilir; scope ayır.
- **Aşırı çekirdek:** 100+ mail özeti tek brifingde — üst 5 + "see L1 full".

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Gmail API — batch](https://developers.google.com/gmail/api/guides/batch) — çoklu istek
- [Microsoft Graph — combine queries](https://learn.microsoft.com/en-us/graph/query-parameters) — `$expand`, `$select`
- [Event sourcing basics](https://martinfowler.com/eaaDev/EventSourcing.html) — birleştirme ve sıra tutarlılığı
