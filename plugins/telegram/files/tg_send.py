#!/usr/bin/env python3
"""Send Telegram message. Args: token chat_id text [markup_json]"""
import json, sys, urllib.request

token   = sys.argv[1]
chat_id = sys.argv[2]
text    = sys.argv[3]
markup  = sys.argv[4] if len(sys.argv) > 4 else ""

data = {"chat_id": chat_id, "parse_mode": "Markdown", "text": text}
if markup:
    try:
        data["reply_markup"] = json.loads(markup)
    except Exception:
        pass

req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"},
)
try:
    urllib.request.urlopen(req, timeout=10)
except Exception as e:
    print(f"send error: {e}", file=sys.stderr)
