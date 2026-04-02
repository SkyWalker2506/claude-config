---
name: opencode
description: "OpenCode terminal asistani — Ollama ile ucretsiz lokal modeller. Triggers: opencode, open code, lokal model, kota bitti."
user-invocable: true
---

# OpenCode — Ucretsiz (lokal) kod asistani

Claude kotasi bittiginde veya API kullanmadan **OpenCode** + **Ollama** ile devam et.

OpenCode, Claude Code’dan bagimsiz bir CLI/TUI aracidir. Bu skill, `claude-config` kurulumunun yazdigi `~/.config/opencode/opencode.json` ile **yalnizca Ollama** (lokal, ucretsiz) kullanmayi hedefler.

## Oncelik sirasi

1. **Ollama** calisiyor mu: `ollama --version`
2. Model cekilmis mi: `ollama list` — yoksa asagidaki gibi cek
3. **OpenCode** CLI: `opencode --version` — yoksa `npm install -g opencode-ai` (npm paket adi: `opencode-ai`, binary: `opencode`)

## Hizli baslangic

```bash
# 1) Ollama: https://ollama.com — sonra ornek model
ollama pull qwen2.5-coder:7b

# 2) Proje dizininde ac
cd ~/Projects/SeninProje
opencode
```

TUI icinde model degistirmek: `/models`

## Yapilandirma

- Global dosya: `~/.config/opencode/opencode.json` (install.sh ilk kurulumda sablon kopyalar; yoksa manuel kopyala: `claude-config/templates/opencode-ollama.json`)
- Sadece lokal kullanmak icin `enabled_providers: ["ollama"]` kullanilir; boylesce Anthropic/OpenAI anahtarlari otomatik yuklenmez.

## Baska Ollama modeli secmek

1. `ollama pull <model>` (ornek: `deepseek-coder-v2:16b`, `codellama`)
2. `~/.config/opencode/opencode.json` icinde:
   - `provider.ollama.models` altina yeni anahtar ekle
   - `model` ve `small_model` degerini `ollama/<ollama-model-adi>` yap

Arac cagrilarinda sorun yasarsan Ollama’daki baglami artir (OpenCode dokumanlari: `num_ctx` ~ 16k–32k).

## claude-config ile senkron

Repoda degisiklik yaptiysan: `cd ~/Projects/claude-config && ./install.sh`

Opsiyonel CLI kurulumu ile: `./install.sh --opencode`

## Not

Ucretsiz bulut API’leri (ornekle sinirli tier’ler) OpenCode’da ayri provider ile mumkun; bu sablon yalnizca **tamamen lokal / ucretsiz** Ollama yolunu sabitler.
