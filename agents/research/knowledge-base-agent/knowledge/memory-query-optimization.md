---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Memory Query Optimization

## Quick Reference

| Teknik | Amaç |
|--------|------|
| **Query rewriting** | Belirsiz kullanıcı dilini netleştir |
| **Session summary** | Uzun sohbeti sıkıştır |
| **Recency bias** | Son mesajlara ağırlık |
| **Budget** | Token limitine göre kırp |

```text
Bütçe: system + summary + last_k turns + retrieved ≤ context_window
```

## Patterns & Decision Matrix

| Bellek türü | Okuma |
|-------------|-------|
| Epizodik | Olay sırası |
| Semantik | Özet vektörü |
| Prosedürel | Adım listesi (dikkat: güncellik) |

**Karar:** Çelişen anılar → yenisi kazanır veya “disputed” etiketi.

## Code Examples

**Bellek çekme:**

```text
[MEMORY] layers=[semantic, episodic] | tokens_used=… | pruned=turns[-8:]
```

## Anti-Patterns

- **Her şeyi hafızaya yazmak:** Gürültü ve maliyet.
- **Kişisel veriyi özetlemeden saklamak:** Minimize et veya şifrele.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- MemGPT / agent memory araştırmaları — mimari fikirler
- [Anthropic long context best practices](https://docs.anthropic.com/) — bağlam yönetimi
