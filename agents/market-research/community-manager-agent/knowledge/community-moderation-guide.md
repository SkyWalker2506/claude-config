---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Community Moderation Guide

## Quick Reference

| Seviye | Aksiyon |
|--------|---------|
| Uyarı | mesaj + kural linki |
| Susturma | süre belirli |
| Ban | tekrar ihlal / güvenlik |

## Patterns & Decision Matrix

| Dil | Mod |
|-----|-----|
| TR + EN | açık kurallar |
| 7/24 | rotasyon + playbook |

## Code Examples

```text
[MOD] case=spam | action=mute_24h | rule_ref=#3 | logged=true
```

## Anti-Patterns

- Tutarsız ceza (aynı ihlal farklı sonuç).

## Deep Dive Sources

- [Discord Moderator Academy](https://discord.com/moderation)
