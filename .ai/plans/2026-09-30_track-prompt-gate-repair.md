# Track prompt and full-song draft gate repair

## Cause and precedent

- `MASTER/style/STYLE.md` and `MASTER/roles/ROLES.md` defined a 900-character STYLE budget, an eight-item EXCLUDE budget, and explicit vocal gender, BPM, and key choices, but `wavvy_harness/gate.py` only checked lyric review records or later audio stages. `wavvy.py` parsed track txt files for final upload without checking those prompt fields. The earlier Track 03 source had a 949-character STYLE, 12 EXCLUDE items, and unknown key/gender, yet a lyric-only result could appear complete.
- `MASTER/WORKFLOWS.md` already requires a `STYLE`/`EXCLUDE`/`LYRICS` txt source before concept archiving. `wavvy.py` already parses this source. The repair attaches a prompt-contract check to the existing `gate --artifact` CLI path and reads that source, rather than treating package installation or a chat summary as evidence.
- Feedback on the generated Track 03 audio exposed a separate gap: a lyric review record did not state whether its draft was a full song, did not plan an intro or section durations, and could not detect a section plan shorter than the requested duration. Text cannot establish actual audio length.

## Scope

- Apply the new track-prompt stage only when explicitly invoked for a newly authored full-track txt source. Keep user-provided remix sources and lyrics-only/review-only/prompt-only work outside this check. Report the inspected source hash and an explicit prompt-contract scope.
- Check only deterministic prompt facts: the STYLE body length, EXCLUDE item count, source sections, numeric BPM, key/mode, vocal gender, and agreement between header and STYLE. Treat 900/8 as Wavvy's current internal budgets, not a claim about Suno's product limits. Do not hard-code fixed musicality slogans, articulation wording, instruments, lyric semantics, or audio quality.
- Add explicit full-song versus excerpt scope to new full-lyric artifacts, then require full-song work to include a target duration, meter, section bar plan, and intro/ending structure. Compare BPM-based estimated duration with the target while stating that the estimate cannot guarantee a generated recording's duration. Preserve review-only and prompt-only boundaries.
- Route the checks through `MASTER/WORKFLOWS.md` and `MASTER/cli/SPEC.md`; skill/spec/lyric policy and Track 03 text are owned by the parallel source/policy worker.

## Verification

- Regression tests through the CLI for the earlier 949-character/12-item/unknown-field failure shape, current valid Track 03, exactly 900 versus 901 Unicode characters, absent/mismatched BPM/key/gender, source binding, and scope separation.
- Regression tests for full-song plan gaps and excerpt/review/prompt-only unaffected behavior. Run `tests/test_harness.py`, Python compilation, live Track 03 gates, and `git diff --check`; save raw outputs under `/tmp/wavvy-prompt-gate-*`.

## Isolated review finding and repair

- **High — silent review-source mismatch.** A txt with a second `=== LYRICS ===` section made the lyric gate read the first body while `parse_track_source` archived the last body. Both gates could pass, and `full_song_ready` could be true although the lyric that would be archived had not been reviewed. The same overwrite risk existed for a repeated STYLE section. This is a silent omission of the required review, so the High finding is retained.
- `wavvy_harness/source.py` now provides the one section parser used by both paths. It rejects duplicate section names before either gate or archiving can select a body. The regression starts from a source that passes both gates, appends a second LYRICS or STYLE section, then verifies both gates fail and `parse_track_source` rejects the file.
- **High — silent BPM-plan mismatch.** A txt with `BPM: 106` followed by `BPM: 125` let the lyric gate read the first header line while track-prompt and archiving used the last. Both gates could pass a 200-second, 92-bar plan, although at 125 BPM those bars estimate only 176.6 seconds. This could mark an unready full song `full_song_ready` without flagging the missing duration obligation.
- The same shared parser now returns canonical header metadata as well as sections. It rejects duplicate header keys, including case and surrounding-space variants, before either path can inspect their values. Both gates and archiving consume that same metadata dictionary. The regression checks duplicate BPM with a 125 BPM STYLE against the artifact's 106 BPM plan and requires both gates to fail, readiness to be false, and archiving to reject the source.

## Final verification

- Track 03 track-prompt and lyrics-review full-song gates PASS; Track 01/02/04 sources parse. The duplicate BPM 106/125 regression rejects both gates and archiving. The full suite passes 33 tests; Python compilation and diffcheck pass. Raw outputs: `/tmp/wavvy-prompt-gate-{track03.json,lyrics03.json,unittest.log,pycompile.log,diffcheck.log,duplicate-header-regression.log,remix-parse.log}`.
- Fresh isolated `shared_parser_review`: Critical/High 0, principle observations 0 (CLEAN). Text checks do not establish generated audio duration or musical quality; Track 03 lyric and proposed settings await user review.
