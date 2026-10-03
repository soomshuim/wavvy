# Scheduled comment follow-up

Use when a Wavvy video is scheduled for later publication and 젠 requested a comment. The 17:00 precedent used a macOS `launchd` job, a per-video script, and a status JSON under `~/Library/Application Support/Wavvy/`. Reuse that operating pattern. Do not edit or restart another series' job.

## Before registration

1. Confirm the saved YouTube video ID, signed-in channel, public time with timezone, and exact approved comment text from the concept. Record a SHA-256 of the exact text. Never infer these from a draft title alone.
2. Set a unique job label containing series and release date, for example `com.wavvy.1700-comment.20261003`. Set stable absolute paths for its script, plist, stdout/stderr logs, and status JSON. Save a job record in the series concept with these paths, video ID, target time, timezone, comment hash, and current status `scheduled`.
3. Write a one-video runner using only the browser product and connection method chosen by 젠. The runner must first verify the watch page is public and the signed-in account owns the Wavvy channel. It must inspect comments by that channel for the **exact** approved text before it posts. A title fragment or first-line marker alone is insufficient. If the exact text exists, skip posting and inspect its pin state. If the page cannot prove absence, record `verification_unavailable` and stop that attempt without posting. After a click with an uncertain response, re-read the page before any retry.
4. The runner writes the status JSON after every attempt: `video_id`, `comment_sha256`, `time_kst`, `attempt`, `result` (`wait_public`, `verification_unavailable`, `posted_unpinned`, `posted_pinned`, `failed`, or `deadline_reached`), and `comment_id` or `comment_url` when the browser exposes one. Never set `posted_*` from a submit click alone. Preserve logs. A later run reads the status file and the live page; it does not blindly submit again. If the exact comment already exists, a missing comment ID does not justify reposting.

## Register and check

1. On macOS, create a `~/Library/LaunchAgents/<label>.plist` with `ProgramArguments` for the runner, `StartCalendarInterval` shortly after public time, explicit `HOME` and `LANG`, and log paths. Set a bounded retry window in the runner. If a job with the same label exists, inspect its video ID and comment hash before reusing it; do not stack duplicate jobs.
2. Run `launchctl bootstrap gui/$(id -u) <plist>` once, then `launchctl print gui/$(id -u)/<label>` to confirm the job is registered and its next run is represented. If bootstrap reports already loaded, inspect the existing job rather than treating that message as success or registering a second one. Record the actual command result and status path in the concept.
3. Before leaving the release, run the runner in a no-post check mode against the target page. Before public time, `wait_public` is expected. A wrong account or wrong video fails registration verification and must be fixed. Registration plus no-post check means `scheduled`, not `posted`.

## Resume after publication

1. Read the status JSON and `launchctl print` result. If the status is missing or stale after target time, inspect stdout/stderr logs, confirm the Mac was awake and the job ran, then launch the **same** runner once after its live-page preflight. Keep the original job identity so a recovery cannot create duplicate schedules.
2. Check the visible public comment and pin state on the watch page. Record the verified comment ID/URL when available, the observed result time, and whether it is pinned in the concept and `.ai/state.json`. A local `posted_pinned` status without a live-page check remains pending verification.
3. If the job cannot recover within its bounded window, record `deadline_reached` and report the remaining manual dependency. Preserve status and logs for diagnosis.
