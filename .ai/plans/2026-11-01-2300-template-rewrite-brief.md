배정: 규모=작음 · 복잡도=큼 · 중요도=큼

# 브리프 T — 23:00 새 곡 가사를 "타입 원곡 가사 틀 그대로 + 내용만 바꾸기"로 다시 쓰기

대상 곡은 워커 프롬프트에 적힌 번호만이다.

## 젠 원문 (2026-11-01~02, 순서대로)
- 「원곡들 가사를 보면, 후렴은 반복적이고 전체적으호 문장이 길지 않아」
- 「전반적으로 후렴이 중독성이 약하네」 → 다시 쓰기 범위: 「11곡 모두 다시 써서 생성 (추천)」, 「귤 통과」(10 귤 제외)
- 짧은 줄 + 의성어 훅으로 다시 쓴 판을 보고: 「아니 ㅜㅜㅜㅜ 야 기존 곡 가사 글자 수 그대로 내용만 바꿔」, 「라디오 후렴 개 극혐이다」(라디오 후렴: `지직지직 라디오 / 흥얼흥얼 따라 불러 / 노래가 흘러 흘러 / 지직지직 라디오`)
- 유지되는 앞선 지시: 따뜻한 그리움(「슬픔보다는 아련함. 따듯함이 느껴지게. 릴랙싱이 컨셉리니까. 옛기억에 위로받는 느낌. 따듯한 그리움」), 「분위기와 감각을 디테일하게」, 한국어 한 단어 제목, 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」

## 방법 — 개사(원곡 가사 틀에 새 말 넣기)
- 틀: 그 곡 **타입 원곡의 Suno 가사**(`.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json`의 해당 타입 `lyrics_full`). 타입은 `.ai/plans/2026-11-01-2300-new-song-styles.json`의 `type`.
- 그대로 지킬 것(검사 도구가 줄마다 잰다):
  1. 빈 줄을 뺀 줄 수와 순서(구간 태그 줄 / 가창 줄의 자리).
  2. **구간 태그 줄은 원곡과 글자 그대로**(예: `[Relaxed male vocal, no harmony]`, `[verse1]`, `[instrumental — Rhodes + warm pad, 8 bars]`).
  3. **가창 줄마다 글자 수(한글 음절 수)가 원곡 그 줄과 같게**. 원곡의 영어 낱말은 모음 덩어리 수로 센다(예: `little light` = 3 → 한국어 3음절).
  4. 원곡이 같은 줄을 되풀이하는 자리(후렴 반복 등)는 새 가사도 같은 줄을 되풀이.
- 가능하면 지킬 것: 줄 안의 띄어쓰기 마디 나눔(예: 원곡 `햇살이 번져가` = 3+3이면 새 줄도 3+3), 원곡 후렴의 줄 끝 소리 흐름. 노래 박자에 같은 자리로 얹히게 하려는 것이다.
- 바꿀 것: **내용 전부**. 그 곡의 장면·중심 감각(아래 표)과 따뜻한 그리움으로 새로 쓴다. 원곡의 핵심 낱말·이미지(햇살·먼지·물결·골목·가로등·안개·이름 부르기·잠든 아이 등)를 가져오지 않는다. 같은 문법 어미(-가, -어 등)가 자연히 겹치는 것은 괜찮다.
- 하지 말 것: 의성어를 늘어놓는 훅(`지직지직`, `흥얼흥얼` 같은 것 — 젠 「극혐」), 원곡에 없는 반복을 새로 만들기, 영어, 눈물·이별 아픔·후회·매달림.
- 노래로 불렀을 때 자연스러운 한국어여야 한다. 글자 수를 맞추려고 억지 낱말을 끼우지 않는다(어색하면 다른 표현을 찾는다).

## 곡 설계 (바꾸지 않음)
| 번호 | 제목 | 타입(틀) | 보컬 | 장면 · 중심 감각 |
|---|---|---|---|---|
| 11 | 라디오 | 먼지 | 남성 | 밤 11시 라디오에서 그 시절 같이 따라 부르던 노래 · 소리(잡음, 안테나, 엉뚱하게 바꿔 부르던 가사) |
| 12 | 스웨터 | 마음 밖 | 여성 | 빌려 입고 못 돌려준 스웨터를 첫 추운 날 꺼내 입음 · 긴 소매·보풀·섬유유연제 냄새 |
| 13 | 편지 | 작은 빛 | 남성 | 서랍 속 손글씨 편지 · 종이 바스락, 꾹꾹 눌러 쓴 글씨, 번진 잉크 |
| 14 | 기타 | 산책 | 남성 | 그 사람이 쳐 주던 서툰 기타 · 줄 소리, 손끝 굳은살, 틀린 코드에 같이 웃음 |
| 15 | 노을 | 물결 | 남성 | 옥상에서 같이 보던 노을과 따뜻한 캔커피 · 주황빛, 손바닥 온기 |
| 16 | 여름밤 | 물안개 | 여성 | 평상에 누워 별 세던 여름밤 · 선풍기, 매미, 모기향, 수박 |
| 17 | 막차 | 골목 | 남성 | 막차 버스에서 어깨에 기대 졸던 무게 · 흔들림, 창에 비친 두 얼굴 |
| 18 | 벚꽃 | 이름 | 여성 | 벚꽃 아래 머리에 앉은 꽃잎을 떼어 주던 손 · 꽃잎, 봄바람 |
| 19 | 그네 | 이름 | 여성 | 밤 놀이터 그네에 나란히 흔들리던 시간 · 흔들림, 밤공기, 쇠사슬 소리 |
| 20 | 포근히 | 숨 | 여성 | 잠들기 전 그 기억이 이불처럼 덮어 줌, 마지막 곡 · 온몸의 온기, 베개 |
- 18·19는 같은 틀(이름)이라 두 곡의 낱말·훅이 서로 닮지 않게 한다. 20은 통과한 10 귤(같은 숨 타입, `SERIES/23-00/input/tracks/10_귤.txt`)과 후렴 낱말이 겹치지 않게 한다.
- 원곡 틀의 구간 태그가 성별을 적고 있으면(예: 숨 `[Female, …]`, 먼지 `[Relaxed male vocal…]`) 그 성별이 위 표와 같다. 틀 태그는 바꾸지 않는다.

## 할 일 (대상 곡마다)
1. **이전 판 보존**: 지금 원고·기록을 `SERIES/23-00/input/source-history/2026-11-01-before-template-lyrics/`(원고)와 그 아래 `lyrics-records/`(기록)로 복사한다(sha256 대조). 그다음 원본을 덮어쓴다.
2. 기록 `.ai/lyrics/2026-11-01_23-00_NN_<제목>-full-draft.md`를 새로 쓴다: Source Map(위 젠 원문 · 틀 원곡 제목/ID · 이전 판 두 개 경로 · 1차 후보 ID 2개), Constraint Freeze(section_bars는 틀의 구간 이름·순서 그대로, target_duration은 틀 원곡의 실제 길이 근처, 틀이 Verse 3개·Intro/Outro 기본과 다르면 `verse_structure_exception`·`intro_outro_exception`에 "같은 타입 원곡 가사 틀을 그대로 따름 — 젠 「기존 곡 가사 글자 수 그대로 내용만 바꿔」"), Lyric Strategy, Draft, Self-Gate(전부 새로).
3. 원고 txt의 `=== LYRICS ===`를 새 Draft로 바꾸고 머리말 Status(`full-lyric-draft (template rewrite on type original — 젠 2026-11-02); generation pending`)·Section Bars·Target Duration만 맞춘다. STYLE·EXCLUDE·나머지 머리말은 그대로.
4. 검사 — 범위: 이번에 다시 쓴 곡만. 모두 PASS가 될 때까지 가사·기록만 고친다:
```bash
cd ~/Project/wavvy
python3 .ai/plans/2026-11-01-2300-template-check.py NN --json-out .ai/validation/2026-11-01-2300-lyrics/NN-template-check.json
python3 wavvy.py lyrics-skill SERIES/23-00 --artifact <기록.md> --mode full-lyric-draft --draft-scope full-song --json   > .ai/validation/2026-11-01-2300-lyrics/NN-lyrics-skill-template.json
python3 wavvy.py gate SERIES/23-00 --stage lyrics-review --artifact <기록.md> --mode full-lyric-draft --draft-scope full-song --json > .ai/validation/2026-11-01-2300-lyrics/NN-lyrics-review-template.json
python3 wavvy.py gate SERIES/23-00 --stage track-prompt --artifact "SERIES/23-00/input/tracks/NN_<제목>.txt" --json > .ai/validation/2026-11-01-2300-lyrics/NN-track-prompt-template.json
```
   (zsh 단어 나누기 사고가 있었으니 반복 실행은 bash로 하고 파일 이름에 공백이 생기지 않게 한다.)
5. txt LYRICS == 기록 Draft, STYLE sha256 == json 값 대조를 `NN-template-compare.json`으로 저장.

## 금지
- 대상 외 곡·01~09·10 귤·STYLE·EXCLUDE·`concept.md`·`suno-candidates.json` 수정 금지(오케스트레이터가 나중에 한 번에 맞춤). 브라우저·생성·커밋 금지.

## 보고
1. 곡별 새 Draft 전문(되풀이 후렴은 한 번만 적고 "같음" 표시 가능).
2. 템플릿 검사·세 검사 결과.
3. 글자 수를 맞추느라 표현이 조금이라도 억지스러운 줄이 있으면 그 줄과 이유(오케스트레이터 검수용).
4. 보존한 이전 판 경로.
5. 미확인.
