# 23:00 업로드 후 정리 — 고정 계획 (2026-11-04)

작성: sonnet-xhigh-worker, 브리프 `.ai/plans/2026-11-04-2300-post-upload-cleanup.md` 1~3단계. **여기서 멈춤.** 삭제·이동·편집은 하나도 하지 않았다(새 기록 파일만 `.ai/cleanup/`에 썼다). 저장소 HEAD `c966a62`, 공개 영상 `wbJQ2WgfJn4`.

## 1. 결정이 필요한 사안 (멈춘 지점)

브리프 A의 「`input/tracks/*.wav` 17개」를 그대로 지우면 **uploaded 게이트와 `state --check`가 새로 FAIL**한다(브리프 ⑥의 「uploaded 게이트 PASS」와 충돌). 가상 삭제 사본의 원시 결과:

| 확인 | 원본 그대로 | 브리프 목록 전부 지움(`removed`) | WAV 17개만 남기고 나머지 전부 지움(`keepwav`) |
|---|---|---|---|
| `gate --stage uploaded` | PASS (exit 0) | **FAIL (exit 1)** | PASS (exit 0) |
| `state --check` | PASS (exit 0) | **FAIL (exit 1)** | PASS (exit 0) |
| `verify-subtitles --stage prepared` | PASS (exit 0) | PASS (exit 0) | PASS (exit 0) |
| `verify-subtitles --stage published` | PASS (exit 0) | PASS (exit 0) | PASS (exit 0) |
| `validate` (참고) | exit 0 | **exit 1** | exit 0 |
| `verify-release` (참고) | PASS (exit 0) | **FAIL (exit 1)** | PASS (exit 0) |
| 테스트 7개 파일(172건) | 전부 OK | 전부 OK, 원본과 동일 | (같은 하네스 코드라 생략) |

- 새 FAIL의 원문(`removed`): `gate` blockers = `No audio files (MP3/WAV) found in: SERIES/23-00/input/tracks` · `source_final requires audio files in input/tracks or concept.md Track Selection source map`; `state --check` blocker = 뒤 문장 하나; `verify-release` = `missing audio for report tracks: 01__작은 빛__… ~ 17__물결__…`.
- 원인(코드 확인): `wavvy.py validate_project`는 premixed 시리즈가 아니면 `input/tracks`에 mp3/wav가 없고 `concept.md ## Track Selection` 원본 지도(compilation)도 없을 때 오류를 낸다. `wavvy_harness/state.py check_state`는 phase `uploaded`(`SOURCE_FINAL_PHASES`)에서 `available_audio_files <= 0`이면 `premixed_valid and uploaded`가 아닌 한 blocker를 낸다. `gate.py`의 `allow_uploaded_cleanup`은 premixed 분기에만 있다(19:30 시리즈가 PASS한 이유). 23:00은 `premixed_audio`·`selected_audio` 둘 다 opt-in이 아니다.
- 선례: 17:30 시리즈는 WAV를 지운 뒤 같은 FAIL이 났고 마감 기록이 「Pre-existing FAIL because source audio was already deleted」로 남겼다(`2026-10-24-post-upload-cleanup-closeout.json`). 23:00은 지금 PASS라서 **새로 생기는** FAIL이다.
- 선택지(결정은 오케스트레이터): (a) WAV 17개를 보호로 옮김 → 나머지 전부 정상(`keepwav` 열). 삭제 후보는 850개 / 6,356,923,986 B로 줄고 WAV 17개 1,282,664,596 B가 남는다. (b) 브리프대로 삭제하고 uploaded 게이트·`state --check` FAIL을 새 정상으로 기록(⑥ 불충족, 코드 변경 없음). (c) 하네스 변경(브리프 범위 밖, 건드리지 않음).
- **안전장치**: 실행기 `--apply`는 `…-dry-run-sandbox.json`의 `result`가 `PASS`이고 `candidates_manifest_sha256`이 현재 목록과 같을 때만 시작한다. 지금 기록은 FAIL이라 **현재 목록으로는 `--apply`가 시작 전에 멈춘다**(장난감 트리 시험으로 확인, `--apply`는 실제 저장소에 실행하지 않았다).

## 2. 지울 목록 요약 (`2026-11-04-2300-post-upload-cleanup-candidates.json`)

| 분류 | 파일 수 | 논리 바이트 | git 추적 | 비추적(복구 불가) |
|---|---:|---:|---:|---:|
| A 미디어 | 219 | 7,557,230,274 (7.04 GiB) | 0 | 219 |
| B 옛 20곡 초안 | 443 | 18,029,257 | 442 | 1 (`.DS_Store`) |
| C 과정 파일 | 16 | 171,741 | 12 | 4 |
| D 세션 임시(저장소 밖) | 189 | 64,157,310 | 0 | 189 |
| **합계** | **867** | **7,639,588,582** (7.11 GiB) | | |

- 모든 행에 경로·sha256·장치·inode·바이트·mtime·nlink·분류·사유·git 추적 여부가 있다. 파일이 빈 뒤 `rmdir`만 할 폴더 목록: 저장소 57개 + 임시 57개(비어 있지 않으면 건너뛰고 보고, 비우지 않음).
- B 중 git에 있는 442개는 HEAD `c966a62`에서 복구 가능. A·D와 C의 `.pyc`·로그 2개는 복구 불가.

### A 미디어 — 219개 · 7,557,230,274 B
- `work/2026-11-04-2300-browser-capture/` 전체 164개 2,729,023,611 B (`captures/` 136개 2,698,826,580 B: raw·가드 WAV 34개 포함; 탐침 WAV 5개, 진단·녹음 실행 파일 3개, 로그·마커). 이 폴더의 파일은 전부 이번 작업이 만든 것(미디어 확장자 전수 조회에서 11/1 이후 다른 미디어 없음).
- `SERIES/23-00/work/` 전체 36개 2,582,870,638 B (`merged.wav`, `norm_tracks/` 17, `preview_*` 18).
- `SERIES/23-00/input/tracks/*.wav` 17개 1,282,664,596 B — **§1의 충돌 대상**.
- `SERIES/23-00/output/final.mkv` 958,208,576 B(업로드한 파일 `e2da2e85…`), `preview.mp4` 4,462,853 B.

### B 옛 20곡 초안 — 443개 · 18,029,257 B
`input/source-history/` 80개(`.DS_Store` 1개 포함) · `input/suno-candidates.json` 1개 · `input/validation/2026-11-01-generation/` 137개 · `…/2026-11-02-regeneration/` 131개 · `.ai/lyrics/2026-11-01_23-00_*` 11개 · `.ai/research/2026-11-01-2300-nine-tracks/` 66개 · `.ai/plans/2026-11-01-2300-*`·`2026-11-02-2300-*` 17개. 코드 확인: `wavvy.py`는 `suno-candidates.json`을 `playback-order.json`이 있을 때(23:00엔 없음)나 `suno-final-selection*.json`이 없을 때만 읽는다. 선택 파일 1개(`suno-final-selection-2026-11-04.json`)가 있어 영향 없음 — 가상 삭제에서 `validate`·게이트 확인됨.
`.DS_Store` 1개는 `source-history/`가 통째로 사라지므로 폴더 정리를 위해 넣었다(Finder 메타데이터).

### C 과정 파일 — 16개 · 171,741 B (각 행의 증거는 `2026-11-04-2300-post-upload-cleanup-reference-scan.json`·후보 목록의 `reason`)
- 실패·대체 기록 8개(`production/video-production-20261104/gates/`): `gate-render-final.json`·`gate-source-final.json`·`gate-upload-ready.json`·`state-check-final.json`(result FAIL → 날짜 접두 PASS 기록이 대체), `finalize-upload-check.log`(FAIL), 브리프가 지목한 `*unpatched*` 2개와 `verify-release-baseline-before-selection-file.json`. 빌더가 내용(FAIL 여부)과 PASS 대체본 존재를 단언한다.
- 중복 사본 1개: `input/validation/2026-11-04-timed-subtitles/candidate-youtube_subtitles_ko_timed_estimated.srt` — `output/…srt`와 sha256·바이트 동일, `subtitles.json`은 `output/` 경로+해시만 묶고 이 경로를 부르는 기록은 없다(기록의 `candidate.srt`는 임시 이름).
- 적용 끝난 패치 1개: `proposed-harness-patch-subtitles.diff` — `patch -R --dry-run`이 현재(커밋된) `wavvy_harness/subtitles.py`에 깨끗이 적용돼 이미 반영됨을 확인. 실제 diff는 `harness-patch-checks/git-diff-wavvy_harness-subtitles.diff`에 남는다.
- `__pycache__` 2개(`production/browser-capture-20261104/`), 완료된 단기 계획 4개(`.ai/plans/2026-11-04-2300-{browser-capture,video-production,subtitles-upload-prep,youtube-upload}.md`, 모두 커밋 `791bea1`에 있음).
- `production/browser-capture-20261104/` 안의 「미완료·진단 시도 기록」은 **후보 0개**: 해당 후보 전부를 보존 기록이 이름으로 부르고 있어 보호(§4).

### D 세션 임시 — 189개 · 64,157,310 B
`scratchpad/` 아래 파일 188개 64,065,997 B(백업·확인 그림·스크립트·`watch.html`·`upload/`·`video/` 등. 이 작업의 `cleanup-work/` 도구 4개 포함 — 삭제하면 목록 재생성 도구도 사라진다) + `~/Downloads/captions.srt` 1개(sha256 `aa317ea87a52af6336ceaec44d88fb05b8b02b492c053c21e87adc8374d1e343`, 크기 91,313 B가 `publication/studio-published-manual-ko.srt`와 같아 조건 충족). 목록은 고정 시점 기준이며 그 뒤 새로 생긴 임시 파일은 실행기가 건드리지 않는다. 세션 `tasks/`는 범위 밖이라 제외.

## 3. 지킬 목록 (`2026-11-04-2300-post-upload-cleanup-protected.json`)

- 해시 고정 4,296개 / 1,231,870,731 B: 저장소 작업 트리의 나머지 일반 파일 전부(`.git`·`.venv` 제외). 다른 시리즈·`work/` 다른 폴더·`.ai/` 기록·코드·테스트·MASTER·skills·brand 포함. 해시 고정에서 뺀 것: `.DS_Store`·`__pycache__`·`.ai/remote-control/`(훅이 계속 씀) 512개(stat만 기록).
- 문서 수정 대상 5개는 「기준 해시만」 기록하고 실행 중 불변만 요구: `SERIES/23-00/concept.md`, `.ai/SESSION.md`, `.ai/HANDOFF.md`, `CHANGELOG.md`, `.ai/state.json`.
- 외부: `.venv` 트리 28,971개 항목의 stat 다이제스트, Whisper 모델 캐시 폴더 10개 항목 다이제스트, git HEAD `c966a62`.
- 코드·manifest로 확인한 묶임(`2026-11-04-2300-post-upload-cleanup-dependency-check.json`): `subtitles.json`(경로+해시 레코드 + 시간표 음성 근거 키 + `report.json`·`concept.md`) 59개가 전부 보호 목록에 있고 후보와 겹치지 않는다. 브리프 「지킬 것」 17개 대표 항목과 글롭 묶음(artwork-final 3·`tracks/*.txt` 17·browser-capture JSON 16·suno-ui 31·youtube-upload-ui 40·timed-subtitles 등) 후보 겹침 없음(`2026-11-04-*` 검증 폴더의 후보 2개 = §2 C의 중복 SRT·적용 diff).
- 이미 있던 작업 트리 변경(우리 것 아님, 그대로 둠): `SERIES/07-00/input/thumb.jpg`·`SERIES/19-30/input/thumb.psd`가 git 기준 삭제 상태. 새 비추적: 이 브리프 파일과 `.ai/research/2026-11-04-youtube-upload-defaults/`(둘 다 보호).

## 4. 애매해서 보호로 둔 항목

| 항목 | 개수·크기 | 보호 이유 | 선택 시 |
|---|---|---|---|
| `.ai/validation/2026-11-01-2300-foundation/`·`…-lyrics/`·`2026-11-02-2300-original-style-gate/`·`…-styles/` | 30+430+11+149개, 약 1.6 MB | 브리프 B 목록에 이름이 없는 옛 초안 검증 폴더 | B에 넣으려면 젠 확인 필요 |
| `.ai/plans/2026-11-01-ego-lite-browser-default-brief.md` | 5,786 B | `2300` 접두가 아니라 B 글롭에 안 걸림, ego lite 기본 브라우저 결정 문서 | 그대로 둠 |
| `…/2026-11-04-timed-subtitles/harness-patch-checks/` | 8개 26,379 B | 하네스 패치 검사 기록(단위시험 출력 등). 선례는 검사 기록 보존 | 그대로 둠 |
| `gates/2026-11-04-verify-subtitles-prepared-patched-copy-temp-series.json` | 1,599 B | PASS 기록이지만 적용 전 임시 사본 검증. 안의 문장이 지울 `proposed-…diff`·`*unpatched*`를 가리킴(지운 뒤 끊김) | 대체 기록으로 C에 넣을지 결정 |
| `gates/state-check-before.json`·`verify-release-final.json`·`2026-11-04-state-write*.log`·`logs/validate*.log` | 소형 PASS 기록 | 서로 바이트가 같은 쌍이 있으나 어느 쪽이 「최종본」인지 단정 불가 | 그대로 둠 |
| `production/browser-capture-20261104/`의 `library-search-incomplete-attempt01.json`·`trash-search.json`·`trash-keyword-search.json`·`browser-sound-settings.json`·`state-check.json`·`library-search.json` | 6개 | 진단·미완료 시도지만 `style-provenance.json`·`capture-manifest.json`·`review-20261104.md`가 이름으로 부름 | 그대로 둠 |
| 같은 폴더의 `original-candidates.json`·`style-validation.json`·`workspace-after-numbering.json`, `suno-ui/` 중 참조 없는 3개(`c961d522…`·`e925ced7…`·`f6a89cb8…`), 스크립트 `browser-tracker.js`·`capture-*.swift`·`verify-capture.py` | 12개 | 참조가 없어도 PASS/출처/스크립트로 브리프가 보호로 지정 | 그대로 둠 |
| 저장소 루트·`wavvy_harness/`·`tests/` 등의 `__pycache__`, 다른 시리즈 `__pycache__` | 해시 고정 제외 | 이번 작업이 만든 것이 아니고 실행 때마다 재생성 | 그대로 둠 |
| `.ai/validation`·`.ai/research` 등 다른 날짜의 기록 | 전부 | 브리프 「`.ai/` 기록」 보호 | 그대로 둠 |

## 5. 문서·링크 후속 (4단계에서 할 일, 아직 수정 안 함)

- `concept.md`: 연속한 6개 절 32~580행(549행) = `## Historical 20-song draft …`·`## Series Overrides`·`## Type Styles`·`## Original Styles`·`## New Song Style Assembly`·`## Track Map`을 제목 1개 + 한 줄(「옛 20곡 초안 자료는 2026-11-04 젠 「지우기」로 삭제, 복원은 git 커밋 `791bea1` 이전 기록.」)로 바꾼다(가상 사본에서 이 교체를 적용해 게이트·자막 검사 확인됨). 절별 해시는 `2026-11-04-2300-post-upload-cleanup-reference-scan.json`의 `concept_edit_plan`. `## Final Track Sources`·`## YouTube Metadata`·`## Upload Status`·`## Source Records`는 그대로.
- 남는 절 안의 낡은 언급 10줄(줄 번호는 `concept_edit_plan.kept_sections_with_stale_mentions`): `## Series Status` 9·11·12·13·14·20행, `## Source Records` 583·585행, `## Upload Status` 695·702행. 거짓이 되는 문장은 **702행 「로컬 `final.mkv`·`upload.csv`·썸네일은 삭제하지 않았다」**와 14행·20행·583행·585행의 경로 안내. `## Local Retention`이라는 절은 현재 concept에 없다(브리프의 「기존 보관 절」에 해당하는 절 없음 → 새로 만들지 결정 필요).
- 완료 계획 4개의 링크: `.ai/SESSION.md` 6·11·14·15행, `.ai/HANDOFF.md` 14·19·22·23행에만 있다(`video-production`·`subtitles-upload-prep`·`youtube-upload` 경로). `browser-capture.md`는 SESSION/HANDOFF에 링크가 없다. **`CHANGELOG.md`와 `concept.md`에는 이 4개 계획의 이름이 없다**(브리프 기대와 다름, 스캔 원문 `plan_link_lines`).
- 지운 뒤 끊기는 말(보존 기록 안, 수정 대상 아님): `tools/NOTE.txt` 9행(diff 경로), 패치 사본 검증 JSON(§4), `capture-manifest.json`·`recordings.md`·`download-manifest.json`·`capture.py`·`verify-capture.py`(삭제될 `work/…` 경로·마크다운 링크), `.ai/plans/2026-11-01-ego-lite-browser-default-brief.md`와 `.ai/validation/2026-11-0[12]-2300-*`(삭제될 계획·가사·nine-tracks 경로). 서술이 아니라 이력 기록이라 이번 계획은 손대지 않는다.

## 6. 4단계(오케스트레이터 검토·결정 뒤) 순서

1. §1 결정 반영. WAV 보호 시: 빌더 `classify_basic`의 WAV 줄을 빼고 목록·실행기를 재생성(`cleanup-work/build_manifests.py`→ 새 해시가 실행기에 박힘), 가상 삭제·dry-run 재실행. 목록이 바뀌면 해시가 달라져 옛 실행기는 스스로 멈춘다.
2. 격리 검토(오케스트레이터) → 적용 지시.
3. 문서 편집(concept 절·링크·보관 문장, SESSION/HANDOFF/CHANGELOG)은 **적용 전**에 해야 링크가 끊기지 않는다. 실행기는 문서 5개를 「실행 중 불변」만 확인하므로 편집 뒤에도 동작한다(단, 이 브리프 파일 `.ai/plans/2026-11-04-2300-post-upload-cleanup.md`는 해시 고정이라 수정하면 재생성이 필요).
4. `python3 .ai/cleanup/execute-2300-post-upload-cleanup-20261104.py --apply`(파일별 정확 unlink, 열린 파일 lsof, 목록 밖 접근 없음) → 마감 기록 `-closeout.json` → `state --write --if-match 105`(필요 시) → 게이트·자막 2단계 → CHANGELOG.

## 7. 원시 근거 파일 (모두 `.ai/cleanup/`)

- `2026-11-04-2300-post-upload-cleanup-inventory.json`(sha256 `b8074dfc61a055307c6f915dbe8c1cb1fa9d921b4125366dba22faebf9cf984e`), `-candidates.json`(`acbfcd1dd159d10968f675b25f01b0bfda8acd7eb095ce7324e90ac98a46e587`), `-protected.json`(`50540fbb60f0fec626d7507bd05001eae240923c7f47ef94900802887577f171`), `-reference-scan.json`(`721aedc0c591177ff8d477fb9be163819a0713baa7eccebe93c2768e86acc69b`), 실행기 `execute-2300-post-upload-cleanup-20261104.py`(`e71aa5aa7c16c6004564b63b95335c228ff066730d83306fd26c1cf702157fa1`).
- `-dry-run.json`(+`.stderr.txt` 0바이트): 실행기 기본 실행 — `dry_run_pass`, 후보 867개 7,639,588,582 B, 보호 4296개 해시·stat 일치, 열린 후보 0, uploaded 게이트·자막 2단계·`state --check` PASS(revision 105).
- `-dry-run-sandbox.json`(+`.stdout.json`·`.stderr.txt`): 가상 삭제 원시 출력 전체(명령·종료 코드·stdout/stderr, 시험 출력 포함). `result: FAIL`(§1).
- `-dependency-check.json`: 코드·manifest 묶임 점검. `-executor-toy-test.py`/`.txt`: 실행기 적용 경로를 장난감 트리에서 시험(19건 OK: 기록 없음·FAIL 기록·다른 목록 기록·후보 변경·열린 후보에서 거부, 정상 적용·폴더 정리·불변·저널, 재실행 거부).
- 고정 해시 표는 위. 이 계획 파일 자체는 해시 고정 대상이 아니다.
