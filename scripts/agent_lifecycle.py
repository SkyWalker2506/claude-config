#!/usr/bin/env python3
"""
Agent lifecycle manager — promote/demote/retire recommendations.

Rules:
  - active agent with 0 dispatches in 90d       -> demote to pool
  - pool agent with 5+ dispatches in 30d         -> promote to active
  - pool agent with 0 dispatches in 180d         -> retire candidate

Reads config/telemetry/events/*.jsonl + config/agent-registry.json.
Writes Reports/lifecycle_recommendations.json. Never mutates the registry.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


def find_base() -> Path:
    env_base = os.environ.get("CLAUDE_CONFIG_ROOT")
    if env_base and Path(env_base).exists():
        return Path(env_base)
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent-registry.json").exists():
        return here
    return Path.home() / "Projects" / "claude-config"


BASE = find_base()


def load_events(days: int) -> list[dict]:
    events: list[dict] = []
    event_dir = BASE / "config" / "telemetry" / "events"
    if not event_dir.exists():
        return events
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for f in event_dir.glob("*.jsonl"):
        try:
            for line in f.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                    ts = datetime.fromisoformat(ev["timestamp"])
                    if ts >= cutoff:
                        events.append(ev)
                except Exception:
                    continue
        except Exception:
            continue
    return events


MIN_SAMPLE = 20


def analyze(force: bool = False) -> list[dict]:
    registry = json.loads((BASE / "config" / "agent-registry.json").read_text())
    agents_map = registry.get("agents") or {}

    events_180 = load_events(180)
    # Need minimum data to make any recommendation at all.
    # Otherwise a fresh install flags every active agent for demotion.
    if not force and len(events_180) < MIN_SAMPLE:
        return []

    now = datetime.now(timezone.utc)

    usage_90d: Counter = Counter()
    usage_30d: Counter = Counter()
    usage_180d: Counter = Counter()

    for e in events_180:
        aid = e.get("agent_id")
        if not aid or aid == "unknown":
            continue
        try:
            ts = datetime.fromisoformat(e["timestamp"])
        except Exception:
            continue
        age = (now - ts).days
        usage_180d[aid] += 1
        if age <= 90:
            usage_90d[aid] += 1
        if age <= 30:
            usage_30d[aid] += 1

    recs: list[dict] = []
    for aid, meta in agents_map.items():
        status = meta.get("status", "pool")
        name = meta.get("name", "")

        if status == "active" and usage_90d[aid] == 0:
            recs.append({
                "agent_id": aid,
                "agent_name": name,
                "current": "active",
                "recommended": "pool",
                "reason": "0 dispatches in 90 days",
            })

        if status == "pool" and usage_30d[aid] >= 5:
            recs.append({
                "agent_id": aid,
                "agent_name": name,
                "current": "pool",
                "recommended": "active",
                "reason": f"{usage_30d[aid]} dispatches in 30 days",
            })

        if status == "pool" and usage_180d[aid] == 0:
            recs.append({
                "agent_id": aid,
                "agent_name": name,
                "current": "pool",
                "recommended": "retire_candidate",
                "reason": "0 dispatches in 180 days",
            })

    return recs


def main() -> None:
    force = "--force" in sys.argv
    recs = analyze(force=force)

    promote = [r for r in recs if r["recommended"] == "active"]
    demote = [r for r in recs if r["recommended"] == "pool"]
    retire = [r for r in recs if r["recommended"] == "retire_candidate"]

    print()
    print("Agent Lifecycle Analysis")
    print("=" * 50)

    if promote:
        print(f"\n[PROMOTE to active] ({len(promote)}):")
        for r in promote:
            print(f"  {r['agent_id']} {r['agent_name']} - {r['reason']}")

    if demote:
        print(f"\n[DEMOTE to pool] ({len(demote)}):")
        for r in demote[:15]:
            print(f"  {r['agent_id']} {r['agent_name']} - {r['reason']}")
        if len(demote) > 15:
            print(f"  ... +{len(demote)-15} more")

    if retire:
        print(f"\n[RETIRE candidates] ({len(retire)}):")
        for r in retire[:10]:
            print(f"  {r['agent_id']} {r['agent_name']} - {r['reason']}")
        if len(retire) > 10:
            print(f"  ... +{len(retire)-10} more")

    if not recs:
        event_dir = BASE / "config" / "telemetry" / "events"
        has_data = event_dir.exists() and any(event_dir.glob("*.jsonl"))
        if not has_data:
            print("\nNo telemetry yet — dispatch events not logged.")
            print("Run workloads with log_dispatch.py hook enabled, then re-run.")
        else:
            print("\nNo lifecycle changes recommended (insufficient sample size <20).")

    out_dir = BASE / "Reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "lifecycle_recommendations.json"
    out.write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    print(f"\nReport -> Reports/lifecycle_recommendations.json")


if __name__ == "__main__":
    main()
