---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# State Management — Riverpod (VocabApp Standard)

## VocabApp Uses flutter_riverpod 3.x
- All providers in `presentation/providers/`
- Provider types by use case

## Provider Types
```dart
// Simple computed value
final wordCountProvider = Provider<int>((ref) {
  return ref.watch(wordListProvider).length;
});

// Async data fetch
final wordsProvider = FutureProvider.autoDispose<List<Word>>((ref) async {
  return ref.read(wordRepositoryProvider).getAll();
});

// Mutable state (form, UI toggle)
final themeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.system);

// Complex state with methods
final quizProvider = StateNotifierProvider<QuizNotifier, QuizState>((ref) {
  return QuizNotifier(ref.read(wordRepositoryProvider));
});

// Stream (real-time data)
final streakProvider = StreamProvider<int>((ref) {
  return ref.read(gamificationRepositoryProvider).watchStreak();
});
```

## AsyncValue Handling
```dart
ref.watch(wordsProvider).when(
  data: (words) => WordList(words: words),
  loading: () => const WordListSkeleton(),
  error: (e, st) => ErrorWidget(message: e.toString(), onRetry: () => ref.invalidate(wordsProvider)),
);
```

## Provider Comparison
| Pattern | VocabApp Use | When |
|---------|-------------|------|
| Riverpod | Primary | All new code |
| Provider (legacy) | None | Don't use |
| BLoC | None | Overkill for this app |
| setState | Local UI only | Toggle, animation flag |

## Best Practices
- `autoDispose` for page-scoped providers (quiz session)
- `family` for parameterized providers (word by ID)
- Keep providers small and focused — one per concern
- Never call `ref.read` in build — use `ref.watch`
- VocabApp providers: `gamification_provider`, `quiz_accuracy_provider`, `streak_chip`
