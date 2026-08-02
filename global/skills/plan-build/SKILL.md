---
name: plan-build
description: "Fable planlar, Opus paralel uygular. Is paketlerine bol, dosya sahipligini ayristir, dalga dalga calistir, her pakete kendi effort'unu sec. Triggers: plan-build, fable ile planla, opus ile uygula, paralel gelistir, planla ve uygula, dual model build."
user-invocable: true
argument-hint: "[hedef tanimi] veya [plan|build|status|resume]"
---

# /plan-build — Fable planlar, Opus paralel uygular

Iki modeli **yaptiklari isin dogasina gore** ayirir: plan yazmak arama ve secim isidir
(Fable), kod yazmak uygulama ve dogrulama isidir (Opus). Aralarindaki tek sozlesme
**is paketi tanimi**dir.

Bu skill'in tek gercek katkisi paralellik degil — **paralelligi guvenli kilan kisit**tir:
iki paket asla ayni dosyayi yazamaz. O kisit saglanmadan paralel calistirmak, agent'larin
birbirinin isini ezmesiyle biter ve seri calismaktan yavastir.

## Argumanlar

| Arg | Ne yapar |
|-----|----------|
| *(hedef metni)* | Bastan sona: recon → Fable plan → kapi → Opus dalgalari → entegrasyon |
| `plan` | Sadece plani uret ve `.plan-build/plan.json`'a yaz, uygulama yok |
| `build` | Mevcut `plan.json` ile uygulama dalgalarini calistir |
| `status` | Hangi paket bitti, hangi dalga acik, hangi kapi kirmizi |
| `resume` | Yarim kalan dalgadan devam et (biten paketleri tekrar calistirma) |

---

## Faz 0 — Recon: kendin yap, delege etme

**Is listesini belirleyen kesfi asla delege etme.** Plan yazacak olan Fable, ne oldugunu
degil ne yapilacagini kararlastirir. Ne oldugunu sen olcersin:

- Repo agaci, mevcut modul sinirlari, derleme/test komutu
- Ilgili knowledge paketleri (`bm-*` hatlari, proje `docs/AI/STATE.md`)
- **Kasitli eksikler** — "TAMAMLAMAYIN" listesi varsa plana kisit olarak girer
- Calisan test suite'i var mi, yesil mi (kirmizidan baslamak paketleri birbirine bulastirir)

Bu fazin ciktisi 20-40 satirlik bir **olgu ozeti**dir. Tahmin degil, olculmus sey.

## Faz 1 — Plan: Fable

Tek `Agent` cagrisi, `model: "fable"`. Prompt'a Faz 0 ozeti + hedef girer. Istenen cikti
sabit semali:

```json
{
  "packages": [
    {
      "id": "P1",
      "title": "Sprite slicing pipeline",
      "why": "Digerlerinin girdisi; once bu bitmeli",
      "owns": ["tools/slice.py", "tools/README.md"],
      "reads": ["ArtSource/AssetManifest.json"],
      "depends_on": [],
      "effort": "medium",
      "gate": "python tools/slice.py --verify → 0 exit, 44 dosya uretir",
      "done_when": "Her sheet icin manifest'teki slice sayisi kadar PNG var"
    }
  ],
  "waves": [["P1"], ["P2","P3","P4"], ["P5"]]
}
```

### Plan'in tasimasi zorunlu dort sey

| Alan | Neden zorunlu |
|---|---|
| `owns` — yazilacak dosyalarin **tam** listesi | Paralelligin tek guvenlik mekanizmasi. Bos veya "vs" iceren liste plani reddettirir |
| `gate` — **calistirilabilir** dogrulama | "Test edildi" bir iddia; `dotnet test` bir olcum. Kapi komut degilse paket bitmis sayilmaz |
| `depends_on` | Dalga hesabinin girdisi. Yanlissa paralel calisanlar birbirinin yarim ciktisini okur |
| `effort` | Asagidaki tabloya gore; paket bazinda, tek tip degil |

### Effort secimi — paket bazinda, tavan `high`

Bunu **model kendi secer**, kullaniciya sormaz:

| Isin dogasi | Effort |
|---|---|
| Mekanik, tek dosya, spec net (boilerplate, config, rename, doc) | `low` |
| Sinirli kapsam, bilinen desen (CRUD, veri sinifi, basit UI) | `medium` |
| Tasarim karari iceren kod, cok dosyali ozellik, hata ayiklama, mimari | `high` |

**Tavan `high`.** `xhigh`/`max`'e cikmak icin kullanicinin acik izni gerekir. Sebep olculmus:
Artificial Analysis'in effort taramasinda skor monoton artiyor ama high→max arasi ~%70 maliyet
artisina karsilik kazanc kucuk. Yani "yuksek effort daha kotu sonuc verir" yanlis — "her zaman
parasini hak etmez" dogru.

## Faz 2 — Plan kapisi: kendin dogrula, Fable'a geri gonder

Plani **uygulamadan once** su kontrollerden gecir. Bunlar saf veri kontrolu, model yorumu degil:

1. **Dosya sahipligi ayrik mi?** Ayni dalgadaki iki paketin `owns` kumeleri kesisiyorsa → RED
2. **Her paketin kapisi calistirilabilir mi?** Komut yoksa veya "manuel kontrol" diyorsa → RED
3. **Bagimlilik dongusu var mi?** DAG degilse → RED
4. **Paket sisman mi?** `owns` > 12 dosya veya iki ayri sorumluluk → bolunmeli
5. **Faz 0'daki "TAMAMLAMAYIN" listesine dokunan paket var mi?** → RED

Kirmizi varsa **tek revizyon turu**: Fable'a sadece ihlalleri gonder, plani bastan yazdirma.
Ikinci turda hala kirmiziysa sorunlu paketi plandan cikar ve kullaniciya bildir — sessizce
kapsam daraltma.

## Faz 3 — Uygulama: Opus, dalga dalga

Her dalga icin **tek mesajda** paralel `Agent` cagrilari, `model: "opus"`, paketin kendi
`effort`u ile. Dalga bitmeden sonraki dalga baslamaz (bagimlilik gercek).

Es zamanli paket sayisi pratikte **4-6**; ustu makine ve dikkat dagitir.

### Her paket prompt'unun tasimasi gerekenler

```
PAKET: {id} — {title}
NEDEN: {why}
YAZABILECEGIN DOSYALAR: {owns}   ← bu listenin disina cikma
OKUYABILECEGIN: {reads}
KAPI: {gate}                      ← bitirmeden once bunu CALISTIR
BITTI SAYILIR: {done_when}

KISITLAR
- owns disindaki hicbir dosyayi degistirme. Gerekiyorsa DUR ve rapor et.
- Istenmeyeni ekleme: yeni ozellik, yeni bagimlilik, yeni soyutlama katmani yok.
- Commit ATMA. Calisma agacini birak, entegrasyonu orkestrator yapar.
- Kapi kirmizi kaliyorsa duzeltmeye calis; olmuyorsa NEDEN oldugunu yaz, yesil taklidi yapma.
```

Son uc madde tesadufi degil, her biri yasanmis bir hatanin karsiligi:
scope creep, canli agent agacinin commit'lenmesi, ve yesil rapor eden kirmizi kapi.

### Unity ve worktree

`isolation: "worktree"` cogu repoda dogru cevap; **Unity projelerinde degildir** —
her worktree kendi `Library/`'sini bastan uretir, dakikalar gider ve `.meta` GUID'leri
carpisir. Unity'de tek calisma agaci + ayrik `owns` kullan.

Worktree kullanacaksan: **once base'i push et.** Push edilmemis base uzerinde acilan
worktree'ler birlesmez.

## Faz 4 — Entegrasyon kapisi

Dalgalar bittikten sonra, **paket kapilarindan bagimsiz olarak**:

1. Tam derleme (Unity: `-batchmode -quit` + hata grep'i; .NET: `dotnet build`)
2. Tum test suite'i — dokunulan **her** repoda, sadece ana repoda degil
3. Degisiklik ozetini oku: plan disi dosya degismis mi? Degistiyse hangi paket, neden?

Paket kapilarinin hepsi yesilken entegrasyonun kirmizi olmasi normaldir ve **bilgi tasir**:
paketler arasi sozlesme yanlis kurulmus demektir. Bunu plan hatasi olarak kaydet.

Kapi yesilse commit + push. Mesaj paket id'lerini tasisin.

## Faz 5 — Ne ogrendik

`.plan-build/run-{tarih}.json`: paket basina sure, kapi ilk seferde yesil miydi, plan disi
dosya dokunusu, revizyon turu sayisi.

Uc tekrar eden sinyal, uc farkli teshis:

| Sinyal | Teshis |
|---|---|
| Kapi cogu pakette ilk seferde kirmizi | `done_when` yeterince kesin yazilmamis |
| Paketler surekli `owns` disina tasiyor | Paket sinirlari gercek modul sinirlariyla ortusmiyor |
| Entegrasyon kirmizi, paketler yesil | Paketler arasi sozlesme plan asamasinda tanimlanmamis |

## Yapma

- **Recon'u delege etme.** Is listesini bilmeden plan istemek, plani tahmine dayandirir.
- **`owns` olmayan plani calistirma.** Paralellik o listeye dayaniyor; yoksa seri calis.
- **Paket icinde plan yazdirma.** Opus paketi uygular; kapsami yeniden tartisirsa paket coker.
- **Kirmizi kapiyi "sonra bakariz"a birakma.** Sonraki dalga onun ciktisini girdi sanar.
