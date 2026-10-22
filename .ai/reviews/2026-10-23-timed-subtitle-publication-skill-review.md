# 17:30 수동 자막 게시·스킬 기록 — 격리 검토 회수 기록

Date: 2026-10-23
Reviewer: `/root/subtitle_skill_record_review`, Codex `gpt-6-astra` / `xhigh` (fresh context)
Controller relay: `/root`가 수신한 판정을 실행 워커가 기록함. 이 파일은 reviewer가 직접 작성한 원문 보고서가 아님.
Reviewed scope: 젠의 기존 영상 자막 게시 후 스킬 수정 요청, 게시 원시 자료, `skills/wavvy-youtube-publish/`의 지정 변경, 17:30의 현행 문서·공식 state·로컬 검사 결과. 가사 시간 맞춤 자체의 재검토는 범위 밖이다.

## 부모가 수신한 판정

**CLEAN — 확인된 Critical/High 0건, 원칙 관찰 없음.** 이전 자막 파일 판정을 이번 검토의 근거로 사용하지 않았다.

- [게시 원시 관찰](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/publication-observation.json)과 [Studio 수동 게시 화면](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-manual-caption-published-studio.png), [공개 자막 메뉴](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/2026-10-23-public-manual-caption-menu.png), 네 시점의 TXT·PNG는 수동 한국어 `게시됨`, 자동 한국어 별도 보존, 공개 수동 한국어 선택 및 정확한 문구 표시를 뒷받침한다.
- [정식 로컬 SRT](../../SERIES/17-30/output/youtube_subtitles_ko_timed_estimated.srt)의 SHA-256은 `29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226`이고, 원고 SHA-256은 `29cd296a8c31bcf6629e2f468862698970931ca7ad50e36fd2f8f547c953ba18`로 불변이다. [Studio 다운로드 SRT](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/studio-published-manual-ko.srt)는 정식 SRT에 마지막 LF 한 바이트만 더한 내용이다.
- 스킬은 **기존 영상 자막 후속**으로만 경로를 넓혔고 원문·제목·공개·댓글을 보존했다. 곡 수, 사용 모델, 고정 cue 길이를 보편 규칙으로 만들지 않았다. 현행 게시 성공과 과거 오류 3회를 구분했다. 공식 state revision 78 `uploaded`·자막 SRT `present`, [로컬 검사 원시](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/publication/local-validation/)와 기록이 일치한다. 큰 영상은 로컬 ignored 상태다.

부모 컨트롤러도 같은 Studio·공개 화면, Studio 다운로드 전체 바이트, 정식 SRT SHA-256, state check revision 78과 uploaded gate를 직접 대조했고 강등 없이 CLEAN을 수용했다.
