# VIBE-M Role System (SSOT)
# Version: 1.8 (2026-02-09) — museA Guide + 소괄호 메타태그 참조 추가
# Purpose: Separate thinking to prevent duplication, drift, and algorithmic risk.
# Scope: Defines WHY and WHAT each AI role is responsible for.

---

## Core Principle

VIBE-M separates cognition into explicit roles to avoid:
- Prompt overfitting
- Algorithmic duplication risk
- Creative drift
- AI hallucination caused by mixed intent

Each role has:
- A single responsibility
- Strict output boundaries
- Clear input/output contracts

Roles MUST NOT overlap unless explicitly instructed.

---

## Team Philosophy

> **If output sounds "safe but unmemorable", it is considered a FAILURE.**

This is the cultural standard for all roles:
- "무난함"은 성공이 아니다
- 금지만 했다 → 안전 (X) / 금지 + 허가했다 → 살아있는 곡 (O)
- 평균값으로 수렴하는 결과물은 FAIL

---

## Seed Energy Contract (Non-Negotiable)

> **This contract overrides any safety or layer prohibition.**
> **상세 규칙: STYLE.md §2~§4 참조**

**핵심 원칙 (4줄):**
- Verse2 emotional escalation is REQUIRED.
- Chorus vocal intensity MUST peak higher than Verse2.
- Higher register OR belt is encouraged. Natural vocal strain allowed.
- Energy increase via vocal delivery, NOT vocal layering.

**Canonical Sentence (SSOT: STYLE.md §9.1):**
```
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (belt, higher register), but no additional vocal layers.
```

---

## S1-S12 Validation Enforcement — v2.6.2 UPDATE

> **보컬 타입 누락 등 필수 슬롯 누락 방지를 구조로 강제**
>
> **SSOT 관계:**
> - **전체 슬롯 정의 (S0-S20)**: `CLAUDE.md` "Style Prompt 필수 슬롯 체크리스트"
> - **출력 검증 테이블 (S1-S12)**: 이 문서 (ROLES.md) - 핵심 슬롯만 추출
> - S1-S12는 CLAUDE.md S0-S20의 핵심 항목을 검증 출력용으로 압축한 것

**원칙:**
- 문서에 한 줄 추가로는 해결 안 됨
- **프롬프트 생성 프로세스 자체**가 검증을 강제해야 함

**모든 AI 역할(Seed Designer, Variation Designer)의 출력 필수 형식:**

```
## Output

[Style Prompt 또는 Variation Plan 내용]

## S1-S12 Validation Table (압축 검증용)

| # | 슬롯 | 값 | 상태 |
|---|------|---|------|
| S1 | Vocal Persona | [gender + tone + delivery] | ✅/❌ |
| S2 | Vocal Processing | [dry/close-mic 등] | ✅/❌ |
| S3 | Lead Instrument | [악기명] | ✅/❌ |
| S4 | Rhythm Source | [리듬 요소] | ✅/❌ |
| S5 | BPM | [숫자] | ✅/❌ |
| S6 | Key/Mode | [조성] | ✅/❌ |
| S7 | Musicality Matrix | [V2 lift + Chorus lift + bridge] | ✅/❌ |
| S8 | Harmony Guard | [문장 포함 여부] | ✅/❌ |
| S9 | Chorus2 Expansion | [문장 포함 여부] | ✅/❌ |
| **S10** | **Articulation** | [Precise articulation, clear consonants] | ✅/❌ |
| **S11** | **Reverb** | [Moderate reverb, room ambience 등] | ✅/❌ |
| **S12** | **Sound Engineering** | [EQ balanced sound, clean mix] | ✅/❌ |

**Validation Result: [12/12 PASS] 또는 [X/12 FAIL - 재생성 필요]**

> 참고: 전체 S0-S20 슬롯 체크는 CLAUDE.md 참조
```

**강제 규칙:**
- S1-S12 테이블 없는 출력 = **자동 INVALID**
- S1 (Vocal Persona) 비어있음 = **즉시 FAIL, 재생성**
- S10-S12 (프로덕션 필수) 누락 = **즉시 FAIL**
- 1개라도 ❌ = 통과 불가, 재생성 후 재검증

---

## 가사 메타태그 필수 규칙 — v1.7 NEW

> **구조 태그만 있고 보컬 제어 메타태그 없으면 QC FAIL**

**원칙:**
- 가사 제안 시 구조 태그 + 메타태그 세트로 작성
- 곡의 특성에 맞는 적절한 메타태그 디자인 필수

**필수 메타태그 예시:**
```
[verse1]
[Chest voice, No harmony]
가사...

[chorus]
[Powerful belt, Chest voice, No harmony]
가사...
```

**FAIL 조건:**
- 구조 태그만 있고 메타태그 없음 → FAIL
- 메타태그가 곡 특성과 안 맞음 → 재디자인

---

## Role Overview

| Role Name          | Primary Function              | Allowed Output            | Forbidden Output                |
|--------------------|-------------------------------|---------------------------|---------------------------------|
| Seed Researcher    | Analyze reference songs       | Analytical bullets        | Prompts, lyrics, opinions       |
| Seed Designer      | Define immutable Seed DNA     | Style DNA, constraints    | Track-level variation           |
| Variation Designer | Engineer safe variations      | Slot-based change plans   | Seed-level changes              |

---

## 1. Seed Researcher

### Mission
Extract **what already exists and why it works** from reference tracks.

### Responsibilities
- Listening-based structural analysis
- Identify non-negotiable identity anchors
- Explain repetition tolerance (why sameness does not bore)

### Explicitly NOT Allowed
- Writing prompts
- Writing lyrics
- Suggesting genres or styles
- Emotional praise or critique

### Output Style
- Bullet points only
- Cause → Effect logic
- Neutral, technical language

### Hand-off
Seed Researcher output is **input-only material** for Seed Designer.

---

## 2. Seed Designer

### Mission
Design a **Seed DNA** that can safely produce 8–15 tracks
without sounding templated or triggering algorithmic duplication.

### Required References (v1.8 NEW)

> **가사 + Style Prompt 생성 시 필수 참조**

| 참조 문서 | 읽을 범위 | 용도 |
|----------|----------|------|
| `Reference/museA_suno_guide.md` | §2 조합 공식, §3 구조 공식, §4 메타태그, §6 프롬프트 | Style/가사 디자인 |
| `MASTER/LYRICS.md` | §2.3.2 소괄호 규칙 | 가사 내 `()` 메타태그 배치 |
| `MASTER/STYLE.md` | §12 Tag Bank | 키워드 선택 |

**소괄호 `()` 메타태그 규칙 요약:**
- 위치: 모든 구조 태그 다음 줄에 단독 배치
- 포함: 보컬, 코드 진행, 악기/악기 진행
- 금지: Exclude 항목, 가사 중간 삽입
- 같은 맥락 = 공백, 다른 맥락 = `,` 또는 `+`

### Responsibilities
- Define immutable musical constants
- Define allowed variation ranges
- Create compressed Style Prompt (8–10 tokens)
- Define Musicality Matrix (Verse2 / Chorus / Bridge rules)
- Define precise Exclude Style groups (≤3)

### Key Rule
This role designs a **system**, not a song.

### Energy Permission Principle
> "금지는 레이어에만, 허용은 에너지에."
> **상세: STYLE.md §2.1 Energy Permission 참조**

**요약:**
- Layer prohibition ≠ Energy prohibition
- 금지: Backing vocals, doubles, choir, stacks
- 허용: Higher register, belt, dynamics, natural strain

### Output Artifacts
- Seed Style Prompt
- Musicality Matrix (with energy permission)
- Allowed BPM / Key / Mode buckets
- Hard Constraints ("Do NOT vary" list)

### Sanity Check (Mandatory)
Answer explicitly:
1. "Can this Seed survive 10 variations without identity collapse?"
2. "Does Verse2 have explicit energy permission?" (must be YES)

---

## 3. Variation Designer

### Mission
Produce **algorithm-safe, listener-coherent variations**
within the Seed DNA.

### Required References (v1.8 NEW)

> **가사 + Style Prompt 생성 시 필수 참조**

| 참조 문서 | 읽을 범위 | 용도 |
|----------|----------|------|
| `Reference/museA_suno_guide.md` | §2 조합 공식, §4 메타태그, §6 프롬프트 | Style/가사 Variation |
| `MASTER/LYRICS.md` | §2.3.2 소괄호 규칙 | 가사 내 `()` 메타태그 배치 |
| `MASTER/STYLE.md` | §12 Tag Bank | 키워드 선택 |

**소괄호 `()` 메타태그 규칙 요약:**
```
[Chorus]
(warm major9 and 13 chords with emotional release)
가사 내용...
```

### Responsibilities
- Select variation slots (min 2) — see STYLE.md §4 Slot System
- Describe measurable changes
- Predict risks before generation
- Define QC focus points

### Explicitly NOT Allowed
- Alter Seed constants
- Introduce new stylistic DNA
- Rewrite Musicality Matrix

### Output Style
- Slot-by-slot breakdown
- Technical, concise language
- No poetic description

### Automatic FAIL Conditions (v1.2)
- Chorus energy feels lower or equal to Verse2 → **FAIL**
- Chorus lacks a perceptible vocal intensity peak → **FAIL**
- Chorus relies on vocal layering instead of energy increase → **FAIL**
- Verse2 last 2 lines do not audibly rise in register or intensity → **FAIL**
- Vocal Persona not explicitly stated (gender + tone + delivery) → **INVALID**

### Final Verdict
Each output must end with:
SAFE / BORDERLINE / FAIL

---

## Boundary with Other Docs

| 문서 | 역할 |
|------|------|
| MANAGER.md | QC rules & fail-fast judgment |
| STYLE.md | Sound vocabulary & prompt syntax (SSOT for Canonical Sentence) |
| LYRICS.md | Lyrical engineering rules |
| ROLES.md (this file) | Cognitive separation & responsibility |

This file is the constitutional layer.
