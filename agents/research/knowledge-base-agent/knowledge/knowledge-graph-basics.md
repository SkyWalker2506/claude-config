---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Knowledge Graph Basics

## Quick Reference

| Kavram | Tanım |
|--------|-------|
| **Node** | Varlık (kişi, kavram, dosya) |
| **Edge** | İlişki türü ile etiketli |
| **Property graph** | Düğüm/kenar özellikleri |
| **RDF triple** | subject–predicate–object |

```text
Sorgu: graph traverse vs SPARQL vs Cypher — ekosisteme bağlı
```

## Patterns & Decision Matrix

| Ne zaman graf? | Ne zaman vektör? |
|----------------|------------------|
| Çok atlamalı ilişki | Bulanık benzerlik |
| Kurallı çıkarım | Serbest metin |
| Provenance zinciri | Tek parça özet |

**Karar:** Şema önce — ontologi olmadan graf genelde çöker.

## Code Examples

**Mini şema:**

```text
[GRAPH] nodes: Service, Owner, Ticket | edges: DEPENDS_ON, OWNED_BY
example_path: Ticket#123 -[:BLOCKED_BY]-> Service#api
```

## Anti-Patterns

- **Her şeyi tek “related” kenarı:** İlişki türü şart.
- **Döngüsel ontologi drift:** Versiyonla ve migration planı yaz.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [W3C RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [Neo4j Cypher manual](https://neo4j.com/docs/cypher-manual/) — property graph
- [OWL overview](https://www.w3.org/OWL/) — ontologi
