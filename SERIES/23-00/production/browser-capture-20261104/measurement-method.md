# 23:00 browser recording method

This collection implements the user's 2026-11-04 browser-recording request. It is not an official Suno download, a verified copy of Suno's original audio file, or approval of musical quality. The current workspace's 17 exact IDs determine scope. Their observed order is a provisional recording index.

## Playback and recording

- User-authorized route: Aside, MCP `mcp__aside__repl`, first existing user Suno tab. The earlier ego lite trials remain diagnostic evidence. The global ego default is unchanged.
- Native ScreenCaptureKit recording binds to the exact Aside PID and bundle `at.studio.AsideBrowser`. It captures all audio from that application, not a single tab. Only one Aside tab was present at the start. The microphone is excluded. System volume and output-device settings are unchanged.
- For each song, open its exact URL, check its heading and playbar identity, load the song, pause and seek to zero, start the native recorder, attach the DOM media-event observer, then play once at rate 1. Preserve the browser's natural `ended` event. A play guard pauses automatic next-song attempts before they reach `playing`.
- Store the actual media clock and event history, the native buffer timestamps/frame offsets, the raw stereo 48 kHz float32 WAV, and recorder logs. Never overwrite attempts. Native capture closes only after the end evidence is exported.

## Technical checks and boundaries

- Verify source identity, zero start, natural end, normal playback rate, nonzero volume, unmuted playback, no active pause/stall/seek/error, media-clock duration, finite stereo samples, nonzero signal, contiguous file frame offsets, and native timestamps throughout source playback.
- Match the browser's wall clock to the native monotonic clock using the median callback wall-clock minus uptime difference. Estimate the browser source origin from the median of wall-clock minus media position across active samples. Record the 1st–99th percentile spread.
- Map each source boundary to its containing native buffer's timestamp **and frame offset**. Do not assume startup timestamp gaps occupy WAV frames. Reject any timestamp discontinuity intersecting source playback; retain and list discontinuities outside it.
- Track 02 exposed a 15.333 ms timestamp gap before playback, approximately −0.402 to −0.387 seconds relative to the estimated source start. The first 1.2 seconds of its raw file are exactly zero; first nonzero frame is at 1.387396 seconds. The source range has continuous timestamps. This diagnostic corrected an overbroad whole-file check; it did not waive missing audio inside a song.
- Output-device latency is uncalibrated. Retain 0.5 seconds of audio before and 0.75 seconds after the estimated source range. These files are guarded collection copies, not final edits. Preserve all raw audio for later boundary decisions.
- Verify exported WAV samples exactly equal the selected raw float32 sample range. Store hashes for the raw WAV, guarded WAV, timing and browser evidence. List exact-zero interior runs of at least one second as listening flags; do not classify a musical rest as a capture failure without evidence.

## Styles

Preserve original and remix Styles as separate exact texts with their Suno URLs. The requested combined record is the original style followed by the remix prompt. Separately retain minus-prefixed exclusions. An explicit parent link or earlier raw parent-link evidence confirms lineage. Matching title and sung lyrics alone remains provisional. For six songs the user replied 「이건 직접 만든거야.」 to the scoped original-link question. Record their current displayed style without inventing a separate original; preserve the exact question and answer in `user-style-clarification.json`. Eight candidate pairings remain provisional.

The original 20-song agent draft and production ledger remain historical. The new 17-song catalog and recording manifest define this collection. The user later added a final sequence and Suno title numbering. `sequence.json` owns the order; `suno-sequence-numbering-20261104.json` records normal-UI Save and same-song reopen confirmation for all 17 exact IDs. Historical capture indices and raw evidence stay unchanged. No new generation, artwork, release or upload is part of this request.
