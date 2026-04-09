---
name: dashboard
description: Terminal dashboard — cache'ten oku, sifir token. Taze veri icin /dashboard-sync kullan.
---

## /dashboard

Cache'ten oku ve dashboard'u goster. Sifir token.

## Uygulama

```bash
python3 scripts/dashboard.py
```

Ciktidan sonra ek aciklama YAZMA.
Cache yoksa: "Cache yok, /dashboard-sync calistir" uyari ver.

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
