---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Anti-Patterns — Common Skill Design Mistakes

## 1. The God Skill
**Problem:** One skill tries to do everything — analyze, plan, implement, review, deploy.
**Fix:** Split into focused skills. The `forge` skill is intentionally a meta-skill that orchestrates others; individual skills should not replicate this pattern.

## 2. Vague Imperatives
**Problem:** "Handle errors appropriately", "Use best practices", "Optimize as needed."
**Fix:** Specify exactly what to do: "On HTTP 4xx, log the error and return a user-friendly message. On 5xx, retry once, then fail with alert."

## 3. Missing Boundaries
**Problem:** Skill description says "manage code quality" but doesn't say what it WON'T touch.
**Fix:** Always include a "Ne yapmaz" / "Does NOT" section. Example from `/refine`: "Yeni ozellik / skill / hook eklemez. Mevcut davranisi degistirmez."

## 4. Placeholder Outputs
**Problem:** Output section says "display results to user" without defining the format.
**Fix:** Include a literal output example with realistic data. Agent will mimic the format.

## 5. Silent Assumptions
**Problem:** Skill assumes CWD is a git repo, or that certain tools exist, without checking.
**Fix:** Add a Phase 0 pre-flight check. Google's skills model this with "ASSUMPTIONS I'M MAKING" blocks that surface assumptions before execution.

## 6. No Error Path
**Problem:** Only the happy path is described. When something fails, agent improvises.
**Fix:** Define fallback behavior per phase. "If no repos found, print 'No changes detected' and exit."

## 7. Trigger Pollution
**Problem:** Too many or too generic triggers cause false activation. A skill triggered by "fix" activates on every bug report.
**Fix:** Use 3-5 specific triggers. Prefer multi-word triggers over single words.

## 8. Copy-Paste Sections
**Problem:** Multiple skills repeat the same commit rules, git safety checks, or output formats.
**Fix:** Extract shared patterns into a referenced skill or a shared section in CLAUDE.md. Use composition (see skill-composition.md).

## 9. Over-Specification
**Problem:** 200+ line skill that micromanages every decision, leaving no room for agent judgment.
**Fix:** Keep skills 40-120 lines. Specify WHAT and WHEN, let the agent decide HOW for obvious steps.

## 10. The Yes-Machine Skill
**Problem:** Skill never tells the agent to push back or ask questions.
**Fix:** Include explicit push-back guidance. Google's meta-skill says: "Sycophancy is a failure mode. Honest technical disagreement is more valuable than false agreement."
