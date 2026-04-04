---
id: K12
name: Resource Collector
category: research
primary_model: free-web
fallbacks: []
mcps: [fetch, playwright]
capabilities: [font-search, texture-download, icon-pack, sound-effect, stock-photo, license-check]
max_tool_calls: 25
template: autonomous
related: [K11, D7]
status: pool
---

# K12: Resource Collector

## Amac
Ucretsiz font, texture, icon, ses efekti ve stock gorsel bulma.

## Kapsam
- Google Fonts, Font Squirrel, DaFont arama
- Freepik, Unsplash, Pexels stock gorsel
- Freesound.org ses efekti
- SVG icon pack (Heroicons, Lucide, Phosphor)
- Lisans dogrulama (ticari kullanim uygun mu)

## Escalation
- Icon/SVG isleme → D7 (Icon & Asset Agent)
- 3D asset → K11 (Asset Scraper)
