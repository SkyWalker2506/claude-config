#!/usr/bin/env python3
"""Fill Bridge / Output Format (+ Cursor blocks) for W2-W4 AGENT.md files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

FILL: dict[str, tuple[str, str]] = {
    "C1": (
        "C2/C3/C5 ile — hook ciktisi review ve CI gate'e beslenir; formatter config repo kokunde.",
        "Hook log ozeti, fail satirlari (kisa), auto-fix uygulandiysa diff ozeti, tekrar calistirma komutu.",
    ),
    "C2": (
        "C1 oncesi secret tarama; B13 guvenlik audit; bagimlilik C1 ile ayni PR'da.",
        "Tarama raporu: arac adi, bulgu listesi (dosya: satir maskeli), severity, suppress gerekcesi.",
    ),
    "C3": (
        "C1/C5 PR kalitesi; C6 insan review SLA; C4 harici bot ile karsilastirma.",
        "Skor veya ozet, bulgu listesi, oneri snippet'leri, false positive isaretleme notu.",
    ),
    "C4": (
        "GitHub PR ve checks; C5 merge politikasi; kod standardi A9/B agentlari.",
        "CodeRabbit config veya kural diff'i, ornek yorum formati, CI entegrasyon adimlari.",
    ),
    "C5": (
        "GitHub Actions / PR API; C4 bot; branch protection kurallari.",
        "PR numarasi, check durumu tablosu, merge blok nedeni, gerekli onay listesi.",
    ),
    "C6": (
        "C3 AI review; uzman B* agentlari; I4/I8 SLA ve raporlama.",
        "Reviewer atama tablosu, SLA durumu, escalation nedeni ve hedef kisi/ekip.",
    ),
    "D3": (
        "D4 tasarim cikti; B3 frontend implement; Tailwind/design token knowledge.",
        "Bilesen listesi, breakpoint kararlari, dosya yollari, acik TODO ve bagimlilik notu.",
    ),
    "D4": (
        "D3 kod entegrasyonu; D2 design system token; export/build pipeline.",
        "Figma link veya dosya, cikarilan token ozeti, component envanteri tablosu.",
    ),
    "D5": (
        "H5/H6 icerik; D9 marka sesi; veri gorsellestirme F3 ile.",
        "Slayt plani veya storyboard, sunum dosyasi yolu veya link, konusmaci notlari.",
    ),
    "D7": (
        "D9 marka renk/font; web build; sprite atlas pipeline.",
        "SVG/sprite cikti yolu, boyut ve format tablosu, favicon/manifest paket listesi.",
    ),
    "D8": (
        "D1 UX arastirma; WCAG erisilebilirlik; K1 kaynak dogrulama.",
        "Audit checklist sonucu, oncelikli bulgular, mockup ve ekran referansi.",
    ),
    "D9": (
        "D4 gorsel dil; D5 sunum; D2 token ile hizalama.",
        "Marka kilavuzu ozeti, palet ve tipografi tablosu, voice/tone ornek cumleler.",
    ),
    "D11": (
        "B19 gameplay ve UI state; D12 akis; USS/UXML knowledge.",
        "UI dokumu listesi, USS/UXML dosya yollari, binding ornekleri, test sahnesi adi.",
    ),
    "D12": (
        "D11 ekranlar; B19 tutorial implementasyonu; K6 ogrenme yollari.",
        "Akis ozeti (ekran sirasi), onboarding adimlari, tutorial tetikleyicileri.",
    ),
    "D13": (
        "B19 dunya ve kamera; D12 navigasyon akisi; HUD bileşen knowledge.",
        "HUD wire ozeti, minimap ayarlari, compass/damage indicator parametreleri.",
    ),
    "J1": (
        "J2 deploy artefakti; J7 incident rollback; registry ve imza.",
        "Dockerfile ve compose diff ozeti, image tag ve boyut, guvenlik tarama sonucu.",
    ),
    "J2": (
        "J1 container; J8 kapasite; IaC state ve ortam.",
        "Deploy plan, terraform/helm ozeti, hedef URL ve surum, smoke test sonucu.",
    ),
    "J3": (
        "J2 edge/CDN; sertifika yenileme otomasyonu; DNS provider.",
        "DNS kayit ozeti, sertifika serial/yenileme tarihi, CDN/proxy notu.",
    ),
    "J4": (
        "J7 olay esigi; J5 maliyet dashboard; SLO tanimlari.",
        "Uptime/health ozeti, alert kural listesi, dashboard veya panel linki.",
    ),
    "J5": (
        "J4 kullanim metrikleri; reserved/spot karari; finans onay.",
        "Maliyet kirilimi, tasarruf onerileri, uygulama sirasi ve risk notu.",
    ),
    "J6": (
        "G10 Firebase deploy; B15 mobil; guvenlik rules B13.",
        "Hedef servisler, rules/index diff ozeti, emulator veya staging test sonucu.",
    ),
    "J7": (
        "J4 alarm; J2 rollback; I4/I8 iletişim.",
        "Olay zaman cizelgesi, RCA ozeti, aksiyon maddeleri ve sahip.",
    ),
    "J8": (
        "J2/J6 hedef mimari; DR ve yedek G6; kapasite plani.",
        "Taslak diyagram notu, IaC modul listesi, olcekleme ve DR onerisi.",
    ),
    "J9": (
        "J4 SLO; staging ortami; performans baseline.",
        "Load test araci ve senaryo, throughput/latency tablosu, bottleneck ve oneri.",
    ),
    "J11": (
        "J1 CI image; J12 asset merge; B19 platform build.",
        "Workflow ozeti, platform matrisi, artefak boyutu ve indirme veya CI run linki.",
    ),
    "J12": (
        "J11 pipeline; B51 Addressables; conflict ve prefab merge.",
        "Merge stratejisi, LFS esigi, kilitleme politikasi, cozulen conflict ozeti.",
    ),
}

CURSOR_EXTRAS: dict[str, dict[str, str]] = {
    "D11": {
        "identity": "UI Toolkit, USS/UXML ve runtime data baglama ile Unity arayuz gelistirme.",
        "when_use": "- USS/UXML layout ve tema\n- UI Builder veya kod ile widget\n- ListView/SerializeField baglama ve responsive davranis",
    },
    "D12": {
        "identity": "Oyun UX — menu, tutorial, akis ve oyuncu onboarding tasarimi ve dokumantasyonu.",
        "when_use": "- Ana/menu akisi ve gecisler\n- Tutorial ve ilk oturum deneyimi\n- Oyuncu rehberligi ve geri bildirim metinleri",
        "escalation": "UI implementasyon D11 → gameplay B19 → arastirma K1",
    },
    "D13": {
        "identity": "HUD, minimap, damage indicator ve compass/waypoint sistemleri tasarimi.",
        "when_use": "- HUD yerlesimi ve okunabilirlik\n- Minimap ve dunya gosterimi\n- Hasar yonu ve pusula/waypoint",
        "escalation": "Sahne entegrasyonu B19 → akis D12 → profil F12",
    },
    "J11": {
        "identity": "GameCI, Unity Cloud Build, Addressables CI ve platform build matrisi ile Unity CI/CD.",
        "when_use": "- GitHub Actions / GameCI workflow\n- Addressables ve asset pipeline CI\n- Coklu platform build ve artefak optimizasyonu",
    },
    "J12": {
        "identity": "Plastic SCM, Git LFS, prefab/sahne merge ve kilitleme ile Unity kaynak kontrolu.",
        "when_use": "- Plastic veya Git UVC is akisi\n- Buyuk asset ve LFS esikleri\n- Prefab/sahne merge ve conflict cozumu",
        "escalation": "CI/build J11 → asset pipeline B51 → kod B19",
    },
}


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

    ex = CURSOR_EXTRAS.get(aid)
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
    bases = [
        AGENTS / "code-review",
        AGENTS / "design",
        AGENTS / "devops",
    ]
    n = 0
    for base in bases:
        for p in sorted(base.rglob("AGENT.md")):
            if "github-manager" in str(p):
                continue
            if patch_agent(p):
                n += 1
                print("patched", p.relative_to(ROOT))
    print(f"Done: {n} files")


if __name__ == "__main__":
    main()
