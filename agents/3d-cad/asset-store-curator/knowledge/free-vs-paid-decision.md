# Free vs Paid Decision Framework

## Decision Matrix

| Scenario | Free Asset | Paid Asset | Recommendation |
|----------|-----------|-----------|-----------------|
| **Prototype / Proof of Concept** | Good | Overkill | Free (1-2 weeks) |
| **Proof of Concept → Production** | Risk | Safety | Migrate to paid if foundation weak |
| **Long-term Maintenance** | High risk | Medium risk | Paid (vendor support > DIY fixes) |
| **Niche Requirement** | Often missing | Often available | Paid (specialization) |
| **Bleeding-Edge Feature** | Rare | Common | Paid (actively maintained) |
| **Support/SLA Needed** | None | $50-300+/yr | Paid (business critical) |
| **Learning Asset** | Good | OK | Free (experimental) |
| **Production Shipping** | Medium risk | Low risk | Paid (quality + stability) |

## When Free Assets Are "Good Enough"

1. **Rapid prototyping** — iteration > polish
2. **Learning/experimentation** — exploring features
3. **Indie solo/small team** — budget constraint
4. **Non-commercial projects** — educational, hobby
5. **Utilities & tools** — low risk of abandonment (simple, focused)
6. **Popular community assets** — hundreds of forks/watchers = implicit maintenance

### Red Flags (Free)
- Last update > 18 months ago
- No Unity 6 / 2024+ mention
- Single-author, no forum activity
- Negative reviews citing "abandoned"
- Deprecated APIs (PostProcessingV1, old Cinemachine)

## When Paid Assets Pay Off

1. **Production deadline** — time saved > asset cost
2. **Specialized domain** (e.g., procedural generation, networking) — expert implementation
3. **Support needed** — vendor SLA + bug fixes guaranteed
4. **Ecosystem dependency** — publisher actively maintains (e.g., Amplify Creations)
5. **Asset churn risk** — licensed, versioned, less likely to be delisted

### Quality Signals (Paid)
- 4.5+ rating with 500+ reviews
- Regular updates (monthly/quarterly)
- Active developer forum
- Multiple render pipelines supported (URP/HDRP/Built-in)
- Clear dependency list + compatibility matrix

## Price Bands

| Band | Cost | Typical Use | Examples |
|------|------|-----------|----------|
| **Trivial** | $0-5 | Single component, utility | Coroutine helpers, UI tweens |
| **Small** | $5-20 | Focused feature pack | Texture pack (100+ textures), animation bundle |
| **Mid** | $20-80 | Substantial system | Character rig + animations, networking library |
| **Investment** | $80-300 | Production-grade system | Full game template, AAA-quality character package |
| **Enterprise** | $300+ | Specialized services | Physics middleware (Havok), AI (Wwise) |

## Asset Churn Risk

Free assets: Higher churn (publisher may stop supporting, links die, assets delisted).
Mitigation: Download and version-control critical free assets.

Paid assets: Lower churn (Unity enforces retention policies for published assets).
Trust tier: Synty Studios > Kinematic Soup > Smaller vendors.

## SLA & Support

**Free:** Community forums, GitHub issues, luck.
**Paid ($20-80):** Email support, bug fix timeline ~2 weeks.
**Paid ($80+):** Priority support, feature requests, integration assistance.

## Migration Cost (Free → Paid)

If upgrading from free to paid for production:
- Code refactor cost: low (usually drop-in replacement)
- Learning curve: medium (new API)
- Performance risk: low (paid assets vetted)
- Estimated effort: 2-4 hours for mid-sized game

### Example
Free asset: SimpleMovement (custom input handler).
Paid upgrade: Rewired (comprehensive input system, $30).
Effort: 2 hours to remap controls.
Payoff: Gamepad support, action-based input, cross-platform.
