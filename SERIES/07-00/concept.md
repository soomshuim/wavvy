# 07:00 — 아침 러닝 (제작 브리프)

Version: 0.2 재제작 · 2026-10-24

## Current Rebuild — 2026-10-24

- 젠은 이전 YouTube 영상을 삭제했다고 알렸고, 기존 선택 20곡을 다시 제작해 업로드하도록 요청했다. 새 영상은 아직 제작·업로드 전이다.
- 확정된 번호순과 후보 ID는 `input/suno-final-selection-2026-10-12.json`을 유지한다. 음악을 새로 생성하거나 선택곡을 바꾸는 요청은 아니다.
- 이번에는 각 곡을 실제로 측정하고 음높이를 유지하며 180 BPM으로 늘리거나 줄인다. 곡이 바뀌는 전환부도 박자가 이어지도록 연결한다. 2026-10-12의 ‘템포 차이만으로 보정하지 않는다’는 결정은 이번 재제작에 적용하지 않는다.
- 20곡을 번호순으로 2회 구성한다. 20→1을 포함해 39개 전환과 40개 실제 시작 시각을 새로 기록한다. 이전 영상의 0.8초 전환과 챕터 시각은 새 제작 기준이 아니다.
- 착수 시점에는 이전 정리로 로컬 음원·영상이 없었다. 같은 선택 ID의 원본 WAV 20곡을 다시 확보했다. 새 다운로드와 과거 원본의 해시는 다르므로 출처 원장에 각각 기록했다. 현재 20곡의 180 BPM 보정과 독립 박자 분석, 2회 연결 음원 제작 및 저장 파일의 기술 검사를 마쳤다. 독립 최종 오디오 검토는 CLEAN이며 젠의 새 음원 청취 확인과 새 영상 제작은 아직 전이다. 아래 2026-10-12 기록은 당시 이력이다.
- 새 장면은 한국 도심 빌딩을 배경으로 위에서 본 세 러너이며 젠이 선택했다. 젠이 직접 만든 `input/thumb.jpg`와 `input/thumb.psd`를 최종본으로 받았다. 새 영상의 정적 이미지 입력은 `input/thumb.jpg`이다. 시간 숫자는 넣지 않으며 색·글자·배치를 다시 편집하지 않는다. 새 업로드 제목은 아직 젠의 확인 전이다.
- 실행 계획: `.ai/plans/2026-10-24-0700-180bpm-remaster.md`.

## Current Audio — 2026-10-24

- 기존 선택 20곡의 ID·번호순은 동일하다. 새로 확보한 원본은 `input/tracks/`, 음높이를 유지한 180 BPM 보정본은 `input/processed-180/`에 각각 보관한다.
- 보정 방식은 FFmpeg `atempo`이다. 곡 안의 구간별 속도를 조정했으며 음높이 변경이나 악기 추가는 하지 않았다. 원본은 덮어쓰지 않았다.
- 현재 2회 연결 음원: `output/continuous-180-20261024/continuous-mix-0700-repeat2.m4a`, 48 kHz·stereo AAC, 6,722.858833초(약 1:52:03), SHA-256 `69304f102a2455446252661fb1696afad94579ebcfab2cde8b559038b53a5afe`.
- 제작·검사 기록: `production/continuous-180-20261024/manifest.json`. 실제 40개 재생 구간·39개 전환이며 20→1도 연결했다. 전환은 16박(5⅓초)씩 겹친다. 2시간 WAV 중간 사본은 쓰지 않았다.
- 전환 20종의 관측 타격음 차이는 각 연결의 90백분위가 최대 19.867 ms이다. 다른 박자 분석 모델의 마디 시작점도 대조했다. 이는 측정 오차를 포함한 추정치이며 모든 연주 타격이 기계적으로 정확히 180 BPM이라는 인증은 아니다.
- 저장 AAC의 39개 전환과 첫 회차 본문 20곳을 원본 재구성 파형과 대조했다. 59곳의 최대 시간 차이는 0샘플, 최소 파형 상관은 0.96926이었다. 최종 음량은 -15.95 LUFS, true peak -3.04 dBTP이며 클리핑은 관측되지 않았다. 원곡의 간주·조용한 본문을 무음이라는 이유로 제거하지 않았다.
- `output/continuous-180-20261024/transitions/`에 전환별 16초 청취 WAV 20개가 있다. 첫 회차 끝에서 두 번째 회차로 이어지는 샘플은 `20-01.wav`이다.
- 실제 40개 시작 시각은 `production/continuous-180-20261024/tracklist.txt`에 기록했다. 곡이 처음 들리는 순간의 인증이 아니라 다음 곡의 페이드가 시작되는 위치다.
- 독립 Astra/high 최종 오디오 검토는 CLEAN(확정 Critical/High 0·원칙 관찰 없음)이다. [검토 범위와 독립 측정](../../.ai/reviews/2026-10-24-0700-continuous-audio-review.md)을 따른다. 기술 검사 통과는 젠의 청취 승인이 아니다. 현재 새 보정본·연결 음원의 청취 승인, 새 업로드 제목 승인, 영상 제작·업로드는 아직 전이다.
- 이전 `Final Selected Audio Sources` 및 `output/report.json`의 해시·시각은 2026-10-12 개별 음원 제작 이력이다. 새 완성 믹스의 출처·시각은 위 제작 기록을 따른다. 새 믹스는 아직 발매 게이트에 맞는 최종 보관 계약으로 승격하지 않았다. `pack`으로 반복·합성을 추가하지 않는다.

## Previous Release Summary — 과거 기록
Status (2026-10-12): 젠이 번호별 최종 음원 20곡을 확정했다. 기존 선택 02·03·04·13·14·18·19 일곱 곡, 1차 선택 01·05·07·08·15·16·17·20 여덟 곡, 2차 11B, 젠의 직접 재제작 06·09·10, 현재 `[07:00]`에 있는 12를 사용한다. 정확한 20개 ID는 `input/suno-final-selection-2026-10-12.json`에 있다. 현재 선택과 일치하는 WAV 20개를 파일 형식·길이·해시로 확인했다(`input/download-manifest.json`, 합계 약 58분 19초). 옛 05·06·07 WAV와 기존 선택 기록은 이력으로 보존한다. 젠은 이 곡들로 20~30분 달리면 평균 케이던스가 대략 180이라고 보고했다. 탐색적 오디오 측정에서는 일부 곡이 약 174~192 BPM으로 추정됐다. 20곡의 채택은 유지하고 `180 BPM`은 목표 케이던스 표기로 쓰며 전곡이 정확히 180 BPM이라는 주장은 하지 않는다. 음악적 품질의 별도 기계 판정은 아직 없다. Wavvy24에 업로드했고 2026-10-12 17:00 KST 공개 예약 시각 이후 Studio에서 공개·4K 처리 완료를 확인했다.

젠의 2026-10-06 다운로드 보류는 2026-10-12 재개 요청으로 끝났다. 확정 20곡을 번호순으로 2회 반복한 40개 재생 구간의 4K 본편을 렌더했고, 40개 시작 시각을 포함한 업로드 문안을 작성했다. 선택 음원의 일부 정확한 원문 프롬프트는 확인되지 않아 최초 보컬 txt를 최종 음원 출처로 승격하지 않는다. 현행 선택 ID·WAV 해시·확인된 원문 또는 관측된 화면 설명을 아래 `Final Selected Audio Sources`와 `input/final-selected-audio-sources.json`에 구분해 기록한다.

2026-10-12 현재: Suno 대화상자에서 Pro 다운로드 20회를 확인한 뒤, 확정된 20곡의 WAV를 수집했다. 06·09·10은 젠이 최종 채택했고, 12는 10월 6일 선택 B와 다른 현재 화면의 음원을 젠이 최종 12번으로 골랐다. 현재 `input/tracks/`의 상위 폴더에는 선택된 WAV만 20개 있다. 옛 05·06·07의 원본 해시와 파일은 `input/historical-downloads-2026-10-03.json` 및 `input/tracks/history/2026-10-03/`에 보존했다. 다운로드 과정에서 자동으로 생긴 M4A는 Downloads에 남겨 두었고 패키지에는 넣지 않았다.

시각 작업(2026-10-12)은 이전 영상의 강변 새벽 장면과 시간 표기가 있는 썸네일이었다. 2026-10-24 새 최종본으로 교체했으며 옛 배경·시안·배치 지시·과정 검토 문서는 이번 썸네일 정리 대상이다. 현재 제작 입력이나 보존 대상이 아니다.

## Final Artwork — 2026-10-24

- 최종 생성 프롬프트: `input/thumbnail-prompt.txt`. 최종 장면의 생성·배경 수정 지시를 모은 재현용 설명이며 동일 픽셀을 보장하는 기록은 아니다.
- 글자 없는 원본: `input/thumbnail-source.png`, 1672×941, SHA-256 `6bfe986cce7ff3ed9c17c60c816e51873d00e89b3cfd2c6adeaf11bb7d2111fe`.
- 젠의 편집 원본: `input/thumb.psd`, 2532×1424, SHA-256 `533a338c6dc1f68f76bbad31b377f37a5287435540e92ecab0f4562a03ae5439`.
- 최종 썸네일 겸 새 영상의 정적 이미지: `input/thumb.jpg`, 2532×1424, SHA-256 `93b63f208ff89c81c705ef64b53fd299911a55d7f65d8a3386bd65fa8feb4944`.
- 새 영상은 최종 JPG를 3840×2160으로 확대해 사용할 예정이며 원본 사진이 4K로 생성됐다고 주장하지 않는다. 아직 영상은 제작하지 않았다.
- 옛 `input/loop.png`를 새 영상 입력으로 사용하지 않는다. 완성된 2회 믹스와 최종 JPG를 직접 연결하는 정적 이미지 제작 방식을 사용한다. 일반 `pack` 반복을 다시 적용하지 않는다.

## Upload Status

- Status: pending
- 현재 작업: 180 BPM 보정·박자 연결·새 썸네일로 재제작 중이며 새 업로드는 아직 하지 않았다.
- 이전 영상 `DU_vBuIdMG4`는 젠이 삭제했다고 보고했다(2026-10-24). 아래 공개 확인은 삭제 전 과거 기록이다.

## Previous Upload — 2026-10-12 과거 기록

- YouTube 업로드 완료: Wavvy24 채널, https://youtu.be/DU_vBuIdMG4, 2026-10-12.
- 공개 예약: 2026-10-12 17:00 서울(GMT+09:00). Studio 확인 대화상자와 콘텐츠 목록의 `예약됨` 상태를 확인했다.
- 최종 제목: `Playlist | 상쾌하게 달릴 준비 됐나요?! 🏃 | 180 BPM Running Mix · 2Hour | Wavvy | 07:00`. 젠의 최종안 승인 후 2026-10-12 YouTube Studio에서 저장 완료를 확인했다. `2Hour`는 제목 표기이며 실제 영상 길이는 1:56:06이다.
- 업로드 파일: `output/final.mp4` (3840×2160 H.264/AAC, 1:56:06). 20곡을 번호순으로 2회 반복했다.
- 2026-10-12 16:08 KST 재확인: 콘텐츠 목록은 `예약됨`이다. 목록에는 `4K까지 처리 ... 완료`가 표시되지만 영상 세부정보의 화질 표시에는 아직 `4K 처리 중`이어서 4K 완료로 판정하지 않는다. `소유권 주장 개요`에는 `동영상에서 소유권 주장이 발견되지 않았습니다`가 표시됐다. 당시 실제 공개는 17:00 이후 확인 대상이었다.
- 2026-10-12 약 17:20 KST 재확인: Studio 세부정보와 새로 불러온 콘텐츠 목록에 모두 `공개`가 표시됐고, 목록에 `4K까지 처리 ... 완료`가 표시됐다. 목록의 게시일은 2026-10-12이다. 앞선 `예약됨`과 세부정보의 `4K 처리 중`은 과거 확인 시점의 상태다.
- 2026-10-12 약 18:22 KST: 아래 고정 댓글 원문을 Wavvy24 계정으로 공개 영상에 게시했다. [댓글 링크](https://www.youtube.com/watch?v=DU_vBuIdMG4&lc=Ugz4aOucarXn6_sgILZ4AaABAg). Aside YouTube 조회에서 동일 원문 댓글 1개를 확인했고, 시청 페이지를 새로 불러온 뒤 `@wavvy24님이 고정함` 표시를 확인했다.
- 아동용 아님, AI 사용 예, 유료 프로모션 없음으로 설정했다. 가사 없는 음원이므로 가사 자막은 제출하지 않았다.

## YouTube Metadata (v2.1 — 삭제된 이전 영상의 문안, 새 제목 승인 전 참고)

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
🏃 02:58 - 02. 파란불
🏃 06:09 - 03. 첫 바퀴
🏃 08:32 - 04. 조금 일찍
🏃 11:43 - 05. 길을 바꿔
🏃 14:41 - 06. 정해 둔 건 없어
🏃 16:45 - 07. 같은 방향
🏃 19:43 - 08. 낮은 비트
🏃 23:02 - 09. 숨을 세어
🏃 26:23 - 10. 생각을 놓고
🏃 28:48 - 11. 다시 해볼게
🏃 31:47 - 12. 바람이 바뀌어
🏃 34:28 - 13. 호흡
🏃 37:39 - 14. 하나씩
🏃 40:49 - 15. 드럼 위로
🏃 43:25 - 16. 비가 갠 뒤
🏃 45:51 - 17. 이어지는 소리
🏃 49:18 - 18. 가까운 곳
🏃 52:29 - 19. 괜찮은 날
🏃 55:40 - 20. 집으로 가는 길
──────────────
다시 한 바퀴
🏃 58:03 - 01. 문을 열고 (반복)
🏃 01:01:01 - 02. 파란불 (반복)
🏃 01:04:12 - 03. 첫 바퀴 (반복)
🏃 01:06:35 - 04. 조금 일찍 (반복)
🏃 01:09:46 - 05. 길을 바꿔 (반복)
🏃 01:12:44 - 06. 정해 둔 건 없어 (반복)
🏃 01:14:48 - 07. 같은 방향 (반복)
🏃 01:17:46 - 08. 낮은 비트 (반복)
🏃 01:21:05 - 09. 숨을 세어 (반복)
🏃 01:24:26 - 10. 생각을 놓고 (반복)
🏃 01:26:51 - 11. 다시 해볼게 (반복)
🏃 01:29:50 - 12. 바람이 바뀌어 (반복)
🏃 01:32:31 - 13. 호흡 (반복)
🏃 01:35:42 - 14. 하나씩 (반복)
🏃 01:38:52 - 15. 드럼 위로 (반복)
🏃 01:41:28 - 16. 비가 갠 뒤 (반복)
🏃 01:43:54 - 17. 이어지는 소리 (반복)
🏃 01:47:21 - 18. 가까운 곳 (반복)
🏃 01:50:32 - 19. 괜찮은 날 (반복)
🏃 01:53:43 - 20. 집으로 가는 길 (반복)
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

## Final Selected Audio Sources

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

## Initial vocal source arc (historical)

The following titles and lanes describe the initial submissions. The lyric angles and proposed leads are historical; they do not apply to the instrumental covers and are not approved Final Track Sources.

| # | Working title | Energy role | Main musical variation | Initial lyric angle | Initial lead |
|---|---|---|---|---|---|
| 01 | 문을 열고 | open | bright synth pluck, dry live-feel drums | air and first beat | Female |
| 02 | 파란불 | open | muted guitar rhythm and synth bass | step into the beat | Male |
| 03 | 첫 바퀴 | open | arpeggiator and crisp kick | settling breath | Female |
| 04 | 조금 일찍 | open | warm keys and light breakbeat | waking through movement | Male |
| 05 | 길을 바꿔 | stride | guitar chop with electronic drums | same pulse, new route | Female |
| 06 | 정해 둔 건 없어 | stride | rubbery bass and short synth replies | leave the distance counter aside | Male |
| 07 | 같은 방향 | stride | layered guitar and pad | own pace | Female |
| 08 | 낮은 비트 | stride | percussive keys and restrained 808 sub-bass | low end and light steps | Male |
| 09 | 숨을 세어 | stride | shimmering sequencer | breathing and counting | Female |
| 10 | 생각을 놓고 | stride | clipped synth chords | release mental noise | Male |
| 11 | 다시 해볼게 | push | heavier live kick and bass synth | recover the pace | Female |
| 12 | 바람이 바뀌어 | push | syncopated synth lead | adjust to a changing breeze | Male |
| 13 | 호흡 | push | sharp drums and warm counter-melody | comfortable breath | Female |
| 14 | 하나씩 | push | bass-led indie dance | one step at a time | Male |
| 15 | 드럼 위로 | push | wide chorus guitar and synth | voice riding the drums | Female |
| 16 | 비가 갠 뒤 | push | driving drum break and lifted chords | air after rain | Male |
| 17 | 이어지는 소리 | return | light piano over steady drums | hold the pulse lightly | Female |
| 18 | 가까운 곳 | return | soft plucked synth, defined bass | focus on the next stretch | Male |
| 19 | 괜찮은 날 | return | open guitar and brushed synth | keep a sustainable pace | Female |
| 20 | 집으로 가는 길 | return | simple repeating synth figure | return without slowing the beat | Male |

## Production status

Initial vocal txt: 20/20, with track-prompt and full-song lyric-record gates PASS. These apply to the first generation only. Instrumental remake txt: 12/12 in `input/remakes/`, with track-prompt gates PASS. First-pass, remake, and Cover IDs remain in their historical manifests. 젠이 20곡을 한 번호당 한 곡으로 정리한 뒤 Suno `[07:00]`을 새로고침해 20곡과 고유 ID를 대조했다. `input/suno-selected.json`은 당시 선택의 역사 기록이고, 현재 선택은 `input/suno-final-selection-2026-10-12.json`이다. 젠의 전곡 청취 및 약 180 케이던스 체감 PASS를 기록했다. 일부 구간의 탐색적 박자 측정은 했지만 전곡·전 구간 정확한 BPM 인증이나 기계적 무가사 검사는 하지 않았다.

The Suno download dialog displayed 7 remaining Pro downloads on 2026-10-03 before that historical download pass. 젠이 당시 01을 MP3/M4A로 받았고, Codex가 당시 선택 ID를 대조해 02–07을 WAV로 다운로드했다. 2026-10-12에는 현재 선택된 20곡을 모두 WAV로 수집했고, 옛 05·06·07은 이력 폴더로 분리했다. 현재 20개 파일은 48 kHz·16-bit PCM·stereo WAV이며 Downloads 원본과 시리즈 복사본의 SHA-256이 일치한다. Suno's [download policy](https://help.suno.com/en/articles/13926209) counts each distinct song once, regardless of format. A browser-stream pulse probe of an earlier 20B candidate at 30–42 seconds suggested a roughly 92–94 BPM low-frequency pulse; that short window was inconclusive and the candidate is not the selected 20. 그 당시 탐색은 Aside 탐색 실패 두 번 뒤 중단했다. 2026-10-12에는 현재 선택 중 일부 WAV 구간을 탐색적으로 측정해 약 174~192 BPM 추정치를 기록했으나, 전곡 정확한 박자 인증으로 해석하지 않는다.

The ten agent-created Covers are recorded separately from the initial 40 and later remakes. 2026-10-03 젠은 당시 01–20 전체를 번호별로 청취 PASS했고 Suno에는 각 번호 한 곡씩만 남겼다. 그날의 20개 ID는 `input/suno-selected.json`에 고정한 역사 기록이다. 당시 청취 러닝감 PASS는 수치 BPM 측정이 아니다. 2026-10-06 재구성 뒤 보존 번호는 02·03·04·13·14·18·19이다. 그날 새로 남긴 1차 아홉 곡 중 12는 2026-10-12에 현재 작업공간의 다른 음원으로 교체됐다. 옛 05·06·07 WAV는 이력으로 보존한다. 젠이 직접 만든 06·09·10은 2026-10-12 최종 채택했다. 최종 출처는 옛 보컬 txt를 복사하는 방식 대신 `Final Selected Audio Sources`의 ID·해시·원문 확인 상태로 구분해 기록한다.
