# [06:30] Suno browser preflight

Observed 2026-10-21 KST. This file records the live Suno UI state before any [06:30] song submission.

## Browser route and account

- Required route: Aside / MCP. First actual browser call: `mcp__aside__repl` using `listBrowserTabs()`; no Suno tab existed then.
- Created Aside tab target ID: `C3E4D56DFD255047841F3ACAB8E9B6A4`. Existing user tabs were left open.
- Signed-in non-sensitive account display: `wavvy24`. Current plan: Pro. UI displayed 2,636 credits remaining and 3 song downloads remaining.
- No purchase, upgrade, song edit, deletion, download, or generation occurred.

## Workspace

- Workspace search for `[06:30]` returned `No workspaces found.`
- Created workspace `[06:30]`, then selected it. Active URL: `https://suno.com/create?wid=4a61c72f-425f-4e82-98b9-2abc0577920c`.
- Final UI check: workspace heading `[06:30]`, form `Save to... [06:30]`, table `No songs found`, credits 2,636, Create disabled with empty inputs.

## Generation UI

- Current UI labels: `Songs` and `Advanced` are selected; the form does not call this mode `Custom`.
- Current model is `v6`. Model chooser also lists `v6-wild` and `v6-mini`.
- Form has separate Lyrics editor, Styles, Exclude styles, optional Song Title, and `Save to...` workspace picker.
- `More Options` has Vocal Gender, Duration (`Auto` or `Custom`; Custom exposed a 3:00 field and slider), Max Mode, Weirdness, Style Influence, Variety, and Personalize. Max Mode `Off` had DOM `data-selected="true"`; `On` had `false`.
- No numeric BPM/Tempo lock input appeared in the full Advanced form or More Options. Prompt text alone cannot establish that output audio is exactly 175 BPM; generated audio must be measured.
- Per-submission credit cost was not displayed on the empty Create button, nor after temporarily entering Style text to enable it. The temporary text was cleared and no submission was made. The exact cost remains unobserved.
- The preflight click on Duration `Custom` exposed 3:00; the eventual 3:00–3:15 setting is pending source bar-plan guidance.

## Candidate preview and download route

- Read-only inspection used an existing `[07:00]` song, then returned to `[06:30]`. Preview playback worked. Its live audio element used a `blob:https://suno.com/...` source; the second audio element was a short silence MP3. No direct HTTP preview media URL was visible in the inspected DOM, so no `fetch()` download was attempted.
- Existing song menu `More options > Download` opened a dialog with M4A, MP3, WAV, and MP4 video asset choices. No format was downloaded. The inspected existing song showed `You've unlocked this song`; that does not establish whether downloading a new candidate consumes one of the 3 remaining download allowances.
- One read-only fetch of that already-observed `blob:https://suno.com/...` URL in the page context returned `TypeError: Failed to fetch`. No retry or other endpoint was used. The preview did not expose a directly readable audio file this way. Before and after, the player was paused at 27.345057 seconds and the active page stayed on `[06:30]`.
- To measure BPM across new candidates, first check each generated candidate's UI for a usable preview or allowed download path. Do not spend the 3 remaining song downloads on all candidates. If the only source is a blob preview and official download consumes allowances, report that limitation rather than asserting an audio BPM.

## Handoff

- Keep `[06:30]` active and check both workspace heading and `Save to...` before each submission.
- Wait for the 20 new source txt files, their hashes, and controller review pass. Submit one initial generation per track only after that signal; do not silently retry credit-consuming submissions.
