배정: 규모=작음 · 복잡도=작음 · 중요도=큼

# 브리프 — Wavvy 23:00 Suno 작업공간 기존 곡 읽기 전용 수집

## 목표
젠이 만든 23:00 시리즈 Suno 작업공간에서 기존 lo-fi 리믹스 곡들의 가사·스타일·설정을 **글자 그대로** 수집한다. 오케스트레이터가 이 자료로 스타일 "타입"을 나누고 새 11곡을 설계한다. 이번 작업은 읽기만 한다.

- 작업공간 URL: https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480
- 찾을 9곡(젠이 알려 준 이름): 먼지, 산책, 숨, 이름, 마음 밖, 물안개, 골목, 물결, 작은 빛
- 실제 화면 제목에는 접미어(예: `(Lo-fi Remix)`)나 다른 표기가 붙어 있을 수 있다. 화면 그대로 기록한다.

## 브라우저 (지정 — 바꾸지 않는다 · 2026-11-01 젠 「Aside 아니고 ego lite로」)
- **ego lite를 `ego-browser` CLI(Bash의 `ego-browser nodejs`)로만** 쓴다. 먼저 `ego-browser skill > "$TMPDIR/ego-browser-skill.md"`로 사용 안내 전문을 저장해 끝 줄(`[ego-browser:skill] end of guide`)까지 읽고 그 API만 쓴다(Playwright 메서드 추측 금지).
- 오케스트레이터가 연결을 확인하며 만든 **TaskSpace `wavvy-2300-suno-read`(spaceId 118, Page `p1`)** 하나만 쓴다. `await taskSpace(118)`로 이어 쓰고, 새 TaskSpace를 만들지 않는다. 막히면 같은 공간 안에서 복구하고, 안 되면 멈추고 보고한다.
- Aside MCP·Chrome·Firecrawl·WebFetch 등 다른 브라우저/웹 도구로 바꾸지 않는다. ego lite가 실패하면 그 시점에서 멈추고 실패 내용(CLI 오류/연결/로그인 구분)을 보고한다.
- Ego Lite 업데이트 안내가 떠도 `ego-browser upgrade`를 실행하지 않는다.
- 젠 소유 탭(`openedBy: "unknown"`)은 닫거나 이동시키지 않는다. 끝나면 직접 연 Page만 닫고 `task.finish()` 방식은 안내서를 따른다(공간 유지 여부는 기본값).
- Suno 로그인이 안 되어 있으면 로그인을 시도하지 말고 멈추고 보고한다.

## 할 일
1. 작업공간 URL을 새 탭에서 연다. 화면에 보이는 작업공간 이름을 정확히 기록한다(예상: `[23:00]` 비슷한 이름 — 다르면 다른 대로 기록).
2. 작업공간의 곡 목록 전체를 기록한다: 화면 제목, 곡 ID(`/song/<id>`), 길이, 모델 표시, 공개 여부 표시, 리믹스/커버/확장 표시.
3. 9곡 이름과 대조한다. 같은 이름의 버전이 여러 개면 **모두** 기록하고 어느 것을 고르지 않는다. 9곡 외 다른 곡이 있으면 "추가 곡"으로 기록하고, 9곡 중 못 찾은 곡은 "없음"으로 기록한다.
4. 목록의 모든 곡(9곡 관련 전부 + 추가 곡)의 상세 화면에서 아래를 **원문 그대로** 수집한다. 접힌 글은 "더 보기"를 펼쳐 전체를 읽는다.
   - 스타일 전문(Styles). 특수 하이픈 `‑`(U+2011)과 일반 하이픈 `-`를 구분해 그대로 보존한다.
   - Exclude(제외 스타일) 칸이 따로 보이면 그 전문. 안 보이면 `null`과 "확인 위치"를 적는다.
   - 가사 전문(대괄호 지시 포함, 줄바꿈 보존).
   - 출처 관계: 커버/리믹스/확장의 원곡 제목·ID가 보이면 기록.
   - 길이, 모델, 페르소나, 보이는 고급 설정(Weirdness·Style Influence·Variety 등).
5. 각 스타일에서 계산만 한다(고치지 않는다):
   - `style_characters`(Python `len`), `style_sha256`(UTF-8).
   - `inline_negative_terms`: 스타일 안에서 `‑` 또는 `-`로 시작하는 쉼표 구분 항목 목록(기호 포함 원문 그대로).
   - `style_without_negative_terms`: 위 항목을 뺀 나머지(쉼표·공백만 정리, 단어·순서 불변).
6. 스타일 문자열이 완전히 같은 곡끼리 묶어 `identical_style_groups`에 적는다(정확히 같은 경우만).

## 금지 (크레딧·데이터 보호)
- 생성·Create 버튼·재생성·커버/리믹스 실행·확장 금지(크레딧 사용 금지).
- 제목·가사·스타일 편집, 공개/비공개 변경, 이동, 삭제, 좋아요, 다운로드, 작업공간 설정 변경 금지.
- 만들기 입력창에 글자 입력 금지. 재생은 필요 없으니 하지 않는다.
- 이 저장소에 커밋·푸시하지 않는다. 아래 출력 폴더 밖 파일을 만들거나 고치지 않는다.

## 출력 (모두 `~/Project/wavvy/.ai/research/2026-11-01-2300-nine-tracks/`)
- `raw/` — 곡별 원시 화면 글(예: `NN-<id앞8자>-detail.txt`), 목록 화면 원시 글.
- `nine-tracks.json` — 아래 선례와 같은 꼴: `observed_at_write_utc`, `workspace`(화면 이름), `workspace_id`, `browser`, `track_count_observed`, `tracks[]`(곡마다 `title_ui`, `matched_name`(9곡 중 어느 이름인지 또는 null), `id`, `url`, `duration_ui`, `model_ui`, `style_full`, `style_characters`, `style_sha256`, `inline_negative_terms`, `style_without_negative_terms`, `exclude_field_observed`, `lyrics_full`, `lineage`, `settings_observed`, 각 항목의 근거 raw 파일), `identical_style_groups`, `missing_names`, `extra_tracks`, `limitations`.
- `styles-verbatim.txt` — 곡별 제목 + 스타일 전문만 모은 글.

## 선례
- `.ai/research/2026-10-26-1930-six-tracks/six-tracks.json` · `styles-verbatim.txt` · `raw/` — 같은 종류의 Suno 읽기 전용 수집. 필드 이름과 근거 기록 방식을 따른다.

## 보고 (마지막 메시지)
1. 작업공간 이름, 관측 곡 수, 곡 목록(제목·ID·길이).
2. 9곡 대조 결과(이름별 버전 수, 없음, 추가 곡).
3. 곡별 스타일 글자 수와 `‑` 항목 개수, Exclude 칸 관측 여부.
4. 같은 스타일 묶음.
5. 이상한 점·확인 못 한 것(추측하지 말고 "미확인"으로).
6. 닫은 Page(직접 연 것만)와 ego lite 사용 증거(spaceId·명령) 위치.
