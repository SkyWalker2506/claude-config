---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Academic Paper Structure

## Quick Reference

| Bölüm | Amaç | Özet odak |
|-------|------|-----------|
| **Title / Abstract** | Tek cümle tez + sonuç | Ana iddia + ölçüm |
| **Introduction** | Boşluk ve katkı | Problem + novelty |
| **Related work** | Konumlandırma | Kim ne yapmış, fark |
| **Method** | Tekrarlanabilirlik | Veri, model, metrik |
| **Experiments / Results** | Kanıt | Tablo, istatistik |
| **Discussion / Limitation** | Genelleme sınırları | Ne çalışmaz |
| **Conclusion** | Özet | Eylem önerisi (varsa) |

```text
IMRaD (çoğu deneysel): Introduction → Methods → Results → Discussion
```

## Patterns & Decision Matrix

| Alan | Yapı farkı |
|------|------------|
| CS / ML | Method + Experiments ağır; Appendix kod |
| İnceleme (survey) | Related work ana gövde |
| Teorik | Theorem / Proof bölümleri |

**Karar:** Özet önce abstract+conclusion hizalaması; çelişki varsa method/results’a in.

## Code Examples

**Bölüm haritası çıktısı:**

```text
[PAPER MAP]
title: …
type: empirical | survey | theory
sections: [{name, pages?, key_figures: n}]
thesis_line: "…"
```

## Anti-Patterns

- **Abstract’ı tekil sonuç sanmak:** Bazı venue’lerde hype; results tablosu ile doğrula.
- **Appendix’i görmezden gelmek:** Hyperparam ve etik detaylar orada.
- **Acknowledgments / funding’i atlamak:** Çıkar çatışması için gerekli.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [ICMJE Recommendations](https://www.icmje.org/recommendations/) — raporlama iskeleti (biyomedikal ağırlıklı)
- [ACM Publication formats](https://www.acm.org/publications/authors/reference-formatting) — bilgisayar bilimi yayınları
