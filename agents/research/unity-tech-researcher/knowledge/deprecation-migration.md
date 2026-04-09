---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Deprecation Migration

## Quick Reference

| Aşama | Eylem |
|-------|-------|
| Obsolete uyarısı | API değişim listesi |
| Removal sürümü | Takvim |
| Kod tarama | `grep -r Obsolete` |

## Patterns & Decision Matrix

| Kapsam | Plan |
|--------|------|
| Tek API | PR başına |
| Pipeline | Aşamalı flag |

## Code Examples

```csharp
#if UNITY_6000_OR_NEWER
// new API
#else
#pragma warning disable 618
// legacy
#endif
```

## Anti-Patterns

- Deprecated API’yi sessizce susturup unutmak.

## Deep Dive Sources

- Unity upgrade guides per major version
