---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# OWASP Top 10 (Web) — Risk-Focused View

## Quick Reference

> **Note:** OWASP published **Top 10:2021** as the latest full web ranking. This file name follows project convention; content maps to current OWASP web risks and 2025–2026 threat landscape. Verify [OWASP Top Ten](https://owasp.org/www-project-top-ten/) for updates.

| ID | Risk area (2021 labels) |
|----|-------------------------|
| A01 | Broken Access Control |
| A02 | Cryptographic Failures |
| A03 | Injection |
| A04 | Insecure Design |
| A05 | Security Misconfiguration |
| A06 | Vulnerable and Outdated Components |
| A07 | Identification and Authentication Failures |
| A08 | Software and Data Integrity Failures |
| A09 | Security Logging and Monitoring Failures |
| A10 | Server-Side Request Forgery (SSRF) |

**Emerging topics (2025–2026):** Supply chain, AI/ML abuse, misconfigured cloud — still map to A05/A06/A04.

## Patterns & Decision Matrix

| Finding | Priority |
|---------|----------|
| AuthZ bypass | P0 |
| Outdated dep with known RCE | P0 after exploitability |

## Code Examples

```text
Checklist: IDOR — can user A access /users/B/data by swapping id?
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Checkbox audit without threat model | Misses logic bugs |

## Deep Dive Sources

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
