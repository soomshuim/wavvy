# Rubrics Creation Process

Version: 1.1
Last Updated: 2026-02-21
Purpose: 새 장르 루브릭 생성 표준 프로세스
Origin: AM_1000 Chillhop 시리즈 작업 중 검증된 패턴

---

## 핵심 철학

> **"Research-First, Rubric-Second"**
>
> 가정 기반 루브릭은 나중에 수정이 필요하다.
> 웹 리서치 + 팀 협의로 Evidence를 확보한 후 루브릭을 작성한다.

---

## 트리거

- 새 시리즈 기획 시 기존 `rubrics/` 폴더에 해당 장르 루브릭이 없을 때
- 기존 루브릭이 있어도 장르 정의가 불명확할 때

---

## Phase 1: Genre Definition & Evidence Gathering

### 1.1 웹 리서치 (필수)

**최소 요구사항:**
- 3개 이상의 신뢰할 수 있는 소스
- BPM 범위, 악기, 특성 정보 수집
- Reference URLs 기록

**검색 쿼리 예시:**
```
"[장르명] music genre characteristics BPM tempo instruments"
"[장르명] vs [유사장르] differences"
"[장르명] definition history"
```

### 1.2 비교표 작성 (필수)

유사 장르와 차이점을 명시:

```markdown
| 항목 | [유사장르] | [대상장르] |
|------|-----------|-----------|
| BPM | - | - |
| 음질 | - | - |
| 악기 | - | - |
| 분위기 | - | - |
| 질감 | - | - |
```

### 1.3 핵심 특성 정리

- 필수 요소 (없으면 해당 장르 아님)
- 권장 요소 (있으면 더 좋음)
- 금지 요소 (있으면 다른 장르로 분류)

---

## Phase 2: Team Consultation (선택)

> 복잡한 장르이거나, 기존 시리즈와 겹침 우려가 있을 때 실행

### 2.1 Lenny's Team 협의

**회의 패턴:** Problem Solving
**추천 참석자:**
- Product Leader (품질 기준)
- Design Director (감각적 판단)
- Marketing Director (포지셔닝)

### 2.2 협의 내용

- 리서치 결과 검토
- 기존 루브릭과 차별점 확인
- 팩터별 배점 논의
- 합의점/충돌점 정리

---

## Phase 3: Rubric Design

### 3.1 Evidence Basis 섹션 (필수)

모든 루브릭은 반드시 Evidence Basis 섹션으로 시작:

```markdown
## Evidence Basis

이 루브릭은 아래 근거를 기반으로 한다.

### 1. [장르명] vs [유사장르] 차이점

| 항목 | [유사장르] | [장르명] |
|------|-----------|----------|
| BPM | - | - |
| 음질 | - | - |
| ... | - | - |

### 2. [장르명] 핵심 특성

- [특성 1]
- [특성 2]
- ...

### References

- [소스 1 제목](URL)
- [소스 2 제목](URL)
- [소스 3 제목](URL)
```

### 3.2 Phase 0 Hard Gates (필수)

점수 계산 전 통과해야 하는 선행 조건:

```markdown
## Phase 0 Hard Gates

1. [필수 조건 1]
2. [필수 조건 2]
3. [필수 조건 3]
4. Exclude가 1-8개이고 하모니 가드 항목 2개 이상 포함
5. 목표 길이 3분 이상 명시
```

**최소 5개 Hard Gate 필수**

### 3.3 6-Factor Rubric (100점)

표준 구조:

| Factor | 배점 | 역할 |
|--------|------|------|
| Factor 1 | 15-20 | 장르 핵심 요소 |
| Factor 2 | 15-20 | 그루브/분위기 |
| Factor 3 | 15 | 음질/질감 |
| Factor 4 | 15-20 | 보컬 처리 |
| Factor 5 | 15 | 구조 흐름 |
| Factor 6 | 10 | 장르 경계 보호 |
| **Total** | **100** | |

**각 팩터 채점 기준:**
```markdown
| 점수 | 기준 |
|------|------|
| 18-20 | 완벽 |
| 14-17 | 양호 |
| 10-13 | 보통 |
| 5-9 | 부족 |
| 0-4 | 실패 |
```

**Critical Fail 규칙:** 개별 팩터 5점 이하 → 총점 무관 재디자인

### 3.4 Calibration Track (필수)

> **Skip 조건**: 첫 트랙 미생성 시 건너뛰기 허용 → 트랙 생성 후 반드시 보완

첫 번째 트랙을 캘리브레이션 기준으로 사용:

```markdown
## Track1 Calibration Baseline

> 기준 트랙: `SERIES/[시리즈]/track01_*`

**베이스라인 관찰 포인트:**
- [관찰 1]
- [관찰 2]
- ...

**샘플 채점:**
| Factor | Score |
|--------|------:|
| Factor 1 | /20 |
| ... | ... |
| Total | /100 (PASS) |
```

---

## Phase 4: SSOT Integration

### 4.1 파일 저장

```
MASTER/rubrics/[GENRE]_RUBRIC.md
```

### 4.2 _INDEX.md 업데이트

SSOT 책임 매트릭스에 행 추가:

```markdown
| [장르명] 트랙 QA | rubrics/[GENRE]_RUBRIC.md |
```

### 4.3 MANAGER.md 참조 추가 (필요시)

Phase 0.4에서 참조 언급

### 4.4 CLAUDE.md Auto Reference 추가

```markdown
| **[장르명] 트랙 QA** | `MASTER/rubrics/[GENRE]_RUBRIC.md` | 전체 (필수) |
```

**장르 게이트 워크플로우에 추가:**
```markdown
IF genre = [장르명] → rubrics/[GENRE]_RUBRIC.md 실행
→ 총점 ≥ 80 AND 개별 팩터 > 5 → PASS
→ 미달 시 재디자인 (유저 제안 금지)
```

---

## Checklist (최종 검증)

```
□ 웹 리서치 3개+ 소스 완료
□ 비교표 작성 (유사 장르 대비)
□ Evidence Basis 섹션 포함
□ Hard Gates 5개+ 정의
□ 6-Factor 100점 구조
□ Critical Fail 규칙 명시
□ References URL 포함
□ rubrics/ 폴더에 저장
□ _INDEX.md 업데이트
□ CLAUDE.md Auto Reference 추가
```

---

## QC 출력 템플릿

```md
[장르명] Rubric Score
- Track: [시리즈] / [번호]
- Hard Gates: PASS/FAIL

| Factor | Score | Notes |
|------|------:|------|
| [Factor 1] |  |  |
| [Factor 2] |  |  |
| [Factor 3] |  |  |
| [Factor 4] |  |  |
| [Factor 5] |  |  |
| [Factor 6] |  |  |
| Total |  |  |

Verdict: PASS / FAIL
```

---

## Examples

### 성공 사례: CHILLHOP_RUBRIC.md (v1.1)

1. **Phase 1**: 웹 리서치로 Lo-fi vs Chillhop 차이 명확화
   - BPM: 60-90 → 80-110
   - 음질: dusty → crisp
2. **Phase 2**: Lenny's Team 협의 (Product, Design, Marketing)
3. **Phase 3**: Evidence Basis + 6-Factor + Hard Gates 작성
4. **Phase 4**: SSOT 통합 완료

### 개선 필요 사례: CITYPOP_RUBRIC.md (v1.0)

- Evidence Basis 섹션 없음
- 향후 웹 리서치 + References 추가 권장

---

## Changelog

- 2026-02-21: v1.1 Calibration Track 필수화 (Team 리뷰 반영)
- 2026-02-21: v1.0 초안 작성 (AM_1000 Chillhop 작업 기반)
