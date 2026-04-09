---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Content Calendar Design

## Quick Reference

| Katman | İçerik |
|--------|--------|
| Tema | aylık omurga |
| Slot | gün + saat + kanal |
| Buffer | olay / kampanya |

## Patterns & Decision Matrix

| Frekans | Risk |
|---------|------|
| Yüksek | tükenmişlik |
| Düşük | unutulma |

## Code Examples

```text
[CAL] week=12 | pillars=[edu, proof, culture] | channels=[li, x]
```

## Anti-Patterns

- Her gün aynı CTA tekrarı.

## Deep Dive Sources

- Sprout / Hootsuite takvim rehberleri
