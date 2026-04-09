---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Agent Testing Strategies

## Quick Reference

- **Unit of test** = behavior of the *definition*: Does `AGENT.md` forbid unsafe actions? Do triggers fire on intended phrases only?
- **Levels:** (1) Static lint — frontmatter keys, broken links, placeholder grep; (2) Golden prompts — expected sections in output; (3) Shadow run — human or harness executes a dry task with logging.
- **Metrics:** task success rate, average tool calls, escalation count, time-to-resolution — track per agent version in `memory/sessions.md` or external sheet.
- **Non-determinism:** Use rubric scoring (1–5) on criteria instead of exact string match for free-text outputs.
- **Regression:** When changing Boundaries or Bridge, re-run golden prompts that hit those rules.

**Date context:** 2025–2026 evaluations favor *process adherence* (did it follow Verification?) plus outcome quality.

## Patterns & Decision Matrix

| Goal | Strategy | Cost |
|------|----------|------|
| Prevent placeholder drift | CI grep for “Cursor dolduracak”, “Hangi alanlarla” | Low |
| Validate knowledge depth | Script: each `knowledge/*.md` has `Quick Reference` + `Deep Dive Sources` | Low |
| Behavioral quality | Small fixed task suite (3–5 scenarios per agent) | Medium |
| MCP integration | Contract test: tool list + schema parse | Medium |
| Load | Soak test many parallel sessions | High — usually sample |

**Rubric example (snippet)**

| Criterion | Weight | Score 1 | Score 5 |
|-----------|--------|---------|---------|
| Followed Boundaries | 30% | Violated Never | Clear Always/Never adherence |
| Correct escalation | 20% | Wrong agent | Exact ID + reason |
| Output format | 20% | Missing sections | Matches Output Format |
| Tool discipline | 30% | Random tools | Minimal necessary calls |

## Code Examples

**Placeholder guard (bash — same family as `bin/mega-rollout.sh`):**

```bash
#!/usr/bin/env bash
set -euo pipefail
BAD=$(grep -Rnl "Hangi alanlarla" agents --include='AGENT.md' || true)
if [[ -n "${BAD}" ]]; then
  echo "Bridge placeholders:" "${BAD}"
  exit 1
fi
```

**Golden prompt file `cases/n2_smoke.md` (illustrative):**

```text
You are simulating dispatch of N2 Agent Builder.
Input task: Add MCP server X to agent J10 with stdio transport.
Expected: mentions reading tool schema, env vars, Verification checklist, escalation to G3 for runtime health.
```

**Pytest-style pseudo-test for rubric:**

```python
def test_n2_output_has_verification(output: str) -> None:
    assert "## Verification" in output
    assert "- [ ]" in output
    assert "Bridge" in output or "bridge" in output.lower()
```

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Only happy-path prompts | Misses boundary violations | Add adversarial user prompts |
| Full auto eval without human spot-check | Reward hacking / format gaming | Weekly sample review |
| Testing the LLM not the spec | Changing scores without doc changes | Freeze agent version when comparing |
| Ignoring tool-count regressions | Cost explosion | Alert when median tools > budget |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [OpenAI — Evals guide](https://platform.openai.com/docs/guides/evals) — datasets, grading models, metrics
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — evaluation and workflow testing mindset
- [Google Cloud — Evaluate agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — reliability layers for agent systems
- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — governance and measurement when agents affect risk posture
