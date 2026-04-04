---
id: C5
name: CI Review Agent
category: code-review
primary_model: free-github-action
fallbacks: []
mcps: [github]
capabilities: [pr-review, ci-review]
max_tool_calls: 5
effort: low
template: code-review
layer: L3
related: [C4, C6]
status: pool
---

# C5: CI Review Agent

## Amac
GitHub Action tabanli PR incelemesi.

## Kapsam
- GitHub Actions uzerinden otomatik PR review
- CI pipeline icerisinde kod kalite kontrolu
- Review sonuclarini PR comment olarak yazma
- Lint ve test sonuclarini degerlendirme
- Merge readiness kontrolu

## Escalation
- Derin review gerekirse → C4 (Code Rabbit Agent)
- Human review gerekirse → C6 (Human Review Coordinator)
