---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Tool Recommendation Framework

## Quick Reference

| Boyut | Soru |
|-------|------|
| **Fit** | Görevi çözüyor mu? |
| **Operasyon** | Self-host / SaaS, SLA |
| **Maliyet** | Lisans + eğitim |
| **Risk** | Vendor lock-in, güvenlik |
| **Ekosistem** | Eklenti, entegrasyon |

```text
Skor: ağırlıklı matris — ağırlıklar hedefe göre değişir (startup vs enterprise)
```

## Patterns & Decision Matrix

| Çıktı | İçerik |
|-------|--------|
| Tek öneri | Güçlü varsayılan + riskler |
| Kısa liste | 2–3 seçenek + karar ağacı |

**Karar:** “En iyi” yerine “şu kısıtlarla en uygun” dilini kullan.

## Code Examples

**Öneri kartı:**

```text
[TOOL] name=… | fit=8/10 | cost=medium | risks=[lock-in] | alt=…
```

## Anti-Patterns

- **Son kullandığın aracı önermek:** Tarafsız kriterleri yaz.
- **Ücretsiz = risksiz:** Destek ve güvenlik maliyetini say.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- ThoughtWorks Tech Radar — değerlendirme disiplini
- OWASP for tooling risk — güvenlik tarafı
