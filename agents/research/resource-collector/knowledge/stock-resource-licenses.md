---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Stock Resource Licenses

## Quick Reference

| Senaryo | Soru |
|---------|------|
| Oyun | Redistribution var mı? |
| Video | Broadcast hakkı |
| Print | Run limit |

## Patterns & Decision Matrix

| Platform | Tipik kısıt |
|----------|-------------|
| Shutterstock | Seat / proje |
| Envato | Tek ürün / çoklu |

## Code Examples

```text
[STOCK] provider=… | sku=… | seats=5 | redistribution=game_build_only
```

## Anti-Patterns

- Watermark’lı preview’ı ship etmek.

## Deep Dive Sources

- Platformların Terms of Service sayfaları
