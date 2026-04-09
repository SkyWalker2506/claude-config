---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# License Compliance

## Quick Reference

| Lisans | Tipik kısıt |
|--------|-------------|
| CC0 | Geniş kullanım |
| CC-BY | Attribution |
| CC-BY-SA | Share-alike zinciri |
| Editorial | Oyun içi yasak olabilir |

## Patterns & Decision Matrix

| Dağıtım | Kontrol |
|---------|---------|
| Oyun build | Redistribution şartı |
| Saaş | Hosted kullanım izni |

## Code Examples

```text
[LICENSE_CHECK] asset_id=… | spdx=CC-BY-4.0 | attribution_text="…" | commercial_ok=true
```

## Anti-Patterns

- “Ücretsiz indirdim” = her kullanım serbest sanmak.

## Deep Dive Sources

- [Choose a License](https://choosealicense.com/)
- [Creative Commons](https://creativecommons.org/licenses/)
