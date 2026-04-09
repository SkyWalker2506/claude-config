#!/usr/bin/env python3
"""Fill Bridge / Output / Cursor blocks for W14 (3d-cad) and W15 (unity backend)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

# E1–E5: yalnizca Bridge + Output
FILL_E: dict[str, tuple[str, str]] = {
    "E1": (
        "E2 model/Blender; E5 optimizasyon butcesi; referans K11/K12.",
        "Konsept dokuman: mood board listesi, kamera/lens plani, polygon/texture butcesi tablosu, risk notu.",
    ),
    "E2": (
        "E1 konsept; E5 mesh cikti; E4 render pipeline.",
        "Blend dosyasi veya script ozeti, export ayarlari, vertex sayisi, bilinen modifier uyari.",
    ),
    "E3": (
        "E2 mesh import; teknik cizim standarti; E5 STL/optimizasyon.",
        "CAD script veya cizim ciktisi, birim/olcek, STL parametreleri, validasyon notu.",
    ),
    "E4": (
        "E2 sahneler; E5 cikti cozunurlugu; farm zamanlamasi.",
        "Render kuyrugu konfigi, frame araligi, cikti formatlari ve yollar, hata log ozeti.",
    ),
    "E5": (
        "E1 butce; E4 hedef cozunurluk; gercek zaman B19 performans.",
        "LOD/draco ayarlari, before/after metrik, dosya boyutlari, platform hedefi.",
    ),
}

# E8–E12 + B24–B52: Bridge + Output + Cursor
FILL_REST: dict[str, tuple[str, str]] = {
    "E8": (
        "B19 gameplay sahne; E11 arazi; E10 isik; tilemap B35 ile.",
        "Sahne hierarsi ozeti, ProBuilder/tilemap notlari, lightmap gereksinimi, test build adimi.",
    ),
    "E9": (
        "B19 oyun kodu; Timeline; E10 isik; E8 layout.",
        "Timeline asset yolu, Cinemachine rig listesi, kesme listesi, Recorder ayarlari.",
    ),
    "E10": (
        "E9 cinematik; E8 sahne; baked perf F12.",
        "Bake ayarlari, probe yerlesim ozeti, reflection/volumetric parametreler, GPU maliyet notu.",
    ),
    "E11": (
        "E8 level; E10 vegetation; streaming B52.",
        "Terrain katmanlari, grass distans ayari, stream tile notu, draw call tahmini.",
    ),
    "E12": (
        "B19 runtime anim; E7/E10 rig ihtiyaci (VFX haric); import ayarlari.",
        "Rig setup, IK hedefleri, blend shape listesi, humanoid retarget notu.",
    ),
    "B24": (
        "B19 gameplay; B49 AI state; animasyon path.",
        "NavMesh ayarlari, agent parametreleri, BT/FSM dosya yollari, pathfinding test sonucu.",
    ),
    "B25": (
        "B19 sahne; cihaz build J11; input B36.",
        "XR rig yapilandirmasi, build hedefi, interaction event listesi, performans notu.",
    ),
    "B26": (
        "B19 AudioSource; FMOD/Wwise entegrasyon; mix J4.",
        "Mixer grup yapisi, spatial ayarlar, bank/event listesi, platform ses limiti.",
    ),
    "B27": (
        "B19 fizik gameplay; F12 profil; layer matrix.",
        "Katman matrisi, joint/raycast ayarlari, fizik material tablosu, deterministik not.",
    ),
    "B28": (
        "B40 cloud; B2 backend; sifreleme ve guvenlik.",
        "Serialize format, migration adimi, bulut endpoint, geri yukleme testi.",
    ),
    "B29": (
        "B28 metin verisi; UI D11; RTL gereksinimi.",
        "String table yolu, locale listesi, font fallback, ceviri anahtari ornekleri.",
    ),
    "B30": (
        "B19 editor is akisi; UPM paket; CI J11.",
        "EditorWindow/Inspector kod yollari, menu item, kullanici rehberi, risk notu.",
    ),
    "B31": (
        "B19 dunya icerik; seed determinizm; E11 arazi.",
        "Algoritma secimi, seed degeri, tile/komsuluk kurallari, performans olcumu.",
    ),
    "B32": (
        "B19 build hedefi; F12 profil; J11 pipeline.",
        "IL2CPP ayarlari, adaptive perf, termal test, bellek budce tablosu.",
    ),
    "B33": (
        "B19 platform derleme; sertifikasyon TRC; input B36.",
        "Platform ifdef listesi, SDK surumu, remap tablosu, uyumluluk notu.",
    ),
    "B34": (
        "B19 gameplay ECS; Burst/Jobs; mono fallback.",
        "Entity tanimlari, system sira, Burst ayarlari, structural change notu.",
    ),
    "B35": (
        "B19 2D oyun; fizik B27; UI D11.",
        "Sprite import, sorting layer, Spine/pixel perfect ayarlari, test sahnesi.",
    ),
    "B36": (
        "B19 player control; UI rebind; B33 platform.",
        "InputAction asset, rebind UI, cihaz test listesi, touch/gesture notu.",
    ),
    "B37": (
        "B19 kamera davranisi; split-screen; cinematik E9.",
        "Cinemachine brain ayarlari, stack/oncelik, custom controller parametreleri.",
    ),
    "B38": (
        "B12/F12 profil; object pool; native leak.",
        "GC alloc raporu, pool boyutlari, NativeContainer kullanimi, profiler capture notu.",
    ),
    "B39": (
        "B19 regresyon; CI J11; kalite C3.",
        "Test assembly listesi, PlayMode senaryolari, coverage veya smoke sonucu.",
    ),
    "B40": (
        "B28 save; remote config; ekonomi B48.",
        "Servis konfig anahtarlari, economy leaderboard entegrasyonu, sandbox test.",
    ),
    "B41": (
        "B48 ekonomi; store B33; backend B2.",
        "IAP urun id'leri, reklam mediation, receipt dogrulama ortami, test hesabi.",
    ),
    "B42": (
        "B2 server dogrulama; B41 odeme; B13 guvenlik.",
        "Client obfuscation adimlari, server endpoint, anti-cheat telemetri, false positive notu.",
    ),
    "B43": (
        "D11 UI; input B36; metin B29.",
        "Erisilebilirlik ayarlari, kontrast tablosu, screen reader test sonucu.",
    ),
    "B44": (
        "B29 metin; narrative tasarim; UI D11.",
        "Diyalog formati, Ink/Yarn asset yolu, dallanma grafigi, lokalizasyon anahtarlari.",
    ),
    "B45": (
        "B44 quest; UI D11; ekonomi B48.",
        "ScriptableObject sema, craft formulu, drag-drop prefab, save B28.",
    ),
    "B46": (
        "B45 esya; animasyon B19; multiplayer B23 (ayri).",
        "Hitbox katmanlari, hasar formulu, combo state makinesi, status efekt tablosu.",
    ),
    "B47": (
        "B44 diyalog; B46 odul; UI D11.",
        "Quest graph ozeti, objective id'leri, odul dagitim kurali, editor araci notu.",
    ),
    "B48": (
        "B41 IAP; B47 odul; denge tasarimi.",
        "Para birimi sema, progression egrisi, gacha olasilik tablosu, simulasyon notu.",
    ),
    "B49": (
        "B46 combat; B47 quest; animasyon.",
        "FSM diyagrami, SO state listesi, hierarchical gecisler, kayit formati.",
    ),
    "B50": (
        "B39 test edilebilirlik; B19 DI kullanimi; Zenject/VContainer.",
        "Lifetime secimi, binding modulu listesi, mock stratejisi, startup sira.",
    ),
    "B51": (
        "J11 CI; Addressables build; E5 optimizasyon.",
        "Addressables gruplari, bundle stratejisi, postprocessor kurallari, import preset.",
    ),
    "B52": (
        "B31 proc; B38 bellek; sahne yukleme.",
        "Streaming adresleri, additive sahne listesi, partition boyutu, async yukleme sirasi.",
    ),
}

CURSOR: dict[str, dict[str, str]] = {
    "E8": {
        "identity": "Terrain, ProBuilder, tilemap ve sahne yonetimi ile Unity level tasarimi.",
        "when_use": "- Graybox ve oynanabilir layout\n- Tilemap 2D/3D ve ProBuilder geometri\n- Sahne organizasyonu ve streaming hazirligi",
        "escalation": "Oyun kodu B19 → arazi E11 → isik E10",
    },
    "E9": {
        "identity": "Timeline, Cinemachine ve Recorder ile cinematik ve kesme uretimi.",
        "when_use": "- Timeline kesme ve shot listesi\n- Cinemachine rig ve takip\n- Recorder cikti ve pipeline",
        "escalation": "Gameplay B19 → isik E10 → ses B26",
    },
    "E10": {
        "identity": "Baked/isik probu, reflection ve volumetric ile Unity sahne aydinlatmasi.",
        "when_use": "- Lightmap bake ve probe yerlesimi\n- Reflection probe ve volumetric ayar\n- Performans/quality dengesi",
        "escalation": "Sahne E8 → cinematik E9 → profil F12",
    },
    "E11": {
        "identity": "Terrain sculpt, vegetation ve ot/grass render optimizasyonu.",
        "when_use": "- Heightmap ve katman dagilimi\n- Agac/cimen sistemleri\n- Terrain streaming ve LOD",
        "escalation": "Level E8 → streaming B52 → performans F12",
    },
    "E12": {
        "identity": "Humanoid rig, IK, blend shape ve skinning is akisi.",
        "when_use": "- Avatar humanoid yapilandirma\n- IK zinciri ve kisitlar\n- Blend shape ve import pipeline",
        "escalation": "Animasyon B19 → mesh E2 → sahne E8",
    },
    "B24": {
        "identity": "NavMesh, pathfinding ve davranis agaci ile Unity AI hareket ve karar sistemi.",
        "when_use": "- NavMesh bake ve agent\n- Behavior tree veya state tabanli AI\n- Crowd ve patrol senaryolari",
        "escalation": "Gameplay B19 → animasyon → ag gerekiyorsa B2",
    },
    "B25": {
        "identity": "AR Foundation ve XR Interaction ile artirilmis ve sanal gerceklik deneyimi.",
        "when_use": "- XR rig ve etkilesim\n- Meta Quest / mobil AR hedefleri\n- Hand tracking ve UI",
        "escalation": "Build J11 → input B36 → performans F12",
    },
    "B26": {
        "identity": "Audio mixer, spatial ses ve muzik adaptasyonu ile Unity ses sistemleri.",
        "when_use": "- Mixer routing ve snapshot\n- FMOD/Wwise veya built-in spatial\n- Adaptive music tetikleri",
        "escalation": "Gameplay B19 → build platform B33",
    },
    "B27": {
        "identity": "PhysX katmanlari, eklemler ve raycast ile Unity fizik ve carpisma.",
        "when_use": "- Collision matrix ve katmanlar\n- Joint ve kinematic senaryolar\n- Performans icin fizik basitlestirme",
        "escalation": "Oyun mantigi B19 → profil F12",
    },
    "B28": {
        "identity": "Kayit formati, sifreleme ve bulut ile Unity save ve serialize.",
        "when_use": "- JSON/binary save\n- Cloud Save ve migration\n- PlayerPrefs alternatifleri",
        "escalation": "Backend B2 → B40 servisleri → guvenlik B13",
    },
    "B29": {
        "identity": "Localization package, string tablolari ve RTL ile coklu dil.",
        "when_use": "- String ve asset localization\n- Font ve RTL destegi\n- CSV/JSON is akisi",
        "escalation": "UI D11 → icerik B44 → build J11",
    },
    "B30": {
        "identity": "Custom Inspector, EditorWindow ve ScriptableWizard ile Unity editor araclari.",
        "when_use": "- Editor-only tooling\n- Property drawer ve inspector genisletme\n- Batch islemler",
        "escalation": "Runtime B19 → paket UPM → CI J11",
    },
    "B31": {
        "identity": "Gurultu, WFC ve dungeon uretimi ile prosedurel icerik.",
        "when_use": "- Seed ve deterministik dunya\n- Tile/komsu kurallari\n- Icerik olcekleme",
        "escalation": "Sahne E8 → performans B32",
    },
    "B32": {
        "identity": "IL2CPP, Adaptive Performance ve termal/bellek ile mobil optimizasyon.",
        "when_use": "- Mobil build profili\n- Termal ve frame pacing\n- Bellek budce",
        "escalation": "Profil F12 → J11 pipeline",
    },
    "B33": {
        "identity": "Platform abstraction, sertifikasyon ve girdi ile konsol/build hedefleri.",
        "when_use": "- Platform ifdef ve SDK\n- TRC/XR uyumluluk\n- Input remap",
        "escalation": "Build J11 → B36 input → destek",
    },
    "B34": {
        "identity": "Entities, Systems, Burst ve Jobs ile DOTS/ECS oyun kodu.",
        "when_use": "- Entity tasarimi ve system sira\n- Burst ve paralellik\n- Structural changes",
        "escalation": "Hybrid B19 → profil F12",
    },
    "B35": {
        "identity": "Sprite, 2D fizik ve Spine/pixel-perfect ile 2D oyun.",
        "when_use": "- Sorting ve 2D fizik\n- Tilemap ve animasyon\n- Pixel Perfect stack",
        "escalation": "UI D11 → B27 fizik",
    },
    "B36": {
        "identity": "Input System action map, rebind UI ve coklu cihaz destegi.",
        "when_use": "- Player ve UI input ayrimi\n- Rebind ve touch\n- Platform mapping",
        "escalation": "B33 platform → erisilebilirlik B43",
    },
    "B37": {
        "identity": "Cinemachine rig, split screen ve kamera stack ile kamera sistemleri.",
        "when_use": "- Follow/aim rigleri\n- Split screen ve stack\n- Custom controller",
        "escalation": "Cinematik E9 → gameplay B19",
    },
    "B38": {
        "identity": "GC, NativeContainer ve object pool ile bellek ve performans yonetimi.",
        "when_use": "- Profiler analizi\n- Pool ve alloc azaltma\n- Native koleksiyonlar",
        "escalation": "F12 profil → B34 ECS → B32 mobil",
    },
    "B39": {
        "identity": "PlayMode/EditMode testleri, otomasyon ve CI ile Unity test.",
        "when_use": "- Regresyon test paketi\n- Performans test framework\n- CI entegrasyonu",
        "escalation": "Kod B19 → CI J11 → C3 review",
    },
    "B40": {
        "identity": "Remote Config, Cloud Save ve Economy ile Unity Gaming Services entegrasyonu.",
        "when_use": "- RC anahtarlari ve varyant\n- Leaderboard ve cloud save\n- Economy paketi",
        "escalation": "Backend B2 → B48 ekonomi",
    },
    "B41": {
        "identity": "IAP, reklam ve receipt dogrulama ile mobil monetizasyon.",
        "when_use": "- Store urunleri\n- Reklam mediation\n- Sunucu receipt",
        "escalation": "Ekonomi B48 → B42 guvenlik → B2",
    },
    "B42": {
        "identity": "Obfuscation, bellek korumasi ve sunucu dogrulama ile anti-cheat.",
        "when_use": "- Client hardening\n- Server authoritative kurallar\n- Sinyal/tabanli tespit",
        "escalation": "B2 backend → B13 guvenlik",
    },
    "B43": {
        "identity": "Screen reader, renk korlugu ve altyazi ile erisilebilirlik.",
        "when_use": "- UI erisilebilirlik ayarlari\n- Kontrast ve input alternatifleri\n- Altyazi senkronu",
        "escalation": "UI D11 → B36 input",
    },
    "B44": {
        "identity": "Diyalog agaci, Ink/Yarn ve lokalizasyon ile hikaye sistemleri.",
        "when_use": "- Branching diyalog\n- Arac entegrasyonu\n- Ceviri anahtarlari",
        "escalation": "B29 locale → UI D11",
    },
    "B45": {
        "identity": "Envanter grid, craft formulu ve drag-drop UI ile esya sistemleri.",
        "when_use": "- ScriptableObject esya DB\n- Craft ve tarifler\n- UI baglama",
        "escalation": "UI D11 → save B28 → ekonomi B48",
    },
    "B46": {
        "identity": "Hitbox, hasar, combo ve status efekt ile savas sistemleri.",
        "when_use": "- Carpisma katmanlari\n- Hasar formulu ve state\n- Combo zinciri",
        "escalation": "Animasyon B19 → B49 state",
    },
    "B47": {
        "identity": "Gorev grafigi, hedefler ve oduller ile quest/mission sistemi.",
        "when_use": "- Quest editor ve runtime\n- Objective takip\n- Odul dagitimi",
        "escalation": "B44 hikaye → B46 combat → UI D11",
    },
    "B48": {
        "identity": "Sanal para, progression ve gacha olasilik ile oyun ekonomisi.",
        "when_use": "- Currency ve sink/source\n- Progression egrisi\n- Gacha dengesi",
        "escalation": "B41 monetizasyon → tasarim urun",
    },
    "B49": {
        "identity": "FSM, hierarchical state ve ScriptableObject durumlari ile oyun durumu.",
        "when_use": "- Menu/oyun durumu\n- Hierarchical ve SO tabanli state\n- Gecis kurallari",
        "escalation": "B46 combat → B47 quest",
    },
    "B50": {
        "identity": "Zenject/VContainer ile bagimlilik enjeksiyonu ve test edilebilirlik.",
        "when_use": "- Installer modulleri\n- Lifetime ve interface baglama\n- Mock/test",
        "escalation": "B39 test → B19 kod",
    },
    "B51": {
        "identity": "Addressables, bundle ve import pipeline ile asset is akisi.",
        "when_use": "- Addressables gruplari\n- Bundle stratejisi\n- Postprocessor",
        "escalation": "J11 CI → E5 optimizasyon",
    },
    "B52": {
        "identity": "Additive yukleme, bolme ve async ile acik dunya streaming.",
        "when_use": "- Scene streaming adresleri\n- Dunya bolme\n- Yukleme sirasi",
        "escalation": "B38 bellek → B31 proc → E8 level",
    },
}

FILL: dict[str, tuple[str, str]] = {**FILL_E, **FILL_REST}


def patch_agent(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^id:\s*(\S+)", text, re.M)
    if not m:
        return False
    aid = m.group(1)
    if aid not in FILL:
        return False
    bridge, out = FILL[aid]
    orig = text

    text = text.replace(
        "### Bridge\n{Hangi alanlarla, hangi noktada kesisim var}",
        f"### Bridge\n{bridge}",
        1,
    )
    text = text.replace(
        "## Output Format\n{Ciktinin formati — dosya/commit/PR/test raporu.}",
        f"## Output Format\n{out}",
        1,
    )

    ex = CURSOR.get(aid)
    if ex:
        if "identity" in ex:
            text = text.replace("## Identity\n{Cursor dolduracak}", f"## Identity\n{ex['identity']}", 1)
        if "when_use" in ex:
            text = text.replace("## When to Use\n{Cursor dolduracak}", f"## When to Use\n{ex['when_use']}", 1)
        if "escalation" in ex:
            text = text.replace("## Escalation\n{Cursor dolduracak}", f"## Escalation\n{ex['escalation']}", 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    skip_dirs = {"unity-vfx-animation", "unity-technical-artist", "unity-shader-developer", "unity-multiplayer"}
    n = 0
    for p in sorted((AGENTS / "3d-cad").rglob("AGENT.md")):
        if any(s in p.parts for s in skip_dirs):
            continue
        if patch_agent(p):
            n += 1
            print("patched", p.relative_to(ROOT))
    for ud in sorted((AGENTS / "backend").glob("unity-*")):
        if ud.name in skip_dirs:
            continue
        agent_md = ud / "AGENT.md"
        if agent_md.is_file() and patch_agent(agent_md):
            n += 1
            print("patched", agent_md.relative_to(ROOT))
    print(f"Done: {n} files")


if __name__ == "__main__":
    main()
