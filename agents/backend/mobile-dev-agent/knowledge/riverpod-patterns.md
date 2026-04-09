---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Riverpod Patterns (flutter_riverpod 3.x)

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## Provider Types Quick Reference
| Type | Mutable | Async | Use Case |
|------|---------|-------|----------|
| Provider | No | No | Computed values, DI |
| StateProvider | Yes | No | Simple toggles, enum |
| FutureProvider | No | Yes | One-shot async fetch |
| StreamProvider | No | Yes | Real-time data |
| StateNotifierProvider | Yes | No/Yes | Complex state + methods |
| NotifierProvider | Yes | No | Riverpod 2.0+ preferred |
| AsyncNotifierProvider | Yes | Yes | Async + methods |

## StateNotifier Pattern (VocabApp Current)
```dart
class QuizNotifier extends StateNotifier<QuizState> {
  QuizNotifier(this._repo) : super(const QuizState.initial());
  final WordRepository _repo;

  Future<void> loadQuestions(QuizConfig config) async {
    state = state.copyWith(status: QuizStatus.loading);
    try {
      final words = await _repo.getRandomWords(config.count);
      state = state.copyWith(status: QuizStatus.ready, questions: words);
    } catch (e) {
      state = state.copyWith(status: QuizStatus.error, error: e.toString());
    }
  }

  void answer(int index, bool correct) {
    state = state.copyWith(
      currentIndex: state.currentIndex + 1,
      score: correct ? state.score + 1 : state.score,
    );
  }
}
```

## AutoDispose + Family
```dart
// Page-scoped: disposed when page unmounts
final quizProvider = StateNotifierProvider.autoDispose<QuizNotifier, QuizState>((ref) {
  return QuizNotifier(ref.read(wordRepositoryProvider));
});

// Parameterized: one provider per word ID
final wordDetailProvider = FutureProvider.autoDispose.family<Word, String>((ref, id) {
  return ref.read(wordRepositoryProvider).getById(id);
});
```

## Dependency Injection
```dart
// Repository layer
final wordRepositoryProvider = Provider<WordRepository>((ref) {
  return WordRepositoryImpl(ref.read(firestoreProvider));
});

// Override in tests
ProviderScope(
  overrides: [wordRepositoryProvider.overrideWithValue(MockWordRepository())],
  child: const MyApp(),
)
```

## VocabApp Provider Files
- `gamification_provider.dart` — streak, XP, badges
- `quiz_accuracy_provider.dart` — quiz scoring
- `progressive_quiz_provider.dart` — adaptive difficulty
- `srs_provider.dart` — spaced repetition scheduling
- `favorite_provider.dart` — word favorites
