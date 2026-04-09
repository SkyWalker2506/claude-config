# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | VocabApp Analysis | opus
- VocabApp uses M3 with `ColorScheme.fromSeed()` and custom `AppColors` for semantic colors (success, star)
- App has gamification: streak, badges, challenges, leaderboard, XP — all provider-based (Riverpod)
- Accessibility: `animDuration()` helper respects reduce-motion; `AppColors` has WCAG contrast docs
- Competitors to benchmark: Duolingo (gamification), Anki (SRS), Quizlet (flashcard UX), Drops (visual)
- Design overhaul targets: bottom nav, M3 tokens, page transitions, 3D flip, accessibility improvements
