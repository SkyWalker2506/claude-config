---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Scheduling Optimization

## Quick Reference

**Hedef:** Minimize toplantı parçalanması + maksimize odak blokları. Tipik odak bloğu 90–120 dk; buffer 10–15 dk aralar.

| Metrik | İyi aralık | Ölçüm |
|--------|------------|-------|
| Meeting load / hafta | <20 saat (bilgi işi) | Takvim toplam süre |
| Context switch | Düşük | ardışık farklı tür toplantı sayısı |
| Maker ratio | >40% takvim | focus etiketli blok / çalışma saati |

**Find a time:** Katılımcı `freeBusy` kesişimi + organizasyon çalışma saatleri.

## Patterns & Decision Matrix

| Strateji | Artı | Eksi | Ne zaman |
|----------|------|------|----------|
| Meeting-free günler | Derin iş | Cross-tz zor | Ürün / mühendislik |
| Tüm toplantıları öğleden önce | Tek blok öğle sonrası | Erken saat yükü | US-centric ekipler |
| Round-robin host | Yük dengeleme | Tutarsız agenda | Dönüşümlü sync |

**Constraint satisfaction:** Önce zorunlu katılımcılar, sonra opsiyonel; en dar pencereden başla.

## Code Examples

**Free/busy kesişimi (pseudo):**

```python
def intersect_free(slots_a, slots_b):
    out = []
    for a in slots_a:
        for b in slots_b:
            s, e = max(a[0], b[0]), min(a[1], b[1])
            if s < e:
                out.append((s, e))
    return merge_adjacent(out)
```

**Google Calendar `freebusy.query` gövdesi:**

```json
{
  "timeMin": "2026-04-10T00:00:00Z",
  "timeMax": "2026-04-10T23:59:59Z",
  "items": [{ "id": "primary" }, { "id": "peer@company.com" }]
}
```

**Optimizasyon çıktısı (agent):**

```text
[SCHEDULE] candidates=3 | best=slot-2
slot-1: 2026-04-10 09:00-09:30 ET | score=72 | fragmentation=high
slot-2: 2026-04-10 10:00-10:30 ET | score=91 | after_focus_block
slot-3: 2026-04-10 14:00-14:30 ET | score=78 | before_1on1
recommendation: slot-2
```

## Anti-Patterns

- **30 dk toplantıyı 8 parçaya bölmek:** Minimum blok 25 dk (pomodoro uyumlu) veya tam iptal.
- **Herkese aynı ağırlık:** Organizer ve decision-maker’a daha yüksek ağırlık ver.
- **Travel time sıfır:** Fiziksel lokasyon varsa önce/sonra 15–30 dk buffer.
- **Gece yarısı sınırı yok:** Global ekip için `earliest_local` / `latest_local` kısıtı koy.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Calendar — Freebusy](https://developers.google.com/calendar/v3/reference/freebusy/query) — müsaitlik API
- [Microsoft Graph — getSchedule](https://learn.microsoft.com/en-us/graph/api/calendar-getschedule) — çoklu takvim
- [Paul Graham — Maker's Schedule](http://www.paulgraham.com/makersschedule.html) — odak vs toplantı çatışması
