---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Quality Standards — Scoring and Review Checklist

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

## Skill Quality Rubric

Score each axis 1-5. A production skill scores 4+ on all axes.

### 1. Clarity (Can an agent follow this without ambiguity?)
- 5: Every step is concrete, no interpretation needed
- 3: Most steps clear, some vague phrases ("handle appropriately")
- 1: Agent must guess what to do at multiple points

### 2. Completeness (Does it cover the full workflow?)
- 5: All phases, error paths, edge cases, output format defined
- 3: Happy path covered, some gaps in error handling
- 1: Only describes the concept, not the execution

### 3. Boundaries (Does it stay in its lane?)
- 5: Explicit "does NOT do" section, clear scope limits
- 3: Implicit boundaries, some overlap with other skills
- 1: Scope creep — tries to do everything

### 4. Actionability (Commands, not concepts?)
- 5: Includes actual commands, file paths, tool references
- 3: Mix of concrete steps and abstract guidance
- 1: Pure theory — "consider the implications of..."

### 5. Testability (Can you verify it worked?)
- 5: Output format defined, success/failure criteria clear
- 3: Some output defined, unclear when to consider it done
- 1: No way to verify correct execution

## Pre-Ship Checklist

Before merging a new skill:

- [ ] Frontmatter has `name`, `description`, triggers
- [ ] At least 3 usage examples in Usage section
- [ ] Flow has numbered phases with concrete steps
- [ ] Output format specified with realistic example
- [ ] Boundaries section states what it does NOT do
- [ ] No overlap with existing skills (check `ls ~/.claude/skills/`)
- [ ] Argument parsing documented if skill takes args
- [ ] Error handling defined (what happens when a phase fails?)
- [ ] Tested manually at least once end-to-end
- [ ] Under 120 lines (if longer, consider splitting)

## Google Agent-Skills Quality Signals

From the reference repo, high-quality skills share these traits:
- **"When to Use" + "When NOT to Use"** — reduces false triggers
- **Concrete code examples** — not pseudocode, real syntax
- **Multi-axis frameworks** — e.g., code-review uses 5 axes (correctness, readability, architecture, security, performance)
- **Push-back guidance** — tells agent when to say "no" or ask questions
- **Assumption surfacing** — agents list assumptions before proceeding
