#!/bin/bash
# telegram-check.sh — Inbox'ta pending mesaj var mı kontrol et
# Çıktı: pending varsa JSON objesi, yoksa boş
# Kullanım: pending=$(bash telegram-check.sh) && [ -n "$pending" ] && echo "$pending"

INBOX="$HOME/.watchdog/telegram-inbox.jsonl"
[ ! -f "$INBOX" ] && exit 0

pending=$(python3 - <<'PYEOF'
import json, sys, os

inbox = os.path.expanduser("~/.watchdog/telegram-inbox.jsonl")
try:
    lines = open(inbox).readlines()
except:
    sys.exit(0)

pending = []
for l in lines:
    l = l.strip()
    if not l:
        continue
    try:
        entry = json.loads(l)
        if entry.get("status") == "pending":
            pending.append(entry)
    except:
        pass

if pending:
    # En eski pending mesajı döndür (FIFO)
    print(json.dumps(pending[0], ensure_ascii=False))
PYEOF
)

echo "$pending"
