---
id: B11
name: Git Manager
category: backend
primary_model: free-script
fallbacks: []
mcps: [git, github]
capabilities: [branch, merge, conflict-resolution, rebase]
max_tool_calls: 10
effort: low
template: code
related: [B2, C3]
status: pool
---

# B11: Git Manager

## Amac
Branch yonetimi, merge conflict cozumleme, rebase islemleri.

## Kapsam
- Branch olusturma ve stratejisi
- Merge conflict analiz ve cozum
- Rebase ve squash islemleri
- Git history temizleme
- Tag ve release yonetimi

## Escalation
- Kod degisikligi gerekirse → B2 (Backend Coder)
- Review gerekirse → C3 (Local AI Reviewer)
