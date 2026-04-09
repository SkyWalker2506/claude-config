---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Form Patterns

## Basic Form Validation
```dart
final _formKey = GlobalKey<FormState>();

Form(
  key: _formKey,
  child: Column(
    children: [
      TextFormField(
        decoration: const InputDecoration(labelText: 'Word'),
        validator: (v) => v == null || v.isEmpty ? 'Required' : null,
      ),
      TextFormField(
        decoration: const InputDecoration(labelText: 'Definition'),
        validator: (v) => v == null || v.length < 2 ? 'Min 2 characters' : null,
      ),
      FilledButton(
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            _formKey.currentState!.save();
            // submit
          }
        },
        child: const Text('Add Word'),
      ),
    ],
  ),
)
```

## Error Handling Pattern
```dart
// Show inline errors + snackbar for server errors
try {
  await repository.addWord(word);
  if (context.mounted) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Word added')),
    );
    Navigator.pop(context);
  }
} catch (e) {
  if (context.mounted) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Failed: ${e.toString()}')),
    );
  }
}
```

## Multi-Step Form (Quiz Setup)
```dart
class QuizSetupStepper extends StatefulWidget {
  @override
  State<QuizSetupStepper> createState() => _QuizSetupStepperState();
}

class _QuizSetupStepperState extends State<QuizSetupStepper> {
  int _step = 0;
  final _config = QuizConfig();

  @override
  Widget build(BuildContext context) {
    return Stepper(
      currentStep: _step,
      onStepContinue: () {
        if (_step < 2) setState(() => _step++);
        else _startQuiz();
      },
      onStepCancel: () {
        if (_step > 0) setState(() => _step--);
      },
      steps: [
        Step(title: const Text('Word Pack'), content: PackSelector(config: _config)),
        Step(title: const Text('Question Count'), content: CountSlider(config: _config)),
        Step(title: const Text('Quiz Type'), content: TypeSelector(config: _config)),
      ],
    );
  }
}
```

## VocabApp Form Pages
- `custom_words_page.dart` — add/edit custom words
- `create_project_page.dart` — new word pack
- `create_challenge_page.dart` — challenge setup
- `import_project_page.dart` — file picker + import

## Best Practices
- Always use `TextFormField` inside `Form` (not raw `TextField`)
- Show validation errors on submit, not on every keystroke
- Disable submit button while loading (use `ValueNotifier<bool>`)
- Preserve form state on rotation with `AutomaticKeepAliveClientMixin`
- M3: use `InputDecorationTheme(filled: true, border: OutlineInputBorder())`
