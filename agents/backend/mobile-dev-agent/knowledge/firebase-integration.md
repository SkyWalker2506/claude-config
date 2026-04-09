---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Firebase Integration (Flutter)

## VocabApp Firebase Stack
- `firebase_core` — initialization
- `firebase_auth` — anonymous + email auth
- `cloud_firestore` — word data, user profiles
- `firebase_database` — real-time leaderboard, challenges
- `firebase_messaging` — push notifications (streak reminders)
- `firebase_storage` — user-uploaded content

## Initialization
```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const ProviderScope(child: MyApp()));
}
```

## Auth Pattern
```dart
final authProvider = StreamProvider<User?>((ref) {
  return FirebaseAuth.instance.authStateChanges();
});

// Anonymous → email upgrade
Future<void> upgradeAnonymous(String email, String password) async {
  final credential = EmailAuthProvider.credential(email: email, password: password);
  await FirebaseAuth.instance.currentUser?.linkWithCredential(credential);
}
```

## Firestore Patterns
```dart
// Offline-first: enable persistence (default on mobile)
// Use snapshots for real-time
final wordsStream = FirebaseFirestore.instance
    .collection('users').doc(uid)
    .collection('words')
    .orderBy('lastReviewed')
    .snapshots();

// Batch writes for bulk operations
final batch = FirebaseFirestore.instance.batch();
for (final word in words) {
  batch.set(wordsRef.doc(word.id), word.toJson());
}
await batch.commit();
```

## FCM (Push Notifications)
```dart
// VocabApp: streak reminder notifications
final messaging = FirebaseMessaging.instance;
await messaging.requestPermission();
final token = await messaging.getToken();

// Handle foreground messages
FirebaseMessaging.onMessage.listen((message) {
  // Show local notification
});
```

## Analytics
```dart
// Track quiz completion
await FirebaseAnalytics.instance.logEvent(
  name: 'quiz_completed',
  parameters: {'score': score, 'total': total, 'quiz_type': type},
);
```

## Offline-First Strategy
- VocabApp is offline-first: Hive for local, Firestore for sync
- Firestore offline persistence enabled by default on mobile
- Conflict resolution: server wins for leaderboard, client wins for personal data
