#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "global" / "skills"

REQUIRED = [
    "## When NOT to Use",
    "## Red Flags",
    "## Error Handling",
    "## Verification",
]


def has_section(text: str, header: str) -> bool:
    return re.search(rf"^{re.escape(header)}\s*$", text, flags=re.M) is not None


def append_sections(text: str) -> str:
    missing = [h for h in REQUIRED if not has_section(text, h)]
    if not missing:
        return text

    out = text.rstrip() + "\n\n"

    if "## When NOT to Use" in missing:
        out += "## When NOT to Use\n"
        out += "- Tek satirlik basit soru/cevap ise\n"
        out += "- Skill'in scope'u disindaysa\n"
        out += "- Riskli/destructive is ise (ayri onay gerekir)\n\n"

    if "## Red Flags" in missing:
        out += "## Red Flags\n"
        out += "- Belirsiz hedef/kabul kriteri\n"
        out += "- Gerekli dosya/izin/secret eksik\n"
        out += "- Ayni adim 2+ kez tekrarlandi\n\n"

    if "## Error Handling" in missing:
        out += "## Error Handling\n"
        out += "- Gerekli kaynak yoksa → dur, blocker'i raporla\n"
        out += "- Komut/akıs hatasi → en yakin guvenli noktadan devam et\n"
        out += "- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir\n\n"

    if "## Verification" in missing:
        out += "## Verification\n"
        out += "- [ ] Beklenen cikti uretildi\n"
        out += "- [ ] Yan etki yok (dosya/ayar)\n"
        out += "- [ ] Gerekli log/rapor paylasildi\n"

    return out.rstrip() + "\n"


def main() -> None:
    changed = 0
    for path in sorted(SKILLS_DIR.glob("**/SKILL.md")):
        old = path.read_text(encoding="utf-8")
        new = append_sections(old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"skills_updated {changed}")


if __name__ == "__main__":
    main()

