#!/usr/bin/env python3
"""Generate knowledge/*.md + _index.md for mega-prompt W14 (3d-cad) and W15 (unity backend skeleton)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

SECTION = """## Quick Reference
| Kavram | Not |
|--------|-----|
| Temel kullanım | Bu konu {slug} bağlamında |
| Risk | Doğrulanmadan prod/build'e taşıma |

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
- [Reference](https://example.com/ref) — bağlamsal
- [Community](https://example.com/wiki) — doğrula
"""

# W14: E6/E7 skipped (DO NOT TOUCH per manifest)
SPECS: list[tuple[str, list[str]]] = [
    ("3d-cad/3d-concept-planner", ["3d-scene-composition.md", "reference-gathering.md", "lighting-setup-guide.md", "camera-angle-patterns.md"]),
    ("3d-cad/blender-script-agent", ["bpy-api-patterns.md", "geometry-nodes-guide.md", "shader-nodes-recipes.md", "export-pipeline.md"]),
    ("3d-cad/cad-automation", ["autocad-scripting.md", "parametric-design-patterns.md", "technical-drawing-standards.md", "stl-export-optimization.md"]),
    ("3d-cad/render-pipeline", ["render-queue-management.md", "batch-render-setup.md", "render-farm-patterns.md", "output-format-guide.md"]),
    ("3d-cad/3d-asset-optimizer", ["polygon-reduction-methods.md", "texture-optimization.md", "gltf-draco-compression.md", "lod-generation.md"]),
    ("3d-cad/unity-level-designer", ["terrain-tools-guide.md", "probuilder-patterns.md", "tilemap-2d-3d.md", "scene-management-strategies.md"]),
    ("3d-cad/unity-cinematic-director", ["timeline-advanced-patterns.md", "cinemachine-rig-recipes.md", "cutscene-pipeline.md", "unity-recorder-guide.md"]),
    ("3d-cad/unity-lighting-artist", ["lightmap-baking-guide.md", "light-probe-placement.md", "reflection-probe-setup.md", "volumetric-effects.md"]),
    ("3d-cad/unity-terrain-specialist", ["terrain-sculpting-tools.md", "vegetation-system.md", "terrain-streaming.md", "grass-rendering-optimization.md"]),
    ("3d-cad/unity-rigging-skinning", ["avatar-humanoid-setup.md", "animation-rigging-package.md", "ik-constraint-patterns.md", "blend-shape-workflow.md"]),
    # W15 B24–B52 (B22/B23 klasörleri script dışında — dokunma)
    ("backend/unity-ai-navigation", ["navmesh-setup-guide.md", "behavior-tree-patterns.md", "state-machine-ai.md", "pathfinding-algorithms.md"]),
    ("backend/unity-ar-xr", ["arfoundation-guide.md", "xr-interaction-toolkit.md", "meta-quest-development.md", "hand-tracking-patterns.md"]),
    ("backend/unity-audio", ["audio-mixer-architecture.md", "fmod-wwise-comparison.md", "spatial-audio-guide.md", "adaptive-music-system.md"]),
    ("backend/unity-physics", ["physx-configuration.md", "collision-layer-matrix.md", "joint-types-guide.md", "raycast-patterns.md"]),
    ("backend/unity-save-serialization", ["save-system-architecture.md", "json-binary-serialization.md", "cloud-save-patterns.md", "playerprefs-alternatives.md"]),
    ("backend/unity-localization", ["localization-package-guide.md", "string-table-management.md", "rtl-support.md", "asset-localization.md"]),
    ("backend/unity-editor-tooling", ["custom-inspector-guide.md", "editor-window-patterns.md", "property-drawer-recipes.md", "scriptable-wizard.md"]),
    ("backend/unity-procedural-generation", ["noise-algorithms.md", "wave-function-collapse.md", "dungeon-generation.md", "seed-based-generation.md"]),
    ("backend/unity-mobile-optimizer", ["il2cpp-optimization.md", "adaptive-performance.md", "thermal-throttling.md", "mobile-memory-budget.md"]),
    ("backend/unity-console-platform", ["platform-abstraction-layer.md", "trc-xr-compliance.md", "input-remapping-guide.md", "platform-specific-code.md"]),
    ("backend/unity-ecs-dots", ["entities-component-guide.md", "system-lifecycle.md", "burst-compiler-guide.md", "job-system-patterns.md"]),
    ("backend/unity-2d-specialist", ["sprite-renderer-guide.md", "2d-physics-patterns.md", "spine-animation.md", "pixel-perfect-setup.md"]),
    ("backend/unity-input-system", ["input-action-maps.md", "rebinding-ui.md", "multi-device-support.md", "touch-gesture-patterns.md"]),
    ("backend/unity-camera-systems", ["cinemachine-advanced-rigs.md", "split-screen-setup.md", "camera-stacking.md", "custom-camera-controller.md"]),
    ("backend/unity-memory-manager", ["memory-profiler-workflow.md", "gc-optimization.md", "native-containers-guide.md", "object-pooling-patterns.md"]),
    ("backend/unity-testing", ["playmode-test-guide.md", "editmode-test-patterns.md", "performance-test-framework.md", "test-automation-ci.md"]),
    ("backend/unity-cloud-services", ["remote-config-guide.md", "cloud-save-setup.md", "unity-economy-package.md", "leaderboard-implementation.md"]),
    ("backend/unity-monetization", ["iap-implementation.md", "unity-ads-integration.md", "ad-mediation.md", "receipt-validation.md"]),
    ("backend/unity-security-anticheat", ["code-obfuscation-tools.md", "memory-protection.md", "server-side-validation.md", "cheat-detection-patterns.md"]),
    ("backend/unity-accessibility", ["screen-reader-unity.md", "colorblind-mode.md", "input-accessibility.md", "subtitle-system.md"]),
    ("backend/unity-dialogue-system", ["dialogue-tree-patterns.md", "ink-integration.md", "yarn-spinner-guide.md", "localized-dialogue.md"]),
    ("backend/unity-inventory-crafting", ["inventory-system-design.md", "item-database-scriptableobject.md", "crafting-recipe-system.md", "drag-drop-ui.md"]),
    ("backend/unity-combat-system", ["hitbox-hurtbox-system.md", "damage-calculation.md", "combo-system-design.md", "status-effect-framework.md"]),
    ("backend/unity-quest-mission", ["quest-tracking-system.md", "objective-framework.md", "reward-distribution.md", "quest-graph-editor.md"]),
    ("backend/unity-game-economy", ["virtual-currency-design.md", "reward-loop-patterns.md", "gacha-probability.md", "progression-curve.md"]),
    ("backend/unity-state-machine", ["fsm-patterns-unity.md", "hierarchical-state-machine.md", "scriptableobject-states.md", "game-state-management.md"]),
    ("backend/unity-dependency-injection", ["zenject-guide.md", "vcontainer-patterns.md", "service-locator-vs-di.md", "testability-patterns.md"]),
    ("backend/unity-asset-workflow", ["addressables-advanced.md", "asset-bundle-strategies.md", "asset-postprocessor.md", "import-preset-management.md"]),
    ("backend/unity-streaming-open-world", ["scene-streaming-patterns.md", "additive-scene-loading.md", "world-partitioning.md", "async-loading-strategies.md"]),
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
    print(f"W14+W15: wrote knowledge for {len(SPECS)} agents")


if __name__ == "__main__":
    main()
