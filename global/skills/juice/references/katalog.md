# Juice katalogu — calisan koddan cikarilmis tarifler

Kaynak: `~/Projects/necrobeat` (dal `main`). Asagidaki her sayi o oyunda
olculdu. Yeni bir projeye tasirken **dosyayi kopyala**, tarifi yeniden yazma.

## Dosya haritasi

| Dosya | Icinde ne var |
|---|---|
| `src/world/Billboards.js` | sprite shader hooku (GLSL) + WebGPU node malzemesi (TSL) + tum setter'lar |
| `src/world/fx/fxconfig.js` | efekt katmaninin TUM ayarlanabilir sayilari |
| `src/world/fx/FlatFX.js` | tek InstancedMesh: halka, patlama, sutun, muhur, koni |
| `src/world/fx/Aura.js` | tier'e gore davranis degistiren aura, cift yol |
| `src/world/fx/LightPool.js` | mangal zemin isigi: nefes + catirti + kenar oynamasi |
| `src/world/fx/ArcFX.js` | yay/simsek/zincir |
| `src/world/fx/DamageNumbers.js` | hasar sayilari |
| `src/world/fx/Dissolve.js` | olum cozulmesi surucusu |
| `src/world/fx/SealMaterial.js` | zemin muhurleri |
| `src/world/fx/ParticleBatches.js` | partikul gruplari |
| `src/systems/Effects.js` | ust seviye API: `burst/impact/ring/column/skyBolt/darken/screenFlash/addShake/dissolve/damageNumber` |
| `src/world/Rig.js` | katmanli cutout rig (bkz. `/animate`) |
| `src/entities/Enemies.js` | `GAIT` tablosu, dusman basina squash surumu |
| `src/entities/Player.js` | `punch` surucusu |
| `tools/rigchk.mjs` | animasyon kapisi ornegi |

---

## Katman 1 — transform (shader yok, maliyet ~0)

### squash + gait

```js
// squash = vurus tepkisi (anlik)
// extra  = duzgun buyume/nefes (en ve boy BIRLIKTE)
// gait   = yuruyus: boy ile en TERS oynar
sprite.scale.set(
  baseW * (1 + squash * 0.35) * extra * (1 - gait * 0.55),
  baseH * (1 - squash * 0.28) * extra * (1 + gait),
  1,
);
```

`+gait` uzayip incelir (adim kalkisi), `−gait` basiklasip genisler (ayak yere basar).
**Agirlik hissini tasiyan sey bu ters oran.** Ayni oranda olceklersen sadece
"buyuyup kuculen resim" olur.

Katmanli rig'de tek sprite yok: **butun grup** olceklenir, katmanlarin kendi
olcegi animasyondan gelir, ustune grup olcegi biner.

### GAIT tablosu (tip basina)

```js
const GAIT = {
  bone:     { amp: 0.055, freq: 5.0 },    // canli, keskin adim
  golem:    { amp: 0.080, freq: 2.4 },    // agir ve yavas
  bellhead: { amp: 0.075, freq: 2.1 },    // en agir
  elite:    { amp: 0.050, freq: 3.2 },
  larva:    { amp: 0.095, freq: 12.0 },   // surunme: hizli ve abartili
};
const gait = Math.sin((time + i * 0.61) * G.freq) * G.amp;   // i = birim indeksi
```

`i * 0.61` sart: yoksa ayni tipteki 40 dusman **ayni anda ayni adimi** atar ve
tek bir organizma gibi okunur.

Yalniz gercekten hareket ediyorsa uygula: `(V.x² + V.z²) > 1e-7`.

### punch (vurus tepkisi)

```js
beat() { this.punch = 1; }
update(dt) {
  this.punch = Math.max(0, this.punch - dt * 6.5);        // ~150 ms
  BB.setSquash(actor, this.punch * 0.5, 1 + this.punch * 0.08);
  BB.setFlash(actor, this.punch * 0.18);
  group.scale.set(1 + punch * 0.1, 1 + punch * 0.22, 1 + punch * 0.1);
}
```

### kamera sarsintisi

```js
addShake(a) { this.shake = Math.min(1, this.shake + a * shakeMul * fxShake); }
// sonme: siddet arttikca daha hizli soner
this.shake = Math.max(0, this.shake - shakeDecay * dt * (0.4 + this.shake));
shakeOffset(t) {
  const s = this.shake * this.shake * 0.9;      // KARESI — kucuk sarsintilar sakin kalir
  return { x: Math.sin(t * 51.3) * s, y: Math.cos(t * 43.7) * s };
}
```

Uygulama yeri kritik: **kamerayi kendi ekseninde kaydir**, bakis hedefini degil.

```js
camera.position.copy(camPos)
  .addScaledVector(camRight, sh.x)
  .addScaledVector(camUp, sh.y);
camera.quaternion.copy(camQuat);      // yon SABIT
```

Bakis hedefini sarsarsan izometrik sahne egilir ve mide bulandirir.

### hitstop

```js
if (this.hitstop > 0 || this.hitstopCooldown > 0) return;      // zincirlenmesin
this.hitstopQueued = Math.min(MAX, Math.max(this.hitstopQueued, s * fxHitstop));
// bitince:
this.hitstopCooldown = 0.075;
```

### beat zoom

`camera.zoom = 1 + camZoom`, `camZoom` her vurusta set edilip `rawDt * 0.45` ile
soner. `updateProjectionMatrix()` cagrilmali.

---

## Katman 2 — sprite shader (tek program)

### Neden tek program

three, program onbellegini `onBeforeCompile`'in **kaynak metniyle** anahtarlar.
Hook fonksiyonu tek ve degismez → tum sprite'lar tek program paylasir. O yuzden
dallar uniform uzerinden yazilir: bir cizim cagrisinda kosul sabittir (uniform
control flow), `fwidth`/`texture` guvenlidir, alinmayan dal ~0 maliyet.

### Uniform seti

| uniform | is |
|---|---|
| `uFlip` | yon cevirme (dokuda, cunku `THREE.Sprite` negatif olcegi yok sayar) |
| `uWobT/A/F/M` | dalgalanma: zaman, genlik, frekans, mod (0 hayalet · 1 etek · 2 nefes · 3 dikey) |
| `uHit`, `uHitDir` | vurus: kenar parlamasi + darbe yonunde UV itmesi |
| `uHitFlash` | tum govde flash'i |
| `uRim` | kalici siluet konturu |
| `uSoft` | hayalet tiplerinde yumusak alfa rampasi |
| `uFlame` , `uFlameT` | alev |
| `uDissolve`, `uFxColor` | olum cozulmesi |

### Cevirme

```glsl
if ( uFlip > 0.5 ) wuv.x = 1.0 - wuv.x;
```
Vurus itmesinde isareti telafi et: `float fs = uFlip > 0.5 ? -1.0 : 1.0;`

### Dalgalanma — hayalet modu

Tek sinus "titreyen bayrak" gibi duruyordu. Akiskan hale getiren uc sey:

```glsl
float lo = 1.0 - wuv.y;                       // etek cok, bas az oynar
wuv.x += sin( wuv.y *  7.0 + wt ) * A * lo;
wuv.x += sin( wuv.y * 13.0 - wt * 1.7 ) * A * lo * lo * 0.55;   // ikinci harmonik
wuv.x += sin( wt * 0.45 ) * A * 0.35;                            // tum siluet suruklenir
wuv.y += cos( wuv.x * 5.0 + wt * 0.7 ) * A * 0.40;
```

**Bu yalnizca siluetin ince/uc bolgelerinde ise yarar.** Dolu govdede gorunmez.

### Vurus kenari — ek doku okumasi YOK

```glsl
float aw  = fwidth( sampled.a );                                  // ekran uzayinda alfa degisimi
float rim = clamp( aw * 2.2, 0.0, 1.0 ) * step( 0.25, sampled.a );
diffuseColor.rgb += mix( uFxColor, vec3(1.0), 0.6 ) * rim * uHit * 1.1;
```

Ayni teknigin **zayif ve surekli** hali kalici siluet konturu (`uRim`, siddet 0.85,
~6 ALU): kalabalikta ust uste binen dusmanlar tek koyu kutle olarak okunuyordu.

```glsl
float rim = clamp( fwidth(a) * 2.6, 0.0, 1.0 ) * step( 0.22, a );
rgb = mix( rgb, rgb * 0.28 + vec3(0.04,0.06,0.11), rim * uRim );
```

### Hasar flash'i

```glsl
vec3 hitPink = vec3( 1.14, 0.72, 0.84 );        // beyaz cekirdek + pembe kenar
rgb = mix( rgb, hitPink, clamp(uHitFlash,0.0,1.0) * 0.90 );
```
Doku detayini tamamen silmez — "hangi dusman vuruldu" bilgisi kalir.
WebGPU'da `material.color` KULLANMA (bir kare gec ya da hic gelir).

### Yumusak kenar

```glsl
a *= mix( 1.0, smoothstep( 0.03, 0.26, a ), uSoft );
```
Malzemede `alphaTest` 0.12 → 0.03'e iner. **0'a indirme** — 0 yeni bir program acar.

### Alev — maske dokudan gelir, ek okuma dal ICINDE

```glsl
if ( uFlame > 0.0 ) {
  float lum  = dot( c.rgb, vec3(0.333) );
  float warm = clamp( (c.r - c.b) * 2.2, 0.0, 1.0 );      // alev sicak, metal ayak soguk
  float hotK = smoothstep(0.26,0.66,lum) * warm * c.a;
  float ust  = clamp( (wuv.y - 0.42) * 2.4, 0.0, 1.0 );   // dibi sabit, ucu savrulur
  // ... fuv'yi gurultu + sinus ile kaydir, ikinci kez ornekle, hotK ile karistir
  float nefes = fxNoise( vec2(uFlameT * 0.55, 0.31) );    // iki FARKLI hiz:
  float catir = fxNoise( vec2(uFlameT * 3.30, 0.73) );    // biri nefes, biri catirti
  float fl = 0.78 + nefes * 0.26 + catir * 0.18;
}
```

Onceki hali `material.color.setScalar()` ile TUM sprite'i kisip aciyordu: metal
ayaklar da yanip soner, **hicbir sey kimildamazdi**. Tek sinus kullanirsan goz
periyodu yakalar ve metronom gibi okunur.

### Olum cozulmesi

```glsl
float n = fxNoise( wuv * 14.0 ) * 0.70 + wuv.y * 0.30;   // x14 = kucuk pullar
float e = n - uDissolve * 1.06;
if ( e < 0.0 ) discard;
float edge = 1.0 - smoothstep( 0.0, 0.09, e );            // DAR serit
```

Gurultu iri olursa buyuk lekeler halinde gider; parlayan serit genis olursa tum
sprite beyaza doner ve "hangi dusman oldu" bilgisi kaybolur.
Sureler: normal 0.42 s · elit 0.6 · boss 1.0. Cozulurken 0.55 birim/sn yukselir,
0.12 daralir.

### WebGPU (TSL) karsiligi

Ayni matematik `SpriteNodeMaterial` uzerinde node zinciri olarak yazilir:

```js
material.colorNode = vec4(flashed, sampled.a);
material.maskNode  = sampled.a.greaterThan(0.025)
  .and(field.add(0.001).greaterThanEqual(dissolve.mul(1.06)));   // discard karsiligi
material.userData.webgpuFx = { dissolve, fxColor, hitFlash, flip, flame, flameT };
```

Setter'lar iki yolu da gunceller. **Masaustu profili WebGPU** — TSL yolunu
yazmazsan efekt oyuncunun oynadigi surumde yoktur.

---

## Katman 3 — efekt katmani

### FlatFX: bes stil, tek draw call

`S_WAVE` (zemine yayilan sok dalgasi) · `S_BURST` (kameraya donuk radyal patlama) ·
`S_COLUMN` (yukselen sutun) · `S_SIGIL` (cift halka + tirtik) · `S_CONE` (boss
telegrafi: merkezden uca DOLAN koni).

Kurallar:
- Kare basina yeni nesne yok — gecici vektor/quaternion bir kez ayrilir.
- Suresi dolan instance **sondan takasla** cikarilir (compaction).
- Instance verisi dogum/olumde yazilir; her kare yalnizca `uTime`.
- Yeni stil eklersen `STIL_SAYISI`'ni artir (compat yolu o kadar mesh kurar).

Halka neden shader: kalinlik, kenar yumusakligi ve on kenarin keskinligi zamanla
degisiyor. Geometriyi olceklersen **kalinlik da olceklenir** ve halka bulanik bir
diske doner. Fragment'te yapinca halka buyudukce INCELIYOR — goz "yayiliyor" diye
okuyor. Kalinlik DUNYA biriminde verilir (0.55), yariçaptan bagimsiz.

### Aura — tier renk degil DAVRANIS degistirir

```
0 RUHANI       soguk mavi-beyaz, yavas donen ince halka   (oyuncu)
1 KOR          turuncu, yukari yalayan diller             (ilk bosslar)
2 LANET        mor-yesil, tirtikli, kesik kesik atan      (orta bosslar)
3 RUHANI ATES  camgobegi-menekse, hizli girdap + cekirdek (gec bosslar)
```

Hepsi **tek shader'in dallari**, stil bir uniform. Tier basina ayri malzeme = tier
basina ayri program; dort boss ayni anda sahnedeyse dort ekstra derleme.
Her auraya kendi fazi verilir, yoksa hepsi ayni anda ayni yerde olur.

Kapisi: hareket eden piksel orani tier'e gore ayrismali (olculdu: sicak %72 /
zemin %48 / yapi %1).

### Yay / simsek

```js
const amp = Math.min(1.7, Math.max(0.16, len * 0.105)) * Math.sin(Math.PI * t);
```

Tavan **uzunlukla olcekli** olmali. Sabit 0.82 tavani 13 birimlik gok simsegini
duz cizgiye ceviriyordu (`13 * 0.105 = 1.37 > 0.82`).

Gok simsegi: tek catallanmis kanal + beyaz cekirdek; ardil cakmalar **spawn
aninda degil**, birkac kare sonra kuyruktan dusulur — ayni karede uc yay cizmek
tek kalin cizgi gibi okunuyor.

### Hasar sayilari

```js
const punch = Math.min(1, t / 0.16);
const sx = t < 0.16 ? 1.38 - punch * 0.38 : 1 + Math.sin((t-0.16)*10) * 0.06 * (1-t);
const sy = t < 0.16 ? 0.66 + punch * 0.34 : 1 - Math.sin((t-0.16)*10) * 0.04 * (1-t);
```
Once ezilerek girer (genis/basik), sonra sonen bir salinimla oturur.

### Ekran katmani

- `screenFlash(a)` — DOM `#flash` opaklik; tavan 0.32, sonme `dt * 3.4`
- `darken(a, tut)` — `tut` saniye tam degerde kalir sonra soner ("isiklar sondu")
- Ikisi de konfor carpanindan gecer

---

## Konfor / erisilebilirlik

```js
g.fxShake = s.shake ? 1 : 0;
g.fxFlash = s.flash ? 1 : 0;
g.fxHitstop = ...
addShake(a)     { ... a * CFG.vfx.shakeMul * this.g.fxShake ... }
screenFlash(a)  { ... a * CFG.vfx.flashMul * this.g.fxFlash ... }
```

Kapali durumda oyunun hala okunakli olmasi **kapinin parcasi**. Seviye atlama
efekti bilerek sarsintisiz ve flash'sizdir: "kucuk ama net".

---

## Kapi ornegi (animasyon)

`tools/rigchk.mjs` sekli:

1. Oyunu ac, **kart sec** (yoksa simulasyon durur — Demir Kural 7)
2. Dongunun iki ucundan 24 ornek al
3. Her parca icin min/max fark > 0 mi
4. Iki referans parca (or. pelerin/cuppe) 24 ornegin **hicbirinde** ayni acida olmamali
5. Cevirme kac parcayi aynaliyor (tam ortadakiler haric)

Ciktisi sayi olmali. "Hareket ediyor" cumlesi kapi degildir.
