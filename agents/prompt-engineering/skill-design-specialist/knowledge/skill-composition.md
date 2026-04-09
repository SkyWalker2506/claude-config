---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Skill Composition — Inter-Skill References and Patterns

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

## Composition Types

### 1. Orchestrator Pattern
A meta-skill calls other skills in sequence. Example: `/forge` orchestrates analysis → sprint-plan → implementation → review → merge.

```
/forge
  ├── /project-analysis
  ├── /sprint-plan
  ├── /yolo (per task)
  ├── /review
  └── /commit-all
```

**Rule:** Orchestrators define the flow and gates. Child skills execute independently — they don't know they're being orchestrated.

### 2. Discovery Pattern
A routing skill examines input and dispatches to the right skill. Example: `/dispatch` analyzes the task, picks an agent, starts a sub-session.

Google's `using-agent-skills` is a pure discovery skill — it maps task types to skills via a decision tree:
```
Task arrives
  ├── Vague idea? → idea-refine
  ├── New feature? → spec-driven-development
  ├── Implementing? → incremental-implementation
  └── Reviewing? → code-review-and-quality
```

### 3. Cross-Reference Pattern
A skill references another for a specific sub-task without invoking it. Example: `code-review-and-quality` says "For detailed security guidance, see `security-and-hardening`."

**Rule:** Use cross-references for optional depth. The skill works standalone; the reference adds detail.

### 4. Shared Behavior Pattern
Multiple skills need the same behavior (e.g., git safety, commit rules). Options:
- **CLAUDE.md globals** — put shared rules in project/global CLAUDE.md
- **Pre-flight phase** — each skill runs the same Phase 0 checks
- **Shared skill** — extract a utility skill (e.g., `/commit-all` used by multiple flows)

**Prefer CLAUDE.md for universal rules**, skill extraction for reusable workflows.

## Composition Rules

1. **No circular dependencies.** If A calls B, B must not call A.
2. **Child skills are stateless.** They don't know their caller. They take input, produce output.
3. **Orchestrators own the gate logic.** The orchestrator decides pass/fail between phases, not the child skill.
4. **Keep nesting shallow.** Max 2 levels deep (orchestrator → skill). If deeper, flatten.
5. **Trigger isolation.** Composed skills must have distinct triggers. `/forge` and `/sprint-plan` must not trigger on the same keywords.

## When to Compose vs. Expand

| Signal | Action |
|--------|--------|
| Skill > 120 lines | Consider splitting into orchestrator + child |
| Two skills share > 30% logic | Extract shared skill or move to CLAUDE.md |
| Skill has 3+ distinct phases | Each phase could be a skill if independently useful |
| Skill is only used inside another | Keep inline — don't extract single-use skills |
