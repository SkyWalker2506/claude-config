---
last_updated: 2026-04-09
confidence: high
sources: 4
---

# RAG Patterns

## Quick Reference

| Pattern | Ne zaman | Risk |
|---------|----------|------|
| **Naive RAG** | Basit Q&A | Bağlam kesilmesi |
| **HyDE** | Belirsiz sorgu | Ek LLM maliyeti |
| **Parent-child chunk** | Uzun doküman | İndeks karmaşıklığı |
| **Rerank** | Çok aday | Gecikme |
| **Agentic RAG** | Çok adımlı araştırma | Döngü / maliyet |

```text
Minimum boru: ingest → chunk → embed → retrieve → (rerank) → augment → generate
```

## Patterns & Decision Matrix

| Sorun | Çözüm |
|-------|-------|
| Chunk sınırında cümle kesilmesi | Overlap veya yapısal bölme (başlık) |
| Tekrarlayan chunk | Dedup hash / canonical URL |
| Güncel olmayan indeks | `indexed_at` ve delta yenileme |

**Karar:** Üretimde mutlaka kaynak atıfı ve “bilinmiyorum” çıkışı.

## Code Examples

**RAG görev özeti:**

```text
[RAG] corpus=… | chunk=512/64ov | top_k=8 | rerank=yes | citation=required
```

## Anti-Patterns

- **Tüm PDF’i tek vektör:** Anlamsız retrieval.
- **PII’yi gömme:** Maskeleme veya ayrı güvenli indeks.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [LangChain RAG concepts](https://python.langchain.com/docs/concepts/rag/) — mimari özet
- [LlamaIndex docs](https://docs.llamaindex.ai/) — indeks türleri
- Research: “Retrieval-Augmented Generation for NLP” — arXiv incelemeleri
