# 19:30 현재 20곡 브라우저 녹음 완료

경로 기준: 이 문서와 동봉한 `capture-manifest.json`의 `work/...` 경로는 저장소 루트 `/Users/zenkim_office/Project/wavvy`를 기준으로 한다. 원본 WAV·시간표·실측 파일은 해당 로컬 경로에 보존하며 Git에 추가하지 않는다. 이 폴더에는 녹음 요약과 검증 기록만 복사했다.

공개 정본의 20개 고유 ID와 정확히 일치하는 전체 녹음을 확보했다. 모든 유효 원본은 48,000 Hz·스테레오·Float32이다. 1배속 재생과 UI 자연 끝, PTS(오디오 조각의 시간표) 연속, 비영(0이 아닌) 신호, 쓰기 오류 없음, 종료 코드 0을 확인했다. 최종화 시 20개 원본 SHA-256(파일 내용 확인값)을 다시 대조했다.

실제 미디어 곡길이 합계 3972.40초. UI 분·초 표시 합계는 66분 12초로, 소수초를 가진 미디어 길이와 조금 다르다. 원본 raw(가공하지 않은 녹음)는 자르거나 속도를 바꾸지 않았다.

Goodbye를 먼저 녹음했다. 아래 번호는 임시 녹음 순서이며 최종 앨범 순서는 아직 정하지 않았다. 직접 청음과 음악 품질 판정은 수행하지 않았다. 곡별 파형·BPM(1분당 박 수)·다운비트(마디의 첫 박)·연결 분석 담당에게 각 유효 파일과 경계 근거를 전달했다.

| 임시 순서 | 곡 | 미디어 길이(초) | 유효 시도 | raw 시작 추정(초) |
|---|---|---:|---|---:|
| 01 | Goodbye | 202.00 | attempt-03 | 2.359043 |
| 02 | Faded Polaroid | 213.20 | attempt-01 | 9.340629 |
| 03 | Warm Pixels | 199.92 | attempt-01 | 2.365013 |
| 04 | Small Satellites | 209.92 | attempt-01 | 2.323714 |
| 05 | Still a Spark | 216.00 | attempt-01 | 2.295098 |
| 06 | After The Rain | 168.00 | attempt-01 | 2.259182 |
| 07 | Night Steps | 219.12 | attempt-01 | 2.360874 |
| 08 | Half Past Home | 208.96 | attempt-01 | 2.372964 |
| 09 | Paper Lanterns | 209.96 | attempt-01 | 2.352556 |
| 10 | Keep the Window Open | 224.72 | attempt-01 | 2.375707 |
| 11 | Sunday Voltage | 165.20 | attempt-01 | 2.445493 |
| 12 | Glass Horizon | 192.24 | attempt-01 | 2.398229 |
| 13 | Open Roads | 182.24 | attempt-01 | 2.452571 |
| 14 | Pocket Sunrise | 156.00 | attempt-01 | 5.918638 |
| 15 | Blue Current | 197.60 | attempt-01 | 2.365030 |
| 16 | In Da Dream | 237.20 | attempt-01 | 5.678261 |
| 17 | Pulse | 209.88 | attempt-01 | 2.507463 |
| 18 | Sunlit | 189.56 | attempt-01 | 5.909614 |
| 19 | A Sorrow Beyond Dreams | 167.48 | attempt-01 | 2.484043 |
| 20 | Dancing Tears | 203.20 | attempt-01 | 6.194490 |

정확한 ID·원본 경로·SHA-256·시간 범위·신호값·PTS·자연 끝 근거는 [capture-manifest.json](capture-manifest.json)에 있다. 각 시도의 capture-verification.json, ui-timeline.json, raw.wav.timing.json을 보존했다.

Goodbye의 첫 무음 시도와 두 번째 부분 시도, 활성 탭 시험 녹음도 별도 보존했고 유효 20곡에서는 제외했다. 실제 활성 기존 Suno 탭으로 전환한 뒤 신호가 정상화됐다. 시스템 음소거·음량·오디오 장치는 변경하지 않았다.

마지막 곡 자연 끝 뒤 다음 곡 자동 재생을 막았다. 최종 UI의 두 audio 요소는 모두 일시정지였다. 활성 Suno 탭을 그대로 두었으며 녹음 프로세스는 0개였다.

곡 경계는 UI 시간과 PTS를 연결한 추정이며 브라우저 출력 지연은 별도 보정하지 않았다. 캡처 대상은 Aside 앱 전체이므로 탭 한정 녹음이라고 주장하지 않는다. 의도적인 첫 쉼이나 단음 사이 침묵은 자동 제거하지 않았다.
