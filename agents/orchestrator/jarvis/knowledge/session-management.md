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
free (Groq) → local (Ollama) → haiku → sonnet
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

### External Agent Dispatch Best Practices

When using Codex CLI or Gemini CLI as execution backends:

**Codex CLI (GPT 5.4):**
- Sandbox: workspace-write only — no git, no network
- Max single-task scope: ~300 lines of file changes
- Always verify output files after task completion
- Commit changes yourself after verifying
- Use stdin for prompts: `cat prompt.md | codex exec --model gpt-5.4 --full-auto -`

**Gemini CLI:**
- Full filesystem access (no sandbox)
- Can run git commands
- Better for large refactoring tasks
- Use for tasks requiring network access

**General Rules:**
- Don't ask external agents to commit — do it yourself
- Break 500+ line tasks into 300-line chunks
- Kill processes stuck >15 minutes
- Check file modification timestamps after task completion
