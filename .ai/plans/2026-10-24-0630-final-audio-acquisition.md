# 06:30 — 선택 음원 20곡 최종 WAV 입력 확보

## 현재 실물 확보 결과 — 2026-10-24

선택 ID 20개의 최종 WAV 20개를 `input/tracks/`에 배치하고 실제 사본 SHA-256(파일 동일성 확인값)·길이·출처를 [최종 목록](../../SERIES/06-30/input/download-manifest.json)에 연결했다. 합계 4134.925187초다.

8·13·18번은 173 BPM 처리 목표, 나머지 보정 대상 15곡은 176 목표이며 5·20번은 원속도 바이트를 보존했다. 전곡 실측 BPM은 미확인이라 파일명은 NA, 목록의 bpm_measured는 null이다.

청취 사본 20개와 자동 재생 없는 index.html을 `/Users/zenkim_office/Downloads/wavvy-0630-final-audio-20261024`에 만들었다. 원본·원시 캡처·실패 파일·기존 Downloads 자료는 보존했다.

12번은 중간 끊김이 있는 첫 원본을 제외하고 정상 r2만 사용했다. 14번은 선택 ID 하나만 라이브러리로 복원했고, 네 번째 시도는 컨트롤러가 반복 실패 규칙으로 중단했다. 젠의 추가 한 번 승인 뒤 성공한 r5만 사용했다. 과거 휴지통 이력과 실패 네 회는 보존했다.

2번은 원본 약 193초 이후 fade(소리가 점점 작아지는 끝부분)의 단독 정밀 BPM을 인증하지 않는다. 6·9·11·17·19번은 출력 전에 선택한 mid(중음역) 측정 근거를 썼다. 9·17번 원본 약 206초 이후와 19번 약 190초 이후 fade도 같은 한계가 있다. 17·19번의 마지막 30초 평균과 마지막 단독 박자 해석 차이는 곡별 measurement_limit에 보존했다. 13번의 UI(화면 조작 상태) pause 확인 경합과 대신 보존한 원시 경계·수동 정지 근거는 목록의 acquisition_note에 유지했다.

20곡의 전체 직접 파일 검사와 18개 처리곡의 앞·중간·끝 30초 측정 54개를 재현했다. 내부 20ms 이상 완전 무음·클리핑·기술 오류는 0건이다. 독립 Astra high 검토는 CLEAN(확인된 Critical/High 0·원칙 관찰 없음)이며 공식 state writer로 revision84 track_source_draft와 실제 입력 음원20개를 기록했다. 이번 음원 확보 범위의 남은 작업은 없다. 새 전곡 청취 승인, 모든 순간의 BPM 인증, source_final 또는 발매 완료를 선언하지 않는다.

초기 체크포인트와 00:35 staging 표는 아래에 과거 이력으로 보존한다. 현행 채택은 최종 목록과 동결한 처리 목록의 20행을 따른다.

## 승인과 범위

- 젠 원문: “모두 통과. 음원 최종 확보해.” 이번 응답은 직전 전달된 8·13·18번 173 BPM 목표 30초 비교본 세 파일의 정확한 SHA-256과 5·20번 원속도 전곡 앱 출력 작업본 두 파일의 청취 통과다.
- 8·13·18번은 이 시리즈의 전곡 처리 목표를 173 BPM으로 채택한다. 나머지 보정 대상 15곡은 승인된 176 BPM 목표를 따른다. 5·20번은 승인된 원속도를 보존하며 실제 BPM은 미확인이다. 173 예외는 전역 정책 변경이 아니다.
- 선택 후보 ID 20개는 input/suno-candidates.json의 곡별 decision.chosen_candidate_id를 따른다. 20번 현행 ID와 예전 30초 전달 ID는 다르며 예전 SHA를 새 후보 승인으로 바꾸지 않는다. 초기에는 12·14·18번의 로컬 과거 자료 수집을 계획했다. 실제 실행에서 14번 선택 ID 하나가 휴지통 상태임을 확인해 라이브러리로 복원했고, 젠의 추가 한 번 승인 뒤 r5 전곡을 확보했다. 초기의 원격 복구 미전제는 현재 14번 상태를 뜻하지 않는다.
- 전곡 음원 확보와 입력 WAV 검증까지가 이번 범위다. 영상, 썸네일, pack, report, source_final 선언은 별도 단계다. 전곡 BPM 기술 인증은 실제 전곡 측정 전까지 선언하지 않는다.

## 목표·출처 대조표

| 순서 | 제목 | 선택 ID | 전곡 처리 목표 | 원속도 전곡 출처 상태 | 권장 최종 입력명 |
|---:|---|---|---|---|---|
| 01 | 첫 박부터 | 24703f3f-c7ce-433f-a892-16d9330b41a9 | 176 BPM 목표 | 원속도 전곡 확보 | 01__첫 박부터__Driven__Hardcore Punk Rock__NA.wav |
| 02 | 가속선 | 67d6a052-21ef-4c59-be09-790468e75152 | 176 BPM 목표 | 원속도 전곡 확보 | 02__가속선__Driven__Post Hardcore Rock__NA.wav |
| 03 | 빛나는 노면 | 872b0aac-6e44-4d54-b8e0-c546359be0fe | 176 BPM 목표 | 원속도 전곡 확보 | 03__빛나는 노면__Driven__Electronic Breakbeat__NA.wav |
| 04 | 전력 곡선 | 5ac0c138-5643-43ee-a2e4-07b02a794cbb | 176 BPM 목표 | 원속도 전곡 확보 | 04__전력 곡선__Driven__Hard Rock__NA.wav |
| 05 | 빛의 마찰 | b868f3f7-a1fb-4cc7-aa18-e6202df90dcd | 원속도 유지 · BPM 미확인 | 원속도 전곡 확보 | 05__빛의 마찰__Driven__Electronic Breakbeat__NA.wav |
| 06 | 다리의 불꽃 | e2196f98-b0f6-432b-b8a2-a900af30a793 | 176 BPM 목표 | 원속도 전곡 확보 | 06__다리의 불꽃__Driven__Hardcore Punk Rock__NA.wav |
| 07 | 하늘을 밀어 | b1e7fe46-ab35-46fd-85a7-25433230a485 | 176 BPM 목표 | 원속도 전곡 확보 | 07__하늘을 밀어__Driven__Alternative Hard Rock__NA.wav |
| 08 | 유리 번개 | 45acc3bc-6c0a-4472-b87f-9c36adba05bf | 173 BPM 목표 | 원속도 전곡 확보 | 08__유리 번개__Driven__Electronic Breakbeat__NA.wav |
| 09 | 한계 위로 | aadf83c5-cd5f-47d0-9819-0d3cbb86efd0 | 176 BPM 목표 | 원속도 전곡 확보 | 09__한계 위로__Driven__Post Hardcore Rock__NA.wav |
| 10 | 전류의 발끝 | 8392855c-26db-400e-9553-e32df268d2c0 | 176 BPM 목표 | 원속도 전곡 확보 | 10__전류의 발끝__Driven__Electronic Breakbeat__NA.wav |
| 11 | 계속 앞으로 | 4aebcc2f-5d02-4761-9dc0-23cef9479acf | 176 BPM 목표 | 원속도 전곡 확보 | 11__계속 앞으로__Driven__Hardcore Punk Rock__NA.wav |
| 12 | 폭발 직전 | 704d6663-6a2f-4a17-ba75-9a87bf768e7a | 176 BPM 목표 | 정상 r2 전곡 확보 | 12__폭발 직전__Driven__Post Hardcore Rock__NA.wav |
| 13 | 황금 주파수 | b51b42b3-2537-483a-b3ab-a65c4274fe6a | 173 BPM 목표 | 원속도 전곡 확보 | 13__황금 주파수__Driven__Electronic Breakbeat__NA.wav |
| 14 | 높은 기어 | f8df1271-a60c-465b-900f-a8863c86f8dc | 176 BPM 목표 | 선택 ID 복원·승인 r5 전곡 확보 | 14__높은 기어__Driven__Hard Rock__NA.wav |
| 15 | 번쩍이는 궤도 | b9c055a2-3726-4073-a103-801dcfafd1bf | 176 BPM 목표 | 원속도 전곡 확보 | 15__번쩍이는 궤도__Driven__Electronic Breakbeat__NA.wav |
| 16 | 가속의 틈 | 7c3bc62b-2599-4bf1-aecc-212fff88d556 | 176 BPM 목표 | 원속도 전곡 확보 | 16__가속의 틈__Driven__Hardcore Punk Rock__NA.wav |
| 17 | 몸이 먼저 | fe8164a4-9a09-4bc0-8414-0f1ad368605b | 176 BPM 목표 | 원속도 전곡 확보 | 17__몸이 먼저__Driven__Post Hardcore Rock__NA.wav |
| 18 | 빛을 따라 | af2385fb-8638-4392-a9a0-7a031e31853e | 173 BPM 목표 | 원속도 전곡 확보 | 18__빛을 따라__Driven__Electronic Breakbeat__NA.wav |
| 19 | 끝까지 당겨 | 08faf4f4-f3fa-404d-97a6-f0515f9ceed3 | 176 BPM 목표 | 원속도 전곡 확보 | 19__끝까지 당겨__Driven__Hardcore Punk Rock__NA.wav |
| 20 | 다시 점화 | 6a6baa59-8576-4538-a157-b2410ce326d0 | 원속도 유지 · BPM 미확인 | 원속도 전곡 확보 | 20__다시 점화__Driven__Electronic Breakbeat__NA.wav |

## 수집·처리·검증 순서

1. 선택 ID와 실제 재생 후보를 일치시켜 원속도 전곡 WAV를 확보한다. 기존 1·5·20번 전곡 작업본은 해시 대조 후 재사용한다. 12·18번은 선택 ID의 원본 출처를 확인하고, 14번은 실제 복원과 젠 추가 한 번 승인으로 성공한 r5를 사용한다. 원격 새 생성·삭제는 수행하지 않았다.
2. 원속도 수집본의 해시, PCM 형식, 채널, 샘플레이트, 길이, 유효 신호와 구간 경계를 기록한다. 원시 수집본을 덮어쓰지 않는다. 1번의 과거 실패한 구간별 시험본은 최종 입력으로 재사용하지 않는다.
3. 15곡은 176 목표, 8·13·18번은 173 목표로 원본에서 음높이 유지 변환한다. 5·20번은 변환하지 않는다. 전체곡 처리의 실패 원인을 1번 시험 결과와 대조하고 작은 실제 시험 후 확장한다.
4. 최종 WAV와 수집본을 각각 해시로 연결한다. 변환 근거에는 입력 SHA, 선택 ID, 목표, 배수 또는 구간별 처리, 명령, 출력 SHA, 독립 측정 범위와 제한을 둔다. 측정하지 않은 전곡 BPM은 통과로 기록하지 않는다.
5. 20곡 실제 최종 WAV가 모두 존재하고 포맷·길이·신호·해시가 검증된 뒤에만 input/tracks/와 input/download-manifest.json을 채운다. 작업 중에는 없는 파일을 manifest에 기입하지 않는다.

## 입력 파일·manifest 계약

- MASTER/WORKFLOWS.md와 skills/wavvy-audio-ingest/SKILL.md를 따른다. 파일명은 NN__제목__Driven__곡별 장르군__NA.wav다. NA는 BPM 미확인이라는 뜻이다. 173·176은 처리 목표이지 파일명에 쓸 전곡 실측 BPM이 아니다.
- 선례 SERIES/17-30/input/download-manifest.json: 최상위 workspace는 원장의 정확한 문자열 [06:30]. tracks 20행마다 order, approved_title, input_filename, duration_seconds, sha256(입력 WAV 실물), candidate_id, source_kind, download_actor 또는 capture_actor, format, codec, sample_rate_hz, channels, bits_per_sample, bpm_measured:null을 둔다.
- 앱 녹음에는 collected_source_path/sha256와 원시 캡처 근거를 별도로 둔다. 변환본에는 tempo_processing_provenance_path/sha256, processing_target_bpm, input WAV와 원본의 서로 다른 해시를 둔다. 5·20번에는 original_speed_preserved:true를 둔다. 결론은 실물 검증 후 기록한다.
- 이번에는 pack/report가 없으므로 source-final 및 verify-release의 최종 결합 판정은 주장하지 않는다. 공식 .ai/state.json은 state writer 외 수동 수정하지 않는다.

## 착수 시점 체크포인트 — 과거 이력

- 2026-10-24 착수: 선택 ID 20개, 승인된 173 비교본 3개, 승인된 원속도 전곡 작업본 5·20번 2개. 1번 원속도 전곡 작업본도 기존에 있으나 과거 구간별 변환은 실패했다. 현재 input/tracks/ 최종 WAV 0개, download-manifest.json 없음, 공식 phase track_source_draft다.
- 원시 30초 BPM 판정과 후보 원격 처분·크레딧 이력은 바꾸지 않는다. 8·13번 175 목표 파일과 이전 176 목표 청취본은 별도 역사로 보존한다.


## 과거 중간 staging — 2026-10-24 00:35 KST

이 표는 실제 입력 디렉터리로 복사하기 전의 임시 연결이다. 1·5·18·20번의 처리 출력은 기술 패킷을 받았지만 최종 input/tracks/ WAV와 download-manifest.json은 아직 만들지 않았다. 18번 원속도 전곡은 확보해 채택 가능 원본 4/20 상태다. 12번 수집 파일은 젠이 중간 끊김 가능성을 지적해 연속성 확인·필요시 재녹음 전까지 채택 보류다. 12번의 고정 배수 처리 작업본도 목표 밖이므로 최종본으로 채택하지 않는다. 18번의 고정 배수 결과는 후반 목표 밖이므로 최종본으로 채택하지 않는다.

| 순서 | 선택 ID | 원속도 수집본 SHA-256 | 임시 처리 출력 SHA-256 | 목표 | 입력명 예약 | 출처·처리 근거 |
|---:|---|---|---|---|---|---|
| 01 | 24703f3f-c7ce-433f-a892-16d9330b41a9 | b1f9c36e5085786008d48f2385b537817f71835e4b54b3bf59e138c38733017a | 314ba0d981c8e273995fde15e819ee0d6f954350cc8b07fd2707ed59f5bde9fe | 176 목표, sparse atempo | 01__첫 박부터__Driven__Hardcore Punk Rock__NA.wav | input/tempo-adjustment/full-source/track01-round4-a-capture-provenance.json · input/audio-processing/2026-10-24/track01-sparse-full-provenance.json |
| 05 | b868f3f7-a1fb-4cc7-aa18-e6202df90dcd | 9f026ccc63df7bb4de31d73a2ec2fd4294278ee8f770f93441a5b694f80e8543 | 9f026ccc63df7bb4de31d73a2ec2fd4294278ee8f770f93441a5b694f80e8543 | 원속도 유지 | 05__빛의 마찰__Driven__Electronic Breakbeat__NA.wav | input/selected-recordings/2026-10-23/05-capture-provenance.json · input/audio-processing/2026-10-24/track05-preserved-full-provenance.json |
| 18 | af2385fb-8638-4392-a9a0-7a031e31853e | 983d7eef23b7b7de6618b96f36d964d3c9b5ac569dbed1f3e22423da2436b8a8 | 7d348f9f9fc10f4c94918591bc982c4200d4cb4d1274ccd8defe7e073395f739 | 173 목표, sparse atempo | 18__빛을 따라__Driven__Electronic Breakbeat__NA.wav | input/audio-acquisition/2026-10-24/18.json · input/audio-processing/2026-10-24/track18-sparse-target173-full-provenance.json |
| 20 | 6a6baa59-8576-4538-a157-b2410ce326d0 | 24d0e92db0e37cd0f23d6f3b04c237a95f2158ff39bb5769cec6a8288487bec7 | 24d0e92db0e37cd0f23d6f3b04c237a95f2158ff39bb5769cec6a8288487bec7 | 원속도 유지 | 20__다시 점화__Driven__Electronic Breakbeat__NA.wav | input/selected-recordings/2026-10-23/20-capture-provenance.json · input/audio-processing/2026-10-24/track20-preserved-full-provenance.json |

부모의 독립 파일 재현은 .ai/validation/2026-10-24-0630-parent-first-packets.json에 있다. 이는 01 원본/출력의 파일·PCM·8개 30초 측정과 18 원시→분리 일치를 확인한 자료이며, 음악성이나 전곡의 모든 순간 BPM 인증은 아니다.

01 처리 출력은 work/0630-final-audio-processing-20261024/01-24703f3f-sparse-target176-full.wav, 18은 같은 폴더의 18-af2385fb-sparse-target173-full.wav, 05·20은 05-b868f3f7-preserved-full.wav·20-6a6baa59-preserved-full.wav다. 모두 pcm_f32le, 48 kHz, 2채널이며 길이는 01 213.262146초, 05 200.6초, 18 201.623625초, 20 210.2초다. 01의 30초 독립 측정 8창은 175.8735–176.3095 BPM, 18의 7창은 173.174–173.352 BPM이다. 이 검사는 전곡의 모든 순간 BPM 인증이나 새 전곡 청취 승인이 아니다. 05·20은 원속도 녹음본의 복사라 원본·출력 해시가 같다.

확정 처리 provenance SHA-256: 01 6db2895c675d4e6c7ecdb497a223dd8aca9366a4a39784cd96c61eb65abeb7be, 05 5535c45a07de6184bc697d771ddb442b8e8c6689539379eaa42d7ab362a00c7c, 18 30fec5c433c96e60efba6d6af06dd15f13fb15c78560facb223bb75639ec1873, 20 82d553dacf654ee0553a7573e41ee7789af138f0a2e3c640f4737655d6115f2c. 18의 고정 배수 출력은 실패 이력이며 위 임시 처리 출력 해시와 다르다.
