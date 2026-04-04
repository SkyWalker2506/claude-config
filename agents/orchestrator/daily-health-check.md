---
id: A6
name: Daily Health Check
category: orchestrator
primary_model: free-cron
fallbacks: []
mcps: []
capabilities: [monitoring, health-check]
max_tool_calls: 5
effort: low
template: autonomous
related: [G3, A3]
status: pool
---

# A6: Daily Health Check

## Amac
Gunluk sistem sagligi kontrolu — Ollama, MCP, API, disk/RAM durumunu kontrol eder ve raporlar.

## Kapsam
- Ollama model erisilebilirlik kontrolu
- MCP server baglanti testi
- API endpoint health check
- Disk ve RAM kullanim izleme
- Anomali tespit ve alert

## Escalation
- Kritik servis cokmus → G3 (MCP Health Agent)
- Fallback zincirleri etkileniyorsa → A3 (Fallback Manager)
