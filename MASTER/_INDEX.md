# MASTER/_INDEX.md — SSOT Router

Version: 1.4
Last Updated: 2026-02-16
Purpose: 모든 규칙의 정의와 우선순위를 한 페이지로 정리하는 SSOT 라우터

---

## 1. Document Hierarchy (우선순위)

```
MANAGER.md (최상위 통제)
├── STYLE.md (Style Prompt 규격)
├── LYRICS.md (가사 입력 규격)
├── ROLES.md (역할 분리/검증표)
├── 24H_UNIVERSE.md (세계관/Time Station)
└── PLAYLIST_GUIDE.md (플레이리스트 컨셉)

CLAUDE.md = 사용 매뉴얼 (SSOT 아님, 요약만)
```

---

## 2. SSOT Responsibility Matrix

| 규칙 영역 | SSOT 문서 | 섹션 | 다른 문서는 |
|----------|----------|------|-----------|
| **QC 최종판정** | `MANAGER.md` | §1-3 | 참조만 |
| **Pure Input 정의** | `LYRICS.md` | §2 | 참조만 |
| **가사 구조/태그** | `LYRICS.md` | §2.2 | 참조만 |
| **보컬 메타태그 필수** | `LYRICS.md` | §2.2 | 참조만 |
| **Style Prompt 슬롯** | `STYLE.md` | §7-8 | 참조만 |
| **글자수 제한 (900자, 공백 포함 문자)** | `STYLE.md` | §0.1 | 참조만 |
| **Exclude 규칙** | `STYLE.md` | §6 | 참조만 |
| **역할 분리** | `ROLES.md` | 전체 | 참조만 |
| **S1-S12 압축 검증** | `ROLES.md` | 검증표 | STYLE.md S0-S20의 요약 |
| **Time Station** | `24H_UNIVERSE.md` | §2-4 | 참조만 |
| **타이틀 생성** | `PLAYLIST_GUIDE.md` | §0 | 참조만 |
| **작업 절차/운영 게이트** | `MANAGER.md` | §2-3 | `CLAUDE.md`는 요약/매뉴얼 |
| **txt→컨펌→concept 반영 절차** | `MANAGER.md` | §3 Phase 0.5 | `CLAUDE.md`는 요약/참조 |

---

## 3. SSOT Parameters (핵심 변수)

> **충돌 방지를 위한 단일 정의**

| 파라미터 | 값 | SSOT 위치 |
|----------|-----|----------|
| `PROMPT_CHAR_LIMIT` | 900 (공백 포함 문자) | STYLE.md §0.1 |
| `LYRICS_ALLOWED_TAGS` | v1.9.1 | LYRICS.md §2.2 |
| `VOCAL_META_TAG_REQUIRED` | true | LYRICS.md §2.2 |
| `EXCLUDE_MAX_TOKENS` | 8 | STYLE.md §6 |
| `SLOT_COUNT` | S0-S20 (21개) | STYLE.md §7-8 |

---

## 4. Cross-Reference Rules

### 4.1 중복 서술 금지

- **원칙:** 규칙 본문은 SSOT 문서에만 존재
- **다른 문서:** 참조 링크 + 요약만 허용
- **예시:** CLAUDE.md의 체크리스트는 "(요약)" 표시 필수

### 4.2 충돌 해결

```
충돌 발생 시: SSOT 문서가 항상 우선
→ 다른 문서는 SSOT에 맞춰 수정
→ CHANGELOG에 "SSOT alignment" 기록
```

### 4.3 버전 동기화

- SSOT 문서 변경 시 → 참조 문서도 확인
- CLAUDE.md 체크리스트 → MASTER 변경 시 자동 드리프트 위험

---

## 5. Document Quick Reference

| 문서 | 역할 | 현재 버전 |
|------|------|----------|
| `MANAGER.md` | 운영/QC 최상위 통제 | v1.5 |
| `STYLE.md` | Style Prompt 규격 | v2.8 |
| `LYRICS.md` | 가사 입력 규격 | v2.2.0 |
| `ROLES.md` | 역할 분리/검증표 | v1.9 |
| `24H_UNIVERSE.md` | 세계관 Bible | v1.0 |
| `PLAYLIST_GUIDE.md` | 플레이리스트 컨셉 | v1.3 |
| `QUICK_REF.md` | 사람용 매뉴얼 | - |
| `VIBE-M_Master_Plan.md` | CLI 스펙 | - |
| `docs/planning/PRD_GPT_LOOP_SIDECAR.md` | GPT 사이드카 제품 요구사항 (비-SSOT) | v0.1 |
| `docs/planning/IMPLEMENTATION_SPEC_GPT_LOOP_SIDECAR.md` | GPT 사이드카 구현 명세 (비-SSOT) | v0.1 |

---

## 6. When to Update This File

- [ ] 새 SSOT 규칙 추가 시
- [ ] 문서 책임 범위 변경 시
- [ ] 핵심 파라미터 값 변경 시
- [ ] 문서 우선순위 변경 시

---

> **이 파일을 먼저 확인하면 "어느 문서를 봐야 하는지" 즉시 알 수 있습니다.**
