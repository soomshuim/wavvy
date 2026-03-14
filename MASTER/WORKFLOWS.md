# Wavvy Workflows

> **모든 작업 워크플로우 통합 문서**
>
> Version: 2.0
> Last Updated: 2026-03-14

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
Track: {제목} ({영문})
Type: {A/B/C}
BPM: {숫자}
Key: {키}
Length: 3min+

=== STYLE ===
{스타일 프롬프트}

=== EXCLUDE ===
{제외 키워드}

=== LYRICS ===
{작사 프롬프트 또는 비움 — LYRICS.md §1 참조}
```

---

## 1. 트랙 프롬프트 생성 워크플로우

> **SSOT: `MASTER/lyrics/LYRICS.md` §1 (Lyric Prompt Guide)**

### 절차
1. `concept.md` + `LYRICS_DNA.md`(있으면) 참조 — 시리즈 톤/방향 확인
2. Style + Exclude + Lyric Prompt(또는 비움) 작성 → txt 저장
3. 사용자 컨펌 → Suno 제출

> Lyric Prompt 3가지 모드: Empty(비움), Prompt(mood/theme 힌트), Structure(구조 태그만). 상세는 LYRICS.md §1 참조.

---

## 2. 스타일/프롬프트 수정 절차

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
