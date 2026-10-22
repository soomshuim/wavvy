# 17:30 시간 맞춤 자막 — 첫 격리 검토 회수 기록

Date: 2026-10-23
Reviewer: `/root/timed_caption_review`, Codex `gpt-6-astra` / `xhigh` (fresh context)
Controller relay: `/root`가 수신한 첫 판정을 실행 워커가 기록함. 이 파일은 reviewer가 직접 작성한 원문 보고서가 아님.
Reviewed artifact: [v1 SRT](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked-v1.srt), SHA-256 `1a439449d9f90a731c0b18cbf634397dddd628abc0f5ff5baab8f6222c430f66`.

## 부모가 수신한 첫 판정

**REVISE — 확인된 High 2건, Critical 0건, 원칙 관찰 없음.** 부모가 아래 원시 자료를 직접 대조했다. 두 건 모두 사용자가 보는 가사 표시의 실제 결함이므로 severity 강등은 없었다.

1. **High 1 — 16번 곡 22행 표시 지연.** `집 앞까지 가고 싶어`의 독립 음향 관측은 곡 상대 92.480–96.540초인데, [v1 자막 근거](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked-v1.json)는 99.097–100.297초에 표시했다. 21행 시작 90.520초와 22행 시작 90.515초의 5ms 경계 역전이 두 행 묶음을 막았고, 후속 보간값이 관측된 자동 자막 범위를 벗어났다. 독립 관측: [16번 곡 Whisper 원시 자료](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-16-line22-88-104-whisper.json).
2. **High 2 — 11번 곡 첫 후렴 반복 누락.** 독립 음향 관측은 11–14행 가창을 38.020–48.820초와 48.820–60.900초에 두 번 확인했다. v1은 11–14행을 45.770–62.039초에 한 번만 표시했다. 독립 관측: [11번 곡 Whisper 원시 자료](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/audio-probe/check-11-first-chorus-35-66-whisper.json).

## 판정 이후 상태

v2에서 위 두 결함을 수정한 뒤, 별도 전곡 대조로 9번 곡 14행의 60.420–64.260초 추가 가창 반복도 발견했다. 최종 현재 [checked SRT](../../SERIES/17-30/input/validation/2026-10-23-timed-subtitles/all-tracks-timed-checked.srt), SHA-256 `29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226`에는 이를 보정했다. **이 첫 REVISE 판정은 v1에만 적용된다.** 최종 파일의 독립 판정은 별도 [최종 검토 기록](2026-10-23-timed-subtitle-final-review.md)에 보존한다. 두 검토 기록은 실제 자막 게시 완료를 뜻하지 않는다.
