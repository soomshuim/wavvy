# 17:00 YouTube package

Date: 2026-10-03
Status: In progress

## Requested result

- Save all 20 finished songs from the Suno `[17:00]` workspace as WAV.
- Use the approved autumn street image for a 3840×2160 static video and a series-consistent thumbnail.
- Build and verify the full playlist with the Wavvy harness.
- Put actual track start times into the YouTube draft, then review the title and description for a clear, compelling 17:00 promise.

## Evidence and sequence

1. `SERIES/17-00/concept.md`, `.ai/state.json`, `MASTER/SSOT.md`, `MASTER/cli/SPEC.md`, and `MASTER/youtube/YOUTUBE.md` govern the package. Existing series thumbnails and descriptions are precedents.
2. The Suno workspace has 20 songs. Search finds tracks 01–05 even though their initial list rows appeared as `Untitled`. Compare clip titles with the approved track map before naming files.
3. Download each WAV through the user-opened Aside Suno tab. Preserve raw files until the 20-file inventory and WAV integrity checks pass. The browser connection for the remaining downloads awaits a user decision after repeated Aside MCP download failures.
4. Place canonical numbered files in `input/tracks/`, run `validate`, render a short `preview`, then `pack --repeat 2 -y`. Read `output/report.json` for exact timestamps and compare video duration with the report.
5. Update YouTube metadata in `concept.md`, review the complete result, then update state/session records according to project gates. Do not mark uploaded without an upload.

## Current artifacts and limits

- `input/loop-4k-candidate-v1.png`: 3840×2160 upscale of a 1672×941 generated image.
- `input/loop.png`: static image rendering input; local/ignored.
- `input/thumb.jpg`: thumbnail candidate.
- One verified 48 kHz/16-bit stereo WAV, `08 취향`, is staged under `input/tracks/.downloads/`.
- Full video and actual timestamps depend on the remaining 19 WAV files.

## Suno title mapping to verify on download

The approved project track titles remain the YouTube track-list names. Suno's clip labels differ for these rows:

| # | Suno clip label | Approved title |
|---|---|---|
| 02 | 공강 (Acoustic Remix) | 공강 (Accoustic Remix) |
| 03 | 너와 (With you) | 너와 |
| 04 | 낮꿈 (Acoustic Remix) | 낮꿈 (Accoustic Version) |
| 05 | 한 정거장만 | 한 정거장 |
| 07 | 봄비같은 너 (Acoustic Remix) | 봄비같은 너 (Accoustic Remix) |
| 10 | 그날 오후 | 그때의 빛 |
| 12 | 이런 데가 있었네 | 서점 |
| 13 | 컵 두개 | 컵 두 개 |
| 18 | 사진 | 흔들린 사진 |

The workspace search returned playable numbered rows for 01–05, resolving the initial `Untitled` placeholders in the unfiltered list. The clip labels alone do not verify that their recorded lyrics match the final text sources.
