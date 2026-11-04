# 23:00 업로드 준비 — 문안 확정 반영 · 가사 원문 기록 · 시간 자막

배정: 규모=큼 · 복잡도=큼 · 중요도=큼

작성: 2026-11-04 Claude 오케스트레이터. 실행: sonnet-xhigh-worker. 저장소: `~/Project/wavvy` (아래 상대경로 기준). 직전 단계 결과: `.ai/plans/2026-11-04-2300-video-production.md`의 렌더 완료(`output/final.mkv` 6654초, report 17곡×2회, verify-release PASS).

## 젠 지시와 결정

- 「좋아. 업로드 하자. 바로 등록」 (2026-11-04) — 오케스트레이터가 채팅으로 보여 준 설명·태그 초안을 승인하고 업로드를 지시했다.
- 자막 순서 질문에 젠 답: **「자막 먼저 만들고 공개」**. 그래서 이번 단계는 1시간 넘는 보컬 영상의 시간 자막을 만들고 `upload-ready` 게이트를 통과시키는 데까지다.
- **이번 단계 범위 밖**: YouTube 업로드·Studio 조작·공개·댓글, Suno 조작, git commit·push. 업로드는 오케스트레이터 확인 뒤 다음 단계에서 한다.

## 먼저 읽을 것

`MASTER/cli/SPEC.md` §4·§5(prepare-subtitles·verify-subtitles·finalize-upload·playback-order 문단), `MASTER/youtube/YOUTUBE.md` §7·§9.2, `skills/wavvy-youtube-publish/SKILL.md` 1–2단계, `skills/wavvy-youtube-publish/references/timed-subtitles.md` 전체, `SERIES/23-00/concept.md`, `SERIES/23-00/production/browser-capture-20261104/style-provenance.{json,md}`.

## 선례

- **17:30 시간 자막(2026-10-23)**: `SERIES/17-30/input/subtitles.json`, 확인된 시간표 `SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.json`, 음성 근거 `.../audio-probe/*-whisper.json`, 검사 기록 `all-tracks-timed-checked-validation.json`. 곡별 Whisper 단어 시각으로 승인 가사 줄을 실제 노래 구간에 맞췄고, 반복 후렴은 실제 음성 근거가 있을 때만 추가 등장으로 넣었다. 이번에도 같은 구조를 따른다.
- **17:30 가사·순서 기록**: 녹음으로 확보한 곡과 기존 txt 번호가 다를 때 `input/playback-order.json`으로 재생번호·원번호·선택 ID·WAV 해시·가사 관찰을 묶었다(SPEC §5 마지막 문단들). 23:00도 하네스가 요구하는 형태를 이 선례에서 고른다.

## 오케스트레이터가 이미 확인한 사실

- 17곡 모두 Suno 곡 화면에서 가져온 가사 원문이 `style-provenance.json`의 `tracks[].remix.lyrics_raw`와 `lyrics_raw_sha256`으로 저장돼 있다. 이 가사가 **승인 가사**다(젠이 Suno에 넣은 각 곡의 가사). 새 가사를 쓰거나 고치지 않는다.
- 같은 파일의 스타일 기록은 원곡 연결 확인 3곡 / 가사 일치 원곡 후보 8곡(잠정) / 젠 직접 제작 6곡으로 나뉜다. 잠정 연결을 확정으로 올리거나 없는 원곡 문구를 지어내지 않는다.
- `finalize-upload --check` 현재 결과: `Missing txt source for report track(s): 돛, 한 잔만 더, 비가 그쳤네, 손 잡아도 될까, 지금 가는 길, 나도 네가 신경 쓰여, 자꾸 네가 신경쓰여, 약속`. 나머지 9곡은 `input/tracks/`의 옛 초안 txt(11/1 관찰한 같은 리믹스)와 제목으로 이어져 있다.
- 로컬에 Whisper 계열 도구가 없다(`whisper`, `faster_whisper`, `mlx_whisper` 모두 없음).

## 할 일

### 1. 승인 설명·태그 반영
concept의 YouTube 문안 절과 `output/upload.csv`의 설명·태그를 아래 승인 문안으로 바꾼다. 제목은 이미 반영된 승인 제목 그대로다. 곡 목록 34줄은 지금 upload.csv에 있는 보고서 기반 줄(`00:00 - 1. 작은 빛` … `55:27 - 1. 작은 빛 (반복)` … `01:48:41 - 17. 물결 (반복)`)을 그대로 쓴다. concept에 승인 원문(「좋아. 업로드 하자. 바로 등록」, 2026-11-04)을 남기고, 설명·태그를 "초안"에서 "승인"으로 바꾼다. 워커가 앞 단계에서 쓴 고정 댓글 초안은 **미승인 초안**으로 남겨 두고 게시하지 않는다. `upload.csv`는 앞 단계처럼 하네스 `generate_upload_csv`로 다시 만든다(렌더 재실행 없음). 그 뒤 `verify-release` PASS 확인.

설명(곡 목록 자리만 실제 34줄로 채움):

```
☕ 23:00, 커피 한 잔과 바람, 그리고 밤의 그루브
우리말 가사의 Lo-fi Pop과 R&B - Wavvy

늦은 밤 커피를 한 잔 내리고,
창문을 조금 열어 선선한 바람을 들이고,
턴테이블 위 음악에 맞춰 고개를 까딱이며
남은 일을 하나씩 정리해 가는 시간.

가게 문을 닫기 전 마지막 손님을 배웅하고,
불 켜진 창밖 도시를 잠깐 바라보다
다시 키보드 위로 손을 올리는 밤.

느긋하게 흔들리는 그루브를 따라
오늘의 남은 시간이 조금 더 가볍게 흘러가길 바라요.

──────────────
🎵 Track List
<1회차 17줄>

🔁 Repeat
<2회차 17줄>

──────────────
Music for your space, 24 hours a day.
All tracks feature Korean lyrics.

🎵 Music: Wavvy
Copyright Ⓒ Wavvy. All rights reserved.

──────────────
#lofipop #rnb #노동요 #카페음악 #매장음악 #한국어가사
#playlist #플리 #wavvy #웨이비
```

태그:

```
lofi pop, lo-fi pop, rnb, r&b, lofi rnb, korean rnb, korean lofi, late night playlist, night cafe music, cafe music, work music, store music, 노동요, 카페음악, 매장음악, 작업음악, 밤플리, 로파이, 알앤비, 한국어가사, korean lyrics, playlist, 플리, wavvy, 웨이비, 23:00
```

### 2. 가사 원문 기록 (Final Track Sources)
- 17곡 모두 현재 Suno 기록(`style-provenance.json`)을 출처로 하는 txt 원문을 만든다. 가사는 `remix.lyrics_raw` 그대로(해시 대조), 스타일·EXCLUDE는 같은 파일의 현재 기록 그대로이고, 잠정·직접 제작 구분과 `actual_generation_input_verified` 값을 txt 머리나 순서 기록에 보존한다.
- 옛 초안 txt 20개와 새 txt가 같은 폴더에서 제목·번호로 충돌하면, 옛 txt는 `input/source-history/2026-11-02-historical-20-draft/`로 **옮긴다(삭제 금지)**. 옮긴 목록·해시는 그 폴더의 `moved-manifest.json`에. 옛 9곡 txt의 가사가 현재 Suno 가사와 다르면 차이를 기록하고 현재 Suno 가사를 쓴다.
- 하네스가 요구하는 연결(필요하면 17:30식 `input/playback-order.json`)을 만들고 `python3 wavvy.py finalize-upload SERIES/23-00 --check` PASS → `python3 wavvy.py finalize-upload SERIES/23-00 --keep-txt`로 concept의 Final Track Sources를 채운다.
- `python3 wavvy.py prepare-subtitles SERIES/23-00`로 시간 표시 없는 가사 원문 자막을 먼저 만든다(SPEC §5).

### 3. 시간 자막
- Whisper 계열 음성 인식 도구를 **저장소 밖 격리 환경**(예: `work/2026-11-04-2300-subtitles/venv` — `work/`는 Git 무시 경로인지 먼저 확인 — 또는 스크래치패드)에 설치한다. 한국어 정확도가 충분한 모델(large 계열)을 쓰고, 단어 시각을 켠다. 설치한 패키지·버전·모델 이름을 기록한다. 전역 Python에 설치하지 않는다.
- `input/tracks/`의 17개 WAV마다 단어 시각 JSON을 만들고 `SERIES/23-00/input/validation/2026-11-04-timed-subtitles/audio-probe/`에 보존한다(17:30과 같은 위치 구조).
- `timed-subtitles.md` 규칙대로 시간표를 만든다: 승인 가사 줄만 쓰고(인식 결과 글자로 가사를 바꾸지 않음), 실제 노래 구간에 붙이고, 긴 간주를 가로질러 보간하지 않고, 반복 후렴은 실제 음성 근거가 있을 때만 추가 등장으로 넣는다(`allowed_added_source_lines_per_pass`·`required_extra_occurrences`·`repeat_evidence`). 약한 줄은 짧은 구간을 다시 인식해 확인하고 그 근거도 보존한다. `[Intro]`·`instrumental` 같은 지시어는 자막에 넣지 않는다.
- `input/subtitles.json` 작성 → `python3 wavvy.py prepare-subtitles SERIES/23-00 --timing-map <확인된 시간표>` → `python3 wavvy.py verify-subtitles SERIES/23-00 --stage prepared --json` PASS.
- 자체 점검: 큐 번호 연속, 시간 겹침 없음, 영상 길이 안, 각 큐 길이가 읽을 만한지, 2회차 큐가 1회차와 같은 글자이고 보고서의 실제 2회차 시작 오프셋을 따르는지. 점검 결과를 `.../2026-11-04-timed-subtitles/`에 남긴다. 사람이 들어 본 것처럼 쓰지 않는다(인식 기반 추정임을 표시).

### 4. 게이트
`python3 wavvy.py verify-release SERIES/23-00 --json`, `python3 wavvy.py gate SERIES/23-00 --stage source-final --json`, `--stage render-final`, `--stage upload-ready --json`, `python3 wavvy.py state SERIES/23-00 --check --json`. 모두 PASS가 목표다. 원시 출력을 `production/video-production-20261104/gates/`에 날짜·단계 이름으로 남긴다.

### 5. 기록
concept(Series Status·Final Track Sources·자막·문안 승인), `.ai/SESSION.md`·`.ai/HANDOFF.md`의 `<!-- 2300-video-current -->` 블록 갱신(다른 블록은 건드리지 않음), `CHANGELOG.md` `[Unreleased]` 첫 항목. state는 하네스 정상 writer로만, 단계 이름은 하네스 정의를 따른다.

## 멈추고 보고할 조건
- 어떤 곡의 승인 가사와 실제 노래가 크게 달라(여러 줄이 노래에 없거나 순서가 다름) 시간표를 만들 수 없을 때 — 그 곡과 증거를 보고.
- 하네스가 젠의 결정(곡·순서·가사 선택)을 요구할 때.
- 같은 원인으로 두 번 고쳐도 같은 실패가 날 때.

## 하지 말 것
- YouTube·Suno 조작, 업로드, 댓글, commit·push.
- 승인 가사·제목·설명·태그 글자 변경(위 승인 문안 반영만 허용).
- `output/final.mkv`·`report.json` 재생성, 렌더 재실행.
- `work/` 녹음 원본·썸네일·배경 이미지 수정, 과거 자료 삭제(옮기기만 허용), 다른 시리즈 수정.

## 보고 형식
단계별 PASS/FAIL과 원시 결과 경로, 옮긴 파일 목록, 가사 차이(옛 9곡 txt vs 현재 Suno), 설치한 도구·모델, 자막 큐 수·추가 반복 줄 수·약한 줄 처리 내역, 게이트 결과 요약, 바꾼 파일 목록.

## 기존 `tests/test_subtitles.py` 오류 13건 — 원인 · 고친 방법 · 결과 (2026-11-04, 젠 「고쳐줄래?」)

**원인.** `tests/test_subtitles.py`의 `SubtitleTests` 13건(`setUp`의 `_clone` → `shutil.copyfile(source, target)`)이 모두 같은 줄에서 실패했다. 오류 원문:

```
FileNotFoundError: [Errno 2] No such file or directory: '…/SERIES/17-30/input/validation/2026-10-23-timed-subtitles/report-at-subtitle-preparation.json'
```

`_clone`은 실제 시리즈 폴더 `SERIES/17-30/`에서 근거 파일 24개 + PNG 6개를 임시 폴더로 복사한다. 그 가운데 `report-at-subtitle-preparation.json`(보고서 사본, 240줄)은 커밋 `1154bb7`(2026-10-23)에 추가됐다가 `0861ddb`(2026-10-24 "chore: finalize 07:00 release and clean uploaded series artifacts")의 업로드 후 정리에서 지워졌다. 같은 해시(`a1a6e1c5…`)의 로컬 `SERIES/17-30/output/report.json`은 Git 무시 경로라 저장소에 남지 않는다. 즉 테스트가 업로드 후 정리로 지워질 수 있는 실제 시리즈 파일에 기대고 있었다. 나머지 2건(`NewSeriesSubtitleTests`)은 합성 데이터라 통과였다.

**고친 방법.** (b) 고정 사본 방식: 필요한 근거만 `tests/fixtures/subtitles_17_30/`에 Git 이력(커밋 `12ea5e2`, 보고서는 `1154bb7`)에서 바이트 그대로 꺼내 두고 `tests/fixtures/subtitles_17_30/README.md`에 파일별 커밋·경로·바이트·SHA-256을 적었다(24개, 1.9 MB). 시간표가 1.4 MB이지만 단언(큐 1270개, SRT 해시, 영상 ID, 줄 번호)이 이 실제 자료에 묶여 있어 합성(a)으로는 같은 동작을 확인할 수 없다고 봤다. 큰 미디어인 공개 화면 PNG 6개(15.2 MB)만 넣지 않았고, 하네스는 그 파일의 존재와 매니페스트 SHA-256만 대조하므로(픽셀을 읽지 않음) `_clone`이 작은 대역 파일을 쓰고 복제본 매니페스트의 해당 해시 6개만 다시 쓴다. `SOURCE` 상수와 `_clone` 외 테스트 본문·단언·`skip`은 바꾸지 않았다(수정 diff: 헤더 상수 + `_clone` + 보조 함수 `_publication_screenshots`).

**결과.** `python3 -m unittest tests/test_subtitles.py` 15건 OK(오류 0, 실패 0). `SERIES/`·`MASTER/` 없이 `tests/`·`wavvy_harness/`·`wavvy.py`만 복사한 임시 폴더에서도 `test_subtitles.py`와 `test_subtitle_timing_contract.py` 32건 OK. 전체 테스트 파일(`test_harness`·`test_integrated_premix`·`test_premixed_audio`·`test_subtitle_timing_contract`·`test_subtitles`·`test_video_artwork`·`test_youtube_titles`) 172건 OK. 원시 출력: `SERIES/23-00/input/validation/2026-11-04-timed-subtitles/harness-patch-checks/`(`unittest-test_subtitles-known-preexisting-failures.txt`는 고치기 전 13건 오류 원문, `unittest-test_subtitles-after-fixture-fix.txt`는 고친 뒤).
