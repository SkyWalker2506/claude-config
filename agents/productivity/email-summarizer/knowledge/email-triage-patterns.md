---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Email Triage Patterns

## Quick Reference

| Pattern | Ne zaman | Araç / sinyal |
|---------|----------|---------------|
| **Inbox Zero batch** | Günde 2–3 blok | Son gelen önce; 2 dk üstü mail → ertesi güne |
| **2-minute rule** | Tek cevap yeter | Hemen yanıtla veya şablonla kapat |
| **Folder + label hybrid** | Gmail / Outlook | `INBOX` sadece okunmamış; proje için `Label` + `Important` |
| **S/MIME / phishing** | Dış domain | SPF/DKIM başarısız → karantina; `reply-to` ≠ `from` → şüphe |

```text
Triage sırası: (1) Kime geldi (To/CC) → (2) Konu satırı + snippet → (3) Ek boyutu / içerik tipi
```

## Patterns & Decision Matrix

| Yaklaşım | Artı | Eksi | Kullan |
|----------|------|------|--------|
| Sadece yıldız / önemli işareti | Hızlı | Ölçeklenmez, arama zayıf | Kişisel düşük hacim |
| Kurallar (filters) | Otomatik | Yanlış pozitif | Tekrarlayen gönderenler |
| Kategori + SLA | Ölçülebilir | Kurulum maliyeti | Ekip gelen kutusu |
| AI özet + insan onayı | Tutarlı öncelik | Model hatası riski | L1 agent varsayılanı |

**Karar:** Tekrarlayen newsletter → kural ile `Updates/`; tek seferlik VIP → `Important` + özet üst sıra.

## Code Examples

**Gmail API: son 24 saat, okunmamış, max 50 (pseudo — gerçek çağrı yapısına uygun):**

```http
GET https://gmail.googleapis.com/gmail/v1/users/me/messages
  ?q=is:unread newer_than:1d
  &maxResults=50
Authorization: Bearer <access_token>
```

**Basit triage çıktısı (agent çıktı şablonu):**

```text
[TRIAGE] 2026-04-09 08:00 UTC | window=24h | count=12
P0 (2): id=18a..., id=19b... — reason=exec-domain + unreplied>48h
P1 (4): ...
P2 (6): ...
SKIP: newsletters (3) — rule=newsletter-senders.list
```

**Outlook Graph (Microsoft 365) filtre örneği:**

```http
GET https://graph.microsoft.com/v1.0/me/messages
  ?$filter=isRead eq false and receivedDateTime ge 2026-04-08T00:00:00Z
  &$orderby=receivedDateTime desc
  &$top=50
```

## Anti-Patterns

- **Tümünü önemli saymak:** Her mail P0 olursa öncelik çöker; en fazla 3 P0/gün kuralı kullan.
- **Kural yazmadan AI’ya güvenmek:** Önce gönderen domain whitelist/blacklist, sonra özet.
- **Thread’i parçalamak:** `Message-ID` / `threadId` ile tek blokta tut; aksi halde aksiyon iki kez atanır.
- **Hassas içeriği loglamak:** Özetde PII maskele (`user@domain.com` → `u***@domain.com`).

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Gmail API — Messages](https://developers.google.com/gmail/api/guides) — listeleme, `q` sözdizimi, batch
- [Microsoft Graph — mail resources](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview) — filtre, delta query
- [RFC 5322 — Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322) — başlık alanları, thread anlamı
