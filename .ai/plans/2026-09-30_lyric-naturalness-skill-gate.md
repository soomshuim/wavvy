# Wavvy lyric naturalness skill and gate alignment

## Precedent and cause

- `SERIES/18-00/concept.md` tracks 02/03/06/07/09 and other user-selected Wavvy lyrics show that direct feeling, explanation, metaphor, ordinary sentences, and loose sensory association can work when each expression reads naturally. Track 03 also shows that matching a melody by forcing wording can weaken a line. A liked song is not evidence that every line in it is good.
- `wavvy.md` §5, `skills/wavvy-lyricist/SKILL.md`, `references/patterns.md`, and the spec currently prefer object words, inferred emotion, short lines, and event-led shifts as near-universal rules. `gate.py` enforces a three-term image quota and rejects direct time/activity vocabulary despite higher-level policy saying the lyric topic is not forced.
- The current `lyrics-review` CLI stage checks the installed skill package without receiving a lyric artifact. `review-only` ignores its Verdict while requiring a nonexistent Self-Gate. Self-reported PASS strings can be mistaken for verified lyric quality.

## Scope

- Align `wavvy.md`, `MASTER/lyrics/LYRICS.md`, the lyric skill, spec, pattern reference, and the thin `/write` route where their active guidance conflicts. Keep Korean and Suno mode contracts; preserve the command entrypoint.
- Remove vocabulary and object-count quality proxies from `wavvy_harness/gate.py`. Keep only deterministic file, mode, source binding, evidence completeness, and status checks. The order for human lyric review is expression → connection → emotional flow.
- Make the lyric gate report its scope and quality status. An installed package is not a reviewed lyric. Full draft/review-only records bind to a readable target by content hash and quote. An awkward line is not rescued by an explanation of its context. Prompt-only mode checks its input contract without requiring full-lyric review axes.
- Route `gate --stage lyrics-review` artifact and mode options through the existing CLI. Add regression tests for stale, absent, empty, conflicting, and failed review evidence and for accepted vocabulary/structure variation.
- Leave series source/media, `AGENTS.md`, `CLAUDE.md`, `.ai/state.json`, and HIPHOP content checks untouched. Commit/push belongs to the later record step.

## Verification

- Focused `tests/test_harness.py` regressions, full unit suite, `python3 -m py_compile`, package/CLI smoke checks, skill `quick_validate.py`, and `git diff --check`.
- Save raw command output under `/tmp/wavvy-lyric-*`; report the paths and any remaining limits. These checks cannot establish that a lyric sounds good or was written by a human.

## Outcome (2026-09-30)

- Completed the active brand/lyric policy, skill, spec, reference for the 13 selected songs, `/write` route, CLI documentation, `gate.py`, CLI plumbing, and regression tests. No series, audio, AGENTS/CLAUDE, state, or HIPHOP content-check files changed. The new autumn R&B series was outside this change; no follow-up work is asserted here.
- The human or lyric-reading agent checks **Expression → Connection → Emotional Flow**. The record binds to the actual Draft or separate lyric-body source with SHA-256 and exact quotes. `review-only` uses Findings/Verdict; prompt-only retains Empty/Prompt/Structure without full-lyric axes. Package-only PASS is installation status (`NOT_REVIEWED`), and `lyrics-review` without an artifact fails. The harness checks structure, source match, and recorded statuses. It does not verify meaning, musical effect, or authorship.
- The 13 cited precedents include stored Wavvy lyrics such as `SERIES/18-00/concept.md` Track 06 「전화」 and the user-provided 「낮꿈」 text, which is absent from the local track file. The user rejected its line “내 이름 불러도 / 살짝 뒤로 미뤄 둬”; its surrounding dream context cannot rescue that wording. 「작은 손/작은빛」 uses the user's instrumental Outro over the stale extra lyric lines in the stored concept. Liked songs are not blanket approval of each line.
- Raw verification: `python3 -m unittest tests/test_harness.py` (20 PASS, `/tmp/wavvy-lyric-unittest.log`), `python3 -m py_compile wavvy.py wavvy_harness/*.py` (PASS, `/tmp/wavvy-lyric-pycompile.log`), skill `quick_validate.py` (PASS, `/tmp/wavvy-lyric-quickvalidate.log`), `git diff --check` (PASS, `/tmp/wavvy-lyric-diffcheck.log`), and package smoke (PASS / PACKAGE_ONLY / NOT_REVIEWED, `/tmp/wavvy-lyric-package-smoke.json`). The controller separately reran 20 tests (`/tmp/wavvy-lyric-controller-tests.log`).
- The controller reported an isolated Astra xhigh review with Critical/High 0 and no principle observations (CLEAN). Its behavior samples accepted direct feeling/explanation and a poetic sensory association without an added plot or resolution (“네가 없는 집에서는 / 작은 소리도 오래 남아”), while rejecting “졸음이 내 시간을 걸어 / 오후를 잠깐 비켜 둬” as an awkward expression and holding its connection judgment. This is qualitative review evidence, not a machine quality guarantee.
