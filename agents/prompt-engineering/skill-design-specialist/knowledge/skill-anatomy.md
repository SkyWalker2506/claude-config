---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Skill Anatomy — Required Sections and Format

## Frontmatter (YAML, required)

Every SKILL.md starts with YAML frontmatter:

```yaml
---
name: skill-name          # kebab-case, matches directory name
description: "One-line purpose. Triggers: keyword1, keyword2."
argument-hint: "[arg1] [--flag]"   # optional, shows usage pattern
---
```

## Required Sections

### 1. Title + One-liner
`# /skill-name — Short Description` — first line after frontmatter.

### 2. Usage Block
Show 3-5 concrete invocation examples with different argument combinations:
```
/skill-name                    # default behavior
/skill-name arg1               # with argument
/skill-name arg1 --dry-run     # with flag
```

### 3. Flow / Steps
Numbered phases describing what the skill does. Each phase should be:
- **Imperative** — "Scan repos", not "Repos are scanned"
- **Concrete** — include actual commands/tools used
- **Gated** — specify what blocks progression to next phase

### 4. Output Format
Define what the skill produces — terminal output, files, commits, PRs.

### 5. Boundaries
What the skill does NOT do. Prevents scope creep.

## Optional Sections

- **Argument Parsing** — table mapping input patterns to resolved values
- **Error Handling** — what to do when phases fail
- **Examples** — before/after or sample outputs

## Key Principles from Reference Skills

1. **One skill = one job.** Google's agent-skills each cover exactly one development phase (e.g., `code-review-and-quality` does review, not implementation).
2. **When to Use / When NOT to Use** — explicitly state both. See `spec-driven-development` skill: "When NOT to use: Single-line fixes, typo corrections."
3. **Actionable over theoretical.** Every section should tell the agent what to DO, not what to think about.
4. **Gate progression.** The spec-driven skill uses `SPECIFY → PLAN → TASKS → IMPLEMENT` with human review between each. Skills should define clear phase gates.

## Our Format vs Google's Format

| Aspect | Google (agent-skills) | Ours (claude-config) |
|--------|----------------------|---------------------|
| Frontmatter | `name` + `description` | + `argument-hint`, triggers in description |
| Language | English prose | Turkish prose, English code |
| Phases | Narrative sections | Numbered steps with commands |
| Output | Implicit | Explicit format section |
| Length | 100-300 lines | 40-120 lines (denser) |
