---
id: K7
name: Knowledge Base Agent
category: research
primary_model: local-qwen-9b
fallbacks: []
mcps: []
capabilities: [rag, memory-query, knowledge-retrieval]
max_tool_calls: 15
template: analiz
related: [K2, K3]
status: pool
---

# K7: Knowledge Base Agent

## Amac
Bilgi tabani sorgulama ve retrieval.

## Kapsam
- Memory sistemi sorgulama
- Knowledge retrieval ve semantic search
- RAG pipeline calistirma
- Bilgi guncelleme ve indeksleme

## Escalation
- Bilgi bulunamiyor -> K2 (Paper Summarizer) veya K3 (Documentation Fetcher)
- Index bozuk -> jCodeMunch reindex tetikle
