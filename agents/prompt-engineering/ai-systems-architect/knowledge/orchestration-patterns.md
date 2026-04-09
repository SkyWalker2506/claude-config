---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Orchestration Patterns

## Five Core Patterns

### 1. Orchestrator-Worker (Fan-Out/Fan-In)

- Central orchestrator assigns tasks, workers execute independently, results merge
- **Use when**: Tasks are parallelizable and independent
- **Example**: Code review — spawn reviewers for security, performance, style in parallel
- **Trade-off**: Orchestrator is single point of failure; bottleneck at merge

### 2. Pipeline (Sequential)

- Each stage processes output of previous stage — assembly line model
- **Use when**: Each step depends on previous output (spec → plan → code → test)
- **Example**: SDD workflow: `/specify` → `/plan` → `/tasks` → build → review
- **Trade-off**: Latency proportional to stage count; no parallelism

### 3. Router/Dispatch

- Classifier routes incoming request to specialized agent
- **Use when**: Requests have distinct categories needing different expertise
- **Example**: Support bot routing to billing/technical/account agents
- **Trade-off**: Routing errors cascade; needs good classification

### 4. DAG (Directed Acyclic Graph)

- Tasks with dependency edges — parallel where possible, sequential where required
- **Use when**: Complex workflows with mixed dependencies
- **Example**: Build system — compile modules in parallel, link sequentially
- **Trade-off**: Complexity in dependency management; needs topological sort

### 5. Hierarchical (Tree Delegation)

- Manager delegates to sub-managers who delegate to workers
- **Use when**: Large-scale tasks that decompose recursively
- **Example**: Project lead → feature leads → individual implementers
- **Trade-off**: Communication overhead grows with depth

## Pattern Combinations

Real systems combine patterns:

```
Router → selects pipeline
Pipeline stage 2 → fan-out to 3 workers → fan-in
Pipeline stage 3 → hierarchical delegation
```

## Implementation in Claude Code Ecosystem

| Pattern | Implementation |
|---------|---------------|
| Fan-out/Fan-in | Sub-agents (max 7 parallel) |
| Pipeline | Skill chaining (`/forge` = analysis → sprint → tasks → PR) |
| Router | `/dispatch` skill — analyzes task, selects agent from registry |
| DAG | Task files with `[P]` parallel markers (spec-kit pattern) |
| Hierarchical | Agent Teams — team lead spawns teammates |

## Anti-Patterns

- **Over-orchestration**: Adding coordination layers that cost more tokens than they save
- **Chat-loop**: Agents endlessly discussing instead of producing artifacts
- **Blind fan-out**: Spawning parallel agents without clear merge strategy
- **Missing circuit breakers**: No timeout/retry/fallback when agent fails

## Choosing a Pattern

1. **Start with Pipeline** — simplest, most predictable
2. **Add Fan-Out** when you identify independent subtasks
3. **Use Router** when input types diverge significantly
4. **Reach for DAG** only when dependency graph is complex and well-defined
5. **Avoid Hierarchical** unless task naturally decomposes 3+ levels deep
