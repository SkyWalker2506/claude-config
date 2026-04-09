---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Cross-Project Patterns

## Ortak Tech Stack
- **Frontend:** Flutter 3.x + Dart
- **State:** Riverpod 3.x (provider types: Provider, StateNotifier, AsyncNotifier, FutureProvider)
- **Backend:** Firebase (Auth, Firestore, FCM, Analytics)
- **Theme:** Material 3, ColorScheme.fromSeed, useMaterial3: true
- **Testing:** flutter_test, integration_test, mockito

## Ortak Kurallar (Tum Projeler)

### Git
- Conventional commit: feat:, fix:, refactor:, chore: (Ingilizce)
- 1-3 dosya → main'e direkt; 4+ dosya → feature branch + PR
- CI degisikligi → her zaman PR
- Force push → ASLA sormadan

### Dosya Yapisi
- lib/core/ — constants, utils, theme
- lib/data/ — models, repositories, services
- lib/presentation/ — pages, widgets, providers
- lib/l10n/ — localization

### Guvenlik
- .env ASLA commit'e girmesin
- Secrets → claude-secrets repo (private)
- Firebase rules → test et
- KVKK/guvenlik → kullaniciya sor

## Ecosystem Sync
Agent/plugin/skill degisikligi yapildiginda:
1. `hq sync` calistir
2. README'leri guncelle
3. Ilgili repo'larda commit

## Jira Ortak Kurallar
- Koda baslamadan In Progress (transition 21)
- Alt gorevler bitmeden ana gorevi Done yapma
- Bekleyen is → WAITING (7)
- IP'de bekletme yok — ya tamamla ya WAITING
