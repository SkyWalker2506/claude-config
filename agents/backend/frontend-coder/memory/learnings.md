# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | VocabApp Architecture Analysis | opus
- Structure: `lib/core/` (theme, config, services), `lib/presentation/` (pages, widgets, providers), `lib/domain/`, `lib/data/`
- State: Riverpod 3.x (flutter_riverpod), providers in `presentation/providers/` — gamification, quiz, SRS, etc.
- 20+ pages, 20+ widgets — well-separated dumb/smart components
- Widgets: `word_card.dart`, `streak_chip.dart`, `flash_card_view.dart`, `empty_state_widget.dart`
- Pages: quiz variants (progressive, voice, time attack, challenge), home, achievements, favorites
