---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# UPM Package Development

## Quick Reference

| File | Role |
|------|------|
| `package.json` | name, version, dependencies |
| **Embedded** | `Packages/com.my.pkg` |
| **Git URL** | UPM dependency |

**Semver:** Unity packages follow major.minor.patch.

## Code Examples

```json
{
  "name": "com.mygame.core",
  "version": "1.0.0",
  "unity": "2022.3"
}
```

## Deep Dive Sources

- [Unity — Creating custom packages](https://docs.unity3d.com/Manual/CustomPackages.html)
