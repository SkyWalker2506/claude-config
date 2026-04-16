---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Orchestration Patterns

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

## 2026 Harness Engineering Research

### Meta-Harness (Stanford, March 2026)

- Automated harness optimization: proposer reads execution traces (~82 files), diagnoses failures, writes new harness
- Haiku with optimized harness outranked Opus on TerminalBench 2
- Self-evolution is THE ONLY consistently helpful module (+4.8 SWE-bench, +2.7 OS World)
- Verifiers actively hurt performance (-0.8 and -8.4 in ablation)
- Multi-candidate search hurt (-2.4 and -5.6)
- Harness optimized on one model transfers to 5 others

### LangChain TerminalBench 2 (rank 30+ to rank 5, harness only)

- Context assembly (feedforward guide): inject env info, tools, best practices upfront
- Self-verification loops: BUILD → TEST → VERIFY → FIX cycle
- Trace-driven debugging: analyze execution traces for patterns
- Loop detection: same tool+args 3x → intervene; 80% budget → warning
- Model-specific tuning per model

### Anthropic's 5 Canonical Patterns

1. Prompt Chaining — sequential for decomposable tasks
2. Routing — classify → specialized handler
3. Parallelization — independent subtasks or voting
4. Orchestrator-Workers — central LLM delegates to workers
5. Evaluator-Optimizer — generate + feedback loop
