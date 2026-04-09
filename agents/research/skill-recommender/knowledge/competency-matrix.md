---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Competency Matrix

## Quick Reference

Satırlar: yetkinlik alanları. Sütunlar: seviye (1–5) veya Beginner→Expert.

| Seviye | Davranış |
|--------|----------|
| 1 | Gözetimle görev |
| 2 | Bağımsız rutin görev |
| 3 | Karma senaryolar, mentorluk |
| 4 | Tasarım ve strateji |
| 5 | kurumsal standart / thought leadership |

```text
[MATRIX] role=… | self_assessment | target_band | gap_cells highlighted
```

## Patterns & Decision Matrix

| Kullanım | Ne zaman |
|----------|----------|
| Hiring | JD ile satır hizalama |
| Promotion | Seviye 3→4 kanıt seti |
| Learning plan | Boş hücre → roadmap modülü |

## Code Examples

**YAML satır örneği:**

```yaml
competencies:
  - id: api_design
    current: 2
    target: 3
    evidence: ["OpenAPI PR #12", "review from staff"]
```

## Anti-Patterns

- **Dunning-Kruger:** tüm hücreleri 4–5 doldurmak.
- **Tek projeyle genelleme:** tek PR ile “expert” iddiası.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [European e-Competence Framework](https://www.ecompetences.eu/) — seviye tanımları
- [Dreyfus model](https://en.wikipedia.org/wiki/Dreyfus_model_of_skill_acquisition) — uzmanlık aşamaları
