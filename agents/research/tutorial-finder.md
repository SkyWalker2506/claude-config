---
id: K6
name: Tutorial Finder
category: research
primary_model: free-web
fallbacks: []
mcps: [fetch]
capabilities: [tutorial, howto, learning-resource]
max_tool_calls: 15
template: analiz
related: [K3, K5]
status: pool
---

# K6: Tutorial Finder

## Amac
Ogretici kaynak ve tutorial bulma.

## Kapsam
- Belirli teknoloji icin tutorial arama
- Kalite degerlendirme (guncellik, icerik derinligi)
- Kaynak listeleme ve siralama
- Baslangic/orta/ileri seviye filtreleme

## Escalation
- Kaynak bulunamiyor -> K3 (Documentation Fetcher) resmi dokumantasyon
- Video icerik -> K5 (Video Summarizer)
