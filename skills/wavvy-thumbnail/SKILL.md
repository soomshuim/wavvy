---
name: wavvy-thumbnail
description: Design and finish Wavvy series video artwork and a typographic YouTube thumbnail. Use automatically during a Wavvy release after the series direction is known, or when the user asks to create or revise a Wavvy thumbnail. For lyric writing use wavvy-lyricist.
---

# Wavvy Thumbnail

Trigger: model-invoked during `wavvy-release` and on Wavvy thumbnail requests. This saves 젠 from starting a separate design task while preserving the visual approval point. The series concept and approved user direction outrank generic design preferences.

## Inputs

Read the target `SERIES/[series]/concept.md`, `wavvy.md`, existing `brand/` assets, and at least two completed Wavvy thumbnails. Read [Taste adaptation](references/taste-adaptation.md) for the transferable visual-design principles. Use the user's supplied reference or image if one exists.

## Steps

1. **Design Read:** State the intended scene, audience, mood, one visual focal point, and short thumbnail copy in one line. Audit the existing Wavvy logo treatment before choosing placement. The default thumbnail does not display a time; use older thumbnails as visual references without copying their time digits. Keep the image concept tied to the actual series, not a generic playlist aesthetic.
2. **Draft:** Make a 16:9 scene image at a review size well below final 4K. Keep title lettering out of the generated scene. Show the draft to 젠 and ask for one visual approval or revision decision. A specific user correction changes the draft brief; repeat the preview only as needed.
3. **After approval:** Produce the final 3840×2160 video background from the approved composition and place the real Wavvy logo on it. The full-length video background contains the scene and Wavvy logo only: no title, BPM, time, or other promotional lettering. This rule applies to every music theme. State whether the pixels came from native generation or enlargement. Separately compose the YouTube thumbnail with the real Wavvy logo and a short title, without time digits in the default format, using a suitable local graphics tool; do not rely on image generation to spell text. Preserve the approved subject, clothing, season, and scene. Never copy or rename the typographic thumbnail into the video input.
4. **Preflight:** Inspect the final image and thumbnail with `view_image` at full size and at a small phone-feed size. Confirm the background's Wavvy logo is visible and title/BPM/other overlay text is absent. Write the exact inspected background path/hash and actual observations to the visual-review JSON, then bind that review plus the separate background/thumbnail paths and hashes in `input/video-artwork.json` using `MASTER/cli/SPEC.md` §Video artwork contract. The harness checks actual 4K dimensions and rejects identical files or decoded pixels. Check exact thumbnail text, readable hierarchy and contrast, safe spacing, intentional negative space, subject integrity, brand consistency, and image artifacts. Remove text that only reads at desktop size. Record the approved draft, resulting paths, and any visible limitation in the series concept.

## Outputs and boundary

- Final video background: `SERIES/[series]/input/video-background.png` (or `.jpg`/`.jpeg`), actual 3840×2160 with Wavvy logo only.
- Final thumbnail: `SERIES/[series]/input/thumb.jpg`.
- Artwork role/hash contract: `SERIES/[series]/input/video-artwork.json` plus its hash-bound visual-review JSON. For already-uploaded series preserve historical artwork and records; do not recreate existing videos to apply the new contract.
- The user's approval is required before expensive final image work. A materially different composition needs another preview. The skill does not choose music, upload a video, or claim a click-rate improvement without measured evidence.
