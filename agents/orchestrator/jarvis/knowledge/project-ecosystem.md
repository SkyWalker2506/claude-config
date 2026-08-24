---
last_updated: 2026-04-12
refined_by: opus
confidence: high
---

# Project Ecosystem

## Aktif Projeler (projects.json'dan)

| Proje | Tech Stack | Durum |
|-------|-----------|-------|
| VocabLearningApp | Flutter/Dart, Firebase, Riverpod | Aktif — Sprint 3 UX overhaul |
| ClaudeHQ | Shell, JSON, Markdown | Aktif — cross-project workspace |
| claude-config | Shell, JSON, Markdown | Aktif — config + agent sistemi |
| ByteCraftHQ | Flutter | Aktif |
| Viralyze | Flutter | Aktif |
| CoinHQ | Flutter | Aktif |
| Gardirop | Flutter | Aktif |
| ProjeBirlik | Flutter | Aktif |
| KnightOnlineAI | Unity/C# | Aktif |
| trading-bot | Python | Aktif |
| football-ai-platform | — | Flutter | Aktif |
| transcriptr | Flutter | Aktif |
| 3d-asset-foundry | — | Python, Blender, multi-LLM (Claude/Gemini/OpenAI/Ollama), refinement loop | Aktif — Phase 0 scaffold (ARCHITECTURE v0.10, STRUCTURE v0.10) |

## 3d-asset-foundry Notlari
- **Mimari:** Intent layer → AI agents → Comparison engine → Learning/refinement loop → Blender tool runner
- **Kritik guvenlik sinir:** §4.6 reference_vault yalitimi; sadece `comparison/vault_reader.py` erisebilir
- **Phase 0 blockers:** `vault_token.py`, comparison dekompozisyonu (aggregator/vault_reader/escalation), `schema_repair.py`, schema split, 7 invariant test
- **Dil/stack:** Python 3, pyproject.toml, pytest, Blender subprocess (lifecycle.py §14.6)
- **Drift report kaynak:** ARCHITECTURE.md §15.0/§15.3/§20.5 ve STRUCTURE.md knowledge-first tree
- **Dispatch rotasi:** Python/3D pipeline satiri — §agent-dispatch-rules

## Claude Ecosystem
| Proje | Amac |
|-------|------|
| claude-config | Tum Claude ayarlari, agent'lar, skill'ler, hook'lar |
| claude-marketplace | Plugin marketplace |
| claude-design-system | Design system |
| claude-agent-catalog | Agent katalogu |
| ccplugin-* (15+) | Claude Code plugin'leri |
| craft-unity | Unity + Claude entegrasyonu |

## Ortak Ozellikler
- Cogu proje Flutter/Dart (mobil ekosistem)
- Python istisna: 3d-asset-foundry, trading-bot
- Unity istisna: KnightOnlineAI, craft-unity
- Firebase yaygin (Auth, Firestore, FCM)
- Riverpod state management standart (Flutter tarafi)
- Material 3 tema sistemi
- Sprint yonetimi local sprint dosyalari ile
- Conventional commit + PR workflow
