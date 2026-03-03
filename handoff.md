# HANDOFF

## Header Rule (Required)
- Every handoff must start with this exact line:
  `HANDOFF: <FROM_AGENT> -> <TO_AGENT>`
- Example:
  `HANDOFF: Codex -> Claude`

HANDOFF: Codex -> Claude

Date: 2026-02-14
Scope: Document alignment for SSOT consistency and spec/code sync

## Updated Files
- `MASTER/_INDEX.md`
- `MASTER/STYLE.md`
- `MASTER/QUICK_REF.md`
- `MASTER/Wavvy_Master_Plan.md`

## What Changed
1. `MASTER/_INDEX.md`
- Updated router version/date to `v1.1`, `2026-02-14`.
- Synced document version table with current real versions:
  - MANAGER `v1.4`
  - STYLE `v2.7`
  - LYRICS `v2.2.0`
  - ROLES `v1.9`
  - PLAYLIST_GUIDE `v1.3`

2. `MASTER/STYLE.md`
- Removed wording that implied `CLAUDE.md` is SSOT for style slots.
- Clarified SSOT source as `STYLE.md §7-8`.
- Kept `CLAUDE.md` as summary/manual only.

3. `MASTER/QUICK_REF.md`
- Relaxed hard ban wording to avoid conflict with actual workflow:
  - from absolute "never write lyrics/styles"
  - to "do not output without explicit user request and role declaration"
- Unified conflict-resolution wording:
  - follow `MASTER/_INDEX.md` responsibility matrix first
  - final QC decision follows `MANAGER.md`

4. `MASTER/Wavvy_Master_Plan.md`
- Bumped spec version to `2.2 (Spec Alignment)`.
- Updated directory example to match current real usage (series folder without required date layer).
- Updated track format from MP3-only to `mp3|wav` to match `vibem.py`.
- Updated validate section accordingly (MP3/WAV).
- Fixed obsolete `vibem.md` reference to `MASTER/Wavvy_Master_Plan.md`.

## Notes
- No `AGENT.md`/`AGENTS.md` exists inside `wavvy`.
- `AGENTS.md` exists in another project: `Project/WDS/AGENTS.md`.
- No direct instruction-file conflict detected for `wavvy`.

---
HANDOFF: Codex -> Claude
Date: 2026-02-16 03:55:00
Project: ~/Project/wavvy
Agent: Codex
Summary: GPT Loop Sidecar 설계(PRD/구현명세)부터 M1~M3.5 구현(템플릿 퍼소나 강화, hard/soft 검증, revise 루프, OpenAI 호출, 버전/리포트 체계)까지 반영 완료. 기본 모델은 gpt-5.2로 설정.
Next-TODO: OPENAI_API_KEY 설정 환경에서 실제 시리즈 트랙 1~2개 파일럿 실행 후 hard rule 임계값 튜닝.
Commits: pending
