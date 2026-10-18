# Model Yonlendirme — kim hangi isi yapar

> Tek kaynak. Skill'ler ve agent'lar model secimini burada tanimlar, kendi
> icinde tekrar etmez. Degisiklik burada yapilir.

## Kural: is **gereken dusunme turune** gore yonlendirilir, kolayliga gore degil

| Is | Motor | Nasil |
|---|---|---|
| Tasarim, mimari, kapsam kesme, sanat yonu, bulanik brief, "neden eglenceli degil" | **Fable 5** (plan) → **Opus 5** (uygula) | Claude'da kalir, delege edilmez |
| Gercekten zor implementasyon: yeni matematik, cetrefil shader, perf gizemi, teshissiz bug | **Opus 5** | Claude'da kalir |
| Mekanik kod: scaffold, boilerplate, rename, refactor, config, test iskeleti, doc sync, format gecisi, modul baglama | **`agy` ile Gemini** | `~/Projects/ClaudeHQ/scripts/hq agy "<gorev>" --dir <proje>` |
| Genis paralel is: bagimsiz moduller, asset manifest, icerik verisi, QA taramasi, bolum ozeti | **Gemini teamwork** | `agy` + `define_subagent` / `invoke_subagent` / `/teamwork-preview` |
| Konsept sanat, placeholder sprite, stil arama, asset uretimi | **Gemini `generate_image`** | `agy` uzerinden |
| Video / hareket referansi | **Web'de Gemini** | tarayicidan gemini.google.com; `agy`'de video motoru yok |

## Kullanıcının genel kota ve bağlam tercihi — 2026-10-18

Bu tercih tüm projelerde geçerlidir; önceki Sonnet/Haiku delegasyon yasağının yerine geçer.
- Rutin/ayak işleri için öncelik **Gemini 3.8 Flash High**, kullanılabilir model kimliğini gerçek sağlayıcı/CLI üzerinden doğrula. Başka bir modeli bu adla sunma.
- Gemini kotasının gerçekten bittiği doğrulanırsa **Haiku** kullan. Kimlik doğrulama/boş çıktı/araç hatası kota bitişi değildir.
- Haiku'da bağlamı **100k token altı** tut; hedef olarak **90k civarında compact** et. Compact sonrası görev, kanıtlar, dosya sahipliği ve açık işler korunmalı. Ölçülemeyen bağlam için sahte token sayısı verme.
- İşin 100k üstünde bağlam gerektirmesi kaçınılmazsa **Sonnet'e geç**; bunu 100k eşiğini aşmadan planla. Desteklenmeyen otomatik model değişimini olmuş gibi raporlama.
- Kullanıcının “100k üstünde Haiku ve Sonnet aynı parayı harcıyor” varsayımı **doğrulanmış fiyat bilgisi değildir**. Güncel resmi sağlayıcı/model fiyatlarını, abonelik/API farkını, cache ücretini ve uzun bağlam eşiklerini araştır; kaynak ve tarihiyle bu notu güncelle. Evrensel 100k fiyat eşiği varsayma.
- Ana ajan karar, teşhis ve doğrulama sorumluluğunu taşır. Proje guardrail'leri önceliklidir: Unity projesinde tek yazıcı ve tek Unity; yardımcılar yalnız ayrılmış salt-okunur snapshot/aday paketlerinde çalışır.

## Kotadan cekinme

Kota korkusu isi ic tarafta tutmak icin gerekce degildir. Paralel `agy` seritleri
kos, subagent takimi serbestce ac, stil tutana kadar gorseli yeniden uret.
Varsayilan `gemini-3.8-flash-high` + `--effort high`.

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
