---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Artifact Hand-off

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

## Principle

Every pipeline phase produces artifacts. Artifacts are files, not memory. The next phase reads them as input.

## Standard Artifacts

| Phase | Output Artifact | Format |
|-------|----------------|--------|
| Define | `spec.md` | Markdown with user stories, requirements |
| Plan | `plan.md` | Tech stack, architecture, file structure |
| Tasks | `tasks.md` | Ordered checklist with IDs, paths, dependencies |
| Build | Source code + commits | Code files, git history |
| Review | Review report | Structured findings with severity |
| Ship | PR / release | Git branch, merged PR |

Supporting artifacts:
- `data-model.md` — entities and relationships
- `contracts/` — API specifications
- `research.md` — technical decisions
- `checklists/*.md` — validation checklists
- `feature.json` — metadata (feature directory path)

## Hand-off Rules

### 1. File-Based, Not Memory-Based

```
# GOOD: Phase reads artifact file
plan.md references spec.md sections
tasks.md generated from plan.md + spec.md

# BAD: Implicit memory passing
"Remember what we discussed about auth"
```

### 2. Each Artifact is Self-Contained

A reader should understand the artifact without conversation context.
Include: what, why, constraints, references to source artifacts.

### 3. Forward References Only

```
spec.md → plan.md → tasks.md → code
         ↑ never backward ↑
```

Later phases reference earlier artifacts. Earlier artifacts don't reference later ones.

### 4. Artifact Discovery

Use `feature.json` or directory conventions so downstream phases find artifacts:

```json
{
  "feature_directory": "specs/003-user-auth"
}
```

The implement command runs a prerequisite script to discover FEATURE_DIR and AVAILABLE_DOCS.

### 5. Format Standards

- **Markdown** for human-readable docs (spec, plan, tasks)
- **JSON** for machine-readable metadata (feature.json, checklists status)
- **Checklist format** for tasks: `- [ ] [T001] [P] [US1] Description with file path`
- **Frontmatter** for metadata: last_updated, status, dependencies

## Inter-Agent Hand-off

When dispatching to sub-agents:

```
Dispatcher → Sub-agent:
  - Task description
  - Relevant artifact paths
  - Constraints and boundaries
  - Expected output format

Sub-agent → Dispatcher:
  - Completed artifact
  - Status (success/failure/blocked)
  - Notes for next agent
```

## Validation at Hand-off

Before accepting an artifact from a prior phase:
1. File exists and is non-empty
2. Required sections are present
3. No unresolved `[NEEDS CLARIFICATION]` markers (or within limit)
4. Checklist items pass (if applicable)

If validation fails → don't proceed. Request the prior phase to fix.
