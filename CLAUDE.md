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
5. **크로스페이드 구분** — 오디오 vs 비디오 반드시 구분

---

## Auto Reference

| 요청 | 참조 |
|------|------|
| 가사 작성 | `MASTER/lyrics/LYRICS.md` |
| Style Prompt | `MASTER/style/STYLE.md` |
| QC/운영 | `MASTER/MANAGER.md` |
| 역할 분리 | `MASTER/roles/ROLES.md` |
| YouTube 제목 | `MASTER/youtube/TITLE_RULES.md` |
| YouTube 설명 | `MASTER/youtube/DESCRIPTION.md` |
| 장르 태그 | `MASTER/youtube/GENRE_TAGS.md` |
| 장르 루브릭 | `MASTER/rubrics/[GENRE]_RUBRIC.md` |
| CLI 스펙 | `MASTER/cli/SPEC.md` |
| 워크플로우 | `MASTER/WORKFLOWS.md` |
| FFmpeg 버그 | `.ai/lessons-learned.md` |
| Suno 가이드 | `Reference/museA_suno_guide.md` |

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
python3 vibem.py validate <path>
python3 vibem.py preview <path>
python3 vibem.py pack <path>
python3 vibem.py shorts <track>
python3 vibem.py clean <path>
```

> **CLI 상세**: `MASTER/cli/SPEC.md`
