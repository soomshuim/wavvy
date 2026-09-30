---
name: wavvy-lyricist
description: Use when writing, rewriting, or reviewing Korean lyrics or Suno lyric prompts for Wavvy series while preserving Wavvy SSOT, copyright safety, and natural sung Korean.
---

# Wavvy Lyricist

Wavvy 전용 한국어 작사 스킬. 목표는 시리즈의 사운드·장르·주제 조건 안에서 문장 자체가 자연스럽게 읽히는 가사를 만드는 것이다. 텍스트 검토와 실제 노래 청취 평가는 구분한다.

## Authority

Read in this order before drafting:

1. `MASTER/SSOT.md` for conflict order.
2. Target `SERIES/[series]/concept.md` for series gates and overrides.
3. `MASTER/lyrics/LYRICS.md` for Suno lyric input policy.
4. `wavvy.md` for brand constants.
5. `skills/wavvy-lyricist/references/patterns.md` for lyric pattern lanes.
6. `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md` for output and gate contract.

Local Wavvy docs override external trend evidence. Per-series overrides are valid only when explicitly written in the series concept.

## Hard Rules

- Korean lyric channel: full lyric drafts should be Korean unless a series concept explicitly permits code-switching.
- Single lead vocal, chest-dominant identity. Do not solve lyric weakness with harmony, backing vocal, falsetto, or choir instructions.
- Time slots define BPM, mood, energy, use case, and vocal tone before lyric topic.
- Time or activity words may be used when the lyric calls for them; a time slot does not force those words into a track.
- Use external songs only as abstract pattern evidence. Do not copy, translate, closely paraphrase, or imitate distinctive lyric lines or cadences.
- Separate full lyric draft mode from Suno prompt-only mode.

## Mode Choice

Choose and name exactly one mode:

- `full-lyric-draft`: Use for track source files, rewrite proposals, or human review. Section tags such as `[Verse]` and `[Chorus]` are allowed as drafting structure.
- `suno-prompt-only`: Use for direct Suno Lyrics input. Choose Empty, or output 1-3 short English direction lines or structure tags. Do not output full Korean lyric rows.
- `review-only`: Use when asked to judge an existing lyric without rewriting.

Never mix prompt-only text and full lyric rows in the same deliverable.

## Draft Workflow

1. Build a Source Map: series concept, Wavvy docs, track/source file, research artifact, and external pattern sources if used.
2. Freeze the known BPM, key, genre, mood, vocal identity, language, subject, and series-specific conditions. Mark unknowns as unknown.
3. Pick a Lyric Strategy suited to this track: speaker/listener, expression, connection, emotional movement, density, and whether repetition or a hook has a role. These are choices, not required plot beats.
4. Draft in the selected mode.
5. Read the actual lines in order: expression first, connection second, emotional flow third. An awkward line is not rescued by an explanation of its context. If a series meter or style condition forces awkward Korean, mark the conflict and revise the wording.
6. Record compact review evidence in `Self-Gate`, or in `Findings` for `review-only`. Never put review metadata inside the lyric rows delivered to listeners.

## Wavvy Writing Principles

- Check whether the speaker would say each line in that moment. A line may ask, answer, reassure, hesitate, notice, decide, repeat, or simply stay with a sensation.
- Follow the lyric's own connection: a heard reply, a changed action, a bodily sensation, or an association can all link lines. Do not require every track to advance an event or teach a lesson.
- Direct feelings, explanation, ordinary sentences, and metaphor are available when they read naturally. A noun list, fixed sentence length, image quota, or forbidden adjective list cannot establish naturalness.
- Let repetition, pauses, and hooks serve the track. A chorus is not required to summarize a verse or add new information on every return.
- Preserve genre, language, and subject constraints from the series concept. Flag a conflict when fitting a syllable or style condition produces awkward expression.

## Avoid

- Phrases that sound forced when read aloud, including a metaphor or ordinary phrase selected only to fill syllables.
- Explanations that claim an awkward line is natural because its surrounding context is good.
- Heavy heartbreak, toxic intimacy, dark room framing, or melodrama unless the target series requires it.
- Prompt-only parentheses such as `(Scene: ...)` or `(Mood: ...)`.
- Production/performance instructions in lyric text; move those to style prompts.

## Required Output

For new drafts and rewrites, output these sections in order:

1. `Source Map`
2. `Constraint Freeze`
3. `Lyric Strategy`
4. `Draft`
5. `Self-Gate`

For `review-only`, output:

1. `Source Map`
2. `Constraint Freeze`
3. `Findings`
4. `Verdict`

## Self-Gate

For `full-lyric-draft`, put this compact record beneath `Self-Gate`. For `review-only`, put it beneath `Findings` and put one `PASS | reason`, `HOLD | next fix`, or `FAIL | reason` in `Verdict`:

- `Review Source: Draft` for a full draft; for review-only, use a separate readable lyric-body file path relative to the review artifact. A full draft artifact may be the source; its `Draft` section is extracted.
- `Source SHA256: <current hash of the stripped lyric body>`. A missing or stale hash fails the gate. A failed check reports the actual hash so it can be copied into the review record after rereading the current lyric.
- `Expression: PASS | "exact lyric quote" | brief reason`, then `Connection` and `Emotional Flow` in that order. Use `HOLD` or `FAIL` when warranted. Quotes must occur in the reviewed body; the harness checks matching and completeness, not the truth of the judgment.
- `Copyright Safety`, `Wavvy Identity`, `Series DNA`, and `Suno Format`: each has one `PASS/HOLD/FAIL | brief reason` line. This keeps the original safety and series checks without turning vocabulary into a quality score.

For `suno-prompt-only`, use just the four contract lines in `Self-Gate`; do not apply full-lyric axes. Keep Empty, Prompt, and Structure input choices from `MASTER/lyrics/LYRICS.md`; an empty `Draft` requires `suno_input: Empty` in `Constraint Freeze`.

The artifact's `Draft` section is the listener-facing lyric. Share only that section when delivering a finished lyric. The surrounding source map, checks, and hashes are working records, never lyric rows. A recorded review is evidence of a review, not an automated guarantee of lyric quality or AI authorship.
