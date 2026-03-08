# Project Wavvy: CLI Spec

Version: 4.0
Last Updated: 2026-03-07
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
│   ├── loop.mp4      # 배경 루프
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

---

## 4. CLI 커맨드

### A. `validate`
- File Check: tracks 1개+, loop.mp4, thumb.jpg
- Naming Check: `__` 규칙
- Audio Integrity: ffprobe (Duration, Decodable, Sample Rate)

### B. `preview`
- **옵션:** `--sec 30`
- Sequential Acrossfade (0.8s) → 앞 30초 자름 → loop+thumb 렌더링
- `-shortest` 필수, normalize 생략

### C. `vfade` (v3.0 — 자동 크롭/로고)
- **옵션:** `--fade 0.5 --duration SEC --test --crop/--no-crop --logo/--no-logo`
- loop.mp4에 FFmpeg xfade 필터 적용 → 끊김 없는 루프 영상 생성
- `--crop`: 자동 pillarbox 감지 및 제거 (기본: 활성화)
- `--logo`: brand/logo_wavvy.png 오버레이 (기본: 활성화, 50% 크기)
- `--test`: 30초 테스트 영상 생성 (loop_xfade_test.mp4)
- 본 생성: loop_xfade.mp4

### D. `pack` (v4.0 — 인터랙티브 모드)
- **옵션:** `--lufs -14 --tp -1.0 --fade 0.8 --repeat N -y`
- **인터랙티브 플랜 모드** (기본): 4가지 설정 확인 후 진행
  1. Video crossfade 사용 여부 (loop_xfade.mp4 있으면 사용)
  2. Track repeat 횟수 (기본: 2)
  3. Pillarbox 자동 크롭 (감지 시)
  4. Logo 오버레이 (brand/logo_wavvy.png)
- `-y`: 확인 없이 기본값으로 진행
- 0. Pre-flight: 비디오 전처리 (크롭 + 로고)
- 1. Re-Validate
- 2. Normalize: -14 LUFS, -1.0 dBTP → `work/norm_tracks/`
- 3. Merge: Sequential Acrossfade + repeat
- 4. Render: `libx264`/`aac`, `-shortest`, → `output/final.mp4`
- 5. Artifacts: `provenance.md`, `upload.csv`, `report.json`

### E. `shorts`
- **옵션:** `--start MM:SS --duration SEC [--title] [--lyric] [--srt]`
- shorts.mp4 루프 → 9:16 크롭 → 텍스트 오버레이
- Output: `output/shorts/short_[TrackName].mp4`

---

## 5. 사용 예시

```bash
# 검증
python3 wavvy.py validate SERIES/[시리즈]

# 미리보기
python3 wavvy.py preview SERIES/[시리즈] --sec 30

# 비디오 크로스페이드 (긴 영상용 — vfade 별도 실행)
python3 wavvy.py vfade SERIES/[시리즈] --test   # Step 1: 테스트
open SERIES/[시리즈]/input/loop_xfade_test.mp4  # Step 2: 확인
python3 wavvy.py vfade SERIES/[시리즈]          # Step 3: 본 생성

# 패키징 (인터랙티브 플랜 모드)
python3 wavvy.py pack SERIES/[시리즈]

# 패키징 (기본값으로 빠르게)
python3 wavvy.py pack SERIES/[시리즈] -y

# 정리
python3 wavvy.py clean SERIES/[시리즈]

# 숏츠
python3 wavvy.py shorts [track.mp3] --start 00:45 --duration 30
```

---

## 6. 영상 패키징 워크플로우

> **⚠️ 크로스페이드 = 오디오 + 비디오 둘 다 필요**
> **⚠️ 플레이리스트 2회 반복 필수** (`--repeat 2`)

### 6.1 기본 워크플로우

`vfade --test` → 확인 → `vfade` → `pack` (§5 사용 예시 참조)

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
| **비디오** | `vfade` → `pack` | 루프 영상 끊김 없는 반복 |

**⚠️ `pack` 단독 실행 = 오디오만 크로스페이드 (비디오 끊김 발생)**
