---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Gamification UX Psychology

## Streak Mechanics
- **Loss aversion** drives streak retention (losing a 30-day streak hurts)
- Visual: flame icon + counter, color intensity scales with length
- Freeze mechanic: 1 free freeze / streak length milestone
- Streak recovery: allow 1-day grace period to reduce frustration
- VocabApp has `StreakChip` widget — enhance with animation on increment

## XP (Experience Points)
- Immediate feedback: XP counter animates on earn
- Sources: quiz correct (+10), daily goal (+50), streak bonus (+5/day)
- Level thresholds: exponential curve (100, 250, 500, 1000...)
- Show XP in profile header + session summary

## Achievements / Badges
- Categories: milestone (100 words), skill (perfect quiz), habit (7-day streak)
- Locked state: show silhouette + progress bar
- Unlock animation: scale + particle burst + haptic
- VocabApp has `badge_provider.dart` and `achievements_page.dart`
- Display: grid with progress, not just earned badges

## Leaderboard
- **Social comparison** motivates competitive users
- Weekly reset: prevents insurmountable gaps
- Show user's rank + 2 above/below (relative positioning)
- Friend leaderboard > global (reduces intimidation)
- VocabApp has `challenge_*` pages — integrate leaderboard widget

## Session Rewards
- End-of-session summary: words learned, accuracy, XP earned, streak
- **Variable reward** > fixed (random bonus XP, surprise badge)
- Progress toward next milestone shown
- Share card for social proof (VocabApp has `shareable_result_card.dart`)

## Engagement Anti-Patterns to Avoid
- Dark patterns: guilt-tripping streak loss notifications
- Pay-to-win: premium users shouldn't dominate leaderboards
- Notification spam: max 1 push/day for streak reminder
- Grinding: XP should reward quality (accuracy) not just volume

## Design Principles
1. **Autonomy**: let users set daily goals
2. **Mastery**: show skill progression, not just points
3. **Purpose**: connect XP to actual vocabulary growth
4. **Fairness**: normalize leaderboard by time spent
