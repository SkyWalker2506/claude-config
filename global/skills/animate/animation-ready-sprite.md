# Animasyona Girecek Sprite'in Formu — I2V Standardi

Tek kaynak. `/animate`, `/image-prompt` ve `/asset-prompt-gen` bu belgeye bakar.
Kural sunlarin toplamidir: bu hattaki **olculmus** hatalar + disaridan dogrulanmis
I2V pratigi. Iddialarin yaninda hangisi oldugu yaziyor.

**Neden bu belge var:** model verilen kareyi canlandirir, **icerigini degistiremez**.
Yon, poz, kadraj ve zemin animasyonun kalitesini belirler — prompt degil. Prompt'u ne
kadar duzeltirsen duzelt, yanlis formda uretilmis bir sprite'tan duzgun yuruyus cikmaz.
Bu yuzden sprite'i **animasyonu dusunerek uretmek** zorundasin; sonradan duzeltilmiyor.

---

## 1. Yon — TEK form: ekrana gore SAGA bakar

| | |
|---|---|
| Kanonik yon | **screen-right** (figur sag tarafa bakar/yurur) |
| Govde acisi | **yan 3/4 — govde ekseni yana, ~20-30 derece kameraya donuk** |
| Sol taraf | uretilmez; **runtime flip** |
| Oyuncu / dusman | ikisi de saga bakan tek asset; dusman sahnede flip ile sola cevrilir |

Neden tam onden degil: side-scroller'da yuruyus ve saldiri **yatay eksende** okunur.
Onden bakan figure yuruyus verilemez — karakteri dondurmek yeni icerik uretmektir,
model bunu yapamaz (bu hattaki kural: animate SKILL "Yuva siluete uymali").

Neden tam profil (90 derece) de degil: kimlik kayboluyor — yuz, zirh plakasi, aksesuar
tek duzleme siziyor; ayrica ince uzuvlar matte'ta kopuyor. 20-30 derece kameraya donuk
yan hem yuruyus eksenini hem kimligi tasir. Disarida da ayni tavsiye: I2V icin "clean
side-view image in a clear action-ready pose" + "medium focal length, center composition".

### Flip guvenligi — sprite'i flip'e dayanikli tasarla

Flip serbest ama **asimetri taraf degistirir**. Uretirken:

- Kilic/kalkan eli **kanonik** yazilir ve flip'te taraf degistirmesi kabul edilir; bu
  aksiyon oyunlarinda standart, kimse fark etmez.
- **Yasak:** harf, rakam, wordmark, okunakli amblem, tek gozu kapatan bant gibi
  "yanlis tarafta" oldugu hemen anlasilan isaretler. Flip'te ters okunur/yanlis durur.
- Kalp/yara/mühür gibi hikayeye bagli tek-tarafli detay varsa GDD'ye **hangi tarafta**
  oldugu yazilir; flip edilen kopya lore'a aykiri sayilmaz, runtime karari olarak gecer.

---

## 2. Poz — notr dovus durusu

- Agirlik iki ayakta, **ayaklar ayrik** (omuz genisligi), dizler hafif kirik.
- Kollar govdeden **ayrik**; eller gevsek.
- T-pose / A-pose **degil**: model bu pozdan baslayinca hareket mekanik ve "rig gibi"
  cikiyor; disarida da rigging disi I2V icin onerilmiyor.
- Donmus dramatik aksiyon pozu da **degil**: kilic havada donmus bir figure idle
  vermek istersen model pozu geri alamaz. Disarida ayni gozlem: "dramatic action poses
  ... motion reads twisted".
- Notr durus, hem idle hem yuruyus hem saldiri icin ortak baslangictir; bir karakterin
  butun klipleri **ayni kaynaktan** uretilir (yoksa birinde kapsonlu birinde kel cikar).

## 3. Silüet — uzuvlar govdeye yapismaz

Matte (BiRefNet) neyi ayirabiliyorsa animasyon onu ayri hareket ettirebilir.

- Kol ile govde arasinda, iki bacak arasinda **negatif bosluk** birak.
- Pelerin/sac/kuyruk govdeye yapisik cizilmez; kenari okunur kalsin.
- Ince uzanti (mizrak sapi, anten, zincir) govdeyi kesmesin — ince kanal olcumu
  (`thinPiercePct`) esigi > 6.5'te uyari veriyor, kaynaktaki yapisiklik en sik sebep.

## 4. Bacaklar gorunur — yuruyecekse zorunlu

Yere kadar cuppeli figure yuruyus verilemez. **Olculdu:** yatay yer degistirme 5 px,
gercek adimda 17 px. Prompt'la duzelmiyor, sorun yapisal.

Yurumesi gereken her karakterde **ayak bilegi ve alt bacak gorunur** cizilir. Hayalet /
suzulen tasarimlarda yuruyus yerine `hover`/`drift` klibi planlanir; o zaman etek serbest.

## 5. Elin icindekisi klip setini belirler

Karede duran nesneyi model **silemez**. Kilic elde uretilmis karaktere "silahsiz
saldiri" verilemez.

Ayni karakterin hem silahli hem silahsiz klibi gerekiyorsa **iki master** uretilir
(`A##` ve `A##.unarmed`), ikisi de ayni kimlik kilidiyle.

## 6. Kadraj, taban ve olcek

| | |
|---|---|
| Kadraj | tam boy; bas ustu ve ayak alti **kesilmez** |
| Pay | her kenarda ~%6 |
| Yatay | figur ortalanmis |
| Dikey | **ayak tabani sabit taban cizgisinde** (foot anchor — kareler arasi zipla-kayma bunu bozar) |
| Olcek sinifi | normal insansi ~%85 tuval yuksekligi · buyuk boss ~%92-95 · kucuk yaratik ~%55-65 |

Olcek sinifi sabit tutulmazsa oyunda ayni odadaki iki dusman farkli "kamera
mesafesinde" duruyormus gibi gorunur. Disarida da ayni: "normalize all frames to the
same foot baseline and character scale".

## 7. Zemin, isik, efekt

- Zemin **duz saf siyah** (#000000). Gradient, vinyet, stüdyo fonu, zemin plakasi,
  **temas golgesi** yok.
- Saydam PNG **oldugu gibi verilmez** — model boslugu karakterin renkleriyle doldurur.
  **Olculdu:** ham RGBA oldugu gibi yuklendiginde **39 klip kullanilmaz cikti** (model
  turuncu/yesil/mavi stüdyo fonu uydurdu, figur kadraj disina tasti).
- Isik: duz, onden ana isik. Sert rim/arka isik yok — govde donunce isik kayiyor ve
  kimlik oynuyor. Disarida da: "keep light source consistent across the I2V sequence".
- Motion blur, partikul, duman, ates, aura, emissive tasma **sprite'a gomulmez**.
  Emissive ayri maske olarak uretilir (GDD helper-asset mantigi).

## 8. Tek figur

Bir asset ID = bir bagimsiz tam govde/tam yaratik PNG. Kolaj, contact sheet, izgara,
bust, uzuv parcasi **animasyon kaynagi olamaz**. (GDD v7.4 §79 duplicate guard ile ayni
kural; A51 ve A55 tam olarak bu yuzden reddedildi.)

---

## 9. Master ile animation anchor ayri seylerdir

GDD §42 bunu zaten yaziyor: *"Animation source hazirligi master PNG'yi degistirmez;
generation input ayri turetilir."*

| katman | ne | yon |
|---|---|---|
| `A##` master | kimlik kanonu, key-art, GDD sayfasi | onden 3/4 olabilir |
| `A##.anim.side` | I2V'ye giren anchor | **saga bakan yan 3/4, bu belgedeki form** |

Var olan onden bakan masterlar **cope gitmez**: anchor onlardan image-to-image ile,
kimlik kilidi master'dan okunarak turetilir. Yeni uretimlerde ikisi ayni turda cikar.

## 10. I2V input hazirligi — mekanik adimlar

```
1. alfa kutusuna kirp
2. kare tuvale otur, kenarda ~%6 pay
3. alfayi DUZ SIYAH zemine duzle
4. 512x512'ye LANCZOS ile indir
```

## 11. Uretim kabul kapisi

Bir sprite animasyona **uygun** sayilmadan once hepsi tutmali:

- [ ] saga bakiyor, govde yan 3/4 (~20-30 derece)
- [ ] notr durus; T/A-pose degil, donmus aksiyon degil
- [ ] ayak bilegi + alt bacak gorunur (yuruyecekse)
- [ ] kol-govde ve bacak-bacak arasinda bosluk var
- [ ] tam boy, ~%6 pay, ayak tabani taban cizgisinde
- [ ] duz siyah zemin; golge/gradient/zemin plakasi yok
- [ ] duz onden isik; sert rim/arka isik yok
- [ ] tek figur; kolaj/bust/parca degil
- [ ] metin/harf/rakam/wordmark yok (flip'te ters okunur)
- [ ] emissive/VFX gomulu degil
- [ ] elindeki nesne planlanan klip setiyle uyumlu

Tutmayan sprite **yeniden uretilir**; animasyon turuna sokulmaz. Bir klibin
kullanilamaz cikmasinin bedeli, sprite'i bastan uretmenin bedelinden buyuk.

---

## Kaynaklar

Disaridan dogrulama (2026-08 taramasi):
[Sorceress — AI animation from image](https://sorceress.games/blog/ai-animation-generator-from-image-game-ready-in-minutes) ·
[Sorceress — sprite generator, walk cycles](https://sorceress.games/blog/ai-sprite-generator-pixel-walk-cycles-idles-and-vfx) ·
[chongdashu/ai-game-spritesheets](https://github.com/chongdashu/ai-game-spritesheets) ·
[ComfyUI Wan 2.2 I2V workflow](https://comfy.org/workflows/video_wan2_2_14B_i2v-8c7511104c80/) ·
[styly-agents/Wan2-2-pixel-animate](https://huggingface.co/styly-agents/Wan2-2-pixel-animate) ·
[Scenario — AI sprite generator](https://www.scenario.com/blog/ai-sprite-generator)

Olculmus veriler bu hattin kendi kayitlarindan: `animate` SKILL.md (39 kullanilmaz klip,
5 px vs 17 px yer degistirme, ince kanal/dikis esikleri).
