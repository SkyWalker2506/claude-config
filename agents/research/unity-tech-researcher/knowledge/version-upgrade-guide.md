---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Version Upgrade Guide

## Quick Reference

| Adım | İçerik |
|------|--------|
| 1 | Yedek + branch |
| 2 | Upgrade Assistant raporu |
| 3 | Paket çözümleme |
| 4 | Smoke: boot + kritik sahne |

## Patterns & Decision Matrix

| Atlama | Güvenli mi |
|--------|------------|
| Minor | Genelde evet |
| Major | Test planı şart |

## Code Examples

```text
[UPGRADE] from=2022.3 LTS to=6000.x | steps=[backup, assistant, packages, tests] | rollback_tag=v-pre-upgrade
```

## Anti-Patterns

- Production’da ilk açılışta upgrade.

## Deep Dive Sources

- [Manual Upgrade Unity](https://docs.unity3d.com/Manual/UpgradeGuide.html)
