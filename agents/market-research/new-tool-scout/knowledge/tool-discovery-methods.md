---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Tool Discovery Methods

## Quick Reference

| Kanal | Kullanım |
|-------|----------|
| GitHub Trending | Repo momentum |
| Product Hunt | Launch dalgası |
| Papers + demos | Araştırma → ürün |
| Discord / Slack | Erken kullanıcı |

## Patterns & Decision Matrix

| Hedef | Süzgeç |
|-------|--------|
| Üretim | lisans + bakım |
| Deney | hızlı POC |

## Code Examples

```text
[SCOUT] query=llm-cli | signals=[stars/week, releases, issues_closed_rate]
```

## Anti-Patterns

- Sadece yıldız sayısına güvenmek.

## Deep Dive Sources

- [OSS Insight](https://ossinsight.io/)
