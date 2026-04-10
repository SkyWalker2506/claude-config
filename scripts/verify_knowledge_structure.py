#!/usr/bin/env python3
"""Exit 0 iff agent coverage tiers are green and all knowledge files pass mega section check.

Used by CI and locally before large merges."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_VERIFY_ENV = {**os.environ, "CLAUDE_VERIFY_AUDIT": "1"}


def main() -> int:
    r1 = subprocess.run(
        [sys.executable, str(ROOT / "scripts/agent_coverage_audit.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=_VERIFY_ENV,
    )
    out1 = r1.stdout + r1.stderr
    print(out1, end="")
    if not re.search(r"P0=0 P1=0 P2=0", out1):
        print("verify: FAIL — expected P0=0 P1=0 P2=0 in agent coverage output", file=sys.stderr)
        return 1

    r2 = subprocess.run(
        [sys.executable, str(ROOT / "scripts/knowledge_quality_audit.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=_VERIFY_ENV,
    )
    out2 = r2.stdout + r2.stderr
    print(out2, end="")
    m = re.search(r"complete=(\d+)/(\d+)", out2)
    if not m or m.group(1) != m.group(2):
        print("verify: FAIL — knowledge topics must be complete=N/N with equal N", file=sys.stderr)
        return 1

    print("verify: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
