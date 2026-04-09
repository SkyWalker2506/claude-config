---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Agent Frameworks Comparison

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

## Top Frameworks (April 2026)

| Framework | Approach | Best For | Maturity |
|-----------|----------|----------|----------|
| LangGraph | Graph-based workflows | Production stateful systems | High |
| CrewAI | Role-based teams | Quick prototyping, team workflows | High |
| AutoGen | Conversational agents | Multi-party agent discussions | Medium (maintenance mode) |
| OpenAI Swarm | Native function calling | Low-latency tool use | Medium |
| LlamaIndex | Data-aware agents | RAG-heavy applications | High |
| Semantic Kernel | Enterprise .NET/Python | Microsoft ecosystem | High |

## Detailed Analysis

### LangGraph
- Workflows as directed graphs (nodes + edges)
- Time-travel debugging, graph visualization
- Most battle-tested for production
- Steeper learning curve
- Best for: complex stateful pipelines with branching logic

### CrewAI
- Agents defined with roles, goals, backstories
- YAML configuration, minimal boilerplate
- 40% faster time-to-production vs LangGraph
- Best for: standard business workflows, parallel task execution

### AutoGen (AG2)
- GroupChat pattern: agents in shared conversation
- Selector determines who speaks next
- Microsoft shifted to maintenance mode (favor MS Agent Framework)
- Best for: research, multi-party agent conversations

### OpenAI Swarm
- Lowest latency — native function calling
- Lightweight, minimal abstraction
- Best for: simple agent chains, OpenAI-native apps

## Selection Guide

```
Need production-grade stateful system?     → LangGraph
Need quick team-based prototype?           → CrewAI
Need multi-party agent conversation?       → AutoGen
Need lowest latency with OpenAI?           → Swarm
Need RAG-heavy data pipeline?              → LlamaIndex
Need Microsoft enterprise integration?     → Semantic Kernel
```

## Our Approach

We use a custom dispatch system (claude-config agents) rather than external frameworks.
Reason: tighter integration with Claude Code, simpler than framework overhead.
Monitor LangGraph for potential adoption if workflow complexity grows.

## Evaluation Criteria

1. **Time-to-production** — how fast can you ship a working agent system
2. **Flexibility** — can it handle your specific workflow pattern
3. **Debugging** — can you inspect agent state and decisions
4. **Community** — docs quality, active maintenance, ecosystem
5. **Lock-in** — model-agnostic vs vendor-locked
