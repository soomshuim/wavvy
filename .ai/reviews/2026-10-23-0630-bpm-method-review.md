# 06:30 BPM 분석 방법 독립 검토 — 1차 REVISE

Date: 2026-10-23
Reviewer: `/root/bpm_audit_review`, 격리 Codex `gpt-6-astra` / `xhigh`
Scope: `SERIES/06-30/input/bpm-audit/analyze.py`와 합성 음원 검증만. 실제 Suno 후보의 유효 분석 음원·BPM 측정은 각각 0개다.
Result: **REVISE — High 1건, 원칙 관찰 없음.** 이 문서는 컨트롤러가 전달한 독립 검토 판정의 요지를 기록한다. 수정 후 재검토 판정이나 최종 CLEAN을 뜻하지 않는다.

## High 1 — 구간 사이의 템포 변화를 놓침

190초 분석의 구간은 0–55초, 67.5–122.5초, 135–190초다. 그 사이 55–67.5초와 122.5–135초가 검사 구간에서 빠진다. 짧은 템포 변화는 전곡 `p95`(값을 크기순으로 놓았을 때 95% 지점의 오차)에도 묻혀, 계획 18행의 “구간 변화는 `uncertain`(수동 확인 필요)” 요구를 위반할 수 있다.

- 176 BPM 합성 음원의 58–62초만 190 BPM으로 바꾼 재현은 `inside`(목표 범위 안), 보수적 구간 175.79880–176.20240, `reasons: []`로 나왔다. 검토 당시 원시 출력: `/tmp/wavvy-bpm-review-brief-190-tempo.json`.
- 180 BPM 합성 음원의 56–65초만 176 BPM으로 바꾼 재현은 `out`(목표 범위 밖), 보수적 구간 179.79881–180.21072, `reasons: []`로 나왔다. 검토 당시 원시 출력: `/tmp/wavvy-bpm-review-outside-with-inside-patch.json`.

두 재현에서 바뀐 구간이 세 검사 창 사이에 놓이고 `reasons`가 비어 있음을 원시 JSON에서 대조했다. `/tmp` 출력을 바이트 그대로 보존한 파일은 [176→190 짧은 구간 원시 결과](../../SERIES/06-30/input/bpm-audit/validation/review-original-brief-190-tempo.json)(SHA-256 `6872f38acbc197fb9d82a22b31341b6ec2efc276838bf3de9886c0d61300f9b6`)와 [180→176 짧은 구간 원시 결과](../../SERIES/06-30/input/bpm-audit/validation/review-original-outside-with-inside-patch.json)(SHA-256 `4f78837e2527bbd3ecf78fb552dbabd88bbb5c137f4096bef9cb9e22a23e84ec`)다. [재현 코드](../../SERIES/06-30/input/bpm-audit/validation/reproduce-short-tempo.py)도 프로젝트에 보존됐다. 이 기록만으로 실제 Suno 후보의 BPM을 판정하지 않는다.

## 범위·후속 상태

이는 새 독립 분석 산출물의 결함이므로 워크플로우 기준 심각도도 **High 유지**다. 실제 후보의 유효 분석 음원 0개, BPM 측정 0개, 삭제 0개여서 현재 실제 삭제 영향은 0이다. 분석 담당자가 수정 중이며 그 결과는 아직 이 문서에서 판정하지 않는다. 앞선 [생성 입력 검토](2026-10-23-0630-source-review.md)의 CLEAN은 20곡 생성 원문에 한정하며 이 BPM 분석 방법의 REVISE를 덮지 않는다.
