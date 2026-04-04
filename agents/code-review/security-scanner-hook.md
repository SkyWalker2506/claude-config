---
id: C2
name: Security Scanner Hook
category: code-review
primary_model: free-deterministic
fallbacks: []
mcps: []
capabilities: [secret-scan, dependency-audit, sast]
max_tool_calls: 3
template: code-review
layer: L1
related: [C1, B13]
status: active
---

# C2: Security Scanner Hook

## Amac
Pre-commit hook: secret scan, dependency audit. Deterministic — AI model kullanmaz.

## Kapsam
- Secret/credential pattern tarama (API key, token, password)
- npm audit / pip audit calistirma
- Secrets dosyasina yazma engelleme (mevcut PreToolUse hook ile)

## Escalation
- Kritik bulgu → B13 (Security Auditor) tetikle
