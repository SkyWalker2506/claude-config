---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Multi-Agent Frameworks Comparison

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

## Framework Overview

| Framework | Architecture | Best For | Learning Curve | Production Ready |
|-----------|-------------|----------|---------------|-----------------|
| **CrewAI** | Role-based crews | Business workflows, rapid prototyping | Low (20 lines to start) | Medium |
| **AutoGen/AG2** | Conversational GroupChat | Multi-party debates, consensus | Medium | Medium (AG2 rewrite maturing) |
| **LangGraph** | Directed graph + conditional edges | Complex orchestration, long-running | High | High (LangSmith, checkpointing) |
| **OpenAI Swarm/Agents SDK** | Handoff functions | Simple routing, stateless pipelines | Low | High (Agents SDK) |
| **Claude Code Sub-Agents** | Spawned instances | Parallel investigation, code tasks | Low | High (native) |

## CrewAI

- **Model**: Role-based DSL — define agents with role/goal/backstory, group into crews
- **Process types**: Sequential, hierarchical, or custom
- **Strength**: Fastest to prototype; maps to org-chart mental model
- **Weakness**: No checkpointing, coarse error handling, limited agent-to-agent direct messaging
- **Scaling trap**: Teams often start here then migrate to LangGraph for production state management

## AutoGen / AG2

- **Model**: Agents converse in GroupChat; each turn is a full LLM call with accumulated history
- **Strength**: Most diverse conversation patterns — group debates, sequential dialogues
- **Weakness**: Expensive at scale — 4 agents x 5 rounds = 20+ LLM calls minimum
- **Best when**: Thoroughness matters more than speed; offline quality-sensitive workflows

## LangGraph

- **Model**: State machine with nodes (agents/tools) and conditional edges
- **Strength**: Durable execution, human-in-the-loop, streaming, parallel branches
- **Checkpointing**: Built-in persistence for long-running workflows
- **Observability**: LangSmith integration for tracing and debugging
- **Best when**: Multiple decision points, conditional routing, production-grade needs

## OpenAI Swarm → Agents SDK

- **Core idea**: Agent = system prompt + functions. Handoff = function returning another agent
- **Swarm**: Educational/deprecated. Agents SDK (March 2025) is production successor
- **Stateless**: Each `run()` starts fresh — no hidden state management
- **Best when**: Clean routing between specialized agents, minimal overhead

## Claude Code Sub-Agents

- **Model**: Main agent spawns up to 7 parallel sub-agent instances
- **Each sub-agent**: Own context window, works independently, returns summary
- **Constraint**: Sub-agents cannot spawn sub-agents (no infinite nesting)
- **Agent Teams**: Advanced mode — team lead coordinates teammates with shared task list
- **Best when**: Parallel code investigation, independent file analysis, codebase exploration

## Decision Matrix

| Need | Choose |
|------|--------|
| Quick prototype, role-based | CrewAI |
| Production orchestration with state | LangGraph |
| Multi-party reasoning/debate | AutoGen |
| Lightweight stateless routing | Agents SDK |
| Parallel code tasks in Claude | Sub-Agents |
| Cost-sensitive, high volume | Agents SDK or Sub-Agents |
