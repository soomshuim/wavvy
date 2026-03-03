# Wavvy LYRICS.md

Version: 3.2
Last Updated: 2026-03-03
Purpose: 가사 규칙 SSOT

> **예시**: `lyrics/REFERENCE_SAMPLE.md`, `lyrics/FAILURE_CASES.md` 참조

---

## 0. Korean Lyric Positioning

> **핵심 차별점: 한국어 가사 플레이리스트**

**원칙:**
- 혼자 읽히고 혼자 들리는 언어
- 말보다 **소리가 먼저 닿는** 한국어
- 장르별 밀도 조절 (Chillhop=텍스처, R&B=서사)

**금지:** 설명적 문장, 감정 직접 표출 (사랑해, 슬퍼), 메타 표현
**지향:** 사물·공간·현상 중심, 한 문장 한 이미지, "가사 없는 듯 들리지만 읽으면 남는 가사"

---

## 1. Core Lyrical Engineering Rules

### 1.1 Metric Mirroring (V1-V2 대칭)
V1과 V2는 **음절 수, 행 수, 문장 구조** 완전 동일

### 1.2 Rhyme / Ending Mirroring
V1-V2 끝 단어: **품사** 엄격히 일치 (동사↔동사, 형용사↔형용사)
- ❌ "서 있어"(동사) vs "차가워"(형용사)
- ✅ "차가워" vs "따가워"

### 1.3 Chorus Static Rule
- 후렴 가사: **전 구간 100% 동일**, **3~4행**
- Chorus 2, 3에서 가사 변경 금지

### 1.4 Bridge Anchor Rule
- **Thesis**: 고정 1라인 (현상 기반, 사람/관계 금지)
- **Scene**: 2~3라인 (동작/감각/이미지)
- B1과 B2: Thesis 동일, Scene 변주

### 1.5 Vocabulary Independence
- 트랙 간 **핵심 은유 겹침 금지**
- 제목 단어 → 다른 트랙 키워드 금지

### 1.6 Snapshot Hook Rule
- Chorus 훅은 **이미지형** ("명사+동사" 스냅샷)
- ❌ "물안개 속에서 혼자 걷는 이 밤"
- ✅ "가로등이 번져" / "발자국이 미끄러져"

### 1.7 V2 Escalation Rule
- Verse 2 **마지막 2행** = 감정 에스컬레이션 유도
- **동사 강화**: 스쳐가 → 휩쓸려
- **감각 강화**: 희미해 → 차가워
- **호흡 단어**: 숨, 목, 가슴, 떨림

예시:
- V1: "걸음을 멈춰도 / 소리만 맴돌아"
- V2: "숨을 삼켜봐도 / 가슴이 떨려와" ← 신체 반응

---

## 2. Pure Lyric Input Rule

### 2.1 절대 금지 (Suno 가사 입력란)
- `(Scene: ...)`, `(Emotion: ...)`, `(Mood: ...)` → Style로 이동

### 2.2 괄호 규칙 (SSOT)

| 규칙 | 설명 |
|------|------|
| `[]` 대괄호 | 구조 태그 전용 |
| `()` 소괄호 | 보컬 + 악기 + 코드 (한 줄 통합) |
| 1행 원칙 | 구조 태그 뒤 `()` **1행만** |
| 필수 메타 | `Chest voice`, `No harmony`, `Direct vocal` 중 1개+ |

### 2.3 금지 태그
`[Kick in]`, `[Drums enter]`, `[Pad widens]` → Style Prompt로

### 2.4 허용 태그
**필수:** `[intro]`, `[outro]`, `[verse]`, `[bridge]`, `[chorus]`
**조건부:** `[pre-chorus]`, `[hook]`, `[instrumental]`, `[end]`

**보컬 키워드:** `No harmony`, `Direct vocal`, `Chest voice`, `Powerful belt`

### 2.5 QC Fail 조건
| # | 조건 |
|---|------|
| F1 | 감정/분위기 태그가 Lyrics에 있음 |
| F2 | 소괄호가 가사와 같은 행 |
| F3 | 대괄호에 악기/편곡 지시 |
| F4 | 보컬 메타에 `[]` 사용 |
| F5 | `()` 2행 연속 |

### 2.6 가사 길이
- 전체: **100-120 단어**
- 섹션: **4-6행**
- 행: **6-10음절**
