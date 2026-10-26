# Wavvy Runtime Rules

Version: 1.0
Last Updated: 2026-05-02
Owns: runtime hard constraints, media execution cautions, approval/safety rules

This file holds rules that agents must know at execution time but that do not belong in thin entrypoint routers.

## Hard Constraints

1. **No Pydub** — use FFmpeg-based paths only.
2. **Audio acrossfade is not video xfade** — do not conflate `acrossfade` for audio merges with `xfade` for video loop transitions.
3. **Fail fast** — stop on input validation, media probe, artifact writer, or gate failures.
4. **Pure input policy** — Suno source work follows `MASTER/WORKFLOWS.md` and the relevant lyrics/style docs.
5. **SSOT before inference** — when docs and files disagree, use `MASTER/SSOT.md` and `.ai/state.json`.
6. **Video artwork is not the thumbnail** — every new static full-length video uses an actual 3840×2160 generated scene with the Wavvy logo only. Title, BPM, time, and other promotional lettering belong to the separate YouTube thumbnail. This applies to every music theme. Require `input/video-artwork.json`, distinct file hashes and decoded pixels, and a visual review bound to the exact background hash before preview/render/pack. Filename alone is not visual evidence. The `generated_scene` field records provenance; the gate does not authenticate image generation. See `MASTER/cli/SPEC.md` §Video artwork contract.

Already-uploaded videos retain their historical artwork and release evidence; do not recreate them to apply this rule. Legacy inspection requires recorded upload completion and retained render identity. It never permits a new render to reuse a thumbnail. Existing video-loop processing remains unchanged; new loop artwork follows the same logo-only visual policy, while the static-image contract checks apply to static inputs.

## Approval And Safety

- 사용자 확인 필수: before broad code changes, destructive cleanup, uploads, or expensive/long media runs, state the approach and get confirmation unless the user has explicitly asked for that exact execution.
- Never delete source docs or track source files unless the relevant workflow says deletion is safe.
- Do not treat ignored/generated media as durable truth. Use state and concept records first.
- Do not commit or push unless the user explicitly requests it.

## Complex Media Protocol

Treat work as complex when it touches 10+ files, runs over 10 minutes of media, uses a new FFmpeg filter, or repeats a previously failed operation.

For complex media work:

1. Confirm the approach.
2. Start with the smallest useful test.
3. Check expected duration before full render.
4. Run validation/gates after completion.

Checklist:

- Audio merge uses sequential acrossfade when appropriate.
- Video xfade is only required for video-loop packaging, not image-mode packaging or already-uploaded series state checks.
- `filter_complex` scale is considered for large track counts.
- `final.mkv` / `upload.csv` may be deleted after upload if `concept.md` records upload completion and state marks them `deleted_after_upload`.

## Verification Gates

Use the narrowest relevant set:

```bash
python3 wavvy.py doctor --json
python3 wavvy.py validate SERIES/[series]
python3 wavvy.py state SERIES/[series] --check --json
python3 wavvy.py gate SERIES/[series] --stage source-final --json
python3 wavvy.py gate SERIES/[series] --stage uploaded --json
```

For code changes:

```bash
python3 -m py_compile wavvy.py wavvy_harness/*.py
python3 -m unittest tests/test_harness.py
git diff --check
```

## Pointers

- Workflow details: `MASTER/WORKFLOWS.md`
- CLI command details: `MASTER/cli/SPEC.md`
- Phase/artifact semantics: `MASTER/SSOT.md`
- Quality gates: `MASTER/MANAGER.md`
