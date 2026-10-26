#19:30 final media cleanup — frozen execution plan

- User quote: `4K 영상과 음원도 필요 없어` after formal no-argument `-record` request.
- Scope: exactly29 regular files,6,738,666,640 logical bytes: selected20 original WAVs, final160/170 WAV+AAC (4), final4K MP4 (1), this task Wish references (4).
- Protect:1,529 actual regular files,282,189,649 bytes; images/PSD/JPG/PNG, prompts, raw JSON, scripts, reports, manifests, reviews, source hashes, analysis, earlier cleanup evidence. No other series, CDS, other sessions, or external directories are deletion targets.
- Prior167-file cleanup records and script remain historical and unchanged. Their former final-media retention is superseded only by the user's new explicit request; no old evidence is rewritten.
- Candidate manifest SHA256: `242a58889b40b313998a1a287d4173e7da292383719d57acccf01eb1a717060c`.
- Protected manifest SHA256: `51d50f880707bf8ba553482c67286bc0262ab7051fa7702a2c818717d2c057ab`.
- Execution script SHA256: `138441383a5882d01593fc97f0abbfa4d0cc4b6236117a148e028160c42e3987`.

## Existing gate policy

`wavvy_harness/gate.py` uploaded premix branch enables missing-media inspection only with recorded completed upload. `integrated_premix._Evidence.bound(media=True)` and `wav` allow absent media while hash-bound nonmedia remains mandatory. `premixed_audio.py` permits absent final AAC/render only for uploaded cleanup plus retained render identity. No validator/gate code is changed. Current public ID is `s5pY5cqvbS8`; upload record is `completed_public_comment_pinned`.

## Process safety and narrow read-only exception

Native CUA inventory, Finder AX state and screenshot showed only a Project Finder window, with no identifiable target audio preview. No window was closed and no process was killed.

Controller explicitly permits only the170WAV `/Users/zenkim_office/Project/wavvy/SERIES/19-30/output/mix-170-20261026/continuous-mix-1930-repeat2.wav`, inode475818468, when every matching open descriptor belongs to `QuickLookUIService` with access `r`. This is a read-only preview reference; unlink can remove the pathname while space remains retained until the preview descriptor closes. Any write descriptor, different process, different inode or any other open candidate blocks execution. Each unlink has a fresh `lsof -nP -Fpcfain` observation and exact stat recheck. Allowed readers are written into the fsynced event journal. No process termination, UI guessing, permissions change or browser action.

## Execution sequence

1. Isolated controller review and explicit apply instruction are required before mutation.
2. Default invocation performs manifest/hash/stat/nofollow checks and uploaded gate; no media mutation.
3. Approved invocation: `python3 .ai/cleanup/execute-1930-final-media-cleanup-20261026.py --apply`.
4. Parent descriptors and file opens prohibit symlink traversal. Every candidate is checked against SHA256, device, inode, length and modification time. Exact `os.unlink` calls only; never recursive directory deletion.
5. Exclusive creation of apply report/event journal prevents a silent duplicate or overwritten partial run. Stop immediately on failure.
6. Verify all1,529 protected hashes/stats unchanged, all29 target paths absent, exact deleted set, and uploaded gate PASS. Record real free bytes before/after separately from logical deletion; space reclamation can be delayed by QuickLook.
7. Only after successful apply, update present retention statements, actual cleanup CHANGELOG entry, and formal session-only `-record` (local/global SESSION/HANDOFF via canonical runtime and record-append.sh). Preserve unrelated dirty edits; scope-stage and normal commit/push only approved cleanup records/own session entries.

## Raw evidence

- `2026-10-26-1930-final-media-cleanup-dry-run.json` and `-dry-run.stderr.txt` contain the final dry-run stdout/stderr.
- Candidate/protected manifests contain every absolute path, SHA256, device, inode, byte count and mtime_ns.
- Review and apply reports are separate future evidence; this plan does not claim apply or deletion completion.
