# Implementation Spec - GPT Loop Sidecar
Version: 0.1 (Draft)
Last Updated: 2026-02-16
Owner: Wavvy
Status: Draft (PRD Approved)

---

## 1) Scope

본 문서는 `docs/planning/PRD_GPT_LOOP_SIDECAR.md`의 구현 명세를 정의한다.

- 파일별 책임
- CLI 인자 계약
- 프롬프트 템플릿 위치/역할
- I/O 스키마
- 실행/로그/오류 정책

비범위:
- SSOT 규칙 문서 수정
- `concept.md` 자동 반영
- `vibem.py` 미디어 파이프라인 변경

---

## 2) File Layout (Planned)

```text
wavvy/
├─ tools/
│  └─ llm_loop.py
├─ tools/llm_loop/
│  ├─ config.py
│  ├─ loader.py
│  ├─ rules_hard.py
│  ├─ rules_soft.py
│  ├─ renderer.py
│  ├─ versioning.py
│  ├─ cross_series.py
│  └─ reporter.py
├─ docs/planning/
│  ├─ PRD_GPT_LOOP_SIDECAR.md
│  └─ IMPLEMENTATION_SPEC_GPT_LOOP_SIDECAR.md
├─ MASTER/prompts/llm_loop/
│  ├─ generate_lyrics.md
│  ├─ generate_style.md
│  ├─ generate_exclude.md
│  ├─ validate_soft.md
│  └─ revise.md
└─ SERIES/[SERIES]/
   ├─ trackNN_lyrics_vX_llm.txt
   ├─ trackNN_style_vX_llm.txt
   ├─ trackNN_exclude_vX_llm.txt
   └─ trackNN_qc_vX_llm.md
```

---

## 3) File Responsibilities

### `tools/llm_loop.py`
- 단일 진입점 CLI
- 명령 파싱/실행 제어
- exit code 관리

### `tools/llm_loop/config.py`
- 기본값, 환경변수 로드
- 모델/반복 횟수/모드 정책 검증

### `tools/llm_loop/loader.py`
- 시리즈/트랙 컨텍스트 로드
- SSOT 문서에서 필요한 섹션만 추출

### `tools/llm_loop/rules_hard.py`
- 기계검증 규칙 구현
- FAIL/HOLD/PASS 판정 + 위반 목록 반환

### `tools/llm_loop/rules_soft.py`
- LLM 보조평가 실행
- K1-K3/패턴 고착/서사 유사도 점수화

### `tools/llm_loop/renderer.py`
- LLM 입력 컨텍스트 생성
- 템플릿 변수 치환

### `tools/llm_loop/versioning.py`
- `_llm` 파일 버전 탐색
- 다음 버전 번호 할당
- 덮어쓰기 방지

### `tools/llm_loop/cross_series.py`
- `lite`/`embed` 중복 리스크 검사
- 임베딩 캐시 관리(옵션)

### `tools/llm_loop/reporter.py`
- QC markdown 생성
- 루프 이력/판정 요약 출력

---

## 4) CLI Contract

## 4.1 Command

```bash
python tools/llm_loop.py run [OPTIONS]
```

## 4.2 Required Options

- `--series TEXT` : 대상 시리즈 (예: `PM_0900`)
- `--track INT` : 트랙 번호 (예: `7`)
- `--provider [openai]` : 초기 제공자

## 4.3 Optional Options

- `--model TEXT` (default: `gpt-5`)
- `--max-iterations INT` (default: `3`, range `1..5`)
- `--cross-series [off|lite|embed]` (default: `lite`)
- `--dry-run` (파일 저장 없이 QC만)
- `--temperature FLOAT` (default: `0.4`)
- `--seed TEXT` (재현성 보조값)
- `--output-dir PATH` (기본 `SERIES/[series]`)
- `--verbose`

## 4.4 Future Commands (Reserved)

- `generate` : 초안만 생성
- `validate` : 검증만 수행
- `revise` : 기존 초안 개선만 수행

---

## 5) Environment Variables

- `OPENAI_API_KEY` (required when `--provider openai`)
- `LLM_LOOP_DEFAULT_MODEL` (optional override)
- `LLM_LOOP_MAX_ITER` (optional override)

비밀값은 파일 저장 금지. 로그 출력 시 마스킹.

---

## 6) Prompt Template Location

- 경로: `MASTER/prompts/llm_loop/`
- 파일:
  - `generate_lyrics.md`
  - `generate_style.md`
  - `generate_exclude.md`
  - `validate_soft.md`
  - `revise.md`

템플릿 원칙:
- SSOT 규칙 본문 복붙 최소화, 필요한 조항만 주입
- 출력 스키마 강제(JSON block 또는 엄격한 섹션)
- revise는 실패 항목만 수정하도록 제한

---

## 7) Input Schema (Runtime)

```json
{
  "series": "PM_0900",
  "track": 7,
  "track_context": {
    "title": "공원",
    "bpm": 68,
    "key": "Db Major",
    "mood": ["관조", "온기"],
    "hook": "공원은 깨어 있어"
  },
  "seed_constraints": {
    "core": ["genre spine", "vocal persona"],
    "variable": ["lead instrument", "lyric angle"]
  },
  "rules": {
    "hard": ["char_limit", "required_tags", "forbidden_layers"],
    "soft": ["k1_k3", "novelty", "cross_series_overlap"]
  }
}
```

---

## 8) Output Schema

## 8.1 Text Artifacts

- `trackNN_lyrics_vX_llm.txt`
- `trackNN_style_vX_llm.txt`
- `trackNN_exclude_vX_llm.txt`

## 8.2 QC Artifact

- `trackNN_qc_vX_llm.md`
- 섹션:
  1. Run Metadata (model/provider/iterations/cost)
  2. Hard Rule Table
  3. Soft Rule Table
  4. Revision Summary
  5. Final Verdict

---

## 9) Versioning Rules

- suffix는 항상 `_llm`
- 덮어쓰기 금지
- 타입별 최대 `vN` 탐색 후 `vN+1` 생성
- 같은 run에서 3개 산출물의 버전 번호는 동일하게 맞춘다

예:
- 기존 `track07_lyrics_v2.txt` + `track07_lyrics_v3_llm.txt` 존재 시
- 다음 llm 출력은 `track07_lyrics_v4_llm.txt`

---

## 10) Rule Evaluation Pipeline

1. Generate (`lyrics/style/exclude`)
2. Hard Validate
3. Soft Validate
4. Revise (필요 시)
5. Re-validate
6. Report + Save

정지 조건:
- Hard rule all PASS and soft score threshold met
- 또는 `max-iterations` 도달

---

## 11) Exit Codes

- `0`: 성공 (`READY_FOR_REVIEW`)
- `1`: 입력/경로 오류
- `2`: API/네트워크 오류
- `3`: 검증 실패(`NEEDS_REWRITE`)
- `4`: 내부 예외

---

## 12) Logging Policy

- 콘솔: 핵심 진행 로그만 (`iteration`, `hard_fail_count`, `verdict`)
- 파일: QC 리포트에 상세 근거 기록
- 민감정보: API key, 프롬프트 원문 전체, 개인 식별정보 저장 금지

---

## 13) Implementation Milestones

1. M1: CLI 골격 + 버전 정책
2. M2: hard rule 엔진 + qc_report 출력
3. M3: GPT 생성/소프트검증/리비전 루프
4. M4: cross-series `lite`
5. M5: 파일럿(`PM_0900` 2트랙), KPI 측정

---

## 14) Definition of Done

- `run` 명령 1회로 `_llm` 4종 파일 생성 가능
- 기존 워크플로우(`txt -> PASS -> concept`)와 충돌 없음
- 덮어쓰기 없이 버전 증가
- 하드/소프트 판정이 QC 문서로 재현 가능

---

## 15) References

- `docs/planning/PRD_GPT_LOOP_SIDECAR.md`
- `MASTER/MANAGER.md`
- `MASTER/ROLES.md`
- `MASTER/LYRICS.md`
- `MASTER/STYLE.md`
