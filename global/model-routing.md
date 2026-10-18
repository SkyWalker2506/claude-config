# Model Yonlendirme — kim hangi isi, hangi effort'la yapar

> Tek kaynak. Tum oturumlar ve tum PC'ler (Windows, Mac) bunu kullanir. Skill'ler ve
> agent'lar model secimini burada tanimlar, kendi icinde tekrar etmez.
> Son yapilandirma: 2026-10-18 (Musab'in kararlari; Jarvis/Opus derledi).

## 1. Ozet

Ucuzdan basla, yetmezse once effort'u, sonra modeli yukselt:

**Gemini 3.8 Flash → Claude Haiku 5.5 → Claude Sonnet 5.5 → Claude Opus 5.5 → (Fable)**

- Her is tipi kendi baslangic seviyesinden baslar (bolum 4).
- Bir modelde tepe effort'a cikilmaz; `high`'dan sonra bir ust modelin `medium`'una gecilir (bolum 3).
- Sonuclar not edilir, baslangiclar zamanla olcumle ayarlanir (bolum 7).
- **Argon hic kullanilmaz. Yerel modeller (Ollama vb.) kullanilmaz** (ekran karti ses uretimi ve Unity icin).

## 2. Veri

### Fiyat (milyon token basina, girdi / cikti)
| Model | Fiyat | Cache okuma | Not |
|---|---|---|---|
| Gemini 3.8 Flash | aboneyle (API: 0.75 / 3.75*) | — | kota 5 saatlik + haftalik; yuksek effort daha cok kota yer* |
| Haiku 5.5, prompt <=100K | 0.10 / 0.50 | 0.01 | prompt uzunluguna cache okuma/yazma da dahil |
| Haiku 5.5, prompt >100K | 0.50 / 2.50 | 0.05 | 5 kat |
| Sonnet 5.5 | 2 / 10 | 0.10 | 100K esigi yok |
| Opus 5.5 | 4 / 20 | 0.20 | 100K esigi yok |
| Fable 5.1 | 10 / 50 | 0.25 | sadece buyuk arastirma |
| Gemini 4 Argon | API 2 / 10* | — | **kullanilmaz** |

Claude fiyatlari: platform.claude.com pricing sayfasi (2026-10-18). `*` isaretliler Gemini'nin kendi web arastirmasi (2026-10-18), kaynaklari zayif, dogrulanmadi.

### Olculmus / bilinen
- 100K esigi **sadece Haiku'da**. 100K ustunde bile Haiku, Sonnet'ten ~4 kat ucuz → Sonnet'e gecis **kalite** icin, fiyat icin degil.
- GPQA Diamond: Haiku 5.5 medium %85, Sonnet 5.5 %91; dogru cevap basina Haiku ~Sonnet'in 1/10'u (Anthropic "Optimizing for cost and intelligence").
- Anthropic: dusuk effort'la kos, sadece basarisiz olanlari yuksek effort'la tekrar kos → ayni basari, ~%40 ucuz. O da yetmezse bir ust model, kendi varsayilan effort'unda.
- Arastirma/bilgi isinde effort egrisi duz (medium ≈ high); uzun kodlama isinde effort basina birkac puan fark var.
- Gemini Flash (kendi arastirmasi, dogrulanmadi): mekanik duzenleme, log ozeti, kare QA'da iyi; derin bagimli cok dosyali refactor'da baglam kaybi yasar.
- **Olculmedi:** "Haiku high = Sonnet medium". Bolum 7'deki kesisme testiyle olculecek.

### Varsayilan effort'lar
| Model | Seviyeler | Varsayilan |
|---|---|---|
| Gemini 3.8 Flash | low / medium / high | medium (`agy-task.sh` varsayilani) |
| Haiku 5.5 | low … max | medium |
| Sonnet 5.5 | low … max | high (biz medium'dan baslatiriz) |
| Opus 5.5 | low … max | medium |

## 3. Effort tavanlari (model gecis esikleri)

Bir modeli tepe effort'ta zorlamak yerine bir ust modele gec.

| Model | Kullanilan en ust effort | Tavan asilacaksa |
|---|---|---|
| Gemini 3.8 Flash | high | Haiku medium |
| Haiku 5.5 | high | Sonnet medium (Haiku xhigh/max kullanilmaz) |
| Sonnet 5.5 | high | Opus medium (Sonnet xhigh/max kullanilmaz) |
| Opus 5.5 | xhigh, nadiren | Fable (Opus max kullanilmaz; sadece arastirma / cok zor karar) |

## 4. Is tipi → baslangic

| Is tipi | Baslangic | Basarisizsa |
|---|---|---|
| Rename, format, manifest, json/veri duzeltme, commit mesaji | Flash low | Flash medium → high → Haiku medium |
| Log/test ciktisi ozeti, dosya arama, hata ozeti | Flash medium | Flash high → Haiku medium |
| Test iskeleti, doc sync, modul baglama, birkac dosyalik duzenleme | Flash medium | Flash high → Haiku medium → high |
| Kare / still / contact sheet QA | Flash medium | Haiku medium (supheli kareyi yonetici kendisi acar) |
| Konsept gorsel, placeholder sprite, stil arama | Flash (`generate_image`, agy) | — |
| Cok adimli ajan isi, uzun bilgi isi, web arastirmasi ozeti | Haiku medium | Haiku high → Sonnet medium |
| Derin bagimli cok dosyali refactor | Sonnet medium | Sonnet high → Opus medium |
| Belirsiz brief, cok dosyali tasarim karari, ince bug, uzun baglamda bilgi bulma | Sonnet medium | Sonnet high → Opus medium |
| Zor implementasyon (yeni matematik, shader, perf gizemi, teshissiz bug) | Opus medium | Opus high → xhigh |
| Tasarim, mimari, kapsam, son karar | Opus medium | Opus high |
| Buyuk arastirma | Fable | — |

Ana dongu (yonetici) Opus medium'dur: isi zincire verir, ciktiyi `git diff` + testlerle dogrular, merge eder, raporlar.

## 5. Yukselme kurali

1. Is tipi tablodaki baslangictan kosar.
2. Sonuc yetersizse (test/kontrol gecmedi, eksik, uydurma) **ayni modelde** effort bir basamak artar, tekrar denenir.
3. Tavana (bolum 3) gelinip yine olmuyorsa bir ust modelin `medium`'una gecilir.
4. Basarisiz denemenin ciktisi silinmez; ust kademeye "su denendi, su yuzden olmadi" diye verilir.
5. Kota biterse (429) o serit bir ust kademeden devam eder; Gemini bittiyse Haiku.

## 6. Baglam bariyeri (Haiku 100K)

- Global ayar (`install.sh` ile kurulur): `~/.claude/settings.json` →
  `"modelSettings": { "claude-haiku-5-5": { "autoCompactWindow": 100000 } }`.
  Claude Code'un izin verdigi en dusuk deger 100000 (90000 kabul edilmez).
- Haiku alt-ajan frontmatter'i:
  ```yaml
  model: haiku
  effort: medium        # tablodan
  autoCompactWindow: 100000
  ```
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` kullanilmaz: global, Opus/Sonnet oturumlarini da erken compact eder.
- Brief'e dosya yolu ver, dosya yapistirma. Sonucu dosyaya yazdir, ozet don. Buyuk dosyanin sadece ilgili bolumunu oku.
- Ekran goruntusu agir: tarayici isinde once metin/JS ile oku, olmazsa tek ve kirpilmis ekran goruntusu al.
- Isin 100K'yi gececegi bastan belli ve ciktisi zor kontrol ediliyorsa dogrudan Sonnet medium.

## 7. Olcum ve kesisme testi

**Kesisme testi:** bir is tipi bir modelde `high`'a cikinca ayni isi bir kez de ust modelin `medium`'unda kos. Karsilastir:
- Kalite: test/diff/kontrol gecti mi, tekrar gerekti mi.
- **Tamamlanan is basina** maliyet: token, sure, tekrar sayisi (ucuz ama tekrar gerektiren deneme ucuz degildir).

Karar:
- Ust model medium daha iyi, ya da yakin maliyetle daha iyi → o is tipinin baslangici ust model medium olur.
- Alt model high yeterli ve belirgin ucuz → alt model high kalir.

Her deneme projenin `docs/model-routing-notes.md` dosyasina bir satir:

```
| tarih | is tipi | model+effort | sonuc (gecti/kaldi) | token/sure | tekrar | karar |
```

Bolum 4'teki baslangiclar bu notlara gore guncellenir. Yeni model cikinca ayni test onunla da kosulur.

## 8. Abonelik notlari

- Max planda alt-ajanlar (Haiku olsa da) ana oturumla ayni 5 saatlik ve haftalik limitten yer; Opus ve Sonnet'in ek aile limitleri var.
- Haiku'nun 100K/5x fiyati resmi olarak API fiyati; plan sayacina nasil yansidigi yazili degil. Yine de 100K alti guvenli taraf.
- En buyuk kota yakici uzun ana oturumdur (her mesajda tum baglam yeniden islenir). Baglam buyuyunce ozetle ya da yeni oturum ac.
- Gemini kotasi 5 saatlik + haftalik pencerelidir; yuksek effort daha cok yer (dogrulanmadi).

## 9. Delegasyon kurallari

- `agy` cagrisi: `AGY_MODEL=gemini-3.8-flash-<low|medium|high> AGY_EFFORT=<ayni> ~/Projects/ClaudeHQ/scripts/hq agy --file <prompt> --dir <proje> --slug <ad>`. Model id'si ile effort eslesmeli.
- Genis paralel is (bagimsiz moduller, asset manifest, icerik verisi, QA taramasi) Gemini teamwork ile (`define_subagent` / `invoke_subagent`).
- Video / hareket referansi: web'de gemini.google.com (`agy`'de video yok).
- **Cikti iddiadir, kanit degil.** Her delege is `git diff` / dosya okuma / sayfayi acma ile dogrulanir. Delege kosular raporunu `docs/runs/<YYYY-MM-DD-HHMM>-<slug>.md`'ye yazar.
- **Paralellik:** arayuz paylasmayan eksende paralellestir (sanat, icerik, QA, arastirma). Olculmus: tek odakli gecis 18 dk, 19 pakete bolunmus 14 ajanli kosu 5 saat. Her seride dosya sahipligi satiri ver:
  > Sadece su dosyalara yaz: `<liste>`. Baska dosya degismesi gerekiyorsa yapma, rapor et.
- Kota korkusu isi ic tarafta tutma gerekcesi degildir; kisitlama sadece gercek rate-limit (429) gelince o seritte devreye girer.
- Antigravity icinde `agy` uygulayicidir: model `--model` / `--effort` ile disaridan verilir, skill kendi icinde model secmez.
