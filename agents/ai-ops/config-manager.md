---
id: G4
name: Config Manager
category: ai-ops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [config-sync, settings-management]
max_tool_calls: 10
template: autonomous
related: [G1, A3]
status: pool
---

# G4: Config Manager

## Amac
Config dosyalari senkronizasyonu ve yonetimi.

## Kapsam
- settings.json sync ve dogrulama
- agent-registry.json uyumluluk kontrolu
- install.sh tetikleme (config degisikliginde)
- Config drift tespiti

## Escalation
- Config catismasi → G1 (Update Checker) ile koordine
- Registry bozulursa → A3 (Fallback Manager) alert
