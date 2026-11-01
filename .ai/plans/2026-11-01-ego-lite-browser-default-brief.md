배정: 규모=작음 · 복잡도=작음 · 중요도=큼

# 브리프 — Wavvy 하네스의 브라우저 연결 기본값을 ego lite로 전환

## 젠 원문 (2026-11-01)
- 「Aside 아니고 ego lite로」 (23:00 시리즈 Suno 읽기 중 Aside 프로필 연결 끊김 뒤)
- 「병렬로 wavvy 하네스의 연결을 모두 ego lite로 바꿔줘」

## 목표
Wavvy 하네스(현행 운영 문서·스킬·계획)가 브라우저 작업에 쓰는 연결을 **ego lite(`ego-browser` CLI, Bash의 `ego-browser nodejs`)** 로 고정한다. 지금 스킬은 "젠이 고른 브라우저 제품·연결 방식"이라고만 적혀 있어 매번 Aside로 흘렀다. 앞으로는 기본값이 ego lite이고, 다른 브라우저는 젠이 그 작업에서 이름을 대 지정할 때만 쓴다.

## 오케스트레이터가 미리 잰 현황 (직접 다시 확인할 것)
- `git grep -n -i "aside"`: 하네스 코드(`wavvy_harness/`, `wavvy.py`, `tests/`, `scripts/`)·`MASTER/`·`skills/`·`.claude/`·`AGENTS.md`/`CLAUDE.md`에는 Aside 하드코딩이 없다.
- 브라우저 연결을 말하는 현행 자리:
  - `skills/wavvy-suno-batch/SKILL.md` 5단계 ("Use the browser product and connection method chosen by 젠")
  - `skills/wavvy-audio-ingest/SKILL.md` 2단계
  - `skills/wavvy-youtube-publish/SKILL.md` 3단계와 "Do not substitute a different browser connection…" 문단
  - `skills/wavvy-youtube-publish/references/comment-followup.md` 3단계
  - `skills/wavvy-youtube-publish/references/timed-subtitles.md` (29행 근처)
  - `.ai/plans/PLAN_music-distribution.md` — TLDR(3행)·§4(100·115·138·205·218행 근처)에 Aside MCP·REPL을 앞으로 쓸 연결로 적어 둠
- 다른 스킬(`wavvy-release`, `wavvy-thumbnail`, `wavvy-lyricist`)에도 브라우저 문구가 있는지 직접 grep 한다.

## 할 일
1. **한 곳에 규칙을 둔다(SSOT)**: `MASTER/ai/RUNTIME_RULES.md`에 짧은 절 `## Browser Connection`(또는 기존 절 구조에 맞는 위치)을 추가한다. 담을 내용:
   - 기본 브라우저 = ego lite, 연결 = `ego-browser` CLI(`ego-browser nodejs`). 근거 줄: 2026-11-01 젠 원문 두 개.
   - 작업 시작 시 `ego-browser skill`로 설치된 버전의 안내서를 읽고 그 API만 쓴다.
   - 한 목표에 TaskSpace 하나, 이어 쓰기, 젠 소유 탭(`openedBy: "unknown"`)은 닫지 않는다.
   - 지정 경로가 실패하면 다른 브라우저로 무음 전환하지 않고 멈추고 보고한다. 다른 브라우저는 젠이 그 작업에서 지정할 때만.
   - `ego-browser upgrade`는 젠에게 물은 뒤에만.
   - 과거 산출물에 적힌 Aside 기록은 당시 사실이며 바꾸지 않는다.
2. **스킬·참고 문서**는 규칙을 복제하지 말고, 위 자리의 문구를 "ego lite via the `ego-browser` CLI (Wavvy default; see `MASTER/ai/RUNTIME_RULES.md` Browser Connection) unless 젠 names another browser for that task" 꼴로 바꾼다. "대체 금지" 문장은 유지한다. 문장 언어는 각 파일의 기존 언어(영어)를 따른다.
3. **유통 계획** `.ai/plans/PLAN_music-distribution.md`: 앞으로 실행할 연결(TLDR·§4 실행 절차·업로드·U7·마지막 상태 문단)을 ego lite로 바꾼다. 단, 2026-10-27의 Aside 실측 사실(프로필 연결·탭 목록·Google 계정 조회 성공)은 "당시 Aside로 확인" 이력으로 남기고, ego lite에서의 Google·각 서비스 로그인 상태와 계정 목록 조회 방법은 **미확인**이라고 적는다(ego lite에 Aside `google-accounts` 같은 기능이 있다고 추측하지 않는다). 10행의 젠 원문 인용은 바꾸지 않고 그 아래에 2026-11-01 전환 원문을 덧붙인다.
4. **바꾸지 않는 것(이력·증거)**: `SERIES/**`(concept 이력 문단·download-manifest·validation·production JSON 등), `.ai/research/**`, `.ai/reviews/**`, `.ai/validation/**`, `.ai/cleanup/**`, `.ai/SESSION.md`, `.ai/HANDOFF.md`, `CHANGELOG.md`, 이미 끝난 옛 계획(`.ai/plans/2026-10-03_17-00-youtube-package.md` 등). 지금 다른 워커가 쓰고 있는 `.ai/research/2026-11-01-2300-nine-tracks/`는 절대 건드리지 않는다.
5. 테스트가 스킬 문구를 검사하는지 확인하고, 깨지면 문구가 아니라 원인을 보고한다.

## 검증 (원시 출력을 보고에 붙인다)
```bash
cd ~/Project/wavvy
python3 -m py_compile wavvy.py wavvy_harness/*.py
python3 -m unittest tests/test_harness.py
python3 wavvy.py doctor --json
git diff --check
git grep -n -i "aside" -- skills MASTER wavvy_harness tests .claude AGENTS.md CLAUDE.md wavvy.py scripts
git grep -n -i "browser product and connection method" -- skills MASTER
```
마지막 두 grep은 0건(또는 남은 건의 이유)을 보고한다. unittest의 기존 실패가 있으면 이번 변경 전(`git stash` 금지 — 대신 변경 파일 목록과 실패 테스트 이름으로 무관함을 설명)과 구분한다.

## 금지
- 커밋·푸시 금지(오케스트레이터가 판단). 브라우저를 실제로 열지 않는다(문서 작업만). `ego-browser upgrade` 금지.
- 하네스 코드에 브라우저 검사 로직을 새로 만들지 않는다(요청 범위 밖).

## 선례
- `skills/wavvy-youtube-publish/SKILL.md`의 "Do not substitute a different browser connection after a specified path fails" — 실패 시 대체 금지 규칙의 기존 문구. 유지·재사용한다.
- 전역 규칙: `~/Project/agent-center/CLAUDE.md` §Common Browser Selection Rule (제품+연결 방식 함께 준수).

## 보고
1. 바꾼 파일과 바뀐 줄 요약(파일별 1~2줄).
2. RUNTIME_RULES 새 절 전문.
3. 검증 명령 원시 출력 요약(통과/실패 수, grep 결과).
4. 바꾸지 않은 Aside 언급의 분류(이력/증거)와 건수.
5. 확인하지 못한 것.
