배정: 규모=큼 · 복잡도=큼 · 중요도=큼

# 브리프 G — 23:00 새 11곡 Suno 첫 생성 (크레딧 사용 승인됨)

## 젠 원문 (2026-11-01)
- 「진행」(새 시리즈 일괄 제작 시작) · 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」
- 브라우저: 「Aside 아니고 ego lite로」 → `MASTER/ai/RUNTIME_RULES.md` Browser Connection.
- 「넘버링은 나중에 일괄로 할게」 → Suno 제목에 번호를 붙이지 않는다.

## 따를 문서
- `skills/wavvy-suno-batch/SKILL.md` 5단계 전부(작업공간 확인 · 곡당 1회 제출 · 후보 2개를 한 제출의 후보로 기록 · 실패를 조용히 다시 시도하지 않음).
- `MASTER/ai/RUNTIME_RULES.md` Browser Connection: ego lite `ego-browser nodejs`만. 먼저 `ego-browser skill` 안내서를 끝 줄까지 읽는다. TaskSpace는 `taskSpace("wavvy-2300-suno-generate")` 하나만 쓰고 이어 쓴다. 다른 브라우저 전환·`ego-browser upgrade` 금지. 젠 소유 탭은 닫지 않는다.

## 입력 (원고가 유일한 근거)
- `SERIES/23-00/input/tracks/10_귤.txt` ~ `20_포근히.txt` 11개. 각 txt의 `=== STYLE ===`, `=== EXCLUDE ===`, `=== LYRICS ===` 본문을 **글자 그대로** 넣는다(앞뒤 공백만 정리). 제목은 txt의 `Track:` 값(번호 없음).
- 제출 전에 각 txt로 `python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "<txt>" --json`이 PASS인지 다시 확인하고 원시 결과를 저장한다. FAIL이면 그 곡은 제출하지 않고 보고한다.

## Suno 작업
- 작업공간: `[23:00]` (`https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480`). **매 제출 직전** 화면에서 활성 작업공간이 `[23:00]`인지 확인한다. 다르면 제출하지 않고 멈춘다.
- Custom 모드로 Lyrics·Styles·Title을 채운다. EXCLUDE가 있는 곡(15 노을)은 고급 옵션의 Exclude 칸에 넣는다. EXCLUDE가 빈 곡은 Exclude 칸을 비운다.
- 보컬 성별 옵션·Weirdness·Style Influence·페르소나·오디오 업로드는 바꾸지 않는다(기본값). 화면에 보이는 모델 버전과 각 설정 값을 그대로 기록한다.
- 제출은 곡당 **정확히 1회**. 넣은 뒤 제출 전에 입력칸 값을 다시 읽어 txt와 같은지 대조한다(줄바꿈 정규화 후). 제출 뒤 그 제목의 새 후보 2개가 작업공간 목록에 나타나는지 확인하고 ID·표시 이름·상태(생성 중/완료)·길이를 기록한 다음 다음 곡으로 간다.
- 제출 결과가 불확실하면(버튼 반응 없음·오류·후보 미표시) 다시 누르지 말고 화면을 다시 읽어 확인한다. 그래도 불확실하면 그 곡에서 멈추고 보고한다. 크레딧을 쓰는 재시도는 하지 않는다.
- 시작 전·끝난 뒤 크레딧 표시를 기록한다(시작 시 756 예상).
- 재생·다운로드·공개 변경·좋아요/싫어요·삭제·기존 9곡 수정 금지.

## 기록 — `SERIES/23-00/input/suno-candidates.json`
- 스킬 5단계 스키마: 최상위 `schema`, `series`(`SERIES/23-00`), `workspace`(화면 이름 정확히), `workspace_id`, `browser`(`ego lite / ego-browser CLI, TaskSpace <id>`), `credits_before`, `credits_after`, `model_observed`, `tracks[]`.
- `tracks[]` 20개(order 1~20):
  - 01~09: `title`(txt Track), `source_txt`(`input/tracks/…`), `source_sha256`(파일 sha256), `candidates`=[기존 리믹스 1개: `id`, `displayed_name`, `url`, `observed_status`], `decision`={`status`:"keep","chosen_candidate_id":<그 id>}, `provenance`: "user-provided lo-fi remix — 젠 2026-11-01 「이미 기존에 만들었던 어울리는 곡들을 lo-fi remix 형태로 만들어두었어」". ID는 `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json`에서 가져온다.
  - 10~20: `title`, `source_txt`, `source_sha256`(제출한 txt), `submission`(시각·입력 대조 결과·설정 관측), `candidates`=[새 후보 2개: `id`, `displayed_name`, `url`, `observed_status`, `duration_displayed`], `decision`={`status`:"pending","chosen_candidate_id":null}.
- 원시 증거: `SERIES/23-00/input/validation/2026-11-01-generation/` (곡별 입력칸 읽기·제출 전후 목록·크레딧·ego 명령 로그).

## 마무리
- 모든 후보가 "완료"가 될 때까지 기다리며 목록을 다시 읽어 최종 상태·길이를 갱신한다(최대 20분, 넘으면 그때 상태로 기록).
- `python3 wavvy.py state SERIES/23-00 --check --json` 결과를 저장한다. state 쓰기는 하지 않는다(오케스트레이터 판단).
- 직접 연 Page만 닫는다. 커밋 금지.

## 보고
1. 곡별 제출 결과(성공/실패/불확실), 후보 2개 ID·길이·상태.
2. 크레딧 전후와 사용량.
3. 작업공간 확인 기록, 모델·설정 관측값.
4. 입력 대조 결과(11곡).
5. 멈춘 곳·미확인.
