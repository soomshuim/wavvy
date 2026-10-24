# Wavvy SSOT Contract

Version: 1.1
Last Updated: 2026-05-22
Purpose: 하네스가 문서/상태/산출물 충돌을 판정하기 위한 단일 기준

---

## Conflict Order

| Priority | File / Artifact | Owns | Notes |
|---|---|---|---|
| 1 | `.ai/state.json` | active series, phase, next action, local artifact availability, current authoritative doc pointers | Machine-readable resume contract. Written only by `python3 wavvy.py state --write`. |
| 2 | `SERIES/[series]/concept.md` | per-series concept, YouTube metadata, Final Track Sources or Final Selected Audio Sources declaration | Vocal source archive after `finalize-upload`; instrumental selection archive must point to its manifest. |
| 2a | `SERIES/[series]/input/final-selected-audio-sources.json` (explicit instrumental opt-in only) | selected candidate IDs, WAV hashes, actual starts, and raw-prompt confirmation status | Checked against final selection, download manifest, report, source evidence, and WAV files. Unknown raw prompts stay `unverified`. |
| 2b | `SERIES/[series]/input/subtitles.json` (timed vocal subtitles) | render report, approved timing map/SRT hashes, and separately observed manual-caption publication | `verify-subtitles` checks it against final lyrics, render timing, retained source evidence, and publication observations. |
| 2c | `SERIES/[series]/production/final-premixed-audio.json` (explicit instrumental retained-premix opt-in only) | current premix/JPG identity, retained producer evidence, actual 40-entry timeline, and declared video/record identity | Requires `concept.md ## Final Premixed Audio`; does not claim deleted individual WAVs are present or generation prompts are confirmed. |
| 3 | `SERIES/[series]/output/report.json` | technical track durations, hashes, processing params | Local generated artifact. Regeneratable by `pack`. |
| 4 | `MASTER/ai/RUNTIME_RULES.md` | runtime hard constraints, media execution cautions, approval/safety rules | Entry files route here; workflow details still live in `WORKFLOWS.md` / `cli/SPEC.md`. |
| 5 | `MASTER/MANAGER.md` | quality gate hierarchy | Conservative fail when no lower rule applies. |
| 6 | `MASTER/WORKFLOWS.md` | operational workflow rules | txt-first, finalize-upload, packaging order. |
| 7 | `MASTER/youtube/YOUTUBE.md` | YouTube title/description/tag format | Final metadata lives in series concept. |
| 8 | `wavvy.md` | brand identity and global defaults | Per-series overrides must be explicit. |
| 9 | `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md` | Wavvy lyric skill output schema, self-gate contract, and static harness acceptance baseline | Subordinate to series concept, `MASTER/lyrics/LYRICS.md`, and brand docs. Routes to `skills/wavvy-lyricist/SKILL.md`. |
| 10 | `.ai/HANDOFF.md` / `.ai/SESSION.md` | historical handoff/session archive | Read newest-first; not the active-state SSOT. |

`MASTER/ai/RUNTIME_RULES.md` is priority 4 because runtime hard constraints and approval/safety rules are absolute execution bounds; `MASTER/MANAGER.md` remains the conservative-fail quality gate fallback inside those bounds.

---

## Phase Contract

| Phase | Definition |
|---|---|
| `concept_draft` | Concept exists but source work is incomplete. |
| `track_source_draft` | Track txt/source prompt work is active. |
| `source_final` | Audio, metadata, report, and verified Final Track Sources, instrumental Final Selected Audio Sources, or instrumental Final Premixed Audio are final enough for upload prep. The premix's retained production manifest is its report; it does not fabricate `output/report.json`. |
| `render_final` | Rendered video and upload CSV exist and match the current report. |
| `upload_ready` | Rendered video and upload support artifacts are present. Vocal releases need subtitles; videos longer than one hour need a validated timed SRT (`verify-subtitles --stage prepared`). A verified instrumental selection archive exempts lyric subtitles. |
| `uploaded` | YouTube video upload is complete; this phase does not assert manual subtitle publication. Large local render artifacts may be deleted if upload completion is recorded in `concept.md`. |

`output/final.mkv` absence is a blocker for `render_final`. It is also a blocker for `upload_ready` unless upload completion is already recorded. It is not a blocker for `source_final` or `uploaded`.

The explicit retained-premix path uses its declared MP4 instead of `final.mkv`. Its source gate verifies the current two-cycle AAC, approved JPG, preserved 20-source identity/hash evidence, and 40 actual starts without requiring a video. Render/upload gates additionally require the bound render record, 4K video, complete unchanged AAC packets/timing, 40 embedded chapters, and matching CSV/metadata. For a corrected two-cycle producer, retained evidence separately binds selected candidate IDs, reacquired original WAVs, correction outputs/records, independent beat records, and the actual transition-chunk timeline. Historical individual-WAV hashes remain historical evidence; their existing gate is unchanged. Unknown generation prompts remain `unverified`. `pack` refuses this opt-in because mixing or repeating again would change the retained master. After recorded upload completion, the declared video/CSV, premix, and corrected producer’s original/corrected WAVs may be absent under an approved retention decision. Retained file paths and hashes must still agree across source and correction records; existing media must still match their hashes. The retained manifests, analysis/correction/beat records, producer scripts, configuration, and render records must remain.

---

## Per-Series Overrides

Global brand defaults in `wavvy.md` apply unless a series explicitly names an override in its `concept.md`.

Examples:

- A hip-hop series may allow code-switching or genre-specific meta tags if the concept documents the exception.
- A time-slot series may alter upload positioning if its YouTube metadata block states the final positioning.

Implicit overrides are not valid. If a global rule and a series concept conflict without a named override, `MASTER/MANAGER.md` conservative fail applies.

Compilation / best-album series may use a `concept.md` `## Track Selection` table as the audio source map. In that case, `SERIES/[series]/input/tracks/` is only a local staging directory for materialized copies; it may be empty or absent when every `Source` path in the table resolves to an existing audio file. The compilation filename in `Copied Filename` remains the report/upload-facing filename.

Wavvy lyric drafting and review tasks should use `skills/wavvy-lyricist/SKILL.md` and the contract in `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`. These files do not override the target series concept or `MASTER/lyrics/LYRICS.md`; they define the agent workflow, output sections, and `lyrics-review` harness expectations.

---

## State Writer Rule

`.ai/state.json` must be written only by:

```bash
python3 wavvy.py state SERIES/[series] --write
```

The writer uses temp-file plus atomic rename. Agents should not edit `.ai/state.json` manually.
The `authoritative_docs` list in state should mirror the current conflict-owner docs in this file, plus the active series `concept.md`.

`.ai/HANDOFF.md` remains append-only because agent-center hooks still read it. State augments handoff; it does not replace hook behavior yet.

---

## Initial Drift Rules

`python3 wavvy.py state SERIES/[series] --check` should warn or fail on these conflicts:

1. `concept.md` has `## Final Track Sources` but status/TODO text still says `draft`, `DRAFT`, or `Suno 생성/검수`.
2. `.ai/state.json` phase is `source_final` or later but `concept.md` lacks a valid `## Final Track Sources` archive, verified instrumental `## Final Selected Audio Sources`, and verified instrumental `## Final Premixed Audio`.
3. `.ai/state.json` next action mentions upload/render while render artifacts are missing:
   - warning for `source_final`
   - blocker for `render_final` / `upload_ready`
   - no warning for `uploaded` when upload completion is recorded

---

## Artifact Policy

Tracked:

- source docs
- concept docs
- rubric/reference docs
- state contract
- peer review records when needed for audit

Ignored/local:

- large media
- `work/`
- most `output/`
- regenerated render artifacts

If an ignored artifact becomes required for resume, state must record its availability and regeneration command.

After YouTube upload, `output/final.mkv` and `output/upload.csv` may be deleted for disk space. The series `concept.md` must then record upload completion so gates can distinguish intentional retention cleanup from an incomplete render.

Use a dedicated `## Upload Status` section with `- YouTube upload: not uploaded yet` before upload and `- YouTube upload: completed` only after observing a successful upload. Keep the observed date, video URL/ID, and raw evidence alongside that field. Existing explicit `YouTube upload completed` / `YouTube 업로드 완료` keys in this section remain recognized. Empty, conflicting, or duplicate status sections do not prove completion. Without this section, only the legacy dedicated `> **YouTube**: <published YouTube URL>` marker is recognized; completion words in prose, metadata, TODOs, or reference-video links are never upload evidence. An explicit pending status overrides a legacy URL marker.
