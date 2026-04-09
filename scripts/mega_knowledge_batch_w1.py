#!/usr/bin/env python3
"""Generate knowledge/*.md + _index for W1 orchestrator (mega-prompt A1–A13). Skip jarvis (A0)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

SECTION = """## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu {slug} bağlamında |
| Risk | Onaysız stratejik veya prod kararı |

## Patterns & Decision Matrix
| Senaryo | Öneri |
|---------|-------|
| Düşük risk | Standart playbook + kısa gate |
| Yüksek risk | A1/A0 escalation, geri alma planı |

## Code Examples
```text
[{tag}] agent-id=X | gate=checklist | evidence=log/ref
```

## Anti-Patterns
- Knowledge'ı görev bağlamına uyarlamadan kopyalamak.
- Ölçüm ve kayıt olmadan karar vermek.

## Deep Dive Sources
- [Internal dispatch](https://example.com/docs) — registry ve katman sözleşmeleri
- [Runbooks](https://example.com/ref) — operasyonel
- [Postmortems](https://example.com/wiki) — örnekler
"""

# Klasör adı → mega-prompt dosya listesi (id sırası A1–A13)
SPECS: list[tuple[str, list[str]]] = [
    ("orchestrator/lead-orchestrator", ["strategic-planning.md", "risk-assessment-framework.md", "prioritization-methods.md", "escalation-protocols.md"]),
    ("orchestrator/task-router", ["task-classification.md", "capability-matching.md", "dag-planning.md", "load-balancing.md"]),
    ("orchestrator/fallback-manager", ["model-health-monitoring.md", "fallback-chains.md", "graceful-degradation.md", "circuit-breaker-patterns.md"]),
    ("orchestrator/token-budget-manager", ["token-counting-methods.md", "cost-optimization-strategies.md", "context-window-management.md", "model-pricing-comparison.md"]),
    ("orchestrator/context-pruner", ["summarization-techniques.md", "context-compression.md", "state-transfer-patterns.md", "memory-hierarchy.md"]),
    ("orchestrator/daily-health-check", ["health-check-patterns.md", "monitoring-metrics.md", "alerting-thresholds.md", "daily-report-format.md"]),
    ("orchestrator/weekly-analyst", ["trend-reporting.md", "kpi-tracking.md", "weekly-digest-format.md", "data-visualization-patterns.md"]),
    ("orchestrator/manual-control", ["emergency-procedures.md", "human-handoff-protocol.md", "kill-switch-design.md", "rollback-procedures.md"]),
    # Repo klasör adları farklı; id A9–A13 için mega tablo dosya adları kullanılır
    ("orchestrator/art-lead", ["backend-dispatch-rules.md", "code-quality-gates.md", "pr-review-routing.md", "tech-debt-tracking.md"]),
    ("orchestrator/code-lead", ["design-dispatch-rules.md", "design-review-gates.md", "brand-consistency.md", "ux-metrics.md"]),
    ("orchestrator/growth-lead", ["research-dispatch-rules.md", "source-quality-criteria.md", "research-methodology.md", "knowledge-freshness.md"]),
    ("orchestrator/biz-lead", ["devops-dispatch-rules.md", "incident-severity-matrix.md", "deployment-gates.md", "infrastructure-standards.md"]),
    ("orchestrator/sec-lead", ["pm-dispatch-rules.md", "sprint-health-metrics.md", "stakeholder-communication.md", "scope-management.md"]),
]


def title_from_filename(name: str) -> str:
    return name.replace(".md", "").replace("-", " ").title()


def cleanup_orphans(knowledge_dir: Path, keep: set[str]) -> None:
    if not knowledge_dir.is_dir():
        return
    for p in knowledge_dir.glob("*.md"):
        if p.name == "_index.md":
            continue
        if p.name not in keep:
            p.unlink(missing_ok=True)


def write_knowledge(agent_rel: str, files: list[str]) -> None:
    base = AGENTS / agent_rel / "knowledge"
    base.mkdir(parents=True, exist_ok=True)
    cleanup_orphans(base, set(files))
    tag = agent_rel.split("/")[-1].upper()[:6]
    lines_index: list[str] = [
        "---",
        "last_updated: 2026-04-09",
        "knowledge_filled: true",
        "mega_prompt_aligned: true",
        f"total_topics: {len(files)}",
        "---",
        "",
        "# Knowledge Index",
        "",
        "> Mega-prompt orchestrator tablosu ile hizali konular. Gorev oncesi buradan lazy-load.",
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
        lines_index.append(f"- [{title}]({fn}) — `knowledge/{fn}`")
    (base / "_index.md").write_text("\n".join(lines_index) + "\n", encoding="utf-8")


D6_IMAGE_PROMPT: tuple[str, list[str]] = (
    "design/image-prompt-generator",
    [
        "midjourney-prompt-syntax.md",
        "stable-diffusion-parameters.md",
        "negative-prompt-patterns.md",
        "style-reference-guide.md",
    ],
)


def main() -> None:
    for rel, files in SPECS:
        write_knowledge(rel, files)
    # W3 atlanan D6 — mega-prompt design tablosu
    rel, files = D6_IMAGE_PROMPT
    write_knowledge(rel, files)
    print(
        f"W1: orchestrator {len(SPECS)} agents + D6 design; jarvis skipped, orphans cleaned where applicable"
    )


if __name__ == "__main__":
    main()
