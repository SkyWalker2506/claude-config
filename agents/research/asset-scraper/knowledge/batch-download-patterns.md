---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Batch Download Patterns

## Quick Reference

| İlke | Uygulama |
|------|----------|
| Rate limit | Retry-After uy |
| Idempotency | Aynı dosyayı iki kez yazma |
| Checksum | SHA-256 doğrula |
| Manifest | JSON satır satır kaynak |

## Patterns & Decision Matrix

| Ölçek | Araç |
|-------|------|
| Küçük | wget/curl loop |
| Orta | rclone / aria2 |
| Büyük | Queue + worker |

## Code Examples

```bash
aria2c -i urls.txt -x 8 -j 4 --checksum=sha-256
```

## Anti-Patterns

- ToS’i ihlal eden paralel crawl.

## Deep Dive Sources

- [aria2 manual](https://aria2.github.io/manual/en/html/)
