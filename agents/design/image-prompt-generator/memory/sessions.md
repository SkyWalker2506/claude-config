# Session Notes

> Onemli kararlar, reasoning ve sonuclar burada kayit altina alinir.
> Format: tarih + karar + neden + sonuc

<!-- Entries will be added by the agent after each significant session -->

## 2026-04-24 — MedievalFactory animation prompts v2 (full rewrite)

- Karar: Tum 15 animasyon promptu sifirdan yazildi. 05_prompts/animation_prompts_v2.md tek kaynak dosya olusturuldu.
- Sebep: Onceki uretimlerde kafa kesilmesi (blacksmith_swing, blacksmith_idle), body drift (miner, peasant), teker donmemesi (cart_wheels), magenta bleed (smoke), stil drift (water/fire) tekrar eden hatalardi.
- Cozum: 8 global kurali (magenta bg + siyah bg istisna + 256x256 frame + FRAMING 20px top/10px bottom + body-identical + GPT Sources ignored + ASCII-only prompt + post-process akisi) her prompta gomdum. Asset-browser missing.json 15 animasyonu status=todo'ya ceviriyor (fire_loop dahil). cart_wheels_8f icin GPT prompt son care; script fallback onerildi.
- Sonuc: Iki dosya degisti -- 05_prompts/animation_prompts_v2.md (yeni), asset-browser/data/missing.json (15 todo entry). Commit+push main branch.
