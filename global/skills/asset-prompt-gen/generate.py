#!/usr/bin/env python3
"""Generate standardized asset prompts (idle + 4 separate strip prompts) from a project config.

Strategy: instead of one 4×8 mega-sheet (which models often render as 5×8 or 5×9),
we produce FOUR independent 2048×256 horizontal strips (one per direction).
After all 4 are generated, the user runs `stitch.py` to assemble them into the final 2048×1024 sheet.

This gives:
  - Reliable 1-row layout (no 5th-row hallucination)
  - Independent identity per row (each prompt has full reference + identity)
  - Easy re-roll of just one row instead of the whole sheet
"""
import json
import sys
import pathlib

# ────────────────────────────────────────────────────────────────────────────
# Universal blocks
# ────────────────────────────────────────────────────────────────────────────

RENDERING_LOCK = """[RENDERING LOCK — CRITICAL]
Output medium: clean digital illustration with hard-edge cel-shading. NOT pixel art (NO visible pixels, NO 8-bit chunkiness, NO 16-bit retro look, NO blocky scaling artifacts). NOT 3D rendered. NOT painterly. NOT anime cel.
Camera direction: see CAMERA/DIRECTION LOCK above — it is the absolute source of truth for view angle. Do NOT default to a generic 3/4 front view if CAMERA/DIRECTION LOCK requests back, side, or any other angle.
Accent enforcement: every visible accent highlight (cyan/orange/red etc.) is a 100% solid flat-fill shape with hard outline. NO inner gradient, NO outer halo, NO glow radius, NO light bleed onto adjacent metal. Reads as solid paint or sealed glass, NEVER emitted light."""

BG_RULE = """[BACKGROUND LOCK — STRICT]
PRIMARY CHOICE: Use solid pure magenta #FF00FF as a flat uniform fill across the entire canvas outside the subject silhouette. This is the default — use it unless your model can guarantee true alpha transparency.
SECONDARY CHOICE (only if true alpha is guaranteed): fully transparent alpha 0.
NO gradient, NO spotlight, NO vignette, NO floor, NO ground plane, NO ground shadow, NO contact shadow, NO atmospheric haze, NO multi-color background, NO grid lines, NO cell separator lines, NO border around cells, NO background objects, NO sky, NO terrain.
The post-processing pipeline strips magenta to transparent — clean uniform magenta is fully acceptable and preferred."""

LAYOUT_LOCK_STRIP = """[LAYOUT LOCK — CRITICAL, NO EXCEPTIONS]
Canvas size MUST be exactly 2048×256 pixels (wide horizontal strip).
Layout MUST be exactly 1 row × 8 columns = 8 cells total.
Each cell is exactly 256×256 pixels, 0px gutter (cells touch directly).
Do NOT create a second row. Do NOT add extra frames. Do NOT add margins.
Do NOT add labels, frame numbers, grid lines, borders, separators, or empty cells.
If you cannot fit the animation into 8 cells, simplify the poses — DO NOT add more cells.
Subject must be perfectly centered in each 256×256 cell (no horizontal drift, no vertical drift)."""

STRICT_NEGATIVES_STRIP = """[STRICT NEGATIVES — NO EXCEPTIONS]
NO wrong camera angle — the view direction specified in CAMERA/DIRECTION LOCK is ABSOLUTE. If BACK VIEW, the face MUST NOT be visible; if FRONT VIEW, the back MUST NOT be visible; if SIDE VIEW, the subject MUST be in profile. Defaulting to 3/4 front view when back/side is requested = WRONG output, reject and re-render.
NO ground shadow under subject. NO ground plane, NO floor, NO horizon, NO ground fog.
NO bloom, NO soft glow, NO neon, NO emitted light, NO accent halo, NO eye glow radius, NO inner light bleed on metal — accents are 100% FLAT solid-fill shapes that read like sealed glass or paint, NEVER like emitting bulbs.
NO pixel art look, NO 8-bit, NO chunky low-res. NO scale variation between cells. NO horizontal/vertical drift (treadmill style — subject stays centered in every cell).
NO TEXT OF ANY KIND rendered into the image — this includes cell numbers (1, 2, 3...), frame indices, labels, captions, watermarks, signatures, prompt fragments, or annotations under or beside any cell. The cell numbering is for prompt structure ONLY and must NOT appear visually. If you see "1", "2", or any digit/letter painted in the image, the output is REJECTED.
NO border, NO grid lines, NO cell separators. NO 2nd row, NO extra cells — STRICTLY 1 row × 8 columns = 8 cells total."""

STRICT_NEGATIVES_IDLE = """[STRICT NEGATIVES]
NO ground shadow, NO floor, NO gradient backdrop. NO bloom, NO soft glow, NO neon. NO pixel art, NO 3D render, NO photorealistic. NO chibi, NO cute big eyes, NO cartoon expression. NO text, NO watermark, NO border."""

# ────────────────────────────────────────────────────────────────────────────
# Frame breakdowns
# ────────────────────────────────────────────────────────────────────────────

def frames_quadruped(direction):
    # Diagonal directions reuse cardinal back/front frames; angle is locked in view_label.
    if direction == "UP_RIGHT": direction = "UP"
    if direction == "DOWN_RIGHT": direction = "DOWN"
    if direction == "UP":
        return [
            "F1 contact: right-front + left-back paws forward in planted stride phase, body slightly raised, tail-stub up, robot seen from BEHIND with rear-end and back of head visible.",
            "F2 lift-off: front-left and rear-right paws enter lifted stride phase, body lowering slightly mid-stride.",
            "F3 high-pass: left-front and right-back paws at highest lifted stride phase, opposite pair in planted stride phase, body at lowest bob point.",
            "F4 contact mirrored: left-front + right-back paws in planted stride phase, opposite pair in lifted stride phase behind, body rising.",
            "F5 passing: right-front and left-back paws beginning lifted stride phase again, body neutral.",
            "F6 high-pass mirrored: right-front and left-back paws at highest lifted stride phase, body at low bob.",
            "F7 pre-contact: right-front and left-back descending toward planted stride phase, body rising.",
            "F8 transition: settling back into F1 pose, completing seamless loop.",
        ]
    if direction == "DOWN":
        return [
            "F1 contact: front-right paw forward, robot seen from FRONT (face/optic toward camera), front-left paw back, head visible.",
            "F2 lift: front-left paw rising forward, body lowering slightly.",
            "F3 high-pass: front-left at peak forward, front-right in planted stride phase, body at low bob.",
            "F4 contact mirrored: front-left lands forward, front-right enters lifted stride phase, body rising.",
            "F5 passing: front-right enters lifted stride phase forward again, body neutral.",
            "F6 high-pass: front-right at peak forward, body low bob.",
            "F7 pre-contact: front-right descending toward planted stride phase, body rising.",
            "F8 transition: settling, seamless loop.",
        ]
    return [
        "F1 contact: SIDE view facing screen-RIGHT, right-front + left-back legs forward in planted stride phase.",
        "F2 lift: front-left and rear-right paws in lifted stride phase, body dipping.",
        "F3 high-pass: front-left at highest lifted stride phase forward, body lowest bob, cables sway.",
        "F4 contact mirrored: left-front + right-back in planted stride phase forward.",
        "F5 passing: right-front enters lifted stride phase forward, body rising.",
        "F6 high-pass mirrored: right-front at highest lifted stride phase forward, body low.",
        "F7 pre-contact: right-front descending toward planted stride phase, body rising.",
        "F8 transition: returning to F1, seamless loop.",
    ]

def frames_biped(direction):
    if direction == "UP_RIGHT": direction = "UP"
    if direction == "DOWN_RIGHT": direction = "DOWN"
    if direction == "UP":
        return [
            "F1 contact: right leg forward, left leg back, robot seen from BEHIND (back of head, shoulders visible), arms swing opposite of legs.",
            "F2 passing: left leg lifting forward, right leg straight, weight on right.",
            "F3 airborne: peak stride, both feet barely off the surface, body lift.",
            "F4 descent: left foot descending, body lowering.",
            "F5 contact mirrored: left leg forward, right back.",
            "F6 passing mirrored: right leg lifting forward.",
            "F7 airborne mirrored.",
            "F8 descent: right foot descending, return to F1.",
        ]
    if direction == "DOWN":
        return [
            "F1 contact: right leg forward, left back, robot facing CAMERA (face, chest, visor visible), arms swing opposite.",
            "F2 passing: left leg lifting, weight on right.",
            "F3 airborne: peak stride, body lifted.",
            "F4 descent: left foot landing.",
            "F5 contact mirrored: left forward, right back.",
            "F6 passing mirrored.",
            "F7 airborne mirrored.",
            "F8 descent: right landing, return to F1.",
        ]
    return [
        "F1 contact: SIDE view facing RIGHT, right leg forward, left back.",
        "F2 passing: left leg lifting forward, body rises, antenna trails.",
        "F3 airborne: peak forward stride.",
        "F4 descent: left foot landing forward.",
        "F5 contact mirrored: left leg forward.",
        "F6 passing mirrored.",
        "F7 airborne mirrored.",
        "F8 descent return to F1.",
    ]

def frames_hover(direction):
    if direction == "UP_RIGHT": direction = "UP"
    if direction == "DOWN_RIGHT": direction = "DOWN"
    if direction == "UP":
        return [
            "F1 neutral hover: robot seen from BEHIND (back of disc/chassis), level, thruster down.",
            "F2 tilt-into-screen: leans forward into screen 8°, thruster angled toward camera, exhaust forms behind.",
            "F3 peak forward lean: full forward tilt, body angled away from camera.",
            "F4 holding: tilt held, motion implied by exhaust.",
            "F5 peak motion: deepest into-screen lean.",
            "F6 easing: tilt reduces, body straightening.",
            "F7 re-leveling.",
            "F8 return to neutral hover, seamless loop.",
        ]
    if direction == "DOWN":
        return [
            "F1 neutral hover: facing CAMERA, level, thruster down.",
            "F2 tilt-toward-camera: leans forward toward viewer 8°.",
            "F3 peak forward lean: full tilt toward viewer.",
            "F4 holding tilt.",
            "F5 peak motion.",
            "F6 easing.",
            "F7 re-leveling.",
            "F8 return neutral, seamless loop.",
        ]
    return [
        "F1 neutral hover: SIDE view facing RIGHT, level.",
        "F2 tilt-right: forward lean 8°, thruster exhaust trails leftward.",
        "F3 peak forward lean: full tilt right.",
        "F4 holding tilt.",
        "F5 peak motion.",
        "F6 easing back.",
        "F7 leveling.",
        "F8 return to neutral, seamless loop.",
    ]

def frames_idle_directional(form, direction):
    """Idle frames for IDLE_UP_RIGHT (back-3/4 stationary) and IDLE_DOWN_RIGHT (front-3/4 stationary)."""
    is_back = direction == "IDLE_UP_RIGHT"
    view_word = "BACK-RIGHT 3/4 stationary view (rear/back end and subject's left flank visible, face hidden)" if is_back else "FRONT-RIGHT 3/4 stationary view (face/optic and subject's left flank visible, rear hidden)"
    if form == "quadruped":
        return [
            f"F1 planted neutral: {view_word}, all four paws planted, head forward, body settled.",
            "F2 weight shift right: subtle sway to right legs, head tilts slightly, ear-antenna twitch.",
            "F3 micro accent flicker: visible accent shape briefly brighter (still flat shape, same proportions); tail-stub micro-flick." if not is_back else "F3 ear-antenna twitch: subtle head dip, tail-stub micro-flick. NO front accent visible.",
            "F4 settling back to neutral.",
            "F5 weight shift left: sway to left legs, head tilts opposite.",
            "F6 ear-antenna twitch on opposite side, cables sway slightly.",
            "F7 micro-bob: chest/back dips 2px (breathing), body rises gently.",
            "F8 return to F1, seamless loop.",
        ]
    if form == "biped":
        return [
            f"F1 ready stance: {view_word}, slight knee bend, weight centered, arms at sides.",
            "F2 weight shift right: hip cocks right, head scans slightly.",
            "F3 micro accent flicker: visible accent shape briefly brighter." if not is_back else "F3 head dip and shoulder roll: subtle relaxed motion. NO front accent visible.",
            "F4 returning to neutral.",
            "F5 weight shift left: hip cocks left.",
            "F6 arm micro-twitch, antenna sway.",
            "F7 subtle breathing rise: chest/back plate lifts 2px.",
            "F8 return to F1, seamless loop.",
        ]
    return [
        f"F1 neutral hover height: {view_word}, level, thruster steady.",
        "F2 rises 4px: hover ascent.",
        "F3 peak height: thruster exhaust micro-puff trailing behind/below.",
        "F4 descending: hover dipping.",
        "F5 low point.",
        "F6 micro accent flicker on visible side." if not is_back else "F6 thruster pulse: subtle exhaust variation. NO front accent visible.",
        "F7 rising again toward neutral.",
        "F8 return to F1, seamless loop.",
    ]

def frames_idle(form):
    if form == "quadruped":
        return [
            "F1 planted neutral: front view, all four paws planted, head forward, optic flat lit.",
            "F2 weight shift right: subtle sway to right legs, head tilts left, ear-antenna twitch.",
            "F3 optic flicker: accent momentarily brighter (still flat shape), tail-stub micro-flick.",
            "F4 settling back to neutral.",
            "F5 weight shift left: sway to left legs, head tilts right.",
            "F6 ear-antenna twitch on opposite side.",
            "F7 micro-bob: chest dips 2px (breathing).",
            "F8 return to F1, seamless loop.",
        ]
    if form == "biped":
        return [
            "F1 ready stance: front view, slight knee bend, weight centered.",
            "F2 weight shift right: hip cocks right, head scans left.",
            "F3 visor flicker: accent momentarily brighter.",
            "F4 returning to neutral.",
            "F5 weight shift left: hip cocks left.",
            "F6 arm micro-twitch.",
            "F7 subtle breathing rise: chest plate lifts 2px.",
            "F8 return to F1, seamless loop.",
        ]
    return [
        "F1 neutral hover height: front view, level, thruster steady.",
        "F2 rises 4px: hover ascent.",
        "F3 peak height: thruster exhaust micro-puff.",
        "F4 descending: hover dipping.",
        "F5 low point.",
        "F6 core/optic flicker.",
        "F7 rising again toward neutral.",
        "F8 return to F1, seamless loop.",
    ]

def view_label(direction):
    return {
        "UP": (
            "STRICT BACK VIEW — camera is positioned BEHIND and ABOVE the subject (back 3/4 isometric, 45° down).\n"
            "VISIBLE: back of head, back of body/chassis, rear/tail end, top planes, rear-facing leg motion, rear cable bundles.\n"
            "HIDDEN: face, eyes, optic, visor, front snout/face area, front chest details. The accent (cyan/orange/etc.) identity STILL belongs to the character but it is NOT drawn in this strip because the camera does not see the front of the subject.\n"
            "If face/eye/optic/visor is visible in any cell → output is WRONG.\n"
            "Walking direction: INTO the screen (away from viewer)."
        ),
        "DOWN": (
            "STRICT FRONT VIEW — camera is positioned IN FRONT of and ABOVE the subject (front 3/4 isometric, 45° down).\n"
            "VISIBLE: face, optic/eyes/visor, chest, front of body, front-facing leg motion. The accent shape (cyan/orange) MUST match the reference image exactly in shape and size.\n"
            "HIDDEN: back of head, tail, rear chassis.\n"
            "If back/tail is visible in any cell → output is WRONG.\n"
            "Walking direction: OUT of the screen (toward viewer)."
        ),
        "RIGHT": (
            "STRICT SIDE VIEW — camera is positioned to the LEFT side of the subject (side 3/4 isometric, slight elevation).\n"
            "VISIBLE: left flank/profile of body, ONE eye/optic in profile, leg motion in profile. The visible accent shape must match the reference image in proportion.\n"
            "HIDDEN: opposite (right) flank.\n"
            "If subject faces toward or away from camera → output is WRONG.\n"
            "Walking direction: RIGHTWARD across the screen."
        ),
        "IDLE": (
            "STRICT FRONT VIEW (stationary) — camera IN FRONT and ABOVE (front 3/4 isometric, 45° down).\n"
            "VISIBLE: face, optic/visor, chest, full front view. Accent shape must match reference exactly.\n"
            "HIDDEN: back/rear.\n"
            "Subject stationary in place — only subtle weight shifts, accent flicker, breathing micro-bob. NO traveling motion."
        ),
        "IDLE_UP_RIGHT": (
            "STRICT BACK-RIGHT 3/4 ISOMETRIC IDLE (stationary) — camera is BEHIND-AND-LEFT of the subject, looking down at 45°.\n"
            "Subject is standing still, oriented toward the UPPER-RIGHT corner (NE in iso world) — same orientation it would have when walking NE.\n"
            "VISIBLE: back of head and body, the subject's LEFT flank/side, rear/back end, top planes.\n"
            "HIDDEN: face, eyes, optic, visor, front snout/face area, front chest, the subject's RIGHT flank.\n"
            "If face/eye/optic is visible → output is WRONG.\n"
            "Subject stationary — only subtle weight shifts, ear/antenna twitch, breathing micro-bob, tail/cable sway. NO traveling motion.\n"
            "Note: this strip will be horizontally flipped at runtime to produce idle-up-left (NW)."
        ),
        "IDLE_DOWN_RIGHT": (
            "STRICT FRONT-RIGHT 3/4 ISOMETRIC IDLE (stationary) — camera is IN-FRONT-AND-LEFT of the subject, looking down at 45°.\n"
            "Subject is standing still, oriented toward the LOWER-RIGHT corner (SE in iso world) — same orientation it would have when walking SE.\n"
            "VISIBLE: face, optic/eyes/visor, front of body, chest, the subject's LEFT flank/side. Accent shape MUST match reference exactly.\n"
            "HIDDEN: back of head, rear, the subject's RIGHT flank.\n"
            "If back/rear is visible → output is WRONG.\n"
            "Subject stationary — only subtle weight shifts, accent flicker, breathing micro-bob. NO traveling motion.\n"
            "Note: this strip will be horizontally flipped at runtime to produce idle-down-left (SW)."
        ),
        # Diagonal isometric directions (preferred for true 3/4 iso games — Diablo/PoE style).
        # Only NE + SE need to be drawn; NW and SW are runtime horizontal flips.
        "UP_RIGHT": (
            "STRICT BACK-RIGHT 3/4 ISOMETRIC VIEW — camera is BEHIND-AND-LEFT of the subject, looking down at 45°.\n"
            "Subject's body axis points to the UPPER-RIGHT corner of the screen (NE in iso world). Body is rotated ~30° clockwise from a pure rear view, NOT a pure-side profile and NOT a rear-only view.\n"
            "VISIBLE: back of head and body, the LEFT flank/side of the subject (subject's own left side faces camera), rear/back end, top planes, leg motion on the visible side.\n"
            "HIDDEN: face, eyes, optic, visor, front snout/face area, front chest, the subject's RIGHT flank.\n"
            "ANTI-SIDE-PROFILE LOCK: this is NOT a side view (subject silhouette must NOT read as a flat horizontal profile facing screen-right). The body has clear depth/foreshortening — back is partially toward camera, head is upper-right of body. If silhouette is a flat side profile (legs walking strictly screen-right with no back-toward-camera), output is WRONG.\n"
            "If face/eye/optic is visible → output is WRONG.\n"
            "Movement vector: diagonal up-right, away from viewer.\n"
            "Note: this strip will be horizontally flipped at runtime to produce up-left (NW)."
        ),
        "DOWN_RIGHT": (
            "STRICT FRONT-RIGHT 3/4 ISOMETRIC VIEW — camera is IN-FRONT-AND-LEFT of the subject, looking down at 45°.\n"
            "Subject's body axis points to the LOWER-RIGHT corner of the screen (SE in iso world). Body is rotated ~30° clockwise from a pure front view, NOT a pure-side profile and NOT a pure-front view.\n"
            "VISIBLE: face, optic/eyes/visor, front of body, chest, the subject's LEFT flank/side (subject's own left side faces camera), front leg motion. Accent shape MUST match reference exactly.\n"
            "HIDDEN: back of head, rear/tail, rear chassis, the subject's RIGHT flank.\n"
            "ANTI-SIDE-PROFILE LOCK: this is NOT a side view (silhouette must NOT read as a flat horizontal profile). The body has clear depth — face is partially toward camera, chest is lower-right of head. If silhouette is a flat side profile (legs walking strictly screen-right with face in pure profile), output is WRONG.\n"
            "If back/rear is visible → output is WRONG.\n"
            "Movement vector: diagonal down-right, toward viewer.\n"
            "Note: this strip will be horizontally flipped at runtime to produce down-left (SW)."
        ),
    }[direction]

# ────────────────────────────────────────────────────────────────────────────
# Builders
# ────────────────────────────────────────────────────────────────────────────

def get_walk_fn(form):
    return {
        "quadruped": frames_quadruped,
        "biped": frames_biped,
        "hover-orb": frames_hover,
        "hover-x": frames_hover,
    }.get(form, frames_biped)

def render_cells(frames):
    return "\n".join(f"  Cell {i}: {f}" for i, f in enumerate(frames, 1))

def build_idle_prompt(item, master_style, project, asset_browser_url, tag):
    return f"""# {item['name']} — Idle Hero (256×256)

```
PROMPT START

OUTPUT SPEC: Generate a 256x256 PNG, 8px padding all sides, subject perfectly centered.

[ART STYLE — MANDATORY]
{master_style}

{RENDERING_LOCK}

{BG_RULE}

[SUBJECT — {item['name'].upper()}]
{item['identity']}

Pose: alert idle, balanced stance, expression serious / utilitarian (NOT cute, NOT chibi).

Lighting: top-left key light, hard-edged two-tone shading on the body. NO ambient occlusion gradient, NO rim glow.

{STRICT_NEGATIVES_IDLE}

PROMPT END
```
"""

def build_strip_prompt(item, direction_label, direction_key, frames_list,
                       master_style, project, asset_browser_url, tag):
    """Build a single 2048×256 strip prompt for one direction (Walk-Up / Walk-Down / Walk-Right / Idle)."""
    ref_url = f"{asset_browser_url}/assets/{tag}/{item['id']}_idle.webp"
    motion_word = "HOVER-GLIDE" if item["form"].startswith("hover") else "WALK"
    motion_label = "IDLE" if direction_key == "IDLE" else f"{motion_word} {direction_key}"

    # View-aware accent rule: only enforce "match reference shape" when the accent IS visible from this angle
    if direction_key == "UP":
        accent_rule = (
            "ACCENT VISIBILITY (this strip): the subject's front-facing accent (cyan/orange optic/visor/core) "
            "is part of the character identity but is HIDDEN in this back-view strip — DO NOT draw any front-facing "
            "eye, optic, or visor. Only rear-side accents (if any exist on the back of the chassis in the reference) "
            "are visible. If you see any front-facing accent in your output, the angle is wrong."
        )
    else:
        accent_rule = (
            "ACCENT VISIBILITY (this strip): the subject's accent shape (cyan/orange optic/visor/core) IS visible in this view.\n"
            "ACCENT SHAPE LOCK — match the reference image PIXEL-FOR-PIXEL:\n"
            "  - Look at the reference idle image. Identify the exact accent shape (round dot? horizontal slit? rectangular visor? hexagonal core?).\n"
            "  - Whatever shape and proportion the reference has, EVERY one of the 8 cells must reproduce that exact shape and size (±10% tolerance).\n"
            "  - If reference shows a SMALL ROUND DOT (single round optic, ~10-15% of head width), do NOT widen it into a horizontal slit, do NOT split it into two eyes, do NOT add a face plate.\n"
            "  - If reference shows a WIDE HORIZONTAL SLIT (visor band), do NOT shrink it to a dot.\n"
            "  - NO shape mutation between cells, NO new face screens, NO upgraded visors, NO additional accent shapes that aren't in the reference."
        )

    # Form-specific gait language for FRAME DELTA RULE
    gait_word = {
        "quadruped": "quadruped walking",
        "biped": "bipedal walking",
        "hover-orb": "hovering glide-motion",
        "hover-x": "hovering glide-motion",
    }.get(item["form"], "walking")

    # Back-view-only: clarify left/right leg labels are from robot's anatomy, not viewer
    leg_clarification = ""
    if direction_key == "UP":
        leg_clarification = (
            "\n[BACK-VIEW LEG NAMING CLARIFICATION]\n"
            "Because this is a rear/back-view strip, leg labels (\"right-front\", \"left-back\", etc.) describe "
            "the robot's OWN anatomy, NOT the viewer's left/right. The robot is walking AWAY from the viewer. "
            "Keep anatomical right/left consistent across all frames. Do NOT rotate the character toward the "
            "camera to show legs more clearly — the back-view orientation must hold for every cell.\n"
        )

    return f"""## {item['name']} — {direction_label} Strip (2048×256)

```
PROMPT START

[REFERENCE IMAGE — IDENTITY SOURCE]
Reference URL: {ref_url}

This image is the official {project} {item['name']} idle hero shot. Match its proportions, palette, outline weight, mechanical detail, material language, silhouette, chassis shape, leg construction, antennae, cables, rust pattern logic, and overall identity. Treat the reference as single source of truth — if any text below conflicts with the image, the IMAGE wins.

[IDENTITY LOCK]
{item['identity']}

{accent_rule}

[CAMERA / DIRECTION LOCK — MOST IMPORTANT]
This is a {motion_label} strip.
{view_label(direction_key)}

OUTPUT SPEC: Generate a single 2048x256 PNG horizontal sprite strip showing one complete {motion_label} cycle.

{LAYOUT_LOCK_STRIP}

{BG_RULE}

[ART STYLE — MANDATORY]
{master_style}

[STYLE OVERRIDES]
- Background: ignore any "transparent background" mentioned in the art style above; background follows BACKGROUND LOCK only (solid magenta #FF00FF preferred).
- Camera angle: ignore any default "3/4 view" wording in the art style; the active camera is defined exclusively by CAMERA/DIRECTION LOCK above.

{RENDERING_LOCK}

[ANIMATION SEQUENCE — 8 FRAMES, LEFT TO RIGHT]
Render each of the 8 cells exactly as described:
{render_cells(frames_list)}
{leg_clarification}
[POSE BLUEPRINT — explicit per-cell leg/body deltas]
Use these concrete deltas (subject-relative, NOT viewer-relative). Apply to whichever leg pair is the lead — for quadrupeds, the diagonal pair (right-front + left-back) leads first half, then mirror.
- Cell 1: lead leg PLANTED forward at maximum stride extension (subject's front-lead leg ~30° forward of vertical). Body at LOW point of bob.
- Cell 2: lead leg passing under body, lifting (~10° forward, knee bent). Trailing leg pushing back. Body rising.
- Cell 3: lead leg at HIGHEST lifted phase (~20° behind vertical, foot tucked under hip). Body at HIGH point of bob (+5px vs Cell 1).
- Cell 4: lead leg descending forward, trailing leg passing under body. Body lowering.
- Cell 5: MIRROR of Cell 1 — opposite-side leg now planted forward at max extension. Body LOW. Cell 1 vs Cell 5 must be visibly mirror-opposite poses.
- Cell 6: mirror of Cell 2 (other leg lifting under body). Body rising.
- Cell 7: mirror of Cell 3 (other leg at highest lifted phase). Body HIGH.
- Cell 8: mirror of Cell 4, settling back toward Cell 1 pose for seamless loop.
Tail/cable/antenna sway: trails OPPOSITE to body bob direction (when body rises, tail dips slightly; when body lowers, tail flicks up). Visible offset between cells.
For idle/hover strips: same Cell 1↔5 mirror principle applies to weight-shift direction (Cell 1 weight on left, Cell 5 weight on right) and accent flicker timing.

[FRAME DELTA RULE — STRICT, ENFORCED]
Each of the 8 cells MUST show a visibly different {gait_word} pose. This is the most common failure mode — do NOT render 8 near-identical copies.
Required differences cell-to-cell:
- Leg/limb positions must visibly change between every adjacent cell pair (Cell N vs Cell N+1).
- Body height (vertical bob) must vary by at least 4-6 pixels across the cycle (low at high-pass frames, high at contact frames).
- Cell 1 vs Cell 5 must be MIRROR-OPPOSITE poses (opposite legs forward) — if they look the same, the strip is broken.
- Cell 3 and Cell 7 are the highest body positions; Cell 1 and Cell 5 are the lowest body positions (or vice-versa, but must differ).
- Tail/cables/antennae positions visibly shift (sway, trail, lift) between cells.
THUMBNAIL TEST: if you scale the strip down to 256×32 and the 8 cells look identical, the strip is REJECTED.
For idle strips: even idle requires per-cell weight-shift, breathing bob, or accent flicker — Cell 1 vs Cell 5 must NOT be pixel-identical.

[CONSISTENCY RULES]
Same character identity, same scale, same palette, same outline thickness, same lighting direction, same camera angle, same view-orientation across ALL 8 frames. NO redesign between frames, NO shape mutation, NO new armor, NO added decorations.

{STRICT_NEGATIVES_STRIP}

[FINAL REJECTION CHECK]
Reject and re-render if ANY of these occur: face/eye/optic/visor visible when CAMERA/DIRECTION LOCK forbids it; front-view or side-view drift away from the requested direction; canvas not exactly 2048×256; layout not exactly 1 row × 8 cells; extra row or extra frame; non-magenta/non-transparent background; ground/floor/shadow/grid/separator/text/watermark visible; character scale or identity changing between frames.

PROMPT END
```
"""

def build_anim_doc(items, master_style, project, asset_browser_url, tag, category_name):
    """Build the full animation MD document — 4 strips per item."""
    walk_fn_cache = {item['id']: get_walk_fn(item["form"]) for item in items}

    doc = f"""# {project.title()} — {category_name.title()}: ANIMATION Strip Prompts

> **Bu dosyanın tepe açıklaması GPT'ye GİTMEZ.** GPT yalnızca her prompt bloğundaki `PROMPT START` ↔ `PROMPT END` arasını görür.

## Strateji: 4 yönlü diagonal isometric (2 walk + 2 idle, NW/SW = runtime flip)

Gerçek 3/4 isometric oyunlarda karakter NE/NW/SE/SW yönlerinde hareket eder. NW = NE'nin horizontal flip'i, SW = SE'nin flip'i — yani 4 yönü kapsamak için sadece **2 gerçek walk + 2 gerçek idle = 4 strip** üretmek yeterli. Karakter durduğunda en son hareket ettiği yöne bakmaya devam eder (kameraya snap geri dönmez).

Her asset için **4 ayrı 2048×256 strip prompt'u**:
- `{{id}}_up_right.webp` (NE walk) → runtime flip → NW walk
- `{{id}}_down_right.webp` (SE walk) → runtime flip → SW walk
- `{{id}}_idle_up_right.webp` (NE idle) → runtime flip → NW idle
- `{{id}}_idle_down_right.webp` (SE idle) → runtime flip → SW idle

Sebep: image gen modelleri 4×8 mega-sheet talebinde sıklıkla 5×8 / 5×9 üretiyor (extra row hallucination). Tek satır 1×8'de bu hata imkansız — model 2. satır ekleyemez.

## Workflow
1. Her strip için **ayrı boş chat** aç (4 chat per asset)
2. İlgili prompt'u kopyala-yapıştır
3. Üretilen 2048×256 PNG'leri indir, asset-browser'a yükle (magenta auto-strip)
4. Oyun kodu 4 strip'i ayrı yükler ve animasyon state'ine göre sırasıyla oynatır

## Avantajları
- 5. satır halüsinasyonu imkansız (1 satır var)
- Tek strip kötü gelirse sadece o yönü re-roll edersin
- Her strip kendi içinde referans + identity lock'lu (bağımsız chat'ler)
- Oyun kodu daha esnek: yön bazlı sprite swap kolay

---

"""

    for item in items:
        walk_fn = walk_fn_cache[item['id']]
        directions = [
            ("Walk Up-Right (NE)", "UP_RIGHT", walk_fn("UP_RIGHT")),
            ("Walk Down-Right (SE)", "DOWN_RIGHT", walk_fn("DOWN_RIGHT")),
            ("Idle Up-Right (NE)", "IDLE_UP_RIGHT", frames_idle_directional(item["form"], "IDLE_UP_RIGHT")),
            ("Idle Down-Right (SE)", "IDLE_DOWN_RIGHT", frames_idle_directional(item["form"], "IDLE_DOWN_RIGHT")),
        ]
        doc += f"\n# {item['name']}\n\n"
        for label, key, frames in directions:
            doc += build_strip_prompt(item, label, key, frames,
                                       master_style, project, asset_browser_url, tag)
            doc += "\n"
        doc += "\n---\n"

    doc += """

## QC CHECKLIST (her strip için)

- [ ] Canvas tam 2048×256 mi? (1 row, 8 col)
- [ ] **2. satır YOK** — modelin halüsinasyon ekleme imkanı yok
- [ ] 8 cell'in her biri birbirinden farklı pose mı?
- [ ] Accent shape reference ile birebir aynı mı? (visor → visor, dot → dot)
- [ ] BG ya tam transparent ya tam uniform magenta #FF00FF mi?
- [ ] Ground shadow yok mu?
- [ ] Robot her cell'de merkezde mi (drift yok)?

## Asset-browser entegrasyonu

4 strip'i tek tek asset-browser'a yükle. İsimlendirme:
- `{robot_id}_up_right.png` → `{robot_id}_up_right.webp` (NE — runtime flip → NW)
- `{robot_id}_down_right.png` → `{robot_id}_down_right.webp` (SE — runtime flip → SW)
- `{robot_id}_idle.png` → `{robot_id}_idle.webp`

Magenta BG asset-browser-upload pipeline'ında otomatik strip edilir.
"""
    return doc

# ────────────────────────────────────────────────────────────────────────────
# PACK MODE — multiple assets in one sprite sheet (icon set, tile set, etc.)
# ────────────────────────────────────────────────────────────────────────────

def build_pack_prompt(category_name, items, layout, master_style, project, tag):
    """Build a single prompt that renders ALL items into one grid sprite sheet.

    layout = {"cols": int, "rows": int, "cell_size": int, "padding": int (optional)}
    Items each have {id, name, description}.
    """
    cols = layout["cols"]
    rows = layout["rows"]
    cell_size = layout["cell_size"]
    padding = layout.get("padding", 0)
    canvas_w = cols * cell_size
    canvas_h = rows * cell_size

    expected = cols * rows
    if len(items) > expected:
        raise ValueError(f"{category_name}: pack has {len(items)} items but layout fits only {expected} ({cols}×{rows})")

    # Build per-cell description map
    cells = []
    for i, item in enumerate(items):
        col = i % cols + 1
        row = i // cols + 1
        cells.append(f"  Cell ({row},{col}) [#{i+1}, id={item['id']}]: {item.get('description', item.get('name'))}")
    # Empty cells (if items < grid)
    for i in range(len(items), expected):
        col = i % cols + 1
        row = i // cols + 1
        cells.append(f"  Cell ({row},{col}) [#{i+1}]: EMPTY — leave fully transparent or solid magenta, no content.")

    return f"""## {category_name.title()} — Pack Sheet ({canvas_w}×{canvas_h}, {cols}×{rows} grid, {cell_size}px cells)

```
PROMPT START

OUTPUT SPEC: Generate a single {canvas_w}×{canvas_h} PNG sprite sheet containing {len(items)} assets in a {cols}-column × {rows}-row grid. Each cell is exactly {cell_size}×{cell_size} pixels with 0px gutter (cells touch directly){', and ' + str(padding) + 'px inner padding inside each cell so the asset does not touch cell edges' if padding > 0 else ''}.

[LAYOUT LOCK — STRICT]
Canvas: exactly {canvas_w}×{canvas_h} pixels.
Grid: exactly {cols} columns × {rows} rows = {expected} cells total.
Each cell: exactly {cell_size}×{cell_size} pixels.
0px gutter between cells.
Do NOT add labels, frame numbers, grid lines, borders, separators, or extra cells.
Each asset perfectly centered inside its {cell_size}×{cell_size} cell.

{BG_RULE}

[ART STYLE — MANDATORY]
{master_style}

[STYLE OVERRIDES]
- Background: ignore any "transparent background" mentioned in the art style above; background follows BACKGROUND LOCK only (solid magenta #FF00FF preferred).
- Camera angle: each asset uses its own natural orientation per description below.

{RENDERING_LOCK}

[ASSET LIST — render each cell exactly as described, left-to-right then top-to-bottom]
{chr(10).join(cells)}

[CONSISTENCY RULES]
- Same outline weight across ALL cells.
- Same lighting direction (top-left key) across ALL cells.
- Same level of detail across ALL cells (don't over-render some, under-render others).
- Each asset readable at its slice size ({cell_size}×{cell_size}).
- Do NOT mix dramatically different art styles between cells.

[STRICT NEGATIVES — NO EXCEPTIONS]
NO ground shadow under any cell. NO cell separator lines, NO grid lines, NO borders. NO bloom, NO soft glow, NO neon. NO pixel art look, NO 8-bit. NO scale variation between cells. NO assets escaping their cell boundaries. NO text labels in cells, NO frame numbers, NO watermark. The grid layout MUST be exactly {cols}×{rows} — no extra cells, no fewer cells.

[FINAL REJECTION CHECK]
Reject and re-render if ANY of these occur: canvas not exactly {canvas_w}×{canvas_h}; grid not exactly {cols}×{rows}; cells not exactly {cell_size}×{cell_size}; non-magenta/non-transparent background; ground/floor/shadow/grid/separator/text/watermark visible; assets bleeding across cell boundaries; inconsistent art style or outline weight between cells.

PROMPT END
```

### Slice notes
After generation, slice the {canvas_w}×{canvas_h} sheet into {expected} individual {cell_size}×{cell_size} cells:
""" + "\n".join([f"- Cell #{i+1} → `{item['id']}.png`" for i, item in enumerate(items)]) + "\n"

# ────────────────────────────────────────────────────────────────────────────
# Mode dispatcher
# ────────────────────────────────────────────────────────────────────────────

def write_single_mode(cat_name, items, master_style, project, asset_browser_url, tag, out_dir, project_root):
    doc = f"# {project.title()} — {cat_name.title()}: Single Asset Prompts\n\nHer prompt ayrı boş chat'e yapıştırılır. Her item kendi PNG'si olarak üretilir.\n\n---\n\n"
    for item in items:
        doc += build_idle_prompt(item, master_style, project, asset_browser_url, tag)
        doc += "\n---\n\n"
    out_path = out_dir / f"{cat_name}_single.md"
    out_path.write_text(doc)
    print(f"  ✓ {out_path.relative_to(project_root)} (single mode, {len(items)} prompts)")

def write_anim4_mode(cat_name, items, master_style, project, asset_browser_url, tag, out_dir, project_root):
    doc = build_anim_doc(items, master_style, project, asset_browser_url, tag, cat_name)
    out_path = out_dir / f"{cat_name}_anim4.md"
    out_path.write_text(doc)
    print(f"  ✓ {out_path.relative_to(project_root)} (anim4 mode, {len(items)} items × 4 strips = {len(items)*4} prompts)")

def write_pack_mode(cat_name, items, master_style, project, tag, layout, out_dir, project_root):
    if not layout:
        print(f"  ⚠ {cat_name}: pack mode requires 'pack_layout' in config — skipped")
        return
    header = f"# {project.title()} — {cat_name.title()}: Pack Sheet Prompt\n\nTüm itemler tek bir grid sprite sheet'te. Sheet üretildikten sonra slice edilir.\n\n---\n\n"
    body = build_pack_prompt(cat_name, items, layout, master_style, project, tag)
    out_path = out_dir / f"{cat_name}_pack.md"
    out_path.write_text(header + body)
    print(f"  ✓ {out_path.relative_to(project_root)} (pack mode, {len(items)} items in 1 sheet)")

# ────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────

DEFAULT_MODES = ["single", "anim4"]

def main():
    if len(sys.argv) < 2:
        print("Usage: generate.py <project_root>", file=sys.stderr)
        sys.exit(1)

    project_root = pathlib.Path(sys.argv[1]).expanduser().resolve()
    config_path = project_root / "art" / "prompts" / "_config.json"
    out_dir = project_root / "art" / "prompts"

    if not config_path.exists():
        print(f"ERROR: config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    config = json.loads(config_path.read_text())
    project = config["project"]
    asset_browser_url = config["asset_browser_url"].rstrip("/")
    master_style = config["master_style"]
    categories = config.get("categories", {})

    out_dir.mkdir(parents=True, exist_ok=True)

    for cat_name, cat in categories.items():
        tag = cat.get("tag", cat_name)
        items = cat.get("items", [])
        modes = cat.get("modes", DEFAULT_MODES)
        pack_layout = cat.get("pack_layout")

        for mode in modes:
            if mode == "single":
                write_single_mode(cat_name, items, master_style, project, asset_browser_url, tag, out_dir, project_root)
            elif mode == "anim4":
                write_anim4_mode(cat_name, items, master_style, project, asset_browser_url, tag, out_dir, project_root)
            elif mode == "pack":
                write_pack_mode(cat_name, items, master_style, project, tag, pack_layout, out_dir, project_root)
            else:
                print(f"  ⚠ {cat_name}: unknown mode '{mode}' — skipped (valid: single, anim4, pack)")

    print(f"\nDone. Output: {out_dir}")
    print(f"Modes available: single (1 PNG/item), anim4 (4 strips/item), pack (1 sheet/category).")

if __name__ == "__main__":
    main()
