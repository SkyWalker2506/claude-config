---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Unity Editor Tooling

## Quick Reference

| API | Use |
|-----|-----|
| **EditorWindow** | Custom panels |
| **CustomInspector** | Component UX |
| **MenuItem** | Quick actions |

**2025–2026:** Put editor scripts under `Editor/` folder; use `SerializedObject` for undo-safe edits.

## Patterns & Decision Matrix

| UI | Araç |
|----|------|
| Hızlı ayar | Custom Inspector |
| Çok adımlı akış | EditorWindow + SerializedObject |

## Code Examples

```csharp
[MenuItem("Tools/MyGame/Build Asset Cache")]
static void BuildCache() { ... }
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Editor’da ağır iş | Donma |
| `OnGUI` ile büyük UI | Performans |

## Deep Dive Sources

- [Unity — Editor Scripting](https://docs.unity3d.com/Manual/EditorScripting.html)
