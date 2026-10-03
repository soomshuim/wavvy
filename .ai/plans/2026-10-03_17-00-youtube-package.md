# 17:00 YouTube package

Date: 2026-10-03
Status: Uploaded privately; YouTube processing pending

## Requested result

- Save all 20 finished songs from the Suno `[17:00]` workspace as WAV.
- Use the approved autumn street image for a 3840×2160 static video and a series-consistent thumbnail.
- Build and verify the full playlist with the Wavvy harness.
- Put actual track start times into the YouTube draft, then review the title and description.

## Result

1. `input/download-manifest.json` records all 20 48 kHz, 16-bit stereo PCM WAV files, their approved titles, durations, SHA-256 hashes, and source names. 젠 downloaded 08 `취향` directly; Codex downloaded the other 19 through the approved Aside CLI. Suno also initiated incidental M4A downloads for locked tracks; no M4A was used.
2. `input/loop-4k-candidate-v1.png` is a 3840×2160 upscale of a 1672×941 generated image. `input/loop.png` is the ignored video background copy. `input/thumb.jpg` is the series-consistent thumbnail candidate. The image is not native 4K detail.
3. The 30-second preview was inspected. The final `output/final.mkv` contains 20 tracks twice, -14 LUFS normalization, -1 dBTP ceiling, and 0.8-second audio crossfades. The YouTube upload copy `output/final.mp4` retains the H.264 image stream and encodes audio to AAC 384 kbps. Both are 3840×2160 and about 02:07:38 long. These large media files remain local and ignored by Git.
4. `concept.md` and `output/upload.csv` contain the 80-character playlist title, full description, tags, and 40 chapter starts derived from `output/report.json`. `output/upload.csv` points to `output/final.mp4` and remains private. `finalize-upload --keep-txt` archived all 20 sources into `concept.md` without deleting the source txt files.
5. The user corrected `Accoustic` to `Acoustic` in 02, 04, and 07 across source titles, filenames, manifest, report, and YouTube metadata. The source recording bytes did not change. Source drafting status through 2026-10-02 is preserved in `archive/2026-10-02-source-progress.md`.

## Verification

- `python3 wavvy.py validate SERIES/17-00`: PASS, 20 audio files.
- `python3 wavvy.py gate SERIES/17-00 --stage source-final --json`: PASS.
- `python3 wavvy.py gate SERIES/17-00 --stage render-final --json`: PASS.
- `python3 wavvy.py finalize-upload SERIES/17-00 --check`: PASS.
- `python3 wavvy.py state SERIES/17-00 --check --json`: PASS with no warnings after current status correction; durable phase write pending final review.
- `python3 -m unittest tests/test_harness.py`: 41 tests PASS; py_compile PASS; doctor PASS with an optional drawtext binary warning.
- `final.mp4` ffprobe: H.264 3840×2160, AAC 48 kHz stereo, duration 7658.0s. Video/audio decode at 0s, 3800s, and 7656s PASS.
- Direct audit: 20 WAV SHA-256 values and titles match manifest/report; all 40 description chapters match calculated starts; CSV description matches concept; title is 80 characters.
- At the time of the package review, `upload-ready` was FAIL because no subtitle artifact existed and `uploaded` was FAIL because upload had not occurred. The later upload execution below supersedes those gate results. Independent Astra xhigh package review: CLEAN, Critical/High 0, principle observations none. Reviewer compared audio at all 40 chapter starts with the source tracks and reported minimum waveform similarity 0.999569.

## Publishing boundary

The YouTube upload is private. Local media is excluded from Git, so a remote clone does not contain the video or WAVs.

## Upload execution (2026-10-03)

- Browser selection: user-approved Aside CLI; actual browser tool `aside repl` on the local Aside browser. No alternate browser connection is authorized.
- Visibility: private, following `output/upload.csv`. Apply the existing title, description with 40 chapters, tags, and thumbnail.
- A 20-song twice-through untimed transcript is available locally at `output/youtube_subtitles_ko_no_timing.txt`; `upload-ready` gate passed before upload.
- Uploaded `output/final.mp4` to Wavvy24 as `https://youtu.be/KGzllkCkozw` and saved it private. YouTube Studio confirmed upload complete; SD and 4K processing and the copyright check had not completed at the last inspection.
- Verified the persisted title, exact description with 40 chapter starts, uploaded thumbnail, all 25 tags, not-made-for-kids selection, and AI-use disclosure in YouTube Studio.
- Submitted the untimed Korean transcript. Publishing the auto-synced subtitles failed while the video was still uploading, then YouTube confirmed the transcript was saved as a draft. Its timing and publication need a later check after processing.
