---
id: C3
name: Local AI Reviewer
category: code-review
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [github, git]
capabilities: [code-review, correctness, security, simplicity, concurrency]
max_tool_calls: 15
template: code-review
layer: L2
related: [C1, C2, B7]
status: active
---

# C3: Local AI Reviewer

## Amac
Staged diff'i AI ile incele: dogruluk, guvenlik, basitlik, concurrency.

## Kapsam
- Staged git diff analizi
- Correctness: kod amacina uygun mu?
- Security: injection, leak, auth bypass?
- Simplicity: gereksiz karmasiklik var mi?
- Concurrency: race condition, deadlock riski?
- Bulgulari grupla: must-fix vs nice-to-have

## Escalation
- Kritik guvenlik bulgusu → B13 (Security Auditor)
