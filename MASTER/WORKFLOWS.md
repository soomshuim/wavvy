# Wavvy Workflows

> **모든 작업 워크플로우 통합 문서**
>
> Version: 1.4
> Last Updated: 2026-03-07

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
2. `LYRICS.md` §메타태그 규칙 참조
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

> **SSOT: `MASTER/cli/SPEC.md`**

- 반드시 시리즈/트랙/구간 확인 후 생성. 시작/종료 시간 임의 수정 절대 금지
- Hook Title (선언문, 가사 그대로 사용 금지) + Bottom Lyric (하단 가사) 2-Layer 구조
- 타이포: Shadow 필수, Stroke 금지, 하단 30% 침범 금지 (YouTube UI 영역)
- CLI: `python3 wavvy.py shorts <track> --start MM:SS --duration SEC [--title "..."] [--srt file.srt]`

---

## 5. 영상 패키징

> **SSOT: `MASTER/cli/SPEC.md` §7**

vfade(테스트) → vfade(본생성) → pack 순서. 상세 명령어와 옵션은 CLI SPEC.md 참조.

---

## 6. YouTube 메타데이터

> **SSOT: `MASTER/youtube/YOUTUBE.md` §9**

Phase 1(Draft) → Phase 2(Final) 순서. 상세 절차는 YOUTUBE.md 참조.
