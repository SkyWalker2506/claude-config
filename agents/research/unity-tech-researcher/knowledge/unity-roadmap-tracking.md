---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Unity Roadmap Tracking

## Quick Reference

| Kaynak | Ne izlenir |
|--------|------------|
| Unity blog / release notes | LTS vs TECH |
| Issue Tracker | Bilinen bug |
| Package manager | com.unity.* sürümleri |

## Patterns & Decision Matrix

| Karar | Sinyal |
|-------|--------|
| LTS’e kal | Uzun destek, konsol |
| TECH’e geç | yeni özellik zorunlu |

## Code Examples

```text
[ROADMAP] unity=6000.x | lts_until=… | package=com.unity.entities@2.x target
```

## Anti-Patterns

- EOL sürümde yeni proje başlatma.

## Deep Dive Sources

- [Unity Roadmap](https://unity.com/releases)
- [Package release notes](https://docs.unity3d.com/Packages/)
