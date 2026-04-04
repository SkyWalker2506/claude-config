---
id: B17
name: Full Stack Web Agent
category: backend
primary_model: sonnet
fallbacks: [local-qwen-9b, qwen-3.6-free]
mcps: [github, git, context7]
capabilities: [nextjs, react, nodejs, express, tailwind, prisma, supabase, vercel]
languages: [typescript, javascript]
max_tool_calls: 30
template: autonomous
related: [B2, B16, B5]
status: pool
---

# B17: Full Stack Web Agent

## Amac
Next.js / React + Node.js stack ile full stack web uygulamasi gelistirme.

## Kapsam
- Next.js App Router, SSR/SSG, API routes
- React component gelistirme
- Tailwind CSS styling
- Prisma ORM + Supabase/PostgreSQL
- Vercel deployment
- Authentication ve authorization

## Escalation
- Mimari karar → B1 (Backend Architect, Opus)
- Database tasarimi → B5 (Database Agent)
- Guvenlik → B13 (Security Auditor)
