---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Discord Server Setup

## Quick Reference

| Yapı | Not |
|------|-----|
| Kanallar | bilgi / duyuru / destek |
| Roller | hiyerarşi + renk |
| Bot | ticket + log |

## Patterns & Decision Matrix

| Büyüklük | Öneri |
|----------|-------|
| <500 | basit kanal |
| 5000+ | forum + etiket |

## Code Examples

```text
[SERVER_MAP] categories=4 | mod_only=… | onboarding_flow=5_steps
```

## Anti-Patterns

- @everyone kötüye kullanımı.

## Deep Dive Sources

- Discord sunucu şablonları
