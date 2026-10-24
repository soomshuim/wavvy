# 06:30 retained premix release contract

## 2026-10-24 마감 — 업로드 후 승인된 미디어 정리

- 현재 요청: 젠의 “이제, 마무리.”. 공개·댓글·좋아요는 기존 직접 관측 원문을 보존한다.
- 선례: `MASTER/SSOT.md`는 기록된 업로드 완료와 보존 결정 아래 선언된 영상·완성 믹스 삭제를 허용한다. 기존 `.ai/cleanup/execute-2026-10-24.py`의 경로·파일 동일성·기록 함수를 재사용하며 이전 대량 목록은 다시 실행하지 않는다.
- 삭제 범위: 새 동결 목록의 정확한 6개 영상·믹스·임시 전송 사본뿐이다. 6·11번 WAV와 사용자 최종 JPG, 문서·선택·믹스·렌더·검사 기록은 보존한다. 두 WAV를 제외한 전체 20곡의 정확한 재확보는 보장하지 않는다.
- 절차: 현재 파일과 보호 자료의 내용 동일성 검사 → 격리 검토 → 지정 6파일 삭제 → 전부 부재·보호 자료 불변 대조 → 전용 상태 저장 → 업로드 완료 전용 검사 → 문서 기록·단일 커밋·푸시.
- 삭제 전 원시: `.ai/cleanup/2026-10-24-0630-post-upload-cleanup-manifest.json` 및 동명 `-dry-run.json`. 논리 합계 2,654,380,359바이트이며 공유 블록 때문에 실제 회수 공간과 같다고 해석하지 않는다.
- 마감 결과: 독립 Astra/high 검토 CLEAN 뒤 6개 전부 삭제했다. 사후 대조에서 전부 부재·보호 및 기록 13개 불변·현재 오디오/영상은 두 WAV뿐임을 확인했다. 전용 상태 저장 1회로 revision 90·uploaded에 갱신했다. 실행·사후 원시는 동명 `-apply.json`과 `-postcheck.json`을 따른다. 문서 기록·최종 검사·단일 커밋·푸시로 마감한다.

- 최종 검사: `state --check`·`gate --stage uploaded`·`git diff --check`·AGENTS/CLAUDE 동일성은 모두 종료값 0이다. 추가 실행한 업로드 전 실물 대조 명령 `verify-release`는 삭제된 믹스 때문에 종료값 1이다. 업로드 후 정리를 허용하는 인자를 쓰지 않는 별도 명령임을 코드·명세로 확인했으며 실패 원시를 보존했다. 이를 완료 판정으로 쓰거나 코드·정책을 바꾸지 않았다. 파일 보유 당시 전체 대조 통과 근거는 기존 기록에 있다. 원시: `.ai/validation/2026-10-24-0630-closeout-gates.json`.

## 현재 06:30 — 즉시 공개·설명 한 줄 삭제·댓글·좋아요 완료

- 젠의 “지금 공개하고 댓글달아.”에 따라 Wavvy24 영상 [FUBJ6OBTzoI](https://youtu.be/FUBJ6OBTzoI)를 즉시 공개했다. 저장 뒤 Studio(유튜브 영상 관리 화면)를 새로 열고 공개 선택을 다시 열어 확인했다. 이전 공개 시점 질문은 해소됐다.
- 승인 제목과 사용자 썸네일을 유지했다. “17BPM이 목표고 실제 곡마다 빠르기는 다르다는 설명은 빼” 요청에 맞춰 실제 설명의 `175 BPM은 이 플레이리스트의 목표 속도예요. 실제 곡마다 빠르기는 달라요.` 한 줄을 삭제하고 서버 저장·로컬 CSV(업로드 문안을 저장하는 표 파일) 일치를 확인했다. 내부 제작·실측 이력은 바꾸지 않았다.
- SD·HD·4K 처리 완료와 현재 소유권 주장·저작권 보호 콘텐츠 미발견 화면을 확인했다. 미래 권리 주장 부재를 보장하지 않는다.
- [일반 댓글](https://www.youtube.com/watch?v=FUBJ6OBTzoI&lc=UgxQyi1zjfh2fk5osSV4AaABAg) 1개를 @wavvy24로 게시했고 정확한 세 줄을 화면과 Aside(연결된 브라우저 도구)의 댓글 조회로 확인했다. 영상 좋아요 적용과 “좋아요 취소”·1 표시도 확인했다. 댓글은 고정하지 않았다.
- 직접 관측: `SERIES/06-30/production/youtube-public-followup-20261024.json` 및 같은 이름의 화면 기록. 공개·댓글 관측 당시에는 미디어 삭제가 없었다. 이후 실제 정리는 위 마감 결과를 따른다.

## 최초 비공개 업로드 이력 — 당시 상태

- 사용자 제작 JPG와 전체 제목을 승인받은 최종 v2 4K 영상의 전체 해독·원본 AAC(압축 오디오 형식) 복사 일치 검사를 마쳤다. 원래 20곡×2회 믹스에 추가 반복은 없다.
- 미업로드 문구를 완료로 오판한 첫 High(중대 결함) 1건을 근본 수정했다. 컨트롤러 직접 테스트100개·upload-ready·verify-release 통과와 미업로드 상태 uploaded 검사의 예상 실패를 확인했다. 새 격리 실제 gpt-6-astra/high 검토는 CLEAN(확인된 Critical/High 중대 결함0건·원칙 관찰 없음)으로 채택됐다. [새 검토 수용 기록](../inbox-reviews/2026-10-24/premixed-release-final-review.md)을 따른다.
- Wavvy24에 정확한 최종 영상을 1회 전송해 비공개 저장했다. 영상 `FUBJ6OBTzoI`의 [시청 주소](https://youtu.be/FUBJ6OBTzoI)와 [편집 화면](https://studio.youtube.com/video/FUBJ6OBTzoI/edit)을 실제로 다시 열어 메타데이터(제목·설명·태그)·썸네일·설정을 확인했다. 원문은 `SERIES/06-30/production/youtube-upload-20261024.json`이다.
- 1080p 서버 재생은 약18.8초와 1:03:05.7에서 오류 없이 관측했고 반복 첫 챕터도 인식했다. 음소거 재생 동작 검사이며 음질 청취·끝부분 재생은 확인하지 않았다. 플레이어는 일시정지·음소거 상태다. 최종 Studio 재열기에서는 SD 완료·HD/4K 처리 중·저작권 검토 진행 중·비공개를 확인했다. 남은 일은 상위 화질 처리·저작권 검토의 결과 확인과 젠의 공개 시점·방식 결정이다. 저작권 무문제로 확정하지 않는다. 실제 댓글 게시0회다. 원본 믹스·최종 영상·임시 전송 사본은 상위 처리·저작권 검사가 남아 있는 동안 보존한다.
- 공식 상태는 컨트롤러가 전용 명령으로 최종 revision 88·uploaded(비공개 업로드 완료)에 저장했다. 기본 저장이 이전 단계를 보존한 revision 87 뒤에 `--phase uploaded --if-match 87`로 명시 단계를 적용했다. 상태 검사·uploaded 검사·verify-release는 모두 종료값 0이다. 원문은 [직접 원시 기록](../validation/2026-10-24-0630-uploaded.json)을 따른다. 공개·처리·저작권 검사 완료와 구분한다.

## 설계·수정 이력

- Requirement: publish the approved JPG as a static 4K video with the retained, already two-cycle mix. Obtain title approval before upload. Do not recover deleted individual WAVs, repeat the mix again, or invent Final Track Sources.
- Precedent: `SERIES/07-00/concept.md` explicitly opts into the instrumental selected-audio archive. That archive requires every current WAV and cannot represent this intentionally retained premix. No existing premixed release contract was found in `MASTER/`, `skills/`, or the harness.
- Cause: `load_finalize_report` / `check_selected_audio` require current individual WAVs; timestamps assume one constant crossfade; state and gates assume `final.mkv`. The retained production manifest instead records historical source verification and 40 actual entry samples.
- Scope: a separate `production/final-premixed-audio.json` opt-in and `Final Premixed Audio` concept section; a dedicated validator; narrow dispatch in validation/release/gates/state; regression tests and owning SSOT/CLI/workflow documentation. Preserve existing WAV validation unchanged. Reject `pack` on this opt-in to prevent merging two retained WAVs or repeating the premix again.
- Source checks: current mix/JPG hashes, producer manifest/config/script hashes, 20 selected source IDs/titles/historical WAV hashes, before/after source checks, 40 increasing entry samples in exactly two cycles, instrumental declaration with retained `[Instrumental]` evidence. Historical prompt status remains unverified.
- Render checks: final render record and video hashes, selected CSV path, H.264/AAC 3840×2160, complete audio packet payload/timing identity, exact audio duration and bounded final-video-frame rounding, approved JPG binding, 40 embedded chapters, matching concept/CSV text and actual chapter starts. Source checks do not require video artifacts.
- State: record the premix/report/upload path separately from surviving individual WAVs. Only the existing writer may change `.ai/state.json`; the controller will invoke it once after final validation. Uploaded cleanup still requires explicit upload-completion evidence.
- Validation: existing unit regressions, focused valid/invalid source identity/order/timing/hash/opt-in cases, render/CSV/chapter/audio mutation cases, stage separation, uploaded cleanup, and rejection of `pack`; compile and diff checks. Run real read-only release/gates after title and render records are final. No media regeneration, commit, or push in this task.
- Upload-status correction: the prior global substring fallback misread the current negative sentence “실제 공개·업로드 완료 기록은 아니다.” as completed and enabled uploaded cleanup. Parse explicit positive upload fields only inside one dedicated Upload Status section, retaining the actual 07/17/17-30/20 field forms and 04-00's dedicated published-URL marker. At correction time, preserve the negative 06-30 sentence for regression coverage and add explicit not-uploaded status. After the separately observed successful private upload, the current concept now records completed(private) with the real video URL and observation evidence. 13-00 has only a TODO completion claim and no observed publication URL/evidence; do not manufacture a new completed field or keep a global prose exception. Regression checks cover negative/incidental completion text, explicit pending overriding legacy URLs, actual legacy positive formats, and missing premix/video being rejected before upload. Controller owns final review and the official state writes, whose exact commands and revisions are recorded separately.
