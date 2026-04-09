# Learnings

- Claude Code leads in reasoning quality (SWE-bench) but is Claude-only — trade-off is model lock-in for optimization depth
- Devin's parallel sessions (Feb 2026) made it the most autonomous but at $500/mo it's 50x Copilot's price
- CrewAI is 40% faster to production than LangGraph but LangGraph wins for complex stateful systems
- AutoGen is in maintenance mode (Microsoft shifted to MS Agent Framework) — avoid for new projects
- MemPalace scored 100% hybrid on LongMemEval and is free/local — strong candidate for our stack
- Our file-based memory (MEMORY.md) is the simplest approach; evaluate MemPalace if cross-session needs grow
- Free model availability rotates — always test before relying, never hardcode a specific free model
- 5-axis scoring (quality/cost/speed/autonomy/integration) with weights prevents single-dimension bias
