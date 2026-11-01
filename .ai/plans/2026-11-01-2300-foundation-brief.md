배정: 규모=작음 · 복잡도=큼 · 중요도=큼

# 브리프 A — 23:00 시리즈 기반 만들기 (concept · 기존 리믹스 9곡 원고 · Exclude 예외 검사)

## 배경과 확정 사항 (젠 원문 2026-11-01 — 바꾸지 않는다)
- 시리즈: **23:00**, 폴더 `SERIES/23-00/`. 컨셉: relax alternative R&B, lo-fi R&B. Suno 작업공간 `[23:00]` (`f578d3c2-f43f-462e-8e05-44d022edd480`).
- 20곡 = 젠이 만든 기존 곡의 lo-fi 리믹스 9곡 + 새 11곡. 「넘버링은 나중에 일괄로 할게」 — 번호는 임시다.
- 「url에서 9곡의 가사 컨셉과 특징, 스타일 프롬프트(그대로 활용)를 각 타입 별로 참고해서 나머지 11곡을 새로 만들어야해.」 → 9곡 스타일이 모두 달라 곡마다 한 타입(9타입).
- 「물결만 원본 트랙의 스타일 프롬프트 + Modern Indie R&B, Lo-fi Remastered, Articulation 를 붙여줘.」 + 「- 붙은 스타일은 exclude인거 알지?」 → 물결 타입: 젠이 준 원본 스타일에서 `‑` 항목을 뺀 앞부분 + `, Modern Indie R&B, Lo-fi Remastered, Articulation` = STYLE, `‑` 항목 13개 = EXCLUDE.
- Exclude 13개 처리 질문에 젠 선택: 「13개 모두 유지 (추천)」 — 검사 도구에 "젠이 준 원본에서 온 항목이면 8개를 넘어도 출처를 기록하고 통과" 예외를 추가.
- 템포·조성·성별이 없는 스타일 질문에 젠 선택: 「선례처럼 끝에 덧붙이기」 — 새 곡 STYLE = 타입 스타일 원문 + (없는 것만) `, NN BPM, X Major|Minor, male|female vocal` 를 끝에 덧붙임. 선례: `.ai/lyrics/2026-10-02_17-00_12_서점-full-draft.md` Source Map.
- 가사(새 곡): 따뜻한 그리움 — 슬픔보다 아련함·따뜻함, 옛 기억에 위로받는 릴랙싱, 분위기·감각 디테일. 제목: 한국어 한 단어(명사·형용사·부사).
- 레퍼런스: 작업공간의 기존 9곡 리믹스가 레퍼런스다. 외부 레퍼런스 곡은 받지 않았다.
- 브라우저: ego lite(`MASTER/ai/RUNTIME_RULES.md` Browser Connection).

## 입력 자료 (원문 출처 — 이 파일들만 근거로 쓴다)
- `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` (9곡: `title_ui`, `id`, `url`, `duration_ui`, `style_full`, `lyrics_full`, `lineage` 등), `styles-verbatim.txt`, `raw/`.
- 물결 원본 스타일(젠이 채팅에 붙여 준 글, 터미널 줄바꿈만 빈칸 하나로 이은 것 · `‑`는 U+2011):
```
Korean Indie Alt R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal, ‑Falsetto, ‑Airy, ‑Whisper, ‑Breathiness, ‑Growl, ‑Vibrato, ‑Opera, ‑Dramatic, ‑Harmonized, ‑Backing vocals, ‑Choir, ‑Intense, ‑Mumbled
```
  → 물결 타입 STYLE(677자 예상): 위에서 `, ‑Falsetto … ‑Mumbled` 제거 + `, Modern Indie R&B, Lo-fi Remastered, Articulation`. EXCLUDE: `Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled`(기호 없이). 글자 수를 직접 재서 기록한다.

## 할 일
### 1. `SERIES/23-00/concept.md` (시리즈 컨셉 brief — 미채택 최종 소스를 넣지 않는다)
- 선례 형식: 최근 시리즈 concept(`SERIES/17-00/concept.md`, `SERIES/17-30/concept.md`)의 머리말·Series Status·Series Overrides 구성을 따른다. `wavvy.py validate`/`state`가 요구하는 필수 절이 있으면 `MASTER/cli/SPEC.md`·`MASTER/SSOT.md`·`wavvy_harness/` 코드로 확인해 맞춘다.
- 담을 것: 위 확정 사항(젠 원문 인용 포함), 레퍼런스 결정, 언어(한국어 가사), 보컬 기본값, 번호 임시 표시, 브라우저.
- `## Type Styles` 절: 9타입 각각 — 타입 이름(곡 제목), 원곡 Suno ID, 원문 STYLE(물결은 위 조립본, 나머지는 `nine-tracks.json`의 `style_full` 그대로), EXCLUDE(물결만 13개, 나머지 비움), 원문에 있는 BPM/조성/성별 표시(있음/없음), 출처 줄. 물결은 "작업공간 표시 스타일(185자)과 다름 — 젠 지시로 원본+3단어"를 적는다. 골목 원문에 "Keep the original song's melodic contour and section flow"가 있다는 사실을 메모로 적는다(문구는 그대로 둔다).
- `## Track Map` 절: 01~09 기존 리믹스(작업공간 순서: 먼지, 산책, 숨, 이름, 마음 밖, 물안개, 골목, 물결, 작은 빛), 10~20 "새 곡 — 설계표 젠 확인 대기"로 자리만 둔다.
### 2. 기존 리믹스 9곡 원고 txt — `SERIES/23-00/input/tracks/NN_<제목> (Lo-Fi Remix).txt` (01~09)
- 선례 형식: `SERIES/17-00/input/tracks/01_서랍 (Acoustic Remix).txt` 머리말(Track/Order/Status/BPM/Key) + `=== STYLE ===`/`=== EXCLUDE ===`/`=== LYRICS ===`. Status에 "user-provided lo-fi remix source; Suno ID …; audio not measured" 와 Suno URL을 적는다.
- STYLE·LYRICS는 작업공간 화면 원문 그대로(`style_full`·`lyrics_full`, 물결도 화면 표시 185자 그대로 — 이 원고는 기존 곡 기록이다). EXCLUDE는 비운다(화면에 Exclude 칸 미관측). BPM/Key/Vocal은 원문에 있으면 "prompt wording; not measured", 없으면 `unknown`.
- 이 9개에는 새 초안 track-prompt 게이트를 적용하지 않는다(`MASTER/WORKFLOWS.md` §1 3단계: 기존 사용자 제공 리믹스 원문에는 소급 적용 안 함).
### 3. Exclude 예외 — 검사 도구
- `wavvy_harness/gate.py` `_track_prompt_gate`의 `exclude_budget`: EXCLUDE가 8개를 넘으면 지금처럼 FAIL. 단, txt 머리말에 `Style Type: <타입 이름>`과 `Exclude Source: user-supplied type style` 줄이 있고, 같은 시리즈 `concept.md`의 `## Type Styles`에 그 타입의 EXCLUDE 항목이 **txt EXCLUDE 항목과 순서까지 정확히 같으면** PASS로 하고 detail에 `N/8 terms; user-supplied type exception (<타입>)`을 남긴다. 타입이 concept에 없거나 항목이 다르면 FAIL과 이유.
- 파싱은 기존 `parse_track_source_fields`·metadata 흐름을 재사용한다. 새 추상화·설정값을 만들지 않는다.
- 테스트(`tests/test_harness.py`): ① 예외 PASS ② 머리말 없음 FAIL ③ concept 항목 불일치 FAIL ④ concept에 타입 없음 FAIL ⑤ 8개 이하 기존 동작 유지. 기존 테스트 스타일을 따른다.
- 규칙 문서: `MASTER/style/STYLE.md` §3 Exclude 예산 줄에 예외 한 줄(근거: 2026-11-01 젠 선택)을 더한다. 다른 문서에 복제하지 않는다.
### 4. 공식 상태 기록
- `MASTER/cli/SPEC.md`의 `state` 사용법대로 `python3 wavvy.py state SERIES/23-00 --check --json`을 먼저 보고, 새 시리즈를 활성으로 기록하는 공식 writer 경로(`--write`, 현재 revision으로 `--if-match`)가 맞는 phase를 추론하는지 확인한 뒤 기록한다. 맞는 phase가 불분명하면 기록하지 말고 보고한다.

## 검증 (원시 출력을 `.ai/validation/2026-11-01-2300-foundation/`에 저장)
```bash
cd ~/Project/wavvy
python3 -m py_compile wavvy.py wavvy_harness/*.py
python3 -m unittest tests/test_harness.py
python3 wavvy.py doctor --json
python3 wavvy.py validate SERIES/23-00 --json   # 실패 항목이 "아직 없는 산출물" 때문이면 그 사실을 분리해 적는다
python3 wavvy.py state SERIES/23-00 --check --json
git diff --check
```
- 9개 리믹스 txt의 STYLE/LYRICS가 `nine-tracks.json` 원문과 바이트 동일함을 스크립트로 대조한 결과를 저장한다.
- 물결 타입 STYLE 글자 수·sha256과 EXCLUDE 13개 목록을 저장한다.
- 예외 검사 시연: 임시 txt(물결 타입 STYLE + 13 Exclude + 머리말 두 줄, 가사는 빈 자리표시 아님 — 짧은 한국어 가사)를 scratch 시리즈 사본이 아니라 **테스트 안에서** 만들어 PASS/FAIL을 확인한다. 실제 `SERIES/23-00/input/tracks/`에는 01~09만 만든다.

## 금지
- 새 곡(10~20) 원고·가사를 쓰지 않는다(설계표 젠 확인 대기). 커밋·푸시 금지. 브라우저를 열지 않는다.
- `.ai/research/2026-11-01-2300-nine-tracks/`는 읽기만 한다. 다른 시리즈·이력 파일을 바꾸지 않는다.
- 사용자 제공 원문(STYLE·LYRICS)을 고치거나 다듬지 않는다.

## 선례
- `SERIES/17-00/concept.md`, `SERIES/17-00/input/tracks/01_서랍 (Acoustic Remix).txt` — 사용자 리믹스 + 새 곡 혼합 시리즈의 concept·원고 형식.
- `.ai/lyrics/2026-10-02_17-00_12_서점-full-draft.md` — 리믹스 STYLE 재사용 + BPM·Key만 덧붙인 새 곡.
- `wavvy_harness/gate.py` `verse_structure_exception` — 기록된 사유가 있을 때만 기본 검사를 예외 처리하는 기존 방식.

## 보고
1. 만든/바꾼 파일 목록과 요약.
2. 물결 타입 STYLE 글자 수·sha256, EXCLUDE 13개.
3. 검증 명령 원시 결과 요약(테스트 수·통과, validate/state 결과와 실패 이유 분류).
4. 9개 원고 원문 대조 결과.
5. 상태 기록 여부(revision 전후)와 이유.
6. 미확인·판단 필요 사항.
