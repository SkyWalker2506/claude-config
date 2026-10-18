# Model Yonlendirme — kim hangi isi yapar

> Tek kaynak. Skill'ler ve agent'lar model secimini burada tanimlar, kendi
> icinde tekrar etmez. Degisiklik burada yapilir.

## KURAL: ayak isi zinciri = Gemini 3.8 Flash high -> Haiku 5.5 -> Sonnet 5.5 (Musab, 2026-10-18)

1. **Ilk tercih Gemini:** her ayak isi (mekanik kod, rename, doc sync, manifest, QA taramasi, kare inceleme) `agy` ile **`gemini-3.8-flash-high` + `--effort high`** kosar. `agy-task.sh` varsayilani budur. Argon kullanilmaz (cok pahali).
2. **Gemini yetersiz kalirsa Haiku 5.5:** ayni isi Claude subagent'ina `model: haiku`, `effort: low` ile ver (dusunme gerektiren is: `medium`). Haiku 5.5 fiyati 100K token'a kadar $0.10/$0.50; 100K'yi asan istekte $0.50/$2.50 (5 kat). Bu yuzden Haiku isi **100K altinda** tutulur:
   - `~/.claude/settings.json` -> `modelSettings.claude-haiku-5-5.autoCompactWindow: 100000` (alt sinir 100K; Haiku oturumu bu pencerede auto-compact olur).
   - Haiku subagent frontmatter'i: `autoCompactWindow: 100000`.
   - Brief kisa, dosya listesi dar; buyuk dosyalari okutma, gereken bolumu ver.
3. **Haiku yetersizse Sonnet 5.5** (`model: sonnet`, `effort: medium`; kolay iste `low`). Not: 100K ustu Haiku bile Sonnet'ten ~4 kat ucuz ($0.50/$2.50 vs $2/$10); Sonnet'e gecis kalite icindir, fiyat icin degil. 100K'yi asacagi belli buyuk baglamli isler (cok dosya, uzun log) dogrudan Sonnet'e gider.
4. Opus / Fable sadece tasarim, zor teshis ve ana dongu icindir; ayak isine verilmez. Fable sadece arastirma.
5. Claude yonetici konumunda durur: isi zincire verir, ciktiyi `git diff` ve testlerle dogrular, merge eder, raporlar.
6. Gemini kotasi biterse (429) zincir Haiku'dan devam eder.
7. **Abonelik notu (2026-10-18, YouTube oturumu ile dogrulandi):** Sonnet 5.5 ve Opus 5.5'te 100K esigi yok (duz fiyat). Haiku'nun 100K/5x fiyati resmi olarak sadece API fiyati; Max plan sayacina uygulanip uygulanmadigi yazili degil. Plan kullaniminda modellerin farkli agirliklandigina dair resmi bilgi yok. Subagent'lar (Haiku olsa da) ana oturumla ayni 5 saatlik/haftalik limitten yer; Opus/Sonnet'in ek aile limitleri var. En buyuk kota yakici uzun ana oturumlardir: baglam buyuyunce ozetle veya yeni oturum ac.
8. **Effort hipotezi (olculmedi):** Haiku-high ile Sonnet-medium benzer sonuc verebilir. Olcum gelene kadar zincirdeki varsayilanlar gecerli.

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
