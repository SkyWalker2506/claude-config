---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Knowledge Retrieval

## Quick Reference

| Strateji | Araç sınıfı | Uygun sorgu |
|----------|-------------|-------------|
| **Dense** | Embedding cosine | Anlamsal benzerlik |
| **Sparse** | BM25, SPLADE | Anahtar kelime kesinliği |
| **Hybrid** | α·dense + (1-α)·sparse | Genel üretim |
| **Filter** | Metadata (ACL, tarih) | Yetki sınırlı |

```text
Skor füzyonu: normalize et → rerank → threshold altını düşür
```

## Patterns & Decision Matrix

| Gecikme bütçesi | Ayar |
|-----------------|------|
| <200 ms | Küçük indeks, rerank yok |
| İnteraktif | top_k düşük + rerank |
| Batch | Geniş aday + rerank |

**Karar:** Aynı sorgu tekrarlanıyorsa cache (embedding + sonuç).

## Code Examples

**Sorgu günlüğü:**

```text
[RETRIEVE] q_hash=… | latency_ms=… | hits=5 | min_score=0.42 | filters: {project=…}
```

## Anti-Patterns

- **Sadece vektör mesafesi:** Kısa sorgularda bağlam kaybı — hybrid düşün.
- **İndeks şemasını versiyonlamama:** Embedding modeli değişince yeniden indeks.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [BEIR benchmark](https://github.com/beir-cellar/beir) — retrieval değerlendirme
- Vespa / Elasticsearch hybrid search dokümantasyonu
