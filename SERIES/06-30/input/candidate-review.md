# 06:30 — 전달본 청취 판정과 현재 후보 선택

## 2026-10-24 최종 음원 입력 20곡 확보

젠의 “모두 통과. 음원 최종 확보해.”로 선택한 20개 ID의 최종 전곡 WAV를 확보했다. 그때의 청취 승인은 정확한 8·13·18번 173 목표 30초 파일과 5·20번 원속도 전곡 파일에 속한다. 이번 18개 처리 전곡에 새 청취 승인을 추가하지 않는다.

- 8·13·18번은 173 BPM 처리 목표, 나머지 보정 대상 15곡은 176 목표이며 5·20번은 원속도 바이트를 보존했다. 전곡 실측 BPM은 미확인이라 파일명은 NA, 목록의 bpm_measured는 null이다.
- 청취 사본 20개와 자동 재생 없는 index.html을 `/Users/zenkim_office/Downloads/wavvy-0630-final-audio-20261024`에 만들었다. 원본·원시 캡처·실패 파일·기존 Downloads 자료는 보존했다.
- 12번은 중간 끊김이 있는 첫 원본을 제외하고 정상 r2만 사용했다. 14번은 선택 ID 하나만 라이브러리로 복원했고, 네 번째 시도는 컨트롤러가 반복 실패 규칙으로 중단했다. 젠의 추가 한 번 승인 뒤 성공한 r5만 사용했다. 과거 휴지통 이력과 실패 네 회는 보존했다.
- 2번은 원본 약 193초 이후 fade(소리가 점점 작아지는 끝부분)의 단독 정밀 BPM을 인증하지 않는다. 6·9·11·17·19번은 출력 전에 선택한 mid(중음역) 측정 근거를 썼다. 9·17번 원본 약 206초 이후와 19번 약 190초 이후 fade도 같은 한계가 있다. 17·19번의 마지막 30초 평균과 마지막 단독 박자 해석 차이는 곡별 measurement_limit에 보존했다. 13번의 UI(화면 조작 상태) pause 확인 경합과 대신 보존한 원시 경계·수동 정지 근거는 목록의 acquisition_note에 유지했다.
- 20곡의 전체 직접 파일 검사와 18개 처리곡의 앞·중간·끝 30초 측정 54개를 재현했다. 내부 20ms 이상 완전 무음·클리핑·기술 오류는 0건이다. 독립 Astra high 검토는 CLEAN(확인된 Critical/High 0·원칙 관찰 없음)이며 공식 state writer로 revision84 track_source_draft와 실제 입력 음원20개를 기록했다. 이번 음원 확보 범위의 남은 작업은 없다. 새 전곡 청취 승인, 모든 순간의 BPM 인증, source_final 또는 발매 완료를 선언하지 않는다.

| 순서 | 선택 후보 ID | 전곡 처리 | 원속도 원본 | 실제 최종 입력 |
|---:|---|---|---|---|
| 1. 첫 박부터 | 24703f3f-c7ce-433f-a892-16d9330b41a9 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/01__%EC%B2%AB%20%EB%B0%95%EB%B6%80%ED%84%B0__Driven__Hardcore%20Punk%20Rock__NA.wav) |
| 2. 가속선 | 67d6a052-21ef-4c59-be09-790468e75152 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/02__%EA%B0%80%EC%86%8D%EC%84%A0__Driven__Post%20Hardcore%20Rock__NA.wav) |
| 3. 빛나는 노면 | 872b0aac-6e44-4d54-b8e0-c546359be0fe | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/03__%EB%B9%9B%EB%82%98%EB%8A%94%20%EB%85%B8%EB%A9%B4__Driven__Electronic%20Breakbeat__NA.wav) |
| 4. 전력 곡선 | 5ac0c138-5643-43ee-a2e4-07b02a794cbb | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/04__%EC%A0%84%EB%A0%A5%20%EA%B3%A1%EC%84%A0__Driven__Hard%20Rock__NA.wav) |
| 5. 빛의 마찰 | b868f3f7-a1fb-4cc7-aa18-e6202df90dcd | 원속도 유지 | 전곡 확보 | [WAV](tracks/05__%EB%B9%9B%EC%9D%98%20%EB%A7%88%EC%B0%B0__Driven__Electronic%20Breakbeat__NA.wav) |
| 6. 다리의 불꽃 | e2196f98-b0f6-432b-b8a2-a900af30a793 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/06__%EB%8B%A4%EB%A6%AC%EC%9D%98%20%EB%B6%88%EA%BD%83__Driven__Hardcore%20Punk%20Rock__NA.wav) |
| 7. 하늘을 밀어 | b1e7fe46-ab35-46fd-85a7-25433230a485 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/07__%ED%95%98%EB%8A%98%EC%9D%84%20%EB%B0%80%EC%96%B4__Driven__Alternative%20Hard%20Rock__NA.wav) |
| 8. 유리 번개 | 45acc3bc-6c0a-4472-b87f-9c36adba05bf | 173 BPM 목표 | 전곡 확보 | [WAV](tracks/08__%EC%9C%A0%EB%A6%AC%20%EB%B2%88%EA%B0%9C__Driven__Electronic%20Breakbeat__NA.wav) |
| 9. 한계 위로 | aadf83c5-cd5f-47d0-9819-0d3cbb86efd0 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/09__%ED%95%9C%EA%B3%84%20%EC%9C%84%EB%A1%9C__Driven__Post%20Hardcore%20Rock__NA.wav) |
| 10. 전류의 발끝 | 8392855c-26db-400e-9553-e32df268d2c0 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/10__%EC%A0%84%EB%A5%98%EC%9D%98%20%EB%B0%9C%EB%81%9D__Driven__Electronic%20Breakbeat__NA.wav) |
| 11. 계속 앞으로 | 4aebcc2f-5d02-4761-9dc0-23cef9479acf | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/11__%EA%B3%84%EC%86%8D%20%EC%95%9E%EC%9C%BC%EB%A1%9C__Driven__Hardcore%20Punk%20Rock__NA.wav) |
| 12. 폭발 직전 | 704d6663-6a2f-4a17-ba75-9a87bf768e7a | 176 BPM 목표 | r2 확보 | [WAV](tracks/12__%ED%8F%AD%EB%B0%9C%20%EC%A7%81%EC%A0%84__Driven__Post%20Hardcore%20Rock__NA.wav) |
| 13. 황금 주파수 | b51b42b3-2537-483a-b3ab-a65c4274fe6a | 173 BPM 목표 | 전곡 확보 | [WAV](tracks/13__%ED%99%A9%EA%B8%88%20%EC%A3%BC%ED%8C%8C%EC%88%98__Driven__Electronic%20Breakbeat__NA.wav) |
| 14. 높은 기어 | f8df1271-a60c-465b-900f-a8863c86f8dc | 176 BPM 목표 | 복원·승인 r5 확보 | [WAV](tracks/14__%EB%86%92%EC%9D%80%20%EA%B8%B0%EC%96%B4__Driven__Hard%20Rock__NA.wav) |
| 15. 번쩍이는 궤도 | b9c055a2-3726-4073-a103-801dcfafd1bf | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/15__%EB%B2%88%EC%A9%8D%EC%9D%B4%EB%8A%94%20%EA%B6%A4%EB%8F%84__Driven__Electronic%20Breakbeat__NA.wav) |
| 16. 가속의 틈 | 7c3bc62b-2599-4bf1-aecc-212fff88d556 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/16__%EA%B0%80%EC%86%8D%EC%9D%98%20%ED%8B%88__Driven__Hardcore%20Punk%20Rock__NA.wav) |
| 17. 몸이 먼저 | fe8164a4-9a09-4bc0-8414-0f1ad368605b | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/17__%EB%AA%B8%EC%9D%B4%20%EB%A8%BC%EC%A0%80__Driven__Post%20Hardcore%20Rock__NA.wav) |
| 18. 빛을 따라 | af2385fb-8638-4392-a9a0-7a031e31853e | 173 BPM 목표 | 전곡 확보 | [WAV](tracks/18__%EB%B9%9B%EC%9D%84%20%EB%94%B0%EB%9D%BC__Driven__Electronic%20Breakbeat__NA.wav) |
| 19. 끝까지 당겨 | 08faf4f4-f3fa-404d-97a6-f0515f9ceed3 | 176 BPM 목표 | 전곡 확보 | [WAV](tracks/19__%EB%81%9D%EA%B9%8C%EC%A7%80%20%EB%8B%B9%EA%B2%A8__Driven__Hardcore%20Punk%20Rock__NA.wav) |
| 20. 다시 점화 | 6a6baa59-8576-4538-a157-b2410ce326d0 | 원속도 유지 | 전곡 확보 | [WAV](tracks/20__%EB%8B%A4%EC%8B%9C%20%EC%A0%90%ED%99%94__Driven__Electronic%20Breakbeat__NA.wav) |

실제 파일 해시·출처·곡별 한계는 [최종 목록](download-manifest.json)에 있다. 아래 2026-10-23 내용은 그 당시 청취·비교 이력이며 현행 수집 상태와 구분한다.

## 2026-10-23 청취·비교 이력
젠의 “모두 통과”는 [처음 전달한 30초 청취본 20개](tempo-adjustment/2026-10-23-listening-delivery.json)의 청취 통과다. 그중 18개는 176 BPM 목표 보정 미리듣기였고 5·20번은 원본 속도 30초였다. 현재 곡별 선택 ID는 20개다. 1–19번은 전달본 ID와 선택 ID가 같고, 20번은 젠이 Suno에 한 곡만 남긴 뒤 녹음을 요청한 현재 후보 `6a6baa59-8576-4538-a157-b2410ce326d0`다. 20번의 옛 전달본 ID `5f0f2be1-7ec8-4f36-aa18-8af4b43199c7`에 대한 청취 판정을 현재 후보의 새 소리로 옮기지 않는다.

8·13번은 앞서 [175 BPM 목표 30초 비교본](tempo-adjustment/slower-08-13/2026-10-23-slower-08-13-target175-provenance.json)을 받았고, 두 파일은 사용자 청취 승인을 받지 않은 비교 이력이다. 이어 젠의 “13, 18, 8은 173 목표로 만들어봐”로 8·13·18번의 [173 BPM 목표 새 30초 비교본](tempo-adjustment/target173-08-13-18/2026-10-23-target173-08-13-18-provenance.json) 세 개를 받았다. 현재 세 파일의 청취 판정은 대기다. 후보 ID는 그대로이고 18번은 로컬에 남은 과거 후보이며 Suno 원격 휴지통을 복구하지 않았다. 기존 176 목표 전달본의 “모두 통과” 기록과 SHA-256은 그 파일에만 적용된다. 독립 절반 격자 측정은 새 파일 첫 30초 결과이며 전곡 175–177 BPM 기술 판정이나 범위 예외가 아니다.

5·20번의 [Aside MCP 원시 화면 기록](selected-recordings/2026-10-23/live-selection-ui.json)에서 현재 Suno 검색은 각각 한 행만 확인했다. 젠의 “5번 20번도 다운로드 폴더에 사본 넣어줘. 다른 것들과 비교해보게”에 따라 [5번](selected-recordings/2026-10-23/05-capture-provenance.json) 200.6초와 [20번](selected-recordings/2026-10-23/20-capture-provenance.json) 210.2초를 앱 출력에서 원속도로 녹음해 Downloads 루트에 동일 해시 사본을 뒀다. 이는 공식 Suno 다운로드나 정식 최종 WAV, 음악적 품질·전곡 175–177 BPM 합격을 뜻하지 않는다. 12·14·18번의 옛 후보 원격 휴지통 상태는 이번 작업에서 건드리지 않았다. 다른 곡의 현재 원격 개수는 재조사하지 않았다.

| 순서 | 제목 | 전달본 출처 후보 ID | 전달 파일 | SHA-256 | 속도 | 원격/로컬 상태 | 청취 판정·현재 선택 |
|---:|---|---|---|---|---|---|---|
| 01 | 첫 박부터 | `24703f3f-c7ce-433f-a892-16d9330b41a9` | `01_첫 박부터_target176-preview.wav` | `395f9b028031551013490682cd8b5bee6482d242121ab585d3883720e17165ff` | 보정 ×0.937436750 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 02 | 가속선 | `67d6a052-21ef-4c59-be09-790468e75152` | `02_가속선_target176-preview.wav` | `39ca39e5edc107cd86b5fe4ea5ffb64da8737a5889915288822a3acd892695bb` | 보정 ×0.974421437 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 03 | 빛나는 노면 | `872b0aac-6e44-4d54-b8e0-c546359be0fe` | `03_빛나는 노면_target176-preview.wav` | `d40bcd2ec083e5f7f858c8d4a3c82cd7625a33e465f2a465bfe0301780347d98` | 보정 ×0.999063378 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 04 | 전력 곡선 | `5ac0c138-5643-43ee-a2e4-07b02a794cbb` | `04_전력 곡선_target176-preview.wav` | `15c578d147e9e569ebdcd78c968d439237140653694e5e24679e658ffc95e134` | 보정 ×0.998411618 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 05 | 빛의 마찰 | `b868f3f7-a1fb-4cc7-aa18-e6202df90dcd` | `05_빛의 마찰_원본속도_박자확인용.wav` | `ca3768edc5efe6879e3ba528cb99f4b4508fecea9131bddec93c8674bc30344f` | 원본 속도 ×1.0 | 현재 Suno 검색 한 행·전달 ID 일치 | 전달본 청취 통과·현재 동일 ID 선택; 전곡 녹음 보존 |
| 06 | 다리의 불꽃 | `e2196f98-b0f6-432b-b8a2-a900af30a793` | `06_다리의 불꽃_target176-preview.wav` | `9332ec28233e49d24f52a9f627f740ca9fe544e0fb535f700a3b90a7dc8f06b7` | 보정 ×1.028337715 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 07 | 하늘을 밀어 | `b1e7fe46-ab35-46fd-85a7-25433230a485` | `07_하늘을 밀어_target176-preview.wav` | `7eb6a9d34a0d2606e97ce9f2f7cfb995a40dd502d2c79eb7a3633da41b3032ac` | 보정 ×0.976746767 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 08 | 유리 번개 | `45acc3bc-6c0a-4472-b87f-9c36adba05bf` | `08_유리 번개_target176-preview.wav` | `505e27292043163fa7cf6e5fa4bf639a29f63c9d508ca120119c97fcbe560922` | 보정 ×0.999772779 | 전달 당시 활성 후보 | 기존본 청취 통과·ID 선택; 175 비교 이력·새 173 목표본 청취 대기 |
| 09 | 한계 위로 | `aadf83c5-cd5f-47d0-9819-0d3cbb86efd0` | `09_한계 위로_target176-preview.wav` | `bb90fd36b5cf51367f46b4efdf9ea056981d3fb7f4432e913c40f911cd7b4cac` | 보정 ×0.975907289 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 10 | 전류의 발끝 | `8392855c-26db-400e-9553-e32df268d2c0` | `10_전류의 발끝_target176-preview.wav` | `99c5a9d1d1399d629227c3ff041b240c6cfc8d88102cdf63eb2f7aa471ec769a` | 보정 ×0.995700385 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 11 | 계속 앞으로 | `4aebcc2f-5d02-4761-9dc0-23cef9479acf` | `11_계속 앞으로_target176-preview.wav` | `aa1639a00e2e852a45f53faa7260fb3e4c56c6d511120d20225894d0b55f1335` | 보정 ×0.990767845 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 12 | 폭발 직전 | `704d6663-6a2f-4a17-ba75-9a87bf768e7a` | `12_폭발 직전_이전후보_target176-preview.wav` | `2b4874869d17e8f10ba42b2b5044a9763cc87c595145daaa8abc477a794ec116` | 보정 ×0.950216228 | 로컬 과거 후보·이번 작업에서 복구 없음 | 전달본 청취 통과·ID 선택 |
| 13 | 황금 주파수 | `b51b42b3-2537-483a-b3ab-a65c4274fe6a` | `13_황금 주파수_target176-preview.wav` | `569572719ac81ba4bcd86ab50244002893a948135c9ac1963cd5ea8c22653fab` | 보정 ×0.992751784 | 전달 당시 활성 후보 | 기존본 청취 통과·ID 선택; 175 비교 이력·새 173 목표본 청취 대기 |
| 14 | 높은 기어 | `f8df1271-a60c-465b-900f-a8863c86f8dc` | `14_높은 기어_이전후보_target176-preview.wav` | `abf57c1ace3f3afde8de73d3ac40f5bddf2df60c59ad02937a5675ca018280f2` | 보정 ×0.963072200 | 로컬 과거 후보·이번 작업에서 복구 없음 | 전달본 청취 통과·ID 선택 |
| 15 | 번쩍이는 궤도 | `b9c055a2-3726-4073-a103-801dcfafd1bf` | `15_번쩍이는 궤도_target176-preview.wav` | `bb32054470bfbf297226333dda5784657970a9b7920935b701a985cd4cb06cd4` | 보정 ×0.975690883 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 16 | 가속의 틈 | `7c3bc62b-2599-4bf1-aecc-212fff88d556` | `16_가속의 틈_target176-preview.wav` | `4abe33702ba3c413c8da89867dbdb1034d41dbb7cd7c04f9a2cd85ee856e2a0a` | 보정 ×0.944991812 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 17 | 몸이 먼저 | `fe8164a4-9a09-4bc0-8414-0f1ad368605b` | `17_몸이 먼저_target176-preview.wav` | `4a02f4c196fc6f3edb57f4017fc07495e34e21f2e093fceaf6ef014c97fcd4c0` | 보정 ×0.966608084 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 18 | 빛을 따라 | `af2385fb-8638-4392-a9a0-7a031e31853e` | `18_빛을 따라_이전후보_target176-preview.wav` | `279adc1e3e1c2fc6f05d3961df462b70c7978906cc910043f22eb88cce50c9da` | 보정 ×1.008318629 | 로컬 과거 후보·이번 작업에서 복구 없음 | 기존본 청취 통과·ID 선택; 새 173 목표본 청취 대기 |
| 19 | 끝까지 당겨 | `08faf4f4-f3fa-404d-97a6-f0515f9ceed3` | `19_끝까지 당겨_target176-preview.wav` | `8a694d9d45930b4c7883e2532fee42ee0b4cbab7544de066e0b214292f68204a` | 보정 ×0.991465510 | 전달 당시 활성 후보 | 전달본 청취 통과·ID 선택 |
| 20 | 다시 점화 | `5f0f2be1-7ec8-4f36-aa18-8af4b43199c7` | `20_다시 점화_원본속도_박자확인용.wav` | `c00140e88c60a56ebbd37ff2e61fe569fc0d6b5488da70dc85c66a2f15b1ce77` | 원본 속도 ×1.0 | 현재 Suno 검색 한 행·전달 ID 불일치 | 옛 전달본 청취 통과; 현재 다른 ID 선택·전곡 녹음 보존 |

20번 현재 선택 ID와 전곡 작업용 파일은 위 [20번 출처 기록](selected-recordings/2026-10-23/20-capture-provenance.json)에 있다. 표의 20번 ID는 **과거 전달본 출처**다.
