# 검토 기록 — msg-0630-suno-retries

## 출처
- 보낸 쪽: `/root/suno_replace_preflight_0630` Sol6.1/xhigh 실행 워커. 2026-10-24 동일 Aside/MCP 실행 메시지·최종 인계와 `input/suno-replacement/2026-10-24/retry-{six,renamed,slower}/` 원장.
- 젠 인용은 현재 대화의 “내가 삭제했어.”, “강제 새로 고침 후 다시 업로드해봐. 이름도 좀 바꿔보고”, “재시도해도 안되면 음원도 길이를 수정해. 1bpm 정도 느리게”와 대조했다. 정책·전역 승인으로 확대하지 않는다.

## 주장별 실측
| 주장 | 실측 방법 | 결과 | 판정 |
|---|---|---|---|
| 삭제 보고 뒤 동일6파일 각1회 시도는 전부 거부 | retry29.raw.json의 정확한6파일 오류와 0of6, retry34/35의14개 JSON을 직접 대조; staged6 실제SHA 계산 | 6거부·대기0·이전14 정확 보존. `.ai/validation/2026-10-24-0630-suno-retry-six-check.json` | 채택 |
| 강제 새로고침 완료 | renamed02/03의 time_origin·navigation_type 원문 직접 대조 | 단축키 뒤 변화가 없고 일반reload만 확인됐다. 캐시 우회 성공은 미검증이다. 워커도 이를 완료라고 주장하지 않았다. | 기각 |
| 이름변경6개 중17/19 수락 | 원시 대기열2of6·4failed, top/bottom16 ID·제목·길이 합집합, 신규2 complete, 실제 stagedSHA 직접 대조 | 원래 바이트의17/19 새ID 수락. 이름변경/새로고침이 원인인지는 미확정. `.ai/validation/2026-10-24-0630-suno-renamed-check.json` | 채택 |
| 실패4개의 감속본 기술 검사 통과 | 실제4WAV 전체 표본·형식·길이176/175·원본SHA·유한 표본·클리핑·20ms 완전무음 직접 검사 | 전부 PASS. 기대 길이 오차 약-0.0215초, clip0·신규 내부무음0. `.ai/validation/2026-10-24-0630-suno-slower-audio-check.json` | 채택 |
| 감속9/12 수락·6/11 거부·최종18곡 | slower06 대기열, slower17/18 unfiltered와20/22 restored 전체합집합·필터16/19 원시, uploadMF의 실제staged/output/sourceSHA 직접 대조 | 정확18 ID·한국어제목·길이·complete·선택false, 대기0. `.ai/validation/2026-10-24-0630-suno-retry-final-check.json` | 채택 |
| 원본·Downloads·원장·state 보존 | 입력20와Downloads20 실제SHA; state/sourceMF/candidates/기존교체MF/기존raw5개 HEAD 바이트 대조, 감속 뒤 원본4SHA 재대조 | 보존됨. 새 원격9/12와 기존 로컬9/12는 다른 바이트임을 분리 기록. `.ai/validation/2026-10-24-0630-suno-retry-six-preservation.json` 및 최종 대조 | 채택 |
| 사용자가 영구삭제 완료 | 원래 대화의 사용자 직접 보고와 에이전트 실행 범위 변경 대조 | 사용자 보고만 확인. 에이전트 삭제0·독립 확인false이며 현재 Trash 전수 확인은 하지 않았다. | 부분 채택 |

## 중복 · 충돌 확인
- 찾아본 파일: MASTER/SSOT.md, MASTER/ai/RUNTIME_RULES.md, skills/wavvy-audio-ingest/SKILL.md, SERIES/06-30/concept.md, 기존replacement-manifest와 source download-manifest/candidates, .ai/state.json, .ai/plans/2026-10-24-0630-suno-retry-six.md.
- 결과: 이전14곡·6거부는 첫 업로드 시점 이력이다. 최신 별도원장18곡·2거부와 시점을 구분한다. 기존 출처 후보ID를 새 업로드ID로 대체하지 않는다. 전역175–177 기준·전곡BPM 판정·기존 청취 승인을 새 사본에 옮기지 않는다. 새 영구 정책이나 결정 번호는 만들지 않았다.

## 반대 근거
- 전체20 완료라면20고유ID가 있어야 한다 → 실제18개이고6/11 exact거부가 있다. 전체 완료 주장은 채택하지 않는다.
- 기존 소실·오업로드라면 이전14나17/19가 누락되거나9/12파일SHA/길이가 어긋나야 한다 → 최종 두 집합과 실제 전송사본이 모두 일치한다.
- 캐시 우회 완료라면 단축키 뒤 실제 탐색 변화 또는 지원된 bypass 근거가 있어야 한다 → 단축키 뒤 변화가 없고 일반reload만 확인했다.
- 원시 보존에 누락이 있는지 직접 비교하다 slower17의 upper18 ID 증거가 durable raw에 빠진 것을 확인했다. 워커가 기존 원문을 추가하고 참조 해시를 갱신했다. 이후14개 observation의 실제 원문·sourceSHA를 직접 대조했다.

## 최종 판정
워커의 실행 결과는 위 실측 범위로 채택한다. 사용자 삭제는 보고 사실로만 부분 채택하며 강제 새로고침·캐시 우회 완료와 전체20곡 교체 완료는 채택하지 않는다. 최신 현황을 concept/SESSION/HANDOFF/CHANGELOG에18곡·6/11 거부로 기록했다. 원본20과 별도175목표 사본4개는 각각 보존한다.
