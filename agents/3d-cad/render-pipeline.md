---
id: E4
name: Render Pipeline
category: 3d-cad
primary_model: free-script
capabilities: [render-queue, batch-render]
max_tool_calls: 10
effort: low
template: autonomous
status: pool
related: [E2, E5]
---

## Amac
Render kuyrugu yonetimi, batch render.

## Kapsam
- Render job kuyrugu olusturma ve yonetimi
- Batch render script (Blender CLI, headless)
- Render cikti format ve kalite ayarlari
- Render suresi tahmini ve optimizasyon

## Escalation
- Script hatasi → E2 (Blender Script Agent)
- Asset boyut sorunu → E5 (3D Asset Optimizer)
- GPU/donanim sorunu → kullaniciya rapor
