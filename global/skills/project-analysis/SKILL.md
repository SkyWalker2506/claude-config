# /project-analysis

> **ÖNEMLİ — skill başlamadan önce:**
> Kullanıcıya şunu göster:
>
> ```
> Analiz başlamadan önce /compact önerilir (agent'lar çok token tüketir).
>
>   1) /compact çalıştır, sonra devam et
>   2) Geç ve devam et
> ```
>
> Kullanıcı "1" yazarsa → `/compact` çalıştırmasını hatırlat, çalıştırdıktan sonra devam et.
> Kullanıcı "2" veya sadece Enter basarsa → direkt devam et.

Bu skill tetiklendiğinde aşağıdaki adımları izle:

## Referans

Tam protokol: `__PROJECTS_ROOT__/PROJECT_ANALYSIS.md`

O dosyayı oku ve içindeki talimatlara **harfiyen** uy.

---

## Adım 1 — Agent atama modunu sor

```
Analiz için ajan atama modunu seç:
  1) Lead Orchestrator — A1 projeyi inceler, her departman için Lead + ajan atar
  2) Manuel            — her kategori için ajan ve modeli kendim seçerim
  3) Hızlı             — tüm kategoriler Sonnet ile, standart agent'lar

Seçiminiz (1/2/3):
```

**1 seçilirse (Lead Orchestrator):**
- A1 (Lead Orchestrator) kısa bir proje taraması yapar
- Her Lead departmanı için: hangi kategoriler, hangi worker agent'lar, hangi modeller → bir atama haritası çıkarır
- Kullanıcıya haritayı göster, onay al
- Leads'leri paralel başlat (`run_in_background=true`)

**2 seçilirse (Manuel):**
- Her kategori için sırayla sor: `Evet / Hayır / Kısmen`
- Kabul edilen her kategori için: hangi agent ID? hangi model?
- `PROJECT_ANALYSIS.md` §3'teki kategori + agent eşleşme tablosuna bak, öner

**3 seçilirse (Hızlı):**
- Tüm 12 kategoriyi Sonnet modeli + varsayılan agent'larla başlat (kategori seçimi yok)

## Adım 2 — Lead'leri başlat (paralel, background)

Her Lead departmanı için bir Agent başlat (`run_in_background=true`).

Lead agent prompt şablonu (`PROJECT_ANALYSIS.md` §5'teki şablonu kullan):
- Lead rolü ve sorumlu kategoriler
- Her kategori için atanan worker agent ve model
- Proje kökü
- Çıktı: `[PROJE]/analysis/[NN_kategori].md`

Lead yapısı:
- **ArtLead**    → UI/UX (#1), Content (#8), Accessibility (#11)
- **CodeLead**   → Performance (#2), Data (#4), Architecture (#10)
- **GrowthLead** → SEO (#3), Growth (#6), Analytics (#9)
- **BizLead**    → Monetization (#5), Competitive (#12)
- **SecLead**    → Security (#7)

## Adım 3 — Watchdog

Her 3 dakikada bir durum göster:
```
Analiz durumu (X/Y tamamlandı):
✅ ArtLead  (UI/UX, Content, Accessibility)
✅ SecLead  (Security)
⏳ CodeLead (Performance ✅, Data ✅, Architecture ⏳)
⏳ GrowthLead (SEO ✅, Growth ⏳, Analytics ⏳)
⏳ BizLead  (Monetization ⏳, Competitive ⏳)
```
8 dakika geçen lead → kullanıcıya sor, onay gelirse yeniden başlat.

## Adım 4 — Master rapor

Tüm Lead'ler tamamlanınca bir **Opus agent** başlat:
- Tüm kategori raporlarını oku
- `[PROJE]/analysis/MASTER_ANALYSIS.md` oluştur
- `PROJECT_ANALYSIS.md` §6'daki master rapor yapısını kullan
- Cross-cutting insights + top 20 aksiyon listesi + maliyet tablosu

## Adım 5 — Kullanıcıya göster

1. Master rapor özeti
2. Dosya konumları
3. En kritik 5 aksiyon
