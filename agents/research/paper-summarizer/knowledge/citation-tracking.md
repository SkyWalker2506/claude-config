---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Citation Tracking

## Quick Reference

| Görev | Araç / format | Not |
|-------|---------------|-----|
| **BibTeX çıkarma** | `.bib` kayıtları | Anahtar çakışması kontrolü |
| **DOI çözümleme** | doi.org | Versiyon (v1/v2) |
| **İlişki grafiği** | Kim kimi alıntılıyor | “Seminal” = yüksek merkezilik (göreli) |
| **Self-citation** | İlk yazar tekrarı | Bias uyarısı |

```text
Edge: citing_paper → cited_paper | reason: background | method | compare
```

## Patterns & Decision Matrix

| Senaryo | Uygulama |
|---------|----------|
| SLR / survey | PRISMA benzeri sayım + dahil/hariç kriteri |
| Hızlı özet | Sadece “Related” ve “Compared against” |
| Çoğaltılmış yayın | Aynı çalışma farklı venue — tek düğüm |

**Karar:** Her önemli iddia için en az bir bağımsız (farklı grup) atıf hedefle.

## Code Examples

**Mini referans listesi:**

```text
[CITATIONS core=5]
1. … (DOI) — role: establishes baseline
2. … — role: negative result (important)
…
```

## Anti-Patterns

- **Sayıyı kalite sanmak:** Çok atıflı eski survey güncel olmayabilir.
- **Preprint vs yayın karıştırmak:** Versiyon ve venue’ü ayrı etiketle.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) — metadata doğrulama
- [OpenAlex](https://docs.openalex.org/) — citation graph ve ID
