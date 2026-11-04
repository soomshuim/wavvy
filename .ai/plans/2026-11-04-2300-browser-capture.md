# 23:00 browser recording and style provenance

User request (2026-11-04): 「자 브라우저 녹음부터 시작하자. 단, 개별 곡의 스타일은 suno에서 리믹스 원곡의 스타일을 찾고 + 리믹스 스타일 프롬프트를 더한 것으로 기록해줘.」

- Scope: the 17 exact songs observed in the user's `[23:00]` workspace on 2026-11-04. Current workspace order is a provisional capture index, not a final album order. The earlier 20-song agent draft remains historical and is preserved.
- Browser: ego lite through `ego-browser nodejs`, TaskSpace 6, playback page p1. No alternative browser connection.
- Precedent: `work/2026-10-25-1930-wish/capture-wish.swift` and `SERIES/19-30/production/capture-analysis-20261026/`. Reuse the ScreenCaptureKit app-audio recorder with an exact ego lite bundle check. Capture excludes microphone and records 48 kHz stereo float32 WAV at source playbackRate 1.
- Start with a short probe. Then record each exact song from time zero through its natural end. Preserve all attempts and raw audio. Log media clocks, identity, rate, natural-end events, recorder timing, hashes, and audio properties. A signal/continuity check is not a musical-quality approval.
- Audio scope is the ego application, not a single tab. Do not change system volume, audio device, or user-owned tabs. Stop on browser control loss, app mismatch, unexpected playback state, or recording errors.
- Read the original and remix Styles on Suno. Preserve each text and URL separately. Combined STYLE is `original style + remix style prompt`, explicitly a reconstruction requested by the user, not verified generation input. Never invent a missing original or infer it from title alone.
- Durable outputs: source catalog, lyrics/style provenance, recording manifest, and series/session status. Large audio and logs stay local/ignored. Existing draft source files and candidate history are retained.
- Verification scope: new recorder/probe, these 17 recordings, and the new provenance records only. Perform one isolated formal review of the new deliverables. No unrelated full-series regression or release work.

## Browser override during execution

- 젠 explicitly requested 「그러면 aside로 시도해봐」, followed by 「suno를 aside  브라우저 첫 탭에 띄워놨어.」. For this task only, audio playback/capture moves to Aside via `mcp__aside__repl`, profile `be41d9e1-db47-4e5c-b567-be8ce72163cc`, first tab target `49405ACFA00DF89F4F32FD5A8096A482`. Ego metadata observations remain their original evidence.
- Aside exact bundle: `at.studio.AsideBrowser`; PID at launch 25877. First verify a short nonzero probe. Preserve ego silent attempts. No automatic change to the project-wide ego default.

## User-added sequence and Suno title numbering

- 젠 requested mixing new and old songs, alternating after the fixed first three and placing remaining old songs consecutively once the new songs run out. Fixed positions: 1 작은 빛, 2 돛, 3 한 잔만 더; later correction: 4 이름, 6 마음 밖. Record exact user messages in `sequence.json`.
- Old cohort = the nine exact IDs in `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json`. New cohort = the other eight IDs in the current 17-song catalog. Preserve workspace order inside each cohort after removing fixed songs. Positions 4–15 alternate old/new; 16–17 are 골목/물결.
- 선례: `SERIES/19-30/production/suno-sequence-numbering-20261026.json` uses `N. existing title`, normal UI edits and reload confirmation. Number these same 17 exact Suno IDs after their capture, retaining their existing titles/suffixes, raw historical evidence and source IDs. This is user-authorized title editing; no new song or publication action.

## Execution records

- `SERIES/23-00/production/browser-capture-20261104/capture-manifest.json`: 17 full-song technical recordings; raw and guarded WAVs stay in local ignored `work/`. Source playback total 3340.12 seconds. No musical-quality approval or final editing.
- `sequence.json` and `suno-sequence-numbering-20261104.json`: selected order and all 17 normal-UI title saves with same-song reopen evidence. Historical capture order is preserved.
- `style-provenance.{json,md}`: three confirmed parent links, eight provisional title/lyric-matched candidates, six user-declared directly created songs with current displayed styles. Exact question/answer scope is in `user-style-clarification.json`.
- Final handoff verification is limited to these 17 new recordings and their sequence/style/title records. Formal isolated review is recorded separately. No unrelated series regression, generation, artwork, release or upload.
