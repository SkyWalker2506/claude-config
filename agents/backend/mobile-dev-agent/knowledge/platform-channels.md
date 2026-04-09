---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Platform Channels

## MethodChannel (Request-Response)
```dart
const channel = MethodChannel('com.vocabapp/tts');

// Flutter side
Future<void> speak(String text, String lang) async {
  await channel.invokeMethod('speak', {'text': text, 'lang': lang});
}

// iOS side (Swift)
let channel = FlutterMethodChannel(name: "com.vocabapp/tts", binaryMessenger: controller.binaryMessenger)
channel.setMethodCallHandler { call, result in
  if call.method == "speak" {
    let args = call.arguments as! [String: String]
    self.tts.speak(args["text"]!, lang: args["lang"]!)
    result(nil)
  }
}
```

## EventChannel (Streaming)
```dart
const eventChannel = EventChannel('com.vocabapp/speech');

// Listen to speech recognition results
eventChannel.receiveBroadcastStream().listen((result) {
  setState(() => _recognized = result as String);
});
```

## VocabApp Platform Usage
- TTS: `tts_provider.dart` — text-to-speech for word pronunciation
- STT: `stt_provider.dart` — speech-to-text for voice quiz
- Haptics: `HapticFeedback` (Flutter built-in, no channel needed)
- Share: `share_plus` package (abstracts platform channels)

## Platform-Specific Code
```dart
import 'dart:io' show Platform;

// Conditional behavior
if (Platform.isIOS) {
  // iOS-specific UI (Cupertino date picker, etc.)
} else {
  // Android/default
}

// Conditional imports for web
// Use kIsWeb from foundation
```

## Best Practices
- Use existing packages before writing custom channels
- Always handle `PlatformException` — channel calls can fail
- Channel names: reverse domain (`com.vocabapp/feature`)
- Test with `TestDefaultBinaryMessenger` in widget tests
- VocabApp doesn't need heavy native code — prefer Flutter/Dart packages
