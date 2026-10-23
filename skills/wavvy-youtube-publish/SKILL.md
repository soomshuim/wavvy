---
name: wavvy-youtube-publish
description: Prepare, upload, schedule, and verify a finished Wavvy playlist on YouTube, or add timed subtitles to an existing published Wavvy video. Use from wavvy-release after the package passes upload-ready, or when 젠 asks to publish or caption a Wavvy video. For artwork use wavvy-thumbnail.
---

# Wavvy YouTube Publish

Trigger: model-invoked after a release package is ready. The user's release request authorizes the requested upload; ask only for a publishing choice that the request and series concept do not resolve.

For a subtitles-only follow-up on an existing video, use [`references/timed-subtitles.md`](references/timed-subtitles.md). Keep that work on the existing video; do not restart this full-upload sequence, ask for title approval again, or repost a comment.

## Steps

1. Read `MASTER/youtube/YOUTUBE.md`, the target `concept.md`, and at least two completed series descriptions. Use `output/report.json` for actual track starts, including repeat and crossfade effects. For a new time-slot title, use the six-part default: `Playlist | {series-specific sensory image + music hook + emoji} | {actual genres} | {suitable uses} | Wavvy | {HH:MM}`. The approved 17:30 title in `YOUTUBE.md` is the writing precedent, not copy to reuse; retain approved individual exceptions such as 07:00 and time-free compilations. Check genre and uses against the selected music, and keep the whole title within 100 characters. Finalize the description, tags, thumbnail copy, and proposed pinned comment against the series direction. Before changing an existing YouTube title, show 젠 the exact final title; for a batch, show one video-to-title list. Apply titles 젠 already specified or approved, then write the final metadata to the concept and `output/upload.csv`; run `python3 wavvy.py verify-release SERIES/[series] --json` to compare metadata, objective title form, chapters, report, approved candidates, and WAV hashes.
2. For a vocal video longer than one hour, follow [`references/timed-subtitles.md`](references/timed-subtitles.md) to prepare and verify the timed SRT before upload. Run `python3 wavvy.py gate SERIES/[series] --stage upload-ready --json` and check the intended upload file with `ffprobe`. Verify resolution, duration, audio stream, chapter count and starts. Stop on a failed gate or a missing file.
3. Use the browser product and connection method 젠 specified. Confirm the signed-in channel identity. Upload privately and apply the checked metadata, thumbnail, audience and disclosure settings. For a long vocal video, upload the verified timed SRT **with timing**; for shorter vocal videos, use the available approved subtitle source. Reopen the YouTube draft and verify that each field persisted. Record the URL and processing/copyright state as observed, without converting pending into passed.
4. Schedule or publish at the time 젠 supplied. If no public time was given, keep the upload private and ask for that one choice. Reopen the visibility control to verify the saved local date, time, timezone, and status.
5. After release, verify the public watch page. Post and pin the approved comment only when comments are available, then verify the visible posted/pinned result. If publication is in the future and a comment was requested, follow `references/comment-followup.md`: register and inspect a durable local job, persist its identity and status paths, and make each attempt check for an existing exact comment before posting. Job registration is not proof of posting. Check later processing or subtitle status when it was still pending at upload time; distinguish a prepared subtitle file from a published manual-language track.
6. Update the series concept and `.ai/state.json` only with observed outcomes, then use the relevant uploaded gate. Keep large generated media under the local artifact policy in `MASTER/SSOT.md`.

## Boundary

Do not substitute a different browser connection after a specified path fails. Do not claim publication, comment pinning, copyright clearance, or subtitle publication from an upload/schedule screen alone.
