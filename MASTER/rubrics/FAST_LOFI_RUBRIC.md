# Fast Lo-fi Genre Rubric

Version: 1.2
Last Updated: 2026-02-16
Purpose: Fast Lo-fi 장르 적합성 평가 루브릭
Scope: 장르가 Fast Lo-fi인 트랙의 Seed Design / Variation Design QA
Pass Criteria: 80점 이상
Fail Criteria: 80점 미만 (재디자인 필수)

---

## 핵심 철학

> **Fast Lo-fi는 느슨한 배경음이 아니라, 저역 드라이브가 있는 몰입형 그루브다.**
>
> lo-fi 질감은 배경으로 남고, 추진력은 드럼과 베이스가 책임진다.

---

## Evidence Basis (v1.2 추가)

이 루브릭은 내부 Track 01 캘리브레이션만이 아니라 아래 외부 근거를 함께 사용한다.

1. Lo-fi 기본 성향:
   - lo-fi hip hop은 일반적으로 60-90 BPM의 느린 템포, 재즈 성향 코드, 질감 중심 미니멀 편성으로 설명됨.
2. Fast 축 근거:
   - house 계열의 대표 템포는 대체로 115-130 BPM.
3. 운동 몰입 근거:
   - 운동 음악 연구/가이드에서 중간-빠른 템포(예: 120-140 BPM, 또는 120-130/150-160 비교)가 동기/몰입/퍼포먼스에 유의미한 영향을 보인다는 보고가 다수 존재.

따라서 AM_0600의 Fast Lo-fi는
`lo-fi texture(질감)` + `house-range drive(115-130)` + `workout-useful tempo zone(120-140 참조)`를 결합한 프로젝트 하이브리드로 정의한다.

운영 범위 110-130은 다음 이유로 유지한다:
- 하한 110: 워밍업/안정 구간 확보
- 중심 122-128: 추진력과 lo-fi 질감의 균형점
- 상한 130: 과도한 EDM화 방지

---

## 트랙1 캘리브레이션 기준 (PASS Baseline)

> 기준 트랙: `SERIES/AM_0600/track01_*` (Concrete Morning, PASS)

**베이스라인 관찰 포인트:**
- Style 첫 토큰이 `Articulation`으로 시작
- BPM 124 (권장 중심 122-128 충족)
- 저역 중심 키워드 명시 (`deep sub bass`, `mid-bass groove`)
- 구조 확장 명시 (`intro/interlude/bridge/instrumental/outro`)
- 목표 길이 명시 (`target runtime over 3 minutes`)
- Exclude 8개 이내 + 하모니/팔세토 금지군 포함

이 기준은 외부 근거 위에서 동작하는 프로젝트 내부 1차 PASS 레퍼런스로 사용한다.

---

## Phase 0 Hard Gates (선행 통과 조건)

아래 항목 중 하나라도 FAIL이면 점수 계산 전에 재작성한다.

1. Style Prompt 첫 단어가 `Articulation`으로 시작
2. BPM이 110-130 범위에 명시
3. Exclude가 1-8개이고 하모니 가드 항목 2개 이상 포함
4. 가사 구조 태그와 `()` 메타 태그를 영어로 작성
5. 목표 길이 3분 이상을 구조 또는 스타일에서 명시

---

## 루브릭 (6개 팩터, 100점)

### 1. Tempo & Drive (BPM/추진력) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | BPM 122-128 중심, 에너지 곡선 안정, 러닝/워크아웃 몰입 유지 |
| 14-17 | BPM 110-130 범위 준수, 일부 구간 추진력 약화 |
| 10-13 | BPM 범위는 맞으나 템포 체감이 느슨함 |
| 5-9 | BPM 불안정 또는 체감 추진력 부족 |
| 0-4 | Fast Lo-fi로 보기 어려운 템포/에너지 |

**핵심 원칙**:
- 운영 BPM 범위: **110-130**
- 기본 권장 중심: **122-128**

---

### 2. Drum Impact (킥/스네어 임팩트) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | 킥 타격감 선명, 스네어 어택 명확, 하이햇으로 속도감 유지 |
| 14-17 | 킥/스네어 존재감 양호, 일부 구간 어택 약함 |
| 10-13 | 드럼은 있으나 밀도/임팩트 부족 |
| 5-9 | 드럼 존재감이 약해 트랙 중심이 흐려짐 |
| 0-4 | 드럼 드라이브 부재 |

**핵심 원칙**:
- punchy kick + tight snare + fast hats
- "크게"보다 "단단하게"

---

### 3. Low-end Clarity (서브/미드베이스 선명도) — 20점

| 점수 | 기준 |
|------|------|
| 18-20 | sub + mid bass 이중 구조, 저역 충돌 최소, 번짐 없음 |
| 14-17 | 저역 중심은 좋으나 일부 구간 탁함 |
| 10-13 | 베이스 존재하나 윤곽 불명확 |
| 5-9 | 킥/베이스 충돌 빈번, muddiness 발생 |
| 0-4 | 저역이 흐리거나 붕뜸 |

**핵심 원칙**:
- sub layer(무게) + mid-bass layer(그루브) 분리
- muddy low-end는 즉시 감점

---

### 4. Lo-fi Texture Balance (질감 밸런스) — 15점

| 점수 | 기준 |
|------|------|
| 14-15 | lo-fi 노이즈/빈티지 질감이 배경에 머물며 본체를 방해하지 않음 |
| 11-13 | 질감은 좋으나 특정 구간에서 과함 |
| 7-10 | 질감 존재는 있으나 음악 본체와 분리 안 됨 |
| 0-6 | 질감이 주연이 되어 드럼/베이스를 가림 |

**핵심 원칙**:
- lo-fi는 분위기 레이어, 메인 엔진은 드럼/베이스

---

### 5. Structural Runtime Control (길이/구조 제어) — 15점

| 점수 | 기준 |
|------|------|
| 14-15 | 섹션 전개가 자연스럽고 목표 재생시간(최소 3분) 안정 달성 |
| 11-13 | 길이는 달성했으나 전개 밀도가 다소 단조 |
| 7-10 | 구조 전개 부족, 반복감 높음 |
| 0-6 | 목표 길이 미달 또는 섹션 설계 부재 |

**핵심 원칙**:
- 최소 길이: **3분 이상**
- 권장 섹션: `intro / verse / pre-chorus / chorus / interlude / bridge / instrumental / outro`
- lyrical track일 경우 `verse`는 **최소 3개** 권장

---

### 6. Genre Boundary Guard (장르 경계 보호) — 10점

| 점수 | 기준 |
|------|------|
| 9-10 | Fast Lo-fi 정체성 명확, 과장르 요소 억제 |
| 7-8 | 대체로 명확하나 일부 경계 혼합 |
| 4-6 | Hip-hop/EDM/Rock 경계가 애매 |
| 0-3 | 장르 정체성 붕괴 |

**핵심 원칙**:
- 금지 경향: EDM supersaw, trance arp, festival riser, rock live drum dominance
- 허용: 힙합 질감 참고는 가능하나 flow/rhyme 강제 트랙으로 변질 금지

---

## 체크리스트 (간이 판정)

```
□ BPM 110-130, 중심 122-128로 유지된다
□ 킥/스네어/하이햇이 추진력을 만든다
□ 저역(sub+mid bass)이 선명하고 탁하지 않다
□ lo-fi 질감이 메인 그루브를 가리지 않는다
□ 최소 3분 이상 구조 전개를 확보했다
□ Fast Lo-fi라고 즉시 설명 가능하다
```

---

## QA 워크플로우

```
Step 1. Seed/Variation 디자인 완료 (가사 + Style + Exclude)
Step 2. 기존 QC 통과 확인 (가사 체크리스트 + S0-S20 + 글자수)
Step 3. Phase 0 Hard Gates 통과 확인
Step 4. 장르가 Fast Lo-fi인 경우 → Fast Lo-fi Rubric 실행
Step 5. 6개 팩터별 채점 + 총점 산출
Step 6. 판정:
        ≥ 80점 → PASS (제안 가능)
        < 80점 → FAIL (재디자인 필수, 유저에게 제안 금지)
        개별 팩터 5점 이하 → 해당 팩터 CRITICAL FAIL (총점 무관 재디자인)
Step 7. PASS 시 채점표와 함께 output
```

**CRITICAL FAIL 규칙**: 총점이 80 이상이어도 개별 팩터 5점 이하가 하나라도 있으면 FAIL.

---

## 트랙1 1차 샘플 채점 (Reference)

| Factor | Score |
|------|------:|
| 1. Tempo & Drive | 18/20 |
| 2. Drum Impact | 17/20 |
| 3. Low-end Clarity | 17/20 |
| 4. Lo-fi Texture Balance | 13/15 |
| 5. Structural Runtime Control | 14/15 |
| 6. Genre Boundary Guard | 8/10 |
| **Total** | **87/100 (PASS)** |

---

## QC 출력 템플릿 (권장)

```md
Fast Lo-fi Rubric Score
- Track: AM_0600 / 01
- Hard Gates: PASS/FAIL

| Factor | Score | Notes |
|------|------:|------|
| Tempo & Drive |  |  |
| Drum Impact |  |  |
| Low-end Clarity |  |  |
| Lo-fi Texture Balance |  |  |
| Structural Runtime Control |  |  |
| Genre Boundary Guard |  |  |
| Total |  |  |

Verdict: PASS / FAIL
```

---

## Changelog

- 2026-02-16: v1.0 초안 작성
- 2026-02-16: v1.1 트랙1 PASS 캘리브레이션 반영 (Hard Gates + 샘플 채점 + QC 템플릿)
- 2026-02-16: v1.2 웹 리서치 근거 반영 (lo-fi/house/workout tempo evidence basis 추가)

---

## References (Web Research, v1.2)

- Native Instruments Blog, "Making lo-fi hip hop beats: the essential guide for beginners" (lo-fi 템포/질감 설명)
  - https://blog.native-instruments.com/lo-fi-hip-hop/
- Native Instruments Blog, "Understanding genre through instruments" (lo-fi 정의/질감)
  - https://blog.native-instruments.com/understanding-genre/
- Wikipedia, "Lofi hip-hop" (특성/다운템포 성향 개요)
  - https://en.wikipedia.org/wiki/Lofi_hip-hop
- Wikipedia, "House music" (대표 템포 115-130 및 4/4 드럼 특성)
  - https://en.wikipedia.org/wiki/House_music
- ACSM, "Music Tempo Guidelines for Exercise" (운동 템포 가이드 출처)
  - https://acsm.org/bmp-music-tempo-guidelines-exercise/
- Current Issues in Sport Science (2019), "Effects of synchronous, auditory stimuli on running performance and heart rate" (동기화/퍼포먼스 향상)
  - https://doi.org/10.15203/CISS_2019.005
- Journal of Science and Medicine in Sport (2012), "Effects of synchronous music on treadmill running among elite triathletes" (음악 동기화와 시간-소진 개선)
  - https://doi.org/10.1016/j.jsams.2011.06.003
