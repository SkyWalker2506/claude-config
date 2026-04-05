#!/bin/bash
set -euo pipefail

# claude-config installer — cross-platform (macOS + Windows/Git Bash)
# Usage:
#   ./install.sh                    # interactive (asks questions)
#   ./install.sh --auto             # non-interactive (defaults, no prompts)
#   ./install.sh --auto --root ~/Dev  # non-interactive with custom root
#   ./install.sh --opencode              # also: npm install -g opencode-ai
#   ./install.sh --refresh-opencode-config  # overwrite ~/.config/opencode/opencode.json from template (backup .bak.*)

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
# --auto: skip all interactive prompts
# --root PATH: projects root directory
# --skip-login: skip GitHub login step
# --skip-secrets: skip secrets step
# --secrets-repo URL: clone this secrets repo
# --stacks LIST: comma-separated project stacks (flutter,firebase,unity,web,python)
# --opencode: install OpenCode CLI globally via npm: opencode-ai
# --refresh-opencode-config: reset opencode.json to repo template (Zen + Ollama)
AUTO=0
CUSTOM_ROOT=""
SKIP_LOGIN=0
SKIP_SECRETS=0
SECRETS_REPO_URL=""
STACKS=""
WITH_OPENCODE=0
REFRESH_OPENCODE_CONFIG=0
WITH_LOCAL_MODELS=0
SKIP_LOCAL_MODELS=0
WITH_AGENTS=1
SKIP_AGENTS=0
SKIP_CRON=0
ONLY_AGENTS=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --auto|-y) AUTO=1; shift ;;
    --root) CUSTOM_ROOT="$2"; shift 2 ;;
    --root=*) CUSTOM_ROOT="${1#*=}"; shift ;;
    --skip-login) SKIP_LOGIN=1; shift ;;
    --skip-secrets) SKIP_SECRETS=1; shift ;;
    --secrets-repo) SECRETS_REPO_URL="$2"; shift 2 ;;
    --secrets-repo=*) SECRETS_REPO_URL="${1#*=}"; shift ;;
    --stacks) STACKS="$2"; shift 2 ;;
    --stacks=*) STACKS="${1#*=}"; shift ;;
    --opencode) WITH_OPENCODE=1; shift ;;
    --refresh-opencode-config) REFRESH_OPENCODE_CONFIG=1; shift ;;
    --with-local-models) WITH_LOCAL_MODELS=1; shift ;;
    --skip-local-models) SKIP_LOCAL_MODELS=1; shift ;;
    --skip-agents) SKIP_AGENTS=1; WITH_AGENTS=0; shift ;;
    --skip-cron) SKIP_CRON=1; shift ;;
    --only-agents) ONLY_AGENTS=1; shift ;;
    *) shift ;;
  esac
done

# Helper: check if a stack is in the STACKS list
has_stack() {
  [[ ",$STACKS," == *",$1,"* ]]
}

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

if [ "$SKIP_LOGIN" -eq 1 ]; then
  echo "Login atlandi (--skip-login)"
elif [ -z "$CURRENT_USER" ]; then
  if ! command -v gh &>/dev/null; then
    echo "⚠️  GitHub CLI (gh) bulunamadi."
    if [ "$OS" = "windows" ]; then
      echo "   Kur: winget install GitHub.cli"
    else
      echo "   Kur: brew install gh"
    fi
  elif [ "$AUTO" -eq 1 ]; then
    echo "⚠️  GitHub login yok. --skip-login veya once 'gh auth login' calistir."
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

_create_secrets_template() {
  mkdir -p "$CLAUDE_SECRETS_DIR"
  if [ ! -f "$CLAUDE_SECRETS_FILE" ]; then
    cat > "$CLAUDE_SECRETS_FILE" <<'TMPL'
# Claude Config Secrets — fill in and keep private
GITHUB_TOKEN=
JIRA_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=
FIREBASE_SERVICE_ACCOUNT_PATH=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
OPENROUTER_API_KEY=
CLAUDE_LOCAL_BASE_URL=http://127.0.0.1:11434
CLAUDE_LOCAL_AUTH_TOKEN=ollama
CLAUDE_LOCAL_MODEL=deepseek-coder:6.7b
TMPL
    echo "  ℹ  claude-secrets/secrets.env şablonu oluşturuldu — doldurun."
  fi
}

# secrets yolu icin ~/.claude mutlaka olsun; kirik symlink (silinen/tasinan hedef) clone'i kirar
mkdir -p "$(dirname "$SECRETS_DIR")"
if [ -L "$SECRETS_DIR" ] && [ ! -e "$SECRETS_DIR" ]; then
  echo "⚠️  Kirilan secrets symlink kaldiriliyor (hedef yok): $SECRETS_DIR"
  rm -f "$SECRETS_DIR"
fi

# Secrets kaynak: claude-secrets/ (gitignore'lu dizin, private repo clone'u)
# Akış: private repo → claude-secrets/secrets.env → symlink ~/.claude/secrets/secrets.env
CLAUDE_SECRETS_DIR="$SCRIPT_DIR/claude-secrets"
CLAUDE_SECRETS_FILE="$CLAUDE_SECRETS_DIR/secrets.env"

# Symlink'i kur (henüz yoksa veya bozuksa)
mkdir -p "$SECRETS_DIR"
if [ ! -L "$SECRETS_DIR/secrets.env" ] || [ "$(readlink "$SECRETS_DIR/secrets.env")" != "$CLAUDE_SECRETS_FILE" ]; then
  rm -f "$SECRETS_DIR/secrets.env"
  ln -sf "$CLAUDE_SECRETS_FILE" "$SECRETS_DIR/secrets.env"
  echo "✅ Secrets symlink: ~/.claude/secrets/secrets.env → claude-secrets/secrets.env"
fi

if [ "$SKIP_SECRETS" -eq 1 ]; then
  echo "Secrets atlandi (--skip-secrets)"

elif [ -d "$CLAUDE_SECRETS_DIR/.git" ]; then
  # Mevcut repo → pull
  git -C "$CLAUDE_SECRETS_DIR" pull --quiet 2>/dev/null && echo "✅ Secrets guncellendi (pull)" || echo "  ⚠️ Pull basarisiz, mevcut kullanilacak."

elif [ -f "$CLAUDE_SECRETS_FILE" ]; then
  echo "✅ Secrets: claude-secrets/secrets.env mevcut"

elif [ -n "$SECRETS_REPO_URL" ]; then
  echo "Secrets clone ediliyor..."
  git clone --quiet "$SECRETS_REPO_URL" "$CLAUDE_SECRETS_DIR" 2>/dev/null && echo "✅ Secrets yuklendi" || echo "❌ Clone basarisiz."

elif [ -n "$CURRENT_USER" ] && [ "$IS_OWNER" -eq 1 ]; then
  echo "Private secrets clone ediliyor..."
  git clone --quiet "$OWNER_SECRETS_REPO" "$CLAUDE_SECRETS_DIR" 2>/dev/null && echo "✅ Secrets yuklendi" || echo "❌ Clone basarisiz. (gh auth kontrolu)"

elif [ -n "$CURRENT_USER" ] && [ "$AUTO" -eq 0 ]; then
  if confirm "Secrets reposunu indirmek ister misin?"; then
    ask "Private secrets repo URL'niz" "" SECRETS_REPO
    if [ -n "$SECRETS_REPO" ]; then
      git clone --quiet "$SECRETS_REPO" "$CLAUDE_SECRETS_DIR" 2>/dev/null && echo "✅ Secrets yuklendi" || echo "❌ Clone basarisiz."
    else
      _create_secrets_template
    fi
  else
    echo "Atlandi. /download-secrets ile sonra indirebilirsin."
    _create_secrets_template
  fi

else
  echo "Secrets atlandi. /download-secrets ile sonra indirebilirsin."
  _create_secrets_template
fi

# Source secrets (symlink → claude-secrets/secrets.env)
SECRETS_ENV="$CLAUDE_SECRETS_FILE"
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

# Windows: wrap npx commands with 'cmd /c npx' for Claude Code compatibility
if [ "$OS" = "windows" ]; then
  node -e "
    const fs = require('fs');
    const p = process.argv[1];
    const s = JSON.parse(fs.readFileSync(p, 'utf8'));
    for (const v of Object.values(s.mcpServers || {})) {
      if (v.command === 'npx') {
        v.command = 'cmd';
        v.args = ['/c', 'npx', ...v.args];
      }
    }
    fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n');
  " "$HOME/.claude/settings.json"
  echo "  Windows npx wrapper uygulandi."
fi

# MCP servers
echo "MCP sunuculari ekleniyor..."
GITHUB_TOKEN_VAL="${GITHUB_TOKEN:-}"
FIREBASE_SA_VAL="${FIREBASE_SERVICE_ACCOUNT_PATH:-}"

# npx wrapper — Windows needs 'cmd /c npx', Mac/Linux uses 'npx' directly
if [ "$OS" = "windows" ]; then
  NPX_CMD="cmd /c npx"
else
  NPX_CMD="npx"
fi

# Claude Code CLI: login olmayan PATH (brew, nvm, npm global) — yoksa "claude mcp add" sessizce duser
if [ "$OS" != "windows" ]; then
  export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
  if [ -s "$HOME/.nvm/nvm.sh" ]; then
    # shellcheck disable=SC1090
    . "$HOME/.nvm/nvm.sh" 2>/dev/null || true
  fi
  if command -v npm &>/dev/null; then
    _npmg="$(npm prefix -g 2>/dev/null)/bin"
    [ -d "$_npmg" ] && case ":$PATH:" in *":${_npmg}:"*) ;; *) export PATH="${_npmg}:$PATH" ;; esac
  fi
fi

# claude mcp add siklikla exit 1 + "already exists" — yine de basari
mcp_register() {
  local label="$1"; shift
  local out
  out="$("$@" 2>&1)" && { echo "  ✅ $label"; return 0; }
  if echo "$out" | grep -qi 'already exists'; then
    echo "  ✅ $label (zaten kayitli)"
    return 0
  fi
  echo "  ⚠️ $label eklenemedi"
  return 1
}

# Core MCPs — always installed
if ! command -v claude &>/dev/null; then
  echo "  ⚠️  claude CLI bulunamadi — MCP kaydi atlandi (PATH / npm i -g @anthropic-ai/claude-code)"
else
  mcp_register github claude mcp add -s user github -e "GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN_VAL" -- $NPX_CMD -y @modelcontextprotocol/server-github
  mcp_register git claude mcp add -s user git -- "$UVX_PATH" mcp-server-git
  mcp_register atlassian claude mcp add -s user atlassian -- $NPX_CMD -y mcp-remote@latest https://mcp.atlassian.com/v1/mcp
  mcp_register context7 claude mcp add -s user context7 -- $NPX_CMD -y @upstash/context7-mcp
  mcp_register jcodemunch claude mcp add -s user jcodemunch -- "$UVX_PATH" jcodemunch-mcp
  mcp_register fetch claude mcp add -s user fetch -- $NPX_CMD -y mcp-fetch-server
fi

# Stack-specific MCPs
if has_stack flutter; then
  if command -v claude &>/dev/null; then
    mcp_register flutter-dev claude mcp add -s user flutter-dev -- $NPX_CMD -y flutter-dev-mcp
  else
    echo "  ⏭️  flutter-dev — claude yok"
  fi
else
  echo "  ⏭️  flutter-dev atlandi (stacks: $STACKS)"
fi

if has_stack firebase || has_stack flutter; then
  if [ -n "$FIREBASE_SA_VAL" ]; then
    if command -v claude &>/dev/null; then
      mcp_register firebase claude mcp add -s user firebase -e "SERVICE_ACCOUNT_KEY_PATH=$FIREBASE_SA_VAL" -- $NPX_CMD -y @gannonh/firebase-mcp
    else
      echo "  ⏭️  firebase — claude yok"
    fi
  else
    echo "  ⏭️  firebase atlandi (FIREBASE_SERVICE_ACCOUNT_PATH ayarli degil)"
  fi
else
  echo "  ⏭️  firebase atlandi (stacks: $STACKS)"
fi

if has_stack unity; then
  # unity-mcp-cli global install (needed for per-project setup)
  if ! command -v unity-mcp-cli &>/dev/null; then
    echo "  unity-mcp-cli kuruluyor..."
    npm install -g unity-mcp-cli 2>/dev/null && echo "  ✅ unity-mcp-cli kuruldu" || echo "  ⚠️ unity-mcp-cli kurulamadi (npm install -g unity-mcp-cli)"
  else
    echo "  ✅ unity-mcp-cli zaten kurulu"
  fi
else
  echo "  ⏭️  unity-mcp atlandi (stacks: $STACKS)"
fi

# Projects — only CLAUDE.md redirector is copied to PROJECTS_ROOT
# All other files (scripts, migration, templates) stay in claude-config
cp "$SCRIPT_DIR/projects/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md"

# Bootstrapper — copy to PROJECTS_ROOT/bootstrapper
if [ -d "$SCRIPT_DIR/bootstrapper" ]; then
  mkdir -p "$PROJECTS_ROOT/bootstrapper"
  cp -r "$SCRIPT_DIR/bootstrapper/"* "$PROJECTS_ROOT/bootstrapper/" 2>/dev/null || true
fi

# OpenCode — global template: Zen (opencode) + Ollama (~/.config/opencode/opencode.json)
echo ""
echo "=== OpenCode (Zen web + Ollama lokal — ikisi birden) ==="
OPENCODE_DIR="$HOME/.config/opencode"
mkdir -p "$OPENCODE_DIR"
OPENCODE_TEMPLATE="$SCRIPT_DIR/templates/opencode.json"
if [ "$REFRESH_OPENCODE_CONFIG" -eq 1 ] && [ -f "$OPENCODE_TEMPLATE" ]; then
  if [ -f "$OPENCODE_DIR/opencode.json" ]; then
    cp "$OPENCODE_DIR/opencode.json" "$OPENCODE_DIR/opencode.json.bak.$TIMESTAMP"
    echo "  📦 Yedek: $OPENCODE_DIR/opencode.json.bak.$TIMESTAMP"
  fi
  cp "$OPENCODE_TEMPLATE" "$OPENCODE_DIR/opencode.json"
  echo "  ✅ opencode.json sablonla guncellendi (Zen ucretsiz model listesi + Ollama lokal)"
elif [ ! -f "$OPENCODE_DIR/opencode.json" ] && [ -f "$OPENCODE_TEMPLATE" ]; then
  cp "$OPENCODE_TEMPLATE" "$OPENCODE_DIR/opencode.json"
  echo "  ✅ opencode.json olusturuldu: $OPENCODE_DIR/opencode.json"
elif [ -f "$OPENCODE_DIR/opencode.json" ]; then
  echo "  ⏭️  opencode.json zaten var — atlandi. Zen+Ollama sablonu icin: ./install.sh --refresh-opencode-config"
else
  echo "  ⚠️  Sablon bulunamadi: $OPENCODE_TEMPLATE"
fi
if [ "$WITH_OPENCODE" -eq 1 ]; then
  if command -v npm &>/dev/null; then
    echo "  OpenCode CLI kuruluyor: npm install -g opencode-ai …"
    npm install -g opencode-ai 2>/dev/null && echo "  ✅ opencode-ai (opencode)" || echo "  ⚠️  opencode-ai kurulamadi"
  else
    echo "  ⚠️  npm bulunamadi — CLI: npm install -g opencode-ai"
  fi
else
  echo "  ℹ️  CLI icin: npm install -g opencode-ai veya ./install.sh --opencode"
fi

# Clean up old files from previous installs (now managed from claude-config)
rm -f "$PROJECTS_ROOT/MIGRATION_GUIDE.md" 2>/dev/null || true
rm -f "$PROJECTS_ROOT/MIGRATION_VERSION" 2>/dev/null || true
rm -f "$PROJECTS_ROOT/PROJECT_ANALYSIS.md" 2>/dev/null || true
rm -rf "$PROJECTS_ROOT/scripts" 2>/dev/null || true
rm -rf "$PROJECTS_ROOT/.claude-templates" 2>/dev/null || true

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
for f in "$HOME/.claude/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md" "$SCRIPT_DIR/projects/scripts/migration_check.sh" "$SCRIPT_DIR/projects/MIGRATION_VERSION"; do
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

# ── 8. Shell integration (fzf + cl function) ──
echo ""
echo "=== Shell ==="

# Detect shell RC file
if [ "$OS" = "windows" ]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.zshrc"
fi

# Install fzf if missing
if ! command -v fzf &>/dev/null; then
  echo "📦 fzf yukleniyor..."
  if [ "$OS" = "mac" ]; then
    brew install fzf 2>/dev/null && echo "✅ fzf yuklendi (brew)" || echo "⚠️  fzf yuklenemedi"
  elif [ "$OS" = "windows" ]; then
    if command -v winget &>/dev/null; then
      winget install junegunn.fzf --silent 2>/dev/null && echo "✅ fzf yuklendi (winget)"
    elif command -v scoop &>/dev/null; then
      scoop install fzf 2>/dev/null && echo "✅ fzf yuklendi (scoop)"
    elif command -v choco &>/dev/null; then
      choco install fzf -y 2>/dev/null && echo "✅ fzf yuklendi (choco)"
    else
      echo "⚠️  fzf yuklenemedi — winget/scoop/choco bulunamadi"
    fi
  else
    echo "⚠️  fzf yuklenemedi — manuel kur: https://github.com/junegunn/fzf"
  fi
else
  echo "✅ fzf mevcut"
fi

# Shell helpers: cl + OpenCode shortcuts (full block replaced each install)
SHELL_HELP_BEGIN="# __CLAUDE_CONFIG_SHELL_BLOCK_START__"
SHELL_HELP_END="# __CLAUDE_CONFIG_SHELL_BLOCK_END__"
touch "$SHELL_RC"
# Legacy: only first function was removed on upgrade → stale claude-free/local possible; strip old marker block
if grep -q "Claude Project Picker" "$SHELL_RC" 2>/dev/null; then
  sed -i.bak '/# Claude Project Picker/,/^}/d' "$SHELL_RC" 2>/dev/null || true
fi
if grep -q "$SHELL_HELP_BEGIN" "$SHELL_RC" 2>/dev/null; then
  sed -i.bak "/$SHELL_HELP_BEGIN/,/$SHELL_HELP_END/d" "$SHELL_RC" 2>/dev/null || true
fi
cat >> "$SHELL_RC" << 'CLEOF'

# __CLAUDE_CONFIG_SHELL_BLOCK_START__
# Claude Code env — flicker fix (experimental renderer, mouse support)
export CLAUDE_CODE_NO_FLICKER=1

# cl: Claude Code proje secici | claude-free: OpenCode Zen (gpt-5-nano) | claude-local: Ollama
function cl() {
  local projects_dir="$HOME/Projects"
  local selected
  if ! command -v fzf &>/dev/null; then
    echo "fzf bulunamadi. Kur: brew install fzf (mac) / winget install junegunn.fzf (win)"
    return 1
  fi
  selected=$(
    for d in "$projects_dir"/*/; do
      { [ -d "$d/.claude" ] || [ -f "$d/CLAUDE.md" ] || [ -d "$d/.claude-plugin" ]; } || continue
      local name=$(basename "${d%/}")
      local tag=""
      if [ -f "$d/pubspec.yaml" ]; then tag="Flutter"
      elif [ -d "$d/Assets" ] || [ -d "$d/ProjectSettings" ]; then tag="Unity"
      elif [ -f "$d/package.json" ]; then
        if [ -d "$d/app" ] || grep -q "next" "$d/package.json" 2>/dev/null; then tag="Next.js"
        else tag="Node.js"; fi
      elif [ -f "$d/pyproject.toml" ] || [ -f "$d/requirements.txt" ]; then tag="Python"
      elif [ -f "$d/Cargo.toml" ]; then tag="Rust"
      elif [ -f "$d/go.mod" ]; then tag="Go"
      else tag="—"; fi
      printf "%-30s [%s]\n" "$name" "$tag"
    done | sort | fzf \
      --height=60% \
      --border=rounded \
      --prompt="▶ Proje: " \
      --header="Claude Projeleri  [Enter: aç, Esc: çık]" \
      --cycle \
      --nth=1
  )
  [ -z "$selected" ] && return
  local dir=$(echo "$selected" | sed 's/ *\[.*$//' | sed 's/ *$//')
  cd "$projects_dir/$dir" && claude
}

function cl_bypass() {
  local projects_dir="$HOME/Projects"
  local selected
  if ! command -v fzf &>/dev/null; then
    echo "fzf bulunamadi."
    return 1
  fi
  selected=$(
    for d in "$projects_dir"/*/; do
      { [ -d "$d/.claude" ] || [ -f "$d/CLAUDE.md" ] || [ -d "$d/.claude-plugin" ]; } || continue
      local name=$(basename "${d%/}")
      local tag=""
      if [ -f "$d/pubspec.yaml" ]; then tag="Flutter"
      elif [ -d "$d/Assets" ] || [ -d "$d/ProjectSettings" ]; then tag="Unity"
      elif [ -f "$d/package.json" ]; then
        if [ -d "$d/app" ] || grep -q "next" "$d/package.json" 2>/dev/null; then tag="Next.js"
        else tag="Node.js"; fi
      elif [ -f "$d/pyproject.toml" ] || [ -f "$d/requirements.txt" ]; then tag="Python"
      elif [ -f "$d/Cargo.toml" ]; then tag="Rust"
      elif [ -f "$d/go.mod" ]; then tag="Go"
      else tag="—"; fi
      printf "%-30s [%s]\n" "$name" "$tag"
    done | sort | fzf \
      --height=60% \
      --border=rounded \
      --prompt="▶ Proje (bypass): " \
      --header="Claude Projeleri — Bypass Modu  [Enter: aç, Esc: çık]" \
      --cycle \
      --nth=1
  )
  [ -z "$selected" ] && return
  local dir=$(echo "$selected" | sed 's/ *\[.*$//' | sed 's/ *$//')
  cd "$projects_dir/$dir" && claude --dangerously-skip-permissions
}

claude-free() {
  if ! command -v opencode &>/dev/null; then
    echo "opencode bulunamadi. Kur: npm install -g opencode-ai veya ~/Projects/claude-config/./install.sh --opencode"
    return 1
  fi
  (( $# )) || set -- .
  opencode -m opencode/gpt-5-nano "$@"
}

claude-local() {
  if ! command -v opencode &>/dev/null; then
    echo "opencode bulunamadi. Kur: npm install -g opencode-ai veya ~/Projects/claude-config/./install.sh --opencode"
    return 1
  fi
  (( $# )) || set -- .
  opencode -m ollama/qwen2.5-coder:7b "$@"
}
# __CLAUDE_CONFIG_SHELL_BLOCK_END__
CLEOF
echo "✅ Shell: cl, claude-free, claude-local → $SHELL_RC"

# ── Phase 8: Local Models (Ollama) ──
setup_ollama() {
  echo ""
  echo "── Phase 8: Local Models (Ollama) ──"

  if [ "$SKIP_LOCAL_MODELS" -eq 1 ]; then
    echo "⏭  Skipped (--skip-local-models)"
    return 0
  fi

  # Detect RAM
  local RAM_GB=0
  if [ "$OS" = "mac" ]; then
    RAM_GB=$(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1073741824)}')
  elif [ "$OS" = "linux" ]; then
    RAM_GB=$(free -b 2>/dev/null | awk '/Mem:/{print int($2/1073741824)}')
  fi
  echo "  RAM detected: ${RAM_GB}GB"

  local DEVICE_PROFILE="mac"
  [ "$RAM_GB" -ge 64 ] && DEVICE_PROFILE="desktop"
  echo "  Device profile: $DEVICE_PROFILE"

  # Install Ollama if missing
  if ! command -v ollama &>/dev/null; then
    if [ "$AUTO" -eq 1 ] || [ "$WITH_LOCAL_MODELS" -eq 1 ]; then
      echo "  Installing Ollama..."
      if [ "$OS" = "mac" ]; then
        brew install ollama 2>/dev/null || curl -fsSL https://ollama.com/install.sh | sh
      else
        curl -fsSL https://ollama.com/install.sh | sh
      fi
    else
      echo "  Ollama not found. Install with: brew install ollama (Mac) or curl -fsSL https://ollama.com/install.sh | sh"
      return 0
    fi
  fi

  # Pull models based on hardware
  if [ "$WITH_LOCAL_MODELS" -eq 1 ] || [ "$AUTO" -eq 1 ]; then
    echo "  Pulling base models..."
    ollama pull qwen3.5:9b 2>/dev/null || echo "  ⚠ qwen3.5:9b pull failed (retry manually)"
    ollama pull gemma4:9b 2>/dev/null || echo "  ⚠ gemma4:9b pull failed (retry manually)"

    if [ "$DEVICE_PROFILE" = "desktop" ]; then
      echo "  Desktop detected — pulling 72B model..."
      ollama pull qwen3.6:72b 2>/dev/null || echo "  ⚠ qwen3.6:72b pull failed (retry manually)"
    fi

    echo "  ✅ Local models ready (profile: $DEVICE_PROFILE)"
  else
    echo "  ℹ  Ollama found. Use --with-local-models to pull models."
  fi
}

# ── Phase 9: Free Cloud Models (OpenRouter) ──
setup_openrouter() {
  echo ""
  echo "── Phase 9: Free Cloud Models (OpenRouter) ──"

  # Check API key in secrets
  local OR_KEY=""
  if [ -f "$SECRETS_DIR/secrets.env" ]; then
    OR_KEY=$(grep -E '^OPENROUTER_API_KEY=' "$SECRETS_DIR/secrets.env" 2>/dev/null | cut -d= -f2- || true)
  fi

  if [ -n "$OR_KEY" ]; then
    echo "  ✅ OpenRouter API key found"
    # Quick connectivity test
    if curl -s --max-time 5 "https://openrouter.ai/api/v1/models" >/dev/null 2>&1; then
      echo "  ✅ OpenRouter API reachable"
    else
      echo "  ⚠ OpenRouter API unreachable — free models will use local fallback"
    fi
  else
    echo "  ℹ  No OPENROUTER_API_KEY in secrets.env — free cloud models disabled"
    echo "     Add to ~/.claude/secrets/secrets.env: OPENROUTER_API_KEY=sk-or-..."
  fi

  # Copy free models list
  mkdir -p "$HOME/.claude/config"
  cp "$SCRIPT_DIR/config/openrouter-free-models.json" "$HOME/.claude/config/" 2>/dev/null || true
  echo "  ✅ Free models list copied"
}

# ── Phase 10: Agent Definitions ──
install_agents() {
  echo ""
  echo "── Phase 10: Agent Definitions ──"

  if [ "$SKIP_AGENTS" -eq 1 ]; then
    echo "  ⏭  Skipped (--skip-agents)"
    return 0
  fi

  mkdir -p "$HOME/.claude/agents"
  mkdir -p "$HOME/.claude/config"

  # Copy agent definitions
  if [ -d "$SCRIPT_DIR/agents" ]; then
    cp -r "$SCRIPT_DIR/agents/"* "$HOME/.claude/agents/" 2>/dev/null || true
    local AGENT_COUNT
    AGENT_COUNT=$(find "$HOME/.claude/agents" -name "*.md" -not -name "README.md" 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✅ Agent definitions: $AGENT_COUNT agents installed"
  fi

  # Copy config files
  for f in agent-registry.json fallback-chains.json model-tiers.json layer-contracts.json model-requirements.json openrouter-free-models.json; do
    if [ -f "$SCRIPT_DIR/config/$f" ]; then
      cp "$SCRIPT_DIR/config/$f" "$HOME/.claude/config/" 2>/dev/null || true
    fi
  done

  # Copy dependency checker
  if [ -f "$SCRIPT_DIR/config/check-agent-deps.sh" ]; then
    cp "$SCRIPT_DIR/config/check-agent-deps.sh" "$HOME/.claude/config/" 2>/dev/null || true
    chmod +x "$HOME/.claude/config/check-agent-deps.sh" 2>/dev/null || true
  fi
  echo "  ✅ Config files copied (registry, fallback, tiers, contracts, deps, models)"

  # Validate registry
  if command -v python3 &>/dev/null && [ -f "$HOME/.claude/config/agent-registry.json" ]; then
    if python3 -c "import json; json.load(open('$HOME/.claude/config/agent-registry.json'))" 2>/dev/null; then
      local ACTIVE
      ACTIVE=$(python3 -c "import json; d=json.load(open('$HOME/.claude/config/agent-registry.json')); print(len([a for a in d['agents'].values() if a.get('status')=='active']))" 2>/dev/null || echo "?")
      echo "  ✅ Registry valid — $ACTIVE active agents"
    else
      echo "  ⚠ Registry JSON invalid — check config/agent-registry.json"
      ERRORS=$((ERRORS + 1))
    fi
  fi
}

# ── Phase 11: Cron / Health Checks ──
setup_cron() {
  echo ""
  echo "── Phase 11: Health Checks ──"

  if [ "$SKIP_CRON" -eq 1 ]; then
    echo "  ⏭  Skipped (--skip-cron)"
    return 0
  fi

  # Copy daily-check.sh
  mkdir -p "$HOME/.claude/config"
  if [ -f "$SCRIPT_DIR/config/daily-check.sh" ]; then
    cp "$SCRIPT_DIR/config/daily-check.sh" "$HOME/.claude/config/daily-check.sh"
    chmod +x "$HOME/.claude/config/daily-check.sh"
    echo "  ✅ daily-check.sh installed"
  fi

  # Create watchdog directory
  mkdir -p "$HOME/.watchdog"
  echo "  ✅ Watchdog directory ready"

  # Create agent-memory directory structure
  mkdir -p "$HOME/.claude/agent-memory/sessions"
  mkdir -p "$HOME/.claude/agent-memory/feedback"
  if [ ! -f "$HOME/.claude/agent-memory/session_state.json" ]; then
    echo '{"version":"1.0","active_layer":null,"layers":{}}' > "$HOME/.claude/agent-memory/session_state.json"
  fi
  echo "  ✅ Agent memory structure ready (sessions/, feedback/, session_state.json)"

  # Cron registration (duplicate-safe)
  CRON_LINE="0 9 * * * bash $HOME/.claude/config/daily-check.sh >> $HOME/.watchdog/cron.log 2>&1"
  if [ "$OS" = "windows" ]; then
    echo "  ℹ  Windows: Task Scheduler ile daily-check.sh zamanla"
  else
    if crontab -l 2>/dev/null | grep -qF "daily-check.sh"; then
      echo "  ✅ Cron zaten kayıtlı"
    else
      (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
      echo "  ✅ Cron eklendi: günlük 09:00 → daily-check.sh"
    fi
  fi
}

# ── Phase 12: Voice (Turkish) ──
setup_voice() {
  echo ""
  echo "── Phase 12: Voice Config (Turkish) ──"
  echo "  ✅ Voice language: tr (Turkish) — configured in settings.json"
  echo "  ℹ  Usage: Hold Space → speak Turkish → release"
}

# ── Phase 13: Telegram ──
setup_telegram() {
  echo ""
  echo "── Phase 13: Telegram Notifications ──"

  # notify.sh, telegram-ask.sh, telegram-wait.sh, telegram-poll.sh kopyala
  for f in notify.sh telegram-ask.sh telegram-wait.sh telegram-poll.sh; do
    if [ -f "$SCRIPT_DIR/config/$f" ]; then
      cp "$SCRIPT_DIR/config/$f" "$HOME/.claude/config/$f"
      chmod +x "$HOME/.claude/config/$f"
    fi
  done

  # Secrets'tan token kontrol
  TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" "$CLAUDE_SECRETS_FILE" 2>/dev/null | cut -d= -f2)
  CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" "$CLAUDE_SECRETS_FILE" 2>/dev/null | cut -d= -f2)

  if [ -n "$TOKEN" ] && [ -n "$CHAT_ID" ]; then
    # Test bildirimi gönder
    RESP=$(curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
      -d chat_id="$CHAT_ID" \
      -d text="✅ Claude Code kurulumu tamamlandı." -o /dev/null -w "%{http_code}")
    if [ "$RESP" = "200" ]; then
      echo "  ✅ Telegram bağlantısı doğrulandı"
    else
      echo "  ⚠️  Telegram token/chat_id hatalı (HTTP $RESP)"
    fi
  else
    echo "  ℹ  TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik — claude-secrets güncelle"
  fi
}

# ── Phase 14: Plugin Marketplace ──
setup_plugins() {
  echo ""
  echo "── Phase 14: Plugin Marketplace ──"

  # Companion repos — clone if missing
  for repo_info in "claude-marketplace:SkyWalker2506/claude-marketplace" "claude-agent-catalog:SkyWalker2506/claude-agent-catalog"; do
    dir_name="${repo_info%%:*}"
    repo="${repo_info##*:}"
    target="$PROJECTS_ROOT/$dir_name"
    if [ ! -d "$target/.git" ]; then
      echo "  📥 $dir_name clone ediliyor..."
      if gh repo clone "$repo" "$target" 2>/dev/null; then
        echo "  ✅ $dir_name klonlandı"
      else
        echo "  ⚠️  $dir_name klonlanamadı (gh auth gerekebilir)"
      fi
    else
      echo "  ○  $dir_name zaten mevcut — güncelleniyor..."
      git -C "$target" pull --rebase --quiet 2>/dev/null || true
    fi
  done

  # claude CLI var mi?
  if ! command -v claude &>/dev/null; then
    echo "  ⚠️  claude CLI bulunamadı — plugin kurulumu atlandı"
    return
  fi

  # Marketplace kaydı
  echo "  📦 SkyWalker2506/claude-marketplace kaydediliyor..."
  if claude plugin marketplace add SkyWalker2506/claude-marketplace 2>/dev/null; then
    echo "  ✅ Marketplace kaydedildi"
  else
    echo "  ○  Marketplace zaten kayıtlı"
  fi

  echo ""
  echo "  Mevcut pluginler (keşfet ve kur):"
  echo "    /plugin > Discover"
  echo "  Veya doğrudan:"
  echo "    claude plugin install telegram-bridge@musabkara-claude-marketplace"
  echo "    claude plugin install ai-review@musabkara-claude-marketplace"
  echo "    claude plugin install daily-check@musabkara-claude-marketplace"
  echo "    claude plugin install sync-agents@musabkara-claude-marketplace"

  # Auto-install plugins based on project type
  echo ""
  echo "── Auto-installing plugins ──"

  # Always install these core plugins
  for plugin in code-quality devtools-setup git-github; do
    claude plugin install "${plugin}@musabkara-claude-marketplace" 2>/dev/null && echo "✅ $plugin" || echo "⚠️  $plugin (install manually)"
  done

  # Flutter projects
  if [ -f "pubspec.yaml" ]; then
    claude plugin install "flutter-firebase@musabkara-claude-marketplace" 2>/dev/null && echo "✅ flutter-firebase" || true
  fi

  # Jira projects (check for CLAUDE_JIRA.md or jira config)
  if [ -f "docs/CLAUDE_JIRA.md" ] || [ -f ".jira" ]; then
    claude plugin install "jira-suite@musabkara-claude-marketplace" 2>/dev/null && echo "✅ jira-suite" || true
    claude plugin install "sprint-planner@musabkara-claude-marketplace" 2>/dev/null && echo "✅ sprint-planner" || true
  fi
}

# ── Run Phase 8-14 ──
if [ "$ONLY_AGENTS" -eq 1 ]; then
  install_agents
else
  setup_ollama
  setup_openrouter
  install_agents
  setup_cron
  setup_voice
  setup_telegram
  setup_plugins
fi

# ── 9. Done ──
echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "=== Kurulum basarili! ==="
else
  echo "=== $ERRORS hata tespit edildi. ==="
fi
echo ""
echo "Kullanim:"
echo "  cd $PROJECTS_ROOT/HerhangiBirProje && claude"
echo "  claude-free   # OpenCode TUI, Zen opencode/gpt-5-nano (/\`/connect ile anahtar)"
echo "  claude-local  # OpenCode TUI, Ollama qwen2.5-coder:7b (once: ollama pull ...)"
echo "  (Yeni shell veya: source $SHELL_RC)"
[ -n "${BACKUP:-}" ] && echo "Yedek: $BACKUP"
