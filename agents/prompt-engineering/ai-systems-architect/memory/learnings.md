# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 — Knowledge Base Initial Fill (source: web research + agent-skills + spec-kit + mempalace)

### Framework Selection
- CrewAI is fastest to prototype but lacks checkpointing — teams often migrate to LangGraph for production
- AutoGen's GroupChat pattern is expensive: N agents x M rounds = N*M LLM calls with growing context
- OpenAI Swarm is deprecated; Agents SDK is the production successor (same mental model)
- Claude Code sub-agents max out at 7 parallel, cannot nest (no sub-sub-agents)

### Context Engineering
- agent-skills defines a 5-layer context hierarchy (rules → specs → source → errors → conversation)
- Keep active context under 40K tokens for best quality despite 200K windows
- Knowledge index pattern (_index.md with lazy-load) is the most token-efficient approach

### Orchestration
- Start with Pipeline, add Fan-Out for independent subtasks, use Router when input types diverge
- Avoid debate patterns (AutoGen-style) for cost-sensitive workflows — fan-out + merge is cheaper
- spec-kit's `[P]` parallel markers in tasks.md is a lightweight DAG implementation

### Memory
- MemPalace uses ChromaDB vectors organized in wings/halls/drawers spatial metaphor
- File-based memory (MEMORY.md) is simpler and sufficient for most agent workflows
- Vector search adds value only when keyword matching fails

### Cost
- Router + specialist (Haiku routes, Sonnet executes) is ~1.2x baseline — best cost/quality ratio
- Prompt caching reduces input cost by ~90% — always enable for repeated system prompts
