#!/bin/bash
# check-agent-availability.sh — /project-analysis öncesi agent erişilebilirlik kontrolü
# Kullanım: ./scripts/check-agent-availability.sh
# Çıktı formatı:
#   AVAILABLE: <model_tipi>
#   UNAVAILABLE: <model_tipi> | <neden> | <kurulum_talimatı> | <fallback>

set -euo pipefail

# --- Secrets yükle ---
SECRETS_FILE="$HOME/.claude/secrets/secrets.env"
if [ -f "$SECRETS_FILE" ]; then
  # shellcheck disable=SC1090
  source "$SECRETS_FILE" 2>/dev/null || true
fi

# ---------------------------------------------------------------------------
# 1. gpt-5.4 — OpenRouter API key + connectivity (primary model for most agents)
# ---------------------------------------------------------------------------
check_gpt54() {
  if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "UNAVAILABLE: gpt-5.4 | OPENROUTER_API_KEY tanımlı değil | ~/.claude/secrets/secrets.env dosyasına OPENROUTER_API_KEY=... ekle | sonnet"
    return
  fi

  # Lightweight ping — modeller listesi (düşük token maliyet)
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    "https://openrouter.ai/api/v1/models" \
    --max-time 5 2>/dev/null || echo "000")

  if [ "$http_code" = "200" ]; then
    echo "AVAILABLE: gpt-5.4"
  elif [ "$http_code" = "401" ]; then
    echo "UNAVAILABLE: gpt-5.4 | OPENROUTER_API_KEY geçersiz (401) | Geçerli bir API key al: openrouter.ai/keys | sonnet"
  else
    echo "UNAVAILABLE: gpt-5.4 | OpenRouter ulaşılamıyor (HTTP $http_code) | İnternet bağlantısını kontrol et | sonnet"
  fi
}

# ---------------------------------------------------------------------------
# 2. gpt-5.4-mini — Same OpenRouter key, lighter model
# ---------------------------------------------------------------------------
check_gpt54_mini() {
  # Same key as gpt-5.4 — if key exists, mini is also available
  if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "UNAVAILABLE: gpt-5.4-mini | OPENROUTER_API_KEY tanımlı değil | ~/.claude/secrets/secrets.env dosyasına ekle | haiku"
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
# 4. Claude Code native models (opus, sonnet, haiku — always available)
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
