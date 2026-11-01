배정: 규모=작음 · 복잡도=큼 · 중요도=큼

# 브리프 B2 — 23:00 재생성 9곡 원고에 원곡 스타일·가사 교정 반영

대상 곡은 워커 프롬프트에 적힌 번호만이다.

## 젠 원문 (2026-11-02)
- 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」 · 「원곡 BPM 그대로」 · 「원곡대로 남성」
- 「기존 곡 가사 글자 수 그대로 내용만 바꿔」(가사 틀은 이미 반영됨) · 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」

## 입력
- 최종 STYLE/EXCLUDE/머리말 값/Suno 파라미터: `.ai/plans/2026-11-02-2300-final-styles.json` (concept `## Original Styles`와 같은 값 — 바이트 그대로 쓴다).
- 오케스트레이터 가사 교정표(아래). 모든 교정은 원곡 틀 글자 수와 같음을 오케스트레이터가 확인했다.

| 곡 | 기존 줄 | 새 줄 |
|---|---|---|
| 11 라디오 | 낮은 목소리가 사연을 | 낮은 목소리 사연 하나 |
| 11 라디오 | 읽고 나면 잡음 속에서 | 끝나고 나면 잡음 속에 |
| 11 라디오 | 틀린 가사 신나게 부르던 | 틀린 가사 신나게 부른 너 |
| 13 편지 | “잘 있어 / 잘 있어” (따옴표 포함 두 줄) | “따뜻해 / 따뜻해” (따옴표 위치 그대로) |
| 13 편지 | 또 올게 (두 줄 모두) | 또 볼게 |
| 15 노을 | 해 지는 쪽부터 주황빛 | 서쪽 하늘이 물들어 가 |
| 17 막차 | 머리에서 나던 샴푸 냄새가 아직 나요 | 그 샴푸 향기가 아직 코끝에 남았어요 |
| 17 막차 | 왠지 네가 앉아 있는 듯이 아늑해요 | 네가 앉았던 것처럼 괜히 따뜻해요 |
| 18 벚꽃 | 꽃잎들이 살짝 모여 쉬었네 | 꽃잎 한 장이 사뿐히 앉았네 |
| 18 벚꽃 | 봄 하나 얹고 | 머리에 한 장 |
| 19 그네 | 내 몸이 먼저 기억을 하네 | 두 다리가 먼저 흔들려 와 |
12·14·16은 가사 교정 없음. 기존 줄이 정확히 없으면 그 곡은 멈추고 보고한다.

## 할 일 (곡마다)
1. **보존**: 지금 원고·기록을 `SERIES/23-00/input/source-history/2026-11-02-before-original-style/`(원고)와 그 아래 `lyrics-records/`(기록)로 복사(sha256 대조).
2. **가사 교정**: 기록 Draft와 원고 LYRICS에 같은 교정을 같은 횟수로. 바뀐 줄을 인용하던 Self-Gate 항목은 새 줄로 맞추고 Source SHA256 갱신.
3. **원고 txt**:
   - `=== STYLE ===` = json `style` 그대로(줄바꿈 보존), `=== EXCLUDE ===` = json `exclude`를 `, `로 이은 한 줄(없으면 비움).
   - 머리말: `BPM`·`Key`·`Vocal`을 json `bpm_header`·`key_header`·`vocal_header`로, `Style Type: <타입>`, `Style Source: user-supplied original style`, `Suno Params: <json suno_params>`. 15의 `Exclude Source` 줄은 지운다. `Genre` 줄은 원곡 STYLE의 장르 표현으로. Status = `full-lyric-draft (template lyrics + original style — 젠 2026-11-02); regeneration pending`. Target Duration·Section Bars는 4번과 같게.
   - `=== META ===` 칸이 있으면 남기되, 사실과 달라진 문장(예: "reference remix lyric was read only for diction")은 지금 방식(원곡 가사 틀 개사 + 원곡 스타일)에 맞게 고친다.
4. **기록**: Constraint Freeze의 bpm·key·vocal_identity·genre_lane을 새 값으로, BPM이 바뀌었으니 `section_bars`·`target_duration_seconds`·duration_plan을 다시 계산(목표는 타입 원곡 길이 근처 — 23:00 리믹스 길이 `nine-tracks.json` `duration_ui` 참고). Source Map에 원곡 스타일 출처(json `source`)와 젠 원문, 이전 판 경로 추가.
5. **검사 — 범위: 이번 대상 곡만**. 원시 결과 `.ai/validation/2026-11-02-2300-styles/NN-*.json`:
```bash
cd ~/Project/wavvy
python3 .ai/plans/2026-11-01-2300-template-check.py NN --json-out .ai/validation/2026-11-02-2300-styles/NN-template-check.json
python3 wavvy.py lyrics-skill SERIES/23-00 --artifact <기록.md> --mode full-lyric-draft --draft-scope full-song --json
python3 wavvy.py gate SERIES/23-00 --stage lyrics-review --artifact <기록.md> --mode full-lyric-draft --draft-scope full-song --json
python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "SERIES/23-00/input/tracks/NN_<제목>.txt" --json
```
   track-prompt 결과의 `style_character_limit`·`exclude_budget` detail에 `user-supplied original style (<타입>)`이 찍혀야 한다(모드가 켜졌다는 증거). 안 찍히면 STYLE/EXCLUDE가 concept과 다른 것이니 json 값으로 다시 맞춘다 — concept은 고치지 않는다. 반복 실행은 bash로, 파일 이름에 공백 없이.
6. 대조: txt STYLE sha256 == json `style_sha256`, txt EXCLUDE 항목 == json, txt LYRICS == 기록 Draft → `NN-apply-compare.json`.

## 금지
- 대상 외 곡·01~10·20·`concept.md`·`suno-candidates.json`·`wavvy_harness/`·`tests/`·`MASTER/` 수정 금지. 브라우저·생성·커밋 금지.

## 보고
1. 곡별 네 검사 결과와 모드 켜짐 증거. 2. 적용한 가사 교정 수. 3. 새 BPM·Key·Vocal·목표 길이. 4. 대조 결과. 5. 미확인.
