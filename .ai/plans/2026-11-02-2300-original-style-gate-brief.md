배정: 규모=작음 · 복잡도=큼 · 중요도=큼

# 브리프 H — track-prompt 검사에 "젠 원곡 스타일 그대로" 모드 추가

## 배경 (젠 원문 2026-11-02)
- 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」, 템포는 「원곡 BPM 그대로」.
- 원곡 스타일 조사 결과: `.ai/plans/2026-11-02-2300-original-styles.{json,md}`. 원곡 STYLE은 Wavvy 내부 예산·검사 형식과 맞지 않는 곳이 있다: 산책 원곡 + `Lo-fi Remix, `가 955자(내부 예산 900), 마음밖은 `96–106 BPM`·`key color like A♭`(Major/Minor 없음), 원곡 EXCLUDE 10~18개(내부 예산 8), 여러 줄 STYLE.
- 이 예산은 Wavvy 내부 예산이다(`MASTER/style/STYLE.md` §3 — Suno 공식 한도가 아님). 젠은 앞서 같은 성격의 결정에서 「13개 모두 유지 (추천)」(사용자 제공 원본 Exclude는 8개를 넘어도 기록되어 있으면 통과)을 골랐다. 이번 모드는 그 원칙을 "젠 원곡 STYLE 전체"로 넓힌다.

## 현재 코드 (선례 — 이 방식을 따른다)
- `wavvy_harness/gate.py` `_user_type_exclude_exception`: txt 머리말 `Style Type`+`Exclude Source: user-supplied type style` → concept `## Type Styles` → `### <타입>` → `- EXCLUDE:` 줄과 항목·순서가 정확히 같을 때만 Exclude 8개 초과를 통과. 테스트는 `tests/test_harness.py`에 있다.

## 만들 것
1. **새 모드 "원곡 스타일 그대로"** (`_track_prompt_gate`):
   - 켜지는 조건: txt 머리말 `Style Type: <타입>`과 `Style Source: user-supplied original style`. 그리고 같은 시리즈 `concept.md`의 `## Original Styles` 절 → `### <타입>` 항목이 정확히 하나 있고, 그 안의 첫 ```` ```text ```` 블록 본문이 txt `=== STYLE ===` 본문과 **바이트 단위로 같고**(앞뒤 공백만 정리, 줄바꿈 보존), 그 항목의 `- EXCLUDE:` 줄 항목이 txt EXCLUDE 항목과 **순서까지 같을** 때.
   - 켜지면: `style_character_limit`(900)과 `exclude_budget`(8)은 막지 않고 detail에 실제 값과 `user-supplied original style (<타입>)`을 남긴다. BPM/Key/Vocal 대조는 STYLE에서 그 값을 읽을 수 있을 때만 지금처럼 막고, 읽을 수 없거나(예: `key color like A♭`) 범위 표기(예: `96–106 BPM`)일 때는 막지 않되 머리말 값이 비어 있으면 막는다. detail에 STYLE에서 읽은 값과 머리말 값을 함께 적는다.
   - 조건이 하나라도 안 맞으면 지금과 똑같이 검사한다(예외 없음) + detail에 맞지 않은 이유.
   - 기존 `Type Styles` Exclude 예외는 그대로 둔다(이미 생성된 10 귤·20 포근히 원고와 이력 재현용).
2. **테스트** (`tests/test_harness.py`, 기존 스타일): ① 모드 PASS(950자·Exclude 14개·여러 줄·Key 모드 없음·BPM 범위) ② STYLE 한 글자 다름 → 기존 검사로 FAIL ③ concept에 타입 없음 → FAIL ④ EXCLUDE 순서 다름 → FAIL ⑤ 머리말 `Style Source` 없음 → FAIL ⑥ STYLE에서 BPM을 읽을 수 있는데 머리말과 다름 → FAIL ⑦ 머리말 Key 비어 있음 → FAIL ⑧ 기존 동작 회귀 없음.
3. **규칙 문서**: `MASTER/style/STYLE.md` §3에 한 줄(근거: 위 젠 원문), `MASTER/cli/SPEC.md` track-prompt 설명에 한 구절로 STYLE.md를 가리킨다. 복제 금지.

## 검증 (원시 출력 `.ai/validation/2026-11-02-2300-original-style-gate/`)
```bash
cd ~/Project/wavvy
python3 -m py_compile wavvy.py wavvy_harness/*.py
python3 -m unittest tests/test_harness.py
python3 wavvy.py doctor --json
git diff --check
```
- 새 테스트가 실제로 판별하는지: 예외 함수를 항상 참/항상 거짓으로 바꾼 복사본에서 해당 테스트가 FAIL하는지 확인(선례: `.ai/validation/2026-11-01-2300-foundation/03-mutation-check.txt`).

## 금지
- `SERIES/23-00/**`(concept·원고)·`.ai/lyrics/**`·`suno-candidates.json` 수정 금지(다른 단계에서 함). 브라우저·생성·커밋 금지.

## 보고
1. 바꾼 파일·함수·줄. 2. 테스트 수와 결과, 판별력 확인. 3. 문서 변경 문장. 4. 미확인.
