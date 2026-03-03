# Rubrics Creation Process

Version: 2.0
Last Updated: 2026-03-03
Purpose: 새 장르 루브릭 생성 표준

---

## 트리거

- `rubrics/`에 해당 장르 루브릭 없을 때
- 기존 루브릭이 불명확할 때

---

## Phase 1: Research

### 1.1 웹 리서치 (필수)
- 3개+ 신뢰 소스
- BPM, 악기, 특성 수집
- Reference URLs 기록

### 1.2 비교표 (필수)
```markdown
| 항목 | [유사장르] | [대상장르] |
|------|-----------|-----------|
| BPM | - | - |
| 음질 | - | - |
| 악기 | - | - |
```

### 1.3 핵심 특성
- 필수 요소 (없으면 해당 장르 아님)
- 권장 요소
- 금지 요소

---

## Phase 2: Team Consultation (선택)

복잡한 장르/겹침 우려 시:
- Lenny's Team 협의
- 기존 루브릭과 차별점 확인
- 팩터별 배점 논의

---

## Phase 3: Rubric Design

### 3.1 Evidence Basis (필수)
```markdown
## Evidence Basis
### 1. [장르] vs [유사장르] 차이점
| 항목 | [유사] | [대상] |
### 2. 핵심 특성
### References
- [URL 3개+]
```

### 3.2 Hard Gates (5개+)
```markdown
## Phase 0 Hard Gates
1. [필수 조건 1]
2. [필수 조건 2]
3. [필수 조건 3]
4. Exclude 1-8개 + 하모니 가드 2개+
5. 목표 길이 3분+
```

### 3.3 6-Factor Rubric (100점)

| Factor | 배점 | 역할 |
|--------|------|------|
| Factor 1 | 15-20 | 장르 핵심 |
| Factor 2 | 15-20 | 그루브/분위기 |
| Factor 3 | 15 | 음질/질감 |
| Factor 4 | 15-20 | 보컬 처리 |
| Factor 5 | 15 | 구조 흐름 |
| Factor 6 | 10 | 장르 경계 |

**채점:** 18-20 완벽, 14-17 양호, 10-13 보통, 5-9 부족, 0-4 실패
**Critical Fail:** 개별 5점 이하 → 총점 무관 재디자인

---

## Phase 4: SSOT Integration

1. `MASTER/rubrics/[GENRE]_RUBRIC.md` 저장
2. `_INDEX.md` 행 추가
3. `CLAUDE.md` Auto Reference 추가

---

## Checklist

```
□ 웹 리서치 3개+ 소스
□ 비교표 작성
□ Evidence Basis 포함
□ Hard Gates 5개+
□ 6-Factor 100점
□ Critical Fail 규칙
□ References URL
□ rubrics/ 저장
□ _INDEX.md 업데이트
```

---

## QC 템플릿

```md
[장르명] Rubric Score
- Track: [시리즈/번호]
- Hard Gates: PASS/FAIL

| Factor | Score | Notes |
|--------|------:|-------|
| F1 |  |  |
| F2 |  |  |
| F3 |  |  |
| F4 |  |  |
| F5 |  |  |
| F6 |  |  |
| Total |  |  |

Verdict: PASS / FAIL
```
