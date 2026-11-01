배정: 규모=작음 · 복잡도=작음 · 중요도=큼

# 브리프 C — 23:00 concept 갱신 (Lo-fi Remix 결정 반영 · 새 곡 STYLE 조립 기록 · Track Map · SPEC 한 줄)

## 젠 원문 (2026-11-01)
- 「Lo-fi remix는 붙여야해 안전빵이야. 현재버전들이 잘나온 이유로 보고있어」
- 이어진 질문 「'Lo-fi Remix' 표시를 새 11곡 중 어디에 붙일까요?」에 젠 선택: 「새 11곡 모두 (추천)」 — 옵션 설명: 11곡 스타일 맨 앞에 모두 'Lo-fi Remix,'를 붙임. 산책·마음 밖은 원문 위치 그대로, 나머지 7개 타입 곡은 맨 앞에 더함.
- 앞선 결정: 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」(골목의 원곡 멜로디 유지 문구 제거는 유지), 「선례처럼 끝에 덧붙이기」(없는 BPM·조성·성별만 끝에 덧붙임).

## 할 일 (파일: `SERIES/23-00/concept.md`, `MASTER/cli/SPEC.md`만)
1. `## Type Styles`
   - **산책·마음 밖**: (b) 새 곡용 STYLE을 (a) 원문과 같게 되돌린다(`Lo-Fi Remix`·`lo-fi remix` 유지). 편집 설명 줄을 "편집 없음 — 젠 「Lo-fi remix는 붙여야해 …」로 앞선 제거를 취소"로 바꾸고 글자 수·sha256을 다시 잰다.
   - **골목** (b) 편집과 **물결**의 `- EXCLUDE:` 줄은 절대 바꾸지 않는다(다른 워커의 검사가 이 줄을 읽는다).
2. 새 절 `## New Song Style Assembly`(Type Styles 뒤):
   - 조립 규칙 3줄: ① 타입의 (b) STYLE ② `lo-fi remix`(대소문자 무관)가 없으면 맨 앞에 `Lo-fi Remix, ` ③ STYLE에 없는 것만 끝에 `, NN BPM`, `, X Major|Minor`, `, male|female vocal` 순서로 덧붙임. 각 줄에 위 젠 원문 근거.
   - 곡별 표(10~20): 번호·제목·타입·보컬·BPM·조성·앞붙임 여부·덧붙인 항목·글자 수·sha256. 값은 `.ai/plans/2026-11-01-2300-new-song-styles.json`에서 가져오고, STYLE 전문은 json을 가리킨다(복제하지 않음).
   - **검증**: 갱신된 concept의 (b) 블록에서 위 규칙으로 11곡 STYLE을 다시 조립해 json의 `style`·`sha256`과 모두 같은지 스크립트로 대조하고 결과를 저장한다. 다르면 멈추고 보고한다.
3. `## Track Map`의 10~20 자리 행을 json 기준으로 채운다: 번호·제목·타입·보컬·조성·BPM·상태 `원고 작성 중 — 생성 전`. 원고 파일 경로는 `input/tracks/NN_<제목>.txt`.
4. `MASTER/cli/SPEC.md` 148행 근처 track-prompt 설명의 "EXCLUDE count (internal maximum eight items)"에, concept `## Type Styles`에 기록된 사용자 제공 타입 Exclude와 정확히 같을 때만 초과를 허용한다는 짧은 구절을 더하고 `MASTER/style/STYLE.md` §3을 가리킨다. 규칙 본문을 복제하지 않는다.

## 검증 (원시 출력을 `.ai/validation/2026-11-01-2300-foundation/2x-*`로 저장)
```bash
cd ~/Project/wavvy
python3 -m py_compile wavvy.py wavvy_harness/*.py
python3 -m unittest tests/test_harness.py
python3 wavvy.py state SERIES/23-00 --check --json
git diff --check
```
- 물결 `- EXCLUDE:` 줄이 이전과 바이트 동일한지 확인한다.

## 금지
- `SERIES/23-00/input/tracks/`, `.ai/lyrics/`, `.ai/plans/2026-11-01-2300-new-song-styles.json` 수정 금지(다른 워커가 동시에 사용). 커밋·브라우저 금지.

## 보고
1. 바꾼 곳 요약. 2. 산책·마음 밖 (b) 새 글자 수·sha256. 3. 조립 재현 대조 결과(11/11). 4. 검증 결과. 5. 미확인.
