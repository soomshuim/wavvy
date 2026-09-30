# Style Prompt and Full-Song Draft Modernization

Date: 2026-09-30
Status: implementation and isolated review complete; commit and push pending

## Problem and precedent

Track 03 「너와」 initially lacked proposed key and vocal gender; its first Style exceeded Wavvy's 900-character budget. A user generation then came out shorter than three minutes and omitted the requested Intro. Existing STYLE/ROLES text treated fixed English tokens and one arrangement arc as universal pass/fail checks. Suno's official materials instead document descriptive style, Custom Exclude, user-provided full lyrics, voice options, and model-dependent maximum length; they do not establish those fixed tokens as guaranteed controls. Source summary: MASTER/style/references/prompt-evidence-2026-09-30.md.

## Scope and decisions

- Modernize MASTER/style/STYLE.md and MASTER/roles/ROLES.md around clear musical intent, source/proposal truth, Wavvy brand defaults, per-track exceptions, internal 900-character Style and 8-item Exclude budgets, and audio verification. Remove universal first-word, 8–10-token, S1–S10, and fixed section-energy requirements.
- Route combined lyric + Style work through MASTER/style/STYLE.md and MASTER/roles/ROLES.md in the lyric skill/spec; preserve lyric-only and existing-source modes.
- Clarify in MASTER/lyrics/LYRICS.md that user-reviewed full lyrics can be used in Suno Custom Mode. For a newly requested full song, plan target duration, meter, BPM, and ordered section bars; require an Intro and Outro by default while allowing a song-specific structure. This is a duration estimate, not an audio guarantee.
- Expand 17:00 Track 03 lyric meaningfully without filler, plan around 3:20 at proposed 106 BPM, keep the longtime-friend theme and user-facing chorus, and record new body hash. The user has not approved the new lyric or suggested musical settings.
- Preserve the user-provided 01/02/04 source texts and their track-scoped exceptions.

## Verification and handoff

The paired code worker owns track-prompt/full-song gate implementation, CLI/workflow routing, and tests. This worker owns style/role/lyric policy and Track 03 text/artifact. Track 03 has STYLE 822 characters, EXCLUDE 6 items, Intro, 67 lyric lines, and body SHA-256 3e2f035302e55f840b1ae93f6ce47514e6034d43c760c6dd11d2393c9d971896. The 92-bar plan at proposed 106 BPM in 4/4 estimates about 208.3 seconds toward the 3:20 target; audio is unverified. Initial isolated reviews found duplicate LYRICS section and duplicate BPM header paths: a synthetic 106/125 header with STYLE 125 could pass both routes although 92 bars at 125 BPM estimates 176.6 seconds, below the 200-second target. With user approval, shared `parse_track_source_fields` now returns canonical metadata and sections, rejects duplicate headers (including case/space variants) and sections, and is used by both gates and archiving. Focused regressions confirm the 106/125 source is rejected by all three paths. Current Track 03 track-prompt and lyrics-review full-song gates and lyric-skill pass, 01/02/04 parse, and 33 tests, py_compile, and diffcheck pass in `/tmp/wavvy-prompt-gate-*` logs. Final fresh isolated `shared_parser_review` returned Critical/High 0 and principle observations 0 (CLEAN). User review of the new lyric and actual generated audio remain outstanding; commit and push are the remaining repository steps.
