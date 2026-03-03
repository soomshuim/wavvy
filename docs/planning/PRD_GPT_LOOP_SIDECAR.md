# PRD - GPT Loop Sidecar for Wavvy
Version: 0.1 (Draft)
Last Updated: 2026-02-16
Owner: Wavvy
Status: Draft (Planning Approved)

---

## 1) Problem

Wavvy의 기존 워크플로우는 문서 규약과 사람 검토 품질이 높지만, 가사/Style/Exclude 초안 작성과 반복 검증에 수동 비용이 크다.  
기존 SSOT와 승인 절차는 유지한 채, 초안 생성과 검증/개선 루프만 옵션형으로 자동화할 필요가 있다.

---

## 2) Goals

- 기존 구조를 변경하지 않고 GPT API 기반 검증/개선 루프를 추가한다.
- `track*_lyrics/style/exclude` 산출물을 기존 1단계 입력물 형태로 생성한다.
- 하드룰 위반률과 PASS까지의 반복 횟수를 줄인다.

### Non-Goals

- `MASTER` 규칙 문서(SSOT) 재정의/수정
- `concept.md` 자동 반영
- 기존 `vibem.py` 핵심 미디어 파이프라인 변경

---

## 3) Invariants (Must Keep)

- SSOT 우선순위는 기존 문서 체계 준수:
  - `MASTER/MANAGER.md`
  - `MASTER/ROLES.md`
  - `MASTER/LYRICS.md`
  - `MASTER/STYLE.md`
- 반영 절차 고정:
  1. txt 산출물 생성/수정
  2. 사용자 PASS
  3. `SERIES/[시리즈]/concept.md` 반영
- `llm-loop`는 제안 생성기이며 최종 승인권은 사람에게 있다.

---

## 4) User Stories

- 작업자는 시리즈/트랙을 지정해 가사/Style/Exclude 제안본을 빠르게 얻고 싶다.
- 작업자는 자동 QC 리포트로 하드룰 위반을 즉시 확인하고 싶다.
- 작업자는 소프트룰(K1-K3, 패턴 고착)은 보조 진단만 받고 최종 판단은 직접 하고 싶다.

---

## 5) Solution Overview (Sidecar)

새로운 옵션형 CLI `llm-loop`를 별도 추가한다.

- 실행: 수동 명령형 (`python tools/llm_loop.py ...`)
- 입력: 시리즈/트랙 컨텍스트 + 관련 SSOT 규칙 요약
- 처리: `generate -> validate -> revise` 최대 N회
- 출력:
  - `trackNN_lyrics_vX_llm.txt`
  - `trackNN_style_vX_llm.txt`
  - `trackNN_exclude_vX_llm.txt`
  - `trackNN_qc_vX_llm.md`

`concept.md`는 읽기 전용 유지.

---

## 6) File/Version Policy

- 위치: `SERIES/[SERIES_NAME]/`
- 네이밍:
  - `trackNN_lyrics_vX_llm.txt`
  - `trackNN_style_vX_llm.txt`
  - `trackNN_exclude_vX_llm.txt`
  - `trackNN_qc_vX_llm.md`
- 충돌 정책:
  - 절대 덮어쓰기 금지
  - 동일 타입 기존 최대 버전 탐색 후 `v(X+1)` 생성

---

## 7) Rule Engine Strategy

## 7.1 Hard Rules (Machine-check first)

- 글자수 제한 (Style Prompt `<= 900자`, 공백 포함 문자)
- 필수 포함 키워드/구조 태그 존재 여부
- 금지 패턴 포함 여부 (Exclude/금지 보컬 레이어 관련)
- 형식 규칙 위반 (구조 태그, 출력 포맷)

Hard fail 발생 시 자동 revise 대상으로 등록한다.

## 7.2 Soft Rules (Model-assisted + Human final)

- Korean Positioning (K1-K3)
- Cross-Series 서사 유사도 리스크
- 패턴 고착/새로움 부족
- 감정 아크 일관성

Soft rule은 점수와 근거를 제공하고, 최종 PASS는 사람 판단으로 유지한다.

---

## 8) Cross-Series Check

- 기본 모드(`--cross-series=lite`):
  - 키워드/제목/훅 중복 저비용 검사
- 확장 모드(`--cross-series=embed`):
  - 임베딩 기반 유사도 검사(옵션)
  - 인덱스 캐시 재사용으로 비용 절감

기본값은 `lite`.

---

## 9) CLI Draft

```bash
python tools/llm_loop.py run \
  --series PM_0900 \
  --track 07 \
  --provider openai \
  --model gpt-5 \
  --max-iterations 3 \
  --cross-series lite
```

### Options (Draft)

- `--series`: 대상 시리즈
- `--track`: 트랙 번호
- `--provider`: `openai` (초기), 추후 확장
- `--model`: 모델명
- `--max-iterations`: 루프 최대 횟수
- `--cross-series`: `lite|embed|off`
- `--dry-run`: 파일 저장 없이 리포트만

---

## 10) Reporting Format

`trackNN_qc_vX_llm.md`는 다음 섹션 고정:

1. Input Summary
2. Hard Rule Table (`PASS/HOLD/FAIL`)
3. Soft Rule Notes (점수 + 근거)
4. Revision Diff Summary
5. Final Verdict (`READY_FOR_REVIEW` or `NEEDS_REWRITE`)

---

## 11) Cost/ROI Guardrails

- 기본 루프: 최대 3회
- 토큰 절감:
  - 규칙 문서 전체가 아니라 필요한 조각만 주입
  - 리비전은 실패 항목만 부분 재작성
- 파일럿 KPI:
  - PASS까지 평균 반복 횟수
  - 수동 수정 라인 수
  - 트랙당 API 비용

---

## 12) Rollout Plan

1. Pilot: `PM_0900` 2트랙
2. 평가: KPI + 사용자 체감
3. 확장: 시리즈 단위 적용
4. 필요 시 `--provider anthropic` 호환 레이어 추가

---

## 13) Risks

- 규칙 해석 오차: 하드/소프트 경계 불명확 시 false fail 가능
- 비용 급증: 과도한 반복 루프
- 톤 일관성 저하: Seed 고정 요소 누락 시 발생

### Mitigation

- 하드룰 우선순위 명시, 소프트룰은 참고점수로 제한
- 반복 횟수 상한 + 실패 항목만 재작성
- Seed Core 고정 프롬프트 잠금

---

## 14) Acceptance Criteria

- 기존 워크플로우(`txt -> PASS -> concept`) 훼손 없이 동작
- `concept.md` 자동 수정 없음
- 버전 충돌 없이 `_llm` 산출물만 신규 생성
- 파일럿 2트랙에서 하드룰 자동검증 리포트 생성 성공

---

## 15) References

- `MASTER/MANAGER.md`
- `MASTER/ROLES.md`
- `MASTER/LYRICS.md`
- `MASTER/STYLE.md`
- `MASTER/QUICK_REF.md`
