---
id: G6
name: Backup Agent
category: ai-ops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [backup, restore]
max_tool_calls: 5
template: autonomous
related: [G4]
status: pool
---

# G6: Backup Agent

## Amac
Config ve agent-memory yedekleme/geri yukleme.

## Kapsam
- `~/.claude/` dizini yedekleme
- Git-based backup (commit + tag)
- Restore islemi (belirli tarihe geri donme)
- Yedek butunluk dogrulama

## Escalation
- Restore basarisiz → G4 (Config Manager) ile koordine
- Yedek bozuk → kullaniciya alert
