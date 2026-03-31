#!/bin/bash
set -euo pipefail

# claude-config installer
# Tek komutla Claude Code konfigurasyonunu kur

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

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

# 3. Mevcut config yedekle
if [ -d "$HOME/.claude" ]; then
  BACKUP="$HOME/.claude.backup.$TIMESTAMP"
  echo "Mevcut ~/.claude/ yedekleniyor → $BACKUP"
  cp -r "$HOME/.claude" "$BACKUP"
fi

# 4. Dizinleri olustur
mkdir -p "$HOME/.claude/skills"
mkdir -p "$PROJECTS_ROOT/scripts"
mkdir -p "$PROJECTS_ROOT/.watchdog"
mkdir -p /tmp/watchdog

# 5. Global dosyalari kopyala
echo "Global dosyalar kopyalaniyor..."
cp "$SCRIPT_DIR/global/CLAUDE.md" "$HOME/.claude/CLAUDE.md"

# Skills — mevcut ek skill'leri koruyarak kopyala
for skill_dir in "$SCRIPT_DIR/global/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$HOME/.claude/skills/$skill_name"
  cp "$skill_dir"* "$HOME/.claude/skills/$skill_name/" 2>/dev/null || true
done

# settings.json — template'den olustur
sed \
  -e "s|__UVX_PATH__|$UVX_PATH|g" \
  -e "s|__PROJECTS_ROOT__|$PROJECTS_ROOT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$SCRIPT_DIR/global/settings.json.template" > "$HOME/.claude/settings.json"

# 6. Projects dosyalari kopyala
echo "Projects dosyalari kopyalaniyor..."
cp "$SCRIPT_DIR/projects/CLAUDE.md" "$PROJECTS_ROOT/CLAUDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_GUIDE.md" "$PROJECTS_ROOT/MIGRATION_GUIDE.md"
cp "$SCRIPT_DIR/projects/MIGRATION_VERSION" "$PROJECTS_ROOT/MIGRATION_VERSION"
cp "$SCRIPT_DIR/projects/PROJECT_ANALYSIS.md" "$PROJECTS_ROOT/PROJECT_ANALYSIS.md"

# migration_check.sh — placeholder degistir + executable yap
sed \
  -e "s|__PROJECTS_ROOT__|$PROJECTS_ROOT|g" \
  -e "s|__HOME__|$HOME|g" \
  "$SCRIPT_DIR/projects/scripts/migration_check.sh" > "$PROJECTS_ROOT/scripts/migration_check.sh"
chmod +x "$PROJECTS_ROOT/scripts/migration_check.sh"

# 7. Templates kopyala
mkdir -p "$PROJECTS_ROOT/.claude-templates"
cp "$SCRIPT_DIR/templates/"* "$PROJECTS_ROOT/.claude-templates/" 2>/dev/null || true

# 8. settings.json hook'undaki path'i guncelle
# Hook zaten __PROJECTS_ROOT__ ile template'de dogru ayarlandi

# 9. Dogrulama
echo ""
echo "=== Dogrulama ==="
ERRORS=0

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

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "=== Kurulum basarili! ==="
  echo ""
  echo "Kullanim:"
  echo "  cd $PROJECTS_ROOT/HerhangiBirProje && claude"
  echo "  → MIGRATION_NEEDED sinyali gelir → /migration setup ile kur"
  echo ""
  echo "Yedek: $BACKUP"
else
  echo "=== $ERRORS hata tespit edildi. Yedek: $BACKUP ==="
fi
