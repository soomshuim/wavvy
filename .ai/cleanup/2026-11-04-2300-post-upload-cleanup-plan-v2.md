# 23:00 업로드 후 정리 — 고정 계획 v2 (2026-11-04)

v1(`2026-11-04-2300-post-upload-cleanup-*.json`, `-plan.md`)은 기록으로 그대로 둔다. v2는 코디네이터 결정 6건을 반영해 문서를 먼저 고친 뒤 다시 고정했다. **삭제·이동은 아직 하나도 하지 않았다.** 저장소 HEAD `c966a62`(하네스·문서 변경은 아직 비커밋), 공개 영상 `wbJQ2WgfJn4`.

## 1. v1 대비 바뀐 것

| 결정 | 반영 |
|---|---|
| 1 WAV 17개 | A 후보에 그대로 유지(1,282,664,596 B). 하네스 수정(`wavvy.py`·`state.py`·`gate.py`·`SSOT.md`·`SPEC.md`·새 시험)이 반영된 트리에서 가상 삭제 통과 |
| 2 옛 초안 검증 폴더 | `.ai/validation/2026-11-01-2300-{foundation,lyrics}/`·`2026-11-02-2300-{original-style-gate,styles}/` 620개를 B로 이동 |
| 3 패치 사본 검증 JSON | `gates/2026-11-04-verify-subtitles-prepared-patched-copy-temp-series.json`을 C로 이동(안의 `proposed_patch`가 지울 diff를, `note`가 지울 `*unpatched*` 기록을 가리킴을 빌더가 단언) |
| 4 `ego-lite-browser-default-brief.md` | 보호 유지 |
| 5 concept | `## Local Retention` 새 절, `## Upload Status`의 삭제 문장 수정, 옛 초안 6개 절 교체(§3) |
| 6 SESSION/HANDOFF 링크 | 해당 줄 4+4개를 「커밋 `791bea1`의 계획 문서 `…md`」로 교체. 이번 정리 브리프는 보존 |

## 2. 지울 목록 요약 (`2026-11-04-2300-post-upload-cleanup-candidates-v2.json`)

| 분류 | 파일 수 | 논리 바이트 | git 추적 | 비추적(복구 불가) |
|---|---:|---:|---:|---:|
| A 미디어 | 219 | 7,557,230,274 (7.04 GiB) | 0 | 219 |
| B 옛 20곡 초안 | 1063 | 19,642,131 | 1062 | 1 (`.DS_Store`) |
| C 과정 파일 | 17 | 173,340 | 13 | 4 |
| D 세션 임시(저장소 밖) | 197 | 64,765,139 | 0 | 197 |
| **합계** | **1,496** | **7,641,810,884** (7.12 GiB) | | |

- A: 구성은 v1과 같다(녹음 작업 폴더 164 · `SERIES/23-00/work/` 36 · `input/tracks/*.wav` 17 · `final.mkv`·`preview.mp4`). B 1063개 = v1 443 + 검증 폴더 620(1,612,874 B). C 17개 = v1 16 + 패치 사본 검증 1(1,599 B). D 197개 = scratchpad 196개 + `~/Downloads/captions.srt` 1개(sha256 `aa317ea8…d1e343`).
- D가 v1보다 8개 늘어난 이유: 이번 작업의 `baseline-docs/` 5개(문서 편집 전 사본)와, 그 사이 scratchpad에 생긴 `run_matrix.sh`·`run_sim.sh`·`summarize.py`(코디네이터 쪽 파일, 「세션 임시 전부」 규칙대로 포함).
- 삭제 후 `rmdir`할 폴더: 저장소 61개 + 임시 58개(비어 있지 않으면 건너뛰고 보고).
- git에 있는 B 1062개 · C 13개는 커밋에서 복구 가능. A·D와 `.DS_Store`·`.pyc`·로그 2개는 복구 불가.
- 지킬 목록 `2026-11-04-2300-post-upload-cleanup-protected-v2.json`: 해시 고정 4,055개 / 1,235,557,484 B(v1 4,296 → 620+1개가 후보로 이동, 새 보호 380개 = `.ai/validation/2026-11-04-uploaded-audio-cleanup/` 364 + v1 정리 기록 15 + `tests/test_uploaded_audio_cleanup.py`), 문서 5개는 기준 해시만, 해시 제외 513개(`.DS_Store`·`__pycache__`·`.ai/remote-control/`), `.venv`·Whisper 캐시 다이제스트, git HEAD.

## 3. 바뀐 문서 diff 요약 (`2026-11-04-2300-post-upload-cleanup-doc-edits-v2.diff`, sha256 `b137bfbc3676ee7292b5266a084ef1d7c3c23dd0b7576091774fd7d63f585b2c`)

| 문서 | 줄 변화 | 내용 | 편집 후 sha256 |
|---|---|---|---|
| `SERIES/23-00/concept.md` | −549 / +14 | ① 32~580행(6개 절: Historical 20-song draft·Series Overrides·Type Styles·Original Styles·New Song Style Assembly·Track Map)을 `## Historical 20-song draft — deleted` 제목 + 「옛 20곡 초안 자료는 2026-11-04 젠 「지우기」로 삭제, 복원은 git 커밋 `791bea1` 이전 기록.」 한 줄로 교체 ② `## Upload Status`의 「로컬 final.mkv·upload.csv·썸네일은 삭제하지 않았다」 → 「로컬 final.mkv·preview.mp4·input/tracks/*.wav는 업로드 후 삭제한다(Local Retention 절). upload.csv·output/report.json·썸네일은 보존한다.」(`- YouTube upload: completed` 줄과 절 수 1개는 그대로) ③ `## Final Track Sources` 앞에 `## Local Retention` 새 절(정리 대상·보존·음원과 하네스·옛 언급 안내·실행 상태, 17:30 선례 형식) | `533f322ba4bfc1ce3a3320c5e69f38af84835496aaf1e7f1b34bfb227a7dfda7` |
| `.ai/SESSION.md` | −4 / +4 | 6·11·14·15행의 `.ai/plans/2026-11-04-2300-{video-production,subtitles-upload-prep,subtitles-upload-prep,youtube-upload}.md` → 「커밋 `791bea1`의 계획 문서 `…md`」 | `781e2de674896dd25de660c4c89f8b30bc78fde7e022654c18b7cf4a962bd5a9` |
| `.ai/HANDOFF.md` | −4 / +4 | 14·19·22·23행 같은 교체 | `7c2009c0c76634ac954321a525a1633f8099fff60d9effb1f8f958607c58c8eb` |
| `CHANGELOG.md`, `.ai/state.json` | 변경 없음 | CHANGELOG 항목과 state 기록은 적용 뒤 | `38d275f85c7c0f5531f27d942f055125a024542f961e301327b83d508199b8c2` / `cedcbdf4d0b6e1d61002e6c4567a039f49ee477ead5eab7677ced9f9d2b8f13d` |

- 편집 직후 실제 저장소에서 `state --check` PASS, `gate --stage uploaded` PASS(WAV 아직 있음). 4개 계획 경로 참조는 SESSION·HANDOFF·CHANGELOG·concept에서 0개(빌더가 단언).
- **알림**: `## Local Retention`의 「실행 상태」 줄은 「삭제 실행 전」이라고 정직하게 적어 두었다. 적용 뒤 실제 결과·마감 기록 경로(`…-v2-closeout.json`)로 바꿔야 한다(그 전까지 이 절은 계획 상태를 말한다).
- 지시 밖이라 손대지 않은 낡은 언급 10줄(적용 뒤 거짓이 되는 곳은 `Series Status` 14행의 `work/…` 경로와 12·20행·`Source Records` 38·40행의 옛 초안 경로 안내, 나머지는 `final.mkv` 해시 사실 서술): 9행, 11행, 12행, 13행, 14행, 20행, 38행, 40행, 150행, 157행. Local Retention 「옛 언급」 항목이 이들이 삭제 전 기록임을 안내한다.

## 4. dry-run·가상 삭제 결과 (통과 기준별)

가상 삭제 사본 = 현재 작업 트리를 APFS 복제(`.git`·`.venv`·`work/` 제외)해 후보 1,135개를 정확 경로로 지운 사본(`work/` 후보 164개는 복제 범위 밖이며 어떤 검사도 `work/`를 읽지 않음: 원본 사본도 `work/` 없이 PASS). 기준 사본 = 같은 트리, 아무것도 안 지움.

| 통과 기준 | 기준 사본 | 가상 삭제 사본 |
|---|---|---|
| `gate --stage uploaded` | PASS (exit 0) | **PASS (exit 0)** (blockers 없음) |
| `state --check` | PASS (exit 0) | **PASS (exit 0)**, `audio_source: deleted_after_upload` (기준 사본 `input_tracks`) |
| `verify-subtitles --stage prepared` | PASS (exit 0) (1490큐) | **PASS (exit 0)** |
| `verify-subtitles --stage published` | PASS (exit 0) | **PASS (exit 0)** |
| 시험 파일 8개(181건) | 전부 OK | 전부 OK, 기준과 동일 |
| 참고: `validate` | exit 0 | exit 0 |
| 참고: `verify-release`(업로드 전 검사) | PASS (exit 0) | **FAIL (exit 1)** — 「missing audio for report tracks: 01…17」, 기준 아님 |

시험 파일별(기준 → 가상 삭제): test_harness.py 82 tests→82 tests OK, test_integrated_premix.py 17 tests→17 tests OK, test_premixed_audio.py 26 tests→26 tests OK, test_subtitle_timing_contract.py 17 tests→17 tests OK, test_subtitles.py 15 tests→15 tests OK, test_video_artwork.py 12 tests→12 tests OK, test_youtube_titles.py 3 tests→3 tests OK, test_uploaded_audio_cleanup.py 9 tests→9 tests OK.

- 실제 저장소에서 실행기 기본 실행(`2026-11-04-2300-post-upload-cleanup-dry-run-v2.json`): `dry_run_pass`, 후보 1,496개 7,641,810,884 B, 보호 4,055개 해시·stat 일치, 문서 5개 기준 해시 확인, 열린 후보 파일 0개(lsof), `.venv`·Whisper 캐시·git HEAD 불변, uploaded 게이트·자막 2단계·`state --check` PASS, 여유 공간 401,856,286,720 B.
- 실행기 `--apply` 안전장치: `…-dry-run-sandbox-v2.json`이 `PASS`이고 v2 candidates 해시와 같아야 시작한다. **이제 그 기록이 PASS**이므로 오케스트레이터의 적용 지시만 남았다. `--apply`는 실제 저장소에서 실행하지 않았고, 적용 경로는 v2 실행기로 장난감 트리에서 19건 시험해 OK(`…-executor-toy-test-v2.txt`, sha256 `6a9c1e23aed0a271e07aa65b8e5c1bcec4593179ea79c90c192a86f13b505590`).
- 코드로 확인한 규칙(`2026-11-04-2300-post-upload-cleanup-dependency-check-v2.json`): `uploaded_audio_cleanup_errors(SERIES/23-00)` = `[]`(Final Track Sources 17곡 Filename·SHA-256 = `output/report.json` 17곡), 자막·시간표 묶임 59개 전부 보호, 결정·브리프 보호 대표 항목 26개 겹침 없음.

## 5. 적용 이후 순서(오케스트레이터 지시 뒤)

1. 격리 검토 → 적용 지시 → `python3 .ai/cleanup/execute-2300-post-upload-cleanup-20261104-v2.py --apply`.
2. 마감 기록 `2026-11-04-2300-post-upload-cleanup-v2-closeout.json`(삭제 개수·바이트·여유 공간 전후·보호 불변·대상 부재·게이트), `state --write --if-match 105`(phase uploaded, `audio_source: deleted_after_upload` 반영), concept `## Local Retention`의 실행 상태 줄 갱신, CHANGELOG 항목.
3. 이 브리프 파일(`.ai/plans/2026-11-04-2300-post-upload-cleanup.md`)·문서 5개는 실행 중 불변만 요구하므로 적용 전에 문서를 더 고쳐도 실행기는 동작한다(브리프 파일은 해시 고정이라 수정하면 재생성 필요).
4. `cleanup-work/` 도구(빌더·실행기 틀·가상 삭제·baseline-docs)는 D에 들어 있어 적용 때 함께 지워진다. 재생성이 필요하면 적용 전에 해야 한다.

## 6. 원시 근거 파일 (모두 `.ai/cleanup/`, 파일명 `2026-11-04-2300-post-upload-cleanup-…` 생략)

| 파일 | sha256 |
|---|---|
| `inventory-v2.json` | `35bd4aceee48d73fa296b6014f450a4dd27903b2625d279b790a7ccd9e0dcb8d` |
| `candidates-v2.json` | `e52db6234af7d33d036d692de1ae5f8e5522b4f02742f3b45cbc0af8ac218a8c` |
| `protected-v2.json` | `645205dee8a429051bac4fd7b4d0bd8a904a741860d127add9471dcf0595102a` |
| `reference-scan-v2.json` | `3a9b007025fae8e533ec7fc8fe7a4f498f2e8efdbfc68f0208119c1095800c1d` |
| `execute-2300-post-upload-cleanup-20261104-v2.py` | `37aab0f11df7032d276e606b601d7c8b5733da5f98dd134ab15562485c98aa02` |
| `dry-run-v2.json` | `a3cf28d37d5110fb577106494ef7b339b27da1fe661dac157a4e037a1601b128` |
| `dry-run-sandbox-v2.json`(+`.stdout.json`·`.stderr.txt`) | `25327bd01b684d26e48e5193c000dd9415bc3fdead52d5e8d662c650db386d97` |
| `dependency-check-v2.json` | `a46954513bd1e2630cfbe969679af07d4b286b5f470b2b311342e0ddea2902ee` |
| `doc-edits-v2.diff` | `b137bfbc3676ee7292b5266a084ef1d7c3c23dd0b7576091774fd7d63f585b2c` |
| `executor-toy-test-v2.py`/`.txt` | `.txt` `6a9c1e23aed0a271e07aa65b8e5c1bcec4593179ea79c90c192a86f13b505590` |

이 계획 파일 자체는 해시 고정 대상이 아니다.
