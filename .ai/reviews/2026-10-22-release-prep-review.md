# 17:30 릴리스 출처 연결 준비 — 격리 검토 회수 기록

- 일자: 2026-10-22
- 검토자 작업: `/root/release_prep_review` (격리 reviewer, 호출 설정 `gpt-6-astra` / `xhigh`, `fork_turns=none`)
- 회수 경로: 부모 컨트롤러가 collaboration `FINAL_ANSWER`를 받아 전달했다. 실제 세션 파일명·런타임 설정의 별도 실측은 기록하지 않는다. 이 파일은 검토자가 직접 작성하지 않았다.
- 판정: **CLEAN**, Critical/High 0건, 원칙 관찰 없음. 기존 자막 결함은 이번 변경 판정과 분리됐다.

## 회수 원문

> TLDR; 젠, 이번 변경은 **CLEAN**이에요. 확정된 Critical/High(중대 결함)는 0건이며, 기존 자막 결함 1건은 이번 판정과 분리했어요.
> - 테스트 67개, 상태 검사, `git diff --check`를 직접 실행해 통과했어요.
> - 실제 WAV 3개와 썸네일·배경의 SHA-256(파일 내용 확인값)이 기록과 일치해요.
> - 임시 폴더에서 20곡 출처 연결, 확정 순서, 생성 입력 확인 6곡·미확인 14곡, 보관 후 원본 txt 20개 보존을 확인했어요. **없는 WAV 17개에는 시험용 파일을 사용했으므로, 전곡 음원 확보·음질 검증 결과는 아니에요.**
> - 원칙 관찰: 없음.
> 별도 기존 결함: wavvy.py:2158은 대괄호 지시가 하나인 줄만 제거해요. `[Chorus] [Strong high chest-mix belt]`처럼 지시가 두 개인 줄은 자막에 남아요.
> 실제 2번 곡 화면 가사로 재현한 원시 결과:
> current_equals_baseline: true
> leaked_lines_count: 6
> 예: [Chorus] [Strong high chest-mix belt]
> 예: [Instrumental] [Rhodes reply]
> 예: [Outro] [Instrumental]
> 실제 20곡 출처를 사용하는 임시 보관 시험에서는 이런 지시문이 총 76줄 남았어요. 기준 커밋의 함수도 동일한 결과를 내므로 이번 변경에서 생긴 결함은 아니에요.
> 영향 경로는 prepare-subtitles:2711 → youtube_subtitles_ko_no_timing.txt예요. 업로드 준비 검사 wavvy_harness/gate.py:914는 자막 파일의 존재만 확인하므로 이 내용을 잡지 못해요. 최종 자막 제작 전에 별도 수정이 필요해요.

검토 범위는 릴리스 출처 연결과 임시 대역을 이용한 구조 검사다. 실제 20개 WAV의 확보·음질 확인이나 YouTube 업로드 판정이 아니다. 위 기존 자막 결함의 수정은 [별도 검토](2026-10-22-subtitle-fix-review.md)에 기록한다.
