# Chillhop Genre Rubric

Version: 1.2
Last Updated: 2026-02-21
Purpose: Chillhop 장르 적합성 평가 루브릭
Scope: 장르가 Chillhop인 트랙의 Seed Design / Variation Design QA
Pass Criteria: 80점 이상
Fail Criteria: 80점 미만 (재디자인 필수)

---

## 핵심 철학

> **Chillhop은 재즈의 세련됨과 따뜻한 폴리싱이 만나는 지점이다.**
>
> Lo-fi의 "dusty/muffled"가 아니라 **"warm but crisp"**.
> 재즈 코드와 라이브 사운드 악기가 곡의 뼈대를 만들고, 보컬은 악기처럼 녹아든다.

---

## Evidence Basis (Web Research)

이 루브릭은 아래 근거를 기반으로 한다.

### 1. Chillhop vs Lo-fi Hip Hop 차이점

| 항목 | Lo-fi Hip Hop | Chillhop |
|------|---------------|----------|
| **BPM** | 60-90 | **80-110** |
| **음질** | Low-fidelity, dusty, muffled | **High-fidelity, crisp, polished** |
| **악기** | Filtered samples, "underwater" | **Live-sounding: Rhodes, sax, acoustic guitar** |
| **분위기** | 밤, 고독, 수면용 | **낮, 활기, 작업/공부용** |
| **질감** | Vinyl crackle, tape hiss 강함 | Warm하지만 깨끗 |

### 2. Chillhop 핵심 특성

- Lo-fi hip hop + Jazz 요소 결합
- **High-fidelity** production with crisp drums
- **Live-sounding instrumentation**: Rhodes piano, saxophone, acoustic guitar
- Swing feel, jazzy chord voicings (7th/9th chords)
- "Daylight" mood vs Lo-fi's "night" mood

### 3. AM_1000 특수 조건

- Korean vocals with buried mix (텍스처화)
- 업무 배경음악 용도
- 운영 BPM 범위: **78-105** (Chillhop 기준 반영)

### References

- [Lo-fi vs Chillhop - Latte Chill](https://lattechill.com/wp/2024/03/25/lofi-vs-chillhop-a-melodic-showdown/)
- [Chillhop - Hip Hop Music History](https://www.hiphopmusichistory.com/subgenres/chillhop/)
- [Music Genres BPM - Gemtracks](https://www.gemtracks.com/resources/guides/view.php?title=music-genres-and-their-typical-bpms&id=823)

---

## Phase 0 Hard Gates (선행 통과 조건)

아래 항목 중 하나라도 FAIL이면 점수 계산 전에 재작성한다.

1. **BPM이 78-105 범위에 명시**
2. **Jazzy 요소 2개 이상 포함** (Rhodes, Wurlitzer, jazz guitar, saxophone, upright bass, swing feel, jazzy chords 중)
3. Vocal buried/low mix 지시 포함 (Style Prompt에 명시)
4. Exclude가 1-8개이고 하모니 가드 항목 2개 이상 포함
5. 목표 길이 3분 이상을 구조 또는 스타일에서 명시
6. **"dusty" 또는 "muffled" 키워드 미포함** (Lo-fi와 구분)
7. **[Intro] = Instrumental only** (no vocals, no humming, no scat)

---

## 루브릭 (6개 팩터, 100점)

### 1. Jazz Elements (재즈 요소) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | 재즈 코드 보이싱(7th/9th) + 스윙 필 + 재즈 악기(Rhodes/Sax/Jazz Guitar) 2개 이상 명확 |
| 14-17 | 재즈 요소 2개 존재하나 일부 구간에서 약함 |
| 10-13 | 재즈 요소 1개만 존재, 추가 필요 |
| 5-9 | 재즈보다 일반 Lo-fi에 가까움 |
| 0-4 | Chillhop으로 보기 어려움 |

**핵심 원칙**:
- **필수 악기 (2개 이상)**: Rhodes, Wurlitzer, Jazz Guitar, Saxophone, Upright Bass
- 7th/9th chord voicings 권장
- Swing 또는 laid-back groove 필수
- **Live-sounding**, not sampled/filtered

---

### 2. Groove & Feel (그루브/분위기) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | Laid-back swing feel 명확, "daylight" 에너지, 세련됨 |
| 14-17 | 그루브 양호, 일부 구간 흐름 어색 |
| 10-13 | 그루브 존재하나 swing feel 부족 |
| 5-9 | 기계적/straight beat, 느긋함 없음 |
| 0-4 | Chillhop 그루브 부재 |

**핵심 원칙**:
- Swing feel, lazy groove, behind-the-beat
- **"Daylight" mood** (밝고 활기참, 밤/고독 아님)
- 급격한 템포/다이나믹 변화 금지
- "깔아두는 음악" 체감 필수

---

### 3. Warmth & Polish (따뜻함과 폴리싱) — 15점

| 점수 | 기준 |
|------|------|
| 14-15 | **High-fidelity but warm**: 깨끗하지만 차갑지 않음, subtle saturation |
| 11-13 | 음질 양호하나 약간 muddy하거나 너무 차가움 |
| 7-10 | Lo-fi처럼 dusty/muffled하거나 너무 sterile |
| 0-6 | 음질 문제 심각 |

**핵심 원칙**:
- ✅ **Crisp, clean, polished** (Chillhop 정체성)
- ✅ **Warm saturation** (subtle, not heavy)
- ❌ **Dusty, muffled, underwater** (Lo-fi 영역)
- ❌ **Heavy vinyl crackle, tape hiss** (과하면 Lo-fi)

---

### 4. Vocal Integration (보컬 통합) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | 보컬이 악기처럼 묻혀서 배경 텍스처로 작용, 집중 방해 없음 |
| 14-17 | 보컬 존재하나 살짝 앞으로 나옴 |
| 10-13 | 보컬이 악기와 분리되어 들림 |
| 5-9 | 보컬이 전면에 나와서 배경음악 부적합 |
| 0-4 | 보컬 처리 실패 |

**핵심 원칙**:
- **Buried vocal**: deep in mix, underneath instruments, far back in soundstage
- Heavy ambient reverb, distant, recessed (not intimate/forward)
- 가사가 "들리지만 귀에 안 꽂히는" 상태
- 배경음악으로 틀어놔도 업무 집중 가능

**Style Prompt 권장 표현**:
```
Vocals buried deep in mix, underneath instruments.
Heavy ambient reverb, far back in soundstage.
Vocal as background texture, not lead.
```

---

### 5. Structural Flow (구조 흐름) — 15점

| 점수 | 기준 |
|------|------|
| 14-15 | 섹션 전환이 부드럽고 예측 가능, 3분+ 자연스럽게 달성 |
| 11-13 | 구조는 있으나 전환이 다소 급격 |
| 7-10 | 반복감 높거나 구조 단조 |
| 0-6 | 목표 길이 미달 또는 구조 설계 부재 |

**핵심 원칙**:
- 최소 길이: **3분 이상**
- 급격한 변화 금지 (업무 집중 방해)
- 권장 섹션: intro / verse / chorus / interlude / bridge / outro

---

### 6. Genre Boundary Guard (장르 경계 보호) — 10점

| 점수 | 기준 |
|------|------|
| 9-10 | Chillhop 정체성 명확, 타 장르 침범 없음 |
| 7-8 | 대체로 명확하나 일부 경계 혼합 |
| 4-6 | Lo-fi Hip Hop/Jazz/R&B 경계 애매 |
| 0-3 | 장르 정체성 붕괴 |

**핵심 원칙**:
- **Chillhop ≠ Lo-fi Hip Hop**: dusty/muffled 피하기
- **Chillhop ≠ Pure Jazz**: 재즈 솔로 과시 금지
- 금지 경향: EDM elements, aggressive drums, rock energy, heavy distortion
- 허용: R&B 보컬 뉘앙스 (단, buried 유지)

---

## 체크리스트 (간이 판정)

```
□ BPM 78-105, 적당히 활기찬 템포
□ 재즈 요소 2개 이상 (Rhodes/Sax/Jazz Guitar/Upright Bass/Swing)
□ Swing feel, laid-back groove 유지
□ High-fidelity but warm (dusty/muffled 아님)
□ 보컬이 묻혀서 텍스처처럼 작용
□ 3분 이상, 부드러운 섹션 전환
□ "Chillhop"이라고 즉시 설명 가능 (Lo-fi 아님)
```

---

## QA 워크플로우

```
Step 1. Seed/Variation 디자인 완료 (가사 + Style + Exclude)
Step 2. 기존 QC 통과 확인 (가사 체크리스트 + S0-S20 + 글자수)
Step 3. Phase 0 Hard Gates 통과 확인
Step 4. 장르가 Chillhop인 경우 → Chillhop Rubric 실행
Step 5. 6개 팩터별 채점 + 총점 산출
Step 6. 판정:
        ≥ 80점 → PASS (제안 가능)
        < 80점 → FAIL (재디자인 필수, 유저에게 제안 금지)
        개별 팩터 5점 이하 → 해당 팩터 CRITICAL FAIL (총점 무관 재디자인)
Step 7. PASS 시 채점표와 함께 output
```

**CRITICAL FAIL 규칙**: 총점이 80 이상이어도 개별 팩터 5점 이하가 하나라도 있으면 FAIL.

---

## QC 출력 템플릿 (권장)

```md
Chillhop Rubric Score
- Track: AM_1000 / 01
- Hard Gates: PASS/FAIL

| Factor | Score | Notes |
|------|------:|------|
| Jazz Elements |  |  |
| Groove & Feel |  |  |
| Warmth & Polish |  |  |
| Vocal Integration |  |  |
| Structural Flow |  |  |
| Genre Boundary Guard |  |  |
| Total |  |  |

Verdict: PASS / FAIL
```

---

## Changelog

- 2026-02-21: v1.0 초안 작성 (AM_1000 업무시간 시리즈용)
- 2026-02-21: v1.2 Track 01 실험 결과 반영
  - Hard Gate 추가: **[Intro] = Instrumental only** (no vocals, no humming, no scat)
  - Vocal Integration 강화: **buried deep, underneath instruments, far back in soundstage**
  - Style Prompt 권장 표현 추가
- 2026-02-21: v1.1 웹 리서치 기반 전면 수정
  - BPM 70-82 → **78-105** (Chillhop 표준 반영)
  - 질감: dusty → **warm but crisp, high-fidelity**
  - Hard Gate: 재즈 요소 **2개 이상** 필수
  - "Lo-fi Texture" → **"Warmth & Polish"** 리네이밍
  - Evidence Basis 추가 (웹 리서치 출처)
  - Lenny's Product Team 협의 반영
