배정: 규모=큼 · 복잡도=큼 · 중요도=큼

# 브리프 G2 — 23:00 9곡(11~19) Suno 재생성 (크레딧 사용 승인됨)

## 젠 원문
- 2026-11-01 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」
- 2026-11-02 다시 쓰기 범위 「11곡 모두 다시 써서 생성 (추천)」(이후 「귤 통과」「포근히 통과」로 10·20 제외 → 11~19 9곡)
- 브라우저 「Aside 아니고 ego lite로」 · 번호 「넘버링은 나중에 일괄로 할게」

## 따를 것
- 1차 생성 브리프 `.ai/plans/2026-11-01-2300-generation-brief.md`의 Suno 작업 규칙 전부(매 제출 직전 `[23:00]` 확인 · 곡당 정확히 1회 · 제출 전 입력칸 재읽기 대조 · 불확실하면 다시 누르지 않고 멈춤 · 재생·다운로드·공개 변경·좋아요/싫어요·삭제·기존 곡 수정 금지). 1차 증거 `SERIES/23-00/input/validation/2026-11-01-generation/`의 스크립트(`ego/scripts/`)를 재사용해도 된다.
- `MASTER/ai/RUNTIME_RULES.md` Browser Connection: ego lite `ego-browser nodejs`만, 먼저 `ego-browser skill` 안내서를 끝까지 읽기, TaskSpace는 `taskSpace("wavvy-2300-suno-regenerate")` 하나, upgrade 금지.

## 입력
- `SERIES/23-00/input/tracks/11_라디오.txt` ~ `19_그네.txt` 9개. 제출 직전 각 txt로 `python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "<txt>" --json`이 PASS이고 detail에 `user-supplied original style`이 있는지 확인(원시 저장). 아니면 그 곡은 제출하지 않고 보고.
- STYLE은 **여러 줄**일 수 있다. 줄바꿈을 그대로 Styles 칸에 넣고, 다시 읽어 줄바꿈 정규화 후 txt와 같은지 대조한다. Suno가 줄바꿈을 지우거나 바꾸면 그 사실과 실제 입력값을 기록한다(멈출 필요는 없음 — 단 글자·낱말이 빠지면 멈춤).
- EXCLUDE: txt 값을 고급 옵션 Exclude 칸에 넣는다. 빈 곡은 칸을 비운다.
- **Suno 파라미터**: txt 머리말 `Suno Params`대로 매 곡 제출 전에 명시적으로 맞춘다. 값이 있으면(11: W20/I80, 14: W25/I75, 15: W20/I80) 그 값, `default`면 1차 관측 기본값 Weirdness 50 / Style Influence 50으로 되돌려 앞 곡 값이 남지 않게 한다. 보컬 성별 옵션은 선택하지 않는다(1차와 같음). 실제 화면 값을 곡마다 기록.
- 제목은 txt `Track:` 값(번호 없음).

## 기록 — `SERIES/23-00/input/suno-candidates.json` 갱신
- 11~19의 기존 후보는 지우지 않고 각 후보에 `generation_round: 1`을 붙인다(없으면). 새 후보 2개를 `generation_round: 2`로 추가하고, 곡 항목에 `submissions[]`(라운드·시각·source_sha256·입력 대조·설정 관측)를 둔다. `source_sha256`·`source_txt`는 이번 제출 txt 기준. `decision`은 `{"status":"pending","chosen_candidate_id":null}`로 되돌리고 이전 `regenerate` 결정과 근거는 `decision_history[]`로 옮긴다.
- 최상위 `credits_before_round2`·`credits_after_round2`(시작 646 예상).
- 01~10·20 항목은 바꾸지 않는다.
- 원시 증거: `SERIES/23-00/input/validation/2026-11-02-regeneration/`.

## 마무리
- 새 후보 18개가 모두 완료될 때까지 목록을 다시 읽어 길이·상태 갱신(최대 20분).
- `python3 wavvy.py state SERIES/23-00 --check --json` 저장. state 쓰기·커밋 금지. 직접 연 Page만 닫는다.

## 보고
1. 곡별 제출 결과와 새 후보 2개 ID·길이·상태.
2. 크레딧 전후.
3. 곡별 Suno 파라미터 관측값, 여러 줄 STYLE 입력 결과(줄바꿈 보존 여부).
4. 입력 대조 결과.
5. 멈춘 곳·미확인.
