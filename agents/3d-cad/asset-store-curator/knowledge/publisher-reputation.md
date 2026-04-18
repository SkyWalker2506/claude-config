# Publisher Reputation Signals

## Reputation Scoring Signals

### Signal 1: Review Count & Rating
- **High confidence:** 500+ reviews, 4.5+ rating
- **Medium confidence:** 100-499 reviews, 4.0+ rating
- **Low confidence:** <100 reviews OR <4.0 rating

Caveat: Older assets (2014-2016) may have fewer reviews but solid reputation.

### Signal 2: Years Active & Update Frequency
- **Actively maintained:** Update within last 2 months
- **Recent maintenance:** Update within last 6 months
- **Stale:** No update in 12+ months (risky for current Unity versions)
- **Abandoned:** No update in 18+ months (consider alternatives)

### Signal 3: Response to Reviews
- **Responsive publisher:** Replies within 1 week, addresses bugs
- **Slow publisher:** Replies within 1 month
- **Unresponsive:** No replies to support requests (red flag)

### Signal 4: Dependency on Deprecated APIs
Risk areas:
- PostProcessing Stack V1 (replaced by PostProcess V2, then Volume Framework)
- Old Cinemachine (0.6.2, pre-2.4)
- Legacy Input Manager (replaced by new Input System)
- OnGUI (replaced by UI Toolkit)

Presence in asset = likely abandoned or low-quality.

### Signal 5: Cross-Marketplace Presence
- Published on multiple platforms (Asset Store + Gumroad + own store) = serious vendor
- Asset Store only = good indicator of commitment to Unity ecosystem
- Single old version everywhere = probably abandoned

### Signal 6: Community Forks & Trust Indicators
- GitHub stars/forks (if open-source)
- Presence in production games (search "made with X")
- Recommended by established studios/educators
- Inclusion in official Unity packages (e.g., NGUI, TextMesh Pro)

## Top 20 Trusted Publishers

| Publisher | Specialty | Est. Years | Reputation |
|-----------|-----------|-----------|-----------|
| Synty Studios | 3D Art, Characters (POLYGON series) | 8+ | Gold standard |
| POLYGON by Synty | 3D Models, stylized | 4+ | Excellent |
| Amplify Creations | Post-processing, shaders | 10+ | Gold standard |
| Opsive | Character controllers, networking | 8+ | AAA-ready |
| Kinematic Soup | Physics, vehicles, mechanics | 6+ | Solid, responsive |
| NGUI Ninja (Tasharen Entertainment) | UI, networking, tweening | 12+ | Historic reliability |
| Michsky | UI, themes, components | 7+ | Very active |
| Jean Moreno | Shaders, post-effects | 8+ | Highly respected |
| Kripto289 | 3D art, environments | 6+ | Quality-focused |
| Unluck Software | General purpose tools | 5+ | Reliable |
| Beffio | 3D models, assets | 5+ | Consistent quality |
| FImpossible Creations | Animation, VFX, shaders | 7+ | Advanced techniques |
| Dustyroom | Game mechanics, puzzle systems | 4+ | Niche expert |
| Ookii Tsuki | UI, UX components | 3+ | Emerging, responsive |
| Code Stage | Utilities, debugging tools | 6+ | Developer-focused |
| Dinopunch | Character rigs, animations | 5+ | Strong in 3D |
| Lovatto Studio | 3D art, characters | 4+ | Contemporary quality |
| SICS Games | Complete game systems | 3+ | Growing reputation |
| WeatherMaker | Weather & atmosphere VFX | 5+ | Specialized |
| ARTnGAME | 3D assets, realistic models | 6+ | Good coverage |

## Red Flags (Avoid These Publishers)

- **No published games:** New publisher, unproven
- **Negative reviews trend:** "Breaks in new Unity" repeated
- **Support ticket backlog:** "Emailed 6 months ago, no response"
- **Asset delisting:** Publisher pulling old versions, selling new ones
- **One-star reviews with specifics:** "Doesn't work with URP", "Won't load", "Scam"
- **Company website down/inactive:** May be defunct

## Reputation Check Workflow

When considering an unknown publisher:
1. Check Asset Store rating (target: 4.0+, 100+ reviews)
2. Scan recent reviews for common complaints
3. Check last update date (target: <6 months)
4. Google "{PublisherName} abandoned" or "{AssetName} broken"
5. If available, visit publisher's website/forum for activity
6. Ask in Unity forums: "Anyone using {Asset}? Still good in 2026?"
