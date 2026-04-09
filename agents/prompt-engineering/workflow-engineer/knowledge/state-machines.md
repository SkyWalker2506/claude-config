---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# State Machines

## Agent State Modeling

Every agent task has a lifecycle. Model it as finite states with explicit transitions.

```
IDLE → PLANNING → EXECUTING → VERIFYING → DONE
                      ↓            ↓
                   BLOCKED      FAILED
                      ↓            ↓
                   WAITING     DEBUGGING → EXECUTING
```

## Core States

| State | Description | Allowed Transitions |
|-------|------------|---------------------|
| IDLE | No active work | → PLANNING |
| PLANNING | Reading spec, breaking down tasks | → EXECUTING, → BLOCKED |
| EXECUTING | Writing code, running commands | → VERIFYING, → FAILED |
| VERIFYING | Running tests, build checks | → DONE, → FAILED |
| BLOCKED | Waiting for external input | → EXECUTING (when unblocked) |
| FAILED | Error occurred | → DEBUGGING |
| DEBUGGING | Diagnosing root cause | → EXECUTING (retry) |
| DONE | Task complete, verified | → IDLE |

## Transition Rules

1. **No skipping states** — can't go IDLE → DONE without EXECUTING
2. **FAILED always goes through DEBUGGING** — no blind retries
3. **BLOCKED requires explicit unblock** — human input or dependency resolution
4. **VERIFYING can loop** — verify → fail → debug → execute → verify

## Task-Level State Machine

For individual tasks in a sprint/plan:

```
TODO → IN_PROGRESS → IN_REVIEW → DONE
          ↓              ↓
       BLOCKED        CHANGES_REQUESTED → IN_PROGRESS
```

## Phase-Level State Machine

For pipeline phases:

```
PENDING → ACTIVE → VALIDATING → COMPLETE
                       ↓
                    FAILED → ACTIVE (retry, max 3)
```

Phase transitions are gated: all tasks in phase must be DONE before phase moves to COMPLETE.

## Implementation Tips

- **Persist state** — if agent crashes, it should resume from last known state
- **Log transitions** — `[2026-04-09 14:30] EXECUTING → VERIFYING (tests triggered)`
- **Guard transitions** — validate preconditions before allowing state change
- **Timeout idle states** — BLOCKED for >30min should escalate
- **Avoid god states** — if a state does too many things, split it
