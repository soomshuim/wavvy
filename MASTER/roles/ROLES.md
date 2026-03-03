# Wavvy Role System

Version: 2.0
Last Updated: 2026-03-03
Purpose: AI 역할 분리 (중복/드리프트 방지)

---

## Core Principle

역할 분리 목적:
- Prompt overfitting 방지
- 알고리즘 중복 리스크 방지
- Creative drift 방지

**규칙:** 역할은 겹치지 않는다. "무난함" = FAIL.

---

## Seed Energy Contract

> **금지는 레이어에만, 허용은 에너지에.**

- Verse2 emotional escalation 필수
- Chorus vocal intensity > Verse2
- Higher register/belt 권장
- Energy = vocal delivery, NOT layering

**Canonical:**
```
Lead vocal remains single and dominant. No stacked harmonies.
Vocal line may intensify dynamically, but no additional layers.
```

---

## S1-S10 Validation

모든 AI 출력에 필수:

| # | 슬롯 | 체크 |
|---|------|------|
| S1 | Vocal Persona | gender + tone + delivery |
| S2 | Vocal Processing | dry/close-mic |
| S3 | Lead Instrument | 악기명 |
| S4 | Rhythm Source | 리듬 요소 |
| S5 | BPM | 숫자 |
| S6 | Key/Mode | 조성 |
| S7 | Musicality | V2 lift + Chorus lift |
| S8 | Harmony Guard | 문장 포함 |
| S9 | Articulation | articulation |
| S10 | Sound Eng | EQ balanced, clean mix |

**S1 비어있음 = 즉시 FAIL**

---

## Role Overview

| Role | Function | Allowed | Forbidden |
|------|----------|---------|-----------|
| Seed Researcher | Reference 분석 | Bullets | Prompts, Lyrics |
| Seed Designer | Seed DNA 정의 | DNA, Constraints | Track variation |
| Variation Designer | 안전한 변주 | Slot changes | Seed 변경 |

---

## 1. Seed Researcher

- Reference에서 "왜 작동하는지" 추출
- Bullet points, Cause→Effect
- Prompts/Lyrics 작성 금지

---

## 2. Seed Designer

- 8-15 트랙 생산 가능한 Seed DNA 설계
- Style Prompt 8-10 토큰
- Musicality Matrix + Exclude ≤3 그룹

**필수 참조:** museA_suno_guide.md, LYRICS.md, STYLE.md

**Sanity Check:**
1. "10 variations 후에도 identity 유지되나?"
2. "Verse2 energy permission 있나?" (YES 필수)

---

## 3. Variation Designer

- Seed 내에서 안전한 변주
- 최소 2개 슬롯 선택
- Seed constants 변경 금지

**FAIL 조건:**
- Chorus ≤ Verse2 에너지
- Chorus에 vocal layering
- V2 마지막 2행 안 올라감
- Vocal Persona 없음

**출력:** SAFE / BORDERLINE / FAIL

---

## Controlled Variation Pattern

| 구분 | 역할 | 예시 |
|------|------|------|
| Core | 고정 | 장르 spine, BPM 범위 |
| Variable | 변주 | 가사 톤, 악기 |
| Gate | 판정 | ≥80점, 개별 >5 |

**규칙:** Core 정의 → Variable만 변경 → Gate 미달 시 FAIL

---

## Clean Slate Protocol

> 3회 연속 FAIL 시 리셋

1. 이전 버전 완전 삭제
2. "이전 가사 모두 잊고" 지시
3. 톤앤매너 완전 변경
4. 새 버전 → Gate 검증
