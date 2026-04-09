# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | VocabApp Motion Analysis | opus
- VocabApp has `animDuration()` in `core/utils/anim_duration.dart` — returns Duration.zero when reduce-motion active
- Existing animated widgets: `flash_card_view.dart` (flip), `streak_chip.dart`, `level_progress_bar.dart`
- Missing: M3 page transitions (container transform, shared axis, fade through), staggered list entrance
- 3D card flip needs perspective transform with Matrix4 — existing flash_card_view needs enhancement
- Haptic pairing not yet implemented — quiz feedback should use HapticFeedback API
