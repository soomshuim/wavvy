# Wavvy local media cleanup — 2026-10-24

## Authorized scope

젠 requested deletion of all videos and audio, plus nonfinal thumbnail images/prompts/materials. On the scope question, 젠 selected **“Wavvy 프로젝트와 Wavvy 임시 복사본 전체 (추천)”**. Final thumbnails and their selected sources/provenance, lyrics, track styles, and concept/source documents are retained. Other repositories and unclassified app/system caches are outside scope. The current new 06:30 video is to be deleted **after its future YouTube upload is verified**; that video does not yet exist.

## Confirmed exception decision

The last recorded Suno upload accepted 18 tracks and rejected 06/11. Do not assume all local corrected audio can be downloaded again. 젠 answered **“이 세 파일만 남기고 나머지 삭제 (추천)”** for these three files, totaling 456,243,068 bytes:

- `SERIES/06-30/input/tracks/06__다리의 불꽃__Driven__Hardcore Punk Rock__NA.wav`
- `SERIES/06-30/input/tracks/11__계속 앞으로__Driven__Hardcore Punk Rock__NA.wav`
- `SERIES/06-30/output/continuous-mix-20261024/repeat2/continuous-mix-0630-repeat2.m4a`

These three remain protected. The two corrected tracks are retained separately; the finished mix is retained until the current video's YouTube upload is verified. This does not assert that every other Suno source is currently downloadable.

## Execution

1. Inventory actual local audio/video and nonfinal thumbnail materials in separate manifests under `.ai/cleanup/`. Freeze per-file identity and size. Do not follow symlinks outside scope.
2. Inspect proven Wavvy temporary copies only. CDS worktrees and unrelated `/private/var/folders/` contents are excluded. Do not delete whole worktree folders or rewrite Git history/objects.
3. Record the confirmed exception answer and review the concrete allowlist independently before deletion. Final tied-hair photo and its exact prompt/provenance are protected; rejected headband/earlier images and failed composition materials are candidates.
4. Delete only authorized, unchanged regular files in the allowlist. Record each result and actual filesystem free space before/after. Stop on identity changes; do not expand scope automatically.
5. Verify protected files and absence of deleted targets. Update local-availability facts in concept/SESSION/CHANGELOG and append HANDOFF. Use `wavvy.py state --write` for state changes. Preserve historical generation/upload/approval evidence as history.
6. Commit/push the scoped durable record. Report deleted logical bytes separately from observed free-space gain. The macOS System Data category is not inferred from a directory total.

## Current thumbnail

The sports band was rejected. The requested band-free short tied-hair photograph is saved as `SERIES/06-30/input/thumbnail-draft-runningwear-tiedhair-20261024.png` (1672×941). Final logo/time/cadence composition has not completed; a font-substitution failure stopped the new compositor. No new typography or photo-generation retry is part of this cleanup.
