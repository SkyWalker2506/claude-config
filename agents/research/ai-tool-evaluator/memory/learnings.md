# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-09 | Web + GitHub Research | Competing Agent System Architectures

**Learned:** 11 agent systems analyzed. Our AGENT.md + knowledge/ + memory/ pattern is closest to GitAgent (open-gitagent/gitagent, 2.6k stars) which uses SOUL.md + agent.yaml + knowledge/ + memory/. No other system combines per-agent personas, knowledge directories, AND persistent memory in a git-native, multi-agent registry.

**Key findings:**
- GitAgent is the only open standard with a comparable file-based agent identity system
- CrewAI has the richest declarative agent fields (25+ params) but requires Python
- Codex AGENTS.md and Cursor .mdc are instruction-injection only — no persona or knowledge layer
- Devin has the most advanced knowledge system (auto-indexes codebase) but is proprietary
- LangGraph memory is the most sophisticated (typed, versioned, graph-backed) but code-only
- Superpowers (142k stars) focuses on workflow skills, not agent identity — complementary to our approach
- AgentSkills spec (15.5k stars) is the foundation we already build on; we extend it with AGENT.md

**How to apply:**
- Consider adopting GitAgent's separation of RULES.md from persona (currently we embed rules in AGENT.md)
- Consider adding a machine-readable agent.yaml alongside AGENT.md for tooling integration
- Our multi-agent registry is a genuine differentiator — no competitor has file-based multi-agent orchestration
- Watch GitAgent closely — most aligned competitor in philosophy
