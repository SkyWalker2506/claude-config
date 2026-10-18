# Model Yonlendirme — kim hangi isi yapar

> Tek kaynak. Skill'ler ve agent'lar model secimini burada tanimlar, kendi
> icinde tekrar etmez. Degisiklik burada yapilir.

## KURAL: ayak isi zinciri = Gemini 3.8 Flash high -> Haiku 5.5 -> Sonnet 5.5 (Musab, 2026-10-18; karar: Jarvis/Opus, resmi dokumanlara dayali)

### Veri (platform.claude.com pricing + effort + cost-optimization sayfalari, 2026-10-18)
| Model | Girdi / cikti $/MTok | Cache okuma | Not |
|---|---|---|---|
| Haiku 5.5, prompt <=100K | 0.10 / 0.50 | 0.01 | cache okuma/yazma da prompt uzunluguna sayilir |
| Haiku 5.5, prompt >100K | 0.50 / 2.50 | 0.05 | 5 kat |
| Sonnet 5.5 | 2 / 10 | 0.10 | 100K esigi yok |
| Opus 5.5 | 4 / 20 | 0.20 | 100K esigi yok |
- Olculmus tek karsilastirma: GPQA'da Haiku 5.5 medium %85, Sonnet 5.5 %91; Haiku'nun dogru cevap basina maliyeti Sonnet'in ~1/10'u.
- "Haiku high = Sonnet medium" olculmus degil. Fiyat farki token basina ~20 kat (<=100K) / ~4 kat (>100K); Haiku high + bir tekrar bile Sonnet medium'dan ucuz kalir.
- Dokuman: dusuk effort ile kos, sadece basarisiz olanlari yuksek effort ile tekrar kos -> ayni basari, ~%40 daha ucuz. O da yetmezse bir ust kademe, kendi varsayilan effort'unda.

### Ana kural (Musab, 2026-10-18; tum oturumlar ve PC'ler icin ortak)
1. Her **is tipi** kendine yeterli gorulen effort'tan baslar (asagidaki tablo). Gemini 3.8 Flash, Haiku ve Sonnet icin ayni mantik.
2. Sonuc yetersizse **o is tipi** icin effort bir basamak artar, tekrar denenir; yine olmazsa bir basamak daha.
3. En ust effort'ta da olmazsa bir ust model: Flash -> Haiku -> Sonnet. Opus sadece gercek ihtiyacta, Fable cok buyuk ihtiyacta (arastirma).
4. Sonuc not edilir: is tipi, model, effort, basarili mi. Is tipinin varsayilani zamanla buna gore ayarlanir (proje icinde `docs/model-routing-notes.md`).
5. Yeni model cikinca degerlendirilir, uygunsa gecilir. **Argon sisteme hic girmez.**
6. **Yerel modeller (Ollama vb.) kullanilmaz:** yerel ekran karti ses uretimi ve Unity icin ayrilmis.

### Is tipi -> baslangic
| Is tipi | Baslangic | Basarisizsa |
|---|---|---|
| Rename, format, manifest, json/data duzeltme, commit mesaji | Flash low | Flash medium -> Haiku low |
| Log/test ciktisi ozeti, hata ayiklama ozeti, dosya arama | Flash medium | Haiku low -> medium |
| Test iskeleti, doc sync, modul baglama, birkac dosyalik refactor | Flash medium | Flash high -> Haiku medium -> high |
| Kare/still/contact sheet QA | Flash medium | Haiku medium (Claude supheli kareyi kendisi acar) |
| Cok adimli ajan isi, bilgi isi, uzun gorev | Haiku medium | Haiku high -> Sonnet medium |
| Belirsiz brief, cok dosyali tasarim karari, ince bug, uzun baglamda bilgi bulma | Sonnet medium | Sonnet high -> Opus |
| Tasarim, mimari, son karar | Opus medium | Opus high |

### Baglam bariyeri (Haiku 100K)
- Global: `~/.claude/settings.json` -> `modelSettings.claude-haiku-5-5.autoCompactWindow: 100000`. Claude Code'un izin verdigi en dusuk deger 100000 (90000 kabul edilmez); compaction pencerenin dolmasindan once tetiklenir.
- Haiku subagent frontmatter: `model: haiku`, `effort: <tablodan>`, `autoCompactWindow: 100000`.
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` kullanilmaz: global, Opus/Sonnet oturumlarini da erken compact eder.
- Brief'e dosya yolu ver, dosyayi yapistirma; sonucu dosyaya yazdir, ozet don. Buyuk log/dosyanin sadece ilgili bolumunu oku.
- Isin 100K'yi asacagi bastan belliyse ve cikti kolay kontrol edilemiyorsa dogrudan Sonnet medium.

### Zincir
1. **Gemini 3.8 Flash** (`agy`; baslangic seviyesi yukaridaki tablodan, `AGY_MODEL=gemini-3.8-flash-<low|medium|high>` + eslesen `AGY_EFFORT`; `agy-task.sh` varsayilani medium). Argon yok. Kota bitikse (429) bu adim atlanir, Haiku'dan devam edilir.
2. **Haiku 5.5** (subagent `model: haiku`):
   - `low`: tek dosya, mekanik, ciktisi kontrol edilebilir is (rename, format, manifest, commit mesaji, log/test ciktisindan hata ayiklama ozeti, json/data duzeltme).
   - `medium` (varsayilan): cok adimli ama iyi tanimli is (test iskeleti, modul baglama, birkac dosyalik refactor, doc sync, kare/still QA).
   - `high`: daha uzun ajan isi, bilgi isi; ya da medium'da basarisiz olan is.
   - **Baglam <100K**: `modelSettings.claude-haiku-5-5.autoCompactWindow: 100000` (global), frontmatter'da `autoCompactWindow: 100000`. Brief'e dosya yolu ver, dosya yapistirma; sonucu dosyaya yazdir.
3. **Sonnet 5.5** (`model: sonnet`, `effort: medium`; sohbet/basit is `low`; zor is `high`). Gecis sebebi **kalite**, fiyat degil:
   - Haiku high'da da basarisiz olan is.
   - Muhakeme agirlikli is: belirsiz brief, cok dosyali tasarim karari, ince bug teshisi, gercekten uzun baglamda bilgi bulma.
   - 100K ustune cikacak ama ciktisi kolay kontrol edilemeyen is. (Kontrol edilebilir ve >100K ise Haiku medium + compaction yine 4 kat ucuz.)
4. **Opus 5.5 medium**: ana dongu, tasarim, zor teshis, son karar. **Fable**: sadece arastirma.
5. Gemini kotasi biterse (429) zincir Haiku'dan devam eder. Claude yonetici: isi zincire verir, ciktiyi `git diff` + testlerle dogrular, merge eder, raporlar.

### Abonelik notu
Haiku'nun 100K/5x fiyati resmi olarak API fiyati; Max plan sayacina nasil yansidigi yazili degil, plan kullaniminda model agirliklari resmi degil. Subagent'lar ana oturumla ayni 5 saatlik/haftalik limitten yer; Opus/Sonnet'in ek aile limitleri var. En buyuk kota yakici uzun ana oturumdur: baglam buyuyunce ozetle / yeni oturum ac.

### Acik olcum
Haiku high vs Sonnet medium bizim isimizde olculmedi. Kontrol edilebilir 10-20 gercek ayak isiyle (test gecer / diff dogru) bir tur olcum yapilinca bu bolum guncellenir.

## Kural: is **gereken dusunme turune** gore yonlendirilir, kolayliga gore degil

| Is | Motor | Nasil |
|---|---|---|
| Tasarim, mimari, kapsam kesme, sanat yonu, bulanik brief, "neden eglenceli degil" | **Fable 5** (plan) → **Opus 5** (uygula) | Claude'da kalir, delege edilmez |
| Gercekten zor implementasyon: yeni matematik, cetrefil shader, perf gizemi, teshissiz bug | **Opus 5** | Claude'da kalir |
| Mekanik kod: scaffold, boilerplate, rename, refactor, config, test iskeleti, doc sync, format gecisi, modul baglama | **`agy` ile Gemini** | `~/Projects/ClaudeHQ/scripts/hq agy "<gorev>" --dir <proje>` |
| Genis paralel is: bagimsiz moduller, asset manifest, icerik verisi, QA taramasi, bolum ozeti | **Gemini teamwork** | `agy` + `define_subagent` / `invoke_subagent` / `/teamwork-preview` |
| Konsept sanat, placeholder sprite, stil arama, asset uretimi | **Gemini `generate_image`** | `agy` uzerinden |
| Video / hareket referansi | **Web'de Gemini** | tarayicidan gemini.google.com; `agy`'de video motoru yok |

## Kotadan cekinme

Kota korkusu isi ic tarafta tutmak icin gerekce degildir. Paralel `agy` seritleri
kos, subagent takimi serbestce ac, stil tutana kadar gorseli yeniden uret.
Varsayilan `gemini-3.8-flash-high` + `--effort high`; is yanlis/eksik donerse zincirde bir sonraki kademeye (Haiku, sonra Sonnet) gecilir. Argon kullanilmaz (Musab, 2026-10-18).
Effort model id'sine gomulu oldugu icin ikisi eslesmeli; `xhigh`/`max` reddedilir.

Kisitlama **sadece gercek rate-limit hatasi** gelince devreye girer; o zaman da
tum delegasyon birakilmaz, o serit geri cekilir.

## Delegasyonun satin almadigi tek sey

`agy` ciktisi **iddiadir, kanit degil.** Her delege is `git diff` / dosya okumasi /
sayfayi acma ile biter. "Yaptim ve dogruladim" diyen rapor, disk onaylayana kadar
hicbir sey ifade etmez. Delege kosular raporunu proje icindeki
`docs/runs/<YYYY-MM-DD-HHMM>-<slug>.md` dosyasina yazar.

## Paralelligi nerede kurmali

Olculmus: ayni icerik tek odakli gecise **18 dakika**, 19 pakete bolunmus 14 ajanli
kosuda **5 saat**. Kayip arayuz kesfindeydi — paketler birbirinin seklini ogrenmeyi
bekledi, ikisi ayni nesne icin cakisan sema uydurdu.

**Arayuz paylasmayan eksende paralellestir.** Sanat, icerik verisi, QA ve arastirma
birbirini beklemez; cekirdek dongu bekler. Her delege seride acik dosya sahipligi
satiri ver:

> Sadece su dosyalara yaz: `<liste>`. Baska bir dosya degismesi gerekiyorsa yapma,
> rapor et.

## Antigravity tarafinda

`agy` bu tabloda **uygulayicidir**, yonlendirici degil. Antigravity icinde kosarken
model secimi `--model` / `--effort` ile disaridan verilir; skill kendi icinde model
secmez.
