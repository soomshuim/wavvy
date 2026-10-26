# 19:30 — 170 BPM 음원 통합 계약 조사와 이번 실행 범위

기록일: 2026-10-26. 이 문서는 기존 규칙·07:00 실물 선례와 이번 컨트롤러 결정을 구분해 보존한다. 음원 생성·검증 결과는 실제 제작 manifest가 소유하며, 이 조사 문서가 완료 판정을 대신하지 않는다.

## 원본 규칙과 실물 선례

- [SSOT](../../../../MASTER/SSOT.md)의 State Writer Rule은 `.ai/state.json`을 `python3 wavvy.py state SERIES/[series] --write`로만 쓰도록 한다. 수동 편집은 금지다. `source_final`은 확정 소스 계약과 실제 산출물 조건을 갖춘 단계다.
- [CLI SPEC](../../../../MASTER/cli/SPEC.md) §4 D의 일반 `pack`은 `--repeat 2`, 곡별 **-14 LUFS**(체감 평균 크기)·**-1.0 dBTP**(재생 최고점 기준) 기본값과 영상 렌더를 묶는다. 일반 결과는 `output/final.mkv`·`report.json` 등이다. 오디오 전용 170 BPM 명령으로 정의된 것은 아니다.
- [실제 07:00 제작 기록](../../../07-00/production/continuous-180-20261024/manifest.json)은 **48 kHz·스테레오 AAC-LC 320k M4A**를 `output/continuous-180-20261024/continuous-mix-0700-repeat2.m4a`에 저장했다. 곡별 일정 gain(음량 배율)의 목표는 -16 LUFS였고, 최종 실측은 -15.95 LUFS·-3.04 dBTP였다. 이 값은 일반 pack 기본값과 구분되는 해당 제작의 선례다.
- 같은 기록은 `repeat_count: 2`, `additional_repeats: 0`과 **40개 실제 진입·39개 연결**을 저장한다. 전체 1→20 순서를 두 차례 재생하며 첫 회 20→다음 회 1 연결을 포함한다. 곡마다 두 번씩 붙이는 순서가 아니다.
- 07:00 manifest는 선택 20 ID, 원본·보정 파일 지문, 보정 기록·독립 박자 기록, 계획·제작 스크립트 지문, 실제 샘플 단위 연결 구간, 최종 디코드·샘플 수·음량 검증을 연결한다. 자동 기술 측정은 직접 청음 승인으로 기록하지 않는다.
- [WORKFLOWS](../../../../MASTER/WORKFLOWS.md)의 `Final Premixed Audio`와 [CLI SPEC](../../../../MASTER/cli/SPEC.md)의 retained-premix 계약은 최종 AAC/JPG·제작 근거·40개 실제 시각을 묶는다. 이미 두 번 반복된 AAC에 `pack`이나 추가 반복을 적용하지 않는다. 영상·게시 검증은 별도 단계다.
- 현행 [premixed_audio.py](../../../../wavvy_harness/premixed_audio.py)의 `_corrected_repeat_evidence`는 `wavvy.continuous_180_plan.v1`, `target_bpm == 180`, `wavvy.reacquisition.v1`을 고정 확인한다. 이번 **170 BPM·브라우저 녹음** 근거를 기존 180/다운로드 재취득 근거로 바꿔 부르는 것은 이 계약의 올바른 재사용이 아니다.
- [RUNTIME_RULES](../../../../MASTER/ai/RUNTIME_RULES.md)는 Pydub 사용 금지, 오디오 acrossfade(두 소리를 겹치며 전환)와 비디오 xfade 구분, 작은 유효 시험→예상 길이 확인→완료 후 해당 범위 검증을 요구한다.

## 이번 사용자 승인과 컨트롤러 결정

사용자 원문: “썸네일은 내가 만들고 알려줄게 너는 음원 만들어. 170BPM 맞추고 곡간 박자 연결되도록 (앞 구간 박자가 늦게 쌓여 들어오는 곡은 어쩔 수 없고. 과감하게 앞을 자르거나 하진마) 2번 반복 알지?”

- **오디오만 제작한다.** [확정 순서](../capture-analysis-20261026/sequence.json)의 Goodbye 1번과 20곡 전체를 두 차례 재생한다. 썸네일 마무리는 젠이 직접 한다. 이번 승인은 영상 렌더·업로드·추가 생성 승인이 아니다.
- **170 BPM으로 맞추고 곡간 박자를 연결한다.** 도입을 과감하게 자르지 않으며 박자가 늦게 쌓이는 구간과 끝 전개를 보존한다. 07:00의 고정 16박 겹침이나 도입 잘라내기를 자동 이식하지 않는다. 실제 처리·검증 수치와 연결 방법은 이번 제작 계획·manifest에 기록한다.
- **출력은 실제 WAV와 M4A다.** 오디오 담당과 컨트롤러가 정한 경로는 `SERIES/19-30/output/mix-170-20261026/continuous-mix-1930-repeat2.wav` 및 `.m4a`다. 같은 최종 PCM(압축 전 음원 표본)에서 **WAV 24-bit/48 kHz 스테레오**, **AAC-LC 320k/48 kHz 스테레오 M4A**를 만든다. 음량 목표와 최종 실측값은 실제 제작 기록으로 확인한다.
- 새 170/브라우저 녹음 전용 제작 manifest와 실제 파일의 직접 기술 검증으로 이번 오디오 작업의 완료를 판정한다. 20 ID·원본 유효 범위/지문, 170 보정 결과와 박자 검증, 40 진입·39 연결의 실제 시각, 두 출력의 디코드·길이/샘플 수·음량/최고점을 묶는다. 정확한 첫박이 불확실한 곳과 자동 측정의 한계는 그대로 기록한다.
- 공용 검증기 개정·기존 180 검사 우회·`Final Premixed Audio` 승격은 이번에 하지 않는다. `source-final`·영상·게시 완료로 주장하지 않는다. 기존 raw(녹음 원본)와 실패 시도도 보존한다.
- **공용 state는 이번에 쓰지 않는다.** 읽기 전용 `python3 wavvy.py state SERIES/19-30 --json`은 `track_source_draft`를 추론했으나 이는 실제 170 오디오 제작 단계를 표현하지 못한다. 확인 당시 저장 상태는 revision 97·07:00·uploaded였다. 거짓 phase(진행 단계)로 강제 승격하지 않고 `concept.md`와 이번 실제 제작 manifest에 현재 음원 상태를 기록한다.
- 정상 writer가 향후 필요한 경우 명령은 `python3 wavvy.py state SERIES/19-30 --write --if-match N --json`이다. `N`은 쓰기 직전 읽은 revision(상태 버전)이며, 이번 조사에서는 실행하지 않았다.

20곡 원곡 범위 합계 **3,972.4초(66:12.4)**와 170 BPM 대표 비율의 1회 무겹침 계산치 **3,145.54초(52:25.54)**는 기존 분석 값이다. 계산치는 두 번 반복·실제 연결·오디오 출력 완료 길이가 아니다. 이 문서 작성 시점에 최종 음원은 제작 중이며 완료 파일이나 검증 결과를 선행 확정하지 않는다.
