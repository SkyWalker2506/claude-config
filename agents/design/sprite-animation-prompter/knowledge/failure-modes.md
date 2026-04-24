# Failure modes (catalogued from real rejections)

## Characters
| Symptom | Root cause | Countermeasure |
|---------|-----------|----------------|
| Head/top-of-helmet cropped | Default composition fills canvas | Explicit pixel margins + height cap (see framing-rules.md) |
| Body pose changes between frames | Prompt didn't lock the body | Add "body IDENTICAL across frames, only {limb} moves, feet anchored at same y" |
| Feet at different y per frame | Anchor implied, not stated | Add: "feet anchored at same pixel y coordinate in every frame" |
| White/gray background despite "transparent" | DALL-E ignores transparent | Use solid MAGENTA (#FF00FF), post-process with magick |
| Anime/manga proportions | Default latent space | Negative: "NO anime, NO manga, NO chibi, NO big eyes" |
| Outlines appearing | Default comic style | Negative: "NO outline, NO line art, NO black edges" |

## Motion
| Symptom | Root cause | Countermeasure |
|---------|-----------|----------------|
| Frames all look identical | Motion too subtle OR prompt vague | Describe each frame separately with a single specific delta |
| No visible motion on rotating object | GPT can't do rotation | FALLBACK: render with ImageMagick rotate + append |
| Sparks/dust inconsistent across frames | FX lacks frame-level direction | Specify F1 base puff, F2 growing, F3 peak, F4 fading - explicit growth curve |
| Motion doesn't loop seamlessly | Last frame not linked to first | Add "F_N is halfway back to F1 for seamless loop" |

## Technical
| Symptom | Root cause | Countermeasure |
|---------|-----------|----------------|
| Frames different widths | Generator doesn't count | State canvas dims AND per-frame dims explicitly. Also state total frame count |
| Dividers appear between frames | Prompt said "separator lines" | Remove that language. Only ask for dividers if you WILL split later |
| Style drift from reference | Sources tab isn't read | Describe style in text: "warm earth tones, hand-drawn painterly, Manor Lords aesthetic" |
| Text/labels on sprite | GPT adds captions | Negative: "NO text, NO labels, NO captions, NO watermarks" |
| Extra features (2 wheels instead of 1) | GPT adds defaults | Explicit: "exactly N wheels visible, do not add more" |

## Project-specific (MedievalFactory)
- GPT Sources tab was tested twice — confirmed ignored.
- Style target: Manor Lords + Kingdom Rush. Always include both names.
- Reference webp filenames (BlackSmithCharacter.webp, MinerCharacter.webp, etc.) must be named in text.
- Fire/particle FX are the only category DALL-E reliably nails without heavy iteration.
