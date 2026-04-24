---
name: asset-browser
description: "Asset browser aç — mevcut projenin asset-browser Vercel URL'ini aç, veya local dev sunucusu başlat. Triggers: asset browser aç, asset browser open, browse assets, open browser"
argument-hint: "[local|online]"
---

# /asset-browser — Asset Browser'ı Aç

Argümansız veya `online` → Vercel canlı URL'i açar.  
`local` → yerel dev sunucusu başlatır ve tarayıcıda açar.

## Kullanım

```
/asset-browser          # online (varsayılan)
/asset-browser online   # Vercel canlı
/asset-browser local    # local dev sunucusu
```

## Çalıştır

```bash
ARG="${1:-online}"

# Proje tespiti — CWD veya bilinen projeler
if [ -f "asset-browser/config.json" ]; then
  PROJECT_DIR="$(pwd)"
elif [ -f "${HOME}/Projects/MedievalFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/MedievalFactory"
elif [ -f "${HOME}/Projects/GameFactory/asset-browser/config.json" ]; then
  PROJECT_DIR="${HOME}/Projects/GameFactory"
else
  echo "ERROR: asset-browser/config.json not found. Run from project directory."
  exit 1
fi

CONFIG="${PROJECT_DIR}/asset-browser/config.json"

# Vercel alias: title lowercase, non-alnum -> dash
TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
VERCEL_URL="https://asset-browser-${SLUG}.vercel.app"
LOCAL_PORT=3001

if [ "$ARG" = "local" ]; then
  # Local dev sunucusu
  if lsof -ti:${LOCAL_PORT} > /dev/null 2>&1; then
    echo "Dev server already running on port ${LOCAL_PORT}"
  else
    echo "Starting asset-browser dev server at ${PROJECT_DIR}/asset-browser ..."
    cd "${PROJECT_DIR}/asset-browser" && npm run dev -- --port ${LOCAL_PORT} &
    sleep 2
    echo "Server started."
  fi
  LOCAL_URL="http://localhost:${LOCAL_PORT}"
  echo "Opening local asset-browser: $LOCAL_URL"
  open "$LOCAL_URL"
else
  echo "Opening asset-browser: $VERCEL_URL"
  open "$VERCEL_URL"
fi
```
