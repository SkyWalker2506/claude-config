---
id: B14
name: Scripting Agent
category: backend
primary_model: local-qwen-9b
fallbacks: [free-router]
mcps: []
capabilities: [bash, python, automation, cron]
max_tool_calls: 20
effort: low
template: code
related: [G8, B9]
status: pool
---

# B14: Scripting Agent

## Amac
Bash/Python otomasyon scriptleri, cron job yapilandirma.

## Kapsam
- Bash script yazimi ve debug
- Python otomasyon scriptleri
- Cron job olusturma ve yonetimi
- Dosya/dizin islemleri otomasyonu
- Pipeline ve workflow scriptleri

## Escalation
- AI workflow gerekirse → G8 (AI Ops Agent)
- CI/CD entegrasyonu gerekirse → B9 (CI/CD Agent)
