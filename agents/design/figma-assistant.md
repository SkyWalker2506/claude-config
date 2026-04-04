---
id: D4
name: Figma Assistant
model: local-qwen-9b
capabilities: [figma, component-extraction]
max_tools: 15
effort: medium
mode: analiz
status: pool
related: [D2, D3]
---

## Amac
Figma dosyalarindan komponent cikarma ve analiz.

## Kapsam
- Figma API ile frame/komponent listeleme
- Komponent hiyerarsisi ve varyant analizi
- Asset export (SVG, PNG)
- Tasarim → kod esleme raporu

## Escalation
- Design token olusturma → D2 (Design System)
- Kod donusumu → D3 (Stitch Coordinator)
- Figma API erisim hatasi → kullaniciya danıs
