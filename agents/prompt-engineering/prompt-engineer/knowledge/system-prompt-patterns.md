---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# System Prompt Patterns

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

## The Four Pillars

Every effective system prompt has these components:

### 1. Persona

Define WHO the agent is. Sets tone, expertise level, and behavior.

```
You are a senior backend engineer specializing in Node.js and PostgreSQL.
You write minimal, tested code. You never guess — you read the code first.
```

Keep it 1-3 sentences. Longer personas dilute focus.

### 2. Instructions

Define WHAT the agent does. Action-oriented, imperative.

```
## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint --fix`

## Workflow
1. Read the task spec
2. Load relevant source files
3. Write failing test
4. Implement minimum code to pass
5. Run full test suite
6. Commit with descriptive message
```

### 3. Constraints (Boundaries)

Define what the agent must NOT do.

```
## Boundaries
- Never commit .env files or secrets
- Never add dependencies without checking bundle size
- Ask before modifying database schema
- Always run tests before committing
```

Constraints prevent the most expensive mistakes. Prioritize by damage potential.

### 4. Output Format

Define HOW responses should be structured.

```
## Response Format
- 3-6 word sentences; no filler
- Run tools first → show result → stop
- No unnecessary explanation
- Code/commit in English, conversation in Turkish
```

## Composition Order

```
persona → instructions → constraints → output format
```

This order matters: identity first, then capabilities, then limits, then style.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Novel-length persona | Agent loses focus | 1-3 sentences max |
| Vague instructions | "Be helpful" | Specific actions: "Read file, then edit" |
| No constraints | Agent does risky things | Add top 5 damage-prevention rules |
| Conflicting rules | Agent picks randomly | Resolve conflicts, add priority order |
| Too many rules | Attention diluted | Keep under 50 lines for core rules |

## Real-World Example

Our claude-config CLAUDE.md follows this pattern:
- Persona: proactive, decisive, minimal questions
- Instructions: tool-first, cost-aware model selection
- Constraints: no secrets in output, ask for dangerous ops
- Format: short sentences, Turkish to user, English for code
