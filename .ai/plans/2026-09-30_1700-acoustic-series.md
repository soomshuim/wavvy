# 17:00 acoustic series source update

Date: 2026-09-30
Scope: series concept and two user-provided remix source texts, followed by the approved state-writer correction and active-state transition. Media generation is outside this step.

## Confirmed brief

- Time slot: 17:00.
- Sound lanes: acoustic R&B, acoustic neo-soul, acoustic indie rock.
- Tempo: medium through 125 BPM. The user explicitly allowed 125 BPM; no lower numeric bound is set.
- Atmosphere: autumn warmth and comfort, with room for buoyant songs. No all-ballad requirement.
- Track 01: `서랍 (Acoustic Remix)`; track 02: `공강 (Accoustic Remix)` (user spelling preserved).
- The target is 20 songs: three acoustic-version remixes (Tracks 01, 02, and 04) plus 17 new songs (Track 03 and Tracks 05–20) to be made with the user. Only 01/02 have supplied source text; 04's earlier song, title, STYLE, and LYRICS remain unidentified. Track 03 is being developed separately. The old `올라가` sample will not be used, and older songs are not reused automatically.
- Both are user-made remixes in a newer Suno model. Exact model version, delivered audio, and measured BPM are unverified.
- The user clarified the cut-off `highly en` in Track 01 STYLE as a high-energy ending and approved completion to `high-energy`.
- The stored originals are `SERIES/16-00` track 09 and track 04, respectively. The user's recollection of earlier `17:00` songs is retained as a recollection, not used to overwrite stored provenance.

## Steps

1. Move the old `17-00` concept and `올라가` sample unchanged into `SERIES/17-00/archive/2026-09-30-pop-rnb/`. Verify both SHA-256 values match their pre-move values.
2. Save the two user-provided STYLE and LYRICS bodies as numbered track txt files. Leave EXCLUDE empty because none was provided. Apply only the user's explicit `highly en` → `high-energy` clarification to Track 01 STYLE and record it outside the prompt.
3. Write the new concept as a draft: explicit 17:00 Pop R&B default override, two supplied source rows, and an unsupplied Track 04 remix placeholder. Mark the old sample as history rather than a production candidate. Do not invent Track 04's identity/source, new-song drafts, audio properties, key/tempo for Track 02, or final upload metadata.
4. Check exact source text, archived bytes, filenames, and `git diff --check`. Do not run media completion gates for this draft.

## Outcome (2026-09-30)

- The current concept contains the 20-song target (three acoustic-version remixes at 01/02/04 and 17 new songs at 03/05–20), two supplied source tracks, and only a placeholder for 04. It preserves the user spelling `Accoustic Remix`, the allowed 125 BPM ceiling, and the clarified `high-energy` ending. Track 03 draft work is separate; no new-song source or media is included in this change.
- The prior concept and `올라가` sample are archived byte-for-byte; SHA-256 comparison against their previous tracked versions passed. They are history, not current production candidates.
- The state writer now keeps manual `phase`/`next_action` on the same series and infers both for a different series from its concept/artifacts. Explicit `--phase` and `--if-match` remain effective. Revision 4 was written by `python3 wavvy.py state SERIES/17-00 --write --if-match 3 --json` without a phase override; it infers `track_source_draft` with two txt sources, no final sources, and a next action to review drafts and follow the concept's next source work.
- Validation: 23 unit tests PASS (`/tmp/wavvy-1700-state-unittest.log`), py_compile PASS (`/tmp/wavvy-1700-state-pycompile.log`), diffcheck PASS (`/tmp/wavvy-1700-state-diffcheck.log`), state write output (`/tmp/wavvy-1700-state-write.json`), and state check PASS with no warnings or blockers (`/tmp/wavvy-1700-state-check.json`). The controller reported an isolated Astra xhigh reviewer CLEAN (Critical/High 0, no principle observations). No musical quality or audio property was inferred from the source text.
