# Model Yonlendirme — kim hangi isi yapar

> Tek kaynak. Skill'ler ve agent'lar model secimini burada tanimlar, kendi
> icinde tekrar etmez. Degisiklik burada yapilir.

## KURAL: Gemini = sadece Gemini 4 Argon, varsayilan low (Musab, 2026-10-14)

1. Gemini'ye giden her is **`gemini-4-argon-low` + `--effort low`** ile kosar. `agy-task.sh` varsayilani da budur.
2. **Gemini 3 serisi (3.x Flash/Pro) kullanilmaz.** Hicbir is icin, fallback olarak bile.
3. Effort **sadece sorun cikan iste** artirilir. Is yanlis, eksik ya da uydurma donerse (olmayan dosya adi, tutmayan iddia), ayni is `gemini-4-argon-medium`/`medium` ile, o da yetmezse `-high`/`high` ile yeniden kosar. Model id'si ile `--effort` eslesmeli; `xhigh`/`max` reddedilir.
4. Claude yonetici konumunda durur. Isi Argon'a verir, ciktiyi `git diff` ve testlerle dogrular, merge eder ve raporlar. Argon'un yapabilecegi is Claude'da tutulmaz.
5. Gemini kotasi biterse (429), kota gelene kadar is Claude'da devam eder. Gemini 3'e dusulmez.

## Kural: is **gereken dusunme turune** gore yonlendirilir, kolayliga gore degil

| Is | Motor | Nasil |
|---|---|---|
| Tasarim, mimari, kapsam kesme, sanat yonu, bulanik brief, "neden eglenceli degil" | **Fable 5** (plan) → **Opus 5** (uygula) | Claude'da kalir, delege edilmez |
| Gercekten zor implementasyon: yeni matematik, cetrefil shader, perf gizemi, teshissiz bug | **Opus 5** | Claude'da kalir |
| Mekanik kod: scaffold, boilerplate, rename, refactor, config, test iskeleti, doc sync, format gecisi, modul baglama | **`agy` ile Gemini** | `~/Projects/ClaudeHQ/scripts/hq agy "<gorev>" --dir <proje>` |
| Genis paralel is: bagimsiz moduller, asset manifest, icerik verisi, QA taramasi, bolum ozeti | **Gemini teamwork** | `agy` + `define_subagent` / `invoke_subagent` / `/teamwork-preview` |
| Konsept sanat, placeholder sprite, stil arama, asset uretimi | **Gemini `generate_image`** | `agy` uzerinden |
| Video / hareket referansi | **Web'de Gemini** | tarayicidan gemini.google.com; `agy`'de video motoru yok |

## Sonnet ve Haiku delegasyon hedefi degildir

Kucuk bir Claude kademesinin kullanilacagi her yerde **`agy` uzerinden Gemini**
gecer. Abonelikle faturalanir, headless kosar ve mekanik iste dusurulmus bir
Claude kademesinden guclu.

Sonnet/Haiku yalnizca kullanici oturum modelini oyle sectiyse ana dongude
gorunur — o zaman da delege edilen ise degil, konusmaya aittir.

## Kotadan cekinme

Kota korkusu isi ic tarafta tutmak icin gerekce degildir. Paralel `agy` seritleri
kos, subagent takimi serbestce ac, stil tutana kadar gorseli yeniden uret.
Varsayilan `gemini-4-argon-low` + `--effort low`. Is yanlis, eksik ya da uydurma donerse ayni isi `-medium`/`medium`, gerekirse `-high`/`high` ile yeniden kos. **Sadece Gemini 4 Argon kullanilir; Gemini 3 serisi (3.x Flash/Pro) kullanilmaz** (Musab, 2026-10-14).
Argon'da effort model id'sine gomulu oldugu icin ikisi eslesmeli; `xhigh`/`max` reddedilir.

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
