---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Testing Patterns

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

## Widget Test
```dart
testWidgets('WordCard shows word and definition', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: WordCard(
          word: Word(id: '1', text: 'hello', definition: 'merhaba'),
          onTap: _noop,
        ),
      ),
    ),
  );
  expect(find.text('hello'), findsOneWidget);
  expect(find.text('merhaba'), findsOneWidget);
});
```

## Riverpod Widget Test
```dart
testWidgets('QuizPage shows loading then questions', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        quizProvider.overrideWith(() => FakeQuizNotifier()),
      ],
      child: const MaterialApp(home: QuizPage()),
    ),
  );
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
  await tester.pump(const Duration(seconds: 1));
  expect(find.byType(QuizQuestionCard), findsOneWidget);
});
```

## Integration Test
```dart
// integration_test/app_test.dart
void main() {
  testWidgets('full quiz flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Navigate to quiz
    await tester.tap(find.text('Start Quiz'));
    await tester.pumpAndSettle();

    // Answer questions
    await tester.tap(find.byKey(const Key('answer-0')));
    await tester.pumpAndSettle();

    // Verify result
    expect(find.text('Quiz Complete'), findsOneWidget);
  });
}
```

## Golden Test
```dart
testWidgets('WordCard golden', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      theme: AppTheme.light(Colors.blue),
      home: const WordCard(word: testWord, onTap: _noop),
    ),
  );
  await expectLater(
    find.byType(WordCard),
    matchesGoldenFile('goldens/word_card_light.png'),
  );
});
```
- Run: `flutter test --update-goldens` to generate baselines
- Test both light and dark themes

## Mocking
```dart
// With mocktail
class MockWordRepository extends Mock implements WordRepository {}

// Setup
final mockRepo = MockWordRepository();
when(() => mockRepo.getAll()).thenAnswer((_) async => [testWord]);
```

## VocabApp Test Strategy
| Layer | Tool | Coverage Target |
|-------|------|----------------|
| Providers | Unit test + mock repos | 90% |
| Widgets | Widget test | Key components |
| Pages | Widget test + Riverpod override | Happy + error path |
| Full flow | Integration test | Critical paths (quiz, onboarding) |
| Visual | Golden test | Theme compliance |
