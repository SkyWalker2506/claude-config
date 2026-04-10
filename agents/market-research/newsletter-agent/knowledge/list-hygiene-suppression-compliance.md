---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# List hygiene, suppression, and compliance

## Quick Reference

| Kavram | Ne zaman |
|--------|----------|
| **Hard bounce** | Kalıcı geçersiz adres — listeden çıkar |
| **Soft bounce** | Geçici (kota, kutusu dolu) — 3–5 deneme sonra suppress |
| **Complaint** | “Spam” işareti — hemen suppress + kök neden |
| **Global suppression** | Tüm kanallarda gönderim durdur |
| **Çift opt-in** | AB için güçlü izin kanıtı (AB ülkeye göre değişir) |

KVKK: işleme şartı, bilgilendirme, saklama süresi — segmentasyonla birlikte **amaç** dokümante.

## Patterns & Decision Matrix

| Sinyal | Aksiyon |
|--------|---------|
| Unsubscribe | Anında listeden çık; tercih merkezine yönlendir |
| Role address (abuse@, postmaster@) | Teknik kontakt; pazarlama gönderme |
| GDPR erase request | CRM + ESP birlikte sil / anonimleştir |

## Code Examples

**Suppression CSV (ESP içe aktarım şeması):**

```csv
email,reason,source_ts,expires_ts
user@example.com,hard_bounce,2026-04-01T12:00:00Z,
other@example.com,complaint,2026-04-02T09:00:00Z,
```

**Webhook pseudo (SendGrid / Postmark — complaint):**

```json
POST /hooks/esp
{
  "event": "spam_complaint",
  "email": "user@example.com",
  "timestamp": "2026-04-10T10:00:00Z",
  "sg_message_id": "abc123"
}
```

→ Handler: `suppression_list.add(email, reason='complaint')`.

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Bounce’u tekrar tekrar göndermek | Gönderici itibar düşüşü |
| “Tek tıkla çık” linkini gizlemek | CAN-SPAM / PECR ihlali |
| Üçüncü parti listeyi ısıtmadan göndermek | Yüksek şikayet, domain blacklist |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [FTC CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — ABD ticari e-posta
- [ICO PECR — electronic mail](https://ico.org.uk/for-organisations/direct-marketing/) — UK
- [Google — Gmail sender guidelines](https://support.google.com/mail/answer/81126) — teslimat ve şikayet
- [M3AAWG — best practices](https://www.m3aawg.org/published-documents) — operasyonel hijyen
