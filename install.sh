#!/bin/bash
set -euo pipefail

# claude-config installer — cross-platform (macOS + Windows/Git Bash)
# Usage:
#   ./install.sh                    # interactive (asks questions)
#   ./install.sh --auto             # non-interactive (defaults, no prompts)
#   ./install.sh --auto --root ~/Dev  # non-interactive with custom root

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SECRETS_DIR="$HOME/.claude/secrets"

OWNER_GITHUB="SkyWalker2506"
OWNER_SECRETS_REPO="https://github.com/SkyWalker2506/claude-secrets.git"

# ── Platform detection ──
OS="unknown"
case "$(uname -s)" in
  Darwin*)  OS="mac" ;;
  Linux*)   OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
esac

# Windows-specific: fix common PATH issues
if [ "$OS" = "windows" ]; then
  # Add common Windows tool paths if missing
  for p in "/c/Program Files/GitHub CLI" "/c/Program Files/Git/bin" "$LOCALAPPDATA/Programs/Python/Python3"*; do
    [ -d "$p" ] && case ":$PATH:" in *":$p:"*) ;; *) export PATH="$PATH:$p" ;; esac
  done
fi

# ── Argument parsing ──
AUTO=0
CUSTOM_ROOT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --auto|-y) AUTO=1; shift ;;
    --root) CUSTOM_ROOT="$2"; shift 2 ;;
    --root=*) CUSTOM_ROOT="${1#*=}"; shift ;;
    *) shift ;;
  esac
done

# Helper: prompt or use default in auto mode
ask() {
  local prompt="$1" default="$2" varname="$3"
  if [ "$AUTO" -eq 1 ]; then
    eval "$varname=\"$default\""
  else
    read -p "$prompt [$default]: " _answer 2>/dev/null || _answer=""
    eval "$varname=\"\${_answer:-$default}\""
  fi
}

confirm() {
  local prompt="$1" default="${2:-E}"
  if [ "$AUTO" -eq 1 ]; then
    return 0  # auto mode = yes to all
  fi
  local answer=""
  read -p "$prompt [${default}]: " answer 2>/dev/null || answer=""
  answer="${answer:-$default}"
  [[ "$answer" =~ ^[EeYy]$ ]]
}

echo "=== Claude Code Config Installer ==="
[ "$AUTO" -eq 1 ] && echo "Mode: auto (non-interactive)"
echo "Platform: $OS"
echo ""

# ── 1. Projects root ──
if [ -n "$CUSTOM_ROOT" ]; then
  PROJECTS_ROOT="$CUSTOM_ROOT"
else
  DEFAULT_ROOT="$HOME/Projects"
  [ "$OS" = "windows" ] && DEFAULT_ROOT="$HOME/Documents/GitHub"
  ask "Proje kok dizini" "$DEFAULT_ROOT" PROJECTS_ROOT
fi
PROJECTS_ROOT="${PROJECTS_ROOT/#\~/$HOME}"

if [ ! -d "$PROJECTS_ROOT" ]; then
  echo "Dizin yok, olusturuluyor: $PROJECTS_ROOT"
  mkdir -p "$PROJECTS_ROOT"
fi

# ── 2. uvx path ──
UVX_PATH=$(which uvx 2>/dev/null || echo "")
if [ -z "$UVX_PATH" ]; then
  echo "⚠️  uvx bulunamadi. jCodeMunch MCP calismayacak."
  if [ "$OS" = "windows" ]; then
    echo "   Kurmak icin: pip install pipx && pipx install uvx"
  else
    echo "   Kurmak icin: pip3 install pipx && pipx install uvx"
  fi
  UVX_PATH="uvx"
fi
echo "uvx: $UVX_PATH"

# ── 3. GitHub Login ──
echo ""
echo "=== GitHub Login ==="

CURRENT_USER=""
if command -v gh &>/dev/null; then
  CURRENT_USER=$(gh api user -q .login 2>/dev/null || echo "")
fi

if [ -z "$CURRENT_USER" ]; then
  if ! command -v gh &>/dev/null; then
    echo "⚠️  GitHub CLI (gh) bulunamadi."
    if [ "$OS" = "windows" ]; then
      echo "   Kur: winget install GitHub.cli"
    else
      echo "   Kur: brew install gh"
    fi
    echo "   Login ve secrets atlaniyor."
  elif confirm "GitHub'a giris yapilmamis. Simdi giris yapmak ister misin?"; then
    gh auth login --web -p https || true
    CURRENT_USER=$(gh api user -q .login 2>/dev/null || echo "")
    if [ -n "$CURRENT_USER" ]; then
      echo "✅ GitHub: $CURRENT_USER"
      gh auth setup-git 2>/dev/null || true
    else
      echo "⚠️  Login basarisiz."
    fi
  fi
else
  echo "✅ GitHub: $CURRENT_USER"
fi

# ── 4. Secrets ──
echo ""
echo "=== Secrets ==="

IS_OWNER=0
[ "$CURRENT_USER" = "$OWNER_GITHUB" ] && IS_OWNER=1

if [ -d "$SECRETS_DIR/.git" ]; then
  echo "✅ Secrets reposu mevcut"
  git -C "$SECRETS_DIR" pull --quiet 2>/dev/null && echo "   Guncellendi." || echo "   ⚠️ Pull basarisiz, mevcut kullanilacak."

elif [ -f "$SECRETS_DIR/secrets.env" ]; then
  echo "✅ Lokal secrets.env mevcut"

elif [ -n "$CURRENT_USER" ]; then
  if confirm "Secrets reposunu indirmek ister misin?"; then
    if [ "$IS_OWNER" -eq 1 ]; then
      echo "Private secrets clone ediliyor..."
      git clone --quiet "$OWNER_SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null && echo "✅ Secrets yuklendi" || { echo "❌ Clone basarisiz."; mkdir -p "$SECRETS_DIR"; }
    else
      ask "Private secrets repo URL'niz" "" SECRETS_REPO
      if [ -n "$SECRETS_REPO" ]; then
        git clone --quiet "$SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null && echo "✅ Secrets yuklendi" || { echo "❌ Clone basarisiz."; mkdir -p "$SECRETS_DIR"; }
      else
        mkdir -p "$SECRETS_DIR"
      fi
    fi
  else
    echo "Atlandi. /download-secrets ile sonra indirebilirsin."
    mkdir -p "$SECRETS_DIR"
  fi
else
  echo "Login yok, secrets atlandi. /admin-login + /download-secrets ile kurabilirsin."
  mkdir -p "$SECRETS_DIR"
fi

# Source secrets
SECRETS_ENV="$SECRETS_DIR/secrets.env"
if [ -f "$SECRETS_ENV" ]; then
  set -a
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*= ]] && eval "export $line" 2>/dev/null || true
  done < "$SECRETS_ENV"
  set +a
fi

# ── 5. Backup ──
if [ -d "$HOME/.claude" ]; then
  BACKUP="$HOME/.claude.backup.$TIMESTAMP"
  echo ""
  echo "Yedek: $BACKUP"
  if command -v rsync &>/dev/null; then
    rsync -a --exclude='secrets/' "$HOME/.claude/" "$BACKUP/"
  else
    # Windows: rsync yok, cp kullan
    mkdir -p "$BACKUP"
    cp -r "$HOME/.claude/"* "$BACKUP/" 2>/dev/null || true
    rm -rf "$BACKUP/secrets" 2>/dev/null || true
  fi
fi

# ── 6. Copy files ──
echo ""
echo "Dosyalar kopyalaniyor..."
mkdir -p "$HOME/.claude/skills"
mkdir -p "$PROJECTS_ROOT/scripts"
mkdir -p "$PROJECTS_ROOT/.watchdog"

# Watchdog temp dir — platform aware
if [ "$OS" = "windows" ]; then
  WATCHDOG_TMP="${TEMP:-/tmp}/watchdog"
else
  WATCHDOG_TMP="/tmp/watchdog"
fi
mkdir -p "$WATCHDOG_TMP"

# Global CLAUDE.md
cp "$SCRIPT_DIR/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md"

# Skills
for skill_dir in "$SCRIPT_DIR/global/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$HOME/.claude/skills/$skill_name"
  cp -r "$skill_dir"* "$HOME/.claude/skills/$skill_name/" 2>/dev/null || true
done

# settings.json — template with path substitution
sed \
  -e "s|__UVX_PATH__|$UVX_PATH|g" \
  -e "s|__PROJECTS_ROOT__|$PROJECTS_ROOT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$SCRIPT_DIR/global/settings.json.template" > "$HOME/.claude/settings.json"

# MCP servers
echo "MCP sunuculari ekleniyor..."
GITHUB_TOKEN_VAL="${GITHUB_TOKEN:-}"
FIREBASE_SA_VAL="${FIREBASE_SERVICE_ACCOUNT_PATH:-}"

claude mcp add -s user github -e "GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN_VAL" -- npx -y @modelcontextprotocol/server-github 2>/dev/null && echo "  ✅ github" || echo "  ⚠️ github eklenemedi"
claude mcp add -s user git -- "$UVX_PATH" mcp-server-git 2>/dev/null && echo "  ✅ git" || echo "  ⚠️ git eklenemedi"
claude mcp add -s user atlassian -- npx -y mcp-remote@latest https://mcp.atlassian.com/v1/mcp 2>/dev/null && echo "  ✅ atlassian" || echo "  ⚠️ atlassian eklenemedi"
claude mcp add -s user flutter-dev -- npx -y flutter-dev-mcp 2>/dev/null && echo "  ✅ flutter-dev" || echo "  ⚠️ flutter-dev eklenemedi"
if [ -n "$FIREBASE_SA_VAL" ]; then
  claude mcp add -s user firebase -e "SERVICE_ACCOUNT_KEY_PATH=$FIREBASE_SA_VAL" -- npx -y @gannonh/firebase-mcp 2>/dev/null && echo "  ✅ firebase" || echo "  ⚠️ firebase eklenemedi"
fi
claude mcp add -s user context7 -- npx -y @upstash/context7-mcp 2>/dev/null && echo "  ✅ context7" || echo "  ⚠️ context7 eklenemedi"
claude mcp add -s user jcodemunch -- "$UVX_PATH" jcodemunch-mcp 2>/dev/null && echo "  ✅ jcodemunch" || echo "  ⚠️ jcodemunch eklenemedi"
claude mcp add -s user fetch -- npx -y mcp-fetch-server 2>/dev/null && echo "  ✅ fetch" || echo "  ⚠️ fetch eklenemedi"

# Projects files
cp "$SCRIPT_DIR/projects/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_GUIDE.md" "$PROJECTS_ROOT/MIGRATION_GUIDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_VERSION" "$PROJECTS_ROOT/MIGRATION_VERSION"
cp "$SCRIPT_DIR/projects/PROJECT_ANALYSIS.md" "$PROJECTS_ROOT/PROJECT_ANALYSIS.md"

cp "$SCRIPT_DIR/projects/scripts/migration_check.sh" "$PROJECTS_ROOT/scripts/migration_check.sh"
chmod +x "$PROJECTS_ROOT/scripts/migration_check.sh" 2>/dev/null || true

cp "$SCRIPT_DIR/projects/scripts/ralph.sh" "$PROJECTS_ROOT/scripts/ralph.sh"
cp "$SCRIPT_DIR/projects/scripts/ralph-prompt.md" "$PROJECTS_ROOT/scripts/ralph-prompt.md"
chmod +x "$PROJECTS_ROOT/scripts/ralph.sh" 2>/dev/null || true

# Templates
mkdir -p "$PROJECTS_ROOT/.claude-templates"
cp "$SCRIPT_DIR/templates/"* "$PROJECTS_ROOT/.claude-templates/" 2>/dev/null || true

# ── 7. Validation ──
echo ""
echo "=== Dogrulama ==="
ERRORS=0

# JSON parse — try python3 first, fall back to python, then node
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
  PYTHON_CMD="python"
fi

if [ -n "$PYTHON_CMD" ]; then
  if $PYTHON_CMD -c "import json; json.load(open('$HOME/.claude/settings.json'))" 2>/dev/null; then
    echo "✅ settings.json gecerli"
  else
    echo "❌ settings.json JSON hatali!"
    ERRORS=$((ERRORS + 1))
  fi
elif command -v node &>/dev/null; then
  if node -e "JSON.parse(require('fs').readFileSync('$HOME/.claude/settings.json','utf8'))" 2>/dev/null; then
    echo "✅ settings.json gecerli"
  else
    echo "❌ settings.json JSON hatali!"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "⚠️  JSON dogrulama atlandi (python/node bulunamadi)"
fi

# File existence
for f in "$HOME/.claude/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md" "$PROJECTS_ROOT/scripts/migration_check.sh" "$PROJECTS_ROOT/MIGRATION_VERSION"; do
  if [ -f "$f" ]; then
    echo "✅ $(basename "$f") mevcut"
  else
    echo "❌ $f bulunamadi!"
    ERRORS=$((ERRORS + 1))
  fi
done

SKILL_COUNT=$(ls -d "$HOME/.claude/skills"/*/ 2>/dev/null | wc -l | tr -d ' ')
echo "✅ $SKILL_COUNT skill yuklendi"

# Secrets check
echo ""
echo "=== Secrets ==="
GITHUB_TOKEN_VAL="${GITHUB_TOKEN:-}"
if [ -n "$GITHUB_TOKEN_VAL" ]; then
  echo "✅ GITHUB_TOKEN ayarli"
else
  echo "⚪ GITHUB_TOKEN ayarlanmamis"
fi

# ── 8. Done ──
echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "=== Kurulum basarili! ==="
else
  echo "=== $ERRORS hata tespit edildi. ==="
fi
echo ""
echo "Kullanim:"
echo "  cd $PROJECTS_ROOT/HerhangiBirProje && claude"
[ -n "${BACKUP:-}" ] && echo "Yedek: $BACKUP"
