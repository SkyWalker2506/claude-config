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

# ── 3. Secrets Vault ──
echo ""
echo "=== Secrets (API key, token vb.) ==="

# GitHub kullanicisini al
CURRENT_USER=""
if command -v gh &>/dev/null; then
  CURRENT_USER=$(gh api user -q .login 2>/dev/null || echo "")
fi
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

elif [ "$IS_OWNER" -eq 1 ]; then
  # ── Sahip, yeni PC → kendi private reposundan otomatik cek ──
  echo "Sahip olarak tespit edildin ($CURRENT_USER)."
  echo "Private secrets reposu clone ediliyor..."
  if git clone --quiet "$OWNER_SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null; then
    echo "✅ Secrets otomatik yuklendi"
  else
    echo "❌ Clone basarisiz. Erisim izninizi kontrol edin."
    echo "   gh auth login ile GitHub'a giris yapin."
    mkdir -p "$SECRETS_DIR"
  fi

else
  # ── Baska kullanici → kendi secrets'ini kursun ──
  echo ""
  if [ -n "$CURRENT_USER" ]; then
    echo "Hosgeldin $CURRENT_USER! Secrets vault kurulumu gerekiyor."
  else
    echo "Secrets vault kurulumu gerekiyor."
  fi
  echo ""
  echo "API key ve token'larinizi guvenli saklamak icin private bir secrets reposu kullanilir."
  echo ""
  echo "Iki secenek:"
  echo "  1) Zaten private secrets reponuz varsa → URL girin"
  echo "  2) Yoksa → simdi olusturalim"
  echo ""
  read -p "Private secrets repo URL'niz var mi? (varsa girin, yoksa ENTER): " SECRETS_REPO

  if [ -n "$SECRETS_REPO" ]; then
    echo "Clone ediliyor..."
    if git clone --quiet "$SECRETS_REPO" "$SECRETS_DIR" 2>/dev/null; then
      echo "✅ Secrets reposu yuklendi"
    else
      echo "❌ Clone basarisiz. URL veya erisimi kontrol edin."
      mkdir -p "$SECRETS_DIR"
    fi
  else
    # Sifirdan olustur
    echo ""
    echo "Secrets'lari girelim (bos birakirsaniz sonra eklersiniz):"
    echo ""

    read -p "  GITHUB_TOKEN: " INPUT_GITHUB_TOKEN
    read -p "  JIRA_URL (orn: https://site.atlassian.net): " INPUT_JIRA_URL
    read -p "  JIRA_USERNAME: " INPUT_JIRA_USERNAME
    read -p "  JIRA_API_TOKEN: " INPUT_JIRA_API_TOKEN

    echo ""
    echo "  Opsiyonel (bos birakilabilir):"
    read -p "  FIREBASE_SERVICE_ACCOUNT_PATH: " INPUT_FIREBASE_SA
    read -p "  TELEGRAM_BOT_TOKEN: " INPUT_TELEGRAM_TOKEN
    read -p "  TELEGRAM_CHAT_ID: " INPUT_TELEGRAM_CHAT

    mkdir -p "$SECRETS_DIR"
    cat > "$SECRETS_DIR/secrets.env" <<ENVEOF
# Claude Config Secrets — $TIMESTAMP
# ASLA public repoya commit etmeyin!

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

    chmod 600 "$SECRETS_DIR/secrets.env"
    echo ""
    echo "✅ secrets.env olusturuldu"

    # Private repo olustur
    echo ""
    echo "Bu secrets'lari baska PC'lere tasimak icin private GitHub repo olusturabilirsiniz."
    read -p "Private secrets reposu olusturulsun mu? [E/h]: " CREATE_SECRETS_REPO
    CREATE_SECRETS_REPO="${CREATE_SECRETS_REPO:-E}"

    if [[ "$CREATE_SECRETS_REPO" =~ ^[Ee]$ ]]; then
      cat > "$SECRETS_DIR/.gitignore" <<'GIEOF'
*.bak
*.tmp
GIEOF
      cat > "$SECRETS_DIR/README.md" <<'RDEOF'
# claude-secrets (private)

Claude Code API key, token ve credential deposu.
`claude-config/install.sh` bu repoyu otomatik clone/pull eder.

## Duzenleme

```bash
nano ~/.claude/secrets/secrets.env
cd ~/.claude/secrets && git add -A && git commit -m "update" && git push
```
RDEOF

      cd "$SECRETS_DIR"
      git init --quiet
      git add -A
      git commit --quiet -m "Initial commit: secrets vault"

      if command -v gh &>/dev/null; then
        REPO_NAME="claude-secrets"
        if gh repo create "$REPO_NAME" --private --source=. --push --description "Private secrets for claude-config" 2>/dev/null; then
          echo "✅ Private repo olusturuldu: https://github.com/$CURRENT_USER/$REPO_NAME"
        else
          echo "⚠️  Otomatik repo olusturulamadi. Manuel:"
          echo "   github.com → New repo → '$REPO_NAME' → Private"
          echo "   git remote add origin <URL> && git push -u origin main"
        fi
      else
        echo "⚠️  GitHub CLI (gh) bulunamadi. Manuel olusturun:"
        echo "   github.com → New repo → 'claude-secrets' → Private"
        echo "   cd $SECRETS_DIR && git remote add origin <URL> && git push -u origin main"
      fi
      cd "$SCRIPT_DIR"
    fi
  fi
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
