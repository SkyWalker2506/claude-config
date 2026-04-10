#!/usr/bin/env python3
"""One-shot: insert ## Code Examples before ## Anti-Patterns for market-research knowledge gaps."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
ANCHOR = "\n## Anti-Patterns\n"

# Path relative to agents/ → block body (includes ## Code Examples header, ends with newline)
BLOCKS: dict[str, str] = {
    "market-research/competitor-analyst/knowledge/benchmark-methodology.md": """## Code Examples

### Örnek: normalize benchmark satırı

```yaml
metric_id: "time_to_first_value_hours"
peer: "Competitor A"
segment: "Mid-market B2B SaaS"
value: 48
currency_normalized: "USD_ACV"
confidence: "medium"
as_of: "2026-01-15"
source_type: "secondary_annual_report"
```

""",
    "market-research/competitor-analyst/knowledge/competitive-positioning.md": """## Code Examples

### Örnek: positioning cümlesi (şablon doldurulmuş)

```text
[AnalyticsBoard] is a [embedded analytics platform] that helps [SaaS PMs]
[ship dashboards without eng weeks] by [SQL-in-UI + row-level cache]
unlike [generic BI tools] we [ship under 200 KB SDK with SSO baked in].
```

""",
    "market-research/competitor-analyst/knowledge/competitor-swot-template.md": """## Code Examples

### Örnek: SWOT özeti (kısa tablo)

```markdown
| | Helpful | Harmful |
|---|---------|---------|
| **Internal** | **S**: NPS 45 enterprise refs | **W**: No EU region |
| **External** | **O**: New data privacy regs | **T**: Big cloud bundles analytics |
```

""",
    "market-research/competitor-analyst/knowledge/feature-comparison-matrix.md": """## Code Examples

### Örnek: özellik matrisi (MVP)

```markdown
| Capability | Us | A | B |
|------------|----|----|---|
| SSO (SAML) | Yes | Yes | Add-on |
| Row-level security | Yes | Partial | No |
| On-prem | Roadmap | Yes | No |
```

""",
    "market-research/content-repurposer/knowledge/content-atomization.md": """## Code Examples

### Örnek: pillar → atom listesi

```markdown
Pillar: "2026 Q1 product webinar"

Atoms:
- [QUOTE] "Ship dashboards in a sprint" — timestamp 12:40
- [STAT] 73% faster time-to-insight (n=120 customers)
- [FAQ] "Does it support Snowflake?" → 3-sentence answer + doc link
```

""",
    "market-research/content-repurposer/knowledge/format-conversion.md": """## Code Examples

### Örnek: blog → LinkedIn dönüşümü

```markdown
Kaynak H2: "Why row-level cache matters"
LinkedIn çıktısı:
Hook: Row-level cache isn't perf — it's permission model.
Bullets: (1) tenant isolation (2) audit trail (3) BI tool sprawl
CTA: Comment "cache" for architecture checklist PDF.
```

""",
    "market-research/content-repurposer/knowledge/multi-channel-adaptation.md": """## Code Examples

### Örnek: tek mesaj, üç kanal

```text
Core claim: "Cut ad-hoc SQL requests by 60% in 90 days."

- Email: subject + 4 bullets + PS with case study
- X/Twitter: 240 chars + link to thread
- Slack customer: 2 sentences + link to Loom walkthrough
```

""",
    "market-research/content-repurposer/knowledge/repurpose-workflow.md": """## Code Examples

### Örnek: basit iş akışı (YAML)

```yaml
source: "webinar_recording.mp4"
steps:
  - extract_transcript
  - tag_chapters
  - generate: [blog_outline, quote_cards, email_digest, short_clips]
owner: "content_lead"
sla_hours: 48
```

""",
    "market-research/geo-agent/knowledge/ai-visibility-optimization.md": """## Code Examples

### Örnek: marka + ürün cevaplılık kontrol listesi

```markdown
Prompt set (aynı session):
1. "Best [category] for [ICP] in [region]?"
2. "Compare [us] vs [top competitor] for [use case]"
Log: cited_brands[], our_rank_or_absent, hallucination_flags[]
```

""",
    "market-research/geo-agent/knowledge/geo-seo-strategies.md": """## Code Examples

### Örnek: GEO öncelik backlog (mini)

```markdown
| Asset | Action |
|-------|--------|
| /docs/pricing | Add FAQ JSON-LD + LLM-readable summary |
| G2 profile | Align first paragraph with canonical positioning |
| YouTube demo | Chapters + transcript for citation snippets |
```

""",
    "market-research/geo-agent/knowledge/llm-seo-patterns.md": """## Code Examples

### Örnek: citation-dostu paragraf yapısı

```markdown
## What is [X]?
One-sentence definition. [Brand] provides [Y] for [ICP] ([source year]).

### Key capabilities
- Bullet with named feature + limitation when relevant
- Link to primary doc, not login wall
```

""",
    "market-research/geo-agent/knowledge/structured-data-markup.md": """## Code Examples

### Örnek: SoftwareApplication + Offer (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "AnalyticsBoard",
  "applicationCategory": "BusinessApplication",
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "0",
    "description": "Free tier — up to 3 dashboards"
  }
}
```

""",
    "market-research/market-researcher/knowledge/competitor-research-methods.md": """## Code Examples

### Örnek: rakip profil kartı

```markdown
## Competitor: Acme Analytics
- ICP: Mid-market SaaS
- Motion: PLG + inside sales
- Proof: G2 4.6 (n=400), mentions "slow support" in 12%
- Differentiation vs us: Deeper Salesforce native; weaker embedded SDK
```

""",
    "market-research/market-researcher/knowledge/market-analysis-framework.md": """## Code Examples

### Örnek: TAM/SAM/SOM tablosu

```markdown
| | Definition | Value | Notes |
|---|------------|-------|-------|
| TAM | All firms with BI spend > $10k/yr | $4.2B | Top-down |
| SAM | Product-led SaaS in NA+EU | $620M | Bottom-up accounts |
| SOM | Win 2% SAM in 36 mo | $12.4M | Assumes 18 mo CAC payback |
```

""",
    "market-research/market-researcher/knowledge/market-sizing.md": """## Code Examples

### Örnek: bottom-up hesap sayımı

```python
# Illustrative — adjust inputs
accounts = 48_000  # firms in ICP
penetration = 0.08
avg_contract = 24_000
sam = accounts * penetration * avg_contract
```

""",
    "market-research/market-researcher/knowledge/trend-analysis-tools.md": """## Code Examples

### Örnek: trend kanıt paketi

```markdown
Signal: "AI copilot for analytics"
Evidence:
- Gartner Hype Cycle 2025 — category position
- GitHub stars growth repo:xyz +180% YoY (snapshot)
- Hiring: 14 "analytics copilot" PM roles on LinkedIn (EU, 30d)
```

""",
    "market-research/pricing-strategist/knowledge/ab-test-pricing.md": """## Code Examples

### Örnek: fiyat A/B test planı

```markdown
Hypothesis: +10% on Pro tier does not reduce conversion >5%
Split: 50/50 by account_id hash (sticky)
Primary metric: net new MRR / visitor
Guardrails: refund rate, sales cycle length
Stop rule: 2 weeks OR 5k exposures per arm
```

""",
    "market-research/pricing-strategist/knowledge/pricing-psychology.md": """## Code Examples

### Örnek: fiyat sunumu (Good / Better / Best)

```markdown
| Tier | Price | Anchor copy |
|------|-------|-------------|
| Starter | $29 | "For individuals" |
| Team | $99 | **Most popular** — "Everything in Starter + SSO" |
| Business | $299 | "SOC2 + audit logs" |
```

""",
    "market-research/pricing-strategist/knowledge/tier-pricing-design.md": """## Code Examples

### Örnek: kullanım metrikleri → tier

```markdown
Metric: "monthly active dashboard viewers"
Free: ≤ 3 | Pro: ≤ 25 | Enterprise: unlimited + SLA
Overage: $2/viewer/month billed arrears
```

""",
    "market-research/pricing-strategist/knowledge/value-based-pricing.md": """## Code Examples

### Örnek: değer hesabı (basit)

```text
Baseline: manual SQL hours / month per analyst = 40
After: 10 hours (75% reduction)
Loaded cost $80/h → $2,400 saved / analyst / month
Price ask: 20% of savings = $480 seat/month ceiling
```

""",
    "market-research/revenue-analyst/knowledge/financial-projection.md": """## Code Examples

### Örnek: 12 aylık gelir projeksiyonu (satır)

```markdown
| Month | New logos | Expansion | Churn | Net MRR |
|-------|-----------|-----------|-------|---------|
| M1 | +12 | +2% | -1.5% | $118k |
| M2 | +14 | +2% | -1.5% | $126k |
```

""",
    "market-research/revenue-analyst/knowledge/pricing-strategy-framework.md": """## Code Examples

### Örnek: strateji seçimi özeti

```markdown
- Value metric: "active dashboards"
- Packaging: Good/Better/Best + usage overage
- Discount policy: max 20% on annual prepay; no multi-year lock without exec approval
```

""",
    "market-research/revenue-analyst/knowledge/revenue-model-patterns.md": """## Code Examples

### Örnek: basit birim ekonomisi

```text
ARPA = $2,400/year
Gross margin = 78%
CAC payback = 14 months (target ≤ 18)
Net retention = 115%
```

""",
    "market-research/revenue-analyst/knowledge/unit-economics.md": """## Code Examples

### Örnek: CAC / LTV kontrol tablosu

```markdown
| Segment | CAC | LTV (36m) | LTV:CAC | Payback |
|---------|-----|-----------|---------|---------|
| SMB PLG | $1.2k | $9k | 7.5x | 11 mo |
| Mid-market | $18k | $96k | 5.3x | 16 mo |
```

""",
    "market-research/seo-agent/knowledge/keyword-research-tools.md": """## Code Examples

### Örnek: intent etiketli kelime kümesi

```csv
keyword,intent,volume,primary_url
"embedded analytics sdk",commercial,1900,/product/sdk
"what is embedded analytics",informational,2400,/learn/embedded-analytics
```

""",
    "market-research/seo-agent/knowledge/meta-tag-optimization.md": """## Code Examples

### Örnek: title + meta şablonu

```html
<title>Embedded Analytics SDK for SaaS | AnalyticsBoard</title>
<meta name="description" content="Ship customer-facing dashboards in days. Row-level security, SSO, &lt;200 KB SDK. SOC2-ready.">
```

""",
    "market-research/seo-agent/knowledge/seo-audit-checklist.md": """## Code Examples

### Örnek: mini audit çıktısı (özet)

```markdown
## SEO audit — example.com (2026-04-10)
**P0:** 120 URLs blocked by robots typo `/disallow: /api` catching `/api-docs`
**P1:** Duplicate titles on paginated blog (pages 2–n)
**P2:** Missing Article schema on 45 posts
```

""",
    "market-research/seo-agent/knowledge/technical-seo-guide.md": """## Code Examples

### Örnek: Core Web Vitals field verisi (CrUX benzeri)

```json
{
  "origin": "https://example.com",
  "LCP": { "p75_ms": 2100 },
  "INP": { "p75_ms": 180 },
  "CLS": { "p75": 0.08 }
}
```

""",
    "market-research/social-media-agent/knowledge/linkedin-content-strategy.md": """## Code Examples

### Örnek: LinkedIn gönderi (kurumsal)

```markdown
Hook: We cut dashboard requests to data team by 60% — not with more headcount.

3 lessons:
1) …
2) …
3) …

CTA: What's your #1 bottleneck — SQL queue or tool sprawl? Comment below.
```

""",
    "market-research/social-media-agent/knowledge/scheduling-tools.md": """## Code Examples

### Örnek: haftalık yayın çizelgesi

```markdown
| Day | Channel | Format |
|-----|---------|--------|
| Tue | LinkedIn | Thought leadership |
| Thu | X | Dev tip + link |
| Fri | Newsletter | Digest |
```

""",
    "market-research/social-media-agent/knowledge/social-media-post-templates.md": """## Code Examples

### Örnek: şablon seti

```text
[Problem] → [Insight] → [Proof point] → [Soft CTA]
"PMs wait 2 weeks for dashboards" → "Embedded analytics fixes handoffs" → "73% faster TTFV (n=120)" → "DM for checklist"
```

""",
    "market-research/social-media-agent/knowledge/twitter-engagement.md": """## Code Examples

### Örnek: thread iskeleti

```text
1/ Problem (one line)
2/ Wrong fix vs right fix
3/ Mini framework (3 bullets)
4/ Link to doc + "follow for B2B analytics"
```

""",
}


def main() -> None:
    for rel, block in BLOCKS.items():
        path = AGENTS / rel
        if not path.is_file():
            print("missing file:", path)
            continue
        text = path.read_text(encoding="utf-8")
        if "## Code Examples" in text:
            print("skip (already has):", rel)
            continue
        if ANCHOR not in text:
            print("skip (no anchor):", rel)
            continue
        path.write_text(text.replace(ANCHOR, "\n" + block + ANCHOR.lstrip("\n"), 1), encoding="utf-8")
        print("updated:", rel)


if __name__ == "__main__":
    main()
