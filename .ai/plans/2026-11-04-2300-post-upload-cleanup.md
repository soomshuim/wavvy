# 23:00 업로드 후 정리 — 실행 지시서

배정: 규모=큼 · 복잡도=큼 · 중요도=큼

작성: 2026-11-04 Claude 오케스트레이터. 실행: sonnet-xhigh-worker. 저장소 `~/Project/wavvy`(아래 상대경로 기준).

## 젠 지시

- 「작업에 쓰인 원본 영상등, 과정 파일들도 다 삭제. 이전 작업 정리 방식 히스토리 확인」 (2026-11-04)
- 범위 질문 「11/1~11/2에 에이전트가 만들었다가 채택되지 않은 옛 20곡 초안도 지울까요?」에 젠 답: **「지우기」**
- 23:00은 YouTube `wbJQ2WgfJn4`로 공개 완료(concept `## Upload Status`: `YouTube upload: completed`), state revision 105 `uploaded`, `gate --stage uploaded` PASS.

## 선례 (이 순서를 그대로 따른다)

- 19:30 최종 미디어 정리 `.ai/cleanup/2026-10-26-1930-final-media-cleanup-plan.md`와 같은 날 임시 정리 `2026-10-26-1930-temp-cleanup-*`, 실행기 `.ai/cleanup/execute-1930-final-media-cleanup-20261026.py`.
- 07:00·17:30 업로드 후 정리 `.ai/cleanup/2026-10-24-*-post-upload-*`, 마감 `2026-10-24-post-upload-cleanup-closeout.json`, 검토 `.ai/reviews/2026-10-24-1730-post-upload-cleanup-review.md`.
- 23:00 아트워크 과정 정리 `.ai/cleanup/2026-11-04-2300-artwork-cleanup.json`.
- 공통 순서: ① 전체 목록(inventory) → ② 지울 목록(candidates)·지킬 목록(protected)을 경로·sha256·장치·inode·바이트·mtime으로 고정 → ③ 변경 없는 미리 실행(dry-run) + 가상 삭제 사본에서 검사 → ④ **격리 검토 후 오케스트레이터의 적용 지시** → ⑤ 정확한 파일 단위 unlink(재귀 삭제 금지, 심볼릭 링크 따라가지 않음, 매 파일 해시·stat 재확인, 열린 파일 lsof 확인, 이벤트 기록, 실패 즉시 멈춤) → ⑥ 지킬 파일 불변·지울 파일 부재·uploaded 게이트 PASS·여유 공간 전후 → ⑦ 기록.
- 선례의 보존 원칙: 최종 썸네일·원본 그림·PSD/JPG/PNG, 가사·스타일 원문, 최종 선택·제작·렌더·게시 기록, 실제 게시 자막과 그 근거, 검사·검토·정리 기록은 남긴다. 미디어·임시 실행 환경·중간 시안·실패 기록·과정 문서는 정리한다.

## 지울 것 (후보 — 실제 목록은 ① 결과로 고정)

A. **미디어**: `work/2026-11-04-2300-browser-capture/` 전체(녹음 원본·가드본·탐침·진단 실행 파일·로그), `SERIES/23-00/work/` 전체(pack 임시), `SERIES/23-00/input/tracks/*.wav` 17개, `SERIES/23-00/output/final.mkv`, `output/preview.mp4`, 그 밖에 이번 작업이 만든 음원·영상 파일.
B. **옛 20곡 초안(젠 「지우기」)**: `SERIES/23-00/input/source-history/` 아래 네 폴더 전부, `input/suno-candidates.json`, `input/validation/2026-11-01-generation/`, `input/validation/2026-11-02-regeneration/`, `.ai/lyrics/2026-11-01_23-00_*`, `.ai/research/2026-11-01-2300-nine-tracks/`, `.ai/plans/2026-11-01-2300-*`, `.ai/plans/2026-11-02-2300-*`. concept의 옛 초안 절(`## Historical 20-song draft …` 이하의 옛 결정·Type Styles·Original Styles 등 옛 초안 전용 절)은 지우고, 그 자리에 「옛 20곡 초안 자료는 2026-11-04 젠 「지우기」로 삭제, 복원은 git 커밋 `791bea1` 이전 기록」 한 줄을 남긴다. 단 `## Final Track Sources`·`## YouTube Metadata`·`## Upload Status`와 현재 17곡 관련 절은 건드리지 않는다.
C. **과정 파일**: 이번 작업의 실패·대체된 기록(예: `production/video-production-20261104/gates/`의 `*unpatched*`·`verify-release-baseline-before-selection-file.json`), 최종본과 바이트가 같은 중복 사본(예: 자막 검증 폴더의 `candidate-youtube_subtitles_ko_timed_estimated.srt` — **단 `input/subtitles.json`이나 다른 보존 기록이 경로·해시로 묶고 있으면 보존**), 적용 끝난 `proposed-harness-patch-subtitles.diff`, `__pycache__`, 완료된 단기 계획 `.ai/plans/2026-11-04-2300-{browser-capture,video-production,subtitles-upload-prep,youtube-upload}.md`(지우기 전에 SESSION/HANDOFF 현재 블록·CHANGELOG·concept 안의 이 파일 링크를 「커밋 `791bea1`의 계획 문서」 표기로 바꾼다), `production/browser-capture-20261104/` 안의 미완료·진단 시도 기록 중 보존 기록이 참조하지 않는 것.
D. **세션 임시 파일(저장소 밖)**: `/private/tmp/claude-501/-Users-zenkim-office-Project-wavvy/9f0bef40-3db1-46d4-9c34-092b5b9edf95/scratchpad/` 아래 이번 작업 하위 폴더·파일 전부(백업·확인 그림·스크립트·watch.html 등). `~/Downloads/captions.srt`는 sha256이 자막 게시 근거 폴더의 보존 사본과 같을 때만 후보로 넣는다.

## 지킬 것 (보호 — 해시 고정)

- `SERIES/23-00/concept.md`(B의 문서 수정 외), `input/thumb.jpg`·`thumb.png`·`video-background.png`·`video-artwork.json`, `production/artwork-final/*`, `production/video-artwork-review.json`.
- `input/tracks/*.txt`, `input/suno-current-sources-2026-11-04.json`, `input/suno-final-selection-2026-11-04.json`, `input/download-manifest.json`, `input/subtitles.json`과 그것이 경로·해시로 묶는 모든 파일(시간표·`audio-probe/`·게시 근거·SRT·`output/report.json`), `input/validation/2026-11-04-*`의 보존 기록·스크립트.
- `output/report.json`·`upload.csv`·`provenance.md`·두 자막 파일.
- `production/browser-capture-20261104/`의 출처 기록(sequence·style-provenance·capture-manifest·source-catalog·suno-ui·measurement-method·handoff-verification·review·스크립트), `production/video-production-20261104/`의 PASS 기록·컷 검증, `production/youtube-upload-*`.
- 저장소 코드·테스트·fixture·`.venv/`·`requirements-whisper.txt`·MASTER·skills, `.ai/` 기록(SESSION·HANDOFF·reviews·inbox-reviews·cleanup·research/2026-11-04-youtube-upload-defaults), 다른 시리즈 전부, Whisper 모델 캐시, CDS·다른 프로젝트.
- 실제로 묶인 의존은 코드(`wavvy_harness/*`)와 manifest를 읽어 확인한다. 이름만 보고 판단하지 않는다.

## 할 일

1. ①② 목록을 만들고 `.ai/cleanup/2026-11-04-2300-post-upload-cleanup-{inventory,candidates,protected}.json`과 `-plan.md`(지울 개수·바이트, 지킬 개수, 분류 근거, 애매해서 보호로 둔 항목)를 쓴다. 실행기 `.ai/cleanup/execute-2300-post-upload-cleanup-20261104.py`는 19:30 실행기 구조를 따른다(기본 실행은 변경 없음, `--apply`일 때만 삭제).
2. ③ dry-run: 실행기 기본 실행 + 저장소를 임시 폴더로 복사해 후보를 뺀 사본에서 `gate --stage uploaded`, `verify-subtitles --stage prepared`·`--stage published`, `state --check`, 테스트 파일 7개(`tests/*.py`를 이름으로 나열) 실행. 원시 출력은 `.ai/cleanup/2026-11-04-2300-post-upload-cleanup-dry-run*.json`.
3. **여기서 멈추고 보고**한다. 오케스트레이터가 격리 검토를 받은 뒤 적용을 지시한다.
4. (적용 지시 후) ⑤⑥ 실행 → `state --write`(필요하면, `--if-match` 현재 revision) → uploaded 게이트·자막 검사 2단계 PASS 확인 → 마감 기록 `-closeout.json`(삭제 개수·바이트·여유 공간 전후·보호 불변·대상 부재·게이트), concept `## Local Retention`(또는 기존 보관 절) 갱신, CHANGELOG 항목.

## 하지 말 것
- 재귀 삭제, 와일드카드 일괄 삭제, 목록 밖 파일 삭제, 다른 시리즈·프로젝트·Git 내부·`.venv`·모델 캐시 건드리기.
- YouTube·Suno 조작, git commit·push(오케스트레이터가 한다).
- 열린 파일이 쓰기 상태로 잡혀 있으면 그 파일 건너뛰지 말고 멈춰서 보고.

## 보고 형식
지울 개수·바이트(분류 A~D별), 지킬 개수, 애매해서 보호로 둔 항목과 이유, dry-run·가상 삭제 검사 결과, 기록 파일 경로. (적용 뒤) 실제 삭제 결과·보호 불변·게이트·여유 공간.
