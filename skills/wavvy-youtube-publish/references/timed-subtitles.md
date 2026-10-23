# Timed subtitles for an existing Wavvy video

Use this path for a subtitle-only change on an existing video and for timed-subtitle preparation before uploading a vocal video longer than one hour. For an existing video, confirm its identity and approved lyric source. Keep its title, description, visibility, video, and comments unchanged unless separately requested. A subtitle follow-up does not require a new title approval or video upload.

## Build from evidence

- The approved lyrics control the words. Automatic speech recognition (ASR) can suggest timing or reveal a sung repeat, but its misheard text must not overwrite the lyrics. Keep the source unchanged. Add a displayed repeat only when the same approved words are supported by actual source evidence; retain that mapping.
- Compare the whole song structure and each repeated pass, not only lines with weak ASR matches. Use the render report's actual track starts and repeat offsets, including crossfades. Rounded chapters and a simple sum of WAV durations are not reliable subtitle offsets.
- Anchor the lines to observed vocal intervals. Do not interpolate across a long instrumental or silent stretch, or place an inferred start outside the supporting observation without flagging and resolving it. Short music-only clips can produce ASR hallucinations; check sufficient surrounding context and retain the raw timing evidence. Do not claim human listening that did not happen.
- Produce a UTF-8 SRT with consecutive cue numbers and `HH:MM:SS,mmm --> HH:MM:SS,mmm` times. Check approved wording and order, evidence-backed extra repeats, positive and readable cue lengths, no overlaps, and bounds within the video. For repeated audio, verify the same text and the actual repeat offset. Timing inferred from ASR remains an estimate, even after these checks.
- Keep the original untimed lyric text as source. First make an explicit timing map with every track's approved source-line occurrences, relative millisecond cues, anchor labels, observed bounds when available, and hashes of retained audio evidence. Before generation, `input/subtitles.json` needs the render report and timing map paths plus SHA-256 hashes, and the SRT destination path. `output_cues`, `srt_sha256`, and `original_source_sha256` in the map are optional; if present, the command checks them. Run `python3 wavvy.py prepare-subtitles SERIES/[series] --timing-map <checked.json>` to derive all rendered-pass cues from the report, generate the SRT, and record the final SRT and lyric-source hashes in the manifest. It refuses to overwrite a different existing SRT and does not infer a complete map from ASR. Then run `python3 wavvy.py verify-subtitles SERIES/[series] --stage prepared --json`; this requires the recorded hashes. Resolve a failure before a long vocal video is uploaded. A generated SRT is prepared evidence, not publication evidence.

The minimal shape is below; these are field examples, not measured timings or usable hashes. Include every report track and every sung source-line occurrence in the real map. Evidence paths are relative to the timing-map directory. `anchor_classes` is required; without `last_asr_end_ms`, it must include `estimated`, `interpolated`, or `independent_whisper`. When a sung line repeats inside a pass, add `allowed_added_source_lines_per_pass` to the map and matching `required_extra_occurrences` plus `repeat_evidence` to the manifest. See the retained [17:30 manifest](../../../SERIES/17-30/input/subtitles.json) and [checked timing map](../../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.json) for a complete case.

`input/subtitles.json` before generation:

```json
{"schema":"wavvy.subtitles.v1","report":{"path":"output/report.json","sha256":"<64 hex digits>"},"timing_map":{"path":"input/timing-map.json","sha256":"<64 hex digits>"},"srt":{"path":"output/youtube_subtitles_ko_timed_estimated.srt"}}
```

One track and cue in `input/timing-map.json`:

```json
{"schema":"wavvy.subtitle-timing.v1","audio_evidence_sha256":{"audio-probe/01-words.json":"<64 hex digits>"},"tracks":[{"track":1,"cues":[{"relative_start_ms":3320,"relative_end_ms":7674,"last_asr_end_ms":8000,"anchor_classes":["direct_cue"],"source_line_occurrences":[{"source_line":1,"occurrence":1,"text":"<approved lyric line>"}],"texts":["<approved lyric line>"]}]}]}
```

## Publish and verify

Use the browser product and connection method 젠 specified. In the existing video's subtitle editor, upload the SRT **with timing** and check that timed lines appear before publishing. Publish once and then verify both Studio's manual-language status (`게시됨`) and the public watch page's manual-language option and visible text at sampled positions. Keep an automatically generated language track separate from the manual track. When available, download the published manual SRT and compare its content and times with the validated file; identical bytes or a trailing newline difference are accepted. Record the observed published manual-track evidence in the series subtitle manifest, including SHA-recorded `studio_raw` and `public_menu_raw` text for the target video and SHA-recorded public raw snapshots showing each sampled lyric. Then run `python3 wavvy.py verify-subtitles SERIES/[series] --stage published --json`. Sample the actual first and last SRT cues plus a middle cue; when the report has repeated passes, sample a repeat as well. The `uploaded` video phase does not assert that manual captions are published.

If the same error recurs without changed evidence or conditions, stop repeated identical clicks and record the observed result. A different evidence-based method within the user's existing approval may be used. An unresolved error is not publication.

[YouTube's subtitle upload help](https://support.google.com/youtube/answer/2734796?hl=en-CA) describes the timed-file route and does not recommend automatic transcript synchronization for videos over one hour. That guidance does not establish the cause of any particular upload error. [YouTube's supported-file help](https://support.google.com/youtube/answer/2734698?hl=en-CA) lists plain UTF-8 SRT as a supported format.
