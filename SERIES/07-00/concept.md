# 07:00 — 아침 러닝 (제작 브리프)

Version: 0.4 재제작 공개·업로드 후 정리 완료 · 2026-10-24

## Current Rebuild — 2026-10-24

- 젠은 이전 YouTube 영상을 삭제했다고 알렸고, 기존 선택 20곡을 다시 제작해 업로드하도록 요청했다. 새 정적 이미지 4K 영상 제작·기술 검사와 source-final·render-final·upload-ready·verify-release 검사를 마쳤다. 독립 최종 검토 CLEAN 이후 Wavvy24에 한 번 업로드하고 즉시 공개했다. 새 영상은 https://youtu.be/7iVqqukk5WA 이며 기존 댓글도 원문 그대로 게시·고정했다. 4K 처리 완료와 공개 페이지의 짧은 재생을 확인했다. 저작권 검토는 아래 마지막 관측 시점에 아직 진행 중이다.
- 확정된 번호순과 후보 ID는 `input/suno-final-selection-2026-10-12.json`을 유지한다. 음악을 새로 생성하거나 선택곡을 바꾸는 요청은 아니다.
- 이번에는 각 곡을 실제로 측정하고 음높이를 유지하며 180 BPM으로 늘리거나 줄인다. 곡이 바뀌는 전환부도 박자가 이어지도록 연결한다. 2026-10-12의 ‘템포 차이만으로 보정하지 않는다’는 결정은 이번 재제작에 적용하지 않는다.
- 20곡을 번호순으로 2회 구성한다. 20→1을 포함해 39개 전환과 40개 실제 시작 시각을 새로 기록한다. 이전 영상의 0.8초 전환과 챕터 시각은 새 제작 기준이 아니다.
- 착수 시점에는 이전 정리로 로컬 음원·영상이 없었다. 같은 선택 ID의 원본 WAV 20곡을 다시 확보했다. 새 다운로드와 과거 원본의 해시는 다르므로 출처 원장에 각각 기록했다. 현재 20곡의 180 BPM 보정과 독립 박자 분석, 2회 연결 음원 제작 및 저장 파일의 기술 검사를 마쳤다. 독립 최종 오디오 검토는 CLEAN이다. 젠은 현재 음원으로 영상 제작·업로드하고 바로 공개하도록 지시했다. 별도의 전곡 청취 승인이 있었다고 기록하지 않는다. 아래 2026-10-12 기록은 당시 이력이다.
- 새 장면은 한국 도심 빌딩을 배경으로 위에서 본 세 러너이며 젠이 선택했다. 젠이 직접 만든 `input/thumb.jpg`와 `input/thumb.psd`를 최종본으로 받았다. 새 영상의 정적 이미지 입력은 `input/thumb.jpg`이다. 시간 숫자는 넣지 않으며 색·글자·배치를 다시 편집하지 않는다. 새 업로드 제목은 젠의 “기존 제목 그대로 (추천)” 확인에 따라 이전 확정 제목을 그대로 쓴다.
- 완료된 실행 계획과 중간 검사는 업로드 후 정리했다. 최종 제작·게시·정리 결과만 보존한다.

## Current Audio — 2026-10-24

- 기존 선택 20곡의 ID·번호순은 동일하다. 제작 때 원본은 `input/tracks/`, 음높이를 유지한 180 BPM 보정본은 `input/processed-180/`을 사용했다. 업로드 후 두 음원 폴더의 WAV를 삭제했으며 ID·해시·보정 기록은 보존한다.
- 보정 방식은 FFmpeg `atempo`이다. 곡 안의 구간별 속도를 조정했으며 음높이 변경이나 악기 추가는 하지 않았다. 원본은 덮어쓰지 않았다.
- 게시에 사용한 2회 연결 음원(로컬 파일 삭제): `output/continuous-180-20261024/continuous-mix-0700-repeat2.m4a`, 48 kHz·stereo AAC, 6,722.858833초(약 1:52:03), SHA-256 `69304f102a2455446252661fb1696afad94579ebcfab2cde8b559038b53a5afe`.
- 제작·검사 기록: `production/continuous-180-20261024/manifest.json`. 실제 40개 재생 구간·39개 전환이며 20→1도 연결했다. 전환은 16박(5⅓초)씩 겹친다. 2시간 WAV 중간 사본은 쓰지 않았다.
- 전환 20종의 관측 타격음 차이는 각 연결의 90백분위가 최대 19.867 ms이다. 다른 박자 분석 모델의 마디 시작점도 대조했다. 이는 측정 오차를 포함한 추정치이며 모든 연주 타격이 기계적으로 정확히 180 BPM이라는 인증은 아니다.
- 저장 AAC의 39개 전환과 첫 회차 본문 20곳을 원본 재구성 파형과 대조했다. 59곳의 최대 시간 차이는 0샘플, 최소 파형 상관은 0.96926이었다. 최종 음량은 -15.95 LUFS, true peak -3.04 dBTP이며 클리핑은 관측되지 않았다. 원곡의 간주·조용한 본문을 무음이라는 이유로 제거하지 않았다.
- 전환별 16초 청취 WAV 20개와 모든 미리보기는 삭제했다. 20→1을 포함한 실제 연결 시각·측정 결과는 최종 제작 기록에 남겼다.
- 실제 40개 시작 시각은 `production/continuous-180-20261024/tracklist.txt`에 기록했다. 곡이 처음 들리는 순간의 인증이 아니라 다음 곡의 페이드가 시작되는 위치다.
- 독립 Astra/high 최종 오디오 검토는 CLEAN(확정 Critical/High 0·원칙 관찰 없음)이다. [검토 범위와 독립 측정](../../.ai/reviews/2026-10-24-0700-continuous-audio-review.md)을 따른다. 기술 검사 통과는 젠의 청취 승인이 아니다. 젠은 “영상 제작하고 업로드하자. 본문이나 댓글은 그대로고 바로 공개”를 지시했고, 제목은 “기존 제목 그대로 (추천)”로 확인했다. 별도의 전곡 청취 승인을 주장하지 않으며 새 영상 제작·검증과 실제 업로드를 구분한다.
- 이전 `Final Selected Audio Sources` 및 `output/report.json`의 해시·시각은 2026-10-12 개별 음원 제작 이력이다. 새 완성 믹스의 출처·시각은 위 제작 기록을 따른다. 새 믹스의 현행 발매 계약은 아래 `Final Premixed Audio`와 `production/final-premixed-audio.json`이다. `pack`으로 반복·합성을 추가하지 않는다.

## Final Artwork — 2026-10-24

- 최종 생성 프롬프트: `input/thumbnail-prompt.txt`. 최종 장면의 생성·배경 수정 지시를 모은 재현용 설명이며 동일 픽셀을 보장하는 기록은 아니다.
- 글자 없는 원본: `input/thumbnail-source.png`, 1672×941, SHA-256 `6bfe986cce7ff3ed9c17c60c816e51873d00e89b3cfd2c6adeaf11bb7d2111fe`.
- 젠의 편집 원본: `input/thumb.psd`, 2532×1424, SHA-256 `533a338c6dc1f68f76bbad31b377f37a5287435540e92ecab0f4562a03ae5439`.
- 최종 썸네일 겸 새 영상의 정적 이미지: `input/thumb.jpg`, 2532×1424, SHA-256 `93b63f208ff89c81c705ef64b53fd299911a55d7f65d8a3386bd65fa8feb4944`.
- 새 영상은 최종 JPG를 3840×2160으로 확대만 한다. 원본 사진이 4K로 생성됐다고 주장하지 않는다. 30초 미리보기와 전체 영상의 화면·기술 검사를 통과했다. 전체 영상의 길이는 6,723.000초이며 AAC는 6,722.859초 그대로다. 마지막 정적 화면의 반올림은 0.141초다.
- 옛 `input/loop.png`를 새 영상 입력으로 사용하지 않는다. 완성된 2회 믹스와 최종 JPG를 직접 연결하는 정적 이미지 제작 방식을 사용한다. 일반 `pack` 반복을 다시 적용하지 않는다.

## Upload Status

- YouTube upload: completed
- 새 공개 영상: Wavvy24, https://youtu.be/7iVqqukk5WA, 2026-10-24. 정상 UI 파일 제출은 한 번이다. 비공개 저장 뒤 제목·본문·태그·썸네일·아동용 아님·AI 사용 예·유료 프로모션 없음을 다시 확인하고 즉시 공개로 저장했다. 다시 연 공개 설정과 새로 불러온 Studio의 `공개`를 확인했다.
- 승인 제목은 기존 제목 그대로다. 본문의 40개 챕터 시각만 새 믹스의 실제 시작점으로 변경했으며 나머지 본문·댓글·태그는 유지했다. Studio 편집 내용과 공개 YouTube 조회의 제목·본문이 업로드 문안과 정확히 같다. 기존 템포 설명도 젠의 본문 유지 지시 범위에서 그대로 뒀다.
- 게시 파일: `output/video-user-thumbnail-20261024/final-0700-4k.mp4`, 3840×2160 H.264/AAC, 실제 1:52:03, 20곡×2회·40챕터. 파일 해시는 `Final Premixed Audio` 계약과 같다. 2026-10-24 18:25 KST에 SD·HD·4K 처리 완료를 관측했다.
- 젠의 추가 “방금 올린 거 좋아요도 하고” 지시로 새 영상에 좋아요를 눌렀고 `좋아요 취소`·1개 표시를 확인했다.
- 기존 댓글 원문을 한 번 게시했고 정확히 같은 댓글 한 개를 조회했다. [고정 댓글](https://www.youtube.com/watch?v=7iVqqukk5WA&lc=UgxFItNn5xsIRHIf6ZF4AaABAg)은 시청 페이지를 다시 불러온 뒤에도 `@wavvy24님이 고정함`이 표시됐다.
- 공개 시청 페이지에서 재생 위치 1.608104→4.610258초의 증가를 실측한 뒤 일시정지했다. 짧은 재생 검사이며 전체 청취나 4K 화질 재생 인증은 아니다. 가사 없는 음원이므로 자막은 제출하지 않았다.
- 저작권 상태: 2026-10-24 마지막 관측은 `검토 완료 대기 중...`이다. 공개 완료·4K 처리 완료와 저작권 최종 판정을 구분한다. 현재 요청의 영상 제작·공개·댓글 작업은 완료했으며 YouTube의 자동 검토 결과는 미확정이다.
- 원시 관측과 최종 결과: `production/youtube-upload-20261024{,-ui}.json`, 공개 문안·댓글 조회, `production/youtube-upload-staging-20261024.json`. 독립 로컬 영상·검증 코드 검토는 `.ai/reviews/2026-10-24-0700-video-release-review.md`의 CLEAN이다. 이 판정을 외부 공개 증거로 대신 사용하지 않았다.
- 업로드 직후 브라우저 제출용 사본 네 파일 679,150,371바이트를 정리했다. 이어 젠의 폴더 정리 지시로 아래 Local Retention의 영상·음원·과정 자료도 정리했다. 최종 썸네일과 제작·게시 근거는 남겼다.
- 이전 영상 `DU_vBuIdMG4`는 젠이 삭제했다고 보고했다(2026-10-24). 아래 공개 확인은 삭제 전 과거 기록이다.

## YouTube Metadata (v2.2 — 2026-10-24 기존 제목·본문·댓글 유지, 실제 챕터 시각 갱신)

Context Mode: Energizing (07:00 러닝)

### 제목
```
Playlist | 상쾌하게 달릴 준비 됐나요?! 🏃 | 180 BPM Running Mix · 2Hour | Wavvy | 07:00
```

### 설명
```
🌅 07:00, 발걸음이 먼저 나가는 아침.
리듬을 따라 하루를 달리기 시작해요 - Wavvy

문을 열자마자 서늘한 공기가 닿고,
신발 끈을 한 번 더 당겨 묶어요.
첫 박자에 맞춰 강변으로 발을 내딛고,
가로등이 꺼질 무렵 호흡이 고르게 이어져요.
어느새 걸음이 길어지고 몸이 가벼워지면,
기타와 드럼이 다음 구간으로 밀어줘요.
한 바퀴를 마치고 같은 곡을 다시 만나도,
내 페이스를 따라 계속 달릴 수 있어요.

20곡을 번호순으로 두 번 이어 듣는 러닝 플레이리스트예요.
180 BPM은 목표 러닝 케이던스입니다. 수록곡의 실제 음악 템포는 곡마다 달라요.
가사 없는 인스트루멘털 중심으로 구성했어요.

──────────────
Track List
🏃 00:00 - 01. 문을 열고
🏃 02:59 - 02. 파란불
🏃 06:04 - 03. 첫 바퀴
🏃 08:23 - 04. 조금 일찍
🏃 11:33 - 05. 길을 바꿔
🏃 14:17 - 06. 정해 둔 건 없어
🏃 16:13 - 07. 같은 방향
🏃 19:10 - 08. 낮은 비트
🏃 22:24 - 09. 숨을 세어
🏃 25:39 - 10. 생각을 놓고
🏃 27:56 - 11. 다시 해볼게
🏃 30:39 - 12. 바람이 바뀌어
🏃 33:10 - 13. 호흡
🏃 36:08 - 14. 하나씩
🏃 39:19 - 15. 드럼 위로
🏃 41:53 - 16. 비가 갠 뒤
🏃 44:18 - 17. 이어지는 소리
🏃 47:30 - 18. 가까운 곳
🏃 50:42 - 19. 괜찮은 날
🏃 53:48 - 20. 집으로 가는 길
──────────────
다시 한 바퀴
🏃 55:58 - 01. 문을 열고 (반복)
🏃 58:50 - 02. 파란불 (반복)
🏃 01:01:55 - 03. 첫 바퀴 (반복)
🏃 01:04:14 - 04. 조금 일찍 (반복)
🏃 01:07:24 - 05. 길을 바꿔 (반복)
🏃 01:10:08 - 06. 정해 둔 건 없어 (반복)
🏃 01:12:04 - 07. 같은 방향 (반복)
🏃 01:15:01 - 08. 낮은 비트 (반복)
🏃 01:18:15 - 09. 숨을 세어 (반복)
🏃 01:21:30 - 10. 생각을 놓고 (반복)
🏃 01:23:47 - 11. 다시 해볼게 (반복)
🏃 01:26:30 - 12. 바람이 바뀌어 (반복)
🏃 01:29:00 - 13. 호흡 (반복)
🏃 01:31:59 - 14. 하나씩 (반복)
🏃 01:35:10 - 15. 드럼 위로 (반복)
🏃 01:37:43 - 16. 비가 갠 뒤 (반복)
🏃 01:40:09 - 17. 이어지는 소리 (반복)
🏃 01:43:21 - 18. 가까운 곳 (반복)
🏃 01:46:33 - 19. 괜찮은 날 (반복)
🏃 01:49:39 - 20. 집으로 가는 길 (반복)
──────────────
Music for your space, 24 hours a day.

🎵 Music: Wavvy
Copyright Ⓒ Wavvy. All rights reserved.
──────────────
#runningmusic #instrumental #indierock #breakbeat
#러닝음악 #아침러닝 #러닝플리 #케이던스180
#playlist #플리 #wavvy #웨이비
```

### 태그 (업로드 시)
```
running music, 180 cadence, running playlist, instrumental, indie rock, breakbeat, jazzy jungle, guitar rock, 아침러닝, 러닝음악, 러닝플리, 케이던스180, 운동음악, playlist, 플리, wavvy, 웨이비
```

### 고정 댓글
```
아침 7시, 첫 발을 내딛을 때의 공기를 담았어요. 🏃
20곡을 두 번 이어 들으며 자기 페이스로 달려보세요.
어떤 곡에서 발걸음이 가장 가벼워지나요?
```

## Packaging Contract

- Playlist repeat: 2
- Video image and thumbnail: `input/thumb.jpg` (젠 제작 최종본; Final Artwork의 해시 적용)
- Legacy `input/loop.png` and thumbnail-layout are replaced; do not use them for this remake.

## Final Premixed Audio

- Manifest: `production/final-premixed-audio.json`
- **Final vocal direction**: Instrumental.
- 게시 때 사용한 입력은 20곡×2회의 완성 AAC 한 개다. 추가 반복·재합성 없이 한 번 복사했고, 공개 완료 뒤 로컬 AAC·MP4·원본/보정 WAV·CSV를 삭제했다. 경로·해시와 최종 제작·검증 기록은 아래 계약에 남는다.
- 원본 재확보 기록은 `production/reacquisition-20261024.json`, 선택 ID는 `input/suno-final-selection-2026-10-12.json`, 원본→180 BPM 보정→2회 믹스 연결은 `production/continuous-180-20261024/manifest.json`을 따른다. 새 원본·보정본·과거 원본의 해시는 서로 다른 역할이며 동일하다고 주장하지 않는다.
- PCM 제작 길이는 6,722.858833초, 저장 AAC의 재생 길이는 6,722.859000초다. 차이 0.167 ms는 저장 형식의 시간 반올림이다. MP4는 AAC의 전체 압축 데이터와 시간 위치를 보존한다.
- 실제 40개 시작점은 다음 곡의 페이드 시작이다. MP4 내부 챕터는 밀리초, YouTube 문안은 가장 가까운 초로 표기한다. `2Hour`는 젠이 승인한 기존 제목 표기이며 실제 길이는 약 1:52:03이다.
- 최종 JPG: `input/thumb.jpg`. 영상 경로: `output/video-user-thumbnail-20261024/final-0700-4k.mp4`. 제작·기술 검사 원시는 `production/video-user-thumbnail-20261024.json` 및 검증 기록을 따른다.
- 원문 생성 프롬프트의 현행 연결 상태는 `unverified`다. 과거 보컬 txt를 현재 무가사 음원의 원문으로 승격하지 않는다. 아래 개별 WAV 출처 선언은 과거 기록이며 현행 발매 계약이 아니다.
- 업로드 문안 보존 대조: `production/upload-metadata-preservation-20261024.json`. 본문 40개 챕터의 시각만 바꾸고 다른 본문·댓글·태그는 정확히 유지한다.

## Previous Selected Audio Sources — 2026-10-12 과거 기록

확정된 20개 무가사 음원의 번호·Suno 후보 ID·WAV SHA-256·실제 첫 재생 시작 시각은 `input/final-selected-audio-sources.json`에 기록한다. 원문 프롬프트가 생성 기록의 후보 ID 및 해시와 직접 연결된 곡만 `confirmed`로 표기한다. 연결을 확인하지 못한 곡은 `unverified`로 두고, Suno 화면에서 관측한 스타일 설명이 있으면 원문 프롬프트와 구별해 보존한다. 처음 만든 보컬 txt는 이력이며 최종 무가사 음원의 가사나 출처가 아니다. 이 시리즈에는 노랫말 자막을 만들지 않는다.

## Series direction

- **Time and use:** 07:00, 젠이 실제로 운동하는 시간. 20곡을 이어 들으며 달리는 아침 플레이리스트. 본편은 선택한 20곡을 번호순으로 2회 반복해 총 40개 재생 구간으로 구성한다(젠 2026-10-12 확인). 2026-10-24 재제작에서는 곡별 180 BPM 보정과 박자 연결을 적용하며 길이와 시작 시각은 새로 확정한다. 이전 영상의 0.8초 전환·약 1시간 56분은 과거 기록이다.
- **Music (current source direction):** 보존 7곡, 1차에서 남긴 8곡, 2차 11B, 젠이 직접 다시 만든 06·09·10, 현재 작업공간의 12를 선택했다. 1차의 4 jungle / 4 drill / 5 rock과 2차 06·09·10의 장르는 생성 당시 이력이다. 젠의 직접 재제작 06은 기존 20과 같은 화면 스타일 설명의 기타 록, 09는 기존 17과 같은 기타 중심 재지 정글, 10은 보존 04와 같은 피아노 중심 인디 브레이크비트다. 세 곡의 채택은 확정됐지만 STYLE 입력 원문은 확인하지 않았다. 16은 젠이 남긴 선택이며 이번 재생성 대상이 아니다.
- **Pulse and acceptance (2026-10-12 historical decision; 재제작에는 위 Current Rebuild 적용):** 교체곡 STYLE에는 180 BPM 지속과 명확한 4분음표 러닝 박자를 지시했지만, 이는 제작 당시 목표였고 실제 음원의 수치 증거는 아니다. 젠은 확정한 20곡을 유지하기로 결정했다. 젠이 이 곡들로 20~30분 달렸을 때 평균 케이던스가 대략 180이었다는 사용 경험을 근거로 썸네일의 `180 BPM`을 목표 러닝 케이던스로 쓴다. 일부 곡의 탐색 측정치는 약 174~192 BPM이어서 전곡이 실제로 정확히 180 BPM이라고 주장하지 않는다. 템포 차이만으로 이미 확정한 곡을 다시 만들거나 보정하지 않는다. 음악적 결함이나 편집 결함의 QC는 별도로 한다.
- **Final vocal direction (2026-10-03 listening correction):** Instrumental. 젠 heard the initial vocal versions and chose to remove lyrics for the running playlist. The 20 lyric-bearing txt files and 40 initial candidate IDs remain as generation history; they are not final instrumental sources. 젠의 “2 완료” 신호 후 **03·05·07·08·11·12·15·16·18·20**의 생존 원본 ID를 확인하고 각각 Suno `... → Remix → Cover`에서 가사 칸을 `[Instrumental]` 한 줄로 바꿔 요청했다. 01은 이 Cover 요청에 포함되지 않았다. 젠은 이 10곡의 Cover 결과를 청취 PASS했으며, 기계적 무가사 분석은 하지 않았다.
- **Duration target:** about three minutes or longer per song. 현재 보존된 03은 2:24 표시/약 2:23.72 WAV로 이 목표보다 짧지만 젠이 남기기로 정했다. 2026-10-03 선택됐던 옛 01의 표시 길이 2:41은 역사 기록이고, 새 01 후보 두 개는 UI에 각각 2:59로 표시된다. 1차 후보 26개의 UI 표시 길이는 `input/redirection-review-2026-10-06.md`, 2차 후보 8개는 `input/redirection-round2-review-2026-10-06.md`에 기록했다. 2차 11A는 3:00 입력에도 2:59로 표시됐고, 현재 남은 11B는 3:00이다. 젠의 직접 재제작 06·09·10은 각각 화면상 2:04·3:22·2:25다. 길이 목표는 전곡 통과로 판정하지 않는다.
- **03 stronger remake:** After the 20-song cleanup, 젠 requested a more powerful 03 only. Its second A/B was judged “느려.” The third prompt added a continuous motorik drum pulse. 젠은 A (`fad9fc49-9b35-4f10-aa76-f62ddd9cf10c`, 화면 2:24)를 남기고 B를 삭제했다. The earlier 03 Cover and second remake remain historical.
- **Arc proposal (earlier 2nd-round direction):** 01 록으로 출발하고 02–04 보존곡을 지난다. 05–12에 06 개러지 록·09 재지 정글·10 어쿠스틱 재즈·11 펑크(funk) 록을 끼운 구상은 2차 생성 당시 안이다. 젠이 06·09·10을 새로 만든 뒤의 최종 흐름은 세 새 후보를 듣고 정한다. 13–14 보존곡을 중심점으로, 15–16은 더 강하게, 17은 밀도만 덜어낸다. 18–19 보존곡 뒤 20은 박자를 늦추지 않는 록으로 닫는다. 번호별 과거 근거는 `input/redirection-2026-10-06.md`에 있다.
- **2026-10-03 remake history:** 당시 02의 두 차례 기타/일렉트로클래시 방향, 04 피아노 브레이크비트, 06 신스펑크, 09 드럼 앤 베이스, 10 일렉트로클래시, 13 jazzy jungle, 14 베이스 브레이크비트, 17 일렉트로닉 포스트록, 19 기타 브레이크비트를 사용했다. 이 중 지금 보존된 13의 실제 소스에는 신스 베이스와 키보드 선율이 있다. 보존곡 원문은 바꾸지 않고 새 jungle은 재즈 화성과 쪼개진 드럼만 선례로 쓴다.

## Precedent and explicit overrides

- `wavvy.md` labels 07:00 “기상 / 시작, 담담.” This series explicitly raises the tempo and energy for morning running because 젠 chose 180 BPM indie electronic for their exercise hour. The current instrumental direction overrides Wavvy's default of Korean lyrics and a lead vocal for this series.
- `SERIES/06-00/concept.md` is instrumental-first fast lo-fi at roughly 110–130 BPM; this series targets a much faster indie electronic pulse and is now also intended to be instrumental.
- `SERIES/20-00/concept.md` is hard after-hours workout hip-hop. This series keeps a morning running purpose and uninterrupted step pulse even as its proposed drill and rock sources grow stronger.
- The instrumental decision applies to every final track. Initial vocal directions in the submitted txt files are historical and do not authorize vocals in the covers.

## Reference videos

- [Paw&Power — 180 BPM Running Music Mix 1Hour Metronome Synced 042026](https://youtu.be/A3psJJwkdSY): use the idea of a sustained, step-aligned 180 BPM pulse.
- [달리런 — Playlist 180BPM 러닝 플리](https://youtu.be/u2eyM-tS6QI): use the idea of a 20-track, continuously motivating running set, with firm bass and some broad hooks. Its YouTube description emphasizes a club setting; 젠 chose a brighter morning sound with medium-strength moments for this series.
- These directions come from the videos' published metadata and descriptions, checked 2026-10-03. 2026-10-03 당시 수치 BPM 분석은 없었다. 2026-10-12 탐색 측정과 젠의 실제 러닝 경험 및 현행 채택 결정은 위의 현재 기준에 기록했다. Do not copy melody, distinctive arrangement, or lyrics from either reference.


## Local Retention — 2026-10-24

젠의 “이제 폴더 파일 정리해 뭐해야하는지 기억해?” 지시로 정확한 목록 198개·3,864,544,687바이트를 삭제했다. 원본/보정 WAV 40개, 완성 AAC·MP4·미리보기·과정 문서, 일치하는 Downloads 사본 20개와 브라우저 검사 사본을 포함한다. 삭제 198개 모두 부재와 보존 164개 모두 내용 불변을 확인했다. 최종 artwork 네 파일과 가사·스타일 원문, 선택 ID·해시·보정/박자/믹스 설정·40개 시각·최종 렌더 검증·게시 근거는 남겼다. 실제 여유 공간 관측 증가량은 3,188,232,192바이트이며 삭제한 논리 파일 크기와 구분한다. 정리 결과는 `.ai/cleanup/2026-10-24-0700-post-upload-cleanup.json`, 동결 목록은 같은 접두사의 `inventory.json`이다. 재제작하려면 같은 Suno 선택 ID의 음원을 다시 확보하고 보존한 최종 제작 설정을 적용해야 한다.
