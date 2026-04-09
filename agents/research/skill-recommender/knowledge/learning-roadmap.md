---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Learning Roadmap

## Quick Reference

| Bileşen | Açıklama |
|---------|----------|
| **Hedef rol / outcome** | Tek cümle north star |
| **Gap listesi** | skill-gap-analysis ile üretilen eksikler |
| **Modüller** | Sıralı bloklar; her biri 1–3 hafta |
| **Doğrulama** | Her modül sonu mini proje veya sertifika |

```text
[ROADMAP] horizon_weeks=N | modules=[M1,M2,...] | verify_per_module=true
```

## Patterns & Decision Matrix

| Horizon | Yaklaşım |
|---------|----------|
| 4–8 hafta | Dar kapsam, tek stack |
| 3–6 ay | Foundation → practice → production shadow |
| 12+ ay | Yetkinlik matrisi + yıllık OKR hizası |

**Trade-off:** Hız vs derinlik — aynı anda iki “foundation” modülü açma.

## Code Examples

**Roadmap özeti (iş listesi için):**

```markdown
## Q2 — Backend path
1. HTTP + REST (K6 tutorial seti) — verify: CRUD API
2. SQL + ORM — verify: migration + test
3. Observability — verify: dashboard + alert
```

## Anti-Patterns

- **Süresiz “öğreniyorum”:** modül bitiş tarihi yok.
- **Sertifika avcılığı:** işe yarayan çıktı yerine koleksiyon.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [SFIA / e-CF](https://www.sfia-online.org/) — yetkinlik seviyeleri
- [Bloom taksonomisi](https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/) — öğrenme hedefi yazımı
