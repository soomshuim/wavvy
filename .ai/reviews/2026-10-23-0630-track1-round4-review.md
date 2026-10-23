# 06:30 1번 네 번째 제출 후보: 30초 박자 판정 기록

젠이 승인한 박자 지시 수정문구로 낸 1번 네 번째 제출의 두 후보에 관해, 격리 BPM 검토자의 판정을 컨트롤러가 원시 코드로 재현해 채택했다. 이는 **원본 오디오의 연속 30초** 범위 판정이며, 자동 분석 JSON의 `uncertain`을 덮어쓰지 않는다.

| 후보 ID | 샘플 SHA-256 | 독립 격자 추정 | 채택 판정 |
|---|---|---|---|
| `24703f3f-c7ce-433f-a892-16d9330b41a9` | `e1ec292f0c079d3eaecad339cc6aa7a5907a9e31ac3653861e3738d9cfe010d9` | 중음 187.746 BPM, 관측 span 29.062초 | `out` |
| `7c3c2109-9aa8-4296-844e-441d60757eb4` | `bd9ffcbd669f4e2db3c9d0be8d2235ccc91d9fa7c8833b324960ce3d06cb0ddf` | 중음 193.258 BPM, 관측 span 27.578초 | `out` |

컨트롤러의 같은 코드 재현은 두 원시 파일 모두 종료 0, 후보 ID·샘플/원녹음/로그 해시·정확한 30초·원녹음에서 자른 구간의 전값 일치를 확인했다. 원시 파일:

- `SERIES/06-30/input/bpm-audit/validation/independent-review-track1-round4-a.jsonl` · SHA-256 `2b8cce1eb3e1c09eb587b3920fdab2a04ce0387d126a000289322290ed32474d`
- `SERIES/06-30/input/bpm-audit/validation/independent-review-track1-round4-b.jsonl` · SHA-256 `afd22ec9feffdbaf63156ad05c6abda41fa686f3b09c1ec1090e865120d50c2f`

현재까지 1번은 네 번 제출한 여덟 후보가 모두 `out`이다. 이 두 후보의 Suno 휴지통 이동은 실행하지 않았으며, 다섯 번째 제출도 자동 진행하지 않는다. 음높이 유지 길이 조절 [별도 30초 시험](../../SERIES/06-30/input/bpm-audit/validation/2026-10-23-track1-atempo-pilot.json)은 원본 후보의 독립 판정을 바꾸지 않는다. 최종 선택은 0개다.
