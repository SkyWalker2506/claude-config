---
name: level-editor
description: "Level editor aç — yerel sunucu başlat (editor.html) veya Vercel online versiyonunu aç. Triggers: level editor, editör aç, editor open, online editor, vercel editor"
argument-hint: "[local|online]"
---

# /level-editor — Level Editor'ı Aç

Argümansız veya `local` → yerel sunucu başlatır ve tarayıcıda açar.  
`online` → Vercel'deki canlı versiyonu açar.

## Kullanım

```
/level-editor          # local (varsayılan)
/level-editor local    # local sunucu
/level-editor online   # Vercel canlı
```

## Çalıştır

```bash
ARG="${1:-local}"
EDITOR_PAGE="editor.html"
VERCEL_URL="https://golf-paper-craft.vercel.app/${EDITOR_PAGE}"
LOCAL_PORT=8000

if [ "$ARG" = "online" ]; then
  echo "Opening online editor: $VERCEL_URL"
  open "$VERCEL_URL"
else
  # Find project root — look for editor.html under www/
  if [ -f "www/${EDITOR_PAGE}" ]; then
    PROJECT_DIR="$(pwd)"
  elif [ -f "${HOME}/Projects/golf-paper-craft/www/${EDITOR_PAGE}" ]; then
    PROJECT_DIR="${HOME}/Projects/golf-paper-craft"
  else
    echo "ERROR: editor.html not found. Run from golf-paper-craft directory."
    exit 1
  fi

  # Start server if not already running
  if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
    echo "Server already running on port ${LOCAL_PORT}"
  else
    echo "Starting server at ${PROJECT_DIR}/www ..."
    python3 -m http.server ${LOCAL_PORT} --directory "${PROJECT_DIR}/www" &
    sleep 1
    echo "Server started."
  fi

  LOCAL_URL="http://localhost:${LOCAL_PORT}/${EDITOR_PAGE}"
  echo "Opening local editor: $LOCAL_URL"
  open "$LOCAL_URL"
fi
```
