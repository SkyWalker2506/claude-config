#!/usr/bin/env python3
"""Generate knowledge/*.md + _index.md for mega-prompt W2/W3/W4 (code-review, design, devops)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

SECTION = """## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu {slug} bağlamında |
| Risk | Doğrulanmadan prod'a taşıma |

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
    # CODE REVIEW C1–C6
    ("code-review/lint-format-hook", ["eslint-prettier-config.md", "dart-analysis-options.md", "pre-commit-hook-setup.md", "auto-fix-strategies.md"]),
    ("code-review/security-scanner-hook", ["secret-scanning-tools.md", "sast-integration.md", "dependency-audit-automation.md", "trivy-snyk-comparison.md"]),
    ("code-review/local-ai-reviewer", ["ai-review-prompts.md", "review-checklist-patterns.md", "severity-classification.md", "false-positive-handling.md"]),
    ("code-review/code-rabbit-agent", ["coderabbit-configuration.md", "review-rule-customization.md", "ci-integration-patterns.md", "review-comment-format.md"]),
    ("code-review/ci-review-agent", ["github-pr-review-api.md", "review-automation-workflow.md", "merge-criteria.md", "status-check-patterns.md"]),
    ("code-review/human-review-coordinator", ["review-routing-rules.md", "reviewer-expertise-matching.md", "review-sla-tracking.md", "escalation-criteria.md"]),
    # DESIGN D3–D13 (D6 image-prompt-generator repo'da yok)
    ("design/stitch-coordinator", ["design-to-code-workflow.md", "tailwind-component-patterns.md", "responsive-breakpoints.md", "css-grid-flexbox-decision.md"]),
    ("design/figma-assistant", ["figma-api-patterns.md", "design-token-extraction.md", "component-inventory.md", "figma-to-code-pipeline.md"]),
    ("design/presentation-builder", ["slide-design-principles.md", "keynote-powerpoint-api.md", "data-visualization-slides.md", "storytelling-frameworks.md"]),
    ("design/icon-asset-agent", ["svg-optimization.md", "sprite-sheet-generation.md", "responsive-image-formats.md", "favicon-manifest-setup.md"]),
    ("design/mockup-reviewer", ["ux-audit-checklist.md", "accessibility-wcag-guide.md", "contrast-ratio-tools.md", "touch-target-guidelines.md"]),
    ("design/brand-identity-agent", ["brand-guide-structure.md", "color-theory-palettes.md", "typography-pairing.md", "voice-tone-framework.md"]),
    ("design/unity-ui-developer", ["ui-toolkit-vs-ugui.md", "uss-uxml-patterns.md", "responsive-layout-strategies.md", "runtime-data-binding.md"]),
    ("design/unity-ux-flow", ["game-ux-patterns.md", "tutorial-system-design.md", "menu-flow-architecture.md", "player-onboarding.md"]),
    ("design/unity-hud-minimap", ["hud-design-patterns.md", "minimap-implementation.md", "damage-indicator-systems.md", "waypoint-compass-systems.md"]),
    # DEVOPS J1–J9, J11–J12 (J10 github-manager — dokunma)
    ("devops/docker-agent", ["dockerfile-best-practices.md", "docker-compose-patterns.md", "multi-stage-builds.md", "container-security.md"]),
    ("devops/cloud-deploy-agent", ["cloud-deployment-strategies.md", "terraform-patterns.md", "cloud-provider-comparison.md", "zero-downtime-deploy.md"]),
    ("devops/ssl-dns-agent", ["ssl-certificate-management.md", "dns-configuration-patterns.md", "lets-encrypt-automation.md", "cdn-dns-setup.md"]),
    ("devops/server-monitor", ["uptime-monitoring-tools.md", "health-check-endpoints.md", "alerting-best-practices.md", "dashboard-design.md"]),
    ("devops/cost-optimizer", ["cloud-cost-optimization.md", "right-sizing-strategies.md", "reserved-vs-spot-instances.md", "cost-monitoring-tools.md"]),
    ("devops/firebase-agent", ["firestore-data-modeling.md", "firebase-auth-patterns.md", "cloud-functions-best-practices.md", "firebase-hosting-rules.md"]),
    ("devops/incident-responder", ["incident-response-playbook.md", "root-cause-analysis-framework.md", "rollback-strategies.md", "post-mortem-template.md"]),
    ("devops/infrastructure-planner", ["capacity-planning-methods.md", "infrastructure-as-code.md", "scaling-strategies.md", "disaster-recovery.md"]),
    ("devops/performance-load-tester", ["k6-load-testing.md", "artillery-patterns.md", "stress-test-methodology.md", "performance-baseline.md"]),
    (
        "devops/unity-devops",
        [
            "gameci-github-actions.md",
            "unity-cloud-build.md",
            "addressables-ci-pipeline.md",
            "build-size-optimization.md",
            "platform-build-matrix.md",
        ],
    ),
    ("devops/unity-version-control", ["plastic-scm-guide.md", "unity-lfs-strategies.md", "merge-prefab-scene.md", "lock-file-patterns.md"]),
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
