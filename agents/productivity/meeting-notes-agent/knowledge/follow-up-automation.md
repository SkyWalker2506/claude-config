---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Follow-Up Automation

## Quick Reference

**Tetikleyiciler:** toplantı bitişi +24h e-posta özeti; due tarihinden -1 gün hatırlatma; blokaj >48h escalasyon. **Kanallar:** L1 taslak e-posta, Slack ping, Jira yorum.

| Otomasyon | İnsan onayı |
|-------------|-------------|
| Özet gönder | Önerilir (ilk hafta) |
| Jira yorum | Opsiyonel |
| Toplantı serisi oluştur | Zorunlu |

```text
idempotency: aynı toplantı için tek "summary sent" bayrağı
```

## Patterns & Decision Matrix

| Akış | Artı | Eksi |
|------|------|------|
| Zapier / Make | Hızlı kurulum | Maliyet + vendor |
| Custom script | Tam kontrol | Bakım |
| Sadece L6 çıktısı | Basit | Gerçek gönderim yok |

**L1 köprüsü:** Follow-up e-postası taslağı L1 şablonlarıyla uyumlu.

## Code Examples

**E-posta özeti gövdesi (metin):**

```text
Subject: [Follow-up] API sunset decision — 2026-04-10

Hi team,

Summary:
- We approved v1 sunset on 2026-09-01 (owner: Bob)
- Carol will send customer comms by 2026-04-20

Open actions:
1. Alice — error metrics by 2026-04-15
2. Carol — comms draft by 2026-04-20

Notes: https://wiki.company.com/x/abc
```

**HTTP webhook (Slack):**

```bash
curl -X POST -H 'Content-type: application/json' \
  -d '{"text":"Reminder: A-20260410-01 due tomorrow — @alice"}' \
  "$SLACK_WEBHOOK_URL"
```

**Durum makinesi (pseudo):**

```text
meeting_ended -> summary_draft -> [user_approve] -> sent -> track_actions
action_due_soon -> reminder -> done | escalate_to_manager
```

## Anti-Patterns

- **Herkesi CC ile spam:** Sadece DACI listesi ve aksiyon sahipleri.
- **Otomatik Jira oluşturma çoğaltması:** Önce duplicate arama (I8).
- **Gizli kararları dışarı sızdırma:** Özet önce iç dağıtım.
- **Hatırlatma saati TZ’siz:** Her alıcı için yerel iş saati.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Zapier — multi-step Zaps](https://zapier.com/) — otomasyon desenleri
- [Jira REST — add comment](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/) — API
- [RFC 5545 — VALARM](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.6) — takvim uyarıları
