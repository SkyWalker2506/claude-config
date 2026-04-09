---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Flutter Widget Testing

## Quick Reference

| API | Use |
|-----|-----|
| `testWidgets` | Async widget test |
| `WidgetTester.pump` | Build frame |
| `find.byType`, `find.text` | Finders |
| `tester.tap`, `enterText` | Interactions |
| `pumpAndSettle` | Wait for animations |

**Golden tests:** `matchesGoldenFile` for visual regression — platform-specific; run in CI with same theme.

**2025–2026:** `integration_test` package for device tests; `flutter test` for widget.

## Patterns & Decision Matrix

| Test | Where |
|------|-------|
| Widget in isolation | `testWidgets` + `MaterialApp` wrapper |
| Provider/Riverpod | `ProviderScope` with overrides |

## Code Examples

```dart
testWidgets('shows error', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: LoginPage()));
  await tester.enterText(find.byType(TextField).first, 'bad');
  await tester.tap(find.text('Submit'));
  await tester.pump();
  expect(find.text('Invalid'), findsOneWidget);
});
```

## Anti-Patterns

| Bad | Fix |
|-----|-----|
| Testing implementation details | Find by key/semantics |
| No `pump` after async | `await tester.pump(Duration.zero)` |

## Deep Dive Sources

- [Flutter — Widget testing](https://docs.flutter.dev/cookbook/testing/widget/introduction)
- [Flutter — Integration testing](https://docs.flutter.dev/testing/integration-tests)
