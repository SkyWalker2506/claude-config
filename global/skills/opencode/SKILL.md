---
name: opencode
description: "OpenCode terminal asistani — OpenCode Zen (opencode.ai) ucretsiz/web modeller + Ollama lokal. Triggers: opencode, open code, zen, kota bitti."
user-invocable: true
---

# OpenCode — Zen (web) + Ollama (lokal)

[OpenCode](https://opencode.ai/) terminal/IDE/desktop icin acik kaynak kod asistani. Claude kotasi bitince veya ek model yolu olarak kullan.

Bu repodaki sablon: **`opencode`** saglayicisi (OpenCode Zen, bulut) + **`ollama`** (ucretsiz, makinede). Ayrinti: [Zen dokumanlari](https://open-code.ai/docs/en/zen), [Providers](https://open-code.ai/docs/en/providers).

## Durum (claude-config)

- Sablon: `claude-config/templates/opencode.json` → `install.sh` ilk calistirmada `~/.config/opencode/opencode.json` **yoksa** kopyalar (mevcut dosyayi ezmez).
- CLI: `npm install -g opencode-ai` veya `./install.sh --opencode`
- Kimlik bilgisi: Zen icin `/connect` → `opencode` → [opencode.ai/auth](https://opencode.ai/auth) uzerinden API anahtari (OpenCode’un sakladigi yer: `~/.local/share/opencode/auth.json`).

## 1) OpenCode Zen — ucretsiz (sinirli sure / kosullu) web modelleri

Zen, OpenCode ekibinin [test ettigi modeller](https://open-code.ai/docs/en/zen) listesi; **ucretsiz** olanlara ornekler (fiyatlandirma tablosuna gore; promosyonlar degisebilir):

| Model ID (Zen) | Not |
|----------------|-----|
| `opencode/gpt-5-nano` | Ucretsiz (tablo) |
| `opencode/minimax-m2.1-free` | Ucretsiz, sinirli sure |
| `opencode/glm-4.7-free` | Ucretsiz, sinirli sure |
| `opencode/kimi-k2.5-free` | Ucretsiz, sinirli sure |
| `opencode/big-pickle` | Ucretsiz, sinirli sure |

**Uyari:** Ucretsiz Zen modellerinin bir kisminda gizlilik notu: gelistirme icin veri toplanabilir. Tam liste ve guncel fiyat: [Zen — Pricing & Privacy](https://open-code.ai/docs/en/zen).

### Akis

1. `opencode` ac
2. `/connect` → **opencode** sec → [opencode.ai/auth](https://opencode.ai/auth) ile anahtar yapistir
3. `/models` ile model sec (ornek: `opencode/gpt-5-nano`)

Varsayilan sablon `model` / `small_model`: `opencode/gpt-5-nano`. Anahtar yoksa once `/connect` yap veya `/models` ile `ollama/...` sec.

## 2) Ollama — tamamen lokal, API anahtari yok

```bash
ollama pull qwen2.5-coder:7b
cd ~/Projects/SeninProje && opencode
```

TUI: `/models` → `ollama/qwen2.5-coder:7b`

## Yapilandirma dosyalari

- Global: `~/.config/opencode/opencode.json`
- Kaynak sablon: `~/Projects/claude-config/templates/opencode.json`
- `enabled_providers`: `["opencode","ollama"]` — sadece lokal istiyorsan `["ollama"]` yap

## claude-config senkron

```bash
cd ~/Projects/claude-config && ./install.sh
```

Opsiyonel CLI: `./install.sh --opencode`
