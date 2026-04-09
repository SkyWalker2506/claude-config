---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Project Ecosystem

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## Aktif Projeler (projects.json'dan)

| Proje | Jira | Tech Stack | Durum |
|-------|------|-----------|-------|
| VocabLearningApp | VOC | Flutter/Dart, Firebase, Riverpod | Aktif — Sprint 3 UX overhaul |
| ClaudeHQ | CHQ | Shell, JSON, Markdown | Aktif — cross-project workspace |
| claude-config | CC | Shell, JSON, Markdown | Aktif — config + agent sistemi |
| ByteCraftHQ | BYT | Flutter | Aktif |
| Viralyze | VIR | Flutter | Aktif |
| CoinHQ | COIN | Flutter | Aktif |
| Gardirop | GARD | Flutter | Aktif |
| ProjeBirlik | PROJ | Flutter | Aktif |
| KnightOnlineAI | KOAI | Unity/C# | Aktif |
| trading-bot | TB | Python | Aktif |
| football-ai-platform | — | Flutter | Aktif |
| transcriptr | TSCR | Flutter | Aktif |

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
- Cogu proje Flutter/Dart
- Firebase yaygin (Auth, Firestore, FCM)
- Riverpod state management standart
- Material 3 tema sistemi
- Jira ile sprint yonetimi
- Conventional commit + PR workflow
