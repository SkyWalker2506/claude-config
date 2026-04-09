---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# License Risk Assessment

## Quick Reference

| Risk | Belirti |
|------|---------|
| Seat limit | Ekip büyüyünce ihlal |
| Redistribution | Build’e gömme şartı |
| Source code | Değiştirilebilir mi |

## Patterns & Decision Matrix

| Proje | Minimum |
|-------|---------|
| Indie | Tek seat açık |
| Studio | Hukuk onayı |

## Code Examples

```text
[LICENSE_RISK] asset=… | seats=unlimited|n | redistribute=binary_ok | source_mod=denied
```

## Anti-Patterns

- “Asset Store aldım” = tüm şirkette serbest.

## Deep Dive Sources

- Asset Store lisans metni (ürün bazlı)
