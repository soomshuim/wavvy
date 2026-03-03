# Wavvy MANAGER.md

Version: 2.0
Last Updated: 2026-03-03
Role: Quality Gatekeeper (최상위 통제)

---

## 1. Core Principles

1. **Quality > Quantity** - 시드 기반 변주만, 무작위 양산 금지
2. **Safety First** - -14 LUFS / -1.0 dBTP 절대 준수
3. **Pure Input** - LYRICS.md §2 준수 (가사 + 구조 태그 + `()` 메타만)
4. **Document-Driven** - 추측 금지, .md 기준으로 판단
5. **Ruthless Critique** - 애매하면 Fail

---

## 2. Document Hierarchy

```
MANAGER.md (최상위)
├── STYLE.md
├── LYRICS.md
├── ROLES.md
└── CLAUDE.md (요약/실행용, SSOT 아님)
```

**충돌 시:** MANAGER.md 우선, 명시 없으면 보수적 Fail

---

## 3. Workflow Phases

### Phase 0.3 New Genre Research
> 트리거: `rubrics/`에 해당 장르 없을 때
> SSOT: `RUBRICS_CREATION_PROCESS.md`

### Phase 0.4 New Series Bootstrap
1. `SERIES/[시리즈]/concept.md` 먼저 생성
2. 시리즈 운영 기준 고정
3. 트랙 산출물 작업

### Phase 0.5 Track Source-of-Truth
1. `trackNN_*.txt` 먼저 수정
2. 사용자 PASS 후에만 `concept.md` 반영
3. txt와 concept 동시 수정 금지

### Phase 1 Seed & Prompt Review
- Target Reference 3곡
- Style Prompt 8-10 토큰
- Exclude 3그룹 이내
- Musicality Matrix 적용

### Phase 1.5 Controlled Variation
- Core/Variable/Gate 정의 확인
- Genre Mix ≤ 2 (Spine + Color)
- Gate 기준 명시 (≥80점)
- 장르 3개+ 스택 → 즉시 FAIL

### Phase 2 Track QC (3-Point Fail Fast)

| 체크 | 기준 | 판정 |
|------|------|------|
| Intro 0:00~0:20 | 발음 뭉개짐 | Fail |
| Chorus | 훅 10초 내 안 잡힘 | Hold |
| Chorus | 합창/EDM 보컬 | **Fail** |
| Outro | 끊김/클릭 | Fail |
| 오디오 | -14 LUFS 미충족 | Fail |

**코러스 Fail:** Backing vocals, Choir, EDM processing, Stacked harmonies

### Phase 2.5 A/B Testing

| 상황 | 모드 | 규칙 |
|------|------|------|
| 정상 제작 | PROD | 2개+ 슬롯 변주 |
| 2회 재발 | DEBUG | **1개 변수만** |

**DEBUG:** 문제 기록 → A/B 비교 → 원인 특정 → PROD 복귀
