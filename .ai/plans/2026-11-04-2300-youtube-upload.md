# 23:00 YouTube 업로드·즉시 공개·고정 댓글 — 실행 지시서

배정: 규모=큼 · 복잡도=큼 · 중요도=큼

작성: 2026-11-04 Claude 오케스트레이터. 실행: sonnet-xhigh-worker. 저장소: `~/Project/wavvy` (아래 상대경로 기준).

## 젠 지시와 결정

- 「좋아. 업로드 하자. 바로 등록」 — 업로드 후 **즉시 공개**.
- 자막 순서: 「자막 먼저 만들고 공개」 — 검증된 시간 자막을 업로드 때 함께 올린다.
- 「고치는 것과 별개로 통과하면 업로드는 진행」 — `upload-ready` 등 게이트 PASS면 진행(기존 테스트 정리는 다른 워커가 따로 한다).
- 「고정 댓글도 달아줘」 + 문구 「확정」 — 아래 3줄을 공개 직후 달고 고정한다.
- 제목·설명·태그는 젠 승인본이며 `SERIES/23-00/output/upload.csv`와 concept `## YouTube Metadata`에 있다. 글자를 바꾸지 않는다.

## 먼저 읽을 것

`MASTER/ai/RUNTIME_RULES.md`(Browser Connection), `skills/wavvy-youtube-publish/SKILL.md`, `skills/wavvy-youtube-publish/references/timed-subtitles.md`(Publish and verify 절), `SERIES/23-00/concept.md`의 `## YouTube Metadata`, 선례 `SERIES/19-30/production/youtube-upload-20261026.json`과 `SERIES/07-00/production/youtube-upload-20261024.json`.

## 선례

- 19:30·07:00 업로드: Studio에서 비공개 초안으로 올려 제목·설명·태그·썸네일·설정을 채운 뒤 공개로 저장. 설정값 `not_for_kids: true`, `ai_generated: true`(변경·합성 콘텐츠 공개 "예"), `paid_promotion: false`, 카테고리 `Music`, 댓글 켬. 업로드 파일 제출 1회. 결과는 `production/youtube-upload-YYYYMMDD.json` + UI 증거 폴더에 남겼다.
- 17:30 자막 게시: Studio 자막 편집기에서 SRT를 **타이밍 포함**으로 올리고, Studio의 수동 한국어 자막 `게시됨`과 공개 시청 페이지의 자막 메뉴·표시 글자를 확인했다(`SERIES/17-30/input/subtitles.json`의 게시 근거 형식).

## 오케스트레이터가 확인한 사실

- 채널: ego lite가 YouTube Studio에 **Wavvy24(@wavvy24, 채널 ID `UC4R4NGwp19Y4lbdNs2HQVcg`)**로 로그인돼 있음(2026-11-04 확인). 업로드 직전 화면에서 다시 확인한다.
- 업로드 파일: `SERIES/23-00/output/final.mkv` (3840×2160 H.264 + FLAC, 6654초, 958,208,576바이트). 썸네일: `SERIES/23-00/input/thumb.jpg` (3840×2160, 1,487,182바이트 — 2MB 이하).
- 자막: `input/subtitles.json`의 SRT 경로·sha256 (게이트 PASS 알림의 값과 같아야 함).

## 할 일

1. **사전 확인**: `python3 wavvy.py gate SERIES/23-00 --stage upload-ready --json`·`verify-release --json`·`verify-subtitles SERIES/23-00 --stage prepared --json` PASS, `ffprobe`로 업로드 파일 해상도·길이·스트림, `upload.csv`의 제목·설명·태그가 concept와 같음을 확인. 하나라도 FAIL이면 멈추고 보고.
2. **브라우저**: `ego-browser skill`을 먼저 읽고 설치된 버전 API만 쓴다. 이 목표용 TaskSpace 하나를 만들어 끝까지 쓴다. `openedBy: "unknown"` 탭은 닫지 않는다. Studio에서 채널 이름·ID가 위와 같은지 확인.
3. **업로드(제출 1회)**: `final.mkv`를 올린다. 제출 전에 콘텐츠 목록에 같은 제목의 초안이 이미 있는지 확인하고, 있으면 새로 올리지 말고 그 초안을 이어 쓴다. 업로드 오류가 나면 같은 클릭을 반복하지 말고 화면을 기록하고 멈춘다.
4. **세부정보**: 제목·설명·태그를 `upload.csv` 값 그대로 입력(설명은 줄바꿈 포함 그대로). 썸네일 `input/thumb.jpg`. 아동용 아님, 변경·합성 콘텐츠 "예", 유료 광고 없음, 카테고리 Music, 댓글 켬, 동영상 언어 한국어(가능하면). 저장 후 초안을 다시 열어 각 칸이 그대로 저장됐는지 확인.
5. **자막**: 자막 편집기에서 한국어로 `input/subtitles.json`의 SRT를 **타이밍 포함**으로 올리고, 미리보기에 시각이 붙은 줄이 보이는지 확인 후 게시. Studio 자막 상태 `게시됨` 확인.
6. **공개**: 공개 상태를 **공개(즉시)**로 저장. 공개 상태 선택을 다시 열어 저장값 확인.
7. **고정 댓글**: 공개 시청 페이지에서 댓글이 열려 있으면 먼저 같은 문구 댓글이 이미 있는지 확인한 뒤, 없을 때만 아래 3줄을 줄바꿈 그대로 1회 게시하고 고정한다. 새로고침 후 고정 표시와 글자를 확인한다.

```
☕ 커피, 바람, 밤, 그리고 Groove
오늘 밤, 이 플리는 어디에서 듣고 계신가요?
마음에 남은 곡 번호나 제목도 댓글로 남겨주세요.
```

8. **공개 페이지 확인**: 제목 일치, 재생 시간(약 1:50:54), 설명의 챕터 표시, 자막 메뉴의 수동 한국어 트랙과 SRT의 첫 큐·중간 큐·2회차 큐(55:27 이후)·마지막 큐 위치에서 보이는 글자. 처리 상태(SD/HD/4K)와 저작권 검사 상태는 **본 그대로** 기록하고 대기를 통과로 바꾸지 않는다.
9. **기록**:
   - `SERIES/23-00/production/youtube-upload-20261104.json`(19:30 형식: 채널·영상 ID·URL·제출 횟수·메타데이터 일치·설정·공개·처리·댓글·자막·증거 경로)과 UI 증거 폴더 `production/youtube-upload-ui-20261104/`.
   - `input/subtitles.json`에 게시 근거(timed-subtitles.md 형식: `studio_raw`·`public_menu_raw` sha 기록, 샘플 원시 스냅샷) 추가 → `python3 wavvy.py verify-subtitles SERIES/23-00 --stage published --json`.
   - `python3 wavvy.py state SERIES/23-00 --check --json` 후 `state --write --phase uploaded --if-match <현재 revision>` → `python3 wavvy.py gate SERIES/23-00 --stage uploaded --json`.
   - concept의 `## Upload Status`를 관찰 결과로 갱신.
   - **`.ai/SESSION.md`·`.ai/HANDOFF.md`·`CHANGELOG.md`는 고치지 않는다**(다른 워커가 같은 시각에 쓰고 있어 오케스트레이터가 마지막에 합친다).

## 멈추고 보고할 조건
- 게이트 FAIL, 채널 불일치, 로그인 화면, 업로드 파일 오류.
- Studio가 젠의 결정을 요구하는 화면(저작권 주장으로 공개 차단·계정 확인 등).
- 같은 오류가 조건 변화 없이 두 번 반복.

## 하지 말 것
- 다른 브라우저(Aside 등)로 바꾸기, `ego-browser upgrade`.
- 업로드 파일 두 번 제출, 기존 공개 영상 수정, 다른 영상 댓글.
- 제목·설명·태그·댓글 글자 변경.
- 로컬 미디어 삭제, git commit·push.

## 보고 형식
단계별 PASS/FAIL, 영상 ID·URL, 제출 횟수, 저장값 확인 결과, 자막 게시·샘플 결과, 공개 상태, 댓글 게시·고정 확인, 처리·저작권 관찰값, 게이트 결과, 증거 파일 경로, 바꾼 파일 목록.
