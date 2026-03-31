#!/bin/bash
set -euo pipefail

# claude-config installer
# Tek komutla Claude Code konfigurasyonunu kur

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SECRETS_DIR="$HOME/.claude/secrets"

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

# ── 3. Secrets Vault ──
echo ""
echo "=== Secrets (API key, token vb.) ==="

SECRETS_LOADED=0

if [ -d "$SECRETS_DIR/.git" ]; then
  echo "Mevcut secrets reposu bulundu: $SECRETS_DIR"
  read -p "Guncellensin mi? [E/h]: " UPDATE_SECRETS
  UPDATE_SECRETS="${UPDATE_SECRETS:-E}"
  if [[ "$UPDATE_SECRETS" =~ ^[Ee]$ ]]; then
    git -C "$SECRETS_DIR" pull --quiet 2>/dev/null && echo "✅ Secrets guncellendi" || echo "⚠️  Pull basarisiz, mevcut versiyon kullanilacak"
  fi
  SECRETS_LOADED=1
else
  echo "Secrets vault kurulumu (opsiyonel):"
  echo "  Private bir git reponuz varsa URL'sini girin."
  echo "  Yoksa secrets'lari elle girebilirsiniz."
  echo ""
  read -p "Secrets repo URL (bos birakirsan elle girersin): " SECRETS_REPO

  if [ -n "$SECRETS_REPO" ]; then
    echo "Secrets reposu clone ediliyor..."
    mkdir -p "$SECRETS_DIR"
    if git clone --quiet "$SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null; then
      echo "✅ Secrets reposu yuklendi"
      SECRETS_LOADED=1
    else
      echo "❌ Clone basarisiz. URL'yi kontrol edin."
      echo "   Secrets'lari elle girebilirsiniz."
    fi
  fi
fi

# Secrets dosyasi kontrol + yukleme
SECRETS_ENV="$SECRETS_DIR/secrets.env"

if [ "$SECRETS_LOADED" -eq 1 ] && [ -f "$SECRETS_ENV" ]; then
  echo "✅ secrets.env yuklendi"
  # .env formatinda source et (yorumlari ve bos satirlari atla)
  set -a
  while IFS= read -r line; do
    # Bos satir, yorum veya sadece bosluk → atla
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Yorum olmayan, = iceren satirlari export et
    [[ "$line" =~ ^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*= ]] && eval "export $line" 2>/dev/null || true
  done < "$SECRETS_ENV"
  set +a
else
  if [ "$SECRETS_LOADED" -eq 0 ]; then
    echo ""
    echo "Elle secret girisi (bos birakirsan sonra eklersin):"
    echo ""

    # Zorunlu
    read -p "  GITHUB_TOKEN: " INPUT_GITHUB_TOKEN
    read -p "  JIRA_URL (orn: https://site.atlassian.net): " INPUT_JIRA_URL
    read -p "  JIRA_USERNAME: " INPUT_JIRA_USERNAME
    read -p "  JIRA_API_TOKEN: " INPUT_JIRA_API_TOKEN

    # Opsiyonel
    echo ""
    echo "  Opsiyonel (bos birakilabilir):"
    read -p "  FIREBASE_SERVICE_ACCOUNT_PATH: " INPUT_FIREBASE_SA
    read -p "  TELEGRAM_BOT_TOKEN: " INPUT_TELEGRAM_TOKEN
    read -p "  TELEGRAM_CHAT_ID: " INPUT_TELEGRAM_CHAT

    # secrets.env olustur
    mkdir -p "$SECRETS_DIR"
    cat > "$SECRETS_ENV" <<ENVEOF
# Claude Config Secrets — otomatik olusturuldu ($TIMESTAMP)
# Bu dosya ~/.claude/secrets/secrets.env konumunda saklanir

# ZORUNLU
GITHUB_TOKEN=$INPUT_GITHUB_TOKEN
JIRA_URL=$INPUT_JIRA_URL
JIRA_USERNAME=$INPUT_JIRA_USERNAME
JIRA_API_TOKEN=$INPUT_JIRA_API_TOKEN

# OPSIYONEL
FIREBASE_SERVICE_ACCOUNT_PATH=$INPUT_FIREBASE_SA
TELEGRAM_BOT_TOKEN=$INPUT_TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=$INPUT_TELEGRAM_CHAT
ENVEOF

    chmod 600 "$SECRETS_ENV"
    echo ""
    echo "✅ secrets.env olusturuldu: $SECRETS_ENV"
    echo "   Daha sonra duzenlemek icin: nano $SECRETS_ENV"

    # Source et
    set -a
    while IFS= read -r line; do
      [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
      [[ "$line" =~ ^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*= ]] && eval "export $line" 2>/dev/null || true
    done < "$SECRETS_ENV"
    set +a
  fi
fi

# 4. Mevcut config yedekle
if [ -d "$HOME/.claude" ]; then
  BACKUP="$HOME/.claude.backup.$TIMESTAMP"
  echo ""
  echo "Mevcut ~/.claude/ yedekleniyor → $BACKUP"
  cp -r "$HOME/.claude" "$BACKUP"
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

# settings.json — template'den olustur
sed \
  -e "s|__UVX_PATH__|$UVX_PATH|g" \
  -e "s|__PROJECTS_ROOT__|$PROJECTS_ROOT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$SCRIPT_DIR/global/settings.json.template" > "$HOME/.claude/settings.json"

# 7. Projects dosyalari kopyala
echo "Projects dosyalari kopyalaniyor..."
cp "$SCRIPT_DIR/projects/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_GUIDE.md" "$PROJECTS_ROOT/MIGRATION_GUIDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_VERSION" "$PROJECTS_ROOT/MIGRATION_VERSION"
cp "$SCRIPT_DIR/projects/PROJECT_ANALYSIS.md" "$PROJECTS_ROOT/PROJECT_ANALYSIS.md"

# migration_check.sh — kendi konumundan path buluyor, duz kopyala + executable yap
cp "$SCRIPT_DIR/projects/scripts/migration_check.sh" "$PROJECTS_ROOT/scripts/migration_check.sh"
chmod +x "$PROJECTS_ROOT/scripts/migration_check.sh"

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

REQUIRED_SECRETS=("GITHUB_TOKEN" "JIRA_URL" "JIRA_USERNAME" "JIRA_API_TOKEN")
OPTIONAL_SECRETS=("FIREBASE_SERVICE_ACCOUNT_PATH" "TELEGRAM_BOT_TOKEN" "TELEGRAM_CHAT_ID")
MISSING_REQUIRED=()
MISSING_OPTIONAL=()

for var in "${REQUIRED_SECRETS[@]}"; do
  val="${!var:-}"
  if [ -n "$val" ]; then
    # Ilk 4 ve son 2 karakter goster, arasi ***
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
    echo ""
    echo "   Veya private repo olustur:"
    echo "     cd $SECRETS_DIR && git init && git add . && git commit -m 'init'"
    echo "     gh repo create claude-secrets --private --source=. --push"
    echo "   Baska PC'de: install.sh sana repo URL'si soracak."
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
