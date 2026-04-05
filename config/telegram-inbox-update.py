#!/usr/bin/env python3
"""
telegram-inbox-update.py — Inbox'taki bir mesajın status'unu güncelle.

Kullanım:
    python3 telegram-inbox-update.py <message_id> <new_status>

Örnek:
    python3 telegram-inbox-update.py 12345 done
"""

import json, os, sys

def main():
    if len(sys.argv) < 3:
        print("Kullanım: python3 telegram-inbox-update.py <message_id> <status>", file=sys.stderr)
        sys.exit(1)

    message_id = int(sys.argv[1])
    new_status = sys.argv[2]
    inbox_file = os.path.expanduser("~/.watchdog/telegram-inbox.jsonl")

    if not os.path.exists(inbox_file):
        print(f"Inbox bulunamadı: {inbox_file}", file=sys.stderr)
        sys.exit(1)

    lines = open(inbox_file).readlines()
    updated = []
    found = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            if entry.get("id") == message_id:
                entry["status"] = new_status
                found = True
        except:
            pass
        updated.append(json.dumps(entry, ensure_ascii=False))

    if not found:
        print(f"Message ID bulunamadı: {message_id}", file=sys.stderr)
        sys.exit(1)

    with open(inbox_file, "w") as f:
        f.write("\n".join(updated) + "\n")

    print(f"✓ message_id={message_id} → {new_status}")

if __name__ == "__main__":
    main()
