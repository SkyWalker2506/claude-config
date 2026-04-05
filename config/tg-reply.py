#!/usr/bin/env python3
"""
tg-reply.py — Secrets'tan token/chat_id okuyarak Telegram'a mesaj gönderir.

Kullanım:
    python3 tg-reply.py "mesaj metni"

tg_send.py'nin secrets-aware wrapper'ı. Jarvis ve /telegram-watch tarafından kullanılır.
"""

import json, os, sys, urllib.request

def load_secrets():
    paths = [
        os.path.expanduser("~/Projects/claude-config/claude-secrets/secrets.env"),
        os.path.expanduser("~/.claude/secrets/secrets.env"),
    ]
    secrets = {}
    for p in paths:
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    secrets[k.strip()] = v.strip().strip('"').strip("'")
    return secrets

def tg_send(token, chat_id, text):
    MAX = 4000
    chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
    for chunk in chunks:
        data = json.dumps({
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown",
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"send error: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 tg-reply.py 'mesaj'", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    secrets = load_secrets()
    token = secrets.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = secrets.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        print("❌ TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID eksik", file=sys.stderr)
        sys.exit(1)

    tg_send(token, chat_id, text)
