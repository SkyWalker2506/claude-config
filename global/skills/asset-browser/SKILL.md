---
name: asset-browser
description: "Asset browser aç veya güncelle — Vercel URL'i aç, local dev sunucusu başlat, veya paket kodunu güncelle + redeploy. Triggers: asset browser aç, asset browser open, browse assets, open browser, asset browser update, browser güncelle, update browser"
argument-hint: "[local|online|update]"
---

# /asset-browser — Asset Browser'ı Aç / Güncelle

| Argüman | Eylem |
|---------|-------|
| (yok) / `online` | Vercel canlı URL'i açar |
| `local` | Yerel dev sunucusu başlatır ve açar |
| `update` | Paketten kodu çeker, redeploy eder |

## Kullanım

```
/asset-browser          # online (varsayılan)
/asset-browser online   # Vercel canlı
/asset-browser local    # local dev sunucusu
/asset-browser update   # paket güncellemesi + redeploy
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
PKG_DIR="${HOME}/Projects/asset-browser"

# Vercel alias: title lowercase, non-alnum -> dash
TITLE=$(python3 -c "import json; c=json.load(open('${CONFIG}')); print(c['title'].lower())" 2>/dev/null)
SLUG=$(echo "$TITLE" | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
VERCEL_URL="https://asset-browser-${SLUG}.vercel.app"
LOCAL_PORT=3001

if [ "$ARG" = "update" ]; then
  # Paketi güncelle + redeploy
  echo "=== asset-browser update: $PROJECT_DIR ==="

  # 1. Paketi pull
  echo "Pulling latest package..."
  (cd "$PKG_DIR" && git pull --quiet) || echo "WARN: pkg pull failed, using local"

  # 2. Kod dosyalarını kopyala (config.json ve data/ korunur)
  echo "Copying code files..."
  cp "$PKG_DIR/api/"*.js  "$PROJECT_DIR/asset-browser/api/"
  cp "$PKG_DIR/public/index.html" "$PROJECT_DIR/asset-browser/public/"
  cp "$PKG_DIR/vercel.json" "$PROJECT_DIR/asset-browser/"
  cp "$PKG_DIR/package.json" "$PROJECT_DIR/asset-browser/"
  cp "$PKG_DIR/deploy.sh"   "$PROJECT_DIR/asset-browser/"
  chmod +x "$PROJECT_DIR/asset-browser/deploy.sh"
  [ -d "$PKG_DIR/scripts" ] && cp "$PKG_DIR/scripts/"*.mjs "$PROJECT_DIR/asset-browser/scripts/" 2>/dev/null || true

  # 3. npm install
  echo "Installing dependencies..."
  (cd "$PROJECT_DIR/asset-browser" && npm install --silent)

  # 4. Git commit
  echo "Committing..."
  (cd "$PROJECT_DIR" && \
    git add asset-browser/ && \
    git diff --cached --quiet || git commit -m "chore: sync asset-browser with latest package" && \
    git push)

  # 5. Redeploy
  echo "Deploying to Vercel..."
  (cd "$PROJECT_DIR/asset-browser" && bash deploy.sh)

  echo ""
  echo "Done! Live: $VERCEL_URL"

elif [ "$ARG" = "local" ]; then
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
