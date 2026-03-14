# Wavvy LYRICS.md

Version: 4.0
Last Updated: 2026-03-14
Purpose: Suno 가사 입력(Lyrics) 규칙 SSOT

---

## 0. Korean Lyric Positioning

> **핵심 차별점: 한국어 보컬 플레이리스트**

**원칙:**
- 혼자 읽히고 혼자 들리는 언어
- 말보다 **소리가 먼저 닿는** 한국어
- 장르별 밀도 조절 (Chillhop=텍스처, R&B=서사)

**지향:** 사물·공간·현상 중심, "가사 없는 듯 들리지만 읽으면 남는 가사"

---

## 1. Lyric Prompt Guide

> Suno 가사 입력란에 넣는 "작사 방향 지시". 풀 가사 대신 mood/theme 힌트를 제공하거나 비워두면 Suno가 자체 작사.
> Style prompt에 보컬 지시를 남겨두면 Suno가 자연스러운 허밍/맨트라 수준 보컬을 자동 생성.

### 1.1 3가지 모드

| 모드 | 설명 | 예시 |
|------|------|------|
| **Empty** | 완전 비움 — Suno 자유 생성 | (LYRICS 섹션 비움) |
| **Prompt** | 1-3줄 mood/theme 힌트 | `Korean lyrics about midday warmth, hazy drowsy rhythm` |
| **Structure** | 구조 태그만 — 섹션 구분 유도 | `[verse][chorus][bridge][outro]` |

### 1.2 Prompt 작성법

- **괄호 없이** 영문으로 직접 작성 (소괄호 사용 금지 — Suno가 보컬로 읽음)
- 핵심 감정/장면 키워드 2-3개
- 시리즈 `LYRICS_DNA.md` 있으면 참조 (톤, 이미지 소재 풀)
- 길이: 1-3줄 (짧을수록 Suno 자유도 높음)

**예시:**
```
Korean lyrics about midday heat, hazy afternoon, drowsy rhythm
Minimal Korean lyrics, repetitive hook chant, English hook in chorus
```

### 1.3 Do / Don't

| Do | Don't |
|----|-------|
| 분위기/장면 키워드 | 풀 가사 직접 작성 |
| 영문 방향 지시 | 한국어 가사 행 나열 |
| 짧고 추상적 | 구체적 운율/음절 지정 |
| 괄호 없이 직접 작성 | `(...)` 소괄호로 감싸기 — Suno가 보컬로 읽음 |

---

## 2. Suno Input Rule

### 2.1 절대 금지 (Suno 가사 입력란)
- `(Scene: ...)`, `(Emotion: ...)`, `(Mood: ...)` → Style로 이동

### 2.2 괄호 규칙 (SSOT)

| 규칙 | 설명 |
|------|------|
| `[]` 대괄호 | 구조 태그 전용 |
| `()` 소괄호 | 보컬 메타 + 작사 프롬프트 (한 줄 통합) |
| 1행 원칙 | 구조 태그 뒤 `()` **1행만** |

### 2.3 금지 태그
`[Kick in]`, `[Drums enter]`, `[Pad widens]` → Style Prompt로

### 2.4 허용 태그
**필수:** `[intro]`, `[outro]`, `[verse]`, `[bridge]`, `[chorus]`
**조건부:** `[pre-chorus]`, `[hook]`, `[instrumental]`, `[end]`

**보컬 키워드:** `No harmony`, `Direct vocal`, `Chest voice`, `Powerful belt`

### 2.5 Song Structure Patterns

| 구조 | 패턴 | 용도 |
|------|------|------|
| **Pop Standard** | V-C-V-C-B-C | 대중적, 안정감 |
| **Storyteller** | V-V-C-V-C | 포크/스토리텔링, Verse 많음 |
| **Short & Sweet** | C-V-C-V-C | 짧고 강렬, 힙합 |
| **K-POP Standard** | V-P-C-V-P-C-B-C | Pre-Chorus 고조 → Chorus |
| **K-POP Hook** | Hook-V-P-Hook-V-P-Hook-B-Hook | 훅 시작, 힙합 |

**태그 매핑:** V=`[Verse]`, C=`[Chorus]`, B=`[Bridge]`, P=`[Pre-Chorus]`, Hook=`[Hook]`
