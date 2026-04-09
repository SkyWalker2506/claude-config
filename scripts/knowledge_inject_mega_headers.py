#!/usr/bin/env python3
"""
Inject mega-prompt knowledge skeleton (Quick Reference … Deep Dive Sources) into
knowledge/*.md files that lack '## Quick Reference'. Inserts after first H1 or after YAML frontmatter.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

BLOCK = """
## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---
"""


def files_missing_qr() -> list[Path]:
    cmd = r"""
    comm -23 \
      <(find agents -path '*/knowledge/*.md' ! -name '_index.md' | sort) \
      <(grep -rl '## Quick Reference' agents --include='*.md' | grep '/knowledge/' | grep -v '_index.md' | sort)
    """
    out = subprocess.check_output(["bash", "-c", cmd], cwd=ROOT, text=True)
    return [ROOT / p.strip() for p in out.strip().splitlines() if p.strip()]


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "## Quick Reference" in text:
        return False

    # After YAML frontmatter + optional blank, find first # line (H1)
    m = re.match(r"^((?:---\n)(?:.|\n)*?(?:\n---\n))(\s*)(# [^\n]+\n)", text)
    if m:
        new_text = m.group(1) + m.group(2) + m.group(3) + BLOCK + text[m.end() :]
        path.write_text(new_text, encoding="utf-8")
        return True

    m2 = re.match(r"^(# [^\n]+\n)", text)
    if m2:
        new_text = m2.group(1) + BLOCK + text[m2.end() :]
        path.write_text(new_text, encoding="utf-8")
        return True

    # No H1: prepend block after frontmatter or at start
    m3 = re.match(r"^((?:---\n)(?:.|\n)*?(?:\n---\n))", text)
    if m3:
        new_text = m3.group(1) + BLOCK + text[m3.end() :]
        path.write_text(new_text, encoding="utf-8")
        return True

    path.write_text(BLOCK.lstrip("\n") + "\n" + text, encoding="utf-8")
    return True


def main() -> None:
    paths = files_missing_qr()
    n = 0
    for p in paths:
        if inject(p):
            n += 1
            print("injected", p.relative_to(ROOT))
    print(f"Done: {n} files (total candidates {len(paths)})")


if __name__ == "__main__":
    main()
