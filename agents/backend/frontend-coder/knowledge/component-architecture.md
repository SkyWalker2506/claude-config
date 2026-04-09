---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Component Architecture

## Atomic Design (Adapted for Flutter)
| Level | Flutter | VocabApp Examples |
|-------|---------|------------------|
| Atom | Single widget | `StreakChip`, `LevelProgressBar` |
| Molecule | Widget group | `WordCard`, `QuizAnswerButton` |
| Organism | Section | `QuizQuestionCard`, `LeaderboardList` |
| Template | Page layout | `QuizPageLayout`, `HomePageLayout` |
| Page | Full page + data | `HomePage`, `QuizPage` |

## Smart / Dumb Separation
```dart
// DUMB (presentation only) — in widgets/
class ScoreDisplay extends StatelessWidget {
  const ScoreDisplay({required this.score, required this.total, super.key});
  final int score;
  final int total;

  @override
  Widget build(BuildContext context) {
    return Text('$score / $total', style: Theme.of(context).textTheme.headlineMedium);
  }
}

// SMART (data-aware) — in pages/
class QuizResultPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final result = ref.watch(quizResultProvider);
    return ScoreDisplay(score: result.correct, total: result.total);
  }
}
```

## Slot Pattern
```dart
class SectionCard extends StatelessWidget {
  const SectionCard({
    required this.title,
    required this.body,
    this.trailing,
    this.action,
    super.key,
  });
  final String title;
  final Widget body;
  final Widget? trailing;
  final Widget? action;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(children: [
              Expanded(child: Text(title, style: Theme.of(context).textTheme.titleMedium)),
              if (trailing != null) trailing!,
            ]),
            const SizedBox(height: 12),
            body,
            if (action != null) ...[const SizedBox(height: 12), action!],
          ],
        ),
      ),
    );
  }
}
```

## VocabApp Structure
```
lib/presentation/
  pages/         → Smart components (ConsumerWidget, data binding)
  widgets/       → Dumb components (StatelessWidget, pure render)
  providers/     → State management (Riverpod providers)
```

## Rules
- Widgets folder: no `ref.watch`, no repository imports
- Pages folder: may use `ref`, orchestrates widgets
- Max 1 level of nesting in widget tree before extracting
