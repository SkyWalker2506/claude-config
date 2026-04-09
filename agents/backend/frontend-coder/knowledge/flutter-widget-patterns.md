---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Flutter Widget Patterns

## Composition Over Inheritance
```dart
// Good: compose small widgets
class QuizPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const QuizAppBar(),
      body: Column(
        children: [
          const QuizProgressBar(),
          Expanded(child: QuizQuestionCard(question: question)),
          QuizAnswerGrid(answers: answers, onSelect: onAnswer),
        ],
      ),
    );
  }
}
```

## Separation of Concerns
- **Page**: scaffold, layout, navigation — no business logic
- **Widget**: pure UI component, receives data via constructor
- **Provider**: state management, data fetching
- VocabApp pattern: `presentation/pages/`, `presentation/widgets/`, `presentation/providers/`

## Reusable Widget Guidelines
```dart
// Accept data + callbacks, no internal state fetching
class WordCard extends StatelessWidget {
  const WordCard({
    required this.word,
    required this.onTap,
    this.showFavorite = true,
    super.key,
  });
  final Word word;
  final VoidCallback onTap;
  final bool showFavorite;
}
```

## Builder Pattern for Complex Widgets
```dart
class AdaptiveWordList extends StatelessWidget {
  const AdaptiveWordList({
    required this.words,
    required this.itemBuilder,
    this.emptyBuilder,
    super.key,
  });
  final List<Word> words;
  final Widget Function(BuildContext, Word) itemBuilder;
  final WidgetBuilder? emptyBuilder;

  @override
  Widget build(BuildContext context) {
    if (words.isEmpty) {
      return emptyBuilder?.call(context) ?? const EmptyStateWidget();
    }
    return ListView.builder(
      itemCount: words.length,
      itemBuilder: (ctx, i) => itemBuilder(ctx, words[i]),
    );
  }
}
```

## Key Principles
- Max 200 lines per widget file — extract sub-widgets
- Use `const` constructors whenever possible
- Private helper widgets as `_SubWidget` in same file only if <50 lines
- Larger helpers → separate file
- VocabApp widgets: `streak_chip.dart`, `word_card.dart`, `flash_card_view.dart`
