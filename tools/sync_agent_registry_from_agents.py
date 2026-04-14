#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
REGISTRY_PATH = ROOT / "config" / "agent-registry.json"


def _parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
    else:
        inner = value
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    out: list[str] = []
    for p in parts:
        if not p:
            continue
        if (p[0] == p[-1]) and p[0] in ("'", '"'):
            p = p[1:-1]
        out.append(p)
    return out


def _read_agent_frontmatter(path: Path) -> dict[str, Any]:
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"^---\n([\s\S]*?)\n---\n", txt)
    if not m:
        return {}
    fm_raw = m.group(1).splitlines()
    fm: dict[str, Any] = {}
    for line in fm_raw:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # Only parse top-level keys (ignore indented blocks like models:).
        if line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if not v:
            fm[k] = ""
            continue
        if re.fullmatch(r"-?\d+", v):
            fm[k] = int(v)
            continue
        if v.startswith("[") and v.endswith("]"):
            fm[k] = _parse_inline_list(v)
            continue
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            fm[k] = v[1:-1]
            continue
        fm[k] = v
    return fm


def _primary_model_from_tier(tier: str) -> str:
    t = (tier or "mid").lower().strip()
    if t == "senior":
        return "opus"
    if t == "junior":
        return "haiku"
    return "sonnet"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    reg_agents: dict[str, Any] = registry.get("agents", {})

    agent_files = [p for p in AGENTS_DIR.glob("*/*/AGENT.md") if "_template" not in str(p)]
    by_id: dict[str, dict[str, Any]] = {}
    for p in agent_files:
        fm = _read_agent_frontmatter(p)
        agent_id = str(fm.get("id", "")).strip()
        if not agent_id:
            continue
        by_id[agent_id] = {
            "name": str(fm.get("name", "")).strip(),
            "category": str(fm.get("category", p.parent.parent.name)).strip(),
            "tier": str(fm.get("tier", "mid")).strip(),
            "status": str(fm.get("status", "pool")).strip() or "pool",
            "mcps": fm.get("mcps", []),
            "capabilities": fm.get("capabilities", []),
            "max_tool_calls": fm.get("max_tool_calls", None),
        }

    file_ids = set(by_id.keys())
    reg_ids = set(reg_agents.keys())

    # Remove registry entries with no file.
    for rid in sorted(reg_ids - file_ids):
        reg_agents.pop(rid, None)

    # Add or sync registry entries for file-backed agents.
    for aid, meta in by_id.items():
        if aid not in reg_agents:
            reg_agents[aid] = {
                "name": meta["name"] or aid,
                "version": "1.0",
                "category": meta["category"],
                "status": meta["status"],
                "primary_model": _primary_model_from_tier(meta["tier"]),
                "fallbacks": ["sonnet"],
                "mcps": meta["mcps"] if isinstance(meta["mcps"], list) else [],
                "capabilities": meta["capabilities"] if isinstance(meta["capabilities"], list) else [],
                "max_tool_calls": meta["max_tool_calls"] if isinstance(meta["max_tool_calls"], int) else 30,
                "effort": "medium",
                "template": "autonomous",
                "tier": meta["tier"].lower() if meta["tier"] else "mid",
                "model_source": "local-free",
            }
        else:
            entry = reg_agents[aid]
            if meta["name"]:
                entry["name"] = meta["name"]
            if meta["category"]:
                entry["category"] = meta["category"]
            if meta["status"]:
                entry["status"] = meta["status"]
            if isinstance(meta["mcps"], list):
                entry["mcps"] = meta["mcps"]
            if isinstance(meta["capabilities"], list):
                entry["capabilities"] = meta["capabilities"]
            if isinstance(meta["max_tool_calls"], int):
                entry["max_tool_calls"] = meta["max_tool_calls"]

    # Sync active_agents list to file-backed + status active.
    active_from_files = sorted([aid for aid, m in by_id.items() if m.get("status") == "active"])
    registry["active_agents"] = active_from_files
    registry["agents"] = reg_agents

    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    removed = len(reg_ids - file_ids)
    added = len(file_ids - reg_ids)
    print(f"synced: removed={removed} added={added} total={len(file_ids)} active={len(active_from_files)}")


if __name__ == "__main__":
    main()

