# Wavvy Lyric Skill Spec

Version: 0.2
Last Updated: 2026-09-30
Owner: `MASTER/lyrics/LYRICS.md` policy layer
Skill: `skills/wavvy-lyricist/SKILL.md`

## Purpose

Define the durable contract for the Wavvy lyric-writing skill and the later harness checks that validate it. This spec does not replace `MASTER/lyrics/LYRICS.md`; it narrows how agents should draft, rewrite, or review Wavvy lyrics.

## Authority And Scope

Applicable tasks:

- Writing or rewriting a Wavvy track lyric.
- Producing Suno Lyrics input for a Wavvy track.
- Reviewing a Wavvy lyric draft for policy, style, or copyright safety.
- Creating genre/time-slot lyric guidance for a series.

Conflict order:

1. `MASTER/SSOT.md`
2. Target `SERIES/[series]/concept.md`
3. `MASTER/lyrics/LYRICS.md`
4. `MASTER/MANAGER.md`
5. `wavvy.md`
6. This spec
7. `skills/wavvy-lyricist/references/patterns.md`

If this spec conflicts with a higher-priority source, the higher source wins.

## Required Skill Files

The lyric skill is complete only when these files exist:

- `skills/wavvy-lyricist/SKILL.md`
- `skills/wavvy-lyricist/references/patterns.md`
- `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`

The skill file must reference both this spec and the patterns reference.

## Source Requirements

Every new draft, rewrite, or review must identify:

- Wavvy authority files used.
- Target series concept path.
- Target track/source file when one exists.
- Research artifact or external sources if current trend claims are used.
- Access date for any new external source.

External lyric pages are not required and should be avoided. If external songs are researched, record only abstract patterns, metadata, interviews, chart context, or production/narration commentary. Do not store lyric text.

## Output Modes

### `full-lyric-draft`

Use for track files, rewrite proposals, and human review.

Allowed:

- Korean lyric rows.
- Structure tags such as `[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Post-Chorus]`, `[Bridge]`, `[Outro]`.
- Short notes outside the draft explaining mode, constraints, and gate results.

Not allowed:

- Treating the full lyric as Suno prompt-only input without saying so.
- Embedding production directions as lyric rows.
- Using harmony/backing-vocal dependency to compensate for weak writing.

### `suno-prompt-only`

Use for direct Suno Lyrics input, including an intentionally Empty input.

Allowed:

- 1-3 short English direction lines for Prompt or Structure, or an empty Draft when `suno_input: Empty` is declared.
- Structure-only tags or compact structure line such as `I-V1-PC-C-PC2-V2-C-B-C-O`.
- Brief mood/theme/image keywords.

Not allowed:

- Full Korean lyric rows.
- Parenthesized prompt-only text such as `(Scene: ...)`.
- Production instructions that belong in the style prompt.

### `review-only`

Use when judging an existing readable lyric-body file without drafting a replacement. Point `Review Source` in `Findings` to that file, relative to the review artifact or absolute. If it is a full-draft artifact, only its `Draft` section is reviewed; a file with production metadata but no `Draft` is not a lyric-body source.

Required:

- Findings tied to exact lines of the reviewed lyric.
- Verdict: `PASS`, `HOLD`, or `FAIL`.
- Minimum viable fix direction for every `HOLD` or `FAIL`.

## Required Output Schema

For `full-lyric-draft` and `suno-prompt-only`, output sections in this exact order:

1. `Source Map`
2. `Constraint Freeze`
3. `Lyric Strategy`
4. `Draft`
5. `Self-Gate`

For `review-only`, output sections in this exact order:

1. `Source Map`
2. `Constraint Freeze`
3. `Findings`
4. `Verdict`

## Constraint Freeze Fields

Include all fields that are known:

- `series`
- `track`
- `mode`
- `genre_lane`
- `bpm`
- `key`
- `mood`
- `vocal_identity`
- `language_policy`
- `time_activity_policy`
- `explicit_overrides`
- `copyright_boundary`
- `suno_input` (`Empty`, `Prompt`, or `Structure`) when a prompt-only Draft is intentionally empty

Unknown fields should be marked `unknown`, not guessed.

If the task also produces Style/Exclude or a song package, route prompt decisions to `MASTER/style/STYLE.md` and `MASTER/roles/ROLES.md`. For a new-song proposal, choose and label vocal gender, key, and numeric BPM as proposals within the series direction instead of leaving the requested creative choices unknown. Preserve unknown facts in existing user-provided sources and review-only work; lyric-only tasks need no Style proposal. Present proposed vocal gender, key, and BPM in a short Korean line before a new song's English Style. Run `python3 wavvy.py gate SERIES/[series] --stage track-prompt --artifact SERIES/[series]/input/tracks/[track].txt --json` for the prompt source; lyric review PASS does not cover this check.

For a newly requested complete song, set `draft_scope: full-song` in `Constraint Freeze` and include `target_duration_seconds`, `meter`, ordered `section_bars`, and `track_source` (the corresponding txt path). Estimate duration from BPM and section bars and include Intro/Outro by default, with an explicit track exception when needed. The plan does not equate lyric lines to fixed bars or guarantee generated length. Do not impose a word-count floor, scene count, or repeated filler. A missing scope in an older artifact remains unspecified; excerpts, review-only, prompt-only, and user-provided original sources do not inherit this new requirement. Validate with `python3 wavvy.py lyrics-skill SERIES/[series] --artifact FILE --mode full-lyric-draft --draft-scope full-song --json`; the gate also compares the artifact Draft to the txt LYRICS body.

## Lyric Strategy Fields

For drafts and rewrites, state the useful choices for this track; do not invent a hook or plot to fill a field:

- `narrator`
- `connection` (conversation, action, sensation, association, or another fitting relation)
- `emotional_movement` (including a held or repeated state)
- `hook_or_repetition_role` (or why it is absent)
- `density`
- `suno_handling`

## Self-Gate Contract

Human review order is **Expression → Connection → Emotional Flow**. First read each sentence without rescuing awkward wording through surrounding context. Then check how the words, actions, unspoken replies, sensations, or associations connect. Finally check how the feeling moves or stays. Direct emotion, explanation, metaphor, ordinary lines, static scenes, and repetition are allowed when they work for this track. Do not count nouns, image terms, short lines, or new events as quality proxies. A series meter/style rule does not justify an awkward line; record the conflict and revise it.

### Compact Review Evidence

For `full-lyric-draft`, place these lines inside `Self-Gate`; for `review-only`, place them inside `Findings` and add one `Verdict` line. The same evidence contract applies to both:

```text
- Review Source: Draft
- Source SHA256: <hash of stripped Draft body>
- Expression: PASS | "exact quote from body" | reason
- Connection: PASS | "exact quote from body" | reason
- Emotional Flow: PASS | "exact quote from body" | reason
- Copyright Safety: PASS | reason
- Wavvy Identity: PASS | reason
- Series DNA: PASS | reason
- Suno Format: PASS | reason
```

In `review-only`, `Review Source` instead names a readable separate lyric-body file. Paths are relative to the review artifact or absolute. A source artifact with a `Draft` heading contributes only its stripped `Draft` body; a plain lyric-only file contributes its stripped whole body. Each axis needs an exact nonblank lyric quote and a specific reason. `Source SHA256` must match the current body. The harness reports the current hash in `reviewed_source_sha256` and the corresponding check detail, including on a stale or missing claim, so the reviewer can reread and update the record. Review evidence is kept outside listener-facing lyric rows.

Each status is exactly one `PASS`, `HOLD`, or `FAIL` with a reason. `HOLD` names the next fix; `FAIL` blocks final handoff. `review-only` uses its own `Findings` and `Verdict`; it has no `Self-Gate`. A `PASS` Verdict cannot contradict a HOLD/FAIL finding. The four contract lines retain copyright, brand, series, and Suno format checks. Time/activity words and hook presence are judged in context under Series DNA, not through a fixed list.

For `suno-prompt-only`, use only the four contract lines in `Self-Gate`. Full-lyric axes, body hash, and quotes do not apply. A blank `Draft` is valid only with `suno_input: Empty` in `Constraint Freeze`; otherwise use one to three direction/structure lines. Preserve the Suno Empty, Prompt, and Structure choices and the English prompt-only input rules in `MASTER/lyrics/LYRICS.md`.

These records show what was checked and which body was read. The harness validates their shape, binding, and status; it does not certify lyrical meaning, musical performance, human authorship, or the correctness of a reviewer's PASS.

## Harness Acceptance Baseline

A file-level harness may validate the skill package with static checks:

- Required files exist.
- `SKILL.md` front matter contains `name: wavvy-lyricist`.
- `SKILL.md` names all three output modes.
- `SKILL.md` contains the required output section labels.
- `patterns.md` states that copied/translated external lyric lines are not stored.
- This spec defines `Self-Gate Contract` and `Harness Acceptance Baseline`.

A lyric-artifact harness validates the record and deterministic input constraints:

- Required output sections appear in order.
- Mode is named exactly once in `Constraint Freeze`.
- `suno-prompt-only` output contains no full Korean lyric rows.
- Full draft/review-only evidence quotes occur in a nonempty current lyric body and the reported hash matches that body.
- Expression, Connection, Emotional Flow, Copyright Safety, Wavvy Identity, Series DNA, and Suno Format each appear once with a status and reason.
- `review-only` Verdict appears once and does not contradict its findings. Missing/duplicate/stale evidence or any FAIL cannot pass; HOLD requires a decision.
- Package-only `PASS` means the skill files are installed. `gate --stage lyrics-review` requires `--artifact`; its result concerns the record's structure and status, not verified lyric quality.

Static checks are necessary but not sufficient. Natural Korean speech and copyright similarity require meaning review by a person or an agent that actually reads the lyric. Musical effect requires listening when it matters. This adds no user-approval step.

## Release Note Requirement

When this skill is changed after initial creation, release/session documentation should record:

- Why the skill changed.
- Which source rule or user feedback caused the change.
- Whether harness expectations changed.

Do not update release/session docs from worker roles unless explicitly assigned that write scope.
