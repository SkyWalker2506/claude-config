---
last_updated: 2026-10-03
confidence: verified-local-execution-with-explicit-limits
scope: A2 cross-project executor routing and evidence gates
---

# Gemini / AGY / Antigravity — reusable dispatch preflight

<!-- 2026-10-03 — task: persist explicit current human model and quota policy across projects -->

## Current human policy — authoritative for future dispatch across projects

- Default (2026-10-14, Musab): **Gemini 4 Argon only**, via AGY: `gemini-4-argon-high` with `--effort high` (verified available in the AGY catalog and answering). For simple mechanical work, `gemini-4-argon-medium`/`medium` or `-low`/`low`. **Never use the Gemini 3 series** (3.x Flash/Pro). The effort is part of the Argon model id; `--effort` must match, and `xhigh`/`max` are rejected.
- Before dispatch, resolve the requested model alias from the installed CLI's current supported catalog/help or source configuration. Do not assume `3.8 Flash` and `3.8 Flash-high` resolve identically. Do not silently substitute the historical `gemini-3.1-pro-high` argument. The 3.1 examples and results below remain historical execution evidence, NOT future defaults; this explicit current human policy overrides their model choice.
- Only **confirmed primary quota exhaustion** permits use of the provider's **extra Claude/GPT quota lanes** until primary quota resets. Choose an available, adequate, low-cost extra lane; the human specified no fixed Claude-versus-GPT priority. Ordinary authentication failures, DNS failures, timeouts and model-not-found errors are NOT evidence of quota exhaustion and do not authorize a server/account fallback, login, new paid service or configuration change.
- Only if those extra Claude/GPT quotas are also exhausted may main Jarvis continue on its own native quota. Conserve the actual remaining account budget: bounded small tasks, minimum necessary context, no redundant model calls, and parallelism limited by observed remaining budget rather than an invented quota or arbitrary resource cap.
- Once primary quota is available again, route **new jobs** back to Gemini 4 Argon. Do not cancel running jobs to switch models. When Gemini quota runs out, Claude continues the work itself until quota returns (no Gemini 3 fallback).
- This is a persistent human preference, not a new model-health test or scheduled monitor. Saving it requires no generation or model spending. Existing 71 Chatterbox TTS jobs and their finite supervisor are unchanged; Gemini performance authoring is already terminal. Source knowledge only: no installer, registry/global-rule edits or generated home-mirror writes are authorized by this note.

<!-- 2026-10-03 — task: retain verified Gemini subscription execution across projects -->

## Pattern: discover the existing route before asking for an API key

- Trigger keywords: Gemini, AGY, Antigravity, subscription, Gemini Ultra, parallel executor, CLI authentication.
- First preserve the human's executor/backend choice. A native coordinator is not a Gemini executor. Never silently substitute native/Claude execution.
- Distinguish direct Google generative API (`GOOGLE_API_KEY`) from installed Antigravity CLI (`agy`, Windows `agy.exe`) using existing subscription/account state. An invalid direct API key does NOT establish that AGY is unavailable. Do not retest an unchanged invalid key.
- Discover the executable from the current machine's configured command resolution or an evidenced installed location; do not hardcode another machine's personal path. Run its current `--help` before choosing flags. Inspect any wrapper before running it.
- Existing local records associated the AGY route with a Gemini Ultra subscription. The account's exact authentication mechanism (OAuth, token source, etc.) was NOT established. Successful execution with a model argument does NOT independently establish the server's resolved model identity.
- No installation, login, account switch, credential/config writes or auth dumps without separate authorization. If the human explicitly restricts execution to direct API, obtain permission before switching to AGY.

## Verified short challenge recipe

Use a new isolated temporary workspace OUTSIDE the target project. Resolve `$agy` to the installed executable; `$lane` is that external directory. These CLI options were inspected in local help and actually exercised on 2026-10-03:

```powershell
# Launch using a hidden, redirected ProcessStartInfo with WorkingDirectory=$lane.
# Build arguments safely; nonce and prompt must contain no secrets.
$nonce = [guid]::NewGuid().ToString('N')
$expected = 'ACK_' + $nonce
$prompt = "Connectivity check only. Reply exactly $expected and nothing else. Do not use tools, read or write files, run commands, inspect accounts, or access any network service beyond this model response."
# Actual supported argument recipe (process management described below):
& $agy --print $prompt --model gemini-3.1-pro-high --mode plan --sandbox `
  --disable-slash-commands --output-format json --print-timeout 110s `
  --log-file "$lane/backend-private.log"
```

The last invocation illustrates arguments, not a complete watchdog implementation. The actual challenge used a hidden process, concurrent stdout/stderr drains and a 120-second owned-process watchdog. Parse JSON privately and require `response.Trim()` to equal `$expected`. Neither process creation nor exit 0 nor an echoed command/prompt is generation proof. Do not print raw backend logs, auth fields, full command lines or account identifiers.

## Trial-and-error: large packets

- Long text sent through standard input stalled in the attempted configuration. The attempted stream-JSON input configuration exited without a usable response. Those owned attempts terminated; they are NOT successful draft evidence.
- Do not infer that every stdin/stream-JSON use is unsupported. The exact supported message protocol was not established; do not guess it, block synchronously on a large write, or retry indefinitely.
- The successful method was a SHORT inline `--print` prompt referencing two pre-created external files per lane: `task.txt` and `source-context.txt`. The prompt explicitly permitted only read-file tools for those two exact paths, overriding the packet's no-tools wording solely for those reads. It prohibited other file access, commands, writes, Unity/Git/network tools and approval requests. Responses were returned to the coordinator, not written by the model.
- Actual final flags: `--print <short-prompt> --model gemini-3.1-pro-high --mode plan --sandbox --disable-slash-commands --output-format json --print-timeout 290s --log-file <external-lane>/backend-private.log`. No stdin redirection and no all-tools autoapproval were used.
- Example short prompt contract: "Read ONLY these exact external task/source files: <task-path>, <source-path>. Return the requested source-grounded DRAFT in your response. No other paths, commands, writes, Unity/Git/network tools or approvals. If unavailable return MISSING_SOURCE. Start SOURCE_<LANE>_<RUN> only after reading the source packet."
- This was a prompt-level read allowlist plus plan/sandbox options, NOT proof of an OS-enforced filesystem allowlist. Review tool activity where safe evidence is available; do not describe sandbox as an absolute security guarantee.
- Inspect opaque wrappers first. The historical `hq agy` wrapper creates a report directory in its target, appends a mandatory file-writing contract, autoapproves tools and uses a 30-minute timeout. It is unsuitable unchanged for a bounded read-only challenge or external draft-only workflow.

## Pattern: bounded parallel read-only dispatch

1. Collect MINIMUM current source/doc excerpts read-only as coordinator. Exclude secrets, private preferences, dirty user assets and unrelated histories. Supply exact approved manifests when relevant. Create prompts/helpers using `apply_patch`; do not depend on the model discovering the project.
2. Use one external directory and source marker per lane. Inject selected role identity/boundaries/knowledge while overriding any write/commit/runtime instruction inconsistent with draft-only scope. Start independent processes before waiting for either result.
3. Use hidden processes (`CreateNoWindow=true` or Hidden when using Start-Process), redirect and asynchronously drain BOTH stdout and stderr immediately. Do not synchronously block on stdin. No arbitrary RAM cap.
4. Persist owned PID, lane, executable/model argument, UTC start, status and source paths immediately. Tool session handles may be scoped to the launching coordinator; other agents should use durable evidence and read-only PID/start validation, not assume they can resume its handle.
5. Use a concurrent 300-second watchdog per owned process alongside CLI `--print-timeout 290s`. Poll both without serial 300-second waits. Timeout means terminate ONLY the process created and tracked for that lane, wait/reap, record terminal status. Preserve foreign AGY sessions; never kill by global process name. No restart until the original owned process is terminal.
6. Parse JSON `response` privately; sanitize before saving `draft.md`. Validate source marker AND source-specific content, correct output shape and absence of fabricated runtime claims. Persist exit, UTC finish, duration, sanitized category, response-saved/source-marker checks and explicit `applied=false`, `testsRun=false`, `noRuntimeClaim=true`.
7. Treat backend logs as private transient data: never emit them or retain account-bearing logs as evidence. Clean up exact owned log files after terminal/reap; cleanup failure must be reported/safely resolved, not silently treated as success. Keep sanitized evidence only.
8. Review each draft for source accuracy and blocking defects before appointing ONE project writer/operator. Parallel external read-only drafts are not permission for concurrent project edits, Unity operation, Git/Jira mutations or feature execution.

## Domain facts and acceptance limits — 2026-10-03

- Model ARGUMENT `gemini-3.1-pro-high`: fresh exact-nonce ACK, PID 5644, exit 0, approximately 44.4 seconds. No timeout. This proves a fresh generated response through the installed AGY path, not server-model/auth-mechanism identity.
- Two actual independent jobs started approximately together: weather PID 65628 at 03:58:59.618 UTC and voice PID 33188 at 03:58:59.668 UTC. Both exit 0; response-source markers/content present; durations 100.2 and 150.6 seconds; both terminal/reaped.
- Neither draft was applied; no tests or Unity runtime were run. Review found blocking defects: weather setup/assertions missing and collider-less warmth fixture; voice dropped detailed transaction feedback and did not resolve competing presentation paths. A successful generation/marker is NOT code readiness, feature acceptance or runtime PASS.
- Draft status hierarchy: started -> generated -> source-reviewed -> ready-for-single-writer-review. Runtime acceptance is a SEPARATE evidence gate. Never promote metadata such as `noRuntimeClaim=true` into proof that the actual response was reviewed.

### Optional dated evidence references (not prerequisites for reuse)

Under the original external `MillionDollars_Temp` root: `agy-ack-20261003/ack-evidence.json`; `agy-parallel-20261003/run-parallel.ps1`; each lane's `job-evidence.json`, `source-context.txt`, `draft.md`; `agy-parallel-20261003/review-disposition.json`. These temporary files may disappear. The recipes and limits above are standalone.

## Source-to-runtime installation gate

On the inspected source checkout, `install.sh --only-agents` only narrows its later phase: earlier global prompt/settings/secrets/MCP/shell-related work still executes. It is NOT an A2-only safe-sync mode. The separate `config/session_sync_claude_config.sh` is network-free but copies global prompts/skills, all agent trees and agent configs; it also regenerates runtime mirrors. It has no inspected per-agent scope option. Do not run either merely to publish this note when existing runtime/dirty changes must be preserved. Keep source knowledge authoritative, report mirror publication pending, and request a separately reviewed narrow-sync route. Do not edit generated home-directory mirrors directly or silently broaden installation scope.
