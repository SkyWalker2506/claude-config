---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Priority Classification

## Quick Reference

**Skor bileşenleri (örnek ağırlık):** gönderen rolü (0–40) + gecikme saati (0–30) + konu anahtar kelime (0–20) + ek varlığı (0–10). Normalize 0–100 → P0≥85, P1 60–84, P2 35–59, P3 <35.

| Sinyal | P0 eşiği örneği |
|--------|-----------------|
| Üst yönetici domain + doğrudan To | +35 |
| SLA ihlali (yanıt süresi >48h iş günü) | +25 |
| Kelime: "urgent", "legal", "invoice due" | +15 each (cap) |

```text
Çıktı: P0|P1|P2|P3 + kısa gerekçe (max 12 kelime) + risk etiketi: FIN|HR|LEGAL|NONE
```

## Patterns & Decision Matrix

| Model | Artı | Eksi | Kullan |
|-------|------|------|--------|
| Sabit kurallar | Açıklanabilir | Esnek değil | Regulated industries |
| Skor + eşik | Ayarlanabilir | Ağırlık drift | L1 varsayılan |
| Tam LLM sınıflandırma | Bağlamsal | Tutarsız | Sadece skor sonrası tie-break |

**Eisenhower × e-posta:** Acil+önemli → P0; önemli değil → digest veya arşiv.

## Code Examples

**Skor hesaplama (YAML politika — kullanıcıya göre düzenlenir):**

```yaml
priority_policy:
  version: 1
  weights:
    sender_tier:
      exec: 40
      team: 25
      external_unknown: 10
    latency_hours_unreplied:
      per_hour_after_sla: 2
      cap: 30
  thresholds:
    P0: 85
    P1: 60
    P2: 35
```

**Sınıflandırma satırı (çıktı):**

```text
[PRIORITY] id=msg-1844 | score=72 | band=P1 | reasons=direct_to+latency_36h | tags=FIN
```

**Basit eşik kontrolü (bash — harici skor dosyasından):**

```bash
score=72
if   (( score >= 85 )); then echo P0
elif (( score >= 60 )); then echo P1
elif (( score >= 35 )); then echo P2
else echo P3
fi
```

## Anti-Patterns

- **Sadece konu satırına güvenmek:** Phishing ve newsletter konu satırı sıklıkla yanıltıcı.
- **Hafta sonu P0 şişirmesi:** Hafta sonu gelenleri SLA dışı say veya `defer_to_monday`.
- **Aynı gönderene sürekli P0:** Rate-limit: gönderen başına max 2 P0/gün.
- **Duygusal dil = aciliyet:** "I'm so sorry" ≠ P0; skor tablosuna bağla.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [NIST — phishing resistance](https://www.nist.gov/itl/applied-cybersecurity/email-and-phishing) — öncelik ve güvenlik ayrımı
- [Eisenhower matrix — productivity research](https://asana.com/resources/eisenhower-matrix) — acil/önemli çerçeve
- [Gmail labels and importance](https://developers.google.com/gmail/api/guides/labels) — API ile etiket senkronu
