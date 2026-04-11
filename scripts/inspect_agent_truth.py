#!/usr/bin/env python3
"""
Inspect the same agent across runtime and source layers.

Layers:
1. Runtime flat registry entry under ~/.claude/agents/<category>/<slug>.md
2. Runtime JSON registry under ~/.claude/config/agent-registry.json
3. Source AGENT tree under agents/<category>/<slug>/AGENT.md
4. Source registry under config/agent-registry.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_AGENTS = Path.home() / ".claude" / "agents"
RUNTIME_REGISTRY = Path.home() / ".claude" / "config" / "agent-registry.json"
SOURCE_AGENTS = ROOT / "agents"
SOURCE_REGISTRY = ROOT / "config" / "agent-registry.json"


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_inline_list(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1].strip()
    if not raw:
        return []
    out: list[str] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if len(part) >= 2 and part[0] == part[-1] and part[0] in ("'", '"'):
            part = part[1:-1]
        out.append(part)
    return out


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return ""
    if raw.startswith("[") and raw.endswith("]"):
        return parse_inline_list(raw)
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^---\n([\s\S]*?)\n---\n?", text)
    if not match:
        return {}

    data: dict[str, Any] = {}
    current_map: str | None = None

    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if indent == 0:
            if value == "":
                data[key] = {}
                current_map = key
            else:
                data[key] = parse_scalar(value)
                current_map = None
            continue

        if current_map and isinstance(data.get(current_map), dict):
            data[current_map][key] = parse_scalar(value)

    return data


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_flat_files() -> list[Path]:
    if not RUNTIME_AGENTS.exists():
        return []
    return sorted(
        path
        for path in RUNTIME_AGENTS.glob("*/*.md")
        if path.name != "AGENT.md"
    )


def source_agent_files() -> list[Path]:
    if not SOURCE_AGENTS.exists():
        return []
    return sorted(SOURCE_AGENTS.glob("*/*/AGENT.md"))


def alias_keys(agent_id: str, name: str, slug: str) -> set[str]:
    keys = {normalize(agent_id), normalize(name), normalize(slug)}
    return {key for key in keys if key}


def build_records() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    runtime_registry = load_json(RUNTIME_REGISTRY)
    source_registry = load_json(SOURCE_REGISTRY)

    for registry_name, registry in (
        ("runtime_registry", runtime_registry.get("agents", {})),
        ("source_registry", source_registry.get("agents", {})),
    ):
        for agent_id, meta in registry.items():
            record = records.setdefault(agent_id, {"id": agent_id})
            record[registry_name] = meta
            if meta.get("name"):
                record.setdefault("name", meta["name"])

    for path in runtime_flat_files():
        meta = parse_frontmatter(path)
        agent_id = str(meta.get("id", "")).strip()
        if not agent_id:
            continue
        record = records.setdefault(agent_id, {"id": agent_id})
        record["runtime_flat"] = meta
        record["runtime_flat_path"] = str(path)
        record.setdefault("name", meta.get("name") or path.stem)
        record.setdefault("slug", path.stem)

    for path in source_agent_files():
        meta = parse_frontmatter(path)
        agent_id = str(meta.get("id", "")).strip()
        if not agent_id:
            continue
        record = records.setdefault(agent_id, {"id": agent_id})
        record["source_agent"] = meta
        record["source_agent_path"] = str(path)
        record.setdefault("name", meta.get("name") or path.parent.name)
        record.setdefault("slug", path.parent.name)

    for agent_id, record in records.items():
        if "slug" not in record:
            record["slug"] = normalize(record.get("name", "") or agent_id)

    return records


def resolve_query(query: str, records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if query in records:
        return records[query]

    q = normalize(query)
    matches = [
        record
        for record in records.values()
        if q in alias_keys(
            record["id"],
            str(record.get("name", "")),
            str(record.get("slug", "")),
        )
    ]

    if not matches:
        raise SystemExit(f"Agent bulunamadi: {query}")
    if len(matches) > 1:
        choices = ", ".join(f"{item['id']}:{item.get('name', item['id'])}" for item in matches)
        raise SystemExit(f"Belirsiz sorgu: {query} -> {choices}")
    return matches[0]


def compact_meta(meta: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in keys:
        value = meta.get(key)
        if value not in (None, "", [], {}):
            out[key] = value
    return out


def compare_notes(record: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    runtime_flat = record.get("runtime_flat", {})
    runtime_registry = record.get("runtime_registry", {})
    source_agent = record.get("source_agent", {})
    source_registry = record.get("source_registry", {})

    flat_model = runtime_flat.get("primary_model")
    runtime_registry_model = runtime_registry.get("primary_model")
    source_registry_model = source_registry.get("primary_model")
    source_mid_model = None
    if isinstance(source_agent.get("models"), dict):
        source_mid_model = source_agent["models"].get("mid")

    if flat_model and runtime_registry_model and flat_model != runtime_registry_model:
        notes.append(
            f"runtime flat primary_model ({flat_model}) != runtime registry primary_model ({runtime_registry_model})"
        )
    if flat_model and source_registry_model and flat_model != source_registry_model:
        notes.append(
            f"runtime flat primary_model ({flat_model}) != source registry primary_model ({source_registry_model})"
        )
    if flat_model and source_mid_model and flat_model != source_mid_model:
        notes.append(
            f"runtime flat primary_model ({flat_model}) != source AGENT mid model ({source_mid_model})"
        )

    if flat_model:
        if flat_model == source_registry_model:
            notes.append("runtime flat mirror matches source registry model truth")
        else:
            notes.append("runtime flat mirror drifted from source registry; source registry wins")
    elif runtime_registry_model:
        notes.append("runtime flat mirror missing; source registry remains canonical")

    if record.get("source_agent_path"):
        notes.append("scope, escalation, and knowledge rules should come from source AGENT.md")
    if record.get("source_registry"):
        notes.append("source registry is canonical model/backend truth")

    return notes


def to_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def print_section(title: str, path: str | None, meta: dict[str, Any]) -> None:
    print(f"{title}:")
    if path:
        print(f"- path: {path}")
    if not meta:
        print("- missing")
        return
    for key, value in meta.items():
        print(f"- {key}: {to_text(value)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Show runtime vs source agent truth")
    parser.add_argument("query", help="Agent id, slug, or name. Example: B15 or mobile-dev-agent")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output")
    args = parser.parse_args()

    records = build_records()
    record = resolve_query(args.query, records)

    payload = {
        "agent": {
            "id": record["id"],
            "name": record.get("name"),
            "slug": record.get("slug"),
        },
        "runtime_flat": {
            "path": record.get("runtime_flat_path"),
            "meta": compact_meta(
                record.get("runtime_flat", {}),
                ["category", "primary_model", "fallbacks", "mcps", "capabilities", "max_tool_calls", "status", "template"],
            ),
        },
        "runtime_registry": {
            "path": str(RUNTIME_REGISTRY) if RUNTIME_REGISTRY.exists() else None,
            "meta": compact_meta(
                record.get("runtime_registry", {}),
                ["category", "primary_model", "primary_model_legacy", "codex_model", "execution_mode", "execution_backends", "status"],
            ),
        },
        "source_agent": {
            "path": record.get("source_agent_path"),
            "meta": compact_meta(
                record.get("source_agent", {}),
                ["category", "tier", "models", "refine_model", "mcps", "capabilities", "max_tool_calls", "status"],
            ),
        },
        "source_registry": {
            "path": str(SOURCE_REGISTRY) if SOURCE_REGISTRY.exists() else None,
            "meta": compact_meta(
                record.get("source_registry", {}),
                ["category", "primary_model", "primary_model_legacy", "codex_model", "execution_mode", "execution_backends", "status"],
            ),
        },
        "notes": compare_notes(record),
    }

    if args.as_json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    print(f"Agent: {payload['agent']['id']} - {payload['agent']['name']}")
    print()
    print_section("Runtime flat entry", payload["runtime_flat"]["path"], payload["runtime_flat"]["meta"])
    print()
    print_section("Runtime registry", payload["runtime_registry"]["path"], payload["runtime_registry"]["meta"])
    print()
    print_section("Source AGENT tree", payload["source_agent"]["path"], payload["source_agent"]["meta"])
    print()
    print_section("Source registry", payload["source_registry"]["path"], payload["source_registry"]["meta"])
    print()
    print("Notes:")
    for note in payload["notes"]:
        print(f"- {note}")


if __name__ == "__main__":
    main()
