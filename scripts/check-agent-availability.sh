#!/bin/bash
# check-agent-availability.sh — /project-analysis öncesi agent erişilebilirlik kontrolü
# Kullanım: ./scripts/check-agent-availability.sh
# Çıktı formatı:
#   AVAILABLE: <model_tipi>
#   UNAVAILABLE: <model_tipi> | <neden> | <kurulum_talimatı> | <fallback>

set -euo pipefail

# ---------------------------------------------------------------------------
# 1. gpt-5.4 — Codex CLI availability
# ---------------------------------------------------------------------------
check_gpt54() {
  if ! command -v codex &>/dev/null; then
    echo "UNAVAILABLE: gpt-5.4 | codex CLI bulunamadı | npm install -g @openai/codex çalıştır | sonnet"
    return
  fi

  login_status=$(codex ls 2>&1 | grep -v 'Not logged in' | grep -q . && echo "logged_in" || echo "not_logged_in")
  if [ "$login_status" = "logged_in" ]; then
    echo "AVAILABLE: gpt-5.4"
  else
    echo "UNAVAILABLE: gpt-5.4 | Codex CLI giriş yapılmamış | codex login çalıştır | sonnet"
  fi
}

# ---------------------------------------------------------------------------
# 2. gpt-5.4-mini — Same Codex CLI
# ---------------------------------------------------------------------------
check_gpt54_mini() {
  if ! command -v codex &>/dev/null; then
    echo "UNAVAILABLE: gpt-5.4-mini | codex CLI bulunamadı | npm install -g @openai/codex çalıştır | haiku"
    return
  fi
  echo "AVAILABLE: gpt-5.4-mini"
}

# ---------------------------------------------------------------------------
# 3. free-web — fetch MCP erişilebilirlik (basit URL testi)
# ---------------------------------------------------------------------------
check_free_web() {
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://www.google.com" \
    --max-time 5 2>/dev/null || echo "000")

  if [ "$http_code" = "200" ] || [ "$http_code" = "301" ] || [ "$http_code" = "302" ]; then
    echo "AVAILABLE: free-web"
  else
    echo "UNAVAILABLE: free-web | İnternet bağlantısı yok (HTTP $http_code) | Ağ bağlantısını kontrol et | haiku"
  fi
}

# ---------------------------------------------------------------------------
# 4. Claude Code native models (opus, sonnet, haiku — always available via Max subscription)
# ---------------------------------------------------------------------------
check_claude_native() {
  echo "AVAILABLE: opus"
  echo "AVAILABLE: sonnet"
  echo "AVAILABLE: haiku"
}

# ---------------------------------------------------------------------------
# Çalıştır
# ---------------------------------------------------------------------------
check_gpt54
check_gpt54_mini
check_free_web
check_claude_native
