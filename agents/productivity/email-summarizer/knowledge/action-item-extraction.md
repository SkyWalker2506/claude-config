---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Action Item Extraction

## Quick Reference

**Sinyal kelimeler (EN + TR):** *please send, by EOD, deadline, review, approve, FYI only, lütfen, son tarih, onay, bekliyoruz*

| Çıkarım tipi | Örnek cümle | Çıktı alanı |
|--------------|-------------|-------------|
| İstek | "Please review the attached PDF by Friday" | `action`, `due=Friday`, `artifact=PDF` |
| Bilgi | "For your awareness, we shipped v2" | `type=fyi`, no due |
| Soru | "Can we move the call to 3pm?" | `action=respond`, `due=implicit-24h` |

**Güven skoru:** 0.0–1.0; `<0.6` → "insan doğrulaması" etiketi.

```text
Alanlar: WHO (owner), WHAT (fiil + nesne), WHEN (ISO-8601 veya relative), WHERE (link/thread)
```

## Patterns & Decision Matrix

| Yöntem | Doğruluk | Maliyet | Ne zaman |
|--------|----------|---------|----------|
| Kural + regex (tarih/saat) | Orta | Düşük | Tekrarlayen iş mailleri |
| NER + fiil çerçevesi (SBV) | Yüksek | Orta | Serbest metin gövde |
| İnsan düzeltme döngüsü | En yüksek | Yüksek | Hukuki / finansal |

**Çakışma:** Aynı thread’de iki farklı due date → en erken tarihi seç ve `conflict=true` işaretle.

## Code Examples

**Yapılandırılmış aksiyon satırı (JSON — araçlar arası):**

```json
{
  "message_id": "18f7ab...",
  "actions": [
    {
      "verb": "review",
      "object": "Q2 budget spreadsheet",
      "assignee": "self",
      "due": "2026-04-12T17:00:00-04:00",
      "confidence": 0.82
    }
  ]
}
```

**Tarih çözümleme (Python — dateutil örnek):**

```python
from dateutil import parser
raw = "EOD Friday"
# Takvim bağlamı: timezone kullanıcı profilinden
due = parser.parse("Friday", fuzzy=True)  # + business rule: EOD = 17:00 local
```

**Özet bloğu (metin çıktı):**

```text
[ACTIONS] msg=18f7ab...
1. [P1] Review Q2 budget — due 2026-04-12 17:00 ET — conf 0.82
2. [FYI] Shipping notice v2 — no action
```

## Anti-Patterns

- **CC’deki kişiyi owner sanmak:** Varsayılan owner = `To` ilk adresi; CC sadece bilgi.
- **"ASAP"i tarih sanmamak:** ASAP → `due=null`, `priority=high`, kullanıcıya net sor.
- **Ek içeriği okumadan aksiyon yazmak:** "See attached" varsa `artifact=attachment_required`.
- **Tamamlanmış işi yeniden açmak:** `Re:` zincirinde "Done" / "Shipped" geçiyorsa yeni aksiyon üretme.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Temporal expressions — TIMEX3 / ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) — tarih normalizasyonu
- [Universal Dependencies — dependency parsing](https://universaldependencies.org/) — özne-fiil-nesne çerçevesi
- [Gmail — Threads and messages](https://developers.google.com/gmail/api/guides/threads) — thread içi bağlam
