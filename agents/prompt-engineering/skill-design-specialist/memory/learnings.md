# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | Reference repo analysis (agent-skills + spec-kit + claude-config skills)

**Source:** Google agent-skills repo (20 skills), spec-kit repo (templates + spec-driven.md), claude-config global skills (~50 skills)

**Key findings:**

1. **Google skills are educational, ours are operational.** Google writes 100-300 line prose explaining frameworks (5-axis review, gated workflows). Our skills are 40-120 lines of numbered steps with commands. Both valid — different audiences.

2. **"When NOT to Use" is a pattern we should adopt.** Google's `spec-driven-development` explicitly lists when not to apply the skill. Most of our skills lack this, causing false triggers.

3. **Assumption surfacing is critical.** Google's meta-skill (`using-agent-skills`) mandates agents list assumptions before proceeding. This prevents silent wrong turns.

4. **Spec-kit's independent testability per user story** (P1/P2/P3 priority with standalone test criteria) is a powerful pattern for PRD/feature skills.

5. **Our trigger keyword system is unique and effective.** Neither Google nor spec-kit has this — they rely on directory structure for discovery. Our `Triggers: keyword1, keyword2` in the description enables runtime skill matching.

6. **Our argument parsing tables are a differentiator.** Skills like `/forge` map complex input patterns (number + project + flags) to resolved values. Google skills don't take arguments at all.

7. **Composition patterns are implicit.** `/forge` orchestrates 5+ skills but this pattern isn't documented anywhere. Now captured in skill-composition.md knowledge file.

**Applied to:** 6 knowledge files created for skill-design-specialist agent.
