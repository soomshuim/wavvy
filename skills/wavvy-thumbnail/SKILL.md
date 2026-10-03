---
name: wavvy-thumbnail
description: Design and finish Wavvy series video artwork and a typographic YouTube thumbnail. Use automatically during a Wavvy release after the series direction is known, or when the user asks to create or revise a Wavvy thumbnail. For lyric writing use wavvy-lyricist.
---

# Wavvy Thumbnail

Trigger: model-invoked during `wavvy-release` and on Wavvy thumbnail requests. This saves 젠 from starting a separate design task while preserving the visual approval point. The series concept and approved user direction outrank generic design preferences.

## Inputs

Read the target `SERIES/[series]/concept.md`, `wavvy.md`, existing `brand/` assets, and at least two completed Wavvy thumbnails. Read [Taste adaptation](references/taste-adaptation.md) for the transferable visual-design principles. Use the user's supplied reference or image if one exists.

## Steps

1. **Design Read:** State the intended scene, audience, mood, one visual focal point, and short thumbnail copy in one line. Audit the existing Wavvy logo/time treatment before choosing placement. Keep the image concept tied to the actual series, not a generic playlist aesthetic.
2. **Draft:** Make a 16:9 scene image at a review size well below final 4K. Keep title lettering out of the generated scene. Show the draft to 젠 and ask for one visual approval or revision decision. A specific user correction changes the draft brief; repeat the preview only as needed.
3. **After approval:** Produce the final 3840×2160 video background from the approved composition. State whether the pixels came from native generation or enlargement. Compose the thumbnail with the real Wavvy logo, series time, and a short title using a suitable local graphics tool; do not rely on image generation to spell text. Preserve the approved subject, clothing, season, and scene.
4. **Preflight:** Inspect the final image and thumbnail at full size and at a small phone-feed size. Check exact text, readable hierarchy and contrast, safe spacing, intentional negative space, subject integrity, brand consistency, and image artifacts. Remove text that only reads at desktop size. Verify actual file dimensions and record the approved draft, resulting paths, and any visible limitation in the series concept.

## Outputs and boundary

- Final video background: `SERIES/[series]/input/loop.png` or the project's selected image-mode input.
- Final thumbnail: `SERIES/[series]/input/thumb.jpg`.
- The user's approval is required before expensive final image work. A materially different composition needs another preview. The skill does not choose music, upload a video, or claim a click-rate improvement without measured evidence.
