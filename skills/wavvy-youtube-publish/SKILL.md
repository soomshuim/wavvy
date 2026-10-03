---
name: wavvy-youtube-publish
description: Prepare, upload, schedule, and verify a finished Wavvy playlist on YouTube. Use from wavvy-release after the package passes upload-ready, or when 젠 asks to publish an already finished Wavvy video. For artwork use wavvy-thumbnail.
---

# Wavvy YouTube Publish

Trigger: model-invoked after a release package is ready. The user's release request authorizes the requested upload; ask only for a publishing choice that the request and series concept do not resolve.

## Steps

1. Read `MASTER/youtube/YOUTUBE.md`, the target `concept.md`, and at least two completed series descriptions. Use `output/report.json` for actual track starts, including repeat and crossfade effects. Finalize and check the title, description, tags, thumbnail copy, and proposed pinned comment against the series direction. Write the approved final metadata to the concept and `output/upload.csv`; run `python3 wavvy.py verify-release SERIES/[series] --json` to compare metadata, chapters, report, approved candidates, and WAV hashes.
2. Run `python3 wavvy.py gate SERIES/[series] --stage upload-ready --json` and check the intended upload file with `ffprobe`. Verify resolution, duration, audio stream, chapter count and starts. Stop on a failed gate or a missing file.
3. Use the browser product and connection method 젠 specified. Confirm the signed-in channel identity. Upload privately, apply the checked metadata, thumbnail, audience and disclosure settings, and any available transcript. Reopen the YouTube draft and verify that each field persisted. Record the URL and processing/copyright state as observed, without converting pending into passed.
4. Schedule or publish at the time 젠 supplied. If no public time was given, keep the upload private and ask for that one choice. Reopen the visibility control to verify the saved local date, time, timezone, and status.
5. After release, verify the public watch page. Post and pin the approved comment only when comments are available, then verify the visible posted/pinned result. If publication is in the future and a comment was requested, follow `references/comment-followup.md`: register and inspect a durable local job, persist its identity and status paths, and make each attempt check for an existing exact comment before posting. Job registration is not proof of posting. Check later processing or subtitle status when it was still pending at upload time.
6. Update the series concept and `.ai/state.json` only with observed outcomes, then use the relevant uploaded gate. Keep large generated media under the local artifact policy in `MASTER/SSOT.md`.

## Boundary

Do not substitute a different browser connection after a specified path fails. Do not claim publication, comment pinning, copyright clearance, or subtitle publication from an upload/schedule screen alone.
