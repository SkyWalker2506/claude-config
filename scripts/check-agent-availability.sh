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

UNAVAILABLE_COUNT=0

# ---------------------------------------------------------------------------
# 1. free-gemini — OpenRouter API key + connectivity
# ---------------------------------------------------------------------------
check_free_gemini() {
  if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "UNAVAILABLE: free-gemini | OPENROUTER_API_KEY tanımlı değil | ~/.claude/secrets/secrets.env dosyasına OPENROUTER_API_KEY=... ekle | sonnet"
    return
  fi

  # Lightweight ping — modeller listesi (düşük token maliyet)
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    "https://openrouter.ai/api/v1/models" \
    --max-time 5 2>/dev/null || echo "000")

  if [ "$http_code" = "200" ]; then
    echo "AVAILABLE: free-gemini"
  elif [ "$http_code" = "401" ]; then
    echo "UNAVAILABLE: free-gemini | OPENROUTER_API_KEY geçersiz (401) | Geçerli bir API key al: openrouter.ai/keys | sonnet"
  else
    echo "UNAVAILABLE: free-gemini | OpenRouter ulaşılamıyor (HTTP $http_code) | İnternet bağlantısını kontrol et | sonnet"
  fi
}

# ---------------------------------------------------------------------------
# 2. local-qwen-9b — Ollama + model
# ---------------------------------------------------------------------------
check_local_qwen() {
  if ! command -v ollama &>/dev/null; then
    echo "UNAVAILABLE: local-qwen-9b | Ollama kurulu değil | brew install ollama && ollama pull qwen2.5:9b | haiku"
    return
  fi

  # Ollama servis çalışıyor mu?
  if ! ollama list &>/dev/null 2>&1; then
    echo "UNAVAILABLE: local-qwen-9b | Ollama servisi çalışmıyor | ollama serve & | haiku"
    return
  fi

  # Qwen modeli indirili mi?
  if ollama list 2>/dev/null | grep -qi "qwen"; then
    echo "AVAILABLE: local-qwen-9b"
  else
    echo "UNAVAILABLE: local-qwen-9b | qwen2.5:9b modeli indirilmemiş | ollama pull qwen2.5:9b | haiku"
  fi
}

# ---------------------------------------------------------------------------
# 3. free-web — fetch MCP erişilebilirlik (basit URL testi)
# ---------------------------------------------------------------------------
check_free_web() {
  # Basit connectivity testi
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
# 4. free-gpt — OpenRouter GPT-4o-mini (aynı key, farklı model)
# ---------------------------------------------------------------------------
check_free_gpt() {
  # OPENROUTER_API_KEY kontrolü free-gemini ile aynı
  if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "UNAVAILABLE: free-gpt | OPENROUTER_API_KEY tanımlı değil | ~/.claude/secrets/secrets.env dosyasına ekle | haiku"
    return
  fi
  # Key varsa OpenRouter ping zaten free-gemini'de yapıldı — available say
  echo "AVAILABLE: free-gpt"
}

# ---------------------------------------------------------------------------
# 5. free-script — Bash tool (her zaman mevcut Claude Code'da)
# ---------------------------------------------------------------------------
check_free_script() {
  echo "AVAILABLE: free-script"
}

# ---------------------------------------------------------------------------
# 6. free-deterministic — Bash tool (her zaman mevcut)
# ---------------------------------------------------------------------------
check_free_deterministic() {
  echo "AVAILABLE: free-deterministic"
}

# ---------------------------------------------------------------------------
# Çalıştır
# ---------------------------------------------------------------------------
check_free_gemini
check_local_qwen
check_free_web
check_free_gpt
check_free_script
check_free_deterministic

# ---------------------------------------------------------------------------
# Özet satırı
# ---------------------------------------------------------------------------
unavailable_list=$(grep "^UNAVAILABLE:" <<< "$(
  check_free_gemini
  check_local_qwen
  check_free_web
  check_free_script
  check_free_deterministic
)" 2>/dev/null | wc -l | tr -d ' ')

# (Özet sadece isteğe bağlı, yukarıdaki çıktı asıl veri kaynağı)
