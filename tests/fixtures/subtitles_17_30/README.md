# Fixture: frozen 17:30 timed-subtitle evidence

Used by `tests/test_subtitles.py`. Verbatim copies of the evidence of the published 17:30 series (video `3HorT4OoDhg`), kept so the tests do not depend on `SERIES/17-30/`, whose files may be cleaned after an upload.

- Paths below are relative to `SERIES/17-30/` and are stored at the same relative path in this folder.
- Source commit for every file except the report: `12ea5e2dc6a61fa5cf63f8f47ec7941cb112fc6c` (git blob content, byte for byte; SHA-256 of each file in the table).
- The report `input/validation/2026-10-23-timed-subtitles/report-at-subtitle-preparation.json` was deleted by `0861ddb` ("chore: finalize 07:00 release and clean uploaded series artifacts", 2026-10-24); it is restored from its adding commit `1154bb79e8e56d1b2a7f8cc5ca35f91e50cc6258` (`1154bb7`). Its SHA-256 `a1a6e1c59fc5bc4119c3e9799ba27a9a2ede3463e1a11cb04f87a39bfe751ca8` equals `report.sha256` in `input/subtitles.json` and the local, Git-ignored `SERIES/17-30/output/report.json`.
- `all-tracks-timed-checked.srt` is the tracked copy of the prepared SRT (`output/youtube_subtitles_ko_timed_estimated.srt` is Git-ignored); its SHA-256 is the `srt.sha256` in `input/subtitles.json`.
- Not vendored (large media): the six publication screenshots (PNG, 15,189,815 bytes in total). The harness only checks that each screenshot exists and matches the SHA-256 recorded in `input/subtitles.json`, never its pixels, so `tests/test_subtitles.py::_clone` writes a small stand-in file per screenshot and rewrites only those six hash entries in the cloned manifest. Original screenshots (SHA-256 at the source commit):

| screenshot (not vendored) | bytes | SHA-256 |
|---|---:|---|
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-manual-caption-published-studio.png` | 579730 | `a3a2720eccc3b08f66bff15f95c6b1782d54ea3eb30cf6129980243382eba437` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-public-manual-caption-menu.png` | 2895294 | `59097745f421d2fa761edfb246040f1610e27b749b0476106bdad6afa5f4935d` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-000005.png` | 2945080 | `54e044ff2f394745d33ede912b6f450b414fddb856f600d8ef5204e1cd298654` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-mid.png` | 2921936 | `440e567cedf95c3de7c17b3c4e070006b56e66a4adedffaa09abcfc1102b06ef` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-repeat.png` | 2963653 | `b4b44b8d152f671c56ea34aacd8993f9c9055a973779ec6e1da171a141d2cbcd` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-ending.png` | 2884122 | `65d607ea98b540e6889f4b24c578ac460c6295f7692d6a0b9cc720d7f6d176fa` |

## Files

| fixture path | source (commit:path in the repository history) | bytes | SHA-256 |
|---|---|---:|---|
| `concept.md` | `12ea5e2:SERIES/17-30/concept.md` | 56432 | `d39e12d39e28b0fb03405d8db2e85c6ac8479d32c8369b36e682aad21c1be9cc` |
| `input/subtitles.json` | `12ea5e2:SERIES/17-30/input/subtitles.json` | 4938 | `4579fd644e01df3c480852a55a65b4a4d4c79b0b3493586b119623ffb5847b97` |
| `input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.json` | 1471451 | `dd5d21b1fa456ca81bdc3a22a94b8bd9af7bd6c5032a8677dcc78aaa54306fa0` |
| `input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.srt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.srt` | 86024 | `29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/09__잘 익은 하루__Bright__Modern R&B__NA-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/09__잘 익은 하루__Bright__Modern R&B__NA-whisper.json` | 40846 | `07f68211992c2af49ece68db7cd9ec4ec35809b7305f3458723a84d8a2f4ecfb` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-03-line41-155-169-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-03-line41-155-169-whisper.json` | 3308 | `9de9c56bef2e9378342f73c16b92ba1daae699f3768d38574420b8d83c1433f2` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-09-repeat-150-180-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-09-repeat-150-180-whisper.json` | 6884 | `20056cd1485a8e0fe7a85f34ecf297cdc899d80f987a870dc38ef3b7465728c8` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-11-first-chorus-35-66-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-11-first-chorus-35-66-whisper.json` | 9131 | `3f52e88a7579b88f71d2e56f03645157b6bc261f03f3a6ebd3f33b5d82723d11` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-11-line24-repeat-88-118-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-11-line24-repeat-88-118-whisper.json` | 10685 | `d4ce20e83b3be5ceab4ebe5b6d97aa2dffd3e827f0f86032a22f793c638ef583` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-16-line22-88-104-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-16-line22-88-104-whisper.json` | 2821 | `f9ce1567fed250a3cd4ada76a7055827d320accf31d33c6a570bdee85a6691a6` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-16-weak-line01-context-0-40-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-16-weak-line01-context-0-40-whisper.json` | 9130 | `ae7a3c698cf96ae140230958a15f99fdcc7d1c8b337bd666f37c7184d4027b56` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/check-20-line39-155-170-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-20-line39-155-170-whisper.json` | 3412 | `27a452c14b7f0312d99fc1eb15b7390bb221d934b297bf9d14583f948eb7e980` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/weak-04-line-25-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/weak-04-line-25-whisper.json` | 1759 | `22f71957bce5abb42d0bd4407e0adaec32d0daba6ed14825e506a077da66f96d` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/weak-12-line-34-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/weak-12-line-34-whisper.json` | 3920 | `8809a9966bc235127fd676850f253285212d2ab1e7047d8cd6048a78940ecec6` |
| `input/validation/2026-10-23-timed-subtitles/audio-probe/weak-14-line-31-whisper.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/weak-14-line-31-whisper.json` | 5265 | `451c8a30cf8beadebef94600e50c2a8f4bee5c36ea73f4421f91dded8908f710` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-manual-caption-published-studio.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-manual-caption-published-studio.txt` | 4062 | `ef5e1b3b8566eb68e9dd082d0bc04e7cf8f2d134b2dc2731fee95fe74e17e6b0` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-public-manual-caption-menu.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-public-manual-caption-menu.txt` | 12957 | `0cc864d1252bf155b9f98d3560897bbc93f3a139144d176f0f12e130f9970fc4` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-000005.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-000005.txt` | 12182 | `8e41f3d0336cf1daeb821c8f048c7c66e93e660d5908823e30c1346b2fb16f39` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-ending.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-ending.txt` | 12399 | `a754f6eec4e8772ce261613ae860b6e205074300ac6364dbf58159519a4e2545` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-mid.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-mid.txt` | 12622 | `33d8e035452743ab71b5a1b72ce775827a77eacef936c4d2e5c66a48ca18a2ce` |
| `input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-repeat.txt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-watch-manual-repeat.txt` | 12656 | `7b500318ce0ca167b512f7a02b1b30193f74edd416e4ed59aa4b66d8abf4f672` |
| `input/validation/2026-10-23-timed-subtitles/publication/publication-observation.json` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/publication-observation.json` | 2951 | `2935c13e98c04991561f4874f0280e5835f3041f10b52dd3034666ef427434e9` |
| `input/validation/2026-10-23-timed-subtitles/publication/studio-published-manual-ko.srt` | `12ea5e2:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/studio-published-manual-ko.srt` | 86025 | `b9ef1541954c96ee07593278d34d0553ed1965e8a6e8758d352d20ea37de1731` |
| `input/validation/2026-10-23-timed-subtitles/report-at-subtitle-preparation.json` | `1154bb7:SERIES/17-30/input/validation/2026-10-23-timed-subtitles/report-at-subtitle-preparation.json` | 7292 | `a1a6e1c59fc5bc4119c3e9799ba27a9a2ede3463e1a11cb04f87a39bfe751ca8` |

Do not edit these files. If the harness contract changes, regenerate the fixture from history and update this table.
