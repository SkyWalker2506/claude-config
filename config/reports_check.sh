#!/bin/bash
# reports_check.sh — Robust unprocessed reports detection
# Hook: SessionStart — runs once per session
# Self-heals missing dirs/files, detects state, sorts by priority

set -euo pipefail

REPORTS_DIR="$HOME/Projects/claude-config/Reports"
PROCESSED_DIR="$REPORTS_DIR/Processed"
SUMMARY_FILE="$REPORTS_DIR/REPORTS_SUMMARY.md"

# ---------------------------------------------------------------------------
# 1. Self-heal directories
# ---------------------------------------------------------------------------
mkdir -p "$REPORTS_DIR" 2>/dev/null || true
mkdir -p "$PROCESSED_DIR" 2>/dev/null || true

# ---------------------------------------------------------------------------
# 2. Self-heal REPORTS_SUMMARY.md
# ---------------------------------------------------------------------------
if [ ! -f "$SUMMARY_FILE" ]; then
  cat > "$SUMMARY_FILE" << 'TMPL'
# Reports Summary

> Her rapor işlenince buraya özet eklenir. İşlenen dosya `Processed/` klasörüne taşınır.

## Sistem

- `Reports/` → İşlenmemiş raporlar burada bekler
- `Reports/Processed/` → İşlenen raporlar buraya taşınır
- `REPORTS_SUMMARY.md` → Bu dosya, tüm raporların özeti

## Startup Kuralı (Claude için)

Her oturum başında:
1. `Reports/` klasörünü tara — `REPORTS_SUMMARY.md`, `TEMPLATE.md` ve `Processed/` dışında dosya var mı?
2. Varsa → raporu oku, içindeki aksiyonları uygula, özeti buraya ekle, dosyayı `Processed/` klasörüne taşı
3. Yoksa → devam et

---

## İşlenen Raporlar

| # | Dosya | Tarih | Öncelik | Özet |
|---|-------|-------|---------|------|
TMPL
fi

# ---------------------------------------------------------------------------
# 3. Scan reports — parse frontmatter (Status, Priority)
# ---------------------------------------------------------------------------
# Priority sort order: CRITICAL=1, HIGH=2, MEDIUM=3, LOW=4, (none)=5
priority_rank() {
  case "$(echo "$1" | tr '[:lower:]' '[:upper:]')" in
    CRITICAL) echo 1 ;;
    HIGH)     echo 2 ;;
    MEDIUM)   echo 3 ;;
    LOW)      echo 4 ;;
    *)        echo 5 ;;
  esac
}

# Parallel arrays for results
unprocessed_files=()
unprocessed_priorities=()
unprocessed_ranks=()
stale_files=()
stale_ages=()

for filepath in "$REPORTS_DIR"/*.md; do
  # Skip glob that matched nothing (no .md files)
  [ -e "$filepath" ] || continue
  # Must be a regular file
  [ -f "$filepath" ] || continue

  filename="$(basename "$filepath")"

  # Skip meta files
  case "$filename" in
    REPORTS_SUMMARY.md|TEMPLATE.md) continue ;;
  esac

  # --- Parse frontmatter (first 10 lines) ---
  status=""
  priority=""
  head_lines="$(head -n 10 "$filepath" 2>/dev/null || true)"

  while IFS= read -r line; do
    # Match Status/Priority — handles both "Status: X" and "> Status: X" (blockquote frontmatter)
    stripped="${line#> }"
    if [[ "$stripped" =~ ^[Ss]tatus:[[:space:]]*(.*) ]]; then
      status="$(echo "${BASH_REMATCH[1]}" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')"
    fi
    if [[ "$stripped" =~ ^[Pp]riority:[[:space:]]*(.*) ]]; then
      priority="$(echo "${BASH_REMATCH[1]}" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')"
    fi
  done <<< "$head_lines"

  # --- Categorize ---
  # DONE → already processed, skip
  if [ "$status" = "DONE" ]; then
    continue
  fi

  # IN_PROGRESS → check if stale (mtime > 30 min)
  if [ "$status" = "IN_PROGRESS" ]; then
    # Get file mtime in seconds since epoch
    if [[ "$(uname)" == "Darwin" ]]; then
      file_mtime="$(stat -f '%m' "$filepath" 2>/dev/null || echo 0)"
    else
      file_mtime="$(stat -c '%Y' "$filepath" 2>/dev/null || echo 0)"
    fi
    now="$(date +%s)"
    age_seconds=$(( now - file_mtime ))
    age_minutes=$(( age_seconds / 60 ))

    if [ "$age_minutes" -ge 30 ]; then
      # Stale IN_PROGRESS — previous session likely crashed
      stale_files+=("$filename")
      stale_ages+=("$age_minutes")
      continue
    fi

    # Fresh IN_PROGRESS — another session is handling it, skip
    continue
  fi

  # UNPROCESSED, or no Status line at all → needs processing
  rank="$(priority_rank "$priority")"
  unprocessed_files+=("$filename")
  unprocessed_priorities+=("$priority")
  unprocessed_ranks+=("$rank")
done

# ---------------------------------------------------------------------------
# 4. Sort unprocessed by priority rank (selection sort — fine for small N)
# ---------------------------------------------------------------------------
count=${#unprocessed_files[@]}
if [ "$count" -gt 1 ]; then
  for (( i=0; i<count-1; i++ )); do
    min=$i
    for (( j=i+1; j<count; j++ )); do
      if [ "${unprocessed_ranks[$j]}" -lt "${unprocessed_ranks[$min]}" ]; then
        min=$j
      fi
    done
    if [ "$min" -ne "$i" ]; then
      # Swap all parallel arrays
      tmp="${unprocessed_files[$i]}"
      unprocessed_files[$i]="${unprocessed_files[$min]}"
      unprocessed_files[$min]="$tmp"

      tmp="${unprocessed_priorities[$i]}"
      unprocessed_priorities[$i]="${unprocessed_priorities[$min]}"
      unprocessed_priorities[$min]="$tmp"

      tmp="${unprocessed_ranks[$i]}"
      unprocessed_ranks[$i]="${unprocessed_ranks[$min]}"
      unprocessed_ranks[$min]="$tmp"
    fi
  done
fi

# ---------------------------------------------------------------------------
# 5. Output stale IN_PROGRESS signal
# ---------------------------------------------------------------------------
stale_count=${#stale_files[@]}
if [ "$stale_count" -gt 0 ]; then
  echo "REPORTS_STALE: $stale_count rapor IN_PROGRESS ama 30dk+ güncellenmemiş (muhtemelen önceki oturum crash oldu):"
  for (( i=0; i<stale_count; i++ )); do
    echo "  • ${stale_files[$i]} (${stale_ages[$i]} dk önce başlamış)"
  done
  echo "CLAUDE_ACTION: Status'ü kontrol et, UNPROCESSED'a geri çevir veya kaldığı yerden devam et."
fi

# ---------------------------------------------------------------------------
# 6. Output unprocessed signal (max 5 listed for token budget)
# ---------------------------------------------------------------------------
if [ "$count" -gt 0 ]; then
  # Add blank line separator if stale signal was also printed
  if [ "$stale_count" -gt 0 ]; then
    echo ""
  fi

  echo "REPORTS_PENDING: $count işlenmemiş rapor var:"

  max_display=5
  display=$(( count < max_display ? count : max_display ))

  for (( i=0; i<display; i++ )); do
    pri="${unprocessed_priorities[$i]}"
    if [ -n "$pri" ]; then
      label="[$pri]"
    else
      label="[—]"
    fi
    echo "  • $label ${unprocessed_files[$i]}"
  done

  if [ "$count" -gt "$max_display" ]; then
    remaining=$(( count - max_display ))
    echo "  (+ $remaining more)"
  fi

  echo "CLAUDE_ACTION: Raporları oku, aksiyonları claude-config'e uygula, REPORTS_SUMMARY.md'ye özet ekle, dosyayı Processed/ klasörüne taşı. Bitince kullanıcıya 'X rapor işlendi, yapı güncellendi' de. Gerekirse 'Claude'u kapat-aç' uyarısı ver."
fi
