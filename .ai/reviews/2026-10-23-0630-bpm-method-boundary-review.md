# 06:30 BPM 분석 방법 경계 재검토 — 2차 REVISE

Date: 2026-10-23
Reviewer: `/root/bpm_final_review`, 격리 Codex `gpt-6-astra` / `xhigh`
Scope: `SERIES/06-30/input/bpm-audit/analyze.py`의 수정 시점 코드와 합성 음원 재현. 실제 Suno 후보의 유효 분석 음원과 BPM 측정은 각각 0개다.
Result: **REVISE — 확인된 High 1건, Critical 0건, 원칙 관찰 없음.** 컨트롤러가 전달한 독립 검토 판정의 요지다. 분석 담당자가 두 번째 수정을 진행 중이며 최종 준비 완료나 CLEAN 판정이 아니다.

## High 1 — 짧은 구간의 경계 밖 박자를 최종 판정에서 제외

검토 대상이던 `analyze.py`(SHA-256 `8c7247ad09f617a5ccf8c9d7d8c9e0cb6af6d6e5a7833afccbbbbdc5f97a2fd6`)의 300–306행은 짧은 구간의 박자를 기준 박자와 ±0.80 BPM으로 비교했지만, 340–354행의 최종 BPM 구간에는 그 짧은 구간 값을 넣지 않았다. 이는 **검토 당시 코드**의 위치이며 수정 중인 현재 코드의 줄 번호나 동작을 단정하지 않는다.

190초 합성 음원의 기본 박자 175.35 BPM에서 55–67초만 174.6 BPM으로 바꿨다. 검토 당시 출력은 `inside`(175–177 안), `reasons: []`, 보수적 구간 175.08369–175.55149였다. 그러나 56–64초와 60–68초의 짧은 창은 모두 174.5947 BPM을 측정했고, 각 coverage(검출된 박자 포착률)는 0.9583·1, residual p95(박자 위치 오차의 95% 지점)는 모두 4.85 ms였다. 경계 밖인 174.6 BPM 구간을 측정해 놓고 최종 `inside`로 통과시킨 재현이다.

[검토 당시 원시 출력](../../SERIES/06-30/input/bpm-audit/validation/review-original-boundary-short-tempo.json)(파일 SHA-256 `e5fe981c63b9dd6bb3f94269d73168af39758b5fadfa7514727ddc130c1679e2`)과 [재현 코드](../../SERIES/06-30/input/bpm-audit/validation/reproduce-boundary-short-tempo.py)를 프로젝트에 보존했다. 재현 코드의 float32 합성 음원 SHA-256은 `13beafd257d39deaf5149af2333109de60e71e6ad9a037b9dca2a64d5aacd228`이다. 원시 JSON의 판정·구간·두 짧은 창 수치를 직접 대조했다.

새 독립 분석 산출물의 결함이므로 워크플로우 기준 심각도는 **High 유지**다. 사용자에게 이 문제는 즉시 보고됐고, 실제 후보 삭제는 0건이다. 이 경계 검토는 [1차 BPM 방법 검토](2026-10-23-0630-bpm-method-review.md)의 REVISE와 같은 분석 작업의 후속 판정이다. 앞선 [생성 원문 검토](2026-10-23-0630-source-review.md)의 CLEAN과 범위를 혼동하지 않는다.
