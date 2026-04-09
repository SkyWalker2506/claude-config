---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Calendar Management

## Quick Reference

**Temel nesneler:** `VEVENT` (toplantı), `VTODO` (görev — bazı istemcilerde ayrı), `VAVAILABILITY` (çalışma saatleri). Google: `calendarId` = `primary` veya paylaşılan ID; Microsoft: `calendarGroup` + `calendar`.

| İşlem | Google Calendar API | Graph API |
|-------|---------------------|-----------|
| Listele | `events.list` | `GET /me/calendarView` |
| Oluştur | `events.insert` | `POST /me/events` |
| Seri | `recurrence[]` RRULE | `recurrence` pattern |

```text
Minimum olay alanları: summary, start, end, timezone, attendees (opsiyonel), transparency (busy/free)
```

## Patterns & Decision Matrix

| Kalıp | Artı | Eksi | Ne zaman |
|-------|------|------|----------|
| Tek takvim | Basit | Karışık öncelik | Kişisel |
| Takvim / renk / proje | Net ayrım | Senkron yükü | Ekip |
| Focus blokları | Derin iş | Overbooking riski | Maker schedule |

**Busy vs Free:** Dış görünürlükte sadece "busy" göster; konu gizli tutulabilir (`private` / `confidential`).

## Code Examples

**iCalendar VEVENT özeti (RFC 5545):**

```text
BEGIN:VEVENT
UID:20260409T140000Z-team-sync@company.com
DTSTAMP:20260409T120000Z
DTSTART;TZID=America/New_York:20260409T100000
DTEND;TZID=America/New_York:20260409T103000
SUMMARY:Team sync
LOCATION:https://meet.company.com/abc-defg-hij
END:VEVENT
```

**Google Calendar — insert gövdesi (JSON):**

```json
{
  "summary": "Design review",
  "start": { "dateTime": "2026-04-10T15:00:00-04:00", "timeZone": "America/New_York" },
  "end": { "dateTime": "2026-04-10T16:00:00-04:00", "timeZone": "America/New_York" },
  "attendees": [{ "email": "peer@company.com" }],
  "conferenceData": { "createRequest": { "requestId": "req-uuid-1" } }
}
```

**Çakışma kontrolü (mantık):**

```text
overlap = (startA < endB) AND (endA > startB)
free_busy_allowed = NOT overlap OR (transparency == transparent)
```

## Anti-Patterns

- **UTC’ye çevirmeden karşılaştırma:** Her zaman IANA TZ ile normalize et.
- **DST atlama günü:** Sabit "offset" kullanma; TZ veritabanı kullan.
- **Seriyi tek tek silmek:** `recurringEventId` + `instance` veya `Range` parametresi.
- **Davetsiz dışarı katılımcı:** `attendees` eklemeden Zoom linki herkese açık paylaşma.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [RFC 5545 — iCalendar](https://www.rfc-editor.org/rfc/rfc5545) — VEVENT, RRULE
- [Google Calendar API — Events](https://developers.google.com/calendar/api/guides/create-events) — insert, conference
- [Microsoft Graph — calendar](https://learn.microsoft.com/en-us/graph/api/resources/event) — event resource
