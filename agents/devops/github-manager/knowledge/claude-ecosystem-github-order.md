# Claude ecosystem — GitHub README update order (J10)

Cross-repo marketing and navigation must tell the same story. When refreshing public GitHub surfaces, follow this **fixed order** so visitors always enter from the agent story first, then plugins, then the full OS, then the workspace hub, then the profile.

## Canonical order (do not skip)

| Step | Repository | Role |
|------|------------|------|
| 1 | [claude-agent-catalog](https://github.com/SkyWalker2506/claude-agent-catalog) | **Entry:** agent inventory, dispatch examples, categories — “what you can run” |
| 2 | [claude-marketplace](https://github.com/SkyWalker2506/claude-marketplace) | **Plugins:** install UX, `install.sh`, plugin tables |
| 3 | [claude-config](https://github.com/SkyWalker2506/claude-config) | **Full OS:** install.sh, MCP, skills, hooks, registry, Telegram |
| 4 | [ClaudeHQ](https://github.com/SkyWalker2506/ClaudeHQ) | **Workspace HQ:** multi-project, projects table, how to open `claude` here |
| 5 | Profile README (`SkyWalker2506/SkyWalker2506`) | **Owner card:** one paragraph + same four links in this order |

## Copy rules

- Each README (1–4) must include a short **“Ecosystem”** or **“Related repos”** block listing the other three + HQ + profile hint, with **step 1 linked first**.
- Numbers (agent count, plugin count) drift over time — prefer phrases like **“full inventory in claude-config”** and link to claude-config or catalog for truth; avoid contradicting `config/agent-registry.json` on the same page.
- If internal backlog items remain (e.g. standalone skills), you may describe the **public story as complete** with a single line: *Minor repo-local polish may land in short iterations; behavior matches claude-config main.*

## Per-repo checklist (minimum)

1. **Agent catalog:** H1 title + ecosystem strip + links to marketplace → config → ClaudeHQ.
2. **Marketplace:** Ecosystem strip with catalog **first**, then config, ClaudeHQ, SDK market optional.
3. **claude-config:** “Ecosystem on GitHub” ordered list matching this doc.
4. **ClaudeHQ:** Ecosystem table rows ordered 1–4 (catalog → marketplace → config → HQ extras).
5. **Profile:** 4 links in order; one sentence each.

## Profile repo (if missing)

```bash
gh repo view SkyWalker2506/SkyWalker2506 >/dev/null 2>&1 || \
  gh repo create SkyWalker2506/SkyWalker2506 --public --description "Musab Kara — Claude ecosystem"
# README.md: short bio + links in order above
```

## When to load this doc

- Any task: “update our GitHub pages”, “align READMEs”, “Claude ecosystem marketing”.
- After `claude-config` agent registry or plugin registry changes that affect counts — refresh step 1–3 first, then 4–5.
