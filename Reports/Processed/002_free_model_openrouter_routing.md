# Report 002 — Claude Code Free Model (OpenRouter) Çalışmıyor

> Date: 2026-04-07  
> Source: Kullanıcı debugging oturumu — ClaudeHQ workspace  
> Status: UNPROCESSED  
> Priority: Critical

---

## Context

Claude Code CLI'da OpenRouter üzerinden ücretsiz model (qwen/qwen3.6-plus:free) kullanılmak isteniyor. `.zshrc` fonksiyonları, `bin/claude`, `bin/_claude-env` düzenlendi; env var'lar (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`) doğru set ediliyor. Ancak Claude Code modeli hâlâ reddediyor.

---

## Root Cause Analysis

### Doğrulanan Gerçekler

| Test | Sonuç |
|------|-------|
| OpenRouter API key geçerli mi? | ✅ `secrets.env`'den yükleniyor, API çağrısı başarılı |
| Model ID doğru mu? | ✅ `qwen/qwen3.6-plus:free` — curl ile test edildi, çalışıyor |
| Env var'lar set ediliyor mu? | ✅ `_claude-env` source ediliyor, `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` doğru |
| `_claude_exec` fonksiyonu çalışıyor mu? | ✅ zsh ve bash'te test edildi, doğru args geçiyor |

### Kök Neden: Claude Code Client-Side Model Validation

```bash
# Bu komut doğrudan binary'ye gider — TÜM env var'lar doğru:
ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1" \
ANTHROPIC_AUTH_TOKEN="Bearer $OPENROUTER_API_KEY" \
/Users/musabkara/.local/bin/claude --model "qwen/qwen3.6-plus:free" -p "say hi" --max-turns 1

# Sonuç:
# "There's an issue with the selected model (qwen/qwen3.6-plus:free).
#  It may not exist or you may not have access to it."
```

**Claude Code, model ID'sini API'ye göndermeden ÖNCE kendi bilinen model listesine karşı doğruluyor.** Sadece Anthropic model ID'lerini (`claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5-*`) kabul ediyor. OpenRouter model ID'leri (`qwen/*`, `nvidia/*` vb.) bu listede olmadığı için reddediliyor.

Bu, env var'larla veya shell wrapper'larla çözülebilecek bir sorun **değil**. Claude Code binary'sinin davranışı.

---

## Identified Issues

### 1. Claude Code Arbitrary Model ID Desteklemiyor

**Problem:** `--model` flag'i ve `ANTHROPIC_MODEL` env var'ı sadece Anthropic model ID'lerini kabul ediyor. Custom `ANTHROPIC_BASE_URL` set edilmiş olsa bile non-Anthropic model ID'leri client-side reddediliyor.

**Impact:** OpenRouter free modelleri Claude Code CLI ile kullanılamaz.

### 2. `.zshrc` + `_claude-env` Gereksiz Karmaşıklaştı

**Problem:** Çalışmayan bir routing mantığı için `.zshrc`, `bin/claude`, `bin/_claude-env` üçü de değiştirildi. Eski çalışan düzen bozuldu.

**Impact:** Mevcut `cl`, `clhq`, `claude-paid`, `m1/m2/m3` komutları da etkilenmiş olabilir.

---

## Çözüm Seçenekleri

### Seçenek A: OpenRouter + Anthropic Model ID (Ücretli ama ucuz)

OpenRouter üzerinden Anthropic modellerini proxy olarak kullan. Claude Code model ID'yi kabul eder çünkü Anthropic ID'si. OpenRouter, Anthropic API'ye yönlendirir.

```bash
ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1" \
ANTHROPIC_AUTH_TOKEN="Bearer $OPENROUTER_API_KEY" \
claude --model claude-sonnet-4-6
```

- **Pro:** Çalışır, ek client gerekmez
- **Con:** Free değil — OpenRouter Anthropic modelleri için ücret alır
- **Maliyet:** ~$3/M input, $15/M output (Sonnet 4.6 via OpenRouter)

### Seçenek B: Claude Code `--model` Bypass (Gelecek özellik)

Claude Code'un `ANTHROPIC_MODEL` env var'ını client-side validation yapmadan kabul etmesini bekle. Bu bir feature request olarak açılabilir:
- GitHub: `anthropics/claude-code` — "Support arbitrary model IDs with custom ANTHROPIC_BASE_URL"

### Seçenek C: Farklı Client Kullan (Free modeller için)

Free model kullanımı için Claude Code yerine OpenRouter-uyumlu başka bir client:

| Client | Açıklama | Free model desteği |
|--------|----------|-------------------|
| `aider` | CLI coding assistant | ✅ `--model openrouter/qwen/qwen3.6-plus:free` |
| `opencode` | Zaten kurulu (claude-local) | ✅ Ollama + OpenRouter |
| `continue.dev` | VS Code extension | ✅ OpenRouter provider |
| `cursor` | IDE | ✅ Custom API endpoint |

### Seçenek D: Hybrid — Free için Aider, Paid için Claude Code

```bash
# .zshrc
alias cf="aider --model openrouter/qwen/qwen3.6-plus:free"  # free coding
alias cl="claude"                                             # paid Claude
```

- **Pro:** Her iki dünyanın en iyisi — free model + Claude Code özellikleri
- **Con:** İki farklı tool, farklı config, farklı CLAUDE.md desteği

---

## Required Actions Summary

| # | Dosya | Değişiklik | Öncelik |
|---|-------|-----------|---------|
| 1 | `~/.zshrc` | OpenRouter routing'i geri al, eski çalışan düzene dön | Critical |
| 2 | `bin/_claude-env` | Sil veya sadece secrets loader olarak sadeleştir | Critical |
| 3 | `bin/claude` | Eski haline döndür (OpenRouter routing olmadan) | Critical |
| 4 | Karar | Seçenek A/C/D arasında karar ver | High |
| 5 | `bin/claude-free` | Silindi — karardan sonra gerekirse yeniden oluştur | Medium |

---

## Notes

- `curl` ile doğrudan OpenRouter API'ye istek atıldığında `qwen/qwen3.6-plus:free` **çalışıyor**. Sorun API tarafında değil, Claude Code client'ında.
- Claude Code v2.1.92 test edildi. Gelecek sürümlerde `--model` validation'ı değişebilir.
- Bu konu `anthropics/claude-code` repo'sunda issue olarak açılabilir.
