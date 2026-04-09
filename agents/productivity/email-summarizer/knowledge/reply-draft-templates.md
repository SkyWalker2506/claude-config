---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Reply Draft Templates

## Quick Reference

**Kurallar:** Taslak asla otomatik gönderilmez; kullanıcı onayı zorunlu. Konu satırına `Re:` ekle; thread `In-Reply-To` / `References` başlıklarını koru.

| Ton | Tetikleyici | Uzunluk |
|-----|-------------|---------|
| Kısa onay | İç ekip, düşük risk | 2–4 cümle |
| Resmî dış | Müşteri / vendor | 1 paragraf + sonraki adım |
| Red / erteleme | Kapasite / scope | Net gerekçe + alternatif tarih |

```text
Yapı: (1) Teşekkür / bağlam (2) Cevap veya taahhüt (3) Sonraki adım + imza
```

## Patterns & Decision Matrix

| Şablon | Kullan | Kaçın |
|--------|--------|-------|
| ACK + tarih | Onay bekleyen iş | Belirsiz "will revert soon" |
| Soru listesi | Netleştirme gerek | Spam thread’de çok soru |
| Escalation notice | Üst yönetim bilgilendirme | Her küçük konuda CC şişirme |

**Dil:** Alıcı dili = gövde dili; karışık thread’de son mesajın diline uy.

## Code Examples

**Dış müşteri — gecikme özürü + yeni tarih:**

```text
Subject: Re: {original_subject}

Hi {first_name},

Thanks for your patience. We’re still reviewing {artifact}. I’ll send an update by {iso_date} EOD {timezone}.

Best,
{signature}
```

**İç ekip — kısa onay:**

```text
+1 on the approach. I’ll take the API changes; @peer can handle docs. Target: {date}.
```

**Gmail API taslak oluşturma (yapı — gönderim yok):**

```http
POST https://gmail.googleapis.com/gmail/v1/users/me/drafts
Content-Type: application/json

{
  "message": {
    "raw": "{base64url_rfc2822_with_thread_headers}"
  }
}
```

**Thread başlıklarını koruma (pseudo-headers):**

```text
In-Reply-To: <CA+...@mail.gmail.com>
References: <prev...@mail> <CA+...@mail.gmail.com>
```

## Anti-Patterns

- **Gönder düğmesi varsayımı:** Taslak ID’sini logla; `SENT` doğrulanmadan arşivleme yok.
- **Yasal bağlayıcı dil:** "We guarantee" yazma; hukuki metin → insan + legal review.
- **BCC sızıntısı:** Taslakta BCC kullanma; gönderim öncesi alanları doğrula.
- **Kişisel hiciv / emoji aşırısı:** Kurumsal dış domain’de sınırlı emoji (0–1).

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [RFC 5322 — reply headers](https://www.rfc-editor.org/rfc/rfc5322) — In-Reply-To, References
- [Gmail API — Drafts](https://developers.google.com/gmail/api/guides/drafts) — taslak oluşturma
- [Microsoft Graph — createReply](https://learn.microsoft.com/en-us/graph/api/message-createreply) — Outlook taslak
