#!/usr/bin/env python3
"""Insert missing ## Patterns & Decision Matrix and ## Anti-Patterns for backend knowledge gaps.

Also fixes files where ## Anti-Patterns incorrectly appears before ## Code Examples.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

PATTERNS: dict[str, str] = {
    "backend/api-gateway-agent/knowledge/auth-middleware-jwt-oauth.md": """## Patterns & Decision Matrix

| Senaryo | Seçim |
|---------|--------|
| Public SPA + API | JWT access short TTL + refresh cookie httpOnly |
| S2S | mTLS veya client credentials + audience claim |
| Mobile | PKCE OAuth; no embedded secrets |

""",
    "backend/api-gateway-agent/knowledge/rate-limiting-algorithms-compared.md": """## Patterns & Decision Matrix

| Algoritma | Ne zaman |
|-----------|----------|
| Token bucket | Burst toleransı gerekirse |
| Sliding window | Adil dakika başına limit |
| Fixed window | Basit sayaç; köşe spike riski |

""",
    "backend/api-gateway-agent/knowledge/request-validation-schemas.md": """## Patterns & Decision Matrix

| Katman | Doğrulama |
|--------|-----------|
| Gateway | Boyut, content-type, coarse schema |
| Servis | İş kuralları, DB varlığı |

""",
    "backend/full-stack-web/knowledge/prisma-schema-patterns.md": """## Patterns & Decision Matrix

| Durum | Şema kararı |
|-------|-------------|
| Çok-tenant | `tenantId` + composite unique |
| Soft delete | `deletedAt` + filtreli unique index |
| Büyük metin | Ayrı tablo veya depolama pointer |

""",
    "backend/full-stack-web/knowledge/tailwind-design-system.md": """## Patterns & Decision Matrix

| İhtiyaç | Yaklaşım |
|---------|----------|
| Tema | CSS variables + `tailwind.config` extend |
| Bileşen kütüphanesi | Headless + token sınıfları |

""",
    "backend/full-stack-web/knowledge/vercel-deployment-optimization.md": """## Patterns & Decision Matrix

| Metrik | Önce bak |
|--------|-----------|
| TTFB yüksek | data fetch edge vs node runtime |
| Cold start | function size + region |

""",
    "backend/python-specialist/knowledge/django-vs-fastapi-decision.md": """## Patterns & Decision Matrix

| Sinyal | Django | FastAPI |
|--------|--------|---------|
| Admin + ORM + migrations | Güçlü | Ekle ile |
| Yüksek I/O async | Channels | Native async |

""",
    "backend/python-specialist/knowledge/fastapi-project-structure.md": """## Patterns & Decision Matrix

| Ölçek | Yapı |
|-------|------|
| Küçük | `app/main.py` + routers |
| Orta+ | domain paketleri + `deps.py` |

""",
    "backend/python-specialist/knowledge/pandas-performance-tips.md": """## Patterns & Decision Matrix

| Teknik | Ne zaman |
|--------|----------|
| `category` | Düşük kardinalite string |
| `observed=True` | Seyrek kategoriler |
| Chunked read | RAM sınırı |

""",
    "backend/python-specialist/knowledge/poetry-dependency-management.md": """## Patterns & Decision Matrix

| Durum | Komut / ayar |
|-------|----------------|
| Kütüphane yayını | Semver üst sınır |
| Uygulama | Lock commit + `poetry install --sync` |

""",
    "backend/security-auditor/knowledge/dependency-vulnerability-management.md": """## Patterns & Decision Matrix

| Öncelik | Aksiyon |
|---------|---------|
| Kritik RCE | Patch veya geçici mitigasyon 24–72s |
| Düşük | Backlog + versiyon planı |

""",
    "backend/unity-developer/knowledge/shader-programming-basics.md": """## Patterns & Decision Matrix

| Hedef | Seçim |
|-------|--------|
| Mobil | URP + basit lit |
| PC konsol | HDRP / URP özellik seti |

""",
    "backend/unity-developer/knowledge/unity-editor-tooling.md": """## Patterns & Decision Matrix

| UI | Araç |
|----|------|
| Hızlı ayar | Custom Inspector |
| Çok adımlı akış | EditorWindow + SerializedObject |

""",
    "backend/unity-developer/knowledge/unity-performance-profiling.md": """## Patterns & Decision Matrix

| Sorun | İlk bakış |
|-------|-----------|
| CPU spike | Profiler Timeline + deep profile |
| GC | Memory Profiler allocations |

""",
    "backend/unity-developer/knowledge/upm-package-development.md": """## Patterns & Decision Matrix

| Yayın | Yol |
|-------|-----|
| Dahili | Git URL / Verdaccio |
| Asset Store | Compliance checklist |

""",
    "backend/web-game-dev/knowledge/asset-loading-strategies.md": """## Patterns & Decision Matrix

| Varlık | Strateji |
|--------|----------|
| Büyük sahne | Chunk / streaming |
| Tekrar kullanım | Pool + blob URL cache |

""",
    "backend/web-game-dev/knowledge/game-loop-patterns.md": """## Patterns & Decision Matrix

| Döngü | Kullanım |
|-------|----------|
| `requestAnimationFrame` | Render senkron |
| Sabit timestep | Fizik / replay |

""",
    "backend/web-game-dev/knowledge/webgl-performance-optimization.md": """## Patterns & Decision Matrix

| Darboğaz | Önce |
|----------|------|
| Draw call | Batch / instancing |
| Bellek | Texture boyutu / mip |

""",
    "backend/websocket-agent/knowledge/connection-lifecycle-management.md": """## Patterns & Decision Matrix

| Aşama | Kontrol |
|-------|---------|
| Handshake | Origin + auth |
| Idle | Ping/pong + timeout |

""",
    "backend/websocket-agent/knowledge/pub-sub-message-patterns.md": """## Patterns & Decision Matrix

| Desen | Ne zaman |
|-------|----------|
| Topic per room | Oyun lobisi |
| Fan-out servis | Yüksek yayın |

""",
    "backend/websocket-agent/knowledge/socketio-scaling-strategies.md": """## Patterns & Decision Matrix

| Ölçek | Mekanizma |
|-------|-----------|
| Tek node | Memory adapter |
| Çok node | Redis adapter + sticky veya mesaj odası |

""",
    "backend/websocket-agent/knowledge/websocket-architecture-patterns.md": """## Patterns & Decision Matrix

| Mimari | Seçim |
|--------|--------|
| İnce gateway | Sadece WS terminate |
| BFF | Auth + rate limit edge |

""",
}

ANTIS: dict[str, str] = {
    "backend/api-gateway-agent/knowledge/api-gateway-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Gateway’de iş mantığı | Dağıtık monolit |
| Sınırsız body | DoS yüzeyi |

""",
    "backend/api-gateway-agent/knowledge/auth-middleware-jwt-oauth.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Uzun ömürlü JWT | Çalınırsa geniş pencere |
| Claims’e güvenip authZ atlama | IDOR |

""",
    "backend/api-gateway-agent/knowledge/rate-limiting-algorithms-compared.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| IP-only limit (CGNAT) | Yanlış kısıtlama |
| Limit yanıtında veri sızıntısı | Enumeration |

""",
    "backend/api-gateway-agent/knowledge/request-validation-schemas.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sadece client-side validate | Bypass |
| Şema sürümü yok | Breaking değişiklik |

""",
    "backend/full-stack-web/knowledge/nextjs-app-router-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Her şeyi client component | Bundle şişer |
| `fetch` önbelleği varsayılanına körü güven | Stale veri |

""",
    "backend/full-stack-web/knowledge/prisma-schema-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| İlişkisiz cascade | Veri kaybı |
| Index’siz sık filtre | Full scan |

""",
    "backend/full-stack-web/knowledge/supabase-auth-realtime.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| RLS test etmeden prod | Veri sızıntısı |
| Service role key istemcide | Tam yetki |

""",
    "backend/full-stack-web/knowledge/vercel-deployment-optimization.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Edge’de ağır Node API | Timeout |
| env secret’ı loglama | Sızıntı |

""",
    "backend/performance-optimizer/knowledge/database-query-optimization.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| N+1 sorgu | Gecikme |
| Select * büyük tabloda | I/O şişmesi |

""",
    "backend/performance-optimizer/knowledge/frontend-performance-metrics.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sadece lab Lighthouse | Field farkı |
| CLS ölçmeden font swap | Layout shift |

""",
    "backend/python-specialist/knowledge/django-vs-fastapi-decision.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| “Hepsi async” zorlaması | Karma karmaşık stack |
| İki framework karışık tek repo | Operasyon yükü |

""",
    "backend/python-specialist/knowledge/fastapi-project-structure.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Global state ile test | Flake |
| Route’da DB session leak | Bağlantı tükenmesi |

""",
    "backend/python-specialist/knowledge/poetry-dependency-management.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Lock dosyasını commit etmeme | Prod drift |
| Üst sınır * açık | Breaking sürpriz |

""",
    "backend/unity-developer/knowledge/shader-programming-basics.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Her frame branch yoğun | GPU dalgalanması |
| Precision gereksiz yüksek | Mobil yavaş |

""",
    "backend/unity-developer/knowledge/unity-ecs-dots-guide.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| ECS’de GameObject karışımı | Burst/job engeli |
| Tek dev struct | Cache miss |

""",
    "backend/unity-developer/knowledge/unity-editor-tooling.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Editor’da ağır iş | Donma |
| `OnGUI` ile büyük UI | Performans |

""",
    "backend/unity-developer/knowledge/unity-performance-profiling.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Editor’da ölçüp build iddiası | Yanıltıcı |
| Tek frame’e güven | Spike kaçırma |

""",
    "backend/unity-developer/knowledge/upm-package-development.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| asmdef eksik | Derleme çakışması |
| Semver ihlali | Bağımlılık kırılması |

""",
    "backend/web-game-dev/knowledge/game-loop-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Değişken timestep fizik | Kaotik simülasyon |
| `setInterval` oyun döngüsü | Throttle tutarsız |

""",
    "backend/web-game-dev/knowledge/threejs-scene-management.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Dispose atlama | GPU bellek sızıntısı |
| Her frame `new` vektör | GC baskısı |

""",
    "backend/websocket-agent/knowledge/pub-sub-message-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Kanal adı tahmin edilebilir | Yetkisiz dinleme |
| Mesaj boyutu limitsiz | DoS |

""",
    "backend/websocket-agent/knowledge/socketio-scaling-strategies.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Redis yokken çok node | Oda tutarsızlığı |
| Sticky olmadan yanlış yönlendirme | Bağlantı kopması |

""",
    "backend/websocket-agent/knowledge/websocket-architecture-patterns.md": """## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| WSS’siz prod | MITM |
| Heartbeat yok | Ölü bağlantı birikimi |

""",
}


def move_anti_after_code(text: str) -> str:
    ia = text.find("\n## Anti-Patterns\n")
    ic = text.find("\n## Code Examples\n")
    id_ = text.find("\n## Deep Dive Sources\n")
    if ia == -1 or ic == -1 or ia > ic or id_ == -1:
        return text
    anti_block = text[ia:ic]
    code_through = text[ic:id_]
    return text[:ia] + code_through + anti_block + text[id_:]


def insert_patterns(text: str, block: str) -> str:
    if "## Patterns & Decision Matrix" in text:
        return text
    for alt in ("## Patterns\n", "## Pattern\n"):
        if alt in text:
            return text
    anchor = "\n## Code Examples\n"
    if anchor in text:
        return text.replace(anchor, "\n" + block.rstrip() + "\n" + anchor, 1)
    anchor2 = "\n## Anti-Patterns\n"
    if anchor2 in text:
        return text.replace(anchor2, "\n" + block.rstrip() + "\n" + anchor2, 1)
    anchor3 = "\n## Deep Dive Sources\n"
    if anchor3 in text:
        return text.replace(anchor3, "\n" + block.rstrip() + "\n" + anchor3, 1)
    return text


def insert_anti(text: str, block: str) -> str:
    if "## Anti-Patterns" in text:
        return text
    anchor = "\n## Deep Dive Sources\n"
    if anchor not in text:
        return text
    return text.replace(anchor, "\n" + block.rstrip() + "\n" + anchor, 1)


def main() -> None:
    all_paths = set(PATTERNS) | set(ANTIS)
    for rel in sorted(all_paths):
        path = AGENTS / rel
        if not path.is_file():
            print("missing:", rel)
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        text = move_anti_after_code(text)
        if rel in PATTERNS:
            text = insert_patterns(text, PATTERNS[rel])
        if rel in ANTIS:
            text = insert_anti(text, ANTIS[rel])
        if text != original:
            path.write_text(text, encoding="utf-8")
            print("updated:", rel)
        else:
            print("unchanged:", rel)


if __name__ == "__main__":
    main()
