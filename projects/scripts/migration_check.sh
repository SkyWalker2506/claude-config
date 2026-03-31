#!/bin/bash
# migration_check.sh — Proje migration + MCP sağlık kontrolü
# Hook: UserPromptSubmit — her mesajda çalışır, max 1 sn
# Çıktı yalnızca aksiyon gerektiğinde üretilir; güncel projede sessiz kalır.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECTS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

MASTER_FILE="$PROJECTS_ROOT/MIGRATION_VERSION"
PROJECT_VERSION_FILE="$(pwd)/.claude/migration_version"
PROJECT_SETTINGS="$(pwd)/.claude/settings.json"
GLOBAL_SETTINGS="$HOME/.claude/settings.json"

# ── Kapsam kontrolü ──
CWD_LOWER=$(echo "$(pwd)" | tr '[:upper:]' '[:lower:]')
PROJECTS_LOWER=$(echo "$PROJECTS_ROOT" | tr '[:upper:]' '[:lower:]')
case "$CWD_LOWER" in
  "${PROJECTS_LOWER}/"*) ;;
  *) exit 0 ;;
esac
case "$CWD_LOWER" in
  "${PROJECTS_LOWER}"|"${PROJECTS_LOWER}/") exit 0 ;;
esac

# claude-config yonetici reposu → migration/index/mcp kontrolu atla
if [ -f "$(pwd)/install.sh" ] && [ -f "$(pwd)/global/CLAUDE.md" ]; then
  # Sadece secrets kontrolu yap, gerisi atla
  SECRETS_ENV="$HOME/.claude/secrets/secrets.env"
  SECRETS_GIT="$HOME/.claude/secrets/.git"
  if [ -f "$SECRETS_ENV" ]; then
    MISSING_SECRETS=""
    for var in GITHUB_TOKEN JIRA_URL JIRA_USERNAME JIRA_API_TOKEN; do
      val=$(grep "^${var}=" "$SECRETS_ENV" 2>/dev/null | head -1 | cut -d'=' -f2-)
      if [ -z "$val" ]; then
        MISSING_SECRETS="$MISSING_SECRETS $var"
      fi
    done
    if [ -n "$MISSING_SECRETS" ]; then
      echo "🔑 SECRETS_MISSING: Eksik zorunlu secrets:$MISSING_SECRETS"
      echo "   Duzelt: nano $HOME/.claude/secrets/secrets.env"
      if [ -d "$SECRETS_GIT" ]; then
        echo "   Sonra: cd ~/.claude/secrets && git add -A && git commit -m 'update' && git push"
      fi
    fi
  fi
  # MCP kurulum kontrolu
  MCP_COUNT=$(claude mcp list 2>/dev/null | grep -c "✓ Connected" || echo 0)
  if [ "$MCP_COUNT" -lt 3 ]; then
    echo "⚠️  MCP_SETUP_NEEDED: Sadece $MCP_COUNT MCP bagli. install.sh calistirip oturumu yeniden baslatin."
  fi
  exit 0
fi

# ── 0. install.sh kurulum kontrolü ──
# claude mcp list hizli degil, sadece dosya varligina bak
if [ ! -f "$HOME/.claude/CLAUDE.md" ] || [ ! -f "$PROJECTS_ROOT/MIGRATION_VERSION" ]; then
  echo "🚨 INSTALL_NEEDED: claude-config kurulumu yapilmamis veya eksik."
  echo "   cd ~/Projects/claude-config && ./install.sh calistirin, sonra oturumu yeniden baslatin."
fi

# ── 1. Versiyon kontrolü ──
MASTER_VERSION=$(cat "$MASTER_FILE" 2>/dev/null | tr -d '[:space:]')
PROJECT_VERSION=$(cat "$PROJECT_VERSION_FILE" 2>/dev/null | tr -d '[:space:]')

if [ -n "$MASTER_VERSION" ]; then
  if [ -z "$PROJECT_VERSION" ]; then
    echo "⚠️  MIGRATION_NEEDED: Bu proje henüz kurulmamış."
    echo "   Master versiyon: $MASTER_VERSION"
    echo "   Aksiyon: /migration komutu çalıştır veya $PROJECTS_ROOT/MIGRATION_GUIDE.md oku."
  elif [ "$PROJECT_VERSION" != "$MASTER_VERSION" ]; then
    echo "🔄 MIGRATION_UPDATE: Proje ($PROJECT_VERSION) → Master ($MASTER_VERSION)"
    echo "   Aksiyon: /migration komutu çalıştır."
  fi
fi

# ── 2. MCP çakışma kontrolü (hızlı — sadece dosya varlığı) ──
GLOBAL_MCP="$HOME/.claude/mcp.json"
PROJECT_MCP="$(pwd)/.mcp.json"

# mcp.json varsa ve settings.json'da da aynı MCP tanımlıysa → çakışma riski
if [ -f "$GLOBAL_MCP" ] && [ -f "$GLOBAL_SETTINGS" ]; then
  # Her iki dosyada da "atlassian" var mı?
  GLOBAL_MCP_HAS=$(grep -c '"atlassian"' "$GLOBAL_MCP" 2>/dev/null || echo 0)
  SETTINGS_HAS=$(grep -c '"atlassian"' "$GLOBAL_SETTINGS" 2>/dev/null || echo 0)
  if [ "$GLOBAL_MCP_HAS" -gt 0 ] && [ "$SETTINGS_HAS" -gt 0 ]; then
    echo "⚠️  MCP_CONFLICT: 'atlassian' hem ~/.claude/mcp.json hem ~/.claude/settings.json'da tanımlı."
    echo "   Bu çakışma MCP'nin çalışmamasına yol açabilir. /migration fix ile düzelt."
  fi
fi

# ── 3. Temel dosya kontrolü (yeni proje için) ──
if [ ! -f "$(pwd)/CLAUDE.md" ] && [ -z "$PROJECT_VERSION" ]; then
  echo "📋 SETUP_HINT: CLAUDE.md bulunamadı. /migration setup ile proje kur."
fi

# ── 4. Watchdog stale detection ──
if [ -d "/tmp/watchdog" ]; then
  NOW=$(date +%s)
  for wf in /tmp/watchdog/*.json; do
    [ -f "$wf" ] || continue
    MTIME=$(stat -f %m "$wf" 2>/dev/null || stat -c %Y "$wf" 2>/dev/null || echo "$NOW")
    AGE=$(( NOW - MTIME ))
    if [ "$AGE" -gt 900 ]; then
      WTASK=$(python3 -c "import json;print(json.load(open('$wf')).get('task','?'))" 2>/dev/null || echo "?")
      MINS=$(( AGE / 60 ))
      echo "⚠️  WATCHDOG_STALE: '$WTASK' son ${MINS}dk dir guncellenmedi. Arka plan agent takilmis olabilir."
      echo "   Dosya: $wf"
    fi
  done
fi

# ── 5. jCodeMunch index kontrolü ──
INDEX_MARKER="$(pwd)/.claude/jcodemunch_indexed"
if [ -f "$INDEX_MARKER" ]; then
  # Marker var — bu session'da zaten sinyal verildiyse tekrarlama
  MARKER_AGE=0
  MARKER_MTIME=$(stat -f %m "$INDEX_MARKER" 2>/dev/null || stat -c %Y "$INDEX_MARKER" 2>/dev/null || echo 0)
  if [ "$MARKER_MTIME" -gt 0 ]; then
    MARKER_AGE=$(( $(date +%s) - MARKER_MTIME ))
  fi
  # 5dk'dan eski ise guncelleme sinyali ver (session basi bir kez)
  if [ "$MARKER_AGE" -gt 300 ]; then
    echo "🔍 INDEX_UPDATE: jCodeMunch index guncelleme zamani."
  fi
else
  # Hic indexlenmemis — kullaniciya sor
  echo "🔍 INDEX_ASK: Bu klasorde jCodeMunch indexleme yapilmamis. Indexleyeyim mi?"
fi

# ── 6. enabledMcpjsonServers kontrolü ──
if [ -f "$PROJECT_SETTINGS" ]; then
  HAS_ENABLED=$(grep -c "enabledMcpjsonServers" "$PROJECT_SETTINGS" 2>/dev/null || echo 0)
  if [ "$HAS_ENABLED" -eq 0 ]; then
    echo "⚠️  MCP_NOT_ENABLED: .claude/settings.json'da enabledMcpjsonServers tanımlı değil."
    echo "   MCP sunucuları bu projede aktif olmayabilir. /migration fix ile düzelt."
  fi
fi

# ── 7. Secrets kontrolü ──
SECRETS_ENV="$HOME/.claude/secrets/secrets.env"
SECRETS_GIT="$HOME/.claude/secrets/.git"
if [ -f "$SECRETS_ENV" ]; then
  MISSING_SECRETS=""
  for var in GITHUB_TOKEN JIRA_URL JIRA_USERNAME JIRA_API_TOKEN; do
    val=$(grep "^${var}=" "$SECRETS_ENV" 2>/dev/null | head -1 | cut -d'=' -f2-)
    if [ -z "$val" ]; then
      MISSING_SECRETS="$MISSING_SECRETS $var"
    fi
  done
  if [ -n "$MISSING_SECRETS" ]; then
    echo "🔑 SECRETS_MISSING: Eksik zorunlu secrets:$MISSING_SECRETS"
    echo "   Duzelt: nano $HOME/.claude/secrets/secrets.env"
    if [ -d "$SECRETS_GIT" ]; then
      echo "   Sonra: cd ~/.claude/secrets && git add -A && git commit -m 'update' && git push"
    fi
  fi
else
  echo "🔑 SECRETS_NONE: Secrets dosyasi bulunamadi."
  echo "   MCP servisleri (GitHub, Jira) calismayabilir."
  echo "   Kurmak icin: cd ~/Projects/claude-config && ./install.sh"
fi
