#!/bin/bash
set -euo pipefail

# claude-config installer
# Tek komutla Claude Code konfigurasyonunu kur

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SECRETS_DIR="$HOME/.claude/secrets"

# Repo sahibi — bu config'i olusturan kisi
OWNER_GITHUB="SkyWalker2506"
OWNER_SECRETS_REPO="https://github.com/SkyWalker2506/claude-secrets.git"

echo "=== Claude Code Config Installer ==="
echo ""

# 1. Proje kok dizini
read -p "Proje kok dizini [$HOME/Projects]: " PROJECTS_ROOT
PROJECTS_ROOT="${PROJECTS_ROOT:-$HOME/Projects}"
PROJECTS_ROOT="${PROJECTS_ROOT/#\~/$HOME}"

if [ ! -d "$PROJECTS_ROOT" ]; then
  echo "Dizin yok, olusturuluyor: $PROJECTS_ROOT"
  mkdir -p "$PROJECTS_ROOT"
fi

# 2. uvx yolunu bul
UVX_PATH=$(which uvx 2>/dev/null || echo "")
if [ -z "$UVX_PATH" ]; then
  echo "⚠️  uvx bulunamadi. jCodeMunch MCP calismayacak."
  echo "   Kurmak icin: pip3 install pipx && pipx install uvx"
  UVX_PATH="uvx"
fi
echo "uvx: $UVX_PATH"

# ── 3. GitHub Login + Secrets Vault ──
echo ""
echo "=== GitHub Login ==="

# GitHub login kontrolu
CURRENT_USER=""
if command -v gh &>/dev/null; then
  CURRENT_USER=$(gh api user -q .login 2>/dev/null || echo "")
fi

if [ -z "$CURRENT_USER" ]; then
  echo "⚠️  GitHub'a giris yapilmamis."
  read -p "Simdi giris yapmak ister misin? [E/h]: " DO_LOGIN
  DO_LOGIN="${DO_LOGIN:-E}"
  if [[ "$DO_LOGIN" =~ ^[Ee]$ ]]; then
    gh auth login --web -p https
    CURRENT_USER=$(gh api user -q .login 2>/dev/null || echo "")
    if [ -n "$CURRENT_USER" ]; then
      echo "✅ GitHub'a $CURRENT_USER olarak giris yapildi"
      gh auth setup-git
    else
      echo "⚠️  Login basarisiz. Secrets adimi atlanacak."
    fi
  fi
else
  echo "✅ GitHub: $CURRENT_USER"
fi

echo ""
echo "=== Secrets (API key, token vb.) ==="

IS_OWNER=0
if [ "$CURRENT_USER" = "$OWNER_GITHUB" ]; then
  IS_OWNER=1
fi

if [ -d "$SECRETS_DIR/.git" ]; then
  # ── Mevcut secrets reposu var → git pull ──
  echo "✅ Secrets reposu mevcut: $SECRETS_DIR"
  git -C "$SECRETS_DIR" pull --quiet 2>/dev/null && echo "   Guncellendi." || echo "   ⚠️ Pull basarisiz, mevcut versiyon kullanilacak."

elif [ -f "$SECRETS_DIR/secrets.env" ]; then
  # ── Lokal secrets.env var, git yok → dokunma ──
  echo "✅ Lokal secrets.env mevcut"

elif [ -n "$CURRENT_USER" ]; then
  # ── Login var, secrets yok → indirmek ister mi sor ──
  echo ""
  read -p "Secrets reposunu indirmek ister misin? [E/h]: " DO_SECRETS
  DO_SECRETS="${DO_SECRETS:-E}"

  if [[ "$DO_SECRETS" =~ ^[Ee]$ ]]; then
    if [ "$IS_OWNER" -eq 1 ]; then
      # Sahip → otomatik clone
      echo "Private secrets reposu clone ediliyor..."
      if git clone --quiet "$OWNER_SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null; then
        echo "✅ Secrets otomatik yuklendi"
      else
        echo "❌ Clone basarisiz. Erisim izninizi kontrol edin."
        mkdir -p "$SECRETS_DIR"
      fi
    else
      # Baska kullanici → URL sor
      read -p "Private secrets repo URL'niz: " SECRETS_REPO
      if [ -n "$SECRETS_REPO" ]; then
        if git clone --quiet "$SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null; then
          echo "✅ Secrets reposu yuklendi"
        else
          echo "❌ Clone basarisiz."
          mkdir -p "$SECRETS_DIR"
        fi
      else
        mkdir -p "$SECRETS_DIR"
      fi
    fi
  else
    echo "Secrets atlandi. Sonra /download-secrets ile indirebilirsin."
    mkdir -p "$SECRETS_DIR"
  fi

else
  # ── Login yok veya basarisiz → secrets atalanacak ──
  echo "GitHub login yok. Secrets atlandi."
  echo "Sonra /admin-login ve /download-secrets ile kurabilirsin."
  mkdir -p "$SECRETS_DIR"
fi

# Secrets dosyasini source et (varsa)
SECRETS_ENV="$SECRETS_DIR/secrets.env"
if [ -f "$SECRETS_ENV" ]; then
  set -a
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*= ]] && eval "export $line" 2>/dev/null || true
  done < "$SECRETS_ENV"
  set +a
fi

# 4. Mevcut config yedekle
if [ -d "$HOME/.claude" ]; then
  BACKUP="$HOME/.claude.backup.$TIMESTAMP"
  echo ""
  echo "Mevcut ~/.claude/ yedekleniyor → $BACKUP"
  rsync -a --exclude='secrets/' "$HOME/.claude/" "$BACKUP/" 2>/dev/null || cp -r "$HOME/.claude" "$BACKUP"
fi

# 5. Dizinleri olustur
mkdir -p "$HOME/.claude/skills"
mkdir -p "$PROJECTS_ROOT/scripts"
mkdir -p "$PROJECTS_ROOT/.watchdog"
mkdir -p /tmp/watchdog

# 6. Global dosyalari kopyala
echo ""
echo "Global dosyalar kopyalaniyor..."
cp "$SCRIPT_DIR/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md"

# Skills — mevcut ek skill'leri koruyarak kopyala
for skill_dir in "$SCRIPT_DIR/global/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$HOME/.claude/skills/$skill_name"
  cp -r "$skill_dir"* "$HOME/.claude/skills/$skill_name/" 2>/dev/null || true
done

# settings.json — template'den olustur (permissions, hooks vb.)
sed \
  -e "s|__UVX_PATH__|$UVX_PATH|g" \
  -e "s|__PROJECTS_ROOT__|$PROJECTS_ROOT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$SCRIPT_DIR/global/settings.json.template" > "$HOME/.claude/settings.json"

# MCP sunucularini claude mcp add ile ekle (claude.json'a yazar)
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

# 7. Projects dosyalari kopyala
echo "Projects dosyalari kopyalaniyor..."
cp "$SCRIPT_DIR/projects/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_GUIDE.md" "$PROJECTS_ROOT/MIGRATION_GUIDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_VERSION" "$PROJECTS_ROOT/MIGRATION_VERSION"
cp "$SCRIPT_DIR/projects/PROJECT_ANALYSIS.md" "$PROJECTS_ROOT/PROJECT_ANALYSIS.md"

# migration_check.sh — kendi konumundan path buluyor, duz kopyala + executable yap
cp "$SCRIPT_DIR/projects/scripts/migration_check.sh" "$PROJECTS_ROOT/scripts/migration_check.sh"
chmod +x "$PROJECTS_ROOT/scripts/migration_check.sh"

# Ralph — autonomous agent loop
cp "$SCRIPT_DIR/projects/scripts/ralph.sh" "$PROJECTS_ROOT/scripts/ralph.sh"
cp "$SCRIPT_DIR/projects/scripts/ralph-prompt.md" "$PROJECTS_ROOT/scripts/ralph-prompt.md"
chmod +x "$PROJECTS_ROOT/scripts/ralph.sh"

# 8. Templates kopyala
mkdir -p "$PROJECTS_ROOT/.claude-templates"
cp "$SCRIPT_DIR/templates/"* "$PROJECTS_ROOT/.claude-templates/" 2>/dev/null || true

# ── 9. Dogrulama ──
echo ""
echo "=== Dogrulama ==="
ERRORS=0
WARNINGS=0

# JSON parse
if python3 -c "import json; json.load(open('$HOME/.claude/settings.json'))" 2>/dev/null; then
  echo "✅ settings.json gecerli"
else
  echo "❌ settings.json JSON hatali!"
  ERRORS=$((ERRORS + 1))
fi

# Dosya varlik
for f in "$HOME/.claude/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md" "$PROJECTS_ROOT/scripts/migration_check.sh" "$PROJECTS_ROOT/MIGRATION_VERSION"; do
  if [ -f "$f" ]; then
    echo "✅ $(basename $f) mevcut"
  else
    echo "❌ $f bulunamadi!"
    ERRORS=$((ERRORS + 1))
  fi
done

# Skill sayisi
SKILL_COUNT=$(ls -d "$HOME/.claude/skills"/*/ 2>/dev/null | wc -l | tr -d ' ')
echo "✅ $SKILL_COUNT skill yuklendi"

# Hook calisir mi
if bash "$PROJECTS_ROOT/scripts/migration_check.sh" >/dev/null 2>&1; then
  echo "✅ migration_check.sh calisir"
else
  echo "⚠️  migration_check.sh hata verdi (kapsam disi olabilir — normal)"
fi

# ── 10. Secrets dogrulama ──
echo ""
echo "=== Secrets Kontrolu ==="

REQUIRED_SECRETS=("GITHUB_TOKEN")
OPTIONAL_SECRETS=("JIRA_URL" "JIRA_USERNAME" "JIRA_API_TOKEN" "FIREBASE_SERVICE_ACCOUNT_PATH" "TELEGRAM_BOT_TOKEN" "TELEGRAM_CHAT_ID")
MISSING_REQUIRED=()

for var in "${REQUIRED_SECRETS[@]}"; do
  val="${!var:-}"
  if [ -n "$val" ]; then
    if [ ${#val} -gt 8 ]; then
      MASKED="${val:0:4}***${val: -2}"
    else
      MASKED="***"
    fi
    echo "✅ $var = $MASKED"
  else
    echo "❌ $var eksik!"
    MISSING_REQUIRED+=("$var")
    WARNINGS=$((WARNINGS + 1))
  fi
done

for var in "${OPTIONAL_SECRETS[@]}"; do
  val="${!var:-}"
  if [ -n "$val" ]; then
    echo "✅ $var ayarli"
  else
    echo "⚪ $var ayarlanmamis (opsiyonel)"
  fi
done

# ── 11. Sonuc ──
echo ""
if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  echo "=== Kurulum basarili! Tum secrets tamam. ==="
elif [ "$ERRORS" -eq 0 ]; then
  echo "=== Kurulum basarili! ==="
  if [ ${#MISSING_REQUIRED[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Eksik zorunlu secrets: ${MISSING_REQUIRED[*]}"
    echo "   Duzelt: nano $SECRETS_ENV"
    echo "   Sonra: ./install.sh tekrar calistir"
  fi
else
  echo "=== $ERRORS hata tespit edildi. ==="
fi

echo ""
echo "Kullanim:"
echo "  cd $PROJECTS_ROOT/HerhangiBirProje && claude"
echo "  → MIGRATION_NEEDED sinyali gelir → /migration setup ile kur"
if [ -n "${BACKUP:-}" ]; then
  echo ""
  echo "Yedek: $BACKUP"
fi
