---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Timezone Handling

## Quick Reference

**IANA öncelik:** `America/New_York` gibi TZ identifier kullan; sabit `-05:00` sadece anlık offset için. Depoda her zaman UTC veya `dateTime` + `timeZone` çifti.

| Kavram | Doğru | Yanlış |
|--------|-------|--------|
| Etkinlik saklama | `2026-07-15T14:00:00` + `Europe/Istanbul` | `UTC+3` sabitle |
| Gösterim | Kullanıcı TZ’de render | Sunucu TZ’sinde string |

**DST:** Geçiş günlerinde "2:30" yerel saat yoksa → API hata veya kaydırma; test et.

```text
Kural: karşılaştırma ve overlap hep UTC instant üzerinden
```

## Patterns & Decision Matrix

| Senaryo | Yaklaşım |
|---------|----------|
| Tek organizer TZ | Tüm davetler organizer TZ gösterimi + UTC alt metin |
| Dağıtık ekip | "Local time for each" + tek Zoom saati UTC |
| Seyahat | `floating` yerine her zaman TZ ID bağla |

**Kütüphane seçimi:** Python `zoneinfo` (3.9+); JS `Intl` + `Temporal` (gelecek); IANA `tzdata` güncel tut.

## Code Examples

**Python — zoneinfo ile instant:**

```python
from zoneinfo import ZoneInfo
from datetime import datetime
start = datetime(2026, 4, 9, 10, 0, tzinfo=ZoneInfo("America/New_York"))
start_utc = start.astimezone(ZoneInfo("UTC"))
```

**JavaScript — kullanıcıya gösterim:**

```javascript
const d = new Date('2026-04-09T14:00:00-04:00');
new Intl.DateTimeFormat('tr-TR', {
  timeZone: 'Europe/Istanbul',
  dateStyle: 'medium',
  timeStyle: 'short'
}).format(d);
```

**Toplantı davetinde çift zaman (metin şablon):**

```text
10:00–10:30 Eastern (15:00–15:30 Istanbul) | UTC 14:00–14:30
```

## Anti-Patterns

- **"EST" ve "EDT" karıştırmak:** Metinde IANA veya UTC kullan.
- **TZ olmadan seri tekrar (RRULE):** RRULE `TZID` ile tanımlanmalı.
- **Yaz saati politikası değişikliği:** Sistem `tzdata` güncellemesi olmadan eski offset.
- **Floating all-day + saatli karışımı:** `DATE` vs `DATE-TIME` ayrımını koru.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [IANA Time Zone Database](https://www.iana.org/time-zones) — güncel bölge tanımları
- [RFC 5545 — TZID](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.5) — iCalendar TZ
- [Unicode CLDR — timezone labels](https://cldr.unicode.org/) — görünen isimler
