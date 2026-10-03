# Project Wavvy: CLI Spec

Version: 4.2
Last Updated: 2026-09-30
Purpose: wavvy CLI 시스템 명세

---

## 1. Hard Constraints

1. **NO Pydub** - 메모리 누수 방지
2. **Pure FFmpeg** - subprocess로 직접 처리
3. **Sequential Acrossfade** - `[S1][S2]acrossfade[M1]; [M1][S3]acrossfade[M2]...`
4. **Fail Fast** - 스펙 불일치 시 즉시 종료

---

## 2. 디렉토리 구조

```
SERIES/[Series_Name]/
├── concept.md
├── input/
│   ├── tracks/       # MP3/WAV (파일명 규칙 필수)
│   ├── loop.mp4      # 배경 비디오 루프 (선택: video mode)
│   ├── loop.png/jpg  # 정적 배경 이미지 (선택: image mode)
│   ├── shorts.mp4    # shorts용 (선택)
│   └── thumb.jpg
├── work/             # (자동생성)
└── output/           # (자동생성)

brand/
└── logo_wavvy.png    # 전역 로고 (50% 크기로 오버레이)
```

---

## 3. 파일명 규칙

**형식:** `NN__Title__Mood__Genre__BPM.(mp3|wav)`
**예시:** `01__새벽의달리기__Energetic__K-Rock__170.mp3`

STYLE에 숫자 BPM이 없는 곡은 마지막 필드에 `NA`를 쓴다. 이 값은 미기재를 뜻하며, 보고서에는 `null`로 기록한다. 숫자가 있는 파일명도 프롬프트 목표치를 나타내며 실제 오디오 템포 측정값으로 해석하지 않는다.

---

## 4. CLI 커맨드

### A. `validate`
- File Check: tracks 1개+, `loop.mp4` 또는 `loop.png/jpg/jpeg`, `thumb.jpg`
- Naming Check: `__` 규칙
- Audio Integrity: ffprobe (Duration, Decodable, Sample Rate)

### B. `preview`
- **옵션:** `--sec 30`
- Sequential Acrossfade (0.8s) → 앞 30초 자름 → loop+thumb 렌더링
- `-shortest` 필수, normalize 생략

### C. `vfade` (v3.0 — 자동 크롭/로고)
- **옵션:** `--fade 0.5 --duration SEC --test --crop/--no-crop --logo/--no-logo`
- video mode 전용: loop.mp4에 FFmpeg xfade 필터 적용 → 끊김 없는 루프 영상 생성
- `--crop`: 자동 pillarbox 감지 및 제거 (기본: 활성화)
- `--logo`: brand/logo_wavvy.png 오버레이 (기본: 활성화, 50% 크기)
- `--test`: 30초 테스트 영상 생성 (loop_xfade_test.mp4)
- 본 생성: loop_xfade.mp4

### D. `pack` (v4.0 — 인터랙티브 모드)
- **옵션:** `--lufs -14 --tp -1.0 --fade 0.8 --repeat N -y`
- **인터랙티브 플랜 모드** (기본): 4가지 설정 확인 후 진행
  1. Video crossfade 사용 여부 (video mode에서 loop_xfade.mp4 있으면 사용, image mode는 스킵)
  2. Track repeat 횟수 (기본: 2)
  3. Pillarbox 자동 크롭 (감지 시)
  4. Logo 오버레이 (brand/logo_wavvy.png)
- `-y`: 확인 없이 기본값으로 진행
- 0. Pre-flight: image mode 감지 또는 비디오 전처리 (크롭 + 로고)
- 1. Re-Validate
- 2. Normalize: -14 LUFS, -1.0 dBTP → `work/norm_tracks/`
- 3. Merge: Sequential Acrossfade + repeat
- 4. Render: `libx264`/`flac` in MKV, `-shortest`, → `output/final.mkv`
- 5. Artifacts: `provenance.md`, `upload.csv`, `report.json`

### E. `shorts`
- **옵션:** `--start MM:SS --duration SEC [--title] [--lyric] [--srt]`
- shorts.mp4 루프 → 9:16 크롭 → 텍스트 오버레이
- Output: `output/shorts/short_[TrackName].mp4`

### F. `lyrics-skill` / `gate --stage lyrics-review` / `gate --stage track-prompt`
- `lyrics-skill SERIES/[시리즈]` checks skill installation only (`scope: PACKAGE_ONLY`, `quality_status: NOT_REVIEWED`).
- `lyrics-skill SERIES/[시리즈] --artifact REVIEW.md --mode review-only` checks a review record and its current source binding. `full-lyric-draft` and `suno-prompt-only` are also accepted modes.
- `gate SERIES/[시리즈] --stage lyrics-review --artifact REVIEW.md --mode review-only` requires an artifact. Without one, the stage fails instead of presenting installed files as reviewed lyrics.
- `reviewed_source_sha256` and the hash-check detail show the current source-body hash. `PASS` means the required record and deterministic checks pass, not that software certified naturalness, musical effect, or authorship.
- New full-song lyric records declare `draft_scope: full-song`, `target_duration_seconds`, `meter`, `section_bars`, and `track_source`. They start with three Verse sections or record `verse_structure_exception` for a different structure. Their Self-Gate records actual Verse sung-line counts, an exact longest sung line, two adjacent lines with a phrasing reason, and a quoted line with space for a breath afterward. Invoke `--mode full-lyric-draft --draft-scope full-song` on both `lyrics-skill` and `gate --stage lyrics-review`. The gate checks this evidence and the Draft against the txt LYRICS body, then compares planned bar duration against the target using the declared BPM (quarter-note assumption). It does not judge the sound of a phrase. `planned_duration_estimate_seconds` is not measured audio duration. Only the exact earlier approved Track 03/05 Draft bodies listed in `MASTER/lyrics/legacy-full-song-approvals.json` skip the new breathing evidence and Verse default. Missing `draft_scope` in an older record is reported as `UNSPECIFIED` with `full_song_ready: false`; a new full-song call with `--draft-scope full-song` fails if that declaration is absent.
- `gate SERIES/[시리즈] --stage track-prompt --artifact SERIES/[시리즈]/input/tracks/[track].txt` checks one newly authored full-track source. It requires the actual txt under that series and reports its SHA-256, `scope: NEW_FULL_TRACK_PROMPT_CONTRACT`, STYLE length (Wavvy's internal 900-character budget including whitespace), EXCLUDE count (internal maximum eight items), numeric BPM, Key/Mode, and explicit vocal gender matching between header and STYLE. This check does not inspect lyric meaning or certify Suno audio. User-provided remix originals are preserved without a retrospective new-draft check.

---

## 5. 사용 예시

```bash
# 검증
python3 wavvy.py validate SERIES/[시리즈]

# 미리보기
python3 wavvy.py preview SERIES/[시리즈] --sec 30

# 비디오 크로스페이드 (video mode 긴 영상용 — vfade 별도 실행)
python3 wavvy.py vfade SERIES/[시리즈] --test   # Step 1: 테스트
open SERIES/[시리즈]/input/loop_xfade_test.mp4  # Step 2: 확인
python3 wavvy.py vfade SERIES/[시리즈]          # Step 3: 본 생성

# 패키징 (인터랙티브 플랜 모드)
python3 wavvy.py pack SERIES/[시리즈]

# 패키징 (기본값으로 빠르게)
python3 wavvy.py pack SERIES/[시리즈] -y

# 하네스 점검
python3 wavvy.py doctor
python3 wavvy.py state SERIES/[시리즈] --check
python3 wavvy.py state SERIES/[시리즈] --write --phase uploaded --if-match N
python3 wavvy.py gate SERIES/[시리즈] --stage source-final
python3 wavvy.py gate SERIES/[시리즈] --stage uploaded
python3 wavvy.py gate SERIES/[시리즈] --stage lyrics-review --artifact REVIEW.md --mode review-only --json
python3 wavvy.py gate SERIES/[시리즈] --stage track-prompt --artifact SERIES/[시리즈]/input/tracks/[track].txt --json
python3 wavvy.py lyrics-skill SERIES/[시리즈] --artifact FULL_DRAFT.md --mode full-lyric-draft --draft-scope full-song --json
python3 wavvy.py gate SERIES/[시리즈] --stage lyrics-review --artifact FULL_DRAFT.md --mode full-lyric-draft --draft-scope full-song --json

# 업로드 FINAL 소스 아카이브
python3 wavvy.py finalize-upload SERIES/[시리즈] --check

# 정리
python3 wavvy.py clean SERIES/[시리즈]

# 숏츠
python3 wavvy.py shorts [track.mp3] --start 00:45 --duration 30
```

`state`는 같은 시리즈를 재개할 때 저장된 `phase`/`next_action`을 유지한다. 다른 시리즈를 지정하면 대상 `concept.md`와 산출물에서 다시 추론하며, 명시한 `--phase`와 `--if-match` revision 조건은 그대로 적용한다.

---

## 6. 영상 패키징 워크플로우

> **⚠️ 오디오 acrossfade와 비디오 xfade는 별개**
> **⚠️ 플레이리스트 2회 반복 필수** (`--repeat 2`)

### 6.1 기본 워크플로우

`pack`은 항상 오디오 acrossfade를 처리한다. 비디오 xfade는 `input/loop.mp4` 기반 video mode에서 루프 경계가 눈에 띄는 경우에만 별도로 만든다.

- Video mode + seamless loop 필요: `vfade --test` → 확인 → `vfade` → `pack`
- Image mode (`loop.png/jpg/jpeg`): `pack`만 실행. `vfade` 불필요
- 이미 `uploaded` 상태인 시리즈 점검: `state/gate`로 확인. 로컬 `final.mkv`/`upload.csv`가 `deleted_after_upload`이면 재생성 불필요

### 6.2 Seamless Loop (81분+ 영상용 — 수동)

> **⚠️ FFmpeg filter_complex 100개 제한 초과 시 필요**

`vfade`로 생성된 `loop_xfade.mp4`는 끝-시작 경계에 미세한 끊김이 있을 수 있음.
**무한 반복 시 완전한 seamless loop**가 필요하면 아래 추가 작업:

```bash
# Step A: 끝 1초 + 시작 1초 xfade 브릿지 생성
ffmpeg -sseof -1 -i input/loop_xfade.mp4 -ss 0 -t 1 -i input/loop_xfade.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=0.5[v]" \
  -map "[v]" -an work/xfade_bridge.mp4

# Step B: 메인(0.5s~끝-0.5s) + 브릿지 결합
ffmpeg -i input/loop_xfade.mp4 -i work/xfade_bridge.mp4 -filter_complex \
  "[0:v]trim=0.5:end-0.5,setpts=PTS-STARTPTS[main];\
   [1:v]setpts=PTS-STARTPTS[bridge];\
   [main][bridge]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -an input/loop_seamless.mp4

# Step C: pack에서 loop_seamless.mp4 사용
```

**원리**: 끝과 시작을 xfade로 연결 → `-stream_loop -1` 무한 반복 시 끊김 없음

### 6.3 크로스페이드 구분

| 종류 | 명령어 | 설명 |
|------|--------|------|
| **오디오** | `pack --fade 0.5` | 트랙 간 오디오 전환 |
| **비디오** | `vfade` → `pack` | video mode 루프 영상 끊김 없는 반복 |

**주의:** video mode에서 `pack` 단독 실행은 오디오만 크로스페이드한다. image mode는 정적 이미지 렌더이므로 비디오 루프 xfade 문제가 없다.
