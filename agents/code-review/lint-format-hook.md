---
id: C1
name: Lint & Format Hook
category: code-review
primary_model: free-deterministic
fallbacks: []
mcps: []
capabilities: [lint, format, type-check]
max_tool_calls: 3
template: code-review
layer: L1
related: [C2, C3]
status: active
---

# C1: Lint & Format Hook

## Amac
Pre-commit hook: lint, format, type check. Deterministic — AI model kullanmaz.

## Kapsam
- ESLint / Dart analyze / Ruff calistirma
- Prettier / dart format
- TypeScript tsc --noEmit
- Hata varsa commit engelle, output'u agent'a geri besle

## Escalation
- Yok — deterministic hook, hata varsa agent kendisi duzeltir
