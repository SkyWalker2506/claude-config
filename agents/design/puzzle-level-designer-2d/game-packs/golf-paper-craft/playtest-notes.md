# Playtesting notes — Golf Paper Craft

## Practical plan (no backend analytics)
- Track per-level `avg_attempts` (10 self-runs + 3 cold players minimum)
- Track `time_to_solve` (seconds)
- Track `quit_after_level` proxy: ask cold player “would you continue?” (yes/no/maybe)
- Record win replays (video) to detect “dead drop” luck solves

## Break thresholds (Golf-specific)
- `avg_attempts > 12` → level not shippable (except boss)
- Tutorial L1–L3: if cold player doesn’t pass on first try → re-teach the mechanic
- `time_to_solve > 150s` on mid-level → readability patch
- Win replay tolerance > 1.5× → “luck solve” risk → sharpen constraints

## Boss (L18) targets
- Target `fail_rate`: 65–72%
- Target `avg_attempts`: 10–14
- Boss `quit_after_level` up to ~40% can be “closure quit” (healthy)

## Golden run
L1→L18 in one session should be < 25 minutes; over suggests pacing problem, under suggests game too short.

