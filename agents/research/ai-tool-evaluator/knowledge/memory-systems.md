---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# AI Memory Systems Comparison

## Landscape (April 2026)

| System | Architecture | Price | LongMemEval Score | Best For |
|--------|-------------|-------|-------------------|----------|
| MemPalace | Local, verbatim storage | Free | 96.6% (raw), 100% (hybrid) | Privacy, zero-cost, local-first |
| Mem0 | Vector + graph (cloud) | $19-249/mo | High | Personalization, managed service |
| Zep | Temporal knowledge graph | $25+/mo | High | Entity relationships over time |
| LangMem | Flat key-value + vector | Free (self-hosted) | Medium | LangGraph integration |

## Detailed Analysis

### MemPalace
- Runs entirely locally — zero API costs
- Stores conversations verbatim (no lossy compression)
- Highest free-tier benchmark score
- Weakness: no cloud sync, manual setup

### Mem0
- Memory compression engine — 80% prompt token reduction claimed
- Both open-source and managed cloud
- Best for: user preference learning, personalization
- Weakness: cloud cost, compression can lose nuance

### Zep
- Temporal knowledge graph — tracks how facts change over time
- Entity extraction and relationship modeling
- Best for: apps needing "what changed when"
- Weakness: complexity, cost

### LangMem
- Simplest architecture — flat key-value with vector search
- No entity extraction or relationship modeling
- Free, self-hosted, full data ownership
- Best for: LangChain/LangGraph shops wanting basic memory
- Weakness: no temporal reasoning, no graph relationships

## Architectural Categories

```
Vector-first:        LangMem, SuperLocalMemory
Vector + graph:      Mem0, Zep, Cognee
Verbatim storage:    MemPalace
Temporal graph:      Zep (leader)
```

## Selection Guide

```
Need free + local + privacy?          → MemPalace
Need managed personalization?         → Mem0
Need temporal entity tracking?        → Zep
Need LangGraph integration?           → LangMem
Need zero-cost + good benchmarks?     → MemPalace
```

## Our Stack

We use file-based memory (MEMORY.md, learnings.md) — simplest possible approach.
MemPalace worth evaluating for cross-session memory if file-based becomes insufficient.

## Evaluation Criteria

1. **Cost** — free/local vs paid cloud
2. **Accuracy** — LongMemEval benchmark scores
3. **Privacy** — local vs cloud data residency
4. **Integration** — compatibility with our agent stack
5. **Complexity** — setup and maintenance burden
