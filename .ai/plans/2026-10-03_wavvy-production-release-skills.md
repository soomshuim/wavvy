# Wavvy production and release skills

Date: 2026-10-03
Status: implemented with release preflight additions; first live series run pending

## Goal and confirmed decisions

- Turn the observed 17:00 workflow into short, reusable skills and a thin coordinator that Claude and Codex can both use.
- After a series is ready for video, start thumbnail drafting automatically. Present the small image draft to 젠; create the final background and typographic thumbnail only after approval.
- Only the explicit `/wavvy-produce` (Claude) or `-wavvy-produce` (Codex) command starts the new-series batch. It first proposes a series time and main musical theme for 젠's feedback, then asks for two or three reference songs or a choice to proceed without them. After that direction is settled, draft all 20 track sources, create/select the Suno `[HH:MM]` folder for the agreed time, and generate the candidates inside it before 젠 listens and chooses what to keep or regenerate. A natural-language idea or project load does not start the batch.
- Only `/wavvy-release` or `-wavvy-release` starts the full release pipeline. Its thumbnail skill starts automatically after that command, with the visual approval pause retained.
- Keep the existing `wavvy.py` media and state gates as the deterministic core. Do not create a second packer.

## Precedent

- `skills/wavvy-lyricist/SKILL.md` and `.claude/commands/write.md` are the repository's shared skill/command pattern.
- `MASTER/WORKFLOWS.md` currently requires source txt first and per-track user confirmation before Suno submission. The new batch path needs an explicit exception for post-generation listening and approval; the existing sequential path remains valid.
- `SERIES/17-00/input/download-manifest.json` binds the 20 delivered WAV files to titles, durations, and hashes. `wavvy.py validate`, `pack`, `gate`, `finalize-upload`, and `state` already cover the media package.
- `SERIES/17-00/input/thumb.jpg` uses the channel logo, time, and a large scene title. The 15:00 precedent's tiny bottom sentence was removed from 17:00 for mobile legibility.
- Taste's applicable core is brief inference, existing brand audit, deliberate layout/typography/color, real imagery, anti-template discipline, and final visual inspection. Web components, motion, and responsive code do not apply to a still thumbnail.

## Thin components and consumers

| New artifact | Responsibility | Consumer and time |
|---|---|---|
| `skills/wavvy-suno-batch/SKILL.md` | Propose time/theme, receive feedback and references, draft 20 distinct txt sources, run gates, generate Suno candidates, present listening selection | Explicit produce command and its active continuation; release begins only after selected recordings exist |
| `skills/wavvy-audio-ingest/SKILL.md` | Download chosen WAVs, bind exact title/order, probe audio, create and check a manifest | `wavvy-release` after listening selections |
| `skills/wavvy-thumbnail/SKILL.md` | Brief read, small image draft, approval, final visual and typography, mobile check | `wavvy-release` automatically before full render |
| `skills/wavvy-thumbnail/references/taste-adaptation.md` | Maps relevant Taste principles to static Wavvy imagery | `wavvy-thumbnail` during design and preflight |
| `skills/wavvy-youtube-publish/SKILL.md` | Draft/final metadata, private upload, scheduling, post-publication verification/comment | `wavvy-release` after render and upload-ready gates |
| `skills/wavvy-release/SKILL.md` | Call the four skills and existing Wavvy CLI in order; pause at the image review | Project router and shared command when a finished series is packaged |
| `.claude/commands/wavvy-release.md`, `.claude/commands/wavvy-produce.md` | Required start entrypoints for Claude `/...` and Codex `-...` | Explicit user invocation; no duplicated domain rules |
| `MASTER/WORKFLOWS.md` batch exception | Authoritative source policy for draft-before-listening mode | `wavvy-suno-batch` and both agent runtimes |
| `AGENTS.md` and `CLAUDE.md` router rows | Route the explicit command to the shared skills in both runtimes | Both agents at project load |

## Flow and evidence

1. **Produce on explicit command:** propose time/theme -> 젠 feedback -> 2–3 reference songs or no-reference choice -> concept brief and series arc -> 20 txt sources -> existing prompt/lyric gates -> active Suno `[HH:MM]` workspace -> candidates recorded with that workspace -> listening decisions. Keep rejected candidates and unapproved text out of `concept.md` final sources. Project load and ordinary chat are not production commands.
2. **Release on explicit command after recordings are selected:** chosen 20 WAV files -> manifest and hash/probe check -> small visual draft -> 젠 approval or revision -> final image and thumbnail -> existing preview/pack/gates -> actual report timestamps and metadata -> private upload/schedule -> verify persisted metadata, publication, and comment result.
3. Use the user's chosen browser product and connection method. A browser UI change is a visible stop with evidence, not permission to switch tools.
4. Record what is verified and what is still pending. A scheduled publication or local comment job is not a posted video/comment result.

## Verification

- Five new skill packages passed `quick_validate.py`; shared Claude `/wavvy-produce` and `/wavvy-release` plus Codex `-wavvy-produce` and `-wavvy-release` command files and router paths exist. Runtime command recognition awaits an actual new-series/release invocation.
- `AGENTS.md` and `CLAUDE.md` are byte identical (`cmp` exit 0).
- Existing harness: `py_compile` PASS, 41 unit tests PASS, `doctor --json` PASS, current `SERIES/17-00` state check and uploaded gate PASS, `git diff --check` PASS.
- Independent Astra xhigh review of the initial skills and wiring, then fresh isolated review of the explicit-command, feedback, and `[HH:MM]` workspace correction: both CLEAN, Critical/High 0, principle observations none. Trigger/Structure/Steering/Pruning reviewed; real behavior remains unverified until live use.

## 2026-10-03 review follow-up

- Added `prepare-subtitles` between `finalize-upload` and `upload-ready`. It takes finalized lyrics from `concept.md`, omits structure/instrumental directions, repeats them according to `report.json`, and preserves an existing edited file on mismatch.
- Added `verify-release` before YouTube upload. It compares actual WAV SHA-256, order, title, and duration with `download-manifest.json` and `report.json`; where Suno candidate records exist, it checks the chosen ID and source txt hash. It also compares title/description/tags and every chapter start/title with `upload.csv` and report-derived timing.
- Added a concrete `launchd` comment follow-up contract under `skills/wavvy-youtube-publish/references/comment-followup.md`: unique job, registration check, status JSON and paths, exact-text existence check before every post, bounded retry and recovery, and live-page verification before marking posted/pinned. The 17:00 job remains untouched.
- Tests: 44 harness unit tests, py_compile, doctor, and read-only `verify-release SERIES/17-00` PASS. Fresh isolated Astra xhigh review checked the new functions, release skills, and existing state/gate interaction: CLEAN, Critical/High 0, principle observations none. A new release's browser upload, scheduled comment runner, and live channel behavior remain untested until first use.

## Limits

- No new series has been provided for a live 20-song Suno generation run. Browser generation and choice quality therefore remain unverified until the next actual series.
- 젠은 다음 실제 적용 대상으로 180 BPM 러닝곡 시리즈를 예고했다. 이는 향후 `-wavvy-produce`/`/wavvy-produce` 호출 때 시작할 첫 파일럿이며, 이번 턴의 생성 승인이나 시작 신호가 아니다. 그 실행에서 얻은 근거로 스킬·하네스를 다듬는다.
- Publication/comment verification for 17:00 is still pending its scheduled time; the new skill must report this separately from upload completion.
