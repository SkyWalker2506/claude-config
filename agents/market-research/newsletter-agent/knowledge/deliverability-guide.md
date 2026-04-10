---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 5
---

# Deliverability guide (SPF, DKIM, DMARC, reputation)

## Quick Reference

| Katman | Ne yapar |
|--------|-----------|
| **SPF** | Hangi host’ların domain adınıza mail gönderebileceğini DNS’te listeler |
| **DKIM** | Mesaja kriptografik imza — transitte değişiklik tespiti |
| **DMARC** | SPF/DKIM başarısızlığında politika (none → quarantine → reject) + raporlama |
| **IP / domain reputation** | Gmail/Outlook “bulk” davranışı — şikayet ve bounce oranı kritik |

**Sıra:** Önce auth (SPF+DKIM+DMARC), sonra içerik ve frekans.

## Patterns & Decision Matrix

| Belirti | Önce bunu kontrol et |
|---------|----------------------|
| Tümü spam klasörü | DMARC raporları + Postmaster Tools |
| Sadece bir ISP’de düşük inbox | O ISP’nin FBL / şikayet oranı |
| Yeni domain | Warm-up: küçük hacim, engaged segment |

| DMARC politikası | Ne zaman |
|------------------|----------|
| `p=none` | İlk doğrulama ve rapor toplama |
| `p=quarantine` | SPF/DKIM stabil |
| `p=reject` | Üretim, spoof riski yüksek |

## Code Examples

**DNS kayıt örnekleri (özet — gerçek değer ESP’den gelir):**

```dns
; SPF — tek satır, include zinciri kısa tutulur
example.com. IN TXT "v=spf1 include:sendgrid.net ~all"

; DKIM — selector._domainkey
s1._domainkey.example.com. IN TXT "v=DKIM1; k=rsa; p=MIGf..."

; DMARC
_dmarc.example.com. IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

**Log satırı yorumu (ESP):**

```text
spf=pass (sender IP authorized) dkim=pass (signature verified) dmarc=pass
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| SPF’de birden fazla all veya çakışan include | Geçersiz / tutarsız auth |
| Shared IP’de şikayetli komşu | Senin domain’e sıçrayan reputation |
| Liste temizlemeden tekrar blast | Kalıcı blok |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Google Postmaster Tools](https://postmaster.google.com/) — domain itibarı
- [Google — Gmail bulk sender guidelines](https://support.google.com/mail/answer/81126)
- [M3AAWG — best practices](https://www.m3aawg.org/published-documents)
- [DMARC.org](https://dmarc.org/) — politika ve raporlama
- [RFC 7489](https://www.rfc-editor.org/rfc/rfc7489) — DMARC spesifikasyonu
