---
id: J1
name: Docker Agent
category: devops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [docker, compose, container]
max_tool_calls: 15
template: autonomous
related: [J2, B9]
status: pool
---

# J1: Docker Agent

## Amac
Dockerfile ve docker-compose olusturma, container yonetimi.

## Kapsam
- Multi-stage build olusturma ve optimizasyon
- docker-compose orchestration
- Volume/network yapilandirmasi
- Image boyut optimizasyonu

## Escalation
- Build hatasi 3x tekrarlanirsa -> J2 (Cloud Deploy Agent)
- Guvenlik zaafiyeti tespit edilirse -> B9 (Security Auditor)
