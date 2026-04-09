---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Landing Page Anatomy

## Quick Reference

**Standard conversion LP stack (single offer):**

1. **Above the fold:** Value prop (H1), supporting subhead, primary CTA, trust strip (logos / metric).
2. **Problem → agitation → solution:** 2–4 sections; each with one idea.
3. **Proof:** Testimonials (specific outcomes), logos, metrics, third-party badges.
4. **Offer detail:** What’s included, for whom, what happens next.
5. **FAQ:** Objections (pricing, security, cancellation).
6. **Final CTA:** Repeat primary action + secondary (calendar / contact).

- **Bridge to M1:** **M1 Free Tool Builder** embeds live in hero or mid-page—match headline promise to tool’s `primary_job`.
- **Bridge to M3:** Section IDs (`#hero`, `#pricing`) map to **M3 A/B Test Agent** variant selectors for DOM experiments.

| Section | Goal | Typical failure |
|---------|------|-----------------|
| Hero | Clarity + CTA | Jargon H1 |
| Proof | Belief | Vague quotes |
| Pricing | Decision | Hidden fees |

## Patterns & Decision Matrix

| Page goal | Structure skew |
|-----------|----------------|
| Lead capture | Short, form above fold on desktop |
| Trial start | Product GIF + steps |
| Webinar | Date block + agenda + speaker proof |
| Book demo | Calendar embed + qualification bullets |

**Navigation**

| Choice | When |
|--------|------|
| No top nav | Single-minded conversion |
| Minimal header | Logo + login only |
| Full nav | Only if SEO page doubles as site page |

## Code Examples

**1) Semantic section outline (HTML)**

```html
<main>
  <section id="hero" aria-labelledby="hero-h1">
    <h1 id="hero-h1">Cut invoice processing time by 40%</h1>
    <p class="subhead">…</p>
    <a class="cta-primary" href="#signup" data-variant="control">Start free trial</a>
  </section>
  <section id="proof" data-analytics-section="social_proof">…</section>
  <section id="faq">…</section>
</main>
```

**2) Stitch / design handoff checklist (Markdown)**

```markdown
## LP — Q2 campaign
- Frame: Desktop 1440 / Mobile 390
- Components: Hero, LogoStrip, FeatureGrid, Testimonial, PricingCard, FAQ
- Embed: M1 tool `/tools/roi-calculator` — iframe height 520px
- Experiments: M3 ticket EXP-1042 — hero headline only
```

## Anti-Patterns

- **Multiple competing CTAs** of equal weight—splits intent.
- **Wall of text** before first CTA on mobile.
- **Stock photo** that contradicts product reality.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Nielsen Norman Group — Landing pages](https://www.nngroup.com/topic/landing-pages/) — scanning behavior
- [Google Ads — Landing page experience](https://support.google.com/google-ads/answer/2404197) — quality factors
- [WebAIM — WCAG quick reference](https://www.webaim.org/resources/quickref/) — accessible headings/CTAs
- [Schema.org — WebPage](https://schema.org/WebPage) — markup for SEO snippets
