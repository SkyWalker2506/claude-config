# Android Native Development Best Practices

## Core Architecture Patterns

### Recommended Pattern: MVVM
- **Model** — data layer, repository pattern, Room/API data sources
- **ViewModel** — business logic, exposes LiveData/StateFlow to UI
- **View** — Activity/Fragment observes ViewModel, no business logic

### Component Architecture Stack
- **ViewModel** — survives configuration changes, holds UI state
- **LiveData / StateFlow** — lifecycle-aware observable data holders
- **Coroutines** — async operations without callback hell
- **Hilt/Dagger** — dependency injection
- **Room** — local database with type-safe queries

## Essential Android Best Practices

### RecyclerView
- Always use RecyclerView for lists (never ListView for new code)
- Use DiffUtil for efficient item updates
- Implement ViewHolder pattern strictly
- Use ListAdapter for automatic diffing

### Dependency Injection
- Use Hilt (preferred) or Dagger2
- Inject ViewModels via `@HiltViewModel`
- Never create dependencies manually in Activities/Fragments

### Async Operations
- Use Coroutines + Flow for all async work
- `viewModelScope` for ViewModel coroutines (auto-cancelled)
- `lifecycleScope` for Fragment/Activity coroutines
- Never use AsyncTask (deprecated)

### State Management
- Use `StateFlow` for UI state (single source of truth)
- Use `SharedFlow` for one-time events (navigation, snackbars)
- Model UI state as sealed classes: Loading, Success, Error

## Testing Pyramid

| Layer | Framework | What to Test |
|-------|-----------|--------------|
| Unit tests | JUnit4 + Mockito | ViewModel, Repository, Use Cases |
| Integration | JUnit4 + Room in-memory | Database, local data layer |
| UI tests | Espresso | User flows, navigation |

## Performance Optimization

### Layout Performance
- Prefer ConstraintLayout to reduce view hierarchy depth
- Avoid nested LinearLayouts
- Use `<merge>` tags to flatten layouts
- Use ViewStub for conditionally shown views

### Memory Management
- Avoid holding Context in objects that outlive Activity
- Use WeakReference when necessary
- Clear references in `onDestroyView()` for Fragments

### Load Time
- Use lazy initialization (`by lazy`)
- Defer non-critical work with `lifecycleScope.launchWhenStarted`
- Use App Startup library for startup task ordering

## Key Jetpack Libraries

- **Navigation Component** — type-safe navigation, back stack management
- **WorkManager** — guaranteed background work, constraint-based
- **Paging 3** — efficient large dataset loading
- **DataStore** — replacement for SharedPreferences (type-safe, async)
- **CameraX** — simplified camera API

## Code Quality Principles (SOLID for Android)

- **Single Responsibility**: Each class does one thing
- **Dependency Inversion**: Depend on interfaces, not concrete classes
- **Open/Closed**: Extend via composition, not modification
- Repository layer must be testable — inject data sources, don't create them
