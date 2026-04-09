---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Skill Gap Analysis

## Quick Reference

| Adım | Girdi | Çıktı |
|------|-------|-------|
| **Hedef rol / görev** | Job desc veya OKR | Yetkinlik listesi |
| **Mevcut envanter** | CV, repo, sınav | Skor veya seviye |
| **Gap** | Hedef − mevcut | Öncelik sırası |
| **Ölçüm** | KPI veya demo | Başarı tanımı |

```text
Gap = required_competency - demonstrated_evidence (kanıt yoksa UNKNOWN)
```

## Patterns & Decision Matrix

| Kanıt türü | Güven |
|------------|-------|
| Üretim sistemi sahipliği | Yüksek |
| Sertifika | Orta |
| Sadece ilgi | Düşük |

**Karar:** Her gap için “neden önemli” ve “ilk 40 saatte ne” maddesi.

## Code Examples

**Gap tablosu:**

```markdown
| Yetkinlik | Gerekli | Mevcut | Gap | Öncelik |
|-----------|---------|--------|-----|---------|
| … | L3 | L1 | … | P0 |
```

## Anti-Patterns

- **Her şeyi P0 yapmak:** En fazla 3 kritik gap.
- **Yumuşak beceriyi atlama:** İletişim / yazılı netlik teknik kadar önemli olabilir.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- SFIA / e-CF yetkinlik çerçeveleri
- O*NET / ESCO — beceri sözlükleri
