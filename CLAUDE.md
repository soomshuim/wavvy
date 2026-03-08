# Claude Code — Wavvy Execution Engine

Version: 4.0
Last Updated: 2026-03-03
Purpose: AI 실행 설정 (How)

> **프로젝트 정체성**: `wavvy.md` 참조

---

## Hard Constraints

1. **NO Pydub** — Pure FFmpeg만
2. **Sequential Acrossfade** — 단순 concat 금지
3. **Fail Fast** — 입력 검증 실패 시 즉시 종료
4. **Pure Input** — Suno 가사란에 가사 + 구조태그 + `()` 메타만
5. **크로스페이드 구분** — acrossfade(오디오) vs xfade(비디오)
6. **Video Crossfade 필수** — `vfade --test` → PASS → `vfade` → `pack`
7. **Pre-flight 체크** — `pack` 실행 시 loop_xfade.mp4 없으면 확인 요청
8. **복잡한 작업 확인 필수** — 아래 "복잡한 작업 규칙" 참조
9. **사용자 확인 필수** — 코드 수정/실행 전 반드시 확인. 테스트 없이 본 실행 금지. 임의 진행 금지.

---

## 복잡한 작업 규칙 (2026-03-07 회고 반영)

**복잡한 작업 정의:**
- 10개 이상 파일 처리
- 10분 이상 미디어
- 새로운 FFmpeg 필터 사용
- 이전에 실패한 유형

**복잡한 작업 시:**
1. "복잡한 작업입니다. 접근 방식 확인드릴게요." 선언
2. 사용자 승인 후 진행
3. Start Simple: 최소 단위 성공 → 확장

**미디어 체크리스트:**
- [ ] xfade(비디오) vs acrossfade(오디오) 구분
- [ ] 예상 output duration 계산
- [ ] filter_complex 100개 제한 인지
- [ ] 테스트: 작은 파일로 먼저 검증

---

## Auto Reference

| 요청 | 참조 |
|------|------|
| 가사 작성 | `MASTER/lyrics/LYRICS.md` |
| Style Prompt | `MASTER/style/STYLE.md` |
| QC/운영 | `MASTER/MANAGER.md` |
| 역할 분리 | `MASTER/roles/ROLES.md` |
| YouTube 메타 | `MASTER/youtube/YOUTUBE.md` |
| 장르 룩업 | `MASTER/reference/GENRES.md` |
| 장르 루브릭 | `MASTER/rubrics/[GENRE]_RUBRIC.md` |
| CLI 스펙 | `MASTER/cli/SPEC.md` |
| 워크플로우 | `MASTER/WORKFLOWS.md` |
| FFmpeg 버그 | `.ai/lessons-learned.md` |

---

## Workflow Rules

> **상세**: `MASTER/WORKFLOWS.md`

| 워크플로우 | 섹션 |
|-----------|------|
| 가사 생성 | §1 |
| Style Prompt | §2 |
| 가사/스타일 수정 | §3 |
| Concept QC | §4 |
| Shorts 생성 | §5 |
| 영상 패키징 | §6 |
| YouTube 메타 | §7 |

---

## Project Gotchas

- **Concept 위치**: `SERIES/[시리즈]/concept.md`
- **DEBUG 모드**: 2회 재발 시 1개 변수만 변경
- **Suno 기본값**: Weirdness 35, Style Influence 65
- **곡 길이 확장**: 가사 아닌 구조 태그 ([interlude])

---

## Quick CLI

```bash
python3 wavvy.py validate <path>
python3 wavvy.py preview <path>
python3 wavvy.py vfade <path> --test      # 비디오 xfade 테스트
python3 wavvy.py vfade <path>              # 비디오 xfade 본 생성
python3 wavvy.py pack <path> --use-xfade   # 패키징 (권장)
python3 wavvy.py shorts <track>
python3 wavvy.py clean <path>
```

> **CLI 상세**: `MASTER/cli/SPEC.md`
