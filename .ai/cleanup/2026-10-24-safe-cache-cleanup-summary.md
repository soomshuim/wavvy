# Mac safe cache cleanup — 2026-10-24 22:27 KST

Authorization: “좋아 정리 가능한건 정리해줘. cds 작업 지장 안미치는 선에서”. This is separate from the earlier Wavvy media cleanup and the old 772.07GB diagnostic. The current user-reported System Data figure was 122.84GB; it was not independently remeasured after cleanup.

## Final result

Deleted 110,993 enumerated regular files, totaling **5,363,057,391 logical bytes**. No directories were removed and no apps or processes were stopped.

| Scope | Files | Logical bytes |
|---|---:|---:|
| Idle Atlas browser `Cache` / `Code Cache`, older than 7 days | 110,597 | 3,147,073,462 |
| Idle Pencil updater downloads, older than 14 days | 3 | 696,794,378 |
| Idle Cherry Studio updater downloads, older than 14 days | 2 | 343,048,829 |
| Idle Notion updater downloads, older than 14 days | 3 | 249,752,413 |
| Closed Adobe / CreativeCloud / NGL `.log` files, older than 30 days | 388 | 926,388,309 |

Age checks covered both modification and metadata-change times. Apps, open files and unchanged file identities were checked again during deletion. Source paths, `Storage`, application support, Claude/Codex work folders and records, CDS source/temporary work, active Chrome/Aside/Codex caches, package/build runtimes, system files and Trash were outside the deletion allowlist. No source or worktree cleanup was attempted.

## Evidence and limits

The exact compressed manifest SHA-256 is `14816a38cdbd8f704bbb9b4d4d5c1eca36928c60b7210d7a99e436cf319bdba4`. The dry-run and deleted journals match all manifest rows. Post-delete checks found every target absent, zero skipped apply rows and no deletion outside the allowlist. Protected roots remained present. The CDS Claude PID 1755 and its Aside PID 2254 were observed before and after cleanup; live process presence is not a CDS functional test, and live source contents were not snapshotted or claimed unchanged.

During deletion, observed free space rose by **5,692,936,192 bytes**. The post-check showed **603,104,706,560 bytes free**. File-size totals, allocated-block totals and free-space changes differ because APFS shares storage and other apps were writing concurrently. These values do not establish the new macOS System Data category size.

Independent isolated review: Astra/high role, CLEAN, confirmed Critical/High 0, principle observations none. The role was configured by the review tool; underlying runtime model telemetry was unavailable to the reviewer. Current request has no remaining cleanup action; CDS-linked work and active application data were deliberately preserved.

Final evidence: [inventory and journals](mac-safe-cache-20261024/), [independent review](mac-safe-cache-20261024/review.md), [execution result](mac-safe-cache-20261024/result.json), [post-delete checks](mac-safe-cache-20261024/verification.json), and [frozen executor](execute-mac-safe-cache-20261024.py).
