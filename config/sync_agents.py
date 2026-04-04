#!/usr/bin/env python3
"""
sync_agents.py — Agent .md frontmatter ↔ agent-registry.json dogrulama + senkronizasyon

Kullanim:
  python3 config/sync_agents.py --check        # uyumsuzluklari raporla
  python3 config/sync_agents.py --fix          # registry'yi .md dosyalarindan guncelle
  python3 config/sync_agents.py --stats        # ozet istatistik
"""

import json
import sys
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = REPO_ROOT / "config" / "agent-registry.json"
AGENTS_DIR = REPO_ROOT / "agents"

REQUIRED_FRONTMATTER_KEYS = ["id", "name", "category", "primary_model", "status"]


def parse_frontmatter(filepath):
    """Parse YAML-like frontmatter from a .md file."""
    content = filepath.read_text()
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    fm_text = content[3:end].strip()
    data = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Parse list values like [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                val = [v.strip() for v in inner.split(",") if v.strip()]
            data[key] = val
    return data


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        f.write("\n")


def collect_agent_files():
    """Return list of (path, frontmatter) for all agent .md files."""
    results = []
    for md_file in AGENTS_DIR.rglob("*.md"):
        if md_file.name == "README.md":
            continue
        fm = parse_frontmatter(md_file)
        if fm and "id" in fm:
            results.append((md_file, fm))
    return results


def check(fix=False):
    registry = load_registry()
    agents_reg = registry.get("agents", {})
    agent_files = collect_agent_files()

    errors = []
    warnings = []
    fixed = []

    # Build a map of id -> (path, frontmatter) from .md files
    md_map = {}
    for path, fm in agent_files:
        agent_id = fm["id"]
        if agent_id in md_map:
            errors.append(f"DUPLICATE ID: {agent_id} in {path} and {md_map[agent_id][0]}")
        md_map[agent_id] = (path, fm)

    # Check required frontmatter keys
    for agent_id, (path, fm) in md_map.items():
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in fm:
                errors.append(f"MISSING KEY '{key}' in {path.relative_to(REPO_ROOT)}")

    # Check .md files vs registry
    for agent_id, (path, fm) in md_map.items():
        if agent_id not in agents_reg:
            warnings.append(f"UNREGISTERED: {agent_id} ({fm.get('name', '?')}) in {path.relative_to(REPO_ROOT)}")
            if fix:
                agents_reg[agent_id] = {
                    "name": fm.get("name", agent_id),
                    "category": fm.get("category", "unknown"),
                    "primary_model": fm.get("primary_model", "haiku"),
                    "fallbacks": fm.get("fallbacks", []),
                    "mcps": fm.get("mcps", []),
                    "capabilities": fm.get("capabilities", []),
                    "max_tool_calls": int(fm.get("max_tool_calls", 10)),
                    "status": fm.get("status", "pool"),
                    "related": fm.get("related", []),
                }
                fixed.append(f"ADDED to registry: {agent_id}")
        else:
            reg_entry = agents_reg[agent_id]
            # Check name mismatch
            if reg_entry.get("name") != fm.get("name"):
                warnings.append(
                    f"NAME MISMATCH: {agent_id} registry='{reg_entry.get('name')}' md='{fm.get('name')}'"
                )
                if fix:
                    reg_entry["name"] = fm.get("name")
                    fixed.append(f"FIXED name for {agent_id}")
            # Check status mismatch
            if reg_entry.get("status") != fm.get("status"):
                warnings.append(
                    f"STATUS MISMATCH: {agent_id} registry='{reg_entry.get('status')}' md='{fm.get('status')}'"
                )
                if fix:
                    reg_entry["status"] = fm.get("status")
                    fixed.append(f"FIXED status for {agent_id}")

    # Check registry entries without .md files
    for agent_id in agents_reg:
        if agent_id not in md_map:
            warnings.append(f"REGISTRY ONLY (no .md): {agent_id} ({agents_reg[agent_id].get('name', '?')})")

    if fix and fixed:
        registry["agents"] = agents_reg
        save_registry(registry)

    return errors, warnings, fixed


def stats():
    registry = load_registry()
    agents_reg = registry.get("agents", {})
    agent_files = collect_agent_files()

    total_reg = len(agents_reg)
    total_md = len(agent_files)
    active = sum(1 for a in agents_reg.values() if a.get("status") == "active")
    pool = sum(1 for a in agents_reg.values() if a.get("status") == "pool")

    by_category = {}
    for a in agents_reg.values():
        cat = a.get("category", "unknown")
        by_category[cat] = by_category.get(cat, 0) + 1

    print(f"\n=== Agent Registry Stats ===")
    print(f"Registry entries : {total_reg}")
    print(f"Agent .md files  : {total_md}")
    print(f"Active           : {active}")
    print(f"Pool             : {pool}")
    print(f"\nBy category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat:<20} {count}")


def main():
    mode = "--check"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    if mode == "--stats":
        stats()
        return

    fix = mode == "--fix"
    errors, warnings, fixed = check(fix=fix)

    if errors:
        print("\n[ERRORS]")
        for e in errors:
            print(f"  ✗ {e}")

    if warnings:
        print("\n[WARNINGS]")
        for w in warnings:
            print(f"  ⚠ {w}")

    if fixed:
        print("\n[FIXED]")
        for f in fixed:
            print(f"  ✓ {f}")

    if not errors and not warnings:
        print("✓ Registry and agent files are in sync.")
    elif not errors and not fix:
        print(f"\n{len(warnings)} warning(s). Run with --fix to auto-correct.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
