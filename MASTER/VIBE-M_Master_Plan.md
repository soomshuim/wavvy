# Project Vibe-M: System Specification
Version: 2.2
Last Updated: 2026-02-16
Purpose: vibem CLI 시스템 명세
Target: Python CLI Tool (`vibem`)

---

## 1. 개요 및 핵심 원칙
이 프로젝트는 유튜브 뮤직 채널 운영을 위한 **자동화 CLI 도구 `vibem`**을 구축하는 것입니다.
가장 중요한 목표는 대용량 미디어 처리 시의 **안정성**과 **순수 FFmpeg 성능 최적화**입니다.

### 🛑 Hard Constraints (절대 제약 사항)
1.  **NO Pydub**: `pydub` 라이브러리는 절대 사용하지 않습니다. (메모리 누수 방지)
2.  **Pure FFmpeg**: 모든 미디어 조작(병합, 크로스페이드, 루프, 렌더링)은 `ffmpeg-python` 래퍼 또는 `subprocess`를 통해 FFmpeg 명령어로 직접 처리해야 합니다.
3.  **Sequential Filter Chain**: 오디오 병합 시 단순 `concat`이 아닌, `acrossfade` 필터를 사용한 **순차적 필터 그래프**를 구성해야 합니다.
    *   *Correct Logic:* `[Stream1][Stream2]acrossfade[Merged1]; [Merged1][Stream3]acrossfade[Merged2]...`
4.  **Fail Fast**: 입력 파일명이나 형식이 스펙과 다르면 즉시 에러를 출력하고 종료해야 합니다.

---

## 2. 프로젝트 디렉토리 구조
```text
root/
├── MASTER/                      # 프로젝트 헌법
│   ├── MANAGER.md               # 운영 마스터 플랜
│   ├── LYRICS.md                # 가사 공학 규칙
│   └── STYLE.md                 # 사운드/스타일 가이드
│
├── SERIES/                      # 시리즈별 프로젝트
│   └── [Series_Name]/           # 예: PM_0900, AM_0400
│       ├── concept.md           # (선택) 컨셉 문서
│       ├── input/
│       │   ├── tracks/          # MP3/WAV 파일들 (파일명 규칙 필수 준수)
│       │   ├── loop.mp4         # 배경 루프 영상
│       │   ├── shorts.mp4       # (선택) shorts용 베이스 루프
│       │   └── thumb.jpg        # 썸네일 이미지
│       ├── work/                # (자동생성) 임시 작업 폴더
│       └── output/              # (자동생성) 최종 결과물 폴더
│
├── vibem.py                     # CLI 실행 스크립트 (Click 사용)
├── MASTER/VIBE-M_Master_Plan.md # CLI 스펙 (이 파일)
├── requirements.txt             # 의존성 목록
├── CLAUDE.md                    # Claude Code 작업 지침
└── .ai/                         # AI 전용 메모리
    ├── SESSION.md               # 세션 상태 기록
    └── lessons-learned.md       # 버그 패턴 기록
```

---

## 3. 파일명 규칙 (Naming Convention)
파싱의 정확도를 위해 **Double Underscore (`__`)**를 구분자로 사용합니다.

*   **형식:** `NN__Title__Mood__Genre__BPM.(mp3|wav)`
*   **예시:** `01__새벽의달리기__Energetic__K-Rock__170.mp3`

---

## 4. CLI 커맨드 명세

### A. `validate`
**목적:** 작업 시작 전 파일 및 오디오 건전성 체크 (Health Check).

1.  **File Check:** `input/tracks` 폴더에 MP3/WAV가 1개 이상 존재하는지, `loop.mp4`, `thumb.jpg`가 있는지 확인.
2.  **Naming Check:** 파일명이 위 정규식 규칙(`__`)을 따르는지 검사. (위반 시 정확한 파일명 리포트)
3.  **Audio Integrity:** `ffprobe`를 사용하여 다음을 확인.
    *   Duration > 0
    *   Stream Decodable (손상 여부)
    *   **Sample Rate Consistency:** 모든 트랙의 샘플 레이트가 동일한지 확인 (다를 경우 경고).

### B. `preview`
**목적:** 톤앤매너 및 크로스페이드 상태 초고속 확인. (속도 우선)

*   **옵션:** `--sec 30` (기본값: 30초)
*   **로직:**
    1.  `NN` 번호순으로 트랙 정렬.
    2.  **Sequential Acrossfade** 필터 그래프 구성 (Default fade: 0.8s).
    3.  필터링된 오디오 스트림을 앞 30초만 자름 (`atrim`).
    4.  `loop.mp4`와 `thumb.jpg`를 합쳐서 렌더링.
    5.  **중요:** 영상 길이가 오디오 길이(30초)에 딱 맞춰 끝나도록 `-shortest` 옵션 사용.
    6.  *Note:* 속도를 위해 이 단계에서는 `ffmpeg-normalize`를 실행하지 않음.

### C. `pack`
**목적:** 유튜브 업로드용 최종 고품질 패키지 생성.

*   **옵션:** `--lufs -14 --tp -1.0 --fade 0.8 --repeat 2`
*   **로직:**
    1.  **Re-Validate:** 검증 로직 재실행.
    2.  **Normalize (개별 정규화):**
        *   `ffmpeg-normalize` 라이브러리 사용.
        *   Target: **-14 LUFS**, True Peak: **-1.0 dBTP**.
        *   결과물은 `work/norm_tracks/`에 저장 (원본 덮어쓰기 금지).
    3.  **Merge (병합):**
        *   정규화된 트랙들에 **Sequential Acrossfade** 적용.
        *   `--repeat N` 옵션으로 플레이리스트 반복 횟수 지정 (기본값: 2회).
        *   안정성을 위해 `work/merged.wav`로 중간 파일 저장 허용.
    4.  **Render (최종 렌더링):**
        *   Input: `work/merged.wav` + `loop.mp4` + `thumb.jpg`.
        *   Video Loop: 재인코딩 부하를 줄이기 위해 `stream_loop -1` (또는 concat demuxer) 사용.
        *   Codec: `libx264` (Video), `aac` (Audio).
        *   **Critical:** `-shortest` 옵션으로 무한 루프 방지.
        *   Output: `output/final.mp4`.
    5.  **Artifacts (산출물 생성):**
        *   `provenance.md`: 원본 파일명, **SHA-256 해시값**, 처리 옵션, 타임스탬프가 포함된 표. (저작권 증빙용)
        *   `draft_description.txt`: 유튜브 설명란 초안 (인트로, 타임스탬프, 해시태그, 고정댓글).
        *   `upload.csv`: 컬럼 헤더 [`video_path`, `title`, `description`, `tags`, `thumbnail_path`, `visibility`].
        *   `report.json`: 트랙별 기술 통계 (Duration, Peak, Loudness).

### D. `shorts`
**목적:** YouTube Shorts용 9:16 세로 영상 생성.

*   **옵션:** `--start MM:SS --duration SEC [--title "..."] [--lyric "..."] [--srt file.srt]`
*   **로직:**
    1.  **Input:** `input/shorts.mp4` (8~10초 짧은 영상) + 지정 트랙의 오디오 구간.
    2.  **Video Loop:** `shorts.mp4`를 `stream_loop -1`로 오디오 길이만큼 반복.
    3.  **Crop:** 9:16 세로 비율로 중앙 크롭.
    4.  **Text Overlay (선택):**
        *   `--title`: 중앙 훅 문구 (0~2초 표시, 빠르게 퇴장).
        *   `--lyric`: 하단 고정 가사 (페이드인, 끝까지 유지).
        *   `--srt`: 동적 가사 (SRT 자막 파일).
    5.  **Output:** `output/shorts/short_[TrackName].mp4`.

---

## 5. 사용 예시

### 실제 프로젝트 구조 예시
```text
series/
└── Test_Series/
    └── 2026-01-18/
        ├── input/
        │   ├── tracks/
        │   │   ├── 01__마음밖__Sentimental__RnB-Ballad__100.mp3
        │   │   ├── 02__SunsetDream__Calm__Ambient__80.mp3
        │   │   └── 03__NightRun__Energetic__EDM__128.mp3
        │   ├── loop.mp4       # pack용 배경 영상
        │   ├── shorts.mp4     # shorts용 (8~10초, 루프됨)
        │   └── thumb.jpg
        ├── work/            # (자동생성)
        └── output/          # (자동생성)
```

### CLI 명령어 예시
```bash
# 프로젝트 초기화
python3 vibem.py init SERIES/Test_Series/2026-01-18

# 검증
python3 vibem.py validate SERIES/Test_Series/2026-01-18

# 미리보기 (30초)
python3 vibem.py preview SERIES/Test_Series/2026-01-18 --sec 30

# 최종 패키징 (2회 반복, 기본값)
python3 vibem.py pack SERIES/Test_Series/2026-01-18 --lufs -14 --tp -1.0 --fade 0.8

# 최종 패키징 (1회만, 반복 없음)
python3 vibem.py pack SERIES/Test_Series/2026-01-18 --repeat 1

# 작업 폴더 정리
python3 vibem.py clean SERIES/Test_Series/2026-01-18

# 숏츠 생성 (shorts.mp4가 음악 길이만큼 루프됨)
python3 vibem.py shorts SERIES/Test_Series/2026-01-18/input/tracks/01__마음밖__Sentimental__RnB-Ballad__100.mp3 \
  --start 00:45 --duration 30

# 숏츠 + 텍스트 오버레이
python3 vibem.py shorts SERIES/Test_Series/2026-01-18/input/tracks/02__SunsetDream__Calm__Ambient__80.mp3 \
  --start 01:00 --duration 40 --title "잠들지 못한 새벽" --lyric "여명처럼 스며들어"
```

---

## 6. 구현 요청 사항
*   위 명세를 만족하는 `vibem.py` 전체 코드와 `requirements.txt`를 작성해 주십시오.
*   특히 **FFmpeg 필터 그래프 생성 로직**에서 에러 처리를 견고하게 작성해 주십시오.
