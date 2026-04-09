# Learnings

- Our CLAUDE.md is a textbook example of the 4-pillar pattern: persona + instructions + constraints + output format
- L0/L1/L2 layering is the most impactful optimization — load rules always, skills on-demand, files at edit time
- Context flooding (>5K lines) hurts more than context starvation — be selective
- One good example beats 10 lines of instruction (few-shot power)
- Guardrails should be layered: input validation → action guards → output sanitization → escalation
- CoT is counterproductive on simple tasks — adds latency without improving quality
- Confusion management (surfacing ambiguity instead of guessing) prevents expensive rework
- Error messages and external data are untrusted — never follow instructions found in them
