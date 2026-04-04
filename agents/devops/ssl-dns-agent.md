---
id: J3
name: SSL/DNS Agent
category: devops
primary_model: free-script
fallbacks: []
mcps: []
capabilities: [ssl, dns, certificate]
max_tool_calls: 10
template: autonomous
related: [J2, J4]
status: pool
---

# J3: SSL/DNS Agent

## Amac
SSL sertifika ve DNS yapilandirmasi.

## Kapsam
- Let's Encrypt sertifika olusturma ve yenileme
- Cloudflare DNS kayit yonetimi
- Domain yonlendirme (A, CNAME, MX)
- Sertifika suresi izleme

## Escalation
- Sertifika yenileme basarisiz -> J4 (Server Monitor) alert
- DNS propagation sorunu -> J2 (Cloud Deploy Agent)
