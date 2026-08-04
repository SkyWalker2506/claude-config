# /asset-prompt-gen — Standardize Asset Prompt Generator

Sprite/asset üretim prompt'larını proje config'inden standardize üretir. Idle + 4-direction animation strip'leri yazar. Image gen modellerinde sıkça görülen failure mode'larını (extra-row hallucination, view drift, accent contradiction, BG ambiguity) prompt seviyesinde önler.

---

## Pipeline philosophy — Anchor-first hybrid (v3, 2026-05-02)

1. **South-facing neutral anchor önce.** Silahsız, efektsiz, nötr poz. Tüm yön/animasyonlar bu anchor'dan türesin (image-to-image). East = West flip.
2. **Pixel grid guide image** — siyah-beyaz grid PNG'yi prompt yanına 2. referans olarak ekle → pixel block discipline.
3. **Walk cycle = video-gen** (Veo/Seedance), idle/attack = image-gen. Image-gen walk cycle güvenilmez. Video prompt'u "treadmill, runs in place, locked camera, body axis fixed" içermeli.
4. **Walk cycle 1-cycle picker** — 80-120 frame video'dan tam 1 yürüyüş döngüsü seç (start pose → next same pose), 8-12 frame'e even-distribute. Helper: `iron-tamer/scripts/walk_cycle_pick.sh`.
5. **Normalization 4 step:** chroma BG remove → bound measure → height correction (jump/cast frame küçülme fix) → foot anchor (south gravity, ayak sabit y).

---

## Strateji: 4 bağımsız 1×8 strip (mega-sheet YOK)

Her asset için **4 ayrı 2048×256 strip prompt'u**:
- `walk_up` — back view (rear 3/4), 1×8
- `walk_down` — front view (front 3/4), 1×8
- `walk_right` — side view (side 3/4), 1×8 (sol = runtime flip)
- `idle` — front view stationary, 1×8

**Neden 4×8 mega-sheet değil:** Image gen modelleri `4 rows × 8 cols` istendiğinde sıklıkla 5×8 veya 5×9 üretiyor (extra-row hallucination). Tek satır 1×8'de bu hata imkansız — model 2. satır ekleyemez.

**Neden birleştirme yok:** Oyun kodu 4 dosyayı ayrı yükler ve animation state'ine göre ilgili strip'i oynatır. Birleştirme gereksiz; tek strip kötü gelirse sadece o yön re-roll.

---

## Prompt mimarisi (her strip aynı yapı)

```
PROMPT START
[REFERENCE IMAGE — IDENTITY SOURCE]   idle PNG URL + match-this-image direktifi
[IDENTITY LOCK]                       per-asset description (config'den)
ACCENT VISIBILITY                     view-aware: BACK view'da accent gizli, diğerlerinde reference'la birebir
[CAMERA / DIRECTION LOCK]             MOST IMPORTANT — per-direction VISIBLE/HIDDEN listesi
OUTPUT SPEC                           2048×256 PNG, 1 row × 8 cols
[LAYOUT LOCK]                         canvas, cell size, no extras
[BACKGROUND LOCK]                     magenta #FF00FF primary, transparent secondary
[ART STYLE]                           project master_style (config'den)
[STYLE OVERRIDES]                     master_style'daki "transparent BG" + "3/4 view" sözcüklerini override eder
[RENDERING LOCK]                      cel-shaded illustration, NOT pixel art / 3D / painterly
[SUBJECT IDENTITY]                    full character description
[ANIMATION SEQUENCE — 8 cells]        per-cell explicit description (gait phase per frame)
[BACK-VIEW LEG NAMING] (UP only)      "subject's anatomy, not viewer's left/right"
[FRAME DELTA RULE]                    per-form: quadruped/biped/hover language
[CONSISTENCY RULES]                   same identity across 8 cells
[STRICT NEGATIVES]                    yasaklar listesi
[FINAL REJECTION CHECK]               reject conditions, re-render trigger
PROMPT END
```

---

## Video-gen prompt template (Veo 3 / Seedance — walk cycle)

Walk cycle için image-gen güvenilmez; video-gen kullan. Anchor PNG'yi referans olarak ver, prompt:

```
[REFERENCE IMAGE]              south/SE-facing neutral anchor PNG (transparent or magenta BG)

[CAMERA LOCK — ABSOLUTE]
- Camera is FROZEN. Locked at fixed isometric angle (45° / 135° per segment).
- Camera does NOT pan, dolly, zoom, or rotate at any point.
- No parallax, no shake, no easing.

[BODY AXIS LOCK]
- Subject body axis stays at the segment angle. Subject does NOT yaw/rotate.
- Hard cut between segments — NO continuous rotation between angles.

[MOTION RULE — TREADMILL]
- Subject runs/walks IN PLACE. World is stationary.
- Subject does NOT translate across the frame. Feet alternate but the pelvis x,y stays centered.
- Subject does NOT exit the frame at any point.
- For jump: vertical hop only, lands on same x. For attack: stationary, no lunge displacement.

[POSE NEUTRAL LOCK]
- Hands EMPTY. No weapon, no spell, no held object unless asked.
- No accent halo, no eye glow, no emissive bloom.

[BACKGROUND LOCK]
- Solid magenta #FF00FF flat fill, OR transparent. Nothing else — no floor, no shadow disk, no environment.

[SEGMENT PLAN — 8s @ 24fps]
- 0–4s @ 45° NE: 1s walk, 1s run, 1s jump, 1s idle
- 4–8s @ 135° SE: 1s walk, 1s run, 1s jump, 1s idle
- Each segment is exactly 1.0 second. HARD CUT at every second.

[ACTION DEFINITIONS — fit one full cycle in 1 second]
- WALK (1s): minimum 2 full gait cycles in 1s — left fore + right hind plant → swap → repeat. Speed up cadence to fit. No translation.
- RUN (1s): minimum 3 full gallop cycles in 1s — both forelegs reach → suspension airborne phase → both hindlegs plant → push off. Faster, lower body, longer stride than walk. No translation.
- JUMP (1s): single jump arc — crouch (4 frames) → push-off airborne (8 frames apex) → land (8 frames) → recover (4 frames). One jump, complete and clean. Lands at same x.
- IDLE (1s): subtle micro-motion — head bob (small nod or look-around), tail/antenna sway, breath rise/fall on chest. NO body translation, NO leg lift. Two soft loops in 1s.

[SPEED RULE]
- Action cadence may be FASTER than realistic; downstream pipeline re-times by stretching across more frames at playback. Prioritize completed cycles over realistic speed.

[NEGATIVES]
- NO camera rotation, NO continuous yaw, NO translation across frame, NO weapon, NO halo,
  NO environment, NO shadow ground, NO motion blur smear, NO watermark.
```

Çıktıyı `walk_cycle_pick.sh` ile parçala — start/end saniye ver, foot-anchor'lı strip çıkar.

---

## Lessons Learned (kanlı bedeller)

Bu skill'in iterasyonlarında öğrenilen kritik prompt mühendisliği dersleri. Yeni proje veya yeni strip türü eklerken bu öğrenimleri koru:

### 1. View-aware accent visibility (back-view çelişkisi)
**Sorun:** "Accent shape every cell'de aynı olmalı" + "back view'da yüz görünmesin" → model çelişkide kalıp ya yüzü çiziyor ya da accent shape'i bozuyor.
**Çözüm:** Per-direction `accent_rule` — UP'ta "accent HIDDEN, do NOT draw front-facing optic", diğerlerinde "accent IS visible, match reference shape".

### 2. Magenta primary, transparent secondary
**Sorun:** "Transparent OR magenta" → model kararsız kalıp gradient/spotlight üretiyor.
**Çözüm:** `[BACKGROUND LOCK]` → "PRIMARY: solid #FF00FF flat fill. SECONDARY (only if alpha guaranteed): transparent." Default explicit magenta.

### 3. master_style "transparent background" çelişkisi
**Sorun:** Master style metni "Transparent background" diyor, BG_RULE magenta diyor → çelişki.
**Çözüm:** `[STYLE OVERRIDES]` bloğu — "ignore any 'transparent background' in art style above; BACKGROUND LOCK is the only source of truth."

### 4. Camera angle çelişkisi
**Sorun:** RENDERING_LOCK içinde "ABOVE and slightly in front 45°" gibi sabit kamera tarifi olduğunda back/side view talepleriyle çelişiyor.
**Çözüm:** RENDERING_LOCK'tan kamera açısı kaldırıldı, `[STYLE OVERRIDES]` ile master_style'daki "3/4 view" sözcüğü override edildi. Tek doğruluk kaynağı: `[CAMERA/DIRECTION LOCK]`.

### 5. Per-form gait language
**Sorun:** Generic "quadruped/biped/hover gait silhouettes" — model hangi formu rendering ettiğine emin değil.
**Çözüm:** `frames_quadruped/biped/hover` ayrı fonksiyonlar + FRAME DELTA RULE'da per-form `gait_word` ("quadruped walking" / "bipedal walking" / "hovering glide-motion").

### 6. Back-view leg naming clarification
**Sorun:** UP/back-view'da "right-front leg" → model viewer perspektifine göre sol/sağ olarak yorumluyor; "bacakları daha iyi göstereyim" deyip ön açıya dönüyor.
**Çözüm:** UP-only `[BACK-VIEW LEG NAMING CLARIFICATION]` — "leg labels describe subject's OWN anatomy, NOT viewer's left/right. Do NOT rotate the character toward camera."

### 7. "Ground/floor" language → "stride phase"
**Sorun:** "paws planted on ground" / "lift off ground" → model contact shadow veya floor mark çiziyor.
**Çözüm:** "in planted stride phase" / "in lifted stride phase" — gait cycle terminolojisi, zemin imajı yok. STRICT NEGATIVES içindeki "NO ground/floor" yasakları kalsın.

### 8. "peak airborne" → "highest lifted stride phase"
**Sorun:** "peak airborne" → model fazla zıplama yorumu yapıyor.
**Çözüm:** Anatomik gait language: "highest lifted stride phase".

### 9. Layout 1×8 strict (mega-sheet 4×8 değil)
**Sorun:** 4×8 talebinde model 5×8 / 5×9 üretiyor.
**Çözüm:** 4 ayrı 1×8 strip — model 2. satır ekleyemez.

### 10. FINAL REJECTION CHECK
**Sorun:** Failure modlarını yakalamak için tek bir kapı yok.
**Çözüm:** Prompt sonunda explicit "Reject and re-render if ANY of these occur: ..." listesi.

---

## Kullanım

```bash
/asset-prompt-gen <project_root>
```

Proje şu yapıda olmalı:
```
<project_root>/
└── art/prompts/
    └── _config.json   ← input (zorunlu)
```

### Config schema

```json
{
  "project": "<project-id>",
  "asset_browser_url": "https://<asset-browser-host>",
  "master_style": "<one-line style guide for the project>",
  "categories": {
    "<category_name>": {
      "tag": "<asset-browser-tag>",
      "items": [
        {
          "id": "<unique_id>",
          "name": "<Display Name>",
          "form": "quadruped | biped | hover-orb | hover-x",
          "identity": "<full subject description in English>"
        }
      ]
    }
  }
}
```

### Config yazarken dikkat

- **`master_style`:** "Transparent background" YAZMA — bunun yerine "Background is controlled only by BACKGROUND LOCK below." de.
- **`master_style`:** "3/4 view" / "isometric angle" gibi camera ifadeleri YAZMA — `[CAMERA/DIRECTION LOCK]` zaten per-direction halleder.
- **`identity`:** İngilizce, full description (color/material/silhouette/parts/wear detayları). Model bunu reference image ile birlikte truth source kabul eder.
- **`form`:** `quadruped` (4 bacak), `biped` (2 bacak), `hover-orb` (yuvarlak hover), `hover-x` (X-shape hover). Form'a göre frame breakdown otomatik seçilir.

### Content-policy safe terminology (TRIGGER WORDS)

Image gen modelleri (özellikle DALL-E / Imagen / Sora) bazı kelimeleri içerik politikası ihlali olarak filtreler. Aşağıdaki güvenli alternatifleri kullan:

| ❌ Tetikleyici | ✅ Güvenli alternatif |
|---|---|
| battle damage / battle-worn | surface wear / weathered |
| weapon pod / weapon mount | utility pod / utility mount |
| scratch marks / scratched | scuff marks / scuffed |
| guard dog | watchdog |
| post-apocalyptic | industrial wasteland |
| scorched / scorch mark | darkened / soot stain |
| wreck / destroyed | derelict / dismantled |
| blood / gore / corpse | (avoid entirely) |
| muzzle flash | ignition flare |
| violent / killing | aggressive / disabling |

**Genel kural:** Identity yazarken görsel tarif odaklı kal — hasar/aşınma için fiziksel/mekanik dilde ifade et ("oxidation", "wear marks", "dents", "patches", "rivets"), savaş/şiddet metaforlarından uzak dur. Model "rust" / "oil stain" / "dent" / "weathered" / "patched" gibi kelimelere takılmıyor.

### Output

`<project_root>/art/prompts/`
- `{category}_idle.md` — idle hero prompt'ları (256×256)
- `{category}_animations.md` — 4 strip prompt per item (2048×256 her biri)

Her prompt 100% standalone (boş chat'e copy-paste hazır). Reference URL `{asset_browser_url}/assets/{tag}/{id}_idle.webp` pattern'inden auto-generate edilir.

---

## Roadmap — yeni strip türleri ekleme

Mevcut: `walk_up`, `walk_down`, `walk_right`, `idle`.

İleride eklenecekler aynı pattern'i izler — yeni `frames_*(direction)` + `view_label(direction)` entry'si:

| Strip | View kilidi | Frames özet |
|-------|-------------|-------------|
| `walk_left` | flip of `walk_right` (skip — runtime flip) | — |
| `attack` | per-asset (bite/melee/ranged); view = front | wind-up → strike → recover |
| `damage` / `hit_react` | front view | recoil → flinch → recover |
| `death` / `destroy` | front view | shake → collapse → wreck (son frame = static loot sprite) |
| `special` | per-asset | ability animation |

**Eklemek için:** `generate.py`'de yeni direction key + frames function + view_label entry. Aynı strict locks otomatik uygulanır.

---

## Çalıştır

```bash
PROJECT_ROOT="${1:-}"
if [ -z "$PROJECT_ROOT" ]; then
  echo "Usage: /asset-prompt-gen <project_root>"
  echo ""
  echo "project_root must contain: art/prompts/_config.json"
  exit 1
fi

CONFIG="$PROJECT_ROOT/art/prompts/_config.json"
[ ! -f "$CONFIG" ] && { echo "ERROR: config not found: $CONFIG"; exit 1; }

python3 ~/.claude/skills/asset-prompt-gen/generate.py "$PROJECT_ROOT"
```
