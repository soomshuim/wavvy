---
description: Wavvy 작사 스킬 호출 - lyric 작성/리라이트/리뷰 전용
allowed-tools: [Read, Glob, Bash]
argument-hint: ["SERIES/[series] lyric request"]
---

# /write Command

Wavvy lyric-only thin shim. In Codex, `-write` resolves to this same local `write` command.

## Scope

Allowed: lyric writing, full lyric draft, rewrite, review, or Suno lyric-slot refinement.

Out of scope:
- YouTube title, description, tags, or thumbnail copy
- Series concept, changelog, session, handoff, or general prose writing

## Required Routing

1. If a target series is named, read `SERIES/[series]/concept.md`; otherwise ask for the target series/track before drafting.
2. Load `skills/wavvy-lyricist/SKILL.md`.
3. Follow `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md` and `MASTER/lyrics/LYRICS.md`.
4. Use the requested mode only: `full-lyric-draft`, `suno-prompt-only`, or `review-only`.
5. Within `full-lyric-draft`, record whether this is a `full-song` or an `excerpt`. For a new complete song, use the full-song gate below; for an excerpt, use `--draft-scope excerpt`. Review-only and prompt-only do not take a full-song plan.
6. Do not copy lyric rules into this command. The skill, spec, and series concept are the SSOT.

## Verification

```bash
python3 wavvy.py lyrics-skill SERIES/[series] --json
python3 wavvy.py lyrics-skill SERIES/[series] --artifact <full-song-record> --mode full-lyric-draft --draft-scope full-song --json
python3 wavvy.py gate SERIES/[series] --stage lyrics-review --artifact <full-song-record> --mode full-lyric-draft --draft-scope full-song --json
```

## Output Contract

Return the sections defined by `skills/wavvy-lyricist/SKILL.md`: Source Map,
Constraint Freeze, Lyric Strategy, Draft or Findings, Self-Gate, and Verdict.
For `review-only`, use `--mode review-only` and keep the review artifact separate from the reviewed lyric file. The source hash and exact lyric quotes belong in `Findings`. If the user wants finished lyrics, deliver the `Draft` lyric rows without the working review record. For an excerpt, use the same artifact commands with `--draft-scope excerpt`; the full-song duration plan is not required. A package-only PASS checks installation, not lyric quality. A full-song PASS checks the declared section plan and bound text, not generated audio duration.
