---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Deliverability Guide

## Quick Reference

| Faktör | Eylem |
|--------|-------|
| SPF/DKIM/DMARC | DNS doğrula |
| Liste kalitesi | Hard bounce temizle |
| İçerik | spam tetikleyici kelime azalt |
| Frekans | Segment bazlı |

## Patterns & Decision Matrix

| Sorun | Önce |
|-------|------|
| Spam klasörü | Auth + reputation |
| Düşük açılış | konu/satır testi |

## Code Examples

```text
[DELIVERABILITY] spf=pass dkim=pass dmarc=quarantine | list_age_days=… | complaint_rate<0.1%
```

## Anti-Patterns

- Satın alınmış liste ile cold blast.

## Deep Dive Sources

- [Google Postmaster](https://postmaster.google.com/)
- [M3AAWG](https://www.m3aawg.org/) — best practices
