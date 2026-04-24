# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

<!-- Entries will be added by the agent when discovering useful information -->

## 2026-04-24 — Animation prompt checklist (zorunlu)

Kaynak: MedievalFactory 3+ aylik deneme-yanilma (sessions/asset-review memory'leri).

Her yeni character/creature/FX animasyon prompt'u yazarken bu 8 maddeyi DAHA metin icinde dogrula:

1. **Arka plan:** Solid MAGENTA (#FF00FF). Gri tonlu FX (smoke/dust) icin BLACK (#000000). Transparent ISTEME -- DALL-E guvenilir vermiyor.
2. **Frame boyutu:** Her frame TAM 256x256 px. Kanvas = N * 256 yatay.
3. **FRAMING:** Top-of-head 20 px alt, feet 10 px ust, max yukseklik 220 px. Sigmazsa "shrink composition, do NOT crop" yaz.
4. **BODY IDENTICAL:** Tum frame'lerde govde/palet/cizgi AYNI; feet pixel-anchor sabit; yalniz hareket eden kisim degisir.
5. **Per-frame tarif:** Frame sayisi kadar numaralandirilmis, kesin poz/aci/efekt icerir. "F6 blends to F1" seamless loop vurgusu.
6. **Stil:** Manor Lords + Kingdom Rush painterly; warm palette; NO outline / NO pixel art / NO anime / NO 3D.
7. **GPT Sources ignored:** Referans PNG yukleme bos; stil TAMAMEN metin icinde lafzen tarif edilmeli. "match X.webp" tek basina yetersiz.
8. **ASCII-only:** Copyable prompt icinde Unicode ok/em-dash yok; `->`, `--`, `[ ]`, `x` kullan.

**GPT limit kurali:** 2 denemede basarisiz olursa -> script/ImageMagick fallback oner. Tipik basarisizliklar: teker rotasyonu, 8f karakter kimlik tutarliligi, perfect transparency, complex radial sparks.

**Uygulama:** Her prompt bloku section 0 global + section per-anim yapisi. asset_generation_master.md'yi zamanla deprecate et; animation_prompts_v2.md tek kaynak olsun.
