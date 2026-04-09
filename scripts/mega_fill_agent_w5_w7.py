#!/usr/bin/env python3
"""Fill Bridge / Output Format (and Unity placeholders) for W5-W7 AGENT.md files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

# id -> (bridge, output_format)
# Turkish prose to match repo style.
FILL: dict[str, tuple[str, str]] = {
    "F1": (
        "F2 (analiz), F9 (kalite), ETL (F4) ile veri akisi; cikti temiz DataFrame/CSV.",
        "Temizlenmis veri ozeti (satir/sutun sayisi), uygulanan kurallar listesi, ornek kod veya notebook parcasi, risk notu.",
    ),
    "F2": (
        "F1 (temiz veri), F3 (gorsel), F10 (istatistik) ile kesinlestirme; rapor F5 ile.",
        "Bulgu ozeti, hipotez/sonuc tablosu, grafik onerisi (F3'e gecis), metrik tanimlari ve sinirliliklar.",
    ),
    "F3": (
        "F2 (metrikler), F5 (rapor) ile hizalama; renk/ERISIM F3 knowledge.",
        "Secilen chart turu gerekcesi, statik/interaktif cikti (png/html), legend ve eksen etiketleri, erisim notu.",
    ),
    "F4": (
        "F1/F9 giris kalitesi; dagitim F8 (deployment) ile; izleme G4 ile.",
        "DAG veya pipeline tanimi, schedule, SLI/alert listesi, idempotent load stratejisi, rollback adimlari.",
    ),
    "F5": (
        "F2/F3 icerik beslemesi; PDF/otomasyon knowledge; paydas I4 raporu ile.",
        "Rapor basligi, ozet, tablo/ekler listesi, uretilen dosya yolu veya CI artefakti, versiyon/tarih.",
    ),
    "F6": (
        "F4 veri modeli; F9 dogrulama kurallari; performans G9 token ile karistirma.",
        "SQL dosyalari veya migration notu, explain ozeti, indeks onerileri, test sorgusu sonuclari.",
    ),
    "F7": (
        "F6 (veri cekme), F5 (tablo cikti); API rate limit ve secret yonetimi.",
        "Sheet/workbook adlari, formuller veya Apps Script ozeti, erisim scope, ornek export.",
    ),
    "F8": (
        "F4 prototip; production CI G8; reproducibility F9 ile.",
        "Notebook veya script listesi, kernel/env, cikti hucresi ozeti, `requirements`/`environment` notu.",
    ),
    "F9": (
        "F1 temizlik oncesi/sonrasi; F4 pipeline gate; F6 constraint kontrolu.",
        "Kural seti, ihlal ornekleri, lineage ozeti, oneri listesi ve sahiplik.",
    ),
    "F10": (
        "F2 hipotez; A/B F12 oyun; raporlama F5.",
        "Model varsayimlari, p-degeri/guven araligi tablosu, etki buyuklugu, alternatif model notu.",
    ),
    "F11": (
        "B19 oyun olaylari; F12 deney; analytics SDK knowledge.",
        "Event sema listesi, funnel adimlari, dashboard linki veya CSV cikti, bilinen sapma notu.",
    ),
    "F12": (
        "F11 metrikler; B19 performans; build pipeline G10.",
        "Profiler capture adimlari, bottleneck sinifi (CPU/GPU/memory), oneri listesi, tekrar uretim komutu.",
    ),
    "F13": (
        "F11 davranis; UX arastirma K1; veri gizliligi kurallari.",
        "Toplama yontemi, orneklem buyuklugu, heatmap/session linki, etik not ve PII maskeleme.",
    ),
    "G1": (
        "A2 routing; B* implement; watchdog ve heartbeat kurallari.",
        "Gorev dagitim ozeti, agent listesi ve sira, bagimlilik grafigi (metin), basarisiz adim ve retry.",
    ),
    "G2": (
        "G9 performans; model registry; uretim G10.",
        "Metrik paneli ozeti (latency/quality), alarm esikleri, karsilastirma tablosu, oneri aksiyonu.",
    ),
    "G3": (
        "MCP registry; plugin kurulum; saglik G2 ile.",
        "Sunucu listesi, son ping sonucu, basarisiz tool ve kok neden, oneri fix veya disable.",
    ),
    "G4": (
        "install.sh; secrets symlink; ortam degiskenleri.",
        "Degisen anahtarlar listesi (deger yok), sema diff ozeti, rollback adimlari, dogrulama checklist.",
    ),
    "G5": (
        "G3 hata ayiklama; G9 maliyet; guvenlik B13.",
        "Pattern ozeti, ornek log satirlari (maskeli), korelasyon notu, oneri kurali.",
    ),
    "G6": (
        "G4 config; disaster recovery; veri G9.",
        "Yedek konumu, boyut, restore test sonucu, schedule ve retention, basarisiz job notu.",
    ),
    "G7": (
        "G4 semver; marketplace plugin; breaking change.",
        "Surum karsilastirmasi, changelog ozeti, risk seviyesi, guncelleme onerisi ve zamanlama.",
    ),
    "G8": (
        "G6 yedek; G9 izleme; macOS launchd.",
        "Cron/launchd tanimi, son calisma zamani, stdout/stderr ozeti, idempotent id notu.",
    ),
    "G9": (
        "G2 kalite; kota yonetimi CLAUDE.md; maliyet raporu.",
        "Token/latency ozeti, budget karsilastirmasi, trend notu, tasarruf onerisi.",
    ),
    "G10": (
        "CI/CD; Firebase/Vercel; onizleme URL.",
        "Hedef ortam, build log ozeti, deploy URL veya commit SHA, smoke test sonucu.",
    ),
    "G11": (
        "B19 Unity sahne; G12 inference; egitim G9 maliyet.",
        "Egitim konfigi, reward tanimi, curriculum asamalari, model cikti yolu ve metrik egrisi.",
    ),
    "G12": (
        "B19 gameplay; G11 model cikti; cihaz performansi F12.",
        "ONNX/Sentis asset yolu, input/output tensor boyutlari, latency olcumu, fallback davranisi.",
    ),
    "I1": (
        "A2 gorev analizi; I2/I4 kapasite; lock docs.",
        "Hedef proje/board, issue key listesi, transition ozeti, atanan sprint ve sahip.",
    ),
    "I2": (
        "I1 giris; I3 parcalama; I7 burndown.",
        "Sprint hedefi, kapasite tablosu, secilen issue listesi, risk ve bagimlilik notu.",
    ),
    "I3": (
        "I2 scope; B* implement; DoD knowledge.",
        "Epic alt task listesi, tahmin ve bagimlilik, tanimlanan DoD, siraya konan sira.",
    ),
    "I4": (
        "I2 ilerleme; I7 metrik; paydas raporu sablonu.",
        "Dashboard ozeti, trend cumleleri, blokaj listesi, sonraki adimlar.",
    ),
    "I5": (
        "I2 oncelik; B13 risk; kullanici onayi WAITING.",
        "Karar ozeti, secenekler ve skor, escalation gereksinimi, kayit linki veya yorum.",
    ),
    "I6": (
        "I2 backlog; I3 detay; I9 retro aksiyonlari.",
        "Oncelik sirasi, story map ozeti, silinen/ertelenen maddeler ve gerekce.",
    ),
    "I7": (
        "I2 plan; I4 rapor; scope degisimi tespiti.",
        "Burn/burnup degerleri, velocity, sapma analizi, duzeltici oneri.",
    ),
    "I8": (
        "I1 guncel isler; I4 status; async tooling.",
        "Katilimci bazli blok notlari, blokajlar, ertelenen isler, takip maddeleri.",
    ),
    "I9": (
        "I8 gunluk; I6 iyilestirme; takim sagligi.",
        "Format secimi, tema ve aksiyon sahipleri, metrik trend (oylama/health), takip tarihi.",
    ),
    "I10": (
        "I2 planlama; I3 parca buyuklugu; I7 gerceklesen.",
        "Tahmin yontemi, story point dagilimi, sapma analizi, bir sonraki sprint icin ogrenilenler.",
    ),
}

DATA_UNITY_EXTRA: dict[str, dict[str, str]] = {
    "F11": {
        "identity": "Unity Analytics ve Custom Events ile oyuncu telemetrisi, funnel ve A/B test metrikleri.",
        "when_use": "- Custom event ve parametre semasi tasarimi\n- Funnel ve cohort analizi\n- A/B deneysel tasarim ve sonuc raporu",
        "escalation": "Oyun entegrasyonu B19 → playtest verisi F13 → performans darbogazi F12",
    },
    "F12": {
        "identity": "Unity Profiler, Frame Debugger ve Memory Profiler ile kare, bellek ve GPU darbogaz analizi.",
        "when_use": "- Profiler capture ve bottleneck siniflandirmasi\n- Frame Debugger ile draw call ve overdraw incelemesi\n- Memory leak, GC ve allocation analizi",
        "escalation": "Sahne ve render B19 → telemetri F11 → cihaz ML cikisi G12",
    },
    "F13": {
        "identity": "Playtest oturumlari, heatmap ve davranis metrikleri ile niteliksel ve nicel geri bildirim analizi.",
        "when_use": "- Playtest protokolu ve veri toplama tasarimi\n- Heatmap ve session replay analizi\n- Oyuncu davranis metrikleri ve raporlama",
        "escalation": "Tasarim geri bildirimi B19 → analytics F11 → KVKK/PII konulari kullaniciya",
    },
}

UNITY_EXTRA: dict[str, dict[str, str]] = {
    "G11": {
        "identity": "Unity ML-Agents ile RL/IL egitimi, curriculum ve self-play senaryolari.",
        "when_use": "- RL/IL egitim konfigurasyonu ve reward tasarimi\n- Egitim ortami ve curriculum asamalari\n- Model cikti ve metrik izleme",
        "escalation": "Oyun AI davranisi B19 → Sentis inference G12 → performans F12",
    },
    "G12": {
        "identity": "Unity Sentis ile ONNX model import, cihaz ustu cikarim ve NPC/oyun AI entegrasyonu.",
        "when_use": "- ONNX/Sentis pipeline ve optimizasyon\n- Runtime inference ve tensor boyutlari\n- NPC/oyun AI icin model entegrasyonu",
        "escalation": "ML-Agents egitim G11 → oyun mantigi B19 → profil F12",
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

    for extra in (DATA_UNITY_EXTRA, UNITY_EXTRA):
        if aid in extra:
            ex = extra[aid]
            text = text.replace("## Identity\n{Cursor dolduracak}", f"## Identity\n{ex['identity']}", 1)
            text = text.replace("## When to Use\n{Cursor dolduracak}", f"## When to Use\n{ex['when_use']}", 1)
            text = text.replace("## Escalation\n{Cursor dolduracak}", f"## Escalation\n{ex['escalation']}", 1)

    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    dirs = [
        AGENTS / "data-analytics",
        AGENTS / "ai-ops",
        AGENTS / "jira-pm",
    ]
    n = 0
    for base in dirs:
        for p in sorted(base.rglob("AGENT.md")):
            if patch_agent(p):
                n += 1
                print("patched", p.relative_to(ROOT))
    print(f"Done: {n} files")


if __name__ == "__main__":
    main()
