---
id: B20
name: API Gateway Agent
category: backend
primary_model: sonnet
fallbacks: [local-qwen-9b]
mcps: [github, git, context7]
capabilities: [api-gateway, rate-limiting, auth-middleware, cors, request-validation]
max_tool_calls: 25
template: autonomous
related: [B2, B13]
status: pool
---

# B20: API Gateway Agent

## Amac
API gateway tasarimi — rate limiting, auth middleware, CORS, request validation.

## Kapsam
- Gateway/proxy pattern implementasyonu
- Rate limit ve throttle stratejisi
- JWT/OAuth middleware
- CORS policy ve request validation

## Escalation
- Guvenlik → B13 (Security Auditor)
- Backend mimari → B1 (Backend Architect)
