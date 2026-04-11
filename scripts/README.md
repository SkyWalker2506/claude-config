# Maintenance scripts

## Agent coverage

| Script | Purpose |
|--------|---------|
| `agent_coverage_audit.py` | Scans `agents/**/AGENT.md` + `knowledge/` + `memory/`. Writes `agents/AGENT_COVERAGE_AUDIT.md` with tiers **P0 / P1 / P2 / OK**. |

```bash
python3 scripts/agent_coverage_audit.py
```

Set `CLAUDE_VERIFY_AUDIT=1` to compute metrics **without** overwriting `agents/AGENT_COVERAGE_AUDIT.md` (used by `verify_knowledge_structure.py`).

**Tier rules (short):** P0 = missing index or zero topic files; P1 = thin topics or memory; P2 = missing `## Knowledge map` in `AGENT.md`; OK = all checks pass.

## Knowledge map injection

| Script | Purpose |
|--------|---------|
| `inject_knowledge_maps.py` | Inserts `## Knowledge map` (table of `knowledge/*.md` topics, H1 or humanized filename) immediately before `## Knowledge Index` when the section is missing. |

```bash
python3 scripts/inject_knowledge_maps.py --dry-run   # count only
python3 scripts/inject_knowledge_maps.py             # apply
```

Re-run the audit after injection to confirm **P2 = 0**.

## CI gate (both audits green)

| Script | Purpose |
|--------|---------|
| `verify_knowledge_structure.py` | Runs coverage + quality audits; **exit 1** if P0–P2 not all zero or knowledge not `complete=N/N`. Used by `.github/workflows/knowledge-audit.yml`. |

```bash
python3 scripts/verify_knowledge_structure.py
```

## Source depth (frontmatter)

| Script | Purpose |
|--------|---------|
| `knowledge_sources_audit.py` | Counts `sources: N` in YAML frontmatter; writes `agents/KNOWLEDGE_SOURCES_AUDIT.md` (optional depth metric; not a CI gate). |

```bash
python3 scripts/knowledge_sources_audit.py
```

Respects `CLAUDE_VERIFY_AUDIT=1` (no write), same as other audits.

## Knowledge section coverage (mega-prompt)

| Script | Purpose |
|--------|---------|
| `knowledge_quality_audit.py` | Counts topic files missing `Quick Reference`, `Patterns & Decision Matrix`, `Code Examples`, `Anti-Patterns`, or `Deep Dive Sources`. Writes `agents/KNOWLEDGE_QUALITY_AUDIT.md`. |

```bash
python3 scripts/knowledge_quality_audit.py
```

Set `CLAUDE_VERIFY_AUDIT=1` to skip writing `agents/KNOWLEDGE_QUALITY_AUDIT.md` when verifying.

One-shot batch (historical / rerun only if restoring from git):

- `batch_mr_code_examples.py` — inserts `## Code Examples` into listed `market-research/**/knowledge/*.md` files (already applied on main when present).

- `batch_backend_patterns_anti.py` — inserts `## Patterns & Decision Matrix` / `## Anti-Patterns` for backend gap list; can reorder Anti after Code when needed.

## Observability — `hq` CLI

Production tooling for the agent OS. The `hq` bash dispatcher fans out to focused
Python scripts; all share `CLAUDE_CONFIG_ROOT` discovery (env → script parent → `~/Projects/claude-config`) and write structured reports.

| Script | Purpose |
|--------|---------|
| `hq` | Bash CLI — `dashboard`, `lifecycle`, `optimize`, `plugin-eval`, `events`, `tail`, `stats`, `health` |
| `hq_dashboard.py` | Aggregates 30 days of telemetry into `config/telemetry/aggregated/dashboard.json` |
| `hq_events.py` | Backs `events` / `tail` / `stats <agent_id>` — telemetry inspection helpers |
| `agent_lifecycle.py` | Promote/demote/retire recommendations → `Reports/lifecycle_recommendations.json`. Min 20 samples or `--force` |
| `route_optimizer.py` | Cheaper-model swap suggestions when alt ≥95% of current SR with ≥5 samples |
| `plugin_eval.py` | Grades `ccplugin-*` repos on 11-point rubric (A–F) |
| `log_dispatch.py` | PostToolUse hook — appends one JSONL event per Task/Bash to `config/telemetry/events/<date>.jsonl` |
| `gate_check.py` | PreToolUse hook — runs `config/gates/pre-{commit,push}.json`; warn-only by default, exit 2 to block in `enforce` mode |

```bash
hq dashboard            # Unified system view
hq dashboard --json     # Pipeable JSON
hq dashboard --watch    # Refresh every 60s
hq events --limit 30    # Last 30 dispatches
hq tail -f              # Live event stream
hq stats B2             # Per-agent breakdown
hq lifecycle            # Promote/demote/retire (≥20 events)
hq optimize             # Route optimization suggestions
hq plugin-eval          # Plugin quality grades
hq health               # All of the above in one pass
```

CI: `.github/workflows/hq-tests.yml` runs `tests/test_hq.py` plus a smoke test on every change to `scripts/hq*` or `config/{gates,telemetry}/**`.
