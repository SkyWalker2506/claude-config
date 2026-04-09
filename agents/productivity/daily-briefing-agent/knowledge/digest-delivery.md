---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Digest Delivery

## Quick Reference

**Kanallar:** e-posta (HTML veya düz metin), Slack/Discord webhook, Telegram bot, yerel dosya (`~/Briefings/2026-04-09.md`). Her kanal için boyut sınırı farklı (ör. Telegram 4096 karakter).

| Kanal | Max uzunluk | Ek |
|-------|-------------|-----|
| Email | ~100 KB | Ekte ICS mümkün |
| Telegram | 4096 | Böl ve devam et |
| Dosya | Sınırsız | Git ile versiyon |

**Zamanlama:** `cron` / `launchd` 07:00 yerel; seyahat modunda TZ override.

```text
delivery: idempotent_key = user_id + date + channel + content_hash
```

## Patterns & Decision Matrix

| Strateji | Artı | Eksi |
|----------|------|------|
| Tek push sabah | Alışkanlık | Gece acil kaçar |
| İki aşama (önizleme + onay) | Güvenli | Sürtünme |
| Sessiz mod (dosya only) | Gizlilik | Bildirim yok |

**Retry:** 429/5xx → exponential backoff; max 3; sonra `FAILED` + kullanıcıya tek uyarı.

## Code Examples

**Webhook (Slack incoming):**

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"'"$(head -c 3500 briefing.md | jq -Rs .)"'"}' \
  "$SLACK_WEBHOOK_URL"
```

**launchd plist özeti (macOS — 07:00):**

```xml
<key>StartCalendarInterval</key>
<dict>
  <key>Hour</key><integer>7</integer>
  <key>Minute</key><integer>0</integer>
</dict>
```

**Teslim log satırı:**

```json
{"ts":"2026-04-09T07:00:05+03:00","channel":"telegram","status":"ok","bytes":2840,"idempotent_key":"u1-2026-04-09-tg"}
```

## Anti-Patterns

- **Aynı brifingi 5 kanala spam:** Varsayılan tek kanal; diğerleri opt-in.
- **Secrets’ı loga yazma:** Webhook URL’si maskele.
- **Kullanıcı uyurken titreşim:** `quiet_hours` saygısı.
- **HTML e-postada dev script:** Sadece düz metin veya sınırlı inline CSS.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Slack — incoming webhooks](https://api.slack.com/messaging/webhooks) — payload limitleri
- [Telegram Bot API — sendMessage](https://core.telegram.org/bots/api#sendmessage) — 4096 limit
- [RFC 5322 — email lines](https://www.rfc-editor.org/rfc/rfc5322) — satır uzunluğu (998)
