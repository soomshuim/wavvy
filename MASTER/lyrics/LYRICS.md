# Wavvy LYRICS.md

Version: 4.5
Last Updated: 2026-09-30
Purpose: Suno 가사 입력(Lyrics) 규칙 SSOT

---

## 0. Korean Lyric Positioning

> **핵심 차별점: 한국어 보컬 플레이리스트**

**원칙:**
- 혼자 읽히고 혼자 들리는 언어
- 말보다 **소리가 먼저 닿는** 한국어
- 장르와 곡에 맞는 밀도 조절 (Chillhop의 텍스처나 R&B의 서사는 가능한 선택지이며 필수 공식이 아니다)
- 시간대 컨셉은 가사 주제 강제가 아니라 BPM/Mood/Energy 포지셔닝이다

**지향:** 읽었을 때 자연스러운 한국어와 곡에 맞는 표현. 사물·공간·현상은 선택 가능한 소재다.

### 0.1 Time Concept vs Lyrics

- 각 시리즈의 시간대는 주로 사운드 톤앤매너를 정한다.
- 가사가 반드시 `17:00`, `퇴근`, `점심`, `수면 전` 같은 시간/활동을 직접 다룰 필요는 없다. 자연스럽게 필요한 경우에는 사용할 수 있다.
- 우선순위는 **BPM → Mood → 장르 에너지 → 보컬 톤 → 가사 주제**다.
- 가사는 해당 시리즈의 사운드·장르·주제 조건과 맞추되, 문장 자체의 자연스러움을 우선한다.
- 시간/활동 소재를 후렴이나 핵심 주제로 쓰는 것도 가능하다. 시간대만을 이유로 소재를 강제하지 않는다.

---

## 1. Lyric Prompt Guide

> 이 절은 Suno가 가사를 직접 쓰게 할 때의 짧은 방향 지시다. 사용자가 검토한 전체 가사는 별도 경로로 Custom Mode의 Lyrics 입력란에 넣을 수 있다(§1.6).

### 1.1 3가지 모드

| 모드 | 설명 | 예시 |
|------|------|------|
| **Empty** | 완전 비움 — Suno 자유 생성 | (LYRICS 섹션 비움) |
| **Prompt** | 1-3줄 mood/theme 힌트 | `Korean lyrics about midday warmth, hazy drowsy rhythm` |
| **Structure** | 구조 태그만 — 섹션 구분 유도 | `[verse][chorus][bridge][outro]` |

### 1.2 Prompt 작성법

- **Prompt-only 모드는 괄호 없이** 영문으로 직접 작성 (소괄호 문장이 노래로 처리될 가능성을 줄이려는 Wavvy 내부 입력 규칙)
- 핵심 감정/장면 키워드 2-3개
- 시리즈 `LYRICS_DNA.md` 있으면 참조 (톤, 이미지 소재 풀)
- 길이: 1-3줄 (짧을수록 Suno 자유도 높음)
- **약칭 구조 포맷 권장** — 구조 태그를 압축하여 키워드 공간 확보 (§1.4 참조)

**예시:**
```
Korean lyrics about midday heat, hazy afternoon, drowsy rhythm
Minimal Korean lyrics, repetitive hook chant where the track calls for it
```

### 1.4 약칭 구조 포맷

> 약칭은 짧은 prompt-only 입력에서 공간을 아끼려는 Wavvy 내부 표기다. 확인한 Suno 공식 자료는 이 약칭의 인식률이나 200자 제한을 보증하지 않는다. 섹션을 분명히 지정해야 하는 완곡 가사는 명시적 구조 태그를 쓴다.

**약칭 매핑:**

| 약칭 | 풀 태그 |
|------|---------|
| I | Intro |
| V / V1 / V2 | Verse / Verse 1 / Verse 2 |
| PC | Pre-Chorus |
| C | Chorus |
| PC2 | Post-Chorus |
| B | Bridge |
| O | Outro |

**사용법:**
- 하이픈 연결로 1행 구조 선언: `I-V1-PC-C-PC2-V2-C-B-C-O`
- 나머지 글자 수를 키워드에 할당

**예시 (풀 태그 vs 약칭):**
```
# 풀 태그 (~89자 구조)
[intro][verse 1]Minimal Korean, sunlight[pre-chorus][chorus]Hook chant[post-chorus]Ad-lib[verse 2][chorus][bridge][chorus][outro]

# 약칭 (~30자 구조, 키워드 공간 +60자)
I-V1-PC-C-PC2-V2-C-B-C-O
Minimal Korean, midday noon heat, lunch hour pause, warm feeling, repeating phrase where useful
```

### 1.3 Do / Don't

| Do | Don't |
|----|-------|
| 분위기/장면 키워드 | prompt-only 입력에 풀 가사 섞기 |
| 영문 방향 지시 | 한국어 가사 행 나열 |
| 짧고 추상적 | 구체적 운율/음절 지정 |
| Prompt-only 모드는 괄호 없이 직접 작성 | Prompt-only 내용을 `(...)` 소괄호로 감싸기 — 노래로 처리될 가능성을 줄이기 위한 내부 규칙 |

### 1.5 Wavvy Lyric Skill / Review Gate

Full lyric drafting, rewrite, and review tasks should use `skills/wavvy-lyricist/SKILL.md`.

- Contract: `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`
- Pattern reference: `skills/wavvy-lyricist/references/patterns.md`
- Package check: `python3 wavvy.py lyrics-skill SERIES/[series] --json`
- Artifact check: `python3 wavvy.py lyrics-skill SERIES/[series] --artifact FILE --mode full-lyric-draft --json`
- New full-song artifact check: `python3 wavvy.py lyrics-skill SERIES/[series] --artifact FILE --mode full-lyric-draft --draft-scope full-song --json`
- Gate stage: `python3 wavvy.py gate SERIES/[series] --stage lyrics-review --json`

This document remains the SSOT for direct Suno Lyrics input. The skill must preserve the mode boundary: `full-lyric-draft` is for human/source review, while `suno-prompt-only` must stay short, English, and prompt/structure-only.

### 1.6 직접 쓴 전체 가사와 곡 길이 계획

Suno [공식 도움말](https://help.suno.com/en/articles/2415873)은 Custom Mode에서 직접 쓴 전체 가사 입력을 안내한다. Wavvy의 `full-lyric-draft`는 사용자 검토를 위한 원문이며, 승인된 본문은 이 경로에 넣을 수 있다. `suno-prompt-only`는 Suno가 가사를 쓰게 하는 별도 선택이다. 두 모드를 한 LYRICS 본문에 섞지 않는다.

새 **완곡**을 요청받으면 초안 기록에 `draft_scope: full-song`, 목표 길이(초), 예상 BPM, 박자, 순서별 섹션 마디 수를 적는다. 예상 길이(초)는 `전체 마디 × 박자 수 × 60 ÷ BPM`으로 계산한다. 기본 출발점은 `[Intro]`, 짧게 나눈 Verse 3개, `[Outro]`다. 곡에 맞는 Chorus·Bridge·연주 구간을 사이에 두고, 가창 구절 뒤 보컬이 쉬는 마디도 계획한다. 다른 Verse 개수가 맞으면 그 곡의 이유를 `verse_structure_exception`에 적는다. 글자 수 하한·행 길이 상한이나 가사 총량 증가를 목표로 삼지 않는다. 한 문장을 줄바꿈만 해서 숨 쉴 틈이 생겼다고 판정하지 않는다. 실제 이어지는 문장 길이와 Verse 밀도, 구절 뒤 쉼을 읽고 소리 내어 검토한다. 짧은 발췌, 기존 원문 기록, review-only, prompt-only에는 이 신규 완곡 계획을 강제하지 않는다.

섹션 마디 수는 작성자가 고른 편곡 계획이며 가사 한 줄을 고정 마디 수로 환산한 값이 아니다. 초안 Self-Gate에는 Verse별 실제 가창행 수, 가장 긴 가창행, 이어지는 두 행의 자연스러운 구절 구분, 인용한 구절 뒤 쉼을 남긴다. 글자 수만으로 가창성을 판정할 수 없으므로 이는 작성자의 검토 근거다. 이 계산과 태그는 제작 목표일 뿐이다. Suno가 실제 Intro·길이·박자·숨 쉴 틈을 지키는지는 생성 후 오디오로 확인하고, 부족하면 가사/구조 또는 Extend를 검토한다. [Suno의 길이 안내](https://help.suno.com/en/articles/13924929)는 단일 생성의 상한과 Extend를 설명하며 특정 곡의 목표 길이를 보장하지 않는다.

---

## 2. Suno Input Rule

### 2.1 절대 금지 (Suno 가사 입력란)
- `(Scene: ...)`, `(Emotion: ...)`, `(Mood: ...)` → Style로 이동

### 2.2 괄호 규칙 (SSOT)

| 규칙 | 설명 |
|------|------|
| `[]` 대괄호 | 구조 태그 전용 |
| `()` 소괄호 | 기본 금지. Structure 모드에서만 구조 태그 뒤 짧은 작사 방향을 한 줄로 통합할 때 예외 허용. 보컬·편곡 지시는 Style로 이동 |
| 1행 원칙 | 예외 사용 시 구조 태그 뒤 `()` **1행만** |

정리: §1 Prompt-only 모드는 괄호를 쓰지 않는다. §2 Structure 모드는 `[Verse]`, `[Chorus]` 같은 구조 태그 뒤에 한 번만 `(Korean lyrics about...)` 형태의 작사 방향을 둘 수 있다. 이 제한은 Wavvy의 입력 정리 규칙이지 Suno의 파싱 보증이 아니다.

### 2.3 금지 태그
`[Kick in]`, `[Drums enter]`, `[Pad widens]` → Style Prompt로

### 2.4 허용 태그
**신규 완곡 초안 기본 구조:** `[Intro]`, Verse 3개, `[Outro]` (명시한 사용자·트랙 예외가 있으면 기록)
**곡에 맞춰 선택:** `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Hook]`, `[Bridge]`, `[Instrumental]`, `[End]`

보컬 성격과 편곡 지시는 가사 줄이나 구조 태그에 끼워 넣지 말고 Style에 쓴다.

### 2.5 Song Structure Patterns

| 구조 | 패턴 | 용도 |
|------|------|------|
| **Pop Standard** | V-C-V-C-B-C | 대중적, 안정감 |
| **Storyteller** | V-V-C-V-C | 포크/스토리텔링, Verse 많음 |
| **Short & Sweet** | C-V-C-V-C | 짧고 강렬, 힙합 |
| **K-POP Standard** | V-P-C-V-P-C-B-C | Pre-Chorus 고조 → Chorus |
| **K-POP Hook** | Hook-V-P-Hook-V-P-Hook-B-Hook | 훅 시작, 힙합 |

**태그 매핑:** V=`[Verse]`, C=`[Chorus]`, B=`[Bridge]`, P=`[Pre-Chorus]`, Hook=`[Hook]`
