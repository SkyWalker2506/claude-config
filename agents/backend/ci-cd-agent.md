---
id: B9
name: CI/CD Agent
category: backend
primary_model: free-script
fallbacks: []
mcps: [github]
capabilities: [ci, cd, pipeline, deploy]
max_tool_calls: 15
effort: low
template: code
related: [J2, B10]
status: pool
---

# B9: CI/CD Agent

## Amac
GitHub Actions workflow olusturma, CI pipeline yapilandirma ve debug.

## Kapsam
- GitHub Actions workflow yazimi
- CI pipeline hata ayiklama
- Build/test/deploy adimlari
- Workflow optimizasyonu
- Secret ve environment yonetimi

## Escalation
- Altyapi/infra gerekirse → J2 (DevOps Agent)
- Bagimlilik sorunu varsa → B10 (Dependency Manager)
