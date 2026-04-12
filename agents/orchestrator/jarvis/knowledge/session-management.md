---
last_updated: 2026-04-12
refined_by: opus
confidence: high
---

# Session Management

## Session Baslangic Kontrolleri

1. **CLAUDE.md oku** — proje kurallari
2. **Hook sinyallerini isle:**
   | Sinyal | Aksiyon |
   |--------|---------|
   | MIGRATION_NEEDED | /migration calistir |
   | INDEX_ASK | Kullaniciya sor, onaylarsa indexle |
   | INDEX_UPDATE | Sessizce guncelle |
   | SECRETS_MISSING | Kullaniciya bildir |
   | INSTALL_NEEDED | install.sh calistir |
3. **AVAILABLE_SECRETS kontrol** — hangi servislere erisim var
4. **MCP listesi kontrol** — kullanilmayanlari kapat
5. **knowledge/_index.md oku** — ilgili bilgileri yukle
6. **projects.json oku** (ClaudeHQ'daysa)

## Context Yonetimi
- **%60 doluluk** → /compact yap
- **%95** → otomatik compact
- **Konu degisimi** → /clear
- **5dk+ mola oncesi** → /compact (prompt cache sifirlanir)
- **Buyuk dosya (>20KB)** → Sonnet'te oku/yaz
- **Terminal cikti** → head -N ile sinirla

## Model Secim Kurallari
```
free (OpenRouter) → free (Groq) → local (Ollama) → haiku → sonnet
```
- Sormadan ucretli baslatma
- Ucretli gecis icin kullaniciya sor
- Sub-agent default: haiku veya free

## Kota Yonetimi
| Kalan | Mod |
|-------|-----|
| ≥10% | Normal — Opus karar, Sonnet kod, Haiku trivial |
| 5-10% | Tasarruf — Opus sadece kritik |
| <5% | Kritik — Sonnet + Haiku only |
| <1% | Sonnet-only |

## Raporlama
- Is bitince kisa ozet ver
- Commit/PR gerekiyorsa hazirla
- Onemli kararlari memory/sessions.md'ye kaydet
- Agent'a aktarilacak bilgi varsa not al
