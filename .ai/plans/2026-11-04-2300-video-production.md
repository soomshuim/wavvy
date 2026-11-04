# 23:00 본편 영상 제작 — 실행 지시서

배정: 규모=큼 · 복잡도=큼 · 중요도=큼

작성: 2026-11-04 Claude 오케스트레이터. 실행: sonnet-xhigh-worker. 저장소: `~/Project/wavvy` (아래 상대경로 기준).

## 젠 지시

「이제 영상 제작하자.」 (2026-11-04). 범위는 **4K 본편 영상 렌더까지**다. YouTube 업로드·공개·자막 게시·커밋·푸시는 범위 밖이다.

## 먼저 읽을 것

`AGENTS.md` → `.ai/state.json` → `MASTER/SSOT.md` → `MASTER/ai/RUNTIME_RULES.md` → `MASTER/cli/SPEC.md`(특히 Video artwork contract, §3 파일명, §4 validate/preview/pack, §6) → `MASTER/youtube/YOUTUBE.md` → `skills/wavvy-release/SKILL.md` 4단계 → `skills/wavvy-audio-ingest/SKILL.md` → `SERIES/23-00/concept.md` → `SERIES/23-00/production/browser-capture-20261104/{recordings.md,sequence.json,capture-manifest.json,measurement-method.md}`.

## 선례

- **17:30 (R&B 보컬, 2026-10-22 공개)**: 시스템 오디오 녹음 17곡 + 공식 다운로드 3곡을 표준 `pack`(0.8초 acrossfade · -14 LUFS · -1.0 dBTP · 2회 반복)으로 묶었다. 입력 3,874.85초 → 영상 7,718.5초. 녹음곡은 raw 녹음에서 곡 경계를 잘라 `input/tracks/NN__제목__Mood__Genre__NA.wav`로 넣었고, `input/download-manifest.json`에 `source_kind: system_audio_capture`, `raw_capture_path/sha256`, `trim_start_raw_seconds`, `trim_end_raw_seconds`, 경계 근거 ref, `capture_integrity_limit`를 남겼다. 항목 예시는 `SERIES/17-30/input/download-manifest.json`의 order 4를 그대로 본뜬다.
- **19:30 (2026-10-26)**: 젠 규칙 「영상에는 썸네일을 그대로 쓰지마. 생성한 4K 이미지를 써」「wavvy 로고만 박힌 버전을 써.」 → 하네스의 Video artwork contract(`input/video-background.png` + `input/video-artwork.json` + 시각 검수 JSON)로 집행 중. 썸네일 파일·바이트·픽셀과 같은 배경은 하네스가 거절한다.
- 23:00은 BPM 통일 믹스(07:00·19:30 방식)가 아니라 17:30과 같은 **표준 pack**을 쓴다. 젠이 BPM 변경을 요청한 적이 없다.

## 오케스트레이터가 이미 확인한 사실

- 확정 순서·Suno ID: `production/browser-capture-20261104/sequence.json` (1 작은 빛 … 17 물결). 원곡 재생 시간 합계 55:40.12.
- 녹음 파일: `work/2026-11-04-2300-browser-capture/captures/<suno-id>/attempt-01/{raw.wav,song-with-guards.wav}`. guard본은 추정 경계 앞 0.5초·뒤 0.75초 여유를 포함하고, 출력 지연은 측정하지 않았다(`measurement-method.md`).
- 썸네일: `SERIES/23-00/input/thumb.jpg`(3840×2160, sha256 f61cc78f…)·`thumb.png`(c23e92bf…) = 장면 + 로고 + 갈색 하단 문장. 제목 없음.
- 글자 없는 장면 원본: `production/artwork-final/scene-original-4k.png`(861513fa…). 로고 위치·크기·색은 `production/artwork-final/artwork.json`의 `logo`.
- 현재 thumb.png와 장면 원본의 차이는 로고(128,96 부근)와 하단 문장(`footer.pixel_difference_bbox` [128,2040,2787,2092])뿐이다.
- `input/tracks/`에는 지난 11/1–11/2 에이전트 초안 txt 20개가 있고, `input/suno-candidates.json`은 그 초안의 후보 장부다. concept는 이 둘을 **보존된 과거 자료, 현재 17곡 선택이 아님**으로 기록한다.
- 시각 검수 JSON의 `method`는 하네스가 문자열 `"view_image"`를 요구한다(`wavvy_harness/video_artwork.py`).

## 할 일

### 1. 과거 초안 자료 정리 (보존 이동)
현재 17곡 WAV와 섞이면 `validate`·`verify-release`가 과거 20곡 txt·후보 장부를 현재 선택으로 읽을 수 있다. 하네스 코드를 읽어 실제로 충돌하는 파일만 `input/source-history/2026-11-02-historical-20-draft/`로 **옮긴다(삭제 금지)**. 옮긴 목록·해시를 같은 폴더의 `moved-manifest.json`에 남기고 concept의 "Preserved earlier draft" 줄에 새 위치를 적는다. 충돌하지 않으면 옮기지 않는다.

### 2. 음원 넣기 (wavvy-audio-ingest)
- 17곡 각각 raw 녹음에서 곡 경계를 정한다. guard본의 여유 구간 안에서 실제 무음/소리 시작·끝을 측정(예: ffmpeg `silencedetect` 또는 RMS 임계)해 자르고, 잘린 길이가 원곡 재생 시간과 크게 다르면(±0.5초 초과) 그 곡에서 멈추고 보고한다. 곡 앞뒤에서 소리를 잘라 먹지 않는다.
- 파일: `SERIES/23-00/input/tracks/NN__<제목>__Relax__Lo-fi R&B__NA.wav` (NN = 두 자리 순서, 제목은 `(Lo-Fi Remix)` 없이 sequence의 곡 이름). 48 kHz 스테레오, 원래 샘플 형식 유지.
- `input/download-manifest.json`: 17:30 order 4 항목 형식 그대로 + `workspace: "[23:00]"`, `suno_ui_title`(현재 `N. 제목` 저장값), `candidate_id` = Suno ID, `capture_actor`(Codex via Aside MCP, 2026-11-04 — capture-manifest 기준), 경계 근거 ref(capture-manifest·capture-verifications 경로), 자른 방법. 각 WAV를 ffprobe로 재고 sha256을 적는다.

### 3. 본편 배경 (로고만)
- 현재 `input/thumb.png`에서 하단 문장 띠(y 2035–2100, 전체 폭)를 `scene-original-4k.png`로 복원해 `input/video-background.png`를 만든다. 사전 확인: 그 띠 안의 thumb↔장면 차이 bbox가 [128,2040,2787,2092] 안인지. 사후 확인: 새 배경↔장면 차이 bbox가 로고 영역 안뿐(하단·제목 영역 차이 없음), 3840×2160, thumb.jpg/png와 해시·디코드 픽셀이 다름.
- 직접 이미지를 열어 보고(Read 도구) 로고만 있고 제목·BPM·다른 문구가 없음을 확인한 뒤 `production/video-artwork-review.json`을 SPEC 형식으로 쓴다. `method`는 하네스 요구값 `"view_image"`, `reviewer`는 실제 관찰자(예: `Claude Sonnet 5.5 worker`), `evidence`에 실제로 본 내용과 사용 도구(Claude Read 이미지 보기)를 적는다.
- `input/video-artwork.json`을 SPEC 형식으로 쓴다(`origin: generated_scene`).

### 4. YouTube 문안 초안 (concept)
`MASTER/youtube/YOUTUBE.md`의 새 제목 기본형·설명·태그 규칙과 최근 시리즈(17:30·19:30 concept)의 형식을 따라 concept에 제목·설명·태그 초안을 쓴다. 장르는 relax alternative R&B / lo-fi R&B, 시간대 23:00. 제목은 **초안**으로 표시하고 젠 승인 대기로 적는다. 챕터 시작 시각은 렌더 보고서가 나온 뒤 채운다.

### 5. 검사·미리보기
`python3 wavvy.py validate SERIES/23-00` PASS → `python3 wavvy.py preview SERIES/23-00 --sec 30` → 미리보기에서 앞·중간·끝 프레임을 뽑아 직접 보고(로고만 보이는 배경, 3840×2160), ffprobe로 길이·스트림을 잰다. 소리가 나오는지(무음 아님) RMS로 확인한다.

### 6. 본 렌더
`python3 wavvy.py pack SERIES/23-00 -y` (기본값: 2회 반복·0.8초 acrossfade·-14 LUFS·-1.0 dBTP). 오래 걸리면 백그라운드로 돌리고 끝까지 기다린다. 끝나면:
- `output/final.mkv` ffprobe(3840×2160·H.264·FLAC·길이), `output/report.json`의 반복·트랙 시작 시각, `upload.csv`.
- 보고서 시작 시각으로 concept의 챕터(1회차 17 + 2회차 17)를 채우고 upload.csv와 맞춘다.
- `python3 wavvy.py gate SERIES/23-00 --stage source-final --json`, `render-final` 게이트(SPEC에 있으면), `python3 wavvy.py verify-release SERIES/23-00 --json`. 자막(1시간 넘는 보컬 영상의 시간 자막)·제목 승인처럼 업로드 단계에서만 필요한 실패는 실패 항목과 이유를 그대로 기록하고 고치려 하지 않는다. 그 밖의 실패는 원인을 고친다.
- 최종 영상 앞·중간(2회차 시작 부근)·끝 프레임을 뽑아 직접 본다.

### 7. 기록
- `python3 wavvy.py state SERIES/23-00 --check --json` 후 정상 writer(`state --write --phase <렌더 완료에 맞는 단계> --if-match <현재 revision>`)로 기록. 단계 이름은 하네스 정의에서 고른다.
- concept의 Series Status·Current artwork(본편 배경 추가)·문안·챕터, `.ai/SESSION.md`와 `.ai/HANDOFF.md` 맨 위에 `<!-- 2300-video-current:start -->`~`end` 새 블록(기존 블록은 건드리지 않음), `CHANGELOG.md` `[Unreleased]` 첫 항목.

## 멈추고 보고할 조건
- 곡 경계를 정할 수 없거나 잘린 길이가 원곡과 ±0.5초를 넘게 다를 때.
- 하네스가 요구하는 값이 젠의 결정(곡 제외·순서 변경·제목 확정·가사 원문 선택 등)을 필요로 할 때.
- 같은 실패를 두 번 고쳐도 같은 원인으로 다시 실패할 때.

## 하지 말 것
- YouTube 업로드·Studio 조작·Suno 조작·새 이미지/음악 생성.
- git commit·push.
- `work/` 녹음 원본 삭제·수정, `scene-original-*.png`·`input/thumb.*` 수정, 다른 시리즈 파일 수정.
- 과거 자료 삭제(옮기기만 허용).

## 보고 형식
단계별 PASS/FAIL과 실제 측정값(곡별 자른 구간·길이·해시 요약, 배경 diff bbox, 미리보기·최종 영상 ffprobe 값, 보고서 총 길이, 게이트 결과 원문 요약), 직접 본 프레임 그림 경로, 남은 업로드 전 의존성 목록, 바꾸거나 옮긴 파일 목록.
