---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Agent Communication

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

## Communication Models

| Model | Mechanism | Coupling | Example |
|-------|-----------|---------|---------|
| **Artifact passing** | Shared files on disk | Loose | Agent A writes spec.md, Agent B reads it |
| **Return value** | Sub-agent returns summary | Medium | Claude sub-agent reports findings |
| **Message queue** | Structured messages | Medium | AutoGen GroupChat turns |
| **Direct handoff** | Agent transfers control | Tight | Swarm handoff function |
| **Shared state** | Mutable state object | Tight | LangGraph state dict |

## Delegation Patterns

### 1. Task Delegation (Fan-Out)
```
Orchestrator: "Review these 3 files for security issues"
  → Sub-agent 1: reviews auth.py → returns findings
  → Sub-agent 2: reviews api.py → returns findings
  → Sub-agent 3: reviews db.py → returns findings
Orchestrator: merges findings into report
```

### 2. Expertise Handoff (Router)
```
Router: classifies request as "database question"
  → Hands off to DB specialist agent
  → Specialist completes task, returns result
  → Router returns result to user
```

### 3. Pipeline Handoff (Sequential)
```
Spec Agent → writes spec.md
Plan Agent → reads spec.md, writes plan.md
Code Agent → reads plan.md, writes implementation
Test Agent → reads implementation, writes tests
```

## Artifact Passing Protocol (Claude Code)

The filesystem is the message bus:

1. **Agent A** writes structured output to a known path
2. **Agent B** reads from that path when it starts
3. **Convention over configuration** — paths are predictable:
   - `specs/{feature}/spec.md` — specification
   - `specs/{feature}/plan.md` — implementation plan
   - `specs/{feature}/tasks.md` — task breakdown
   - `progress/{project}.json` — status tracking

### Benefits
- Naturally version-controlled (git)
- Human-readable and editable
- No serialization/deserialization overhead
- Works across sessions (persistent)

## Sub-Agent Communication in Claude Code

- Sub-agents receive: a prompt describing the task + tool access
- Sub-agents return: a text summary of findings/actions
- Sub-agents **cannot**: access parent's conversation history
- Sub-agents **cannot**: spawn their own sub-agents
- Max 7 parallel sub-agents

## Error Handling in Agent Communication

| Failure Mode | Mitigation |
|-------------|-----------|
| Agent times out | Set explicit timeout; fallback to simpler approach |
| Agent returns garbage | Validate output schema before accepting |
| Agent contradicts another | Orchestrator resolves conflicts with priority rules |
| Handoff drops context | Include summary in handoff message, not just "continue" |
| Circular delegation | Prevent sub-agent re-delegation; max depth = 1 |

## Best Practices

1. **Prefer artifacts over messages** — files survive session crashes
2. **Include context in handoffs** — don't assume the next agent knows anything
3. **Define output contracts** — what structure must the response have?
4. **Keep delegation shallow** — 1 level of sub-agents, not recursive trees
5. **Log handoffs** — track which agent did what for debugging
