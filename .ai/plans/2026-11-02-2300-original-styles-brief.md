배정: 규모=작음 · 복잡도=작음 · 중요도=큼

# 브리프 S — 23:00 재생성 9곡의 "원곡 스타일" 수집과 새 STYLE 조립안 (원고는 고치지 않음)

## 젠 원문 (2026-11-02)
- 「스타일도 수정하자」
- 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」
- 「템포도 좀 쳐져」 → 템포 질문에 젠 선택: 「원곡 BPM 그대로」

## 대상과 원곡 위치 (오케스트레이터 확인 — 직접 다시 확인)
| 새 곡 | 타입 | 원곡 위치 (23:00 리믹스 이전 원곡) | 원곡 BPM |
|---|---|---|---|
| 11 라디오 | 먼지 | `SERIES/14-00/concept.md` `### Track 09: 먼지` | 72 |
| 12 스웨터 | 마음 밖 | `SERIES/04-00/concept.md` 01 마음밖 (파일명 `01__마음밖__Sentimental__RnB-Ballad__90.mp3`) | 90 |
| 13 편지 | 작은 빛 | `SERIES/22-00/concept.md` 10 작은 빛 (Little Light) | 72 |
| 14 기타 | 산책 | `SERIES/14-00/concept.md` `### Track 03: 산책` | 74 |
| 15 노을 | 물결 | `SERIES/14-00/concept.md` `### Track 06: 물결` (젠이 채팅에 준 원본과 같은지 대조: `SERIES/23-00/concept.md` `### 물결` (a)) | 74 |
| 16 여름밤 | 물안개 | `SERIES/04-00/concept.md` 04 물안개 (`04__물안개__Hazy__Lo-fi-RnB__80.mp3`) | 80 |
| 17 막차 | 골목 | `SERIES/18-00/concept.md` Track 07 골목 (또는 `SERIES/Single/`의 골목 자료) | 67 |
| 18 벚꽃 · 19 그네 | 이름 | `SERIES/18-00/concept.md` `## 12. Track 09 "이름"` | 72 |

원곡 STYLE이 concept의 Final Track Sources나 트랙 절(`**Style Prompt:**`, `#### STYLE` 등)에 여러 판으로 있으면, **실제 발매·최종으로 표시된 판**을 고르고 고른 근거를 적는다. 확정할 수 없으면 후보를 모두 적고 "미확정"으로 둔다(추측 금지).

## 할 일 (읽기 + 조립안만 — `SERIES/23-00/input/tracks/*`·concept 수정 금지)
1. 타입마다 원곡의: STYLE 원문(줄바꿈 그대로), EXCLUDE(있으면), Suno Parameters(Weirdness·Style Influence 등 기록된 값), BPM·Key·보컬 성별, 출처(파일·제목줄·행 번호)를 모은다.
2. 새 STYLE 조립안: `Lo-fi Remix, ` + 원곡 STYLE. 단 장르 낱말 중 **alternative/Alt/얼터너티브, Modern R&B/모던 알앤비**에 해당하는 말만 뺀다(예: `Korean Indie Alt R&B` → `Korean Indie R&B`). 뺀 말을 정확히 기록한다. 그 밖의 단어·순서·BPM은 바꾸지 않는다. 원곡 STYLE 안에 `‑`/`-`로 시작하는 제외 항목이 있으면 STYLE에서 빼서 EXCLUDE 목록으로 옮긴다(23:00 물결 선례).
3. 조립안마다: 글자 수(900자 제한, 공백·줄바꿈 포함), STYLE 안 BPM 숫자 집합, Key, male/female 낱말 집합, EXCLUDE 항목 수를 잰다.
4. 새 곡 설계와 부딪히는 점을 표시만 한다: 설계 보컬(11 남·12 여·13 남·14 남·15 남·16 여·17 남·18 여·19 여)과 원곡 성별이 다른 곳, 900자 초과, EXCLUDE 8개 초과, BPM/Key가 STYLE에 없는 곳, 여러 줄 STYLE.

## 산출물
- `.ai/plans/2026-11-02-2300-original-styles.json`: 곡별 `{order, title, type, source:{path, heading, lines}, original_style, original_exclude, suno_params, bpm, key, vocal_gender, removed_words, proposed_style, proposed_exclude, chars, conflicts:[...]}`
- `.ai/plans/2026-11-02-2300-original-styles.md`: 사람이 읽는 요약표.

## 금지
- 원고·기록·concept·suno-candidates 수정 금지. 브라우저·생성·커밋 금지.

## 보고
1. 곡별 원곡 출처, BPM·Key·성별, Suno 파라미터.
2. 뺀 말, 조립안 글자 수, EXCLUDE 수.
3. 설계와 부딪히는 점 목록.
4. 미확정·미확인.
