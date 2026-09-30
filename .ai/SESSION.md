# Session State — Wavvy

> Last updated: 2026-06-02 (34차 업데이트 — historical artifact pruning)

## 진행 중

- **Historical artifact pruning** (2026-06-02 34차, `-record`)
  - ✅ **삭제 기준 확인**: `concept.md`는 시리즈별 전곡 정보 원장으로 보존. 하네스/스킬/에이전트 라우팅 참조가 없는 과거 기록만 삭제 대상으로 분류
  - ✅ **삭제 완료**: `.ai/auto-handoff/`, `.ai/peer-review/runs/`, 미참조 `.ai/pipeline/runs/*`, `.ai/meetings/`, `reviews/`, `Reference/`, 미참조 `meetings/*.md`, 미참조 `report/*.md`, `.ai/lessons-learned.md`
  - ✅ **보존 확인**: `.ai/state.json`, `.ai/HANDOFF.md`, `.ai/SESSION.md`, 전체 `concept.md`, MASTER/스킬/하네스 문서, lyricist 스킬이 직접 참조하는 리서치 run 2개, 20-00 루브릭/컨셉 근거 리포트와 회의록
  - ✅ **검증 PASS**: `py_compile`, `unittest` 15개, `doctor`, `state --check`, `validate SERIES/20-00`, `gate --stage uploaded`, `git diff --check`, `git diff --cached --check`
  - **남은 TODO**: 없음. 향후 과거 기록이 필요하면 git history에서 확인

- **17-00 Track 01 self-spell rewrite** (2026-05-22 33차)
  - ✅ **사용자 피드백 반영**: `올라가` 훅 대신 `기분 좋아져라` 셀프 주문형 콘셉트로 변경
  - ✅ **샘플 파일 갱신**: `SERIES/17-00/input/tracks/01_기분 좋아져라 (Feel Good Spell).txt`로 파일명/트랙명/Style hook phrase/가사/Listen For 동기화
  - ✅ **concept 동기화**: `SERIES/17-00/concept.md` Track Map과 Next Steps의 Track 01 참조를 새 제목으로 변경
  - **남은 TODO**: Track 01 Suno V5.5 샘플 생성 → `기분 좋아져라` hook memorability / bright mood / R&B DNA / no minor-dark drift 기준 PASS 판정

- **`/write` / `-write` lyricist command shim** (2026-05-22 32차, `-director`)
  - ✅ **로컬 command 추가**: `.claude/commands/write.md` 생성. Claude Code `/write`와 Codex `-write`가 같은 Wavvy-local `write` command 이름으로 해석되도록 연결
  - ✅ **thin shim 원칙 유지**: command 본문에는 작사 규칙을 복사하지 않고 `skills/wavvy-lyricist/SKILL.md`, `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`, `MASTER/lyrics/LYRICS.md`로 라우팅
  - ✅ **스코프 제한 반영**: 가사 작성/리라이트/리뷰만 허용. YouTube copy, concept/changelog/session, 일반 문서 작성은 `/write` 범위 밖으로 명시
  - **남은 TODO**: 없음. 다음 17-00 가사 작업부터 `-write SERIES/17-00 ...` 또는 Claude `/write SERIES/17-00 ...`로 호출

- **`/write` lyricist routing decision** (2026-05-22 31차, `-team`)
  - ✅ **팀 결론**: Claude Code에서는 `/write`, Codex에서는 `-write`를 Wavvy lyric-only thin alias로 연결하는 방향이 적절
  - ✅ **SSOT 원칙**: command에는 작사 규칙을 복사하지 않고 `skills/wavvy-lyricist/SKILL.md`, `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md`, `wavvy.py lyrics-skill`로 라우팅
  - ✅ **스코프 제한**: `/write`는 가사 작성/리라이트/리뷰 전용. YouTube copy, concept 문서, changelog 등 비가사 작성은 다른 라우터로 분리
  - ✅ **완료**: 2026-05-22 32차에서 Wavvy-local `/write` / `-write` command shim 구현

- **Wavvy lyricist skill + lyrics-review harness** (2026-05-22 30차, `-play` worker run)
  - ✅ **리서치 baseline 작성**: `.ai/pipeline/runs/20260522-095007_wavvy-lyrics-skill-harness/research/lyrics-skill-baseline.md`와 `source-index.md`에 2026 Pop R&B/Neo-soul 패턴, Wavvy SSOT, 이전 17-00 교정 포인트를 통합
  - ✅ **스킬/계약 추가**: `skills/wavvy-lyricist/SKILL.md`, `skills/wavvy-lyricist/references/patterns.md`, `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md` 생성. `full-lyric-draft` / `suno-prompt-only` / `review-only` 모드와 self-gate 계약 확정
  - ✅ **하네스/CLI 추가**: `python3 wavvy.py lyrics-skill SERIES/[series] --json`와 `python3 wavvy.py gate SERIES/[series] --stage lyrics-review --json`로 스킬 패키지와 optional lyric artifact를 검증
  - ✅ **문서 연결**: `MASTER/SSOT.md`, `MASTER/lyrics/LYRICS.md`, `wavvy.md`, `CHANGELOG.md`, release notes에 새 skill/spec/gate의 권한 위치와 release readiness 기록
  - ✅ **검증 PASS**: `PYTHONPYCACHEPREFIX=/private/tmp/wavvy-pycache python3 -m py_compile wavvy.py wavvy_harness/*.py`, `python3 -m unittest tests/test_harness.py` 15 tests, `python3 wavvy.py lyrics-skill SERIES/17-00 --json`, `python3 wavvy.py gate SERIES/17-00 --stage lyrics-review --json`, `git diff --check`
  - ✅ **Doctor 경로 보정**: `peer_review_script` 기본 경로를 `/Users/zenkim_office/Project/agent-center/scripts/peer-agent-review.sh`로 정정. `state SERIES/17-00 --check`와 `source-final` gate는 17-00이 아직 draft source 단계라 FAIL
  - **남은 TODO**: 다음 17-00 가사/프롬프트 작업부터 `skills/wavvy-lyricist`를 사용하고, lyric draft 산출물은 `lyrics-skill --artifact ... --mode full-lyric-draft`로 검증

- **17-00 Main POP R&B concept draft** (2026-05-21 29차)
  - ✅ **사용자 방향 반영**: 다음 시리즈는 `기분 좋은 POP(Main) R&B`
  - ✅ **Hard gate 확정**: 최소 `120 BPM`, `Major key only`. 119 BPM 이하 / Minor key / dark late-night R&B / slow jam 금지
  - ✅ **시간 슬롯 확정**: `17:00`. 18:00 퇴근길 위로와 겹치지 않게 `퇴근 전부터 기분을 먼저 올리는 시간`으로 포지셔닝
  - ✅ **신규 시리즈 초안 생성**: `SERIES/17-00/concept.md` 작성. Style A Main Pop R&B, Style B Bright Contemporary R&B, Style C Light Funk Pop R&B, 18트랙 draft map, YouTube Draft 포함
  - ✅ **샘플 곡 리디자인**: 초기 `올라가 (Up Again)` 샘플 작성 후 2026-05-22 33차에서 `SERIES/17-00/input/tracks/01_기분 좋아져라 (Feel Good Spell).txt`로 변경. 124 BPM, D Major, Female vocal, Main Pop R&B / Pop Neo-Soul. `기분 좋아져라` 셀프 주문형 반복 훅 중심
  - ✅ **가사 정책 보정**: 시간대는 BPM/Mood/Energy 포지셔닝이고 가사 주제 강제가 아님. `wavvy.md`, `MASTER/lyrics/LYRICS.md`, `SERIES/17-00/concept.md`에 반영하고 Track 01 가사에서 업무/퇴근 직전 소재를 제거
  - **남은 TODO**: Track 01 Suno V5.5 샘플 생성 → `기분 좋아져라` hook memorability / bright mood / R&B DNA / no minor-dark drift 기준 PASS 판정 → 18-track prompt batch 확장

- **RNB-BEST source-map compilation 하네스 보강** (2026-05-21 28차)
  - ✅ **트랙 폴더 부재 정책 반영**: `RNB-BEST`는 `input/tracks/`에 오디오를 복사하지 않아도 `concept.md`의 `## Track Selection` `Source` 경로를 오디오 SSOT로 인정하도록 정리
  - ✅ **validate/pack 보강**: local tracks가 없으면 compilation source map을 읽어 원본 경로를 ffprobe/normalize 대상으로 사용하고, `Copied Filename`을 report/provenance filename으로 유지
  - ✅ **state/gate 보강**: `available_audio_files`, `audio_source=concept_track_selection`, `source_map_*` 상태를 추가하고, source-final gate가 source map 기반 compilation을 PASS 처리
  - ✅ **문서 보정**: `MASTER/SSOT.md`에 compilation source map 정책 추가. `SERIES/RNB-BEST/concept.md`의 stale source path 2건(`피크닉`, `약속`)을 실제 존재하는 13-00 norm track 경로로 수정
  - ✅ **검증 PASS**: `python3 -m py_compile wavvy.py wavvy_harness/*.py`, `python3 -m unittest tests/test_harness.py`, `python3 wavvy.py validate SERIES/RNB-BEST`, `python3 wavvy.py gate SERIES/RNB-BEST --stage source-final --json`, `git diff --check`
  - ✅ **Doctor 상태**: `peer_review_script` 기본 경로를 `/Users/zenkim_office/Project/agent-center/scripts/peer-agent-review.sh`로 정정. 이번 RNB-BEST 변경 자체와 별개인 환경 blocker는 해소
  - **남은 TODO**: 실제 render/upload-ready 검증이 필요하면 `python3 wavvy.py pack SERIES/RNB-BEST -y`로 output artifacts를 재생성

- **RNB-BEST compilation 패키징/메타데이터 정리** (2026-05-08 27차)
  - ✅ **신규 시리즈 구성**: `SERIES/RNB-BEST`를 기존 Wavvy R&B/R&B-adjacent 곡 재활용 best compilation으로 구성. 사용자 선곡 33곡을 최종 러닝 오더로 재번호화하고 `concept.md`에 source map 기록
  - ✅ **콘셉트/메타데이터 확정**: 제목 `Playlist | R&B Best | 와..이 노래 제목 뭐야? ✨ 틀자마자 리듬에 그루비 😎 | CHILL · R&B · SOUL | 카페 · 작업 · 매장 음악 | Wavvy` 확정. 한국어+영문 description, `🌊 Track List`, 원곡 시리즈 표기(`· 22:00` 등), `#` 해시태그 블록과 `#` 없는 tags 동기화
  - ✅ **영상 제작/정리**: 4K image-mode 영상 제작 및 검증 완료 후 사용자 요청에 따라 `.mkv` 렌더 파일 삭제. `output/provenance.md`, `output/report.json`, `output/upload.csv`는 로컬 산출물로 복구/보존
  - ✅ **검증 PASS**: `python3 wavvy.py validate SERIES/RNB-BEST` PASS. output 세 파일은 `.gitignore` 대상이라 커밋에는 포함되지 않으며, 필요 시 `python3 wavvy.py pack SERIES/RNB-BEST -y`로 재생성 가능
  - **남은 TODO**: 실제 업로드가 필요하면 `.mkv`를 다시 생성하거나 별도 보관본을 사용. 현재 커밋 대상은 `concept.md`, `input/thumb.jpg`, `.ai` 회의/리뷰/파이프라인 기록 중심

- **Record checkpoint** (2026-05-04 26차)
  - ✅ **작업 커밋/푸시 완료**: `0d78e41 docs: harden wavvy ssot and prune legacy docs`
  - ✅ **원격 동기화**: `origin/master`와 local `master` 차이 0
  - ✅ **검증 상태**: legacy pruning 전 검증 전체 PASS 유지 (`py_compile`, `unittest`, `doctor`, `validate`, `state`, `gate`, `git diff --check`)
  - **남은 TODO**: 없음

- **Legacy markdown pruning + SSOT/harness hardening record** (2026-05-04 25차)
  - ✅ **`-team` 검토**: `meetings/2026-05-04_legacy-doc-pruning.md`에 AI Ops / Engineering / Product / QA 관점으로 삭제 기준 기록
  - ✅ **삭제 완료**: `.ai/plans/PLAN_wavvy_agent_instruction_minimalism.md`, `.ai/plans/PLAN_wavvy_harness_setting.md`, `meetings/2026-02-07_vibem-swot-analysis.md`, `meetings/2026-03-07_final-mp4-retrospective.md`, `reviews/2026-03-07_vibem-to-wavvy-rename.md`
  - ✅ **보존 원칙**: `.ai/HANDOFF.md`, `.ai/SESSION.md`, `.ai/peer-review/*`, `.ai/pipeline/*`, MASTER SSOT 문서, active series concept/research는 유지
  - ✅ **검증 PASS**: `py_compile`, `unittest`, `doctor --json`, `validate SERIES/20-00`, `state --check --json`, `gate --stage upload-ready --json`, `gate --stage uploaded --json`, `git diff --check`
  - ✅ **커밋/푸시 완료**: `0d78e41 docs: harden wavvy ssot and prune legacy docs`
  - **남은 TODO**: 없음

- **SSOT/문서 중복·충돌 + 하네스 설정 점검/수정** (2026-05-02 24차)
  - ✅ **`-play` 하네스 실행**: `.ai/pipeline/runs/20260502-025736_ssot-harness-audit/`에 team analysis, peer review, plan, plan review, implementation, record artifact 생성
  - ✅ **Peer gates**: analysis review PASS, plan review PASS. Plan review의 Medium finding은 구현 전 반영 (`_upload_completed` 정확 패턴, `upload-ready` check UX, doctor stale scan scope)
  - ✅ **State/SSOT 정합화**: `.ai/state.json` revision 3으로 재작성. `authoritative_docs`가 `MASTER/SSOT.md`, `MASTER/ai/RUNTIME_RULES.md`, `MASTER/MANAGER.md`, `MASTER/WORKFLOWS.md`, `MASTER/cli/SPEC.md`, `MASTER/youtube/YOUTUBE.md`, `wavvy.md`, active `concept.md`를 가리킴
  - ✅ **Gate 의미 보정**: `upload-ready`는 업로드 전 준비 상태이므로 실패성 `youtube_upload_completed` 체크 대신 `youtube_upload_status: pending|completed` PASS check로 보고. `uploaded` stage만 upload completion을 필수로 유지
  - ✅ **Upload inference 강화**: bare `uploaded`/`phase: uploaded` 텍스트만으로 업로드 완료 추론하지 않음. 명시적 `Upload Status`, YouTube URL, 업로드 완료 문구만 인정
  - ✅ **Doctor hygiene 추가**: SSOT docs 존재, AGENTS/CLAUDE router target, entrypoint stale pattern, state authoritative docs, tracked `.DS_Store` absence를 검사
  - ✅ **문서 drift 정리**: vfade는 video-loop packaging에만 scoped, image-mode/uploaded state exempt 명시. LYRICS 괄호 규칙, MANAGER hierarchy, YOUTUBE brand/tag mapping, wavvy title format 중복 정리
  - ✅ **검증 PASS**: `py_compile`, `unittest`, `doctor --json`, `validate SERIES/20-00`, `state --check --json`, `gate --stage upload-ready --json`, `gate --stage uploaded --json`
  - **남은 TODO**: 없음. 사용자 요청에 따라 2026-05-04 legacy pruning과 함께 커밋/푸시 예정.

- **20-00 Final Track Sources 최종 보정 + YouTube 자막 테스트 산출물** (2026-04-30 22차)
  - ✅ **최종 소스 보정**: 사용자 제공 final prompt/lyrics 기준으로 05 Old Cassette, 06 Real Talk, 12 Small Talk, 13 Concrete, 15 Old Page, 19 Side Street, 20 Slow Glow의 Final Track Sources를 정리
  - ✅ **실제 교체**: 12/15/19/20은 STYLE/EXCLUDE/LYRICS 또는 LYRICS를 교체하고 manual final replacement META 추가
  - ✅ **확인/메타 정정**: 05/06/13은 제공본과 본문 일치 확인 후 manual final confirmation META 추가, stale Track 13/15 표기를 현재 05/13 기준으로 수정
  - ✅ **Source checksum 주석 보정**: Final Track Sources 상단에 manual override가 있는 track은 checksum이 pre-override git source checksum일 수 있음을 명시
  - ✅ **YouTube 자막 테스트 산출물**: `output/youtube_subtitles_ko_no_timing.txt`(타이밍 제외 transcript)와 `output/youtube_subtitles_ko_timed_estimated.srt`(report 기반 추정 SRT) 생성. 둘 다 `output/` ignored 로컬 산출물
  - ✅ **자막 정리 규칙**: 가사 외 `[section]`, 괄호 지시문, parens/brackets, STYLE/EXCLUDE/META, timestamps/source metadata 제거. 영상 2회 반복에 맞춰 20곡 x2 반영
  - ✅ **검증 PASS**: no-timing 마크업 0건, SRT 1,732 cues 문법/시간 겹침 0건, `git diff --check`, `python3 wavvy.py validate SERIES/20-00`
  - **상태 보정**: 2026-05-02 사용자 정정에 따라 YouTube 업로드는 완료. 자막 산출물은 로컬 보조 artifact로 보존하며, 남은 TODO는 `wavvy-subtitles` 스킬/하네스화 후 남은 시리즈 일괄 적용.

- **20-00 finalize-upload 하네스 + Final Track Sources 아카이브** (2026-04-30 21차)
  - ✅ **업로드 전환 하네스 구현**: `wavvy.py finalize-upload <series>` 추가. `--check`, `--keep-txt`, `--restore-from COMMITISH` 지원
  - ✅ **소스 계약 명문화**: `input/tracks/*.txt`의 `=== STYLE ===` + 비어 있지 않은 `=== LYRICS ===`를 필수로 검증. `=== EXCLUDE ===`는 선택이며 없으면 `None`으로 아카이브
  - ✅ **복원/매칭 안정화**: 현재 파일시스템에 txt가 없을 때 `--restore-from 'b6f13c4^'` git tree에서 소스를 읽고, stale `Order`가 아니라 정규화한 제목으로 현재 `output/report.json` 트랙과 매칭
  - ✅ **concept.md 업로드용 SSOT 확정**: `SERIES/20-00/concept.md`에 `## Final Track Sources` 20블록 생성. Timestamp, Repeat Timestamp, Filename, Title, Mood, Genre, Type, BPM, Key, Length, Vocal, audio SHA-256, Source Title, Source Checksum, STYLE, EXCLUDE, LYRICS, META 포함
  - ✅ **삭제 안전장치**: 실제 run은 아카이브 검증 후에만 `input/tracks/*.txt` 삭제. 20-00은 이미 txt가 없어서 git 복원 소스를 concept에 이식하고 삭제 대상 0건으로 완료
  - ✅ **운영 문서 보강**: `MASTER/WORKFLOWS.md`와 `MASTER/youtube/YOUTUBE.md`에 `finalize-upload --check` PASS 전 txt 삭제 금지, upload FINAL SSOT 전환 절차 기록
  - ✅ **Peer review**: Claude plan review 1차 FAIL → 수정 후 PASS. 구현 review는 direct Claude CLI PASS
  - ✅ **검증 PASS**: `py_compile`, 11-00/12-00/20-00 validate, `finalize-upload --check`, 실제 `finalize-upload`, negative fixture 3종, `git diff --check`
  - **남은 TODO**: 20-00 자막 생성은 이제 `concept.md`의 `Final Track Sources` LYRICS를 기준으로 진행. 영상/`upload.csv`가 다시 필요하면 `wavvy.py pack SERIES/20-00 -y` 재실행.

- **20-00 YouTube Metadata SSOT 하네스 + 업로드 문안 확정** (2026-04-30 20차)
  - ✅ **`concept.md` 최상단 배치**: `## YouTube Metadata v0.5 (FINAL)`를 문서 상단으로 이동해 업로드 직전 바로 확인 가능하게 정리
  - ✅ **최종 제목 확정**: `Playlist | 20:00 | 💪 앞으로 이 플리 없이 절대 운동 못할걸?! | Drill · Rage · Trap · Boombap | 헬스·러닝 BGM | Wavvy`
  - ✅ **최종 설명문 확정**: `20:00, 앞으로는 이 플리 없이 절대 운동 못할 거예요.` + `아드레날린 강제 폭주시키는 Drill · Rage · Trap · Boombap Hiphop Mix Workout 플리 - Wavvy`로 시작
  - ✅ **해시태그 블록 정리**: 사용자 제공 태그 리스트를 `#운동BGM ... #showmethemoney #쇼미더머니` 형태로 description 하단에 반영
  - ✅ **하네스 보강**: `wavvy.py validate/pack`이 `concept.md`의 `## YouTube Metadata` 또는 `## YouTube Draft`에서 `제목/설명/태그`를 파싱. 누락 시 warning, pack 시 `upload.csv` 자동 채움
  - ✅ **기존 포맷 호환 검증**: 12-00/14-00/15-00/18-00의 기존 `YouTube Draft/Metadata` 포맷도 파싱 PASS
  - ✅ **출력 정리**: `concept.md`를 SSOT로 남기고 별도 YouTube 보조 파일(`youtube_*.txt`, `youtube_upload_info.md`, `upload.csv`) 삭제. 사용자가 `final.mkv`도 삭제 완료
  - **남은 TODO**: 필요 시 `wavvy.py pack SERIES/20-00 -y`로 영상/`upload.csv` 재생성. 업로드 문안은 `concept.md` 최상단 metadata를 사용.

- **20-00 WAV 리네임 + YouTube 영상 패키징 완료** (2026-04-30 19차)
  - ✅ **WAV 20곡 리네임 완료**: `concept.md` v0.6 최종 러닝 오더 기준 `NN__Title__Style__Genre__BPM.wav` 형식으로 정리
  - ✅ **Fake/Engine 순서 교정**: 입력 폴더는 `17. Engine.wav` / `18. Fake.wav`였지만, 최종 맵 기준으로 `17 Fake (140 BPM)` / `18 Engine (150 BPM)`이 맞아 제목 기준으로 교환
  - ✅ **검증 PASS**: `python3 wavvy.py validate SERIES/20-00` 통과. 20 tracks, 48kHz WAV, `loop.png`, `thumb.jpg` 확인
  - ✅ **자동 패키징 완료**: `python3 wavvy.py pack SERIES/20-00 -y` 실행. -14 LUFS 정규화, 0.8s 크로스페이드, 20곡 x2 반복 머지
  - ✅ **산출물 생성**: `SERIES/20-00/work/merged.wav` 7,876.24s / `SERIES/20-00/output/final.mkv` H.264 + FLAC / `provenance.md` / `upload.csv` / `report.json`
  - ✅ **영상 QA PASS**: 초기 render의 61s container tail을 remux-trim해 최종 container duration 7,879s로 보정. `ffprobe`와 video/audio decode checks PASS
  - ⚠️ **상태 주의**: WAV, merged WAV, MKV, output artifacts는 `.gitignore` 대상이므로 git 커밋에는 포함되지 않음. 업로드 파일은 로컬 산출물로 보존됨
  - **상태 보정**: 2026-05-02 사용자 정정에 따라 YouTube 업로드 완료. `output/final.mkv`는 로컬 용량 정리를 위해 삭제된 상태이며 필요 시 `pack`으로 재생성.

- **20-00 v0.6 최종 러닝 오더 확정 + 트랙 txt 삭제** (2026-04-30 18차)
  - ✅ **최종 순서 확정**: 단순 번호/BPM이 아니라 장르·질감·체감 속도까지 종합해 5곡 단위 `강-약-중-강-약` 파형으로 재배치
  - ✅ **최종 20곡 v0.6**: 01 Paycheck / 02 Night Rider / 03 Bottom to the Top / 04 Yang Gang / 05 Old Cassette / 06 Real Talk / 07 LLC / 08 Boomerang / 09 Black Mirror / 10 Bottom Line / 11 Overtime Flame / 12 Small Talk / 13 Concrete / 14 Cold Stack / 15 Old Page / 16 Rewrite / 17 Fake / 18 Engine / 19 Side Street / 20 Slow Glow
  - ✅ **Slow Glow 엔딩 확정**: 108 BPM half-time melodic cooldown 체감이 가장 느려 20번 최종 엔딩으로 배치
  - ✅ **피크 역할 분리**: Black Mirror는 150 BPM sultry female dark trap 질감 피크, Cold Stack은 180 BPM 속도 피크로 정리
  - ✅ **분포 검증 문서화**: Hard 65% = A3+C5+D3+F2, Non-Hard 35% = B5+E2, 보컬 M14/F6 유지
  - ✅ **개별 txt 프롬프트 정리**: `SERIES/20-00/input/tracks/*.txt` 전체 삭제. 이후 개별 프롬프트 복원이 필요하면 `concept.md` v0.6을 SSOT로 사용
  - ⚠️ **상태 주의**: `SERIES/20-00/input/new_loop.png` 삭제와 `SERIES/20-00/input/thumb.jpg` 추가가 같은 워크트리에 남아 있어 이번 record 커밋에 포함됨
  - **남은 TODO**: (1) draft 8곡(05/06/07/09/10/11/13/18) Suno 생성/검수. (2) PASS 곡 누적 시 concept.md Status만 갱신. (3) 오디오 파일은 v0.6 순서 기준으로 리네임/패키징.

- **20-00 Track 17 `Small Talk` 리네임 + Rage Tuned sing-rap 전환** (2026-04-30 17차)
  - ✅ **제목/파일명 변경**: `17_Late Lane.txt` → `17_Small Talk.txt`, Track명 `Late Lane` → **Small Talk (스몰 토크)**
  - ✅ **가사 주제 전환**: 새벽 lane drive 자존 → **크루끼리 편 갈라 싸우는 모습이 같잖다는 냉소**. 단톡/DM/스토리/캡처/타임라인으로 번지는 online crew-chat 정치 이미지로 정리
  - ✅ **가사 톤 반복 보정**: 유치한 `안녕하세요/반갑습니다` 라임, 올드한 `잔/악수/체면/입술` 이미지, 식상한 `말끝만 갈라` 표현 제거. 현재 Verse 1 시작은 `피드는 새벽, DM은 빨라 / 스토리 위엔 불만 켜져`
  - ✅ **사운드 전환**: 175 BPM F Faster Dark Trap → **150 BPM B Rage Tuned Singing**. 이유: 한국어 라임 발음 뭉개짐 + final hook 댄스화 발생
  - ✅ **Suno 보정**: `[Final Chorus]` 제거, 반복 `[Chorus]`로 변경. `same locked 2-bar drum loop`, `no tempo increase`, `no final lift`, `no dance beat`, `no faster drums`를 STYLE/EXCLUDE/LYRICS/META에 모두 반영
  - ✅ **concept.md 동기화**: Track 17 `B | Male | 150`, 분포 `A3/B5/C5/D3/E2/F2`, Hard 65%로 갱신. v0.5 정정 사항에 Small Talk 전환 사유 기록
  - ⚠️ **검증 상태**: `check_lyric_avoid.sh 17_Small Talk.txt` PASS. `check_series_gate.sh SERIES/20-00/`는 현행 v1.4 목표(B4/F3, HIIT 5-7, A·B 인접 회피)와 충돌해 FAIL(S1/S2/S3). Small Talk를 B축으로 유지할지, 게이트/순서 재조정할지 다음 라운드 결정 필요.
  - **남은 TODO**: (1) Suno V5.5에서 현 `Small Talk` 버전 생성. (2) sing-rap hook이 영하게 들리는지, 한국어 발음이 유지되는지 확인. (3) 반복 Chorus에서 드럼/템포가 댄스곡처럼 바뀌면 FAIL 처리. (4) Small Talk PASS 후 Track Map 최종 순서/게이트 정책 재정렬. (5) PASS 시 Status/META 확정.

- **20-00 PASS/DRAFT 1-12 제목·가사·스타일 정합화 + Black Mirror femme fatale 보정** (2026-04-28 16차)
  - ✅ **사용자 제공 fixed 제목·스타일·가사 반영**: Night Rider, LLC, Bottom to the Top, Paycheck, Fake, Overtime Flame, Boomerang, Yang Gang, Cold Stack, Rewrite 중심으로 txt 본문/STYLE/LYRICS/META 정합화
  - ✅ **09 rename**: `Block Signal` → **Bottom Line**. 파일명 `09_Bottom Line.txt`, Track Map, concept.md, Side Street 참조까지 동기화
  - ✅ **12 Black Mirror 보정**: 기존 힙합 주제 보정 후 사용자 피드백 반영. `Black Mirror`는 영어 훅 키워드로 유지하고, 검은 화면 출근 같은 어색한 은유 제거. femme fatale club clock-in / red-light / seductive female dark trap 콘셉트로 재작성
  - ✅ **라임 방향 보정**: 영어 라임 과다를 줄이고 `비춰/낮춰/맞춰/갇혀/끌려` 계열 한글 라임으로 hook rhyme 정리. 식상한 `낮동안 삼킨 말들`류 표현 제거
  - ✅ **STYLE 동기화**: Black Mirror는 더 sexy/sultry한 female Korean dark trap 스타일로 조정. 단, 노골적 성적 묘사는 금지하고 차갑고 유혹적인 attitude로 제한
  - ✅ **이미지 포함**: 사용자 첨부 loop 이미지 `SERIES/20-00/input/new_loop.png`를 이번 푸시에 포함
  - ✅ **검증 PASS**:
    - `check_lyric_avoid.sh SERIES/20-00/input/tracks` PASS 20/20
    - `check_series_gate.sh SERIES/20-00/` PASS 7/7
  - **남은 TODO**: (1) Suno V5.5에서 draft 12곡 생성/검수. (2) PASS 곡만 `Status` 확정. (3) 20곡 PASS 후 강-약-중-강-약 최종 셔플. (4) 오디오 리네임 + YouTube Metadata + 패키징.

- **20-00 가사 = hip-hop 본연 정책 강화 + 5곡 교체 + 3곡 retheme** (2026-04-28 15차)
  - ✅ **사용자 피드백 반영**: "운동 컨셉보다 힙합 본연 주제로 조정. 안어울리는 트랙은 교체"
  - ✅ **Codex peer review FAIL → 모든 finding 수용 후 정비**
  - ✅ **5곡 컨셉 교체** (Style Prompt 그대로, lyrics 전체 새로):
    - 12 Black Interval (HIIT cardio) → **Black Mirror** (vanity vs 진짜, 검은 거울 응시)
    - 13 Dust Timer (locker post-workout) → **Old Cassette** (90s K-rap 회상 lyricism)
    - 16 Iron Set (마지막 set) → **Real Talk** (씬 비판 직설 디스)
    - 17 Tunnel Run (HIIT 터널) → **Late Lane** (새벽 도시 lane drive 자존)
    - 20 Last Echo (locker walk back) → **Old Page** (무대/cypher ritual lyricism, 13과 차별화)
  - ✅ **3곡 retheme** (제목·Style Prompt 유지, lyrics 운동 어휘 제거):
    - 14 Engine — 헬스장/덤벨/플레이트/세트/rep/근육 제거 → 8시 도시 시동 / 야간 그라인드. 심장박동=808 메타포 유지
    - 15 Concrete — 운동가방/단백질 셰이크/dumbbell/grip은 tax 제거 → 노동자 그라인드 (자수성가 = 힙합 코어) 강화
    - 19 Slow Glow — stretching mat/warmup/플레이트/round 제거 → 새벽 도시 introspective glow
  - ✅ **어색한 라인 정리**: 12 진짜 다리→진짜 자리 / 16 다 끝리→다 잠겨 / 15는 verse 3 전체 재작성으로 자연 해결
  - ✅ **20 Old Page Verse 3+ 재작성** — 13 Old Cassette(female 90s nostalgia writer at desk)와 차별화, male battle/cypher ritual angle (mic check / 무대 직전·후 / 한 줄에 다 거는 ritual / 동료 cypher) 적용
  - ✅ **concept.md v0.5 작성** — 라벨 정책(사운드 포지셔닝) 명문화, 최종 20곡 테마 표(hip-hop core), 4막 라벨 dual-read(사운드+narrative arc), Hard 70% 분배 검증 갱신, v0.5 정정 사항 5건 정리
  - ✅ **검증 PASS**:
    - `check_lyric_avoid.sh SERIES/20-00/input/tracks` PASS 20/20
    - `check_series_gate.sh SERIES/20-00/` PASS 7/7 (S1-S7)
  - **남은 TODO**: (1) 시리즈 라벨 최종 결정 — 현재 `💪 AFTER HOURS WORKOUT` 유지 권장 (Codex 의견). (2) 12곡 draft Suno V5.5 생성/검수. (3) PASS 곡만 `Status` 확정. (4) 20곡 PASS 후 강-약-중-강-약 최종 순서 셔플. (5) 오디오 리네임 + YouTube Metadata v0.5 + 패키징.

- **20-00 추가 7곡 draft 작성 + 20곡 게이트 PASS** (2026-04-28 14차)
  - ✅ **추가 7곡 draft txt 일괄 작성** (`SERIES/20-00/input/tracks/14-20_*.txt`)
    - 14 Engine (엔진) — B Male 150 BPM, LLC와 다른 male hip-hop edge tuned trap
    - 15 Concrete (콘크리트) — C Male 145 BPM, C4 husky/distorted/muddy 톤(미사용 분기) 콘크리트 그라인드
    - 16 Iron Set (아이언 셋) — A Male 154 BPM, Paycheck 변주, 마지막 set 기록 갱신 narrative
    - 17 Tunnel Run (터널 런) — F Male 175 BPM, Cold Stack 변주, HIIT 터널 시야 카운트다운
    - 18 Side Street (사이드 스트릿) — D Female 144 BPM, Rewrite 변주, 메인 도로 옆길 K-drill female
    - 19 Slow Glow (슬로우 글로우) — B Female 108 BPM, introspective 워밍업, 헤드폰 끼고 시동
    - 20 Last Echo (라스트 에코) — E Male 94 BPM, Dust Timer 남성 카운터파트, 운동 후 거울/라커룸/walk back home
  - ✅ **20곡 시리즈 게이트 7/7 PASS** (`./MASTER/scripts/check_series_gate.sh SERIES/20-00/`)
    - S1 곡수 분포 + Hard 60%+: PASS (A:3 B:4 C:5 D:3 E:2 F:3 = 20곡 / Hard 14 = 70%)
    - S2 BPM 분포: PASS (워밍업 2 / 메인 10 / HIIT 6 / 쿨다운 2)
    - S3 A·B 인접 회피: PASS
    - S4 시리즈 길이: PASS (73분 55초)
    - S5 Track 01 워밍업 B축: PASS (Night Rider B 112 BPM)
    - S6 마지막 멜로딕 마무리: PASS (Track 20 E 94 / 19 B 108 / 18 D 144)
    - S7 보컬 성별 분포: PASS (Male 14 / Female 6)
  - ✅ **20곡 가사 회피 PASS** (`./MASTER/scripts/check_lyric_avoid.sh SERIES/20-00/input/tracks` 20/20)
  - ✅ **draft 작성 패턴**: LLC/Night Rider/Overtime Flame full-lyrics 패턴 채택. 모든 트랙 8마디 호흡 포켓 + 3:20 이상 길이 룰 + Verse 3 + Final Chorus 포함
  - **남은 TODO**: (1) **Suno V5.5에서 12곡 draft 생성/검수** (02/06/09/12/13/14/15/16/17/18/19/20). (2) PASS 곡만 `Status` 확정. (3) 20곡 PASS 후 강-약-중-강-약 최종 순서 재배치. (4) 오디오 파일 리네임 (`NN__제목__영문__장르__BPM.wav`). (5) YouTube Metadata v0.4 확정 + 썸네일/loop.png + 패키징.

- **20-00 Track 06 `Overtime Flame` 클럽 열기 개사 + 호흡 포켓 실험** (2026-04-28 13차)
  - ✅ 사용자 요청 반영: `Overtime Flame`을 사무실 야근불 콘셉트에서 **after-hours club heat / neon / bass / floor 열기** 콘셉트로 개사
  - ✅ 도입부 룰 확정: **8 bars instrumental, 808 bass lead only**, 보컬/애드립/훅/bell melody 금지. bell melody는 intro 이후 Verse 1부터 진입
  - ✅ 호흡 이슈 대응: `No Vocal Break`가 Suno에서 잘 무시되어, 최종적으로 **A/B verse 구조 + [Ad-lib Pocket]** 방식 채택
  - ✅ `chant`가 어색하다는 피드백 반영: `Stop Chant`, `Bridge Chant`, 파일 내 `chant` 표현 제거. 포켓은 구호가 아니라 짧은 rapper aside(`huh/yeah/uh`)로 처리
  - ✅ `./MASTER/scripts/check_lyric_avoid.sh SERIES/20-00/input/tracks/06_Overtime Flame.txt` PASS
  - **남은 TODO**: 현 버전으로 Suno 생성 후 도입부 808-only 준수 여부, bell melody 진입 타이밍, Ad-lib Pocket 호흡감, club heat 콘셉트 정합성 검수

- **20-00 Track 03 `Bottom to the Top` 최종 PASS 기록** (2026-04-28)
  - ✅ 사용자 제공 원본 6 Verse 전문 반영
  - ✅ 8마디마다 `[Instrumental Break]` 1마디 구조를 넣었지만 실제 생성에서 호흡은 여전히 약함
  - ✅ 사용자 결정: 호흡은 거의 안 쉬지만 **PASS 유지**
  - ✅ 메타에 “호흡은 약하지만 최종 PASS” 기록

- **20-00 최종 20곡 체제 + 남성 14 / 여성 6 확정** (2026-04-27 12차)
  - ✅ **최종 트랙 수 복원**: 13곡은 현재 작업 세트, 최종은 **20곡**
  - ✅ **최종 축 분포 확정**: **A 3 / B 4 / C 5 / D 3 / E 2 / F 3 = 20곡**
    - Hard A+C+D+F = 14곡 (70%)
    - Non-Hard B+E = 6곡 (30%)
  - ✅ **보컬 성별 분포 확정**: **남성 14곡 / 여성 6곡**
    - 현재 13곡 계획상 M9/F4
    - 추가 7곡은 M5/F2로 배정
    - 01/03/05/07/08/10 txt 헤더에 누락된 `Vocal: Male` 메타만 보강해 현재 13곡 S7 카운트와 concept를 일치시킴
  - ✅ **추가 7곡 확장 슬롯**:
    - 14 B 신규 3 — Male, 148-152 BPM
    - 15 C 신규 5 — Male, 145-150 BPM
    - 16 A 변주 2 — Male, 152-156 BPM
    - 17 F 변주 2 — Male, 170-178 BPM
    - 18 D 변주 3 — Female, 142-146 BPM
    - 19 B 신규 4 — Female, 105-115 BPM
    - 20 E 보너스 2 — Male, 92-96 BPM
  - ✅ **문서/게이트 업데이트**:
    - `SERIES/20-00/concept.md` v0.4 — 20곡 + 성별 분포 + 추가 7곡 슬롯
    - `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` v1.4 — S7 성별 게이트 추가
    - `MASTER/scripts/check_series_gate.sh` v1.4 — TARGET 20곡 + S7 Vocal 메타 검사
  - ✅ **검증**:
    - `bash -n MASTER/scripts/check_series_gate.sh` PASS
    - `./MASTER/scripts/check_lyric_avoid.sh SERIES/20-00/input/tracks` PASS 13/13
    - `./MASTER/scripts/check_series_gate.sh SERIES/20-00/`는 20곡 기준 expected FAIL (현재 13곡, M9/F4, 길이 47:00)
  - **남은 TODO**: (1) 현재 draft 5곡(02/06/09/12/13) Suno 생성/검수. (2) 추가 7곡 중 14-20 설계/작사. (3) 전곡 `Vocal:` 메타 정리 후 20곡 기준 게이트 검증. (4) 전곡 PASS 후 강-약-중-강-약 최종 순서 재배치.

- **20-00 draft verse 길이 보강 룰 적용** (2026-04-28)
  - ✅ 사용자 피드백 반영: "3분이 안되네 좀 짧아" → 신규/draft는 실제 출력 최소 **3:20** 목표
  - ✅ `concept.md` LYRICS 작성 가이드 수정: `Length:` 메타만 믿지 말고 가사 본문에서 verse 분량 확보
  - ✅ `LLC (Low Light Code)` Length 3:45 + Verse 3 + Final Chorus 추가
  - ✅ `09_Block Signal` Length 3:45 + Verse 4 + 마지막 Refrain 추가
  - ✅ `12_Black Interval` Length 3:45 + Verse 3 + 반복 Final Chorus 지시 추가
  - ✅ `06_Overtime Flame`, `13_Dust Timer`에 3분 미만 방지 길이 룰 추가

- **20-00 변주 6곡 Suno draft + Track Map S6 정합화** (2026-04-27 11차)
  - ✅ **변주 6곡 draft txt 생성** (`SERIES/20-00/input/tracks/01/02/06/09/12/13_*.txt`)
    - Night Rider — B Rage Tuned after-dark, 112 BPM, PASS / 번호 없는 파일명
    - LLC (Low Light Code) — B Rage Tuned, 158 BPM, 번호 없는 파일명 + `Order: 02`
    - 06 Overtime Flame — A Rage Dry, 152 BPM, Paycheck 변주
    - 09 Block Signal — D K-Drill, 142 BPM, Rewrite 변주
    - 12 Black Interval — F Faster Dark Trap, 175 BPM, Cold Stack 변주
    - 13 Dust Timer — E 빡센 붐뱁, 92 BPM, 최종 쿨다운
  - ✅ **Track Map 정합화** (`SERIES/20-00/concept.md`)
    - 기존 13번 D축 마지막 배치가 S6와 충돌 → **E 붐뱁을 Track 13 최종 쿨다운으로 이동**
    - D 변주를 Track 09로 이동해 A/B 인접 회피 + S6 마지막 B/E 조건 충족
  - ✅ **`.gitignore` 보정**
    - `SERIES/*/input/tracks/*`는 계속 미디어 무시
    - `!SERIES/*/input/tracks/*.txt` 추가로 txt 프롬프트 추적 가능
  - ✅ **검증 통과**
    - `./MASTER/scripts/check_series_gate.sh SERIES/20-00/` → 당시 v1.3 기준 PASS 6/6 (draft 포함 13곡, 47:00)
    - `./MASTER/scripts/check_lyric_avoid.sh SERIES/20-00/input/tracks` → PASS 13/13
    - 이후 v1.4에서 20곡 기준으로 올라갔기 때문에 현재 13곡 세트는 `check_series_gate.sh` expected FAIL 상태
  - ⚠️ **상태 주의**: Night Rider는 PASS. 02/06/09/12/13 5곡은 `Status: DRAFT - Suno test pending`.
  - ✅ **2026-04-27 추가 운영 룰**: 타이트한 랩 스타일은 8마디마다 숨표/애드립/반마디 포켓을 둔다. 숨 없이 16마디 이상 밀지 않음. 01 Night Rider는 사용자 PASS 버전 유지, 02/06/09/12/13 draft에 호흡 룰 반영.
  - ✅ **2026-04-27 추가 보정**: 01 제외 전체 txt(02-13)에 "덜 raw하되 BPM/808/hi-hat density 유지" 지시 반영. 기존 PASS 트랙은 결과물 유지, 재생성/변주용 운영 룰만 추가.
  - ✅ **2026-04-27 순서 정책**: 현재 Track Map은 제작/검증용 임시 배치. 20곡 PASS 후 최종 순서는 **강-약-중-강-약** 흐름으로 다시 섞는다.
  - ✅ **2026-04-27 보컬 성별 정책 정정**: 최종 20곡은 **남성 14 / 여성 6**. 기존 PASS 트랙은 txt에서 임의 성별 재라벨링 금지. 현재 13곡 계획상 M9/F4, 추가 7곡은 M5/F2.
  - **남은 TODO**: (1) Suno V5.5에서 draft 5곡 각 2-3회 생성. (2) 사용자 정성 PASS/FAIL. (3) PASS 곡만 `Status/META` 확정. (4) 14-20 추가 7곡 설계/작사. (5) 20곡 오디오 파일 리네임 후 패키징.

- **20-00 7곡 일괄 검토 + RUBRIC v1.3 + concept v0.3 + 13곡 분포 + F축 신설** (2026-04-26 10차)
  - ✅ **7곡 일괄 검토 PASS** (사용자 결과물 정성 평가 우선)
    - 1. Rewrite (D K-Drill) — 90점, NY/Brooklyn drill hybrid
    - 2. Bottom to the Top (C lazy monotone) — chest voice + 808
    - 3. Fake (C 디스 sarcastic) — Hook "Fake! Fake!" 강력
    - 4. Boomerang (C 디스 sarcastic) — Hook "부메랑" 강력
    - 5. Paycheck (A Rage Dry, 매칭 정정 B→A) — 대만족 / 가사 메타 우선
    - 6. Cold Stack (F Faster Dark Trap, 신규 축) — 새로운 스타일
    - 7. Yang Gang (C chant gang hook) — 결과 minor + workout
  - ✅ **/coach 옵션 2 채택** (B축 우선 + boombap 보너스 + 변주 베이스 활용 균형)
  - ✅ **RUBRIC v1.3 보정 7개 항목** (`MASTER/rubrics/HARD_HIPHOP_RUBRIC.md`):
    1. H4 한국어 비중 룰 → 권장만 감점 X (코드스위치는 한국 본가 표준)
    2. 메타태그 [Bridge] [Pre-Chorus] [Chorus] [Final Chorus] **인정** (이전 v1.0 금지 룰 폐지)
    3. **F축 신설** — Faster Dark Trap 165-180 BPM hub (Cold Stack 후행 인정)
    4. C축 톤 분기 4가지 명시 (husky/distorted/muddy / lazy monotone deadpan / 디스 sarcastic / chant gang hook)
    5. B축 introspective laid-back 변종 명시 (Travis Scott Astroworld)
    6. BPM 룰 확장 140-160 → 140-180
    7. 사운드 우선 정책 명문화 — "가사 내용 크게 중요하지 않아, 사운드 톤앤매너만" (사용자 정정)
  - ✅ **concept.md v0.2 → v0.3** (`SERIES/20-00/concept.md`)
    - 곡수 20곡 → **13곡 축소** (사용자 "지금까지 7곡 + 변주 6곡")
    - 분포: **A 2 / B 2 / C 4 / D 2 / E 1 / F 2 = 13곡** (Hard A+C+D+F = 10곡 77%, Hard 60% 정책 충족)
    - 변주 6곡 슬롯: A 변주 1 / B 신규 2 / D 변주 1 / F 변주 1 / E 보너스 신규 1
    - Track Map 4막 × 13곡 스켈레톤 재작성
    - 5축 + 보너스 Style Templates (7곡 PASS Style Prompt 그대로 인용)
    - EXCLUDE v4 (F축 추가)
    - QA 체크리스트 사운드 우선
  - ✅ **`check_series_gate.sh` v1.3 수정**:
    - TARGET 13곡 + F축 추가
    - Hard 60% minimum threshold (정확 60% → 60%+ 충족)
    - 시리즈 길이 60-90분 → **40-65분** (13곡 기준)
    - S6 룰 완화 (마지막 1-2곡 중 하나는 B/E)
    - 12-00 시리즈로 재테스트 통과 (다른 RUBRIC FAIL 정상)
  - ✅ **7곡 메타 파일 생성** (`SERIES/20-00/input/tracks/03~11_*.txt`)
    - Track Map v0.3 슬롯 정착 (03/04/05/07/08/10/11)
    - Style Prompt + 가사 요약 + RUBRIC 매칭 + PASS 일자 메타
    - 변주 슬롯 비어 있음 (01/02/06/09/12/13)
  - ⚠️ **남은 변주 6곡** (사용자 작업, 1-2시간):
    - A 변주 1 (Paycheck Style 베이스, 신규 가사)
    - B 신규 2 (베이스 없음, RUBRIC v1.3 §Style B Suno Prompt 2종 활용)
    - D 변주 1 (Rewrite Style 베이스, 다른 가사)
    - F 변주 1 (Cold Stack Style 베이스, 다른 가사)
    - E 보너스 신규 1 (붐뱁 Style)
  - **남은 TODO**: (1) 변주 6곡 Suno 작업. (2) 6곡 결과 PASS/FAIL → RUBRIC v1.4 미세 조정 필요 시. (3) 13곡 누적 후 `check_series_gate.sh` PASS 검증. (4) 시리즈 패키징 (썸네일·YouTube 메타). (5) 미해결 5건 다음 라운드 (Loopy MARNI 청취 / K-FLIP+ BPM / 헬스 인플루언서 BGM / Spotify Korea Workout / YouTube Music).

- **20-00 HARD_HIPHOP_RUBRIC v1.1 + 자동화 스크립트 2건 + Hard 60% 정책 반영** (2026-04-26 9차)
  - ✅ **/team Decision Meeting** (실행 플랜): PL + EL Round 1 + QA Round 2 만장 (평균 93점). 순서: 루브릭 v1.0 → 사용자 검토 → 스크립트 + Suno 병렬. MVP 정책 (스크립트 50 키워드 + 6 게이트, 단위 테스트 v1.1). 회의록: `meetings/2026-04-26_20-00-genre-gate-execution-plan.md`
  - ✅ **사용자 정책 결정**: **Hard 비중 60%** (A Rage Dry + C Hardcore Trap + D K-Drill = 12곡 / B Tuned + 보너스 붐뱁 = 8곡, 20곡 확정)
  - ✅ **HARD_HIPHOP_RUBRIC.md v1.1 작성** (225줄) — 4단 구조: Hard Gates 8 + Style-Specific Gates 13 + 8-Factor Scoring 100점 + Series Gates 6
    - Hard Gates 8개 (H6/H8 자동화 → 실질 수동 6개)
    - Style Gates 13개 (A 3 + B 4 + C 2 + D 3 + E 2)
    - 8-Factor 100점 (Trap Groove 15 / 808 10 / Hook&Adlib 15 / Korean Vocal 15 음성만 / Energy 10 / Workout BPM 10 / Production 15 / 장르 정체성 10)
    - Series Gates 6개 모두 자동화
    - Style Checklist 8축 표 + 운영 워크플로우 + 자동화 스크립트 인터페이스 예시
  - ✅ **`MASTER/scripts/check_lyric_avoid.sh` 작성** — H8 가사 회피 자동 검사
    - 50 키워드 5카테고리: 폭력·살해(10) / 마약(10) / 혐오(10) / 자해·자살(10) / 노골적 성행위(10)
    - **K-Drill 본가 어휘(갱·크루·블록·동네·디스·flex·돈·자랑·반항) 회피 X 보존**
    - PASS/FAIL + 매칭 키워드 카테고리별 출력
    - 단일 파일 + 디렉토리 모두 지원
    - 테스트 통과 (PASS 케이스 / FAIL 케이스 정확)
  - ✅ **`MASTER/scripts/check_series_gate.sh` 작성** — S1-S6 시리즈 자동 검증
    - 트랙 메타 파일 헤더 파싱 (Type/BPM/Length)
    - S1 곡수 분포 + Hard 60% (A 4/B 5/C 5/D 3/E 3 = 20곡 / Hard 12·Non-Hard 8)
    - S2 BPM 4단계 분포 (워밍업 100-120 / 메인 130-150 / HIIT 140-180 / 쿨다운 90-110)
    - S3 A·B 인접 회피 (시퀀스 검증)
    - S4 시리즈 길이 60-90분 합산
    - S5 Track 01 = B축 + BPM 100-120
    - S6 마지막 곡 = B 또는 E + BPM 90-115
    - 12-00 시리즈로 작동 테스트 통과 (다른 RUBRIC이라 FAIL 정상)
  - ✅ **concept.md v0.2 → v0.2.1 업데이트** (Hard 60% 반영)
    - §Series Status 배분: A 4 / B 5 / C 5 / D 3 / 보너스 3 = 20곡 (Hard 60% 명시)
    - §Style Templates 곡수: A 4 / C 5 / 보너스 3 (각 헤더 수정)
    - §Track Map v0.2 4막 × 20곡 스켈레톤 재작성 (Track 19에 A Rage Dry 추가로 Hard 60% 보강 / 마지막 Track 20만 B 멜로딕)
    - §QA 시리즈 PASS 기준: A 4 / B 5 / C 5 / D 3 / 보너스 3 = 20곡 Hard 60%
  - **남은 TODO**: (1) **Suno V5.5 5곡 1차 테스트** (A Dry / B Tuned / C Hardcore / D K-Drill / 보너스 붐뱁 각 1) → 루브릭 v1.1 PASS/FAIL 판정. (2) 통과 가사 2건 복원 결정 (사용자 pending) — `불붙은 paycheck` (A) / `씬에 침 뱉어` (D) git history `ec04577` 이전. (3) 5곡 테스트 결과 기반 루브릭 v1.2 미세 조정. (4) 미해결 5건 다음 라운드 (Loopy MARNI 청취 / K-FLIP+ BPM / 헬스 인플루언서 BGM / Spotify Korea Workout / YouTube Music).

- **20-00 시리즈 장르 게이트(루브릭) v1.0 설계 — /team 만장 합의** (2026-04-26 8차)
  - ✅ **/team Trade-off Discussion** (Product Leader + Marketing Director + Engineering Lead Round 1 + QA Reviewer Round 2)
  - ✅ **5개 안건 만장 합의** (평균 94.6점, 모든 Gate 개별 PASS, G5 90 BORDERLINE)
    - **안건 1 — Hard Gates 8개**: BPM(86-95 OR 140-160) / Drum Pattern / Bass / Vocal Korean Hard Rap / Hook / EXCLUDE 공통 / Workout 사운드 정합 / 콘텐츠 회피 (H6/H8 자동화)
    - **안건 2 — Style-Specific Gates 13개**: A Dry 3(no autotune/blown-out/short reverb) + B Tuned 4(autotune 시그니처/melodic chorus/cathedral reverb/KC vangdale 광택) + C Hardcore 2(husky/distorted 808+dark piano) + D K-Drill 3(sliding 808/drill snare/된소리+다크) + E 붐뱁 2(dusty drum/라이리시즘). **A1 vs B1 = 시리즈 핵심 차별점** (Section A.3.4 EXCLUDE 분리표 게이트화)
    - **안건 3 — 8-Factor Scoring 100점**: F1 Trap Groove 15 / F2 808 10 / F3 Hook&Adlib 15 / F4 Korean Vocal Identity 15(음성·발음·톤만, 가사 X) / F5 Energy Arc 10 / F6 Workout BPM 단계 매칭 10 / F7 Production 15 / F8 장르 정체성 10. 판정 85+ PASS / 70-84 BORDERLINE / <70 FAIL / Critical Fail = 개별 Factor ≤30%
    - **안건 4 — 가사 자유 정책 게이트 반영**: F4 음성만 / 가사 = Hard Gate H8 회피 영역 자동 grep 50개 키워드 5카테고리(폭력·살해/마약/혐오/자해/노골적성) / K-Drill 본가 어휘(갱·크루·블록·동네·디스) 보존 / 라이리시즘은 보너스 붐뱁 E2만 점수화
    - **안건 5 — Series Gates 6개**: S1 곡수 분포(A 3-4/B 5/C 5-6/D 3/보너스 2-3=18-21곡) / S2 BPM 분포(워밍업 100-120 / 메인 130-150 / HIIT 140-180 / 쿨다운 90-110) / S3 A·B 인접 회피 / S4 60-90분 / S5 Track 01 워밍업 B축 / S6 마지막 2-3곡 멜로딕(B+보너스). 6개 모두 자동화 가능
  - ✅ **충돌 해소 3건**:
    - MD "H7 자동화 부담" vs EL "자동 grep 비용 0" → **EL 승**
    - EL "F6 점수화 어려움" vs PL "곡 단위 평가 필요" → **PL 절충 (BPM 단계 분류만)**
    - EL "Style Gate 16개 너무 많음" vs PL "13개 축소" → **PL 승 (C·D BPM Hard Gate 중복 제거)**
  - ✅ **QA Round 2 판정**: PASS (평균 94.6, 모든 Gate ≥90, G5 운영 효율만 BORDERLINE 90 — Style Gate 13개 다소 많음 추후 11개 축소 검토 가능)
  - **남은 TODO**: (1) `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` v1.0 작성 (위 4단 구조). (2) 자동화 스크립트 2개 — `MASTER/scripts/check_lyric_avoid.sh` (가사 회피 50 키워드 grep) + `MASTER/scripts/check_series_gate.sh` (S1-S6 자동 검증). (3) Suno 1차 5곡 테스트 (A/B/C/D/보너스 각 1) → 루브릭 v1.0 PASS/FAIL 판정 → v1.1 조정. (4) 통과 가사 2건 복원 결정 (사용자 pending).
  - **산출물**: `meetings/2026-04-26_20-00-genre-gate-rubric-design.md`

- **20-00 `💪 AFTER HOURS WORKOUT` concept.md v0.2 + P0 갭 보충 리서치 통합 + 가사 가이드 정정** (2026-04-26 7차)
  - ✅ **P0 갭 보충 리서치 2건 병렬 호출** (researcher × 2, 각 백그라운드, 약 10-19분):
    - **Section A** (Korean Tuned Singing Rage Trap 정밀): 시간순 정리 2023-2026 / KC 라인업(Sik-K·HAON·Lil Moshpit·Vangdale·NOWIMYOUNG·JMIN) + Loopy MARNI + Jvcki Wai MOLLAK 검증 / K-FLIP+ PUBLIC ENEMY 161 BPM E minor 확정 / 글로벌 Dry vs Tuned 보컬 체인 비교(Carti·Yeat·Travis·Don Toliver retune speed·formant·reverb tail) / Suno V5/V5.5 키워드 분리표(Dry/Tuned 정체성 보호 EXCLUDE 분리) / 검증된 Suno Rage 프롬프트 5건 / Korean 권장 프롬프트 템플릿 2종. 신뢰도 72%
    - **Section B** (Workout K-rap 페르소나 + 한국 운동 BGM): Bugs/Melon/Apple Music 7건 큐레이션 분석 → 한국 헬스장 큐레이션 = K-pop·외산 팝·EDM 우세, 빡센 트랩 0% / "격하게 운동할 때 듣는 힙합" Apple Music 15곡 = 외산 트랩·Rage rap 80%+ Korean rap 0% **빈자리** / 직장인 헬스 30.9%(1위)·러닝 +232%(30대 1위)·76.4% 저녁 운동·헬스장 매장 30대 25.6% / K-Drill BPM·사운드 PASS 가사 무드 부조화 / 시리즈 가설 **CONDITIONAL PASS** + Korean Workout Hip-Hop 빈자리 채우기 명분. 신뢰도 80%
    - 산출물: `SERIES/20-00/report/2026-04-25_workout-tuned-rage-supplement.md` (50KB)
  - ✅ **concept.md v0.2 작성** (497줄, 신규 — v0.1 리셋 후 새로 작성):
    - **시리즈 라벨 `💪 AFTER HOURS WORKOUT`** 확정 (Section B 페르소나 검증 PASS)
    - **신 4축 + 보너스 곡수 절충안**: A Rage Dry 3-4 / B Rage Tuned 5 / C Hardcore Trap 5-6 / D K-Drill 액센트 3 / 보너스 빡센 붐뱁 2-3 = **18-21곡** (Section A 권장 A 2-3 + Section B 권장 A 5-6 가운데 절충)
    - **Style Templates 5종** Section A.3 Suno 키워드 분리표 인용 + Paycheck v3 통합 + KC vangdale 광택 디자인 시그니처 반영
    - **EXCLUDE v3 축별 특화표** (A Dry/B Tuned 정체성 보호 분리)
    - **Workout 배치 룰** (운동 단계별 BPM 매칭): 워밍업 100-120 (B) → 메인 130-150 (C+A+보너스) → HIIT 140-180 (C+D) → 쿨다운 90-110 (B+보너스 붐뱁)
    - **Track Map v0.2** 4막 × 19-21곡 스켈레톤 + 배치 원칙 (Track 01 워밍업 / A·B 인접 회피 / 마지막 2-3곡 멜로딕)
    - **LYRICS 가이드** Verse 16 bar 표준 + 메타태그 금지 (`[Final Hook]`/`[Drop]`/`[Bridge]`) + Refrain 4행 축약
    - **QA 체크리스트** 곡별 + 시리즈 + FAIL 패턴 대응표
    - **YouTube Metadata v0.2** 초안 (제목/태그/해시태그/설명 템플릿)
  - ✅ **정정 사항 v0.2 반영** (Section A.7):
    - SMTM12 = **2026-01-15 프리미어 / 2026-04-02 결승 / HAON 우승** (1차 1162줄 리포트 명시 안 됨)
    - Loopy `MARNI` 메인 PD = **SanityTooFye** (일부 자료의 Dayrick은 잘못)
    - NOWIMYOUNG = electropop 비중 → B축 단순 편입 부적합, "인접 사례"로만
    - MOLLAK (Jvcki Wai × Vangdale 2025-07-04) = **Female Korean Tuned Singing Rage 인접 신규 사례** (1차 §3.5 "Female 부재" 정정)
  - ✅ **사용자 피드백 정정** (2026-04-26): "가사까지 workout일 필요는 없어. 그냥 트랙들의 톤앤매너(BPM이나 에너지)만 workout스러우면 돼"
    - **§핵심 원칙 → 코어**: "운동 텐션 + 그라인드 정서 표현" → "일반 하드 힙합 자유 서사. Workout 어휘 강제 X — Workout 정합은 사운드(BPM·에너지·페이스)에서만"
    - **§Style D**: "K-Drill Workout 액센트" → "K-Drill 액센트". 가사 리라이트 필수 → 본가 무드 자유. 회피 영역만 명시 (무차별 폭력·살해·총기·마약 직접 묘사)
    - **§LYRICS 공통 원칙 6번**: "Workout 어휘 우선" → "주제 자유 (퇴근·도시·디스·자랑·반항·내면). 회피 영역만"
    - **§주제 어휘 풀**: 운동 어휘 강제 → 자유 영역 + 회피 영역
    - **§QA 체크리스트**: "Workout 어휘 정합" → "주제 자유 / 회피 영역 미사용"
    - **§D축 통과 가사 복원**: "Workout 가사 리라이트 필수" → "본가 K-Drill 무드 유지"
    - 메모리 저장: `~/.claude/projects/-Users-zenkim-office/memory/feedback_wavvy-lyrics-vs-sound-separation.md` (시리즈 컨셉 정합 = 사운드 영역, 가사는 자유)
  - ⚠️ **미해결**: (1) 통과 가사 2건 복원 결정 — `불붙은 paycheck` (A Rage Dry 정합 ✅) / `씬에 침 뱉어` (D K-Drill 본가 무드 유지) git history `ec04577` 이전 commit에서 복원 가능, 사용자 결정 대기. (2) Loopy MARNI 11곡 곡별 BPM/Key + 보컬 처리 청취 검증 (Confidence 40%). (3) K-FLIP+ 10곡 곡별 BPM (PUBLIC ENEMY 161 외 미확보). (4) 헬스 인플루언서 BGM AHA Music·Shazam 직접 식별. (5) Spotify Korea 공식 워크아웃 플레이리스트 직접 분석.
  - **남은 TODO**: (1) 통과 가사 2건 복원 결정. (2) Suno V5.5 5곡 1차 테스트 (A Dry / B Tuned / C Hardcore / D K-Drill / 보너스 붐뱁 각 1곡). (3) 3+ PASS 시 19-21곡 확장. (4) 미해결 5건 다음 라운드.

- **20-00 Paycheck 인사이트 B~D 확산 + EXCLUDE 축별 특화 + Rewrite 4차 수용 + Verse 16 bar 표기** (2026-04-25 6차)
  - ✅ **concept.md §Style A 반영 완료** (5차 "일단 통과" 해결) — v3 Style Prompt (`same 2-bar trap drum loop throughout no beat switch no final lift` 앞쪽, `screamed raw shouted + chest voice dry close vocal`, autotune 제거, `raw uncut rage energy`, `dense ad-libs between rap lines`) + EXCLUDE v2 rage 13종 + 가사 구조 (Refrain 4행, `[Hook]/[Final Hook]/[Drop]` 금지 메타태그)
  - ✅ **서사 아크 6단 "자유"로 격하** (사용자 피드백 "서사 아크는 필수가 아냐") — Paycheck 6단은 예시 수준으로만 표기
  - ✅ **test-prompts.md §곡 1 Paycheck** Style v3 + EXCLUDE rage v2 동기화
  - ✅ **B/C/D 축별 EXCLUDE 특화 재설계** (각 13종, 공통 5종 `sung hook, drum fill, beat switch, double-time drums, halftime switch`)
    - **B K-Drill**: `+ amapiano, jersey club, trap 808 sustain` (Drill→Trap hybrid drift 차단)
    - **C Boom bap**: `+ auto-tune` (80s-90s chest voice 무드 보존, C축만 auto-tune 추가) + `synth FX, EDM FX` 유지
    - **D Hard Trap**: `+ EDM drop, pitch-shifted vocals, glitch drums` (Rage drift 차단 최강화) — `32nd triplet burst, vocal chop` 미포함(D축 시그니처)
  - ✅ **B/D Style Prompt 비트 고정 앞쪽 배치** (A축 v3 패턴 준용) — D축 `no beat switch no final lift` 최강(Rage 인접)
  - ✅ **B/C/D chest voice 명시 강화** (Wavvy DNA) — B `chest voice dry close vocal` / C `chest voice dry close vocal` 독립 배치 / D `chest voice` (husky 공존)
  - ✅ **Rewrite(씬에 침 뱉어) 4차+5차 재설계 수용**
    - 4차: V1-V6 → V1-V4 (V5/V6 삭제), Pre-Hook 제거, Refrain 4회 교대, Refrain 가사 고유화(뱉어/place/mistake/trace), V3/V4 완전 교체(가면 디스 / 반격·판 접기), V1/V2 부분 수정(crash/freeze/증명/dust/rust/fold)
    - 5차 EXCLUDE 수정: Rage v2 13종 오적용 → B축 특화 13종 (사용자 "rage 전용 exclude는 내 실수" 교정)
  - ✅ **test-prompts.md §곡 2/3/4 동기화** — Style Prompt v2 + EXCLUDE 축별 특화 13종
  - ✅ **Verse 16 bar 표준 표기 반영** (사용자 "플랜+테스트 프롬프트 V1~V6 16마디 반영 안 됨" 지적)
    - concept.md §Style A "Verse 2택" → **16 bar 단일 표준** + Paycheck 완성 트랙 예외 명시 (다른 A축 3곡 Track 03/07/18은 16 bar 표준 적용)
    - concept.md §Style B "V3-V6 NEW" → "V1-V4 각 16행 = 64 bar" 정정 (Rewrite 4차 구조 반영)
    - test-prompts.md §곡 2: `V1(16 bar) → Refrain①(4 bar) → ... → V4(16 bar) → Outro` 명시 (64 bar + 16 bar)
    - test-prompts.md §곡 3 Come Up: `### 구조` 섹션 신규 + 약칭 `I-V1(16)-H(4-8)-V2(16)-H-V3(16)-O` + LYRICS 프롬프트 `Verse 16 bars each (4 lines × 4 blocks)` 추가
    - test-prompts.md §곡 4 Paranoia: `### 구조` 섹션 신규 + 약칭 `I-V1(16)-PH(4)-H(8)-V2(16)-PH-H-O` + LYRICS 프롬프트 `Verse 16 bars each` 추가
  - ⚠️ **Paycheck 미변경** (사용자 지시 "paycheck은 신경쓰지 말고 이미 완성했으니까") — V6 × 8행 완성 트랙 유지, 신규 16 bar 확장 없음
  - **현황**: 4곡 Suno V5.5 재테스트 대기 — 각 축 특화 EXCLUDE 효과 관찰 + Rewrite 4차 구조(Pre-Hook 제거 + Refrain 4회) 효과 검증
  - **남은 TODO**: (1) Suno 4곡 재테스트 (§곡 1 Paycheck v3 / §곡 2 Rewrite 4차 / §곡 3 Come Up C v2 / §곡 4 Paranoia D v2). (2) FAIL 패턴 축별 관찰 후 EXCLUDE v2 조정 판단. (3) 3+ PASS 시 20곡 확장. (4) A축 Paycheck 제외 3곡(Track 03/07/18) 신규 제작 시 Verse 16 bar 표준 적용. (5) 3/4번 제목(`Come Up`/`Paranoia`) 사용자 확인.

- **20-00 Paycheck/Rewrite 가사 Verse 6 확장 + Rage Style v3 + Verse 16 bar 표준 정립** (2026-04-25 5차)
  - ✅ **외부 분석 검토** — GPT-5 등 다른 세션에서 받은 Rage Trap 비트 스위치 트러블슈팅 분석 (~14단 진단). 핵심 새 인사이트 수용:
    - `supersaw`가 EDM 드롭 트리거 (그러나 완전 제거 시 rage 정체성 상실 → supersaw 유지, 다른 요소로 균형)
    - Style Prompt 앞쪽이 Suno 우선순위 → 비트 고정 지시 앞쪽 배치
    - Hook 8행 × 2회 + Final Hook 구조 자체가 Suno drop 유도 → Refrain 4행 축약 + Final 삭제
    - `rage trap` 용어 후반 폭주 해석 경향 (단, 완화하면 rage 상실 → 용어 유지 + 내부 키워드 조정)
    - Cover / Extend / 파라미터 낮춤 운영 처방
  - ✅ **Rage Style Prompt v3 도출** — 균형점: `Korean rage trap, 150 BPM, same 2-bar trap drum loop throughout no beat switch no final lift, distorted sliding 808 bass hard clipped low end, rolling 1/16 hi-hats steady, supersaw 7-voice detuned sustained stab, simple dark bell melody, screamed raw shouted male Korean rap, chest voice, dry close vocal, sharp articulation, dense ad-libs between rap lines, raw uncut rage energy, gritty lo-fi saturation, hard rap only`
    - 비트 고정 앞쪽 / supersaw 유지 / rage 정체성 유지 / `32nd triplet burst` 삭제 / `vocal chop` 삭제 / `mosh pit energy` → `raw uncut rage energy` / `loud master` 삭제 / `high density ad-lib layer` → `dense ad-libs between rap lines` (layer 제거)
  - ✅ **EXCLUDE v2 13종** — rage 특화 (기존 10종과 상당히 다름)
    - `EDM drop, vocal chop, vocal stutter, pitch-shifted vocals, beat switch, drum fill, double-time drums, halftime switch, breakbeat, glitch drums, riser, sung hook, 32nd triplet burst`
    - 제거: `k-pop, melodic singing, four-on-the-floor, arpeggiated synth, synth FX, EDM FX`
    - 추가: `EDM drop, vocal chop, vocal stutter, pitch-shifted vocals, beat switch, double-time drums, halftime switch, breakbeat, glitch drums, riser, 32nd triplet burst`
  - ✅ **Paycheck 가사 Verse 6 확장** — `input/tracks/불붙은 paycheck (Paycheck on Fire).txt`
    - 기존 Verse 2개 × 8행 + Hook 반복 → Verse 6개 × 8행 + Refrain 3번 구조
    - 서사 아크 6단: 허슬(V1) → 의심 극복(V2) → 크루/자립(V3 NEW) → 반격/증명(V4 NEW) → 상승/지속(V5 NEW) → 최종 선언(V6 NEW)
    - 기존 V3(shade/sent it back) 폐기 — V2와 80% 유사 문제
    - Refrain 배치: V1 뒤 / V2-V3 뒤 / V4-V5 뒤 · V6 뒤 Outro 직행 (final drop 유도 차단)
    - 라임 스킴 6Verse 교차 설계: V1 -eep · V2 -ack · V3 -ire/-own · V4 -op/-ight · V5 -ay/-est · V6 -urn/-ine
    - Paycheck 파일에 `=== STYLE ===` / `=== EXCLUDE ===` 섹션 추가 (12-00 Afrobeats 포맷 준용)
  - ✅ **Rewrite(씬에 침 뱉어) 가사 Verse 6 확장** — `input/tracks/씬에 침 뱉어 (Spit on the Scene).txt`
    - V1/V2 12행 → 16행 확장 (각 4번째 블록 추가: V1 fake/week/peek/freak, V2 fake/make/stay/retake)
    - V3-V6 NEW 16행씩 작성 (크루/반격/장악/선언)
    - 구조: V1 → Pre-Hook → Refrain → V2 → V3 → Refrain → V4 → V5 → Pre-Hook → Refrain → V6 → Outro
    - Pre-Hook 2번 (drill tension 빌드 특성 유지), Refrain 3번
    - `[Hook]/[Final Hook]` → `[Refrain]` 통일 (Paycheck 구조와 통일)
  - ✅ **Verse 16 bar 표준 정립** — `concept.md §LYRICS 작성 가이드` 기본 원칙 5번 추가
    - "힙합 씬 표준. 짧은 Verse(8 bars)는 Suno 조기 종료 유도 + 곡 길이 1분대 문제 원인. 4행 × 4블록 = 16행이 기본"
    - Style D 가사 구조 권장에 Verse bar 표기 통일 (`Verse 1 (16 bar) → Pre-Hook → Hook (chant) → Verse 2 (16 bar) → ...`)
    - Style A/B/C는 기존부터 16 bar 표기 있었음
  - ⚠️ **부분 미반영** — "일단 통과":
    - concept.md Style A Template Style Prompt + EXCLUDE 전체 반영 실패 (Edit old_string mismatch)
    - test-prompts.md 1번 Paycheck Style Prompt + EXCLUDE v3/v2 반영 보류
    - paycheck.txt에만 Style v3 + EXCLUDE v2 반영됨 (파일 간 불일치 상태 의도적 유지)
  - **현황**: Suno V5.5 재테스트 대기 — Paycheck/Rewrite 풀 가사 + Style A 기존(미반영)으로 먼저 생성 → 결과 보고 concept.md / test-prompts.md 전체 반영 여부 결정
  - **남은 TODO**: (1) 3/4번 제목(`Come Up`/`Paranoia`) 사용자 확인. (2) concept.md Style A Template 반영 재시도 or 통과 확정. (3) Rewrite 파일 Style + EXCLUDE 섹션 추가 여부.

- **20-00 Suno 프롬프트 대대적 튜닝** (2026-04-25 4차) — Wavvy 첫 힙합 시리즈 방어막 구축
  - ✅ **샘플링 키워드 4축 전부 추가** (사용자 요청: 샘플 소스 영어 무관)
    - A Rage: `pitched-up vocal chop sample top layer`
    - B K-Drill: `flipped soul sample melodic hook pitched-up chop`
    - C Boom bap: `chopped 70s-80s soul or ballad sample loop with vinyl crackle` (Korean 한정 → 범용)
    - D Hard Trap: `dark pitched vocal sample loop minor key`
  - ✅ **`singing in Korean` → `rapping in Korean`** 전 프롬프트 교체 — 보컬 드리프트 방지 (멜로딕 싱잉 차단)
  - ✅ **EXCLUDE 3 → 10종 확장** (V5.5 안정, 12-00 선례 9개 근거)
    - 공통 6종: `melodic singing, four-on-the-floor, drum fill, double-time switch, sung hook, arpeggiated synth, electronic riser, synth FX, EDM FX`
    - 축별 1종: A/B/D `k-pop` · C `trap`
    - 각 증상 → EXCLUDE 매핑: 멜로딕 싱잉 / 테크노 쿵짝 / 드럼 필인-배속 전환 / 훅 노래화 / 전자 아르페지오-스터터 반복 / sweep-riser-EDM FX 삽입
  - ✅ **Style Prompt Positive 다층 지시** (전축 공통 꼬리)
    - `locked drum pattern throughout no fills no switch-up`
    - `hard rap only no singing`
    - `no arp synth no stutter loop`
    - `rapping in Korean`
  - ✅ **보컬 디스크립터 rap 밀도 강화**
    - A Rage: `screamed autotune male vocal` → `screamed autotune male rap vocal`
    - D Hard Trap: `husky male vocal` → `husky male rap vocal`
  - ✅ **악기 디스크립터 반복 키워드 제거**
    - D Hard Trap: `muted electric guitar arpeggio minor key` → `muted electric guitar chord minor key`
    - A Rage (test): `supersaw 7-voice detuned short staccato loop` → `supersaw 7-voice detuned sustained stab`
  - ✅ **Bridge 제거 + Chorus/Pre-Chorus → Hook/Pre-Hook**
    - 4축 가사 구조 권장에서 Bridge 섹션 제거 (`[Bridge]`가 노래로 변주 유도 원인)
    - concept.md §LYRICS 가이드 메타태그 업데이트 (Style B/D)
    - 약칭 구조 `B` 제거, `PH = Pre-Hook` 도입 (20-00 전용)
    - test-prompts.md BLOCK/INSOMNIA 약칭: `I-V1-H-V2-H-B-H-O` → `I-V1-PH-H-V2-PH-H-O`
  - ✅ **4곡 재설계**
    - **1 `Paycheck`** (한글 `불붙은 paycheck`) — A Rage / Suno 샘플 PASS 가사 Custom Mode 풀 가사 입력. 새벽 허슬·돈·바닥→상승
    - **2 `Rewrite`** (한글 `씬에 침 뱉어`) — B K-Drill / Suno 샘플 PASS 가사 Custom Mode. 씬 디스·가짜 vs 진짜·판 뒤집기. 사용자 공유 프롬프트(`NY Drill Hiphop, rap lyrics. Korean. perfect rhyme use korean with english. about disrespect the scene with strong korean slang.`) 결과 PASS
    - **3 `Come Up`** (한글 `올라와`) — C Boom bap 작사 프롬프트. 바닥→상승 서사·밤 그라인드·펜→마이크·한국 거리→무대
    - **4 `Paranoia`** (한글 `편집`) — D Hard Trap 작사 프롬프트. 편집증·불신·밤 그림자·거리 코드
  - ✅ **가사 파일 2건 저장** — `SERIES/20-00/input/tracks/` 폴더 생성
    - `불붙은 paycheck (Paycheck on Fire).txt` — Suno 샘플 FAIL 판정 가사(SESSION 2026-04-25 3차) + Bridge 제거 + [Pre-Chorus]→[Pre-Hook] + [Chorus]→[Hook]
    - `씬에 침 뱉어 (Spit on the Scene).txt` — Suno 샘플 PASS + Bridge 제거 + [Pre-Chorus]→[Pre-Hook] + [Chorus]→[Hook] + [Final Chorus]→[Final Hook]
  - ✅ **test-prompts.md 헤더 업데이트** — 곡 1/2 Custom Mode 풀 가사 재활용, 곡 3/4 작사 프롬프트 테스트 명시
  - ✅ **FAIL 대응표 5행 추가** (테크노 쿵짝 / 드럼 빨라짐 / 훅 노래화 / 전자 반복 / Bridge 노래화 / Chorus 태그 / Sweep-EDM FX)
  - **현황**: Suno V5.5 4곡 재테스트 대기 (곡 1/2 Custom Mode 풀 가사 / 곡 3/4 Suno 자체 작사). 3+ PASS 시 20곡 확장 진행

- **20-00 `🌃 AFTER HOURS` 시리즈 기획 착수** (2026-04-25) — Wavvy 첫 힙합 시리즈
  - ✅ **4축 모델 확정** — 1 Rage/Aggressive Trap (KC 레이블 Sik-K·HAON·Vangdale + FDT 크루) / 2 K-Drill NY·UK (Fleeky Bang·Blase·Silkybois·deadbois·NO:EL) / 3 모던 하드코어 붐뱁 (B-Free×Hukky·Owen·Huckleberry P·Paloalto·Kid Milli·QM) / 4 하드코어 트랩 젊은 씬 (ZENE THE ZILLA·Ash Island·Loopy·EK·KWAII)
  - ✅ **핵심 룰** — 힙합 장르는 기존 Wavvy 가사 룰(설명/메타/직접 표출 금지) 예외 적용. "시간 감성 표현"만이 코어 (사용자 2026-04-24 지정). 메모리 저장: `feedback-wavvy-genre-lyrics-rules.md`
  - ✅ **2차 딥리서치 완료** — 10 parallel researcher agents, 신뢰도 88%, 소스 180+. Output: `SERIES/20-00/report/2026-04-24_hard-hiphop-4axis-musical-deep.md` (리포트 ~1,500줄, 4축 × 악기·프로덕션·보컬·믹싱 전수 + 2026 글로벌 트렌드 + Korean 현지화 + Suno V5.5 최적화)
  - ✅ **/team Trade-off Discussion** — Marketing Director + Product Leader + Growth Expert + Design Director + QA Reviewer(Round 2). 5 안건 만장 합의
    - 시리즈명: **`🌃 AFTER HOURS`** / 부제 `밤 여덟시 하드 힙합`
    - 포지셔닝: 하이브리드 (After Hours 감정 프레임 × Dark City 시각 미학)
    - 20곡 배분: **4:5:7:4** (Rage 4 / K-Drill 5 / 모던 하드코어 붐뱁 7 / 하드코어 트랩 4)
    - 썸네일: 블루아워 도시 실루엣 + 네온 악센트 + Wavvy 로고 좌상단 (Option B + 네온)
    - Suno: V5.5 1,000자 Style 필드 활용, LYRICS 200자 QA 규칙 유지
    - 회의 기록: `meetings/2026-04-25_20-00-hard-hiphop-positioning.md`
  - ✅ **리서치 오류 6건 교정**
    - AMADU (I'MMA DO) = **2019-12-03** (2024 X). NOISEMASTERMINSU 프로듀싱, Dingo X DAMOIM Part 2
    - Deepflow `Legacy` 2024 = **미존재**. 2024 핵심 = Garion 3 Executive Producer
    - Loopy The Cohort 소속 = **X**. AOMG 정식 사인 = **X**. 실제 경로: MKIT RAIN(2016-22) → AI0213(2022) → UNWANTED WRLD(2023-). `MARNI`(2024.04) = Rage 컨셉 앨범
    - ZENE THE ZILLA(이상용, 1991 춘천) ≠ 조광일 (SMTM 10 우승자 별개)
    - KC는 레이블/콜렉티브 (Sik-K 설립 2023~, 멤버 Sik-K·HAON·Vangdale·NOWIMYOUNG·JMIN). 솔로 X
    - 한국 Jersey Drill 전담 아티스트 **미정립**. Fleeky Bang은 NY/UK drill
  - ✅ **concept.md v0.1 스캘폴딩 완료** (2026-04-25) — `SERIES/20-00/concept.md` 생성
    - Series DNA v0.1 (기존 12 시리즈 대비 포지션)
    - 핵심 원칙: 힙합 가사 룰 예외 명시 (Chest voice · Articulation · 한국어 95%+는 유지)
    - 4축 Style Templates (A Rage / B K-Drill / C Boom bap / D Hard Trap) — 각 200자 Style Prompt + EXCLUDE 3개 포함
    - Track Map v0.1 4막 × 20곡 스켈레톤 (개별 곡 TBD, 15-00 역추출 방식 계승)
    - YouTube Metadata v0.1 초안
    - LYRICS 축별 작성 가이드
    - Suno V5.5 생성 규칙 + QA 체크리스트
  - ✅ **Suno 1차 테스트 프롬프트 4곡 준비 완료** — `SERIES/20-00/test-prompts.md`
    - 1 `ESCAPE` (Rage, 150 BPM) — 퇴근 직후 점화·해방
    - 2 `BLOCK` (K-Drill, 140 BPM) — 우리 동네·지역 프라이드 (02)
    - 3 `CLOCK OUT` (Boom bap, 90 BPM) — 퇴근 자전 서사·한강·막차
    - 4 `INSOMNIA` (Hard Trap, 142 BPM) — 불면·새벽 직전 내면
    - 각 곡: Style Prompt 200자 + EXCLUDE 3개 + LYRICS 샘플(메타태그 포함 ~190자) + 체크포인트 + FAIL 시 튜닝 가이드
  - ⚠️ **Suno 1차 테스트 결과 (2026-04-25 3차)** — **가사 품질 FAIL**
    - 사용자 공유 Suno 자동 생성 샘플("불붙은 paycheck" 훅) 분석 결과:
      - 영어 비중 50%+ (미국 믹스테입 B급 클리셰: "I don't sleep / got receipts / keep it neat / no second chance / make it stack / check that swag")
      - 훅 의미 없음 ("불붙은 paycheck" = 불+월급봉투 억지 비유)
      - Suno 영어 rap 데이터 드리프트 기본값 (2010s 느낌)
      - 20-00 시간 감성 제로 (퇴근/밤/도시/네온/한강/막차/야근 레퍼런스 전무)
      - "Korean to English, check that swag" 메타 가사 자체가 촌스러움
    - 근본 원인: `singing in Korean` 태그만으로는 **가사 내용 드리프트 방지 불가**. Suno는 영어 rap 학습 비중 절대적
    - **Claude의 ESCAPE 재작성 시도도 실패**:
      - 라임 밀도 0 (어미 반복 "뒤집어/뒤집어" 수준)
      - 서정시·미문체로 빠짐 ("엘리베이터 거울에 내가 두 명")
      - 힙합 구어체·펀치라인·swag 부재
      - 래퍼 1인칭 아닌 3인칭 관찰자 시점
      - "Wavvy 사물·공간 중심" 룰에 집착해 힙합 본연의 구어 어투 훼손
  - 🔄 **다음 세션 경로 3개 제안 (미결정)**
    - **A. 사용자 리드 + Claude 라임/구조 어시스트** — 사용자 1-2 bar 초안 → Claude 라임 보강·플로우 튜닝. 15-00 방식(사용자 직접 제작 14/20) 계승
    - **B. 실존 Korean hard rap 가사 5-10곡 분석 → 라임 패턴·어휘 풀·구어 리듬 추출 문서** — KC BUST IT DOWN / HAON 꼴통 / Fleeky MY NAME IS / Odyssey.1 금도끼은도끼 등 레퍼런스 기반 스타일 템플릿
    - **C. Suno 자동 가사 + cherry-pick 반복** — 재생성 여러 번 후 PASS 가사만 선택, 나머지 사용자 재작성
    - **Claude 추천: B + A 조합** (레퍼런스 분석 → 사용자 리드 + Claude 어시스트)
  - **현황: 사용자 다음 세션에 경로 선택 + Suno 테스트 재개 예정**
  - **종료 기준 (미변경)**: 4곡 중 3개 이상 가사+음악 PASS 시 20곡 확장 진행

- **15-00 PACK + YouTube 업로드 완료** (2026-04-20 00:18)
  - ✅ **썸네일 v1.0 확정** — `🕶️ AFTERNOON DRIVE` (Wavvy 로고 좌상단 + 15:00 / 메인 텍스트 하단 / 채널 카피 1줄). 후보 비교: DRIVE(평범) / WEEKEND DRIVE(v1.3 결정과 충돌) / GOING OUT(밤 뉘앙스+드라이브 SEO 누락) / NOON DRIVE(noon=12시 의미 충돌) → **AFTERNOON DRIVE** (시간대 명시 + 13-00 차별 + SEO)
  - ✅ **loop.png 4K 제작** — 5504x3072 해안 도로 + 빨간 컨버터블, 채도 조정 후 v2 적용
  - ✅ **wavvy.py crop 버그 수정** — 이미지가 16:9보다 넓을 때 (target_h > img_h) width crop 분기 추가. 기존 코드는 height만 crop → 5504x3072 (1.79:1) 케이스에서 5504x3096 (height 늘리기) 시도 → FFmpeg `Invalid too big size` 에러. 13-00 (4096x2336, 1.75:1)은 height crop으로 작동했으나 미처리 분기 발견
  - ✅ **PACK COMPLETE** — `output/final.mkv` 1.27GB, 101.2분, 5460x3072 (16:9 width crop), 16곡 x2, FLAC/48kHz, 로고 overlay (192,136), CRF 18 medium preset
  - ✅ **YouTube Metadata 타임스탬프 재계산** — concept.md TBD 16곡 채움 + 2회차 추가 (acrossfade 0.8s 반영, report.json 기반). 마지막 트랙 1:38:18 + 175.72s = 1:41:14 (final_duration 정확 일치)
  - ✅ **YouTube 업로드 완료**
  - **현황: 시리즈 완료**

- **다른 시리즈 썸네일 텍스트 영문화 검토** (2026-04-20)
  - 06-00 MORNING JOG (기존 WORKOUT → BPM 100-130 가벼운 조깅에 더 정확)
  - 11-00 LO-FI 또는 LO-FI FOCUS (LoFi Girl 그림자 우려, 컨셉 시각화 위해 변형 권장)
  - 14-00 SUNLIT DAZE (햇살에 멍해지는 시간 직역)
  - 18-00 WAY HOME 또는 GOLDEN HOUR (NEO-SOUL 장르명 → 활동/시간 전환)
  - 21-00 CITY POP (장르명 그대로, 트렌드성 강함)
  - 04-00 SLEEPLESS (불면 상태 직격)
  - 12-00 AFROBEATS (장르명, 글로벌 트렌드)
  - **결정 framework**: 장르 specificity + brand power + search traffic 3박자 통과 시 GENRE, 아니면 ACTIVITY/STATE
  - **현황: 텍스트 안 결정, 사용자가 PSD 직접 작업 (커밋된 thumb.jpg/psd 다수)**

- **15-00 오후 3시, 라디오 — 시리즈 리셋** (2026-04-19)
  - 리셋 계기: 확정 13곡 분석 시 Funky 4곡 + Neo-Soul 계열 9곡으로 수렴, 원 기획 4축(Doowop/Funk-R&B/Neo-Soul/Modern R&B) 균형 실제 구현 실패. **Funky Neo-Soul R&B 하이브리드 시리즈**로 자연 재편된 상태. "Retro" 라벨 잔존 + ★ 예외 카테고리 정체성 약화 등 누적 불일치
  - 리셋 범위: `SERIES/15-00/concept.md` 전량 (1000줄+) + `input/tracks/` txt 17개 git rm, 빈 스켈레톤 재생성
  - 보존: `report/2026-04-17_track06-dear-future-husband.md` 리서치 리포트, `.ai/HANDOFF.md` 2026-04-17 엔트리 2건
  - 새 접근: Suno PASS 곡 데이터를 처음부터 누적 → 충분히 쌓이면 시리즈 DNA / 배분 / 4막 구조 역추출 → Track 20까지 설계
  - **현황: concept.md 빈 스켈레톤 상태, Suno PASS 곡 입력 대기**

- **15-00 시리즈 재설계 완료** (2026-04-19 21:23)
  - ✅ **Suno PASS 16곡 정보 전량 입력** — 함께/그레이투그린/오렌지/라디오/달려가는중/체리소다봄길/오늘드라이브/밝은공기냄새/같은재생목록/창문내려/잠깐도망가자/잔디에누워/기울어진햇살/곁에서/봄냄새/믹스테잎
  - ✅ **16곡 완결 결정** (20곡 확장 없음, 타이트한 러닝타임 / BPM 120 중심 Funky 몰입도 우선)
  - ✅ **Series DNA v1.0 역추출** — 라벨 `FUNKY R&B · URBAN NEO-SOUL | 오후 3시 · 드라이브 · 라디오`. 13-00 대비 차별화: BPM 120 중심(더 빠른 그루브) + Funky 비중 높음 + 솔로 일탈+커플 혼재. 시그니처 요소: Warm Rhodes/EP + round bass + laid-back pocket + stacked harmonies + Bridge breakdown. Doo-Wop 2곡(체리소다봄길/믹스테잎) retro 양념 예외
  - ✅ **Track Map v1.0 4막 구조** — 기(1-4): 오렌지/라디오/봄냄새/오늘드라이브 / 승(5-8): 달려가는중/창문내려/잠깐도망가자/그레이투그린 / 전(9-12): 같은재생목록/기울어진햇살/곁에서/체리소다봄길 / 결(13-16): 밝은공기냄새/함께/잔디에누워/믹스테잎. 보컬 F11:M5:Duet0, Minor 2곡(5 달려가는중 Em / 11 곁에서 Am)
  - ✅ **미정 Key 3곡 Db Major 임시 지정** (2 라디오를 켜고, 8 그레이 투 그린, 14 함께) — ⚠️ Db Major 5곡 중복 과다 플래그, 추후 조정
  - ✅ **달려가는 중 Key 정정** — Style prompt "in E major" 기재되어 있으나 Suno 생성 결과 Minor로 사용자 확정 → E Minor (prompt 원문 병기 유지)
  - ✅ **체리, 소다, 봄길 가사 변경** — "두 톤 같은 내 영혼 안 잔치" → "네온 같은 내 영혼 안 파티", "걱정들이 선을 타" → "걱정들이 바람 타" (오타 "같은 같은" 1건 수정)
  - ✅ **주제 규칙 완화** — "드라이브"는 무드 기준, 가사 주제는 드라이브 필수 아님 (이전 v0.2 "길 위 POV 전곡 검증" 규칙 폐기)
  - ✅ **YouTube Metadata v1.0 → v1.1** — /team 회의 결과 반영
  - 🔄 **/team 회의 (Trade-off Discussion)** — 라디오 vs 드라이브 → **드라이브 메인 결정**
    - 참여: Marketing Director + Product Leader + Growth Expert + QA Reviewer (PASS)
    - 근거 3중: 콘텐츠 실체(16곡 중 8+곡 드라이브 씬 직접 언급) + 트래픽 볼륨(드라이브음악 키워드 압도적) + 브랜드 직관성
    - 13-00과 `드라이브` 공유는 Cannibalize 아닌 Bundle 효과
    - 변경: 제목 `오후 3시, 라디오를 켜고` → **`오후 3시 드라이브`**, 태그 `오후 드라이브 · 라디오 · 봄` → `드라이브 · 오후 · 봄`, 해시태그 `드라이브음악/드라이브플레이리스트/오후드라이브/봄드라이브` 최상단, 라디오는 롱테일 유지, 썸네일 후보 2 "창문 내린 드라이브" 우선
    - 회의 기록: `meetings/2026-04-19_15-00-radio-vs-drive.md`
  - **현황: 16곡 확정 + Track Map v1.0 + YouTube Metadata v1.1 확정, WAV 정리 + 패키징 대기**

- **15-00 WAV 리네임 + 제목 v1.3 확정** (2026-04-19 22:00)
  - ✅ **WAV 16곡 리네임** — `NN__제목__영문__장르__BPM.wav` 컨벤션 적용 (22-00 선례). 원 번호 파일 → 신 넘버링 01-16 기반. `6. 체리, 소다, 봄길` → `12__체리, 소다, 봄길__Cherry, Soda, Spring Road__Doo-Wop Neo-Soul__120.wav` (파일명 신 번호 불일치 수정)
  - 🔄 **제목 v1.1 → v1.2 → v1.3 3회 변경**
    - v1.2 (폐기): 주말 키워드 흡수 시도 → 사용자 레퍼런스 문장 "창문열고 달리면 기분좋은 바람이 딱 좋은 요즘"과 복붙 수준 유사해져 폐기
    - v1.3 (확정): **`🕶️ 바람 좋은 날의 드라이브`** — 주말/평일 무관 범용 타겟팅. 주제 태그 `드라이브 · 바람 · 봄`. 사용자 피드백 "주말 단어 빼고 창문/바람/드라이브 키워드로 범용 타겟팅" 반영
  - ✅ **해시태그/태그/고정 댓글 동기화** — `주말드라이브` 제거, `바람좋은날` · `창문열고달리는` 추가
  - **현황: 16곡 WAV 리네임 완료, YouTube Metadata v1.3 확정. 다음 세션 썸네일 작업 예정**

- **22-00 수면 전 릴랙스 시리즈** — Suno 테스트 + 장르/프롬프트 대폭 리뉴얼 (2026-03-31)
  - 시간대: 22:00 (밤 10시) — 수면 전 의도적 이완
  - 장르: **Ambient Slow Jam / Chill R&B** (Bedroom R&B → Chill R&B / Slow Jam 전환)
  - 테마: 다양한 수면 전 릴랙스 (이불, 목욕, 향, 야경, 일기, 명상 등)
  - 차별점: 04:00(불면/Slow R&B) vs 22:00(이완/Bedroom R&B), Belt 금지
  - ✅ concept.md v1.0~v1.1 — 이전 이력 유지
  - ✅ **concept.md v1.2 — 장르 2차 전환** (2026-03-31)
    - Style A: Ambient Chill R&B → **Ambient Slow R&B**
    - Style B: Quiet Storm → **Bedroom R&B**
    - Style C: Acoustic Chill R&B → **Acoustic Bedroom R&B**
    - YouTube 제목/태그 업데이트
  - ✅ **Track 01~09 Suno PASS 버전 반영** (풀 가사 + 싱글라인 스타일)
    - 01 스위치 (Switch) — Korean Slow R&B, F, PASS
    - 02 잠옷 (Comfort) — Ambient Slow R&B, M, PASS (제목 Pajamas→Comfort)
    - 03 조명 (Lights) — Acoustic Chill R&B, F, PASS
    - 04 소파 (Sofa) — Bedroom R&B, F, PASS (Key D Minor→D Major)
    - 05 야경 (Nightscape) — 커스텀 Bedroom R&B (lo-fi), M, PASS (Type A→B)
    - 06 목욕 (Bath) — Bedroom R&B, F, PASS
    - 07 향기 (Scent) — Bedroom R&B, M, PASS (제목 향→향기, Type A→B)
    - 08 체온 (Warm) — BedroomChill R&B, F, PASS
    - 09 풀어져가 (Let it unwind) — Ambient Slow R&B, F, PASS (제목 풀림→풀어져가, Type C→A)
  - ✅ **Track 10 주제 변경** — 찻잔 (Teacup) → 작은 손 (Tiny Hand), 잠든 아기 테마
  - ✅ **보컬 비율 변경** — F12:M7:Inst1 → **M10:F8:Inst1** (Track 14,15,18 F→M 전환)
  - ✅ **코러스 감정 피크 추가** — Track 10~20 전곡 (12 Inst 제외)
    - "chorus builds with emotional swell, tender vocal intensity, aching warmth"
  - ✅ **Track 12 컨셉 변경** — 호흡 (Breath) → 창문 (Window), Inst→M 전환
  - ✅ **Track 13 제목 변경** — 달빛 (Moonlight) → 달빛 커튼 (Moonlit Curtain)
  - ✅ **Inst 트랙 폐지** — 전곡 보컬, M11:F9 (55:45)
  - ✅ **Track 10 풀 가사 반영 + 코러스 훅 변경** — "It's okay" → **"little light"** (2026-03-31)
    - Verse 2 "모든 걸 다 비추는 불"과 이미지 연결
    - "I'm okay"도 "little light"로 통일
  - ✅ **Track 15 주제 변경** — 커튼 (Curtain) → **비 (Rain)**, F 전환 (2026-03-31)
    - 13 달빛 커튼과 주제 중복 해소
    - Type A (Ambient Slow R&B), 65 BPM, D Major 유지
  - ✅ **20/20 전곡 PASS + 풀 가사 입력 완료** (2026-04-02)
  - ✅ **장르 용어 전환** — Bedroom R&B → Chill R&B, Slow R&B → Slow Jam (concept + RUBRIC + WAV 파일명)
  - ✅ **txt → concept.md 통합** — 20곡 Style+Lyrics를 concept.md Track Details로 이동, txt 삭제
  - ✅ **WAV 리네이밍** — `NN__제목__영문__장르__BPM.wav` 컨벤션 적용 (20곡)
  - ✅ **Track Map 정리** — Track 01 Off, 10 작은 빛, 15 비, 18 맞잡은 손, 20 눈을 감으면
  - ✅ **YouTube 메타 작성** — 트랙리스트 + 서정적 설명문 + 해시태그 + 썸네일/루프 컨셉 기록
  - ✅ **썸네일 확정** — 다크 로프트 침실 + 네온 빌딩 야경 + 파자마 DJ
  - ✅ **루프영상 v2 제작** — 0.5x 감속 + 프레임보간 + 팔린드롬 (31.7s, 4K, 50fps)
  - ✅ **PACK COMPLETE** — final.mkv 8.7GB, 137분, 20곡x2, CRF 26 (2026-04-03)
  - ✅ **YouTube 제목 확정** — "느좋 릴랙스 플리" 컨셉, 타임스탬프 20곡 반영
  - ✅ **YouTube 태그 리스트 추가** (# 없는 버전)
  - ✅ **YouTube 업로드 완료** (2026-04-04)
  - ✅ **YouTube 제목 변경** — 태그 세분화 (수면·릴랙스·카페 → 릴랙스·카페음악·매장음악·수면음악)
  - **현황: PACK + YouTube 업로드 완료**

- **12-00 Korean Afrobeats 시리즈** — PACK v2 COMPLETE (2026-03-22)
  - **현황: 20/20 트랙 PASS, PACK v2 4K/FLAC 완성, Shorts 1건 완성**
  - ✅ YouTube 업로드 완료

- **brand/logo_wavvy.psd** — 로컬 삭제 상태 (의도 확인 필요)

- **12-00 Korean Afrobeats 시리즈** — Suno 자체 작사 방식 전환 완료 (2026-03-14)
  - ✅ 워크플로우 리팩토링: 풀 가사 작성 → 작사 프롬프트 / 비움
  - ✅ LYRICS.md v4.0 (§1 Lyric Prompt Guide 신규)
  - ✅ WORKFLOWS.md v2.0 (6단계 → 3단계)
  - ✅ RUBRIC 가사→보컬 체크리스트 전환 (L1-19 → V1-5)
  - ✅ Track 01-04 제목 변경 + 가사 제거
    - 01 한낮 (Haze), 02 먼지 (Dust), 03 볕 (Sunlit), 04 무음 (Mute)
  - ✅ REFERENCE_SAMPLE.md, FAILURE_CASES.md 삭제
  - ✅ 잔존물 정리: lessons-learned dead 섹션 삭제 + SESSION stale 메모 제거
  - ✅ Track 03 "볕 (Sunlit)" 작사 프롬프트 작성 (198자, 풀 구조+DNA)
  - ✅ LYRICS.md §1.2 소괄호 금지 규칙 반영
  - ✅ LYRICS.md v4.1 — §1.4 약칭 구조 포맷 추가 (I-V-PC-C 등, Suno 인식 확인)
  - ✅ Track 03 Suno 테스트: 가사 생성됨, "아침" 톤 이슈 발견 → noon 키워드 보강 필요
  - ✅ Track 04 "무음 (Mute)" 작사 프롬프트 + 스타일 단일 라인화 (2026-03-16)
  - ✅ Track 05 "갈증 (Thirst)" 신규 디자인 (E, 104, Ab Major) — 스타일 톤 조정 (dark→heavy groove)
  - ✅ Track 06 "낮 그림자 (Noon Shadow)" 신규 디자인 (E, 107, Bb Minor) → Male로 변경
  - ✅ Track 07 "낮꿈 (Daydream)" 신규 디자인 (E, 102, Db Major, Female)
  - ✅ Track 04 Suno 테스트 PASS — 가사 자체 생성 품질 우수 (만트라+서사 대비 구조)
  - ✅ Track 05-07 Suno 테스트 PASS (2026-03-16)
  - ✅ Track 08 "차가워진 (Cold At Noon)" 신규 디자인 (D, 112, E Minor, Male, djembe bass) + Suno PASS
  - ✅ Track 09 "맥박 (Pulse)" 신규 디자인 (E, 106, F# Major, Female) + Suno PASS (2026-03-17)
  - ✅ Track 10 "잔상 (Afterimage)" 신규 디자인 (E, 108, A Minor, Male) + Suno PASS (2026-03-17)
  - ✅ Track 11 "그늘 (Shade)" 신규 디자인 (E, 100, B Major, Instrumental) + Suno PASS (2026-03-17)
  - ✅ Track 12 "기다림 (Waiting)" 신규 디자인 (D, 105, D Minor, Female) + Suno PASS (2026-03-17)
  - Track 01-02는 Empty 모드 확정 (가사 없이 PASS)
  - 보컬 비율 변경: Female 70/Male 30 → **Female 60/Male 40** (F9:M6)
  - ✅ Track 13 "정오의 균열 (Midday Crack)" 신규 디자인 (E, 110, Eb Minor, Male) + Suno PASS (2026-03-18)
  - ✅ STYLE.md §0.6 Articulation First 규칙 추가 + 전곡 반영 (2026-03-18)
  - ✅ Track 14 "설렘 (Flutter)" 디자인 (E, 104, G Major, Female) (2026-03-18)
  - ✅ **20곡 확장 결정** — Team Meeting (Product/Design/Strategy) 전원 합의 (2026-03-18)
  - ✅ Track 15-20 디자인 완료 + 프롬프트 파일 생성 (2026-03-18)
    - 15 온기 (Warmth) — E, 107, A Major, F
    - 16 미열 (Low Fever) — D, 103, F# Minor, F
    - 17 진동 (Vibration) — E, 109, C Minor, M
    - 18 얼룩 (Stain) — E, 102, Db Major, F (Track 07 동일 스타일)
    - 19 폭발 (Burst) — E, 111, B Minor, M
    - 20 고요 (Stillness) — D, 100, F Major, F
  - ✅ concept.md v5.0 — 20트랙 확장 + 배분 규칙 업데이트
  - Track 01-02는 Empty 모드 확정 (가사 없이 PASS)
  - 보컬 비율: **F12:M7:Inst1** (60:37:5)
  - 4막 구조: 기(01-05) → 승(06-10) → 전(11-15) → 결(16-20)
  - ✅ Track 14 "설렘 (Flutter)" Suno PASS (2026-03-18)
  - ✅ Track 15 "온기 (Warmth)" 사용자 직접 가사 작성 + Suno PASS (2026-03-18)
    - Chorus 중심 영한 혼합 가사, Verse/Pre-Chorus/Outro instrumental
  - ✅ Track 18 "얼룩 (Stain)" → Track 07 동일 스타일로 변경 (D→E, Afropiano→Afro-Drill, 102 BPM, Db Major) (2026-03-19)
  - ✅ Track 18 Suno PASS (2026-03-19)
  - ✅ Track 19 "폭발 (Burst)" LYRICS QA 트리밍 208→196자 (2026-03-19)
  - ✅ Track 16-19 Suno PASS (2026-03-20) — Track 19 제목 터짐→폭발 변경
  - ✅ Track 20 "고요 (Stillness)" Instrumental 전환 + PASS (2026-03-20)
  - **현황: 20/20 트랙 PASS (Track 11, 20 Instrumental)**
  - ✅ 썸네일 확정 — 밀림 젬베 + god rays (Team Meeting 3회, Image 3 선택) (2026-03-20)
  - ✅ WAV 파일 리네이밍 — `XX__제목__감정__장르__BPM.wav` 컨벤션 적용 (20곡) (2026-03-20)
  - ✅ TXT 제목 동기화 — Track 06/08/13 원본 제목 반영 (2026-03-20)
  - ✅ 루프 영상 제작 — 팔린드롬 (0.5배속 + 정방향/역방향), god rays 빛 움직임 (2026-03-21)
  - ✅ vfade PASS — 로고 오버레이 (96,68), 크로스페이드 0.5s (2026-03-21)
  - ✅ **PACK COMPLETE** — final.mp4 102.7분, 20곡 x2, -14 LUFS (2026-03-21)
  - ✅ concept.md v5.1 — YouTube 메타데이터 완성 ("리듬 맛집" 컨셉) (2026-03-21)
  - ✅ 워크플로우 보완 2건 — WAV 네이밍 컨벤션 + YouTube 설명 참조 규칙 (2026-03-20/21)
  - ✅ **음질 최적화 리서치** — YouTube DASH 오디오 파이프라인 조사, 4K 업스케일 무효 확인 (2026-03-21)
  - ✅ **wavvy.py 오디오 설정 개선** — AAC 320k/44.1kHz → FLAC lossless/48kHz, generation loss 1회로 제한 (2026-03-21)
  - ✅ **4K 리마스터** — original.mp4(네이티브 4K) → 팔린드롬 loop → vfade → pack (2026-03-21)
  - ✅ **PACK v2 COMPLETE** — final.mkv 4K/FLAC/48kHz, 102.7분, 16GB (2026-03-21)
  - ✅ **Shorts 제작** — Track 18 "얼룩 (Stain)" 전곡, 팔린드롬 루프 + 로고(288px, 60, 160) (2026-03-22)
    - 영상: Downloads/loop.mov (1190x2116, 30.7s) → 팔린드롬 → 루프
    - 로고: 288px, left 60px, top 160px
    - Output: output/shorts/short_얼룩.mp4 (~123MB, 2:49)
- **13-00 벚꽃 산책 시리즈** — Korean Indie Pop + Dream Pop 신규 시리즈 (2026-04-04)
  - 시간대: 13:00 — 점심 후 벚꽃길 산책
  - 장르: **Korean Indie Pop (메인) + Dream Pop (질감)**
  - 테마: 봄의 감정들 — 첫사랑, 설렘, 벚꽃, 햇살, 두근거림
  - 레퍼런스: 마틴스미스 "봄 그리고 너" (핵심), 케이윌 "러브블라썸" (무드)
  - ✅ 레퍼런스 리서치 완료 (`report/2026-04-04_13-00-reference-research.md`)
  - ✅ 장르 딥리서치 완료 (`report/2026-04-04_indie-pop-dream-pop-genre-research.md`)
  - ✅ `INDIE_POP_RUBRIC.md` v1.0 작성 (Hard Gate 7개, 8-Factor, Drift 6종)
  - ✅ Genre Gate 추가 (concept.md)
  - ✅ concept.md v0.1 — Series DNA, Style Template 3종 (A/B/C), Track Map 20곡
  - ✅ Track Map 검증 — Minor 4곡 배치 (F#m, Bm, Em, Dm), Key 중복 해소
  - 보컬: F11:M9 (55:45), Bright/Sweet/Clear 톤
  - Style: A 10 : C 6 : B 4 (50:30:20)
  - ✅ **20곡 트랙 txt 파일 생성** — Style/Exclude/Lyrics 포맷 완비
  - ✅ **Lyrics 약칭 포맷 적용** — `I-V1-PC-C-V2-PC-C-B-C-O` + 키워드 + English hook
  - ✅ **Track 01 Suno 테스트 PASS** — Style A, "Here comes the wind" 훅 (v0.1, 이후 v0.2에서 폐기)
  - ✅ **Track 02 Male Duet 전환** — call-and-response duet
  - 🔄 **v0.2 장르 재정의 (2026-04-11)** — Korean Indie Pop + Dream Pop → **Korean Light Pop + K-Pop Sweet Ballad**
    - 계기: Track 01 청취 후 레퍼런스(마틴스미스·러브블라썸)와 톤 어긋남 판단. 리서치 재분석 시 두 곡 모두 "폴리시드 팝" 성향 확인 (마틴스미스 Melon "댄스·인디음악"/Light Pop 병기, 러브블라썸 Urban Soul/폴리시드 K-Pop)
    - ✅ `concept.md` v0.1 → v0.2 — DNA/차별점/레퍼런스 해석/Style A/B/C 템플릿/Vocal Persona/Track Map 전면 재작성
    - ✅ **Style A: Korean Light Pop** (폴리시드 클린 기타 리프 + Rhodes chord bed + 스트링 패드 + 폴리시드 미디엄 그루브)
    - ✅ **Style B: K-Pop Sweet Ballad** (스윗 피아노 리드 + 리치 스트링 편곡 + 펑키 웜 베이스, 러브블라썸 타입)
    - ✅ **Style C: Polished Pop Blend** (A+B 혼합 완충 구간)
    - ✅ Style 재배분: A9:B5:C6 선언/실제 불일치 → **A13:B4:C3 (65/20/15)**
    - ✅ BPM 범위 확장: 90-118 → **86-118** (Track 14 벚꽃 96→88, Track 05 꽃비 96→90)
    - ✅ Vocal Persona: Airy 제거 (STYLE.md §1.1 Default 재정렬) → **Bright/Sweet/Polished/Warm**
    - ✅ **`MASTER/rubrics/K_LIGHTPOP_RUBRIC.md` v1.0 신규 작성** (250줄)
      - Hard Gate 7개 (H1 BPM 86-118, H3 폴리시드 클린 기타 또는 스윗 피아노 리드)
      - Style-Specific Gates (A1 Polished Clean Guitar, B1 Sweet Piano Lead, B2 String Arrangement)
      - 8-Factor 재설계 (F4 멜로디 악기 확장, F7 스트링/피아노 레이어)
      - Drift 재편: Shoegaze 제거, **Indie DIY Drift** 강화, **Over-Polished Idol K-Pop Drift** 신규, K-Pop Drift 완화
    - ✅ `MASTER/rubrics/INDIE_POP_RUBRIC.md` 삭제 (git rm, 13-00 전용이었음)
    - ✅ `MASTER/reference/GENRES.md` Pop 섹션 확장: `Light Pop`, `Sweet Ballad` 2행 추가
    - ✅ **20곡 txt STYLE/EXCLUDE 일괄 교체** — 900자 한도 이하 (749-808자) + LYRICS `dreamy` 잔재 4건 정리
    - ✅ Track 01 "첫 바람" 추가 튜닝 (Suno 1차 결과 "촌스러움" 피드백 반영):
      - **Rhodes electric piano** (piano → Rhodes, 촌스러움 해소)
      - **Chorus 감정 고조 명시** (STYLE.md §3 Musicality Matrix 반영: emotional swell + sweet intensity lift to peak + 1 held note + Verse2 lift + Bridge build)
      - **Soulful R&B Vocal** (Bright/Sweet/Soulful R&B/Smooth/Chest voice/melodic runs)
    - 보컬 방향성 전환: Light Pop 베이스 + **R&B inflection vocal** (현대 Korean R&B Pop 크로스오버, 폴킴/적재/아이유 계열)
    - ✅ **Track 01 Suno 재테스트 PASS** (2026-04-11) — Rhodes + Chorus build + Soulful R&B vocal 조합 검증
    - ✅ **v0.2.1 전체 롤아웃** (2026-04-11) — 19개 트랙 txt 일괄 반영 완료:
      - Style A풀세트 12곡 (02 Duet 포함): piano → **Rhodes**, vocal에 **Soulful R&B + Smooth + melodic runs**, Chorus build 2줄 구조
      - Style B 4곡 (05/09/14/20): 그랜드 피아노 유지, vocal에 **Soulful R&B + melodic runs**, Chorus build 2줄 (tender sustained)
      - Style C 3곡 (04/10/18): piano chord layer → **Rhodes**, vocal에 **Soulful R&B + Smooth + melodic runs**, Chorus build 2줄
      - Track 02 Duet: `Male Duet vocal: Bright, Sweet, R&B, Clear, Chest voice, melodic runs, articulation,` (Duet 구조 유지 + R&B 살짝)
      - 전체 20곡 STYLE 섹션 846~893자 (900자 제한 통과)
    - ✅ concept.md Style Template 3개 동기화 (v0.2.1)
    - 🔄 **v0.3 장르 라벨 재정의 (2026-04-11)** — `Korean Light Pop` → **`Korean Bright Pop R&B`**
      - 계기: v0.2.1 테스트에서 R&B 느낌 안 나옴. Suno는 장르 라벨에 가장 민감.
      - **리서치 오분류 정정**: 마틴스미스 "봄 그리고 너" = Korean Pop R&B (적재 세션 기타 증거), 케이윌 "러브블라썸" = Urban Soul = Pop R&B. Melon "댄스·인디음악" 태그를 "Light Pop"으로 곧이곧대로 받아들인 v0.2 분류 오류.
      - 사용자 테스트 확인: `Korean Bright Pop R&B Like Spring Sprout` 라벨로 Track 02 재테스트 → R&B 느낌 확인
      - ✅ **전 20곡 장르 라벨 통합** → `Korean Bright Pop R&B, Like Spring {Title}` (Style A/B/C 통합, 악기/BPM/분위기로만 차별화)
      - ✅ Track 15 "Spring Rain" / Track 20 "Our Spring" 은 "Spring" 중복 방지
      - ✅ **"Verse2 last lines rise" 제거** — 2절 지르는 지시 삭제 (사용자 요청)
      - ✅ Rhodes / Soulful R&B vocal / Chorus build 유지
      - ✅ concept.md Style A/B/C 템플릿 3개 + Track Map 헤더 동기화
      - 전체 20곡 STYLE 838~898자 (900자 제한 통과, Track 01 898 최대)
    - 🔄 **v0.4 Silky R&B 전환 (2026-04-11)** — Suno auto-gen 샘플 분석 기반 전면 재작성
      - 계기: v0.3 테스트에서 "R&B 느낌 전혀 안 남" 피드백 → 사용자가 `봄 새싹 R&B, Korean Pop. 남성/여성` 입력으로 Suno 자동생성 → 훨씬 좋은 결과
      - **Auto-gen Sample 1 (Male)**: `Silky midtempo Korean R&B with male vocals, warm Rhodes and soft electric piano chords over a relaxed bounce, Tight close-mic lead, subtle vocal doubles on key words, Chorus blooms with airy harmonies, light funk guitar chops, round sub-bass lift, gentle rimshots and brushed snare, intimate, hook circles like a mantra, r&b, korean pop`
      - **Auto-gen Sample 2 (Female)**: `Silky Korean R&B / K-pop blend with female vocals; soft electric piano and warm Rhodes, gentle groove over round bass and crisp rim shots, Verses intimate close-mic'd with subtle guitar fills, pre-chorus lifts with airy pads and rising harmonies, Chorus opens brighter with stacked vocals and light synth bells, Final hook over mellow breakdown, spotlight on lead vocal, korean pop, r&b`
      - **성별 차이 발견**: Male = `subtle vocal doubles` (미니멀), Female = **`stacked vocals + airy harmonies`** (풍부) → v0.2/v0.3 `No stacked harmonies` 룰 **과잉 제약** 판명
      - ✅ **Style A/B/C 폐지 → Male/Female 2종 템플릿** (~490자, v0.3 대비 절반)
      - ✅ **전 19곡 Write 롤아웃** (Track 02 제외 — 사용자 직접 완성)
        - Male 8곡 (04, 07, 09, 11, 13, 15, 17, 19): Male 템플릿
        - Female 11곡 (01, 03, 05, 06, 08, 10, 12, 14, 16, 18, 20): Female 템플릿
      - ✅ EXCLUDE에서 `choir, stacked harmonies, backing vocal layers, doubled vocals` 라인 삭제 (R&B 하모니 허용)
      - ✅ "Spring {Theme}" 가변 (Track 15 "Spring Rain", 20 "Our Spring" 중복 방지)
      - ✅ Articulation. 필수 유지 (wavvy 규칙)
      - ✅ `Bridge builds with emotional swell, 1 held note. Higher register encouraged.` 유지
      - ✅ concept.md v0.4 반영 (Style Templates / Series DNA / 차별점 / 레퍼런스 분류 정정 / Track Map Template 컬럼 / Vocal Persona 재편 / Genre Gate 루브릭 재검토 메모)
      - 전체 19곡 STYLE 482~494자 (~절반 압축), Track 02만 889자 (사용자 처리)
      - **리서치 분류 정정 기록**: 마틴스미스 "봄 그리고 너" = Korean Pop R&B (적재 세션 기타 증거), 케이윌 "러브블라썸" = Urban Soul = Pop R&B. v0.2 "Light Pop + Sweet Ballad" 오분류는 Melon "댄스·인디음악" 태그 곧이곧대로 받아들인 것이 원인.
    - 플랜 파일: `~/.claude/plans/hashed-sniffing-comet.md`
  - **현황: v0.4 롤아웃 완료. Track 02는 사용자 완성본 대기. 전 트랙 Suno 테스트 대기**
  - 🔄 **트랙 삽입 + 리넘버링 (2026-04-12)** — 사용자 직접 제작 Track 11-12 삽입, 기존 11-19 → 13-21
    - ✅ **Track 11 "봄 향기 (Spring Scent)"** — Neo-Soul/Funk, F, 사용자 직접 제작 PASS
    - ✅ **Track 12 "약속 (Promise)"** — Neo-Soul, M, 100 BPM, 사용자 직접 제작 PASS
    - ✅ 기존 11-19 → 13-21 파일 리넘버링 완료
    - ✅ concept.md Track Map 21트랙 업데이트 + 4막 구조 재배분
    - ✅ **Track 07 "두근" 스타일 교체** — v0.4 Silky R&B → Urban Soul groove (사용자 커스텀)
    - ✅ **Track 08 "미소" 스타일 교체** — v0.4 Silky R&B → Urban Neo-Soul R&B (사용자 커스텀, jazz chords + vinyl texture)
    - ⚠️ **동명 트랙**: Track 12 / Track 18 모두 "약속 (Promise)" — 사용자 추후 변경 예정
    - 13~21 추가 변경 예고됨 (사용자 알림 대기)
  - 🔄 **v0.5 전면 업데이트 (2026-04-12)** — 사용자 직접 제작 트랙 대폭 추가 + 전곡 PASS
    - ✅ **Track 07 "두근" → "봄 꽃 (Spring Blossom)" 교체** — Urban Soul, M, 사용자 직접 제작
    - ✅ **Track 03 "햇살" 스타일+BPM 교체** — 112→102 BPM, Neo-Soul/Funk
    - ✅ **Track 13~19 전곡 커스텀 스타일+풀 가사 교체** (사용자 직접 제작)
    - ✅ **Track 20 "만개" DROP** → `_excluded/`, Track 21 "우리의 봄" → 20번 M+F Duet
    - ✅ **제목 변경 5건**: 16 봄비같은너, 17 봄빛, 18 봄의약속, 19 봄노을, 07 봄꽃
    - ✅ **Track 20 "우리의 봄" 스타일 Funky Neo-Soul Duet** + 가사 2차 교체
    - ✅ **concept.md v0.5** — Track Details 20곡 Style+Lyrics 통합, txt 파일 삭제
    - ✅ **Track "두근" DROP** → `_excluded/`
    - 20트랙 체제: Custom 14 / Legacy 1 / Male 2 / Female 3 / F10:M8:Duet2
  - ✅ **WAV 리네이밍** (2026-04-13) — 20곡 `NN__제목__영문__장르__BPM.wav` 컨벤션 적용, Track 07/11 BPM 100 기재
  - ✅ **_excluded/ 삭제** (2026-04-13) — 07 두근, 20 만개 txt 정리
  - ✅ **YouTube 메타 작성** (2026-04-13) — concept.md 최상단, "봄이라 괜히 기분 좋은 하루 🌸 | FEEL GOOD R&B · URBAN NEO-SOUL | 봄플리 · 산책 · 드라이브" 컨셉
  - ✅ **이미지 기반 영상 제작** (2026-04-13) — loop.png(4096x2336, 벚꽃길 커플 사진) 직접 렌더, `-loop 1 -tune stillimage -r 1` 최적화
  - ✅ **PACK COMPLETE** — final.mkv 1.3GB, 135.4분, 20곡 x2, FLAC/48kHz (2026-04-13)
  - ✅ **YouTube 업로드 완료** (2026-04-13)
  - 🔄 **v0.5.1 재패키지 + YouTube 재업로드 (2026-04-13)** — Track 01 교체 + 트랙 스왑
    - ✅ **Track 01 "첫 바람" → "봄이 번져 (Spring Bleeds)" 교체** — Urban Neo-Soul, 110 BPM, E Major, F, 사용자 직접 제작 (Warm EP + round bass + airy stacked vocals chorus)
    - ✅ **트랙 3-way 사이클 재배열**: (기존 02 새싹, 03 햇살, 11 봄 향기, 12 약속, 13 피크닉) → 로컬 순서 (02 봄 향기, 03 약속, 11 피크닉, 12 햇살, 13 새싹)
    - ✅ **concept.md Track Map 재배열** — 배분 규칙: Custom 15 / Male 2 (04,13) / Female 3 (05,06,09), Key 순환 01 E Major ↔ 20 G Major
    - ✅ **YouTube Tracklist 실제 타임스탬프 재계산** — report.json 기반, 1회차 누적 + acrossfade 0.8s 반영
    - ✅ **wavvy.py image mode 버그 수정** — `ProjectPaths.__init__` dead code (self.logo 등 `is_image_mode` property 뒤로 잘못 위치 → AttributeError) + 로고 스케일 `iw/2:ih/2` → `iw:ih` (50%→100%, 4K 기준 572x312 원본 표시)
    - ✅ **PACK v0.5.1 COMPLETE** — final.mkv 1.4GB, 135.6분, 4096x2304 static image mode + 로고 100% (2026-04-13)
    - ✅ **YouTube 재업로드 완료** (2026-04-13)
    - ✅ **loop.png 교체** (사용자 제공 신규 이미지, 4096x2336)
  - **현황: 시리즈 완료 (v0.5.1)**

- **MASTER 문서 v3.2 완료** — Writing Formula + 워크플로우 분리 (2026-03-08)

## 현재 세션 (2026-04-25)

### 완료된 작업

| 작업 | 비고 |
|------|------|
| **20-00 K-Drill 통과 샘플 vs 게이트 정합성 점검** | `씬에 침 뱉어` (Rewrite 4차 PASS)가 음악 게이트(BPM/Style Prompt/EXCLUDE/구조) 충족, 가사 게이트(한국어 95%+ vs 실측 75%, Ad-libs `(Grr!)/(Bow!)` 부재, 크루 chant 부재) 미달 발견. 옵션 A(K-Drill 본가 NY/Brooklyn drill 영어 어휘 침투 인정 → §QA / §Style B / §LYRICS 가이드 동기화) 권장 결론. |
| **Loopy `Gear 2` 장르 검증** | 트랩 (붐뱁 아님). 근거: 힙합엘이/나무위키 "aggressive trap beats 강점", Loopy 본인 "초기 trap 시기 대표곡", 프로듀서 Denis The Menace + 808/hi-hat roll 컨벤션. 20-00 D축 분류 정합 (단 Loopy 후기곡과 구분 필요, 시기 명시 권장). |
| **2026 글로벌 트렌드 외부 리서치 (Plugg 1순위)** | researcher 5에이전트 병렬. PluggnB Splice +342.8% (2024 가장 빠른 성장), Sexy Drill 차트, Drift Phonk Spotify 1위. 1순위 4축 안: A Rage / B K-Drill+Sexy Drill / C PluggnB / D Hardcore Trap + 붐뱁 보너스. |
| **2026 국힙 신규 리서치 (사용자 정정 반영)** | researcher. KHA 2026 Sik-K Artist of the Year + KMA 2026 Effie 6관왕 + 붐뱁 H2 2025 모멘텀 약화 검증. **글로벌 추천 무효화**: PluggnB·Sexy Drill·Phonk 모두 K-rap 진입 사례 부족. Hyperpop·Digicore가 진짜 2026 국힙 부상 트렌드. |
| **/team 4축 재편안 검증 회의** | Marketing/Product/Growth/Design + QA Round 2 인라인. **5/5 PASS**. A안 보정 (35/20/25/10+5) 만장 합의: Rage 4→7 격상(KC + EK 흡수 후보), K-Drill 5→4 축소, Hardcore Trap 4→5(YUMDDA 추가), Hyperpop·Digicore Edge 2곡(Sion+Effie raged 한정), 모던 붐뱁 7→1-2 보너스. 회의: `meetings/2026-04-25_20-00-4axis-realignment.md` |
| **음악 디테일 조사 충분성 검증 회의** | Music Production Engineer / Music Data Analyst / A&R Genre Specialist + QA Round 2. Critical 갭 3건(YUMDDA / Sion eigensinn / Effie raged) + Major 갭 2건(EK YAHO 분류 / 멜랑콜릭 Rage 한국 사례) 식별. 회의: `meetings/2026-04-25_20-00-music-detail-audit.md` |
| **차트·청자 검증 신규 리서치 (사용자 의심 정정)** | researcher. 사용자 "진짜 Korean 2026 trend에 적합한가?" 의심 정확. **시상식 직반영 4축 안 FAIL**: 벅스 2025 힙합/R&B TOP30에서 Rage/Drill/Hyperpop 진입 0-1곡, 멜로딕 트랩/Trap-Soul 8-10곡 / KT지니 30대 1위 G-DRAGON `TOO BAD` / Effie 본인 "보수적 청자는 내 음악 싫어한다" 인용. 사용자 첫 직감(트렌디 트랩 비트 기반) 재확인. 리포트: `SERIES/20-00/report/2026-04-25_chart-vs-awards-validation.md` |
| **20-00 시리즈 산출물 전면 리셋** | 사용자 결정: 기존 4축 안 폐기. 삭제: `concept.md` v0.1(437줄) / `test-prompts.md`(414줄) / `input/tracks/` 가사 2건(Paycheck Rage / Rewrite K-Drill). 보존: 1162줄 deep dive 리포트 + 미팅 노트 4건 + 차트 검증 리포트 (audit trail). 새 방향은 사용자와 별도 논의 예정. |
| **2026 K-Hiphop 트랩 영역 정밀 트렌드 리서치** | researcher. 벅스 2025 TOP30 분포 재검증(멜로딕/Trap-Soul 8-10 / 협업 트랩 3-4 / Rage·Drill·Hyperpop 0-1). 핵심 발견: Lil Moshpit=Lee Hwi-min=GroovyRoom 절반 (Sik-K K-FLIP Rage 프로듀서가 멜로딕 트랩 메인) → 멜로딕 ↔ Rage 양립 시그널. dress 프로듀서 BIG Naughty `Hero Death` + Mark `Fraktsiya` 동시 (멜로딕 ↔ K-drill 양립). Trap-Soul 한국 토착 = DEAN/Crush/Colde/pH-1/BIBI. 리포트: `SERIES/20-00/report/2026-04-25_k-hiphop-trap-trends-deep.md` |
| **20-00 새 시리즈 정체성 합의 — Workout 컨셉 + 빡센 트랩 위주** | 사용자 결정: After Hours 퇴근/내면 → **AFTER HOURS WORKOUT** (저녁 8시 운동·그라인드). 페르소나: 25-35 직장인 헬스/PT/홈트/러닝. **빡센 트랩 위주 + Rage Trap dry voice + tuned singing 양립**. 새 4축: A Rage Dry Voice 5-6 / B Rage Tuned Singing 4-5 / C Hardcore Trap 5-6 / D K-Drill Workout 액센트 3-4 + **보너스 빡센 붐뱁 1-2** = 총 19-22곡. |
| **GPT 빡센 붐뱁 딥리서치 자료 보존** | 사용자 제공 `Downloads/deep-research-report.md` (311줄, Suno 붐뱁 프롬프트 엔지니어링). 1162줄 §5 모던과 보완적 — 90s-2000s 정통 + 한국 토착 레퍼런스 3건(가리온 `무투/금기어` / 데드피 `Check My Swag` 공식 inst / 제이호 `LOCALS ONLY` 위스퍼 톤) + Suno 추천 프롬프트 6개 + Exclude 디테일. 보존: `SERIES/20-00/report/2026-04-25_suno-boom-bap-prompt-engineering-gpt.md` (출처 표기 추가). |

| **/team 회의 — concept.md v0.2 작성 전 리서치 갭 점검** | Music Production Engineer / Music Data Analyst / A&R Genre Specialist (Workout 도메인 흡수) + QA Round 2 인라인. **5/5 PASS**. 만장 합의: P0 갭 2건(Korean Tuned Singing Rage Trap 음악 디테일 + Workout K-rap 페르소나·운동 BGM 사례) 신규 리서치 필요 → P1/P2 갭(YUMDDA / EK YAHO / dry/tuned Suno 키워드 분리표 / Workout BPM 표준)은 concept 작성 + Suno 테스트로 흡수. 핵심 위험: Workout K-rap 페르소나 검증 안 하면 시리즈 가설 자체 흔들림 (차트 30대 = 멜로딕 트랩 우세 vs Workout = 빡센 트랩 가설 정합 미검증). 회의: `meetings/2026-04-25_20-00-pre-concept-research-gaps.md` |

### 다음 단계
- **20-00 시리즈 라벨 확정** — `💪 AFTER HOURS WORKOUT` 초안 OK (사용자 확인)
- **통과 가사 복원** — pending (보류, 사용자 결정)
- **P0 리서치 2건 병렬 호출** — (1) Korean Tuned Singing Rage Trap 정밀 분석 (Sik-K K-FLIP+ / Lil Moshpit / Loopy MARNI / HAON SMTM12 후속 / 글로벌 dry vs tuned 비교 / Suno 키워드 분리) + (2) Workout K-rap 페르소나 + 한국 운동 BGM 사례 (헬스/PT/홈트 BGM, Spotify Korea Workout, Workout 1세션 길이, BPM 분포)
- **결과 → 종합 보충 리포트 작성** — `report/2026-04-25_workout-tuned-rage-supplement.md`
- **concept.md v0.2 재작성** — 신 4축 + 보너스 붐뱁 Style Templates + Track Map (Workout 배치 룰: 워밍업/메인 푸시/하이 인텐시티/그라인드 지속/쿨다운+마지막 폭발) + EXCLUDE

## 다음 할 일

- [x] ~~13-00 Style A Suno 테스트~~ — Track 01 PASS v0.2 (2026-04-04)
- [x] ~~13-00 Track 01 Rhodes+R&B 재테스트~~ — PASS v0.2.1 (2026-04-11)
- [x] ~~13-00 v0.2.1 전체 롤아웃~~ — 19곡 txt 일괄 반영 (2026-04-11)
- [x] ~~13-00 v0.3 장르 라벨 통합~~ — Korean Bright Pop R&B, Verse2 제거 (2026-04-11)
- [x] ~~13-00 v0.4 Silky R&B 전환~~ — Male/Female 2종 템플릿, 19곡 Write (2026-04-11)
- [x] ~~13-00 Track 02 "새싹" PASS v0.4~~ — Male 템플릿 + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 01 "첫 바람" PASS (legacy)~~ — Korean Light R&B 구버전 유지, 사용자 완성 가사 저장 (2026-04-11)
  - ⚠️ **예외 1건**: Track 01은 v0.4 Silky R&B 템플릿 적용 제외. 사용자가 이전 Korean Light R&B 스타일 유지 요청 (EXCLUDE에 stacked harmonies 포함)
- [x] ~~13-00 Track 03 "햇살" PASS v0.4~~ — Female 템플릿 + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 04 "꽃길" PASS v0.4~~ — Male 템플릿 + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 05 "꽃비" PASS v0.4~~ — Female 템플릿 (F#m 90 BPM, 첫 Minor 앵커) + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 06 "눈맞춤" PASS v0.4~~ — Female 템플릿 + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 07 "두근" PASS v0.4~~ — Male 템플릿 + 데이트 대기 POV (boom boom mantra, waiting on you 훅) + 사용자 완성본 저장 (2026-04-11)
  - B안 적용: 대화체 포기 → mantra hook + 감정 상승곡. 구조 단순화 (V-PC-C-V-PC-C-B-C). 1차 A안은 Suno에서 반복 실패했음
- [x] ~~13-00 Track 08 "고백" DROPPED~~ — 시리즈 의도와 안 맞음, `_excluded/` 이동. 시리즈 20곡 → **19곡** 전환 (2026-04-11)
- [x] ~~13-00 파일 리넘버링~~ — 기존 09-20 → 08-19 (고백 제외 후 연속 번호화, 2026-04-11)
  - 새 Track Map: 01 첫바람 / 02 새싹 / 03 햇살 / 04 꽃길 / 05 꽃비 / 06 눈맞춤 / 07 두근 / **08 미소** / **09 손끝** / **10 그네** / **11 피크닉** / **12 무지개** / **13 벚꽃** / **14 봄비** / **15 눈부심** / **16 약속** / **17 노을** / **18 만개** / **19 우리의 봄**
  - Key 순환: Track 01 = Track 19 = G Major
  - Minor 배치: 05(F#m) / 09(Bm) / 10(Em) / 14(Dm)
- [x] ~~13-00 Track 08 "미소" PASS v0.4~~ — Male 템플릿 + 사용자 완성 가사 저장 (2026-04-11)
- [x] ~~13-00 Track 09 "손끝" PASS v0.4~~ — Female 템플릿 + 사용자 완성 가사 저장 (2026-04-11). **Key 변경: B Minor → B Major** (Suno 테스트 결과 Major가 자연스러움). Minor 배치 3곡으로 축소.
- [x] ~~13-00 Track 10 "그네" PASS v0.4~~ — **Male/Female Duet 커스텀 스타일** (trading lines + thirds/fifths 화음) + 사용자 완성 가사 저장 (2026-04-11)
  - 가사는 1인칭 회상 POV지만 Suno Duet 보이싱으로 Verse가 남녀 교대로 분할됨. 듀엣 주제 우려는 결과가 해소.
- [x] ~~13-00 Track 11-12 삽입 + 리넘버링~~ — 사용자 직접 제작 2곡 삽입, 기존 11-19→13-21 (2026-04-12)
- [x] ~~13-00 Track 07/08 스타일 교체~~ — 사용자 커스텀 Urban Soul/Neo-Soul (2026-04-12)
- [x] ~~13-00 v0.5 전면 업데이트~~ — 07 봄꽃 교체, 03/13-19 커스텀 스타일+가사, 20 만개 DROP, concept.md Track Details 통합, txt 삭제 (2026-04-12)
- [x] ~~13-00 WAV 리네이밍~~ — 20곡 `NN__제목__영문__장르__BPM.wav` 컨벤션 (2026-04-13)
- [x] ~~13-00 YouTube 메타 작성~~ — concept.md 최상단, FEEL GOOD R&B · URBAN NEO-SOUL (2026-04-13)
- [x] ~~13-00 영상 제작 + PACK~~ — 이미지 베이스 (loop.png 4K), final.mkv 1.3GB 135.4분 (2026-04-13)
- [x] ~~13-00 YouTube 업로드~~ — 완료 (2026-04-13)
- [x] ~~wavvy.py 이미지 모드 지원~~ — loop.png/jpg 감지 시 vfade 스킵, `-loop 1 -tune stillimage -r 1` 직접 렌더 (2026-04-13)
- [x] ~~K_LIGHTPOP_RUBRIC.md 폐기~~ — v0.5 Custom 중심 시리즈라 루브릭 불필요, 파일 삭제 (2026-04-13)

- [x] ~~15-00 Suno PASS 곡 정보 누적 입력~~ — 16곡 완료 (2026-04-19)
- [x] ~~15-00 시리즈 DNA / 배분 / 4막 구조 역추출~~ — v1.0 완료, 라벨 `FUNKY R&B · URBAN NEO-SOUL | 오후 3시 · 드라이브 · 라디오` (2026-04-19)
- [ ] 15-00 미정 Key 3곡 확정 (2 라디오를 켜고 / 8 그레이 투 그린 / 14 함께)
- [x] ~~15-00 YouTube Metadata 작성~~ — v1.3 확정 `🕶️ 바람 좋은 날의 드라이브` (2026-04-19)
- [x] ~~15-00 WAV 파일 리네임~~ — 16곡 `NN__제목__영문__장르__BPM.wav` 컨벤션 (2026-04-19)
- [x] ~~15-00 썸네일 작업~~ — `🕶️ AFTERNOON DRIVE` v1.0 확정, loop.png 4K 제작 (2026-04-20)
- [x] ~~15-00 pack~~ — final.mkv 1.27GB / 101.2분 / 5460x3072 / 16곡 x2 (2026-04-20)
- [x] ~~15-00 YouTube Metadata 타임스탬프 재계산~~ — concept.md TBD 16곡 채움 + 2회차 추가 (2026-04-20)
- [x] ~~15-00 YouTube 업로드~~ — 완료 (2026-04-20)
- [x] ~~wavvy.py crop 버그 수정~~ — 이미지 16:9보다 넓은 케이스 width crop 분기 추가 (2026-04-20)

- [ ] 다른 시리즈 썸네일 텍스트 영문화 적용 (검토 완료, PSD 작업 진행 중)
  - 04-00: SLEEPLESS / 06-00: MORNING JOG / 11-00: LO-FI(또는 LO-FI FOCUS) / 12-00: AFROBEATS
  - 14-00: SUNLIT DAZE / 18-00: WAY HOME(또는 GOLDEN HOUR) / 21-00: CITY POP

## 핸드오프 메모

- 채널 브랜딩: `wavvy.md` §7 참조
- 12-00: YouTube 업로드 완료
- 22-00: YouTube 업로드 완료
- 13-00: 20트랙 전곡 PASS, concept.md v0.5 Track Details 통합 완료, WAV 리네이밍+패키징 대기
  - 루브릭: `MASTER/rubrics/INDIE_POP_RUBRIC.md`
  - 리서치: `report/2026-04-04_*.md` (2건)
- 리서치 리포트: `report/2026-03-21_youtube-audio-quality-optimization.md`

### 2026-04-29

- [x] 20-00 힙합 시리즈 트랙 프롬프트 정리
  - Black Mirror / Bottom Line / Old Cassette / Engine / Concrete / Real Talk 사용자 제공 최종 본문 반영
  - `-` negative tag 항목은 `EXCLUDE`로 분리하는 규칙 재확인 및 Bottom Line 수정
  - `17_Late Lane.txt`~`20_Old Page.txt` 제외, `03_`~`16_` 트랙 txt 파일명 넘버링 제거
  - Concrete는 instrumental-only intro 및 hook dance 전환 방어 버전으로 정리
- [x] 20-00 트랙 파일명 넘버링 제거 후 gate 검증 복구
  - 번호 제거된 03-11 트랙 헤더에 `Order:` 메타 추가
  - `check_series_gate.sh SERIES/20-00/` PASS 7/7 복구
  - `check_lyric_avoid.sh SERIES/20-00/input/tracks` PASS 20/20 확인

### 2026-05-02

- [x] Wavvy harness engineering 분석/계획/구현
  - `/team` 관점 분석 산출: `meetings/2026-05-02_wavvy-harness-engineering-analysis.md`
  - Claude analysis review 1차 NEEDS_USER_DECISION 보완 후 PASS: `.ai/peer-review/runs/20260502-003021-claude-review-49474.md`
  - 구현 계획 산출/Claude plan PASS: `.ai/plans/PLAN_wavvy_harness_setting.md`, `.ai/peer-review/runs/20260502-003357-claude-plan-57722.md`
  - `/director` 구현: `wavvy.py doctor/state/gate`, `wavvy_harness/`, `.ai/state.json`, `MASTER/SSOT.md`, 20-00 `uploaded` 정리, `tests/test_harness.py`
  - 구현 Claude review PASS: `.ai/peer-review/runs/20260502-004637-claude-review-91756.md`
  - 검증 PASS: `py_compile`, `unittest`, `doctor --json`, `validate`, `state --check --json`, `gate --stage upload-ready --json`, `gate --stage uploaded --json`, `git diff --check`
  - 상태 보정: 20-00은 업로드 완료. `final.mkv`/`upload.csv` 부재는 업로드 후 용량 정리를 위한 `deleted_after_upload`로 처리

- [x] Agent instruction minimalism refactor
  - Pre-research check: AI Ops Expert skill/reference에 원칙이 이미 포함되어 있어 외부 research 생략
  - Team review PASS: `meetings/2026-05-02_wavvy-agent-instruction-minimalism-team.md`, `.ai/peer-review/runs/20260502-011803-claude-review-65918.md`
  - Plan review PASS: `.ai/plans/PLAN_wavvy_agent_instruction_minimalism.md`, `.ai/peer-review/runs/20260502-012050-claude-plan-72307.md`
  - 구현: `AGENTS.md` canonical router, `CLAUDE.md` 29줄 Claude overlay, `MASTER/ai/RUNTIME_RULES.md`, `MASTER/SSOT.md` priority 4 integration
  - 구현 review: 1차 records gap FAIL 후 보완, 최종 PASS `.ai/peer-review/runs/20260502-012932-claude-review-93881.md`
  - 보존: `사용자 확인 필수`는 삭제하지 않고 `MASTER/ai/RUNTIME_RULES.md` Safety/Approval owner로 이동
  - 검증 PASS: line-count/drift checks, `py_compile`, `unittest`, `doctor --json`, `validate`, `state --check --json`, `gate --stage uploaded --json`, `gate --stage upload-ready --json`, `git diff --check`

### 2026-05-22 00:52:48 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`13%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260522-005248_codex-context-low`
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-22 11:13:34 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`24%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260522-111333_codex-context-low`
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-22 14:18:42 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`23%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260522-141842_codex-context-low`
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-22 14:22:01 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`21%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260522-142200_codex-context-low`
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 18:48:05 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`14%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-184805_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-184805_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 19:56:14 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`18%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195613_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195613_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 19:57:13 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`17%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195713_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195713_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 19:58:06 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`12%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195806_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-195806_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 21:08:13 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`22%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210813_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210813_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 21:09:04 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`17%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210904_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210904_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 21:09:50 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`12%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210950_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-210950_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-23 21:10:36 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`7%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-211035_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260523-211035_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 13:35:13 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`22%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-133512_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-133512_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 13:37:26 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`20%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-133726_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-133726_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 13:42:38 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`18%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-134238_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-134238_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 15:28:51 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`16%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-152851_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-152851_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 17:09:31 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`18%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-170931_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-170931_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-24 17:15:16 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`16%` remaining)
- Project: `/Users/zenkim_office/Project/wavvy`
- Resume trigger: `Codex: -wavvy; Claude: /wavvy`
- Snapshot: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-171516_codex-context-low`
- Pending user requests: `/Users/zenkim_office/Project/wavvy/.ai/auto-handoff/20260524-171516_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zenkim_office/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `pending-user-requests.md` before older TODOs. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-05-27 17:28:20 +0900 Agent Center Path Reference Cleanup

- Updated stale `claude-center` references to `agent-center` in the Wavvy harness engineering meeting notes.
- Kept the change scoped to documentation path references only.

### 2026-06-02 19:52:16 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`18%` remaining)
- Project: `/Users/zen/Project/wavvy`
- Resume trigger: `cd /Users/zen/Project/wavvy && cat /Users/zen/Project/wavvy/.ai/HANDOFF.md`
- Primary repo: `/Users/zen/Project/wavvy` (`implementation`)
- Secondary repos: `none`
- Do not resume from: `/Users/zen/Project`
- Snapshot: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-195216_codex-context-low`
- Pending user requests: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-195216_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zen/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `continuation-target.json` before older TODOs. Treat `pending-user-requests.md` as context-only prior requests unless the target file is missing. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-06-03 15:22:17 +0900 Policy Audit + Safe Mutation

- Trigger: `-director`
- Project: `/Users/zen/Project/wavvy`
- Audit mode: read-only audit first, then user-approved safe mutation.
- Scope checked: 236 document candidates (`.md`, `.txt`, `.json`, `.yml/.yaml`, `.toml`) under repo root, excluding `.git`, dependency/cache/build/vendor paths, binaries, and large media artifacts.
- Precedence used: repository-defined `MASTER/SSOT.md` Conflict Order. `SERIES/20-00/concept.md` has higher authority than `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` and legacy shell validators for per-series final distribution.
- Main finding: `SERIES/20-00/concept.md` current final state says A 3 / B 5 / C 5 / D 3 / E 2 / F 2 = 20 tracks and Hard 65%, while older v0.4 notes, `HARD_HIPHOP_RUBRIC.md` v1.4, and `check_series_gate.sh` still implied A 3 / B 4 / C 5 / D 3 / E 2 / F 3 and Hard 70%.
- Mutations:
  - Added `.ai/plans/2026-06-03_policy-audit-mutation.md`.
  - Marked the stale v0.4 distribution lines in `SERIES/20-00/concept.md` as superseded by v0.5/v0.8.
  - Updated `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` to v1.5 with current 20-00 final distribution and state/gate priority.
  - Marked `MASTER/scripts/check_series_gate.sh` as a legacy pre-final txt source validator and aligned S1/S2/S3/S5 with current final concept.
  - Added this session record and `CHANGELOG.md` entry.
- Deletion/archive: none. `meetings/`, `report/`, and selected `.ai/pipeline/runs` artifacts remain referenced by current rubric or lyric pattern docs, so they were not deleted.
- Pending verification: bash syntax, `py_compile`, unit tests, `doctor`, `state/gate`, `git diff --check`, and `git status`.

### 2026-06-02 19:57:30 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`18%` remaining)
- Project: `/Users/zen/Project/wavvy`
- Resume trigger: `cd /Users/zen/Project/wavvy && cat /Users/zen/Project/wavvy/.ai/HANDOFF.md`
- Primary repo: `/Users/zen/Project/wavvy` (`implementation`)
- Secondary repos: `none`
- Do not resume from: `/Users/zen/Project`
- Snapshot: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-195730_codex-context-low`
- Pending user requests: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-195730_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zen/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `continuation-target.json` before older TODOs. Treat `pending-user-requests.md` as context-only prior requests unless the target file is missing. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-06-02 21:36:58 +0900 Auto Context Handoff

- Trigger: Codex context below `25%` (`16%` remaining)
- Project: `/Users/zen/Project/wavvy`
- Resume trigger: `cd /Users/zen/Project/wavvy && cat /Users/zen/Project/wavvy/.ai/HANDOFF.md`
- Primary repo: `/Users/zen/Project/wavvy` (`implementation`)
- Secondary repos: `/Users/zen/Project/agent-center (audit_record_only)`
- Do not resume from: `/Users/zen/Project, /Users/zen/Project/agent-center (secondary: audit_record_only)`
- Snapshot: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-213658_codex-context-low`
- Pending user requests: `/Users/zen/Project/wavvy/.ai/auto-handoff/20260602-213658_codex-context-low/pending-user-requests.md` (`available`, 5 request(s))
- Continuation sentinel: `/Users/zen/.codex/auto-handoff/clear-required.json`
- Record mode: `commit_push`
- Continuation: headless continuation starts by default after checkpoint and must read `continuation-target.json` before older TODOs. Treat `pending-user-requests.md` as context-only prior requests unless the target file is missing. Manual resume is fallback only if `continue_action` is not `started`.

### 2026-06-03 15:34:00 +0900 Policy Audit Post-Review Safety Correction

- Trigger: user/reviewer feedback on possible gate weakening in `MASTER/scripts/check_series_gate.sh`.
- Evidence check: reconstructed the current 20-00 final fixture from `SERIES/20-00/concept.md`; the original HEAD script failed S1/S2/S3/S5.
- Correction:
  - `check_series_gate.sh` emits S2 as ADVISORY and does not count it as a hard gate.
  - S2 decision SSOT: `MASTER/rubrics/HARD_HIPHOP_RUBRIC.md` section `S2 Advisory Disposition`.
  - S1/S3/S5 precedence evidence is documented in the final user report for this turn.
- Verification: bash syntax, `py_compile`, unit tests, doctor, state, uploaded gate, legacy fixture check, and `git diff --check` passed. Uploaded gate warnings remain non-blocking: local `final.mkv`/`upload.csv` deleted after upload and `rubric_unverified_after_finalize`.

### 2026-06-03 16:05:30 +0900 Record

- Trigger: `-record`
- Project: `/Users/zen/Project/wavvy`
- Mode: session record; no extra CHANGELOG entry was needed because the policy audit and S2 safety correction were already recorded in `CHANGELOG.md`.
- Scope committed: 20-00 final concept sync, `HARD_HIPHOP_RUBRIC.md` v1.5, legacy `check_series_gate.sh` S2 advisory handling, local audit plan, SESSION/HANDOFF records.
- Remote check: `origin/master` ahead/behind was `0/0` before commit.
- Verification before record: bash syntax, `py_compile`, unit tests, doctor, state, uploaded gate, legacy fixture check, and `git diff --check` passed.

### 2026-09-30 20:30:47 +0900 Wavvy Lyric Naturalness Skill and Gate

- Trigger: 젠이 기존 작사 스킬과 하네스 전체에 선호 가사 분석을 반영하라고 요청. 현재 20-00 업로드 상태는 변경하지 않았고, 새 가을 R&B 시리즈는 이번 범위에 포함하지 않았다.
- Cause and precedent: 지정한 13곡의 선례 중 저장된 Wavvy 본문과 젠이 채팅에서 제공한 「낮꿈」 가사를 구분해 `skills/wavvy-lyricist/references/patterns.md`에 기록했다. 이 근거는 직접 감정·설명·비유·평범한 말, 대화와 감각 연상, 정지와 반복을 허용한다. `SERIES/18-00/concept.md` Track 06 「전화」의 생략된 상대 대답처럼 발화 목적과 연결이 중요하다. 좋아하는 곡도 모든 행이 승인된 것은 아니다. 젠은 「낮꿈」의 “내 이름 불러도 / 살짝 뒤로 미뤄 둬”를 문장 자체가 억지스럽다고 기각했다. 「작은 손/작은빛」은 사용자 제공 기악 Outro를 우선한다.
- Changed: `wavvy.md` §5, `MASTER/lyrics/LYRICS.md`, 작사 SKILL/spec/patterns, `/write` 라우터, CLI spec, `wavvy_harness/gate.py`, `wavvy.py`, 테스트와 `.ai/plans/2026-09-30_lyric-naturalness-skill-gate.md`. 평가 순서는 문장 표현→앞뒤 연결→감정 흐름. 특정 단어/사물 3개/시간 단어/무조건 후크 검사를 제거했다. 시리즈의 장르·언어·주제 조건은 유지하되 어색한 문장을 그 조건으로 합리화하지 않는다.
- Review evidence contract: full draft는 `Self-Gate`의 Draft 본문, review-only는 `Findings`의 실제 읽을 수 있는 가사 본문을 SHA-256과 정확 인용으로 묶는다. `review-only`는 자체 Verdict를 판정하고, Suno prompt-only는 Empty/Prompt/Structure를 유지하며 풀가사 3축을 강요하지 않는다. `gate --stage lyrics-review`는 artifact 필수다. package-only PASS는 설치 확인(`quality_status: NOT_REVIEWED`)이다. 자동 코드는 검토 기록의 형식·대상 일치·상태만 확인하고 의미·가창·AI 작성 여부를 인증하지 않는다. 사용자에게 전하는 완성 가사와 내부 검토 기록은 분리한다.
- Raw validation: `python3 -m unittest tests/test_harness.py` 20/20 PASS (`/tmp/wavvy-lyric-unittest.log`); `python3 -m py_compile wavvy.py wavvy_harness/*.py` PASS (`/tmp/wavvy-lyric-pycompile.log`); `python3 /Users/zenkim_office/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/wavvy-lyricist` PASS (`/tmp/wavvy-lyric-quickvalidate.log`); `git diff --check` PASS (`/tmp/wavvy-lyric-diffcheck.log`); `python3 wavvy.py lyrics-skill SERIES/18-00 --json` returned `PASS / PACKAGE_ONLY / NOT_REVIEWED` (`/tmp/wavvy-lyric-package-smoke.json`). Controller independently reran 20 tests (`/tmp/wavvy-lyric-controller-tests.log`).
- Review and behavior evidence reported by controller: isolated Astra xhigh review CLEAN (Critical/High 0; principle observations 0), reviewer reran 20 tests and checked CLI artifact PASS / no-artifact exit 1. Skill samples A (direct feeling and explanation) and C (poetic sensory association without an added plot or resolution: “네가 없는 집에서는 / 작은 소리도 오래 남아”) were handled appropriately. Sample B (“졸음이 내 시간을 걸어 / 오후를 잠깐 비켜 둬”) was judged an expression failure with connection on hold. This is a reading judgment, not an automated quality guarantee.
- Remote before record: `git fetch origin master` succeeded; `HEAD...origin/master` ahead/behind `0/0` (`/tmp/wavvy-lyric-record-fetch.log`). No pre-existing staged files or external changes were found. Series/media, `.ai/state.json`, AGENTS/CLAUDE, HIPHOP content checks, and other repositories were not changed. Final record commit/push belongs to this turn.
- 2026-09-30 -record 최종 세션 기록: Wavvy 작사 자연스러움 스킬·하네스 개선(24a0fed)은 테스트 20개 PASS와 독립 Astra CLEAN 후 원격 반영을 마쳤다. 이 명령은 로컬·전역 SESSION/HANDOFF 기록을 동기화하며, 새 가을 R&B 시리즈는 이번 작업 범위에 포함되지 않았다.

### 2026-09-30 21:17:28 +0900 17:00 Acoustic Series and State Transition

- 젠 확정: 17:00의 가을빛 편안함과 밝은 여지, Acoustic R&B/Neo-Soul/Indie Rock, 중간 템포에서 125 BPM까지 허용. 총 20곡 목표는 어쿠스틱 버전 리믹스 3곡(01 「서랍」, 02 「공강」, 04 원곡·제목 미제공)과 젠과 새로 만들 17곡(03, 05–20)으로 구성한다. 03의 별도 작업은 이번 기록/커밋에 포함하지 않고, 04의 STYLE/LYRICS도 아직 없다.
- 01 「서랍 (Acoustic Remix)」와 02 「공강 (Accoustic Remix)」의 사용자 제공 STYLE/LYRICS를 txt로 저장했다. 02의 `Accoustic` 표기는 그대로 두고, 01 STYLE의 잘린 `highly en`은 젠 확인대로 `high-energy`로 보완했다. EXCLUDE는 제공되지 않아 비웠다. 이전 17-00 Pop R&B concept와 「올라가」 샘플은 바이트 동일성을 확인해 archive에 보관했고 현재 후보에서 제외했다.
- 기존 state writer는 active_series가 바뀌어도 20-00의 `uploaded` phase/next_action을 넘겼다. `wavvy_harness/state.py`는 같은 시리즈의 수동 값을 보존하고 다른 시리즈는 실제 concept/artifact에서 다시 추론하도록 수정했다. `check_state`도 다른 시리즈 phase를 끌고 오지 않는다. 명시 `--phase`와 `--if-match`는 유지한다.
- 실제 `state --write --if-match 3`은 `SERIES/17-00`, revision 4, `track_source_draft`, txt 2개, final sources 없음으로 기록했다. `state --check --json`은 PASS/warnings[]/blockers[]. 검증: unittest 23개 PASS(`/tmp/wavvy-1700-state-unittest.log`), py_compile PASS(`/tmp/wavvy-1700-state-pycompile.log`), diffcheck PASS(`/tmp/wavvy-1700-state-diffcheck.log`), writer/check 원시 JSON(`/tmp/wavvy-1700-state-write.json`, `/tmp/wavvy-1700-state-check.json`). Root가 전달한 격리 Astra xhigh 검토는 CLEAN(Critical/High 0, 원칙 관찰 없음). 음원·실측 BPM·음악 품질은 검증하거나 확정하지 않았다.
