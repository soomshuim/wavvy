# Wavvy Workflows

> **모든 작업 워크플로우 통합 문서**
>
> Version: 1.3
> Last Updated: 2026-03-06

---

## 0. 절대 규칙: txt 파일 우선

> **⚠️ 가사/스타일/exclude 작업 시 반드시 준수**

### 절차
1. **txt 파일 먼저 생성** → `SERIES/[시리즈]/input/tracks/{N}_{제목}.txt`
2. 유저에게 제시 → **PASS 컨펌 받기**
3. PASS 후에만 concept.md 반영

### 금지
- ❌ txt 없이 바로 concept.md 수정
- ❌ txt와 concept.md 동시 수정
- ❌ 컨펌 전 concept.md 반영
- ❌ 채팅으로만 제시하고 txt 생성 안 함

### 파일 네이밍
| 파일명 | 용도 |
|--------|------|
| `{N}_{제목}.txt` | 통합 (Style + Exclude + Lyrics) |

예: `02_멀어져.txt`

### 파일 포맷
```
Track {N}: {제목} ({영문})
Type: {A/B/C}
BPM: {숫자}
Key: {키}
Length: 3min+

=== STYLE ===
{스타일 프롬프트}

=== EXCLUDE ===
{제외 키워드}

=== LYRICS ===
{구조태그 + 가사}
```

---

## 1. 가사 생성 워크플로우

> **SSOT: `MASTER/lyrics/LYRICS.md` (체크리스트) + `MASTER/MANAGER.md` Phase 0.5 (수정 절차)**

### ⚠️ Pre-condition (필수)
1. **Read `MASTER/lyrics/LYRICS.md`** — 허용 태그, 괄호 규칙, 길이 제한 확인
2. **Read `MASTER/rubrics/[GENRE]_RUBRIC.md`** — 장르별 가사 규칙 확인
3. 참조 없이 가사 작성 시 → **FAIL (재작성)**

### 절차
1. `LYRICS.md` + 이전 트랙 키워드 확인 + 크로스시리즈 겹침 검증 (3축 중 2개 이상 겹침 = FAIL)
2. `Reference/museA_suno_guide.md` §3-4 참조 (구조 공식, 메타태그 규칙)
3. 초안 생성 → self-QC (LYRICS.md 전항목) → Korean Positioning (K1-K3) → 메타태그 검증 → 패턴 고착 검사
4. **루브릭 테스트 (셀프 루프)**
   - Hard Gates 체크 → **1개라도 FAIL 시 즉시 수정 후 재체크**
   - Hard Gates PASS 후 6-Factor 채점 → **80점 미만 시 수정 후 재채점**
   - 유저에게 제안 전 PASS 필수
5. 전부 PASS시 QC 테이블과 함께 출력 (통과 전 유저 제안 금지)
6. .txt 파일 저장 + pbcopy → 유저 컨펌 후 concept.md 반영

---

## 2. 가사/스타일 수정 절차

> **SSOT: `MASTER/MANAGER.md` Phase 0.5**

txt 먼저 수정 -> 유저 컨펌 -> concept.md 반영 (역순 금지, 동시 수정 금지)

---

## 3. Concept 파일 최종 QC

> **SSOT: `MASTER/MANAGER.md`**

concept 작성 완료 후 검증: 편곡지시 분리, 글자수, 타이틀/Description 포맷, Cross-Series 겹침, 저작권 표기, SSOT version

---

## 4. Shorts 생성

> **SSOT: `MASTER/Wavvy_Master_Plan.md` (CLI 스펙)**

- 반드시 시리즈/트랙/구간 확인 후 생성. 시작/종료 시간 임의 수정 절대 금지
- Hook Title (선언문, 가사 그대로 사용 금지) + Bottom Lyric (하단 가사) 2-Layer 구조
- 타이포: Shadow 필수, Stroke 금지, 하단 30% 침범 금지 (YouTube UI 영역)
- CLI: `python3 vibem.py shorts <track> --start MM:SS --duration SEC [--title "..."] [--srt file.srt]`

---

## 5. 영상 패키징 워크플로우

> **⚠️ 크로스페이드 = 오디오 + 비디오 둘 다 필요**
> **⚠️ 플레이리스트 2회 반복 필수** (`--repeat 2`)

### 5.1 CLI 기반 워크플로우 (v2.0)

```bash
# Step 1: 비디오 크로스페이드 테스트 (30초)
python3 vibem.py vfade SERIES/[시리즈] --test

# Step 2: 테스트 영상 확인 (끊김 없으면 PASS)
open SERIES/[시리즈]/input/loop_xfade_test.mp4

# Step 3: 비디오 크로스페이드 본 생성
python3 vibem.py vfade SERIES/[시리즈]

# Step 4: 패키징 (--use-xfade 필수!)
python3 vibem.py pack SERIES/[시리즈] --fade 0.5 --repeat 2 --use-xfade
```

### 5.2 필수 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--fade` | **0.5** | 오디오 크로스페이드 (초) |
| `--repeat` | **2** | 플레이리스트 반복 횟수 |
| `--use-xfade` | - | 비디오 크로스페이드 사용 (**권장**) |

### 5.3 Pre-flight 체크

`pack` 실행 시 자동 확인:
- `loop_xfade.mp4` 없으면 경고 + 확인 요청
- `--force` 사용 시 확인 생략 (비권장)

### 5.4 크로스페이드 구분

| 종류 | 명령어 | 설명 |
|------|--------|------|
| **오디오** | `pack --fade 0.5` | 트랙 간 오디오 전환 |
| **비디오** | `vfade` → `pack --use-xfade` | 루프 영상 끊김 없는 반복 |

**⚠️ `pack` 단독 실행 = 오디오만 크로스페이드 (비디오 끊김 발생)**

---

## 6. YouTube 메타데이터 생성 워크플로우

> **SSOT: `MASTER/youtube/YOUTUBE.md`**

### 7.1 Phase 1: 시리즈 초기 생성 (Draft)

**시점:** 시리즈 폴더 + concept.md 최초 생성 시

**필수 요청 (유저에게):**
1. Context Mode (Settling/Transition/Energizing/Focusing)
2. 감정 훅 키워드 또는 방향
3. 고정 댓글 훅 아이디어

**작성 내용 (Track List 외 전부 초안):**
- 제목 (템플릿 기반, 장르/용도)
- 설명 인트로 (2줄 훅 + 확장 훅)
- 해시태그/태그 (시리즈 장르 매핑 참조)
- 고정 댓글 초안
- 아웃트로 (고정 템플릿)

**Track List:** `(트랙 완성 후 추가)` placeholder

**버전 태그:** `## YouTube Draft (v1 — 트랙 미완성)`

**⚠️ 유저 요청 없이 임의 생성 금지 — 필수 요청 항목 먼저 확인**

### 7.2 Phase 2: 시리즈 완성 (Final)

**시점:** 모든 트랙 PASS + 패키징 완료 시

**업데이트:**
1. Track List에 실제 타임스탬프 + 곡명 + 이모지
2. 버전 태그 변경: `(v1 — 트랙 미완성)` → `(v2.1)`
3. 해시태그/태그 최종 검토
4. 장르 태그 매핑 테이블 참조 (`youtube/YOUTUBE.md`)

### 7.3 장르 혼동 방지 체크

1. **concept.md 헤더**에서 장르 확인
2. `youtube/YOUTUBE.md` 시리즈별 장르 태그 매핑 참조
3. 제목/태그에 정확한 장르 반영

**⚠️ 장르 태그 매핑 확인 없이 메타데이터 작성 금지**
