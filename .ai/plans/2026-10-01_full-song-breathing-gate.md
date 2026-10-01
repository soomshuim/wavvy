# Full-song phrasing and breathing gate

## Precedent and scope

- Track 03 and the original Track 05 full-song records use two long verses. Track 05's original source was approved after hearing the result, even though the text looked crowded. Preserve those exact approved Draft bodies.
- Apply the new default to newly written complete songs across Wavvy, not only the 17:00 series. Excerpts, review-only, prompt-only, and user-provided/remix sources do not inherit it.
- Change the lyric skill, its owning lyric policy/spec, the full-song artifact gate, CLI documentation, and focused tests. Do not edit series sources, concept, state, or session files in this worker.

## Contract

- Start a new complete song with three Verse sections. Allow a different count when `verse_structure_exception` records a concrete song/user/series reason. Keep Intro/Outro planning and the existing section-bar duration check.
- Require Self-Gate evidence of each verse's actual sung-line count, the longest written sung line and its phrasing decision, a short phrase (one line or two adjacent lines if one thought spans rows), and an exact lyric quote with a stated breath or instrumental space after it. The gate checks counts, exact quotes, optional adjacency, and statuses. It cannot hear phrasing or certify that the reasons are musically sound.
- Do not introduce a lyric-line minimum, line-length ceiling, syllable quota, or requirement to add total words. Plan duration with sections and playing space.
- Keep only the approved Track 03/05 Draft hashes in a small legacy manifest. Both artifact path and Draft hash must match. Rewrites at either path use the new contract.

## Verification

- Focused tests for three-Verse PASS, supported structural exception, missing/false breathing evidence, same-path revised draft, and legacy original PASS.
- Run the harness suite, Python compile, skill validation, live 03/05 gates, and diff check. Save raw command results under `/tmp/wavvy-breath-*`.

## Outcome (2026-10-01)

- New full-song artifacts enforce the three-Verse default or a recorded structural reason, plus four current-Draft breathing evidence lines. The checks bind line counts and exact quotes but do not judge sung naturalness or generated audio.
- The earlier approved 03 and original 05 Drafts both passed the live full-song lyric gate using the path-and-hash legacy manifest. A revised Draft at the same path enters the new contract. Excerpt, review-only, prompt-only, and existing user-provided sources are outside this new gate.
- Raw checks: 36 tests PASS (`/tmp/wavvy-breath-unittest.log`), Python compile PASS (`/tmp/wavvy-breath-pycompile.log`), skill validator PASS (`/tmp/wavvy-breath-quickvalidate.log`), live 03/05 gate PASS (`/tmp/wavvy-breath-03-gate.json`, `/tmp/wavvy-breath-05-gate.json`), diffcheck PASS (`/tmp/wavvy-breath-diffcheck.log`). Controller reported isolated Astra xhigh review CLEAN (Critical/High 0), reran 36 tests, and checked the restored 05 source sections against `ef48c6f`.
