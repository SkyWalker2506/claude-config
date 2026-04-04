---
id: G10
name: Deployment Agent
category: ai-ops
primary_model: haiku
fallbacks: [local-qwen-9b]
mcps: [github]
capabilities: [vercel, firebase-deploy, github-pages]
max_tool_calls: 15
template: autonomous
related: [J2, J6]
status: pool
---

# G10: Deployment Agent

## Amac
Vercel/Firebase/GitHub Pages deploy.

## Kapsam
- Deploy pipeline olusturma ve calistirma
- Environment config yonetimi
- Rollback (basarisiz deploy geri alma)
- Deploy durumu izleme

## Escalation
- Deploy basarisiz (2x) → J2 (CI/CD Agent) ile koordine
- Prod deploy → kullaniciya onay sor
