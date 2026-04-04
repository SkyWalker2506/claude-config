---
id: K5
name: Video Summarizer
category: research
primary_model: local-qwen-9b
fallbacks: []
mcps: [fetch]
capabilities: [youtube-transcript, video-summary]
max_tool_calls: 15
template: analiz
related: [K1, K6]
status: pool
---

# K5: Video Summarizer

## Amac
YouTube ve video transkript ozetleme.

## Kapsam
- Transkript indirme (fetch MCP)
- Anahtar noktalar cikarma
- Zaman damgali ozet olusturma
- Icerik kategorize ve etiketleme

## Escalation
- Transkript alinamiyor -> K1 (Web Researcher) alternatif kaynak
- Iliskili tutorial -> K6 (Tutorial Finder)
