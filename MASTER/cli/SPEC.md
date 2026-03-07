# Project Wavvy: CLI Spec

Version: 3.0
Last Updated: 2026-03-03
Purpose: vibem CLI 시스템 명세

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

### C. `vfade` (v2.0 신규)
- **옵션:** `--fade 0.5 --duration SEC --test`
- loop.mp4에 FFmpeg xfade 필터 적용 → 끊김 없는 루프 영상 생성
- `--test`: 30초 테스트 영상 생성 (loop_xfade_test.mp4)
- 본 생성: loop_xfade.mp4

### D. `pack`
- **옵션:** `--lufs -14 --tp -1.0 --fade 0.8 --repeat 2 --use-xfade --force`
0. Pre-flight: loop_xfade.mp4 확인 (없으면 경고)
1. Re-Validate
2. Normalize: -14 LUFS, -1.0 dBTP → `work/norm_tracks/`
3. Merge: Sequential Acrossfade + repeat
4. Render: `libx264`/`aac`, `-shortest`, → `output/final.mp4`
   - `--use-xfade`: loop_xfade.mp4 사용 (권장)
5. Artifacts: `provenance.md`, `draft_description.txt`, `upload.csv`, `report.json`

### E. `shorts`
- **옵션:** `--start MM:SS --duration SEC [--title] [--lyric] [--srt]`
- shorts.mp4 루프 → 9:16 크롭 → 텍스트 오버레이
- Output: `output/shorts/short_[TrackName].mp4`

---

## 5. 사용 예시

```bash
# 검증
python3 vibem.py validate SERIES/[시리즈]

# 미리보기
python3 vibem.py preview SERIES/[시리즈] --sec 30

# 비디오 크로스페이드 (권장 워크플로우)
python3 vibem.py vfade SERIES/[시리즈] --test   # Step 1: 테스트
open SERIES/[시리즈]/input/loop_xfade_test.mp4  # Step 2: 확인
python3 vibem.py vfade SERIES/[시리즈]          # Step 3: 본 생성

# 패키징 (--use-xfade 권장)
python3 vibem.py pack SERIES/[시리즈] --fade 0.5 --repeat 2 --use-xfade

# 정리
python3 vibem.py clean SERIES/[시리즈]

# 숏츠
python3 vibem.py shorts [track.mp3] --start 00:45 --duration 30
```
