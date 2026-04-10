---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 5
---

# Email Copywriting

## Quick Reference

| Eleman | İpucu |
|--------|--------|
| **Konu satırı** | Fayda + merak — 40–60 karakter test |
| **Ön metin** | Konuyu destekle, tekrar etme |
| **İlk cümle** | Kişiselleştirme veya net değer |
| **CTA** | Fiil + sonuç (“Rezervasyonu gör”) |
| **PS** | Son bir itirazı kapat |

**Ton:** Marka sesi rehberi — resmî / samimi / teknik.

## Patterns & Decision Matrix

| Kampanya | Yapı |
|----------|------|
| Nurture serisi | Problem → içerik → sosyal kanıt → demo |
| Lansman | Hikaye → özellik → sık sorulan itiraz |

### Okunabilirlik

- Kısa paragraflar, madde işaretleri
- Jargon — sadece ICP uygunsa

## Code Examples

**Konu satırı varyant seti (A/B/C test için JSON — ESP metadata):**

```json
{
  "campaign_id": "summer_launch_2026",
  "subjects": [
    { "id": "A", "text": "Yeni API: 40% daha az gecikme", "preheader": "Ölçümler canlı ortamda" },
    { "id": "B", "text": "Sadece bugün: erken erişim", "preheader": "Kuyruk sırası korunur" },
    { "id": "C", "text": "{{first_name}}, son 3 yer kaldı", "preheader": "Workshop kaydı için" }
  ]
}
```

**Markdown → düz metin gövde (CTA tek):**

```markdown
{{first_name}},

Dün anlattığımız *batch inference* limiti artık hesabınızda.

[Limiti kontrol et →](https://app.example.com/usage?utm_source=news&utm_medium=email&utm_campaign=summer26)

— Ekip
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Clickbait konu + zayıf içerik | Şikayet ve churn |
| ALL CAPS | Spam filtresi |
| Çok kişisel veri (yanlış birleştirme) | Güven kaybı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Copyhackers — email](https://copyhackers.com/) — dönüşüm odaklı yazım
- [DMA — email marketing](https://thedma.org/) — endüstri ilkeleri
- [AP Stylebook](https://www.apstylebook.com/) — tutarlı dil (isteğe bağlı)
- [Google — Gmail bulk sender guidelines](https://support.google.com/mail/answer/81126) — teslimat bağlamı
- [Litmus — subject line](https://www.litmus.com/blog/) — test ve trend yazıları
