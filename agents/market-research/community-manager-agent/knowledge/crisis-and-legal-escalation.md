---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Crisis, brigading, and legal escalation

## Quick Reference

| Olay | İlk 15 dk |
|------|-----------|
| **Koordineli spam / brigading** | Slowmode + mod kanalı + pin’li kural hatırlatması |
| **Dox / tehdit** | Mesaj sil, kullanıcı ban, güvenlik / hukuk |
| **Sahte resmi hesap** | Platform raporu + duyuru |
| **Yasal talep (DMCA, mahkeme)** | Kayıt sakla — yanıtı Legal |

H14 hukuk tavsiyesi vermez; **runbook + iletişim hattı** verir.

## Patterns & Decision Matrix

| Şiddet | Mod aksiyonu |
|--------|--------------|
| Küfür | Uyarı → mute |
| Taciz / hedef gösterme | Mute → ban |
| Suç unsuru | Ban + log export |

## Code Examples

**Discord slowmode (yönetici komutu):**

```
/slowmode duration:2m channel:#general reason:spam_wave_20260410
```

**Olay günlüğü (iç wiki şablonu):**

```markdown
## INC-2026-0410 — Brigading
- Detected: 10:02 UTC — 40 benzer mesaj / 3 dk
- Actions: slowmode 120s, 12 kullanıcı timeout 1h
- Comms: #announcements pin
- Owner: @mod-lead — Legal notified: no
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Tartışmayı mod kanalında halka sızdırmak | Kaos büyür |
| Ban without log | İtirazda savunma yok |
| Otomatik ban kelime listesi | Yanlış pozitif |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Discord — Community guidelines](https://discord.com/guidelines)
- [Slack — Acceptable use](https://slack.com/intl/en-tr/terms-of-service)
- [EFF — DMCA](https://www.eff.org/issues/intellectual-property/dmca) — bağlam
