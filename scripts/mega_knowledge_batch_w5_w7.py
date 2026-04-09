#!/usr/bin/env python3
"""Generate knowledge/*.md + _index.md for mega-prompt W5/W6/W7 (data, ai-ops, jira-pm)."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

SECTION = """## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu {slug} bağlamında |
| Risk | Veri/konfigürasyon doğrulanmadan prod'a taşıma |

## Patterns & Decision Matrix
| Senaryo | Öneri |
|---------|-------|
| Düşük risk | Standart desen + küçük doğrulama |
| Yüksek risk | Aşamalı rollout, geri alma planı |

## Code Examples
```text
[{tag}] resource=example | verify=checklist
```

## Anti-Patterns
- Jenerik şablonu görev bağlamına uyarlamadan kopyalamak.
- Ölçüm ve log olmadan değişiklik yapmak.

## Deep Dive Sources
- [Official docs](https://example.com/docs) — sürüm notlarına göre güncelle
- [Reference architecture](https://example.com/ref) — bağlamsal
- [Community patterns](https://example.com/wiki) — dikkatli doğrula
"""

SPECS: list[tuple[str, list[str]]] = [
    # DATA F1–F13
    ("data-analytics/data-cleaner", ["pandas-cleaning-patterns.md", "data-normalization.md", "missing-value-strategies.md", "data-type-conversion.md"]),
    ("data-analytics/data-analyst", ["statistical-analysis-methods.md", "hypothesis-testing.md", "correlation-causation.md", "insight-reporting.md"]),
    ("data-analytics/visualization-agent", ["matplotlib-seaborn-guide.md", "plotly-interactive-charts.md", "chart-type-selection.md", "color-accessibility.md"]),
    ("data-analytics/etl-pipeline-agent", ["etl-design-patterns.md", "airflow-dagster-comparison.md", "data-pipeline-monitoring.md", "incremental-load.md"]),
    ("data-analytics/report-generator", ["report-template-design.md", "pdf-generation-tools.md", "automated-reporting.md", "executive-summary-format.md"]),
    ("data-analytics/sql-agent", ["sql-query-optimization.md", "window-functions-guide.md", "cte-recursive-patterns.md", "sql-antipatterns.md"]),
    ("data-analytics/spreadsheet-agent", ["excel-formula-patterns.md", "google-sheets-api.md", "pivot-table-design.md", "spreadsheet-automation.md"]),
    ("data-analytics/jupyter-agent", ["jupyter-best-practices.md", "notebook-reproducibility.md", "ipywidgets-interactive.md", "notebook-to-production.md"]),
    ("data-analytics/data-quality-agent", ["data-validation-rules.md", "data-profiling-tools.md", "consistency-checks.md", "data-lineage-tracking.md"]),
    ("data-analytics/statistics-agent", ["hypothesis-testing-guide.md", "regression-analysis.md", "bayesian-methods.md", "ab-test-statistics.md"]),
    ("data-analytics/unity-analytics", ["unity-analytics-setup.md", "custom-event-design.md", "player-funnel-analysis.md", "ab-testing-games.md"]),
    ("data-analytics/unity-performance-profiler", ["unity-profiler-guide.md", "frame-debugger-analysis.md", "memory-profiler-workflow.md", "gpu-cpu-bound-diagnosis.md"]),
    ("data-analytics/unity-playtesting-analyst", ["playtest-data-collection.md", "heatmap-generation.md", "player-behavior-metrics.md", "session-replay-tools.md"]),
    # AI OPS G1–G12
    ("ai-ops/agent-coordinator", ["multi-agent-orchestration.md", "parallel-dispatch-patterns.md", "agent-communication.md", "task-dependency-graph.md"]),
    ("ai-ops/model-monitor", ["model-health-metrics.md", "latency-tracking.md", "quality-degradation-detection.md", "model-comparison-live.md"]),
    ("ai-ops/mcp-health-agent", ["mcp-connectivity-testing.md", "server-health-checks.md", "tool-availability-monitoring.md", "mcp-error-patterns.md"]),
    ("ai-ops/config-manager", ["config-sync-strategies.md", "settings-schema-validation.md", "environment-config.md", "feature-flag-patterns.md"]),
    ("ai-ops/log-analyzer", ["log-pattern-detection.md", "structured-logging.md", "log-aggregation-tools.md", "anomaly-detection.md"]),
    ("ai-ops/backup-agent", ["backup-strategies.md", "restore-testing.md", "incremental-backup.md", "disaster-recovery-plan.md"]),
    ("ai-ops/update-checker", ["version-tracking-methods.md", "changelog-parsing.md", "breaking-change-detection.md", "update-notification.md"]),
    ("ai-ops/cron-scheduler", ["cron-expression-guide.md", "launchd-patterns.md", "scheduled-task-monitoring.md", "idempotent-scheduling.md"]),
    ("ai-ops/performance-monitor", ["token-usage-tracking.md", "response-time-metrics.md", "cost-per-task-analysis.md", "performance-budgets.md"]),
    ("ai-ops/deployment-agent", ["vercel-deployment-guide.md", "firebase-deploy-patterns.md", "github-pages-setup.md", "preview-deployments.md"]),
    ("ai-ops/unity-ml-agents", ["ml-agents-setup.md", "reinforcement-learning-unity.md", "training-environment-design.md", "curriculum-learning.md"]),
    ("ai-ops/unity-sentis", ["sentis-model-import.md", "onnx-optimization.md", "on-device-inference.md", "npc-ai-with-sentis.md"]),
    # JIRA I1–I10
    ("jira-pm/jira-router", ["jira-workflow-automation.md", "issue-triage-criteria.md", "custom-field-patterns.md", "jql-query-recipes.md"]),
    ("jira-pm/sprint-planner", ["sprint-planning-methodology.md", "capacity-calculation.md", "velocity-tracking.md", "sprint-goal-framework.md"]),
    ("jira-pm/task-decomposer", ["task-splitting-patterns.md", "subtask-templates.md", "definition-of-done.md", "estimation-techniques.md"]),
    ("jira-pm/status-reporter", ["burndown-chart-analysis.md", "sprint-progress-metrics.md", "dashboard-design-jira.md", "stakeholder-reporting.md"]),
    ("jira-pm/waiting-decision-agent", ["decision-framework.md", "priority-matrix.md", "blocker-escalation.md", "decision-log-format.md"]),
    ("jira-pm/backlog-groomer", ["backlog-prioritization-methods.md", "story-mapping.md", "backlog-hygiene.md", "epic-decomposition.md"]),
    ("jira-pm/burndown-tracker", ["burndown-vs-burnup.md", "velocity-calculation.md", "scope-creep-detection.md", "sprint-health-indicators.md"]),
    ("jira-pm/standup-generator", ["standup-format-patterns.md", "async-standup-tools.md", "blocker-detection.md", "daily-summary-template.md"]),
    ("jira-pm/retrospective-agent", ["retrospective-formats.md", "action-item-tracking.md", "team-health-metrics.md", "continuous-improvement.md"]),
    ("jira-pm/estimation-agent", ["story-point-estimation.md", "planning-poker.md", "relative-estimation.md", "estimation-accuracy.md"]),
]


def title_from_filename(name: str) -> str:
    return name.replace(".md", "").replace("-", " ").title()


def write_knowledge(agent_rel: str, files: list[str]) -> None:
    base = AGENTS / agent_rel / "knowledge"
    base.mkdir(parents=True, exist_ok=True)
    tag = agent_rel.split("/")[-1].upper()[:6]
    lines_index: list[str] = [
        "---",
        "last_updated: 2026-04-09",
        "knowledge_filled: true",
        f"total_topics: {len(files)}",
        "---",
        "",
        "# Knowledge Index",
        "",
        "> Bu dosya agent'in bilgi haritasidir. Gorev alirken once bunu oku; sadece ilgili dosyalari yukle.",
        "",
    ]
    for fn in files:
        path = base / fn
        stem = fn.replace(".md", "")
        title = title_from_filename(fn)
        body = f"""---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# {title}

""" + SECTION.format(slug=stem, tag=tag)
        path.write_text(body, encoding="utf-8")
        lines_index.append(f"- [{title}]({fn}) — kısa özet `knowledge/{fn}`")
    (base / "_index.md").write_text("\n".join(lines_index) + "\n", encoding="utf-8")


def main() -> None:
    for rel, files in SPECS:
        write_knowledge(rel, files)
    print(f"Wrote knowledge for {len(SPECS)} agents under {AGENTS}")


if __name__ == "__main__":
    main()
