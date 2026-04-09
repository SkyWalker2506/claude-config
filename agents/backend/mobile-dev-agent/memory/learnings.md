# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | VocabApp Tech Stack | opus
- Flutter SDK ^3.11.3, Dart SDK ^3.11.3
- Firebase: core, auth, firestore, database, messaging, storage
- State: flutter_riverpod 3.3.1
- Offline-first: Hive (encrypted) for local storage, Firestore for sync
- Platform features: TTS (tts_provider), STT (stt_provider), haptics
- M3 enabled: `useMaterial3: true`, `ColorScheme.fromSeed()` — need NavigationBar, FilledButton migration
