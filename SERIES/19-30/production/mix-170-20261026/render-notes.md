# 19:30 · 실제 170 BPM 제작과 검증 범위

현재 제작 방식은 [Rubber Band 계획](rubberband-plan.md)과 `render-rubberband-170.py`예요. 이전 `render-170.py`의 atempo 렌더 경로와 실패 기록은 보존했고 실제 최종 음원 제작에는 실행하지 않았어요. 그 파일의 원본 범위 추출·기존 측정 경로 재사용 함수만 새 제작자가 불러요.

## 소스와 시간 보정

정확한20곡 ID와 순서는 [원래 확정표](../capture-analysis-20261026/sequence.json)를 따랐어요. 각 raw의 UI/PTS 유효 범위를 source0으로 두고 자연 끝까지 모두 전달했어요. 음악 도입이나 긴 tail을 잘라서 붙이지 않았어요. 녹음 대기 padding만 제외했어요. 유효 범위는 캡처 시 UI/PTS 추정이며 출력 지연은 별도 교정되지 않았다는 원래 한계도 남아요.

기존 mid/high 반복주기 측정으로 가이드한 source quarter path를 [입력 시간맵](source-time-maps/)에서 재사용했어요. [Rubber Band map](rubberband-time-maps/)은 본체의 양수 입력 frame을 `first_grid_sample+round(k×288000/17)` 출력 frame에 대응시켜요. 48kHz에서 한 박을16941표본으로 고정해 누적하지 않았어요. source0→output0은 implicit 원점이고, 마지막 입력 전체 길이에 대응하는 정확한 출력 길이는 CLI `-D`로 지정했어요. 드럼이 희박한 도입과 끝은 인접16박 평균 속도로 보간했어요. 입력 전체·총길이·경계 표본·대응 attack 에너지 전개를 검사했어요. 음높이는 `-p0`으로 유지했어요. 첫/끝 표본의 진폭이 같다는 뜻은 아니며, 변환이 음악의 파형 자체를 바꾸는 것이 정상이에요.

## 서로 다른 증거를 분리했어요

- [곡별 수치 요약](source-validation-summary.json): 전체20곡 출력 길이 오차0표본, 대응 attack 위치의 신뢰 구간 p90 최대4ms, mid/high 반복주기 중앙값169.887~170.075BPM, 대응 스펙트럼의 음높이 이동 중앙값 모두0cent였어요. 이 반복주기 검색 범위는 목표 부근이며 보편적인 무전제 BPM 검출기는 아니에요.
- [독립 Beat This 출력](independent-beats/)은 raw 박 시각을 그대로 저장했어요. 전체 단일 median으로 full~170은8곡이고 mixed/uncertain은12곡이에요. mixed를170으로 강제 환산하지 않았어요.
- [20초 구간 진단](model-alias-diagnosis/)은 모델 박간격 분포·170격자 상대 위상·별도 attack autocorrelation·50~220BPM FFT 후보를 함께 남겨요. 예를 들어 Warm Pixels는85와170간격을 섞어 잡고, Night Steps 후반에는 추가 peak가 들어가 단일 모델 median이 달라져요. 대응 입출력 attack 위치와 반복주기 근거를 함께 보므로 모델 단일 median만을 정답으로 취급하지 않아요. FFT 후보도 배음이나 세분박일 수 있어요.
- Dancing Tears의 원곡 half/full 해석, source 첫마디와 downbeat는 청음으로 확정하지 않았어요. 소스의 full pulse 선택은 기존 반복주기 근거를 따랐고170에 가까운 값을 고르지 않았어요. Warm Pixels의 모델 누락 이후 음악과 Glass Horizon의 긴 끝부분도 모두 보존했어요.

## 반복과 연결

[실제 계획](mix-plan.json)은 전체1→20순서를 두 차례 놓은40진입/39연결이에요. 20→1 반복 경계가 한 번 있어요. 각 보정 파일 전체를 쓰고 위치만 옮겨 약1마디의 equal-power 겹침을 만들었어요. 시작·마지막 끝은 자연 보존했어요. quarter grid의 계산 위상은 정렬했지만 정확한 첫마디나 모든 순간의 audible170박이 확인됐다는 뜻은 아니에요. 드럼이 늦게 들어오는 도입을 그대로 두었어요.

[40곡 시각표](tracklist.md)의 시작은 incoming fade 시작 시각이에요. 첫 소리가 들리는 시각이나 확정된 첫박을 뜻하지 않아요. [39개 연결 시각](transition-timeline.csv)은 실제 표본 위치를 기록해요. 과거52:25.54는 대표 배율의 단일 회차 산술 값이고 이번 실제 출력 길이와 달라요.

## 최종 출력

곡별 일정 gain으로 -16LUFS 부근 균형을 준비하고, 전체 조립에 통합 loudnorm을 한 번 적용했어요. 최종 목표는 -14LUFS이며 AAC 뒤 실제 true peak≤-1dBTP를 위해 PCM ceiling을-1.5로 정했어요. 같은 최종 PCM을 분기해 WAV24/48kstereo와 AAC-LC320k를 만들었어요. AAC 인코딩 세대는1이에요.

실제 파일·음량·39연결/40본문의 소스 내용과 표본 위치 검사는 `final-technical-validation.json`, 최종 정본 연결은 `manifest.json`이 맡아요. 이 문서는 그 검사의 성공을 대신하지 않아요. 직접 청음 승인은 없어요. 영상·source-final·공용 상태를 승격하지 않았어요.

최종 실제 길이는299829124표본, 01:44:06.440이에요. [최종 기술 검증](final-technical-validation.json)은 원본20개 지문 불변과79개 내용·위치 검사를 통과했어요. WAV/AAC 상관 최솟값은0.9992305이고 모든 검사창의 위치 차이는0표본이에요. 실제 파일 전체를 잰 음량은 WAV −14.00LUFS/−1.46dBTP, AAC −14.04LUFS/−1.33dBTP예요. [음원 전달 기록](final-premixed-audio.json)은 이번170/capture 전용이며 기존180 계약을 사용한 검사 통과나 영상 승격을 뜻하지 않아요.

## 압축 파일 시간표와 검사 추출

첫 AAC 출력의 말미 packet PTS(압축 조각의 재생 시각)에 한 번 2876표본의 간격이 있었어요. [수정 기록](aac-pts-repair.json)의 `-c:a copy` 재포장으로 시간표만 연속되게 고쳤어요. 모든292803개 packet의 압축 내용과 전체 압축 해제 PCM 지문은 수정 전후 동일해요. AAC를 다시 인코딩하지 않았어요. 첫 priming1024표본과 마지막 packet의 실제 길이900표본도 보존했어요. 최종 재생 시각의 끝은 WAV와 같은299829124표본이고, AAC를 끝까지 해제하면 codec padding124표본이 더 나와요. 원래 AAC와 실패 로그는 work에 보존했어요.

최초 연결16 검사에서는 검사 위치로 바로 이동한 AAC 해제 파형의 상관이0.9397로 기준0.95보다 낮았어요. [원시79구간 기록](final-window-audit.json)과 [독립 추출 대조](transition16-decoder-preroll-audit.json)를 남겼어요. 같은 위치보다1초 또는2초 먼저 해제한 다음 정확한 표본 범위를 선택하면 상관은0.999896이었어요. 이2초 사전 해제 결과는 파일 처음부터 순서대로 해제한 같은 범위와 byte 단위로 같았어요. 따라서 최종 검사는 decoder(압축을 푸는 도구)를2초 먼저 작동시킨 뒤 검사창을 추출해요. 검사 상관·위치 기준과 실제 음원 파일은 이 때문에 바꾸지 않았어요.
