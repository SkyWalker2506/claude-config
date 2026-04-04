#!/usr/bin/env python3
"""Parse Telegram getUpdates response → tab-separated lines for bash."""
import json, sys

auth_chat = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    raw = sys.stdin.buffer.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        data = json.loads(raw.decode("utf-8", errors="surrogateescape")
                         .encode("utf-16", "surrogatepass")
                         .decode("utf-16"))
except Exception:
    sys.exit(0)

for u in data.get("result", []):
    uid = u["update_id"]
    if "callback_query" in u:
        cq = u["callback_query"]
        if str(cq["message"]["chat"]["id"]) == auth_chat:
            print(f"CB\t{uid}\t{cq['id']}\t{cq['data']}")
    elif "message" in u:
        msg = u["message"]
        if str(msg.get("chat", {}).get("id", "")) == auth_chat:
            caption = msg.get("caption", "")
            if msg.get("text"):
                print(f"MSG\t{uid}\t{msg['text']}")
            elif msg.get("photo"):
                # En yüksek çözünürlüklü fotoğraf
                file_id = msg["photo"][-1]["file_id"]
                print(f"PHOTO\t{uid}\t{file_id}\t{caption}")
            elif msg.get("document"):
                doc = msg["document"]
                file_id = doc["file_id"]
                fname = doc.get("file_name", "document")
                print(f"DOC\t{uid}\t{file_id}\t{fname}|{caption}")
            elif msg.get("voice"):
                file_id = msg["voice"]["file_id"]
                print(f"VOICE\t{uid}\t{file_id}\t{caption}")
            elif msg.get("sticker"):
                emoji = msg["sticker"].get("emoji", "?")
                print(f"MSG\t{uid}\t{emoji}")
