---
name: telegram-watch
description: "Telegram inbox'ı izle — yeni mesaj varsa Jarvis işlesin. Triggers: telegram izle, tg watch, telegram dinle, telegram inbox."
argument-hint: ""
---

# /telegram-watch

Telegram inbox'ını izle ve gelen mesajları Jarvis bağlamıyla işle.

## Nasıl çalışır

`telegram-agent.py` relay modunda çalışır: Telegram'dan gelen mesajları `~/.watchdog/telegram-inbox.jsonl` dosyasına yazar.
Bu skill o dosyayı periyodik olarak kontrol eder, `status: "pending"` mesajları işler, cevabı Telegram'a gönderir.

## Secrets

Secrets dosyasından token ve chat_id oku:
$(python3 -c "
import os
paths = [os.path.expanduser('~/Projects/claude-config/claude-secrets/secrets.env'), os.path.expanduser('~/.claude/secrets/secrets.env')]
for p in paths:
    if os.path.exists(p):
        for l in open(p):
            l = l.strip()
            if l.startswith('TELEGRAM_BOT_TOKEN=') or l.startswith('TELEGRAM_CHAT_ID='):
                k, v = l.split('=', 1)
                print(f'{k}=<set>' if v.strip().strip('\"').strip(\"'\") else f'{k}=MISSING')
        break
" 2>/dev/null || echo "Secrets okunamadı")

## Akış

1. `~/.watchdog/telegram-inbox.jsonl` dosyasını oku
2. `status: "pending"` olan mesajları bul (FIFO — en eskiden başla)
3. Her mesaj için:
   a. Mesaj metnini oku, Jarvis bağlamıyla değerlendir
   b. Gerekirse agent dispatch et (A2 → uygun agent)
   c. Cevabı oluştur
   d. Cevabı Telegram'a gönder:
      ```bash
      python3 ~/Projects/claude-config/config/tg-reply.py "<cevap>"
      ```
   e. Mesajın status'unu "done" olarak güncelle:
      ```bash
      python3 ~/Projects/claude-config/config/telegram-inbox-update.py <message_id> done
      ```
4. 10 saniye bekle, tekrarla (veya `/loop 10s /telegram-watch` ile çalıştır)

## Cevap formatı

- Kısa cevap (<3500 karakter): direkt metin
- Uzun cevap: özet + "Detaylar için Claude Code session'ına bak" notu
- Hata: `❌ [hata mesajı]`
- Başarı: `✅ [özet]`

## Önemli notlar

- `telegram-agent.py`'nin çalışıyor olması gerekir (relay modu)
- Inbox dosyası: `~/.watchdog/telegram-inbox.jsonl`
- Her mesajı işledikten sonra status'u "done" yap — tekrar işleme
- Jarvis bağlamı: tüm kurallar, agent dispatch, memory geçerli
