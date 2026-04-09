---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Font Sources Guide

## Quick Reference

| İhtiyaç | Kaynak tipi |
|---------|-------------|
| UI | Variable font, OFL |
| Oyun | Bitmap / SDF pipeline |
| Marka | Lisanslı aile |

## Patterns & Decision Matrix

| Dağıtım | Lisans |
|---------|--------|
| Web | WOFF2 subset |
| Embeded app | Embedding clause oku |

## Code Examples

```text
[FONT] family=Inter | license=OFL | weights=[400,700] | subset=latin
```

## Anti-Patterns

- Adobe font’u build’e gömüp lisansı atlama.

## Deep Dive Sources

- [Google Fonts](https://fonts.google.com/)
- [SIL OFL](https://openfontlicense.org/)
