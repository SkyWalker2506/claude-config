#!/usr/bin/env python3
"""
hq events / hq tail / hq stats — telemetry inspection helpers.

Usage:
  python3 hq_events.py events [--limit N]            List the last N events (default 20)
  python3 hq_events.py tail [--follow]               Print events as they arrive (poll every 2s)
  python3 hq_events.py stats <agent_id>              Per-agent breakdown over the last 30 days

Reads config/telemetry/events/*.jsonl. Never mutates anything.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
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


def event_dir() -> Path:
    return find_base() / "config" / "telemetry" / "events"


def iter_events(days: int | None = None):
    """Yield events from oldest to newest. Optional day cutoff."""
    d = event_dir()
    if not d.exists():
        return
    cutoff = None
    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for f in sorted(d.glob("*.jsonl")):
        try:
            for line in f.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                if cutoff is not None:
                    try:
                        ts = datetime.fromisoformat(ev["timestamp"])
                    except Exception:
                        continue
                    if ts < cutoff:
                        continue
                yield ev
        except Exception:
            continue


def fmt_event(e: dict) -> str:
    ts = str(e.get("timestamp", ""))[:19].replace("T", " ")
    aid = e.get("agent_id", "unknown") or "unknown"
    name = e.get("agent_name", "") or ""
    name = (name[:22] + "…") if len(name) > 23 else name
    model = (e.get("model_used", "?") or "?")
    model = (model[:18] + "…") if len(model) > 19 else model
    outcome = e.get("outcome", "?")
    task = e.get("task_type", "?")
    project = e.get("project", "?")
    icon = {"success": "OK", "failed": "FAIL", "partial": "WARN",
            "timeout": "TOUT", "unknown": "----"}.get(outcome, "?")
    return f"{ts} [{icon:>4}] {aid:>5} {name:<23} {model:<19} {task:<10} {project}"


def cmd_events(limit: int) -> int:
    events = list(iter_events())
    if not events:
        print("No telemetry events yet.")
        return 0
    tail = events[-limit:]
    print(f"Last {len(tail)} events (of {len(events)} total):")
    print()
    print(f"{'timestamp':<19} {'state':>6} {'id':>5} {'name':<23} {'model':<19} {'task':<10} project")
    print("-" * 110)
    for e in tail:
        print(fmt_event(e))
    return 0


def cmd_tail(follow: bool) -> int:
    seen: set[str] = set()
    # Prime with the last 5 events so the screen isn't blank.
    initial = list(iter_events())[-5:]
    for e in initial:
        eid = e.get("event_id", "")
        if eid:
            seen.add(eid)
        print(fmt_event(e))

    if not follow:
        return 0

    print("\n[tail -f] watching for new dispatch events. Ctrl-C to stop.\n")
    try:
        while True:
            time.sleep(2)
            for e in iter_events():
                eid = e.get("event_id", "")
                if not eid or eid in seen:
                    continue
                seen.add(eid)
                print(fmt_event(e))
    except KeyboardInterrupt:
        print()
        return 0


def cmd_stats(agent_id: str) -> int:
    events = [e for e in iter_events(days=30) if e.get("agent_id") == agent_id]
    if not events:
        print(f"No events found for agent '{agent_id}' in the last 30 days.")
        return 0

    total = len(events)
    outcomes = Counter(e.get("outcome", "unknown") for e in events)
    success = outcomes.get("success", 0)
    failed = outcomes.get("failed", 0)
    sr = (success / total * 100) if total else 0.0

    models = Counter(e.get("model_used", "unknown") for e in events)
    projects = Counter(e.get("project", "unknown") for e in events)
    tasks = Counter(e.get("task_type", "unknown") for e in events)

    durs = [float(e.get("duration_seconds", 0) or 0) for e in events]
    avg_dur = (sum(durs) / len(durs)) if durs else 0.0

    name = events[-1].get("agent_name", "")
    category = events[-1].get("category", "")

    print(f"Agent stats — {agent_id} {name} ({category})")
    print("=" * 60)
    print(f"Period:        last 30 days")
    print(f"Dispatches:    {total}")
    print(f"Success rate:  {sr:.1f}% ({success} ok / {failed} failed)")
    print(f"Avg duration:  {avg_dur:.2f}s")
    print()
    print("Models used:")
    for m, n in models.most_common():
        print(f"  {n:>4}  {m}")
    print()
    print("Projects:")
    for p, n in projects.most_common(10):
        print(f"  {n:>4}  {p}")
    print()
    print("Task types:")
    for t, n in tasks.most_common():
        print(f"  {n:>4}  {t}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="hq_events", add_help=True)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_events = sub.add_parser("events", help="List recent dispatch events")
    p_events.add_argument("--limit", type=int, default=20)

    p_tail = sub.add_parser("tail", help="Print events as they arrive")
    p_tail.add_argument("--follow", "-f", action="store_true",
                        help="Keep watching for new events")

    p_stats = sub.add_parser("stats", help="Per-agent breakdown")
    p_stats.add_argument("agent_id", help="Agent ID, e.g. B2")

    args = parser.parse_args()
    if args.cmd == "events":
        return cmd_events(args.limit)
    if args.cmd == "tail":
        return cmd_tail(args.follow)
    if args.cmd == "stats":
        return cmd_stats(args.agent_id)
    return 1


if __name__ == "__main__":
    sys.exit(main())
