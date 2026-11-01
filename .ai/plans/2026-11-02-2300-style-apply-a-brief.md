배정: 규모=작음 · 복잡도=큼 · 중요도=큼

# 브리프 A2 — 23:00 재생성 9곡의 최종 STYLE 확정과 concept·장부 정리

## 젠 원문 (2026-11-02)
- 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」
- 「템포도 좀 쳐져」 → 「원곡 BPM 그대로」
- 여름밤·벚꽃·그네 보컬 질문 → 「원곡대로 남성」
- 앞선 원칙: 「- 붙은 스타일은 exclude인거 알지?」(빼 달라는 항목은 EXCLUDE 칸), 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」(새 곡에서 뜻이 없는 원곡 가사 전용 지시만 최소 편집 + 기록), 「Lo-fi remix는 붙여야해 안전빵이야」
- 탈락·통과: 「라디오 탈락」, 「귤 통과」「귤은 B」, 「포근히 통과」「포근히 B」, 다시 쓰기 범위 「11곡 모두 다시 써서 생성 (추천)」 → 재생성 대상 11~19 9곡.

## 입력
- `.ai/plans/2026-11-02-2300-original-styles.json` / `.md` (원곡 STYLE 원문·출처·Suno 파라미터·조립안·충돌 목록 — 워커 S 결과).

## 할 일
1. **최종 STYLE/EXCLUDE 확정** — 곡별(18·19는 같은 '이름' 항목 하나):
   - STYLE = `Lo-fi Remix, ` + 원곡 STYLE 원문(줄바꿈 보존). 편집은 아래만, 모두 기록:
     a. 장르 낱말의 alternative/Alt·Modern R&B만 제거(조사 결과: 산책·물결의 `Alt` 2건).
     b. 원곡 STYLE 안에 들어 있는 `Exclude Style:`/`EXCLUDE:` 줄(11 먼지, 17 골목, 18·19 이름)은 STYLE에서 빼서 EXCLUDE로 옮긴다. 먼지는 같은 절의 별도 EXCLUDE 블록(10개)을 쓴다.
     c. 원곡 가사에 묶여 새 곡에서 뜻이 없는 지시만 최소 편집(조사 결과: 이름의 `Last "괜찮아"` 관련 구절, 원곡에만 있는 `Bridge3` 지칭). 지울 범위를 가장 작게 하고 원문·편집본을 둘 다 남긴다. 다른 곳에서 비슷한 것을 찾으면 고치지 말고 보고한다.
     d. 성별은 원곡대로(16·18·19 남성 — 젠 「원곡대로 남성」). BPM 숫자·Key·나머지 문구는 바꾸지 않는다(12 마음밖의 `96–106 BPM`, `key color like A♭`, `no catchy hook`도 원문 그대로).
   - EXCLUDE = 원곡 EXCLUDE(있으면) + b에서 옮긴 항목(순서 보존, 중복 제거 시 기록).
   - Suno 파라미터: 원곡에 기록된 값(11: W20/I80, 14: W25/I75, 15: W20/I80)은 그대로 쓰고, 기록이 없으면 `default`.
   - 결과를 `.ai/plans/2026-11-02-2300-final-styles.json`에 곡별로: `order, title, type, style, style_chars, style_sha256, exclude[], suno_params, bpm_header, key_header, vocal_header, edits[]`. 머리말 값은 STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현 그대로(예: `96–106 (original STYLE wording; release file 90)`, `A♭ (original wording "key color like A♭"; mode not stated)`).
2. **`SERIES/23-00/concept.md`**:
   - 새 절 `## Original Styles`(검사 도구가 읽는 형식 — `.ai/plans/2026-11-02-2300-original-style-gate-brief.md`): 타입별 `### <타입>` 아래 출처·편집 목록·Suno 파라미터 줄, 첫 ```` ```text ```` 블록 = 최종 STYLE 그대로, `- EXCLUDE: a, b, c` 한 줄. 타입: 먼지, 마음 밖, 작은 빛, 산책, 물결, 물안개, 골목, 이름.
   - `## Series Overrides`에 두 항목: 가사(타입 원곡 가사 틀 — 줄 수·태그·줄별 글자 수·반복 그대로, 내용만 바꿈 + 젠 원문), 스타일(위 규칙 + 젠 원문). 이전 Overrides 중 "짧은 줄" 항목이 있으면 "대체됨"으로 표시.
   - `## New Song Style Assembly` 절 머리에 "10·20만 해당(1차 생성 원고). 11~19는 `## Original Styles`로 대체 — 2026-11-02"를 적는다.
   - `## Track Map` 11~19행: 보컬·BPM·Key를 원곡 기준으로, 상태 `재생성 대기 (원곡 가사 틀 + 원곡 스타일)`. 10·20행: `확정 — 후보 B` 와 ID.
3. **`SERIES/23-00/input/suno-candidates.json`**: 11~19의 `decision`을 `{"status":"regenerate","chosen_candidate_id":null}`로, `decision_evidence`에 젠 원문(「라디오 탈락」, 「전반적으로 후렴이 중독성이 약하네」, 「11곡 모두 다시 써서 생성 (추천)」)과 날짜. 기존 후보는 지우지 않는다. 10·20은 이미 기록됨 — 건드리지 않는다.

## 검증
- 최종 STYLE을 concept의 text 블록에서 다시 읽어 json `style`과 바이트 비교(9/9), 편집 전후 diff가 `edits[]`와 같은지 확인 → `.ai/validation/2026-11-02-2300-styles/a2-check.json`.
- `python3 wavvy.py state SERIES/23-00 --check --json` PASS 확인.

## 금지
- `SERIES/23-00/input/tracks/*`·`.ai/lyrics/*` 수정 금지(다음 단계). `wavvy_harness/`·`tests/`·`MASTER/` 수정 금지(다른 워커 작업 중). 브라우저·생성·커밋 금지.

## 보고
1. 곡별 최종 STYLE 글자 수·EXCLUDE 수·편집 목록. 2. concept 바꾼 절. 3. 장부 변경. 4. 검증 결과. 5. 미확인.
