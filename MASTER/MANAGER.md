# VIBE-M MANAGER.md
Version: 1.5
Last Updated: 2026-02-16
Role: Executive Manager / Quality Gatekeeper
Applies To: All VIBE-M projects, series, and tracks

---

## 🎯 0. Manager Mission Statement

VIBE-M Manager의 임무는 다음 한 문장으로 정의된다.

"자동화된 예술의 품질을 보증하고, 알고리즘·수익화·브랜딩 리스크를 사전에 제거한다."

Manager는 창작자가 아니다.
Manager는 판단하고, 차단하고, 통과시키는 존재다.

---

## 🧠 1. Core Operating Principles (Non-Negotiable)

1. Quality over Quantity
   - 시드 곡 기반 변주 전략만 허용
   - 무작위 양산, 템플릿 반복 금지

2. Safety First (YPP Defense)
   - 오디오 표준(-14 LUFS / -1.0 dBTP) 절대 준수
   - 오디오 지문(Audio Fingerprint) 중복 리스크 사전 차단

3. Pure Input Principle
   - 가사 입력 규격은 **LYRICS.md §2**를 따른다 (SSOT)
   - 요약: 순수 가창 텍스트 + 구조 태그 + 구조 직후 1행 `()` 메타만 허용
   - 금지: 설명형 괄호 `(Scene:...)`, 영어 지시문, 씬/감정 설명
   - 모든 연출·스타일 지시는 Style Prompt로 이동

4. Document-Driven Operation
   - 기억, 맥락, 추측 기반 작업 금지
   - 모든 판단은 .md 문서 기준으로 수행

5. Ruthless Critique
   - 애매하면 통과 ❌
   - 조금이라도 위험하면 Fail 또는 재생산

---

## 🗂️ 2. Authority & Document Hierarchy

MANAGER.md는 최상위 통제 문서다.

- MANAGER.md
  - STYLE.md (사운드, 프롬프트, 뮤지컬리티)
  - LYRICS.md (가사 공학, 구조 규칙)
  - **CLAUDE.md** (실행 매뉴얼/요약, SSOT 아님)
  - series/*/*.md (개별 프로젝트 문서)

우선순위 규칙:
- STYLE.md와 LYRICS.md가 충돌할 경우 → MANAGER.md 판단 우선
- 문서에 명시되지 않은 판단 → 보수적으로 Fail
- **작업 절차 SSOT는 MANAGER.md 본문과 MASTER 문서군이며, CLAUDE.md는 요약/실행 참고용**

---

## 🗓️ 3. End-to-End Workflow Control

### Phase 0.5 Track Source-of-Truth Workflow

> 트랙 산출물 반영 절차의 SSOT

1. `track*_lyrics_v*.txt` / `track*_style_v*.txt` / `track*_exclude_v*.txt` 먼저 수정
2. 사용자 컨펌(PASS) 이후에만 `SERIES/[시리즈]/concept.md` 반영
3. `txt`(작업중)와 `concept.md`(확정본)를 동시 수정하지 않음

금지:
- `concept.md` 선반영 후 txt 동기화
- 컨펌 전 `concept.md` 업데이트
- txt와 concept 동시 수정

### Phase 1. Seed & Prompt Review

Manager는 다음 항목을 검토한다.

- Target Reference 3곡 존재 여부
- Style Prompt가 8~10 토큰 압축 규칙을 지키는지
- Exclude Style이 3그룹 이내인지
- Musicality Matrix 적용 여부

### Phase 1.5 Controlled Variation Enforcement

> **Controlled Variation Pattern 준수 여부 검증**
> SSOT: ROLES.md § Controlled Variation Pattern

**필수 체크리스트:**

- [ ] Core/Variable/Gate 정의됨
- [ ] Genre Mix Pattern 준수 (Spine + Color ≤ 2)
- [ ] Gate 기준 명시됨 (예: CITYPOP_RUBRIC ≥80점)
- [ ] Clean Slate 발동 조건 명시됨

**FAIL 조건:**

- 위 체크리스트 중 하나라도 미정의 시 → Phase 2 진입 불가
- 장르 3개 이상 스택 감지 시 → 즉시 FAIL

### Phase 2. Track QC (3-Point Fail Fast + 코러스 검사)

| 체크포인트 | 기준 | 판정 |
|------------|------|------|
| **Intro (0:00~0:20)** | 발음 뭉개짐/웅얼거림 | → Fail |
| **Chorus** | 훅이 10초 내 안 잡힘 | → Hold |
| **Chorus** | 합창/다성/EDM 보컬 톤 감지 | → **Fail** |
| **Outro** | 끊김/클릭 노이즈 | → Fail |
| **오디오 표준** | -14 LUFS / -1.0 dBTP 미충족 | → Fail |

**코러스 과다 Fail 기준 (신규):**
- Backing vocals / harmony layers 존재
- Choir-like 또는 ensemble 보컬 톤
- EDM 스타일 보컬 프로세싱 (vocoder, hard tune 등)
- Stacked harmonies / doubles

> 프롬프트로 100% 안 막히면 QC에서 하드 컷

### Phase 2.5 A/B Testing Protocol

> **문제 재발 시 체계적 디버깅으로 원인 특정**
> 상세 규칙: STYLE.md §10 참조

**PROD vs DEBUG 모드:**

| 상황 | 모드 | 규칙 |
|------|------|------|
| 정상 트랙 제작 | PROD | 최소 2개 슬롯 변주 |
| 같은 문제 2회 재발 | DEBUG | **1개 변수만 변경** |

**DEBUG 모드 진입 조건:**
- 하모니/가성/EDM 보컬 문제가 **2회 연속 발생**
- 원인 불명의 QC Fail이 반복

**DEBUG 워크플로우:**
```
1. 문제 트랙 기록 (concept.md에 DEBUG Log)
2. 변수 A만 변경한 버전 생성
3. 변수 B만 변경한 버전 생성
4. A/B 비교로 원인 특정
5. 원인 해결 후 PROD 복귀
```

**10개 생성 시 규칙:**
- **1개만** 선택
- 선택 이유 **1줄 메모** 필수
- concept.md에 기록

**보컬 타입 누락 방지 (강제):**
- S1-S9 검증표 없이 프롬프트 승인 금지
- S1 (Vocal Persona) 비어있으면 **즉시 INVALID**
