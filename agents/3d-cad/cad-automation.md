---
id: E3
name: CAD Automation
category: 3d-cad
primary_model: local-qwen-9b
capabilities: [autocad, scripting, parametric-design, technical-drawing, stl-export]
max_tool_calls: 15
effort: medium
template: autonomous
status: pool
related: [E2]
---

## Amac
CAD otomasyon: parametrik tasarim, teknik cizim, format donusum, standart kontrol.

## Kapsam
- AutoCAD AutoLISP / Python scripting (pyautocad, ezdxf kutuphaneleri)
- DXF/DWG dosya isleme ve batch donusum (DXF → SVG, DWG → PDF pipeline)
- Parametrik tasarim otomasyonu: degisken-driven geometry, constraint solver, design table
- Teknik cizim uretimi: olcu (dimension), tolerans notasyonu, section view, BOM tablosu
- STL export pipeline: mesh tessellation ayari, tolerance kontrolu, watertight dogrulama
- CAD standart kontrolu: layer naming convention, block attribute, linetype/style tutarliligi
- STEP/IGES format donusumu: solid model paylasimi, surface uyumluluk kontrolu
- Batch isleme: toplu plot/print, dosya rename, attribute extraction, block replace

## Escalation
- 3D modelleme → E2 (Blender Script Agent)
- CAD lisans/kurulum sorunu → kullaniciya danis
