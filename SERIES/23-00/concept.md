# 23:00 Relax Alternative R&B / Lo-fi R&B

Version: 0.29
Last Updated: 2026-11-04

## Series Status

- **Current work (2026-11-04)**: 젠 rejected the earlier agent-made style/lyrics and supplied songs in `[23:00]`. The current workspace observation contains 17 exact Lo-Fi Remixes, with displayed durations totaling 55:41. These 17 IDs are the browser-recording scope; 젠 then selected the 17-song order by fixing 1 작은 빛, 2 돛, 3 한 잔만 더, 4 이름 and 6 마음 밖, alternating old/new from position 4, then placing remaining old songs at the end. See `production/browser-capture-20261104/sequence.{json,md}`. See `production/browser-capture-20261104/source-catalog.json`.
- **Video production (2026-11-04, 젠 「이제 영상 제작하자.」)**: 4K 본편 영상 렌더까지 마쳤다. YouTube 업로드·공개·자막 게시·커밋·푸시는 하지 않았다. 17곡을 `input/tracks/NN__제목__Relax__Lo-fi R&B__NA.wav`(48 kHz stereo float32)로 넣었다. 각 곡은 가드 구간(앞 0.5초·뒤 0.75초) 안에서 두 채널이 정확히 0.0이 아닌 첫 샘플과 마지막 샘플로 잘랐고, 결과 WAV는 `raw.wav` 조각과 바이트가 같다. 컷 길이는 원곡 재생 시간보다 +0.0086~+0.0089초 길고(허용 ±0.5초 이내), 합계 3,340.268초(원곡 재생 합계 3,340.12초)다. 곡별 컷 구간·해시는 `input/download-manifest.json`(`source_kind: system_audio_capture`)과 `production/video-production-20261104/audio-cut-verification.json`에 있다. 현재 선택 17곡의 기계 기록은 `input/suno-final-selection-2026-11-04.json`이다(`sequence.json`에서 파생, 새 결정 아님). 표준 `pack`(0.8초 acrossfade · -14 LUFS · -1.0 dBTP · 2회 반복)으로 `output/final.mkv`(3840×2160 H.264 + FLAC, 컨테이너 6654.0초, 오디오 디코드 6653.95초)와 `output/report.json`(final_duration 6654.14초)·`upload.csv`·`provenance.md`를 만들었다. 2회차 첫 곡 시작은 오디오 일치로 3326.668초를 실측해 보고서 계산과 맞았다. 챕터(1회차 17 + 2회차 17)는 아래 `## YouTube Metadata`에 채웠고 `upload.csv`와 같다. 제목은 젠이 승인했다(「확정. R&B 포함.」, 2026-11-04, 오케스트레이터 전달): `Playlist | 커피, 바람, 밤, Groove ☕ | LO-FI POP · R&B | 노동요 · 카페 · 매장 · 작업 | Wavvy | 23:00`(85자). `upload.csv`의 제목·설명·태그는 concept와 같고 `verify-release`로 대조했다. 설명·태그·해시태그·고정 댓글은 이후 젠이 승인했다(아래 업로드 준비 항목과 `## YouTube Metadata`). 업로드 뒤 정리로 `final.mkv`·`preview.mp4`·`input/tracks/*.wav`는 삭제했다(Local Retention 절; 곡별 파일명·SHA-256은 Final Track Sources가 보존).
- **Upload preparation (2026-11-04, 젠 「자막 먼저 만들고 공개」)**: 업로드·Studio·공개·댓글·Suno 조작·커밋·푸시는 하지 않았다.
  1. *승인 문안*: 설명·태그를 오케스트레이터가 보여 준 승인 문안으로, 고정 댓글을 승인 3줄로 바꿨다(`## YouTube Metadata`, 원문 「좋아. 업로드 하자. 바로 등록」·「확정」은 오케스트레이터 전달). `output/upload.csv`는 하네스 `generate_upload_csv`로 다시 만들었고(렌더·`final.mkv`·`report.json` 그대로) `verify-release` PASS. 고정 댓글 게시는 다음 업로드 단계다.
  2. *가사 원문 기록*: 17곡 모두 `input/tracks/NN_<제목>.txt`로 만들었다. 가사는 Suno 곡 화면의 `lyrics_raw` 그대로(해시 대조), STYLE·EXCLUDE는 `style-provenance.json` 기록 그대로이며 원곡 연결 확인 3곡 / 가사 일치 후보 8곡(잠정) / 젠 직접 제작 6곡의 구분과 `actual_generation_input_verified: false`를 각 txt의 SOURCE RECORD 절에 남겼다. 옛 txt 20개는 `input/source-history/` 아래 보존 폴더로 옮겼다가 2026-11-04 젠 「지우기」로 삭제했다(Local Retention 절; 복원은 git 커밋 `791bea1` 이전 기록). 옛 9곡 txt의 가사는 현재 Suno 가사와 줄·글자가 모두 같다. 선택 ID↔txt 해시는 `input/suno-current-sources-2026-11-04.json`이 묶는다. `finalize-upload --check` PASS 뒤 `--keep-txt`로 아래 가사 원문 보관 절을 채웠고, 시간 표시 없는 자막은 `output/youtube_subtitles_ko_no_timing.txt`로 만들었다.
  3. *시간 자막*: 저장소 `.venv/`의 mlx-whisper 0.4.3 + `mlx-community/whisper-large-v3-turbo`로 17곡의 단어 시각을 얻어 `input/validation/2026-11-04-timed-subtitles/`에 시간표(`all-tracks-timed-checked.json`)·음성 근거 39개·자체 점검(`self-check-result.json`)을 남겼다. 회차당 큐 745개(전체 1,490), 노래에서 추가로 반복된 승인 가사 10줄(8번 먼지 2줄, 10번 산책 4줄, 16번 골목 4줄), 약한 줄은 짧은 구간 재인식으로 확인했다. 노래에 없는 승인 가사 8줄(2번 돛 2줄, 12번 숨 2줄, 지시어 `instrumental` 4줄)은 시간표에 `unsung_source_lines`(원문·이유·해시된 음성 근거)로 선언했다. 이 선언과 보고서 길이 합 계산(곡별 반올림 대신 정확한 합 뒤 한 번 반올림)을 위해 오케스트레이터가 승인한 `wavvy_harness/subtitles.py` 패치를 적용했다(적용 끝난 `proposed-harness-patch-subtitles.diff`는 정리로 삭제했고 실제 diff와 검사 원문은 `input/validation/2026-11-04-timed-subtitles/harness-patch-checks/`, 새 테스트는 `tests/test_subtitle_timing_contract.py`). 인식 기반 추정이며 사람이 들어 본 검증이 아니다. `prepare-subtitles --timing-map` → `verify-subtitles --stage prepared` PASS(1,490큐, `output/youtube_subtitles_ko_timed_estimated.srt` sha256 `ad40da726de76d79baca9d340164372a3c6b13866647dd1146ad045552047fe9`)이고 `source-final`·`render-final`·`upload-ready` 게이트, `verify-release`, `state --check`가 모두 PASS다(state phase `upload_ready`). 자막 게시(`published`)는 업로드 단계의 일이다.
- **Recording**: all 17 full-song recordings are technically verified, with source playback durations totaling 55:40.12. Ego probes were silent; 젠 requested Aside and its first Suno tab. Capture used Aside MCP and exact bundle `at.studio.AsideBrowser`, excluding microphone. Raw and guarded stereo 48 kHz float32 WAVs were kept locally under `work/2026-11-04-2300-browser-capture/` until the post-upload cleanup deleted that folder (Local Retention section). The guarded copies retain 0.5 seconds before and 0.75 seconds after estimated boundaries; output latency is uncalibrated. See `production/browser-capture-20261104/recordings.md` and `capture-manifest.json`. Browser recording is not an official source download, final edit or musical-quality approval.
- **Style records**: preserve current Suno Styles and lyrics for all 17 remixes. Record `original STYLE + remix STYLE` and keep minus-prefixed EXCLUDE items separate. Three exact original links are evidenced; eight title/lyric-matched originals are provisional. For the other six, 젠 replied 「이건 직접 만든거야.」 on 2026-11-04; record their current displayed style without inventing a separate original style. The reply and exact scope are preserved in `production/browser-capture-20261104/user-style-clarification.json`. The current source is `production/browser-capture-20261104/style-provenance.{json,md}`. Do not promote provisional pairings or fill missing original text by guesswork.
- **Time Slot**: 23:00.
- **Genre Lanes**: relax alternative R&B, lo-fi R&B.
- **Numbering**: all 17 exact Suno song IDs have `N. existing title` saved and confirmed after reopening. The selected album sequence is owned by `production/browser-capture-20261104/sequence.json`; persistence evidence is `suno-sequence-numbering-20261104.json`. Capture indices 01–17 retain collection order only. Earlier 20-song Track Map/file numbers are historical.
- **Suno workspace**: `[23:00]` (`f578d3c2-f43f-462e-8e05-44d022edd480`) — https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480
- **Earlier 20-song material (deleted 2026-11-04)**: the 20 agent source txt files, their source history, the candidate ledger `input/suno-candidates.json` and the 11/1–11/2 generation/selection records were historical material, not the current 17-song recording selection. 젠 answered 「지우기」 and the post-upload cleanup deleted them (Local Retention section); `verify-release` reads `input/suno-final-selection-2026-11-04.json`. The earlier request to choose round-2 A/B candidates is superseded by 젠's current songs. No replacement music generation or upload was requested. 젠 separately requested title numbering for these 17 current songs; all saved titles have been reopened and confirmed. 젠 then requested the thumbnail described below.
- **Machine state (2026-11-04)**: the 17 current recordings were cut into `input/tracks/*.wav` (see Video production above) and the 17 current source txt files sit beside them. The final-source archive section below was written by `finalize-upload --keep-txt` from those 17 txt files; its STYLE/EXCLUDE are the recorded Suno display text (original + remix for 11 songs, current style for 6 songs 젠 made directly), not proof of the exact generation input. The uncut raw and guarded recordings stay in local `work/`. State phase is `upload_ready` (timed subtitles prepared and verified; publication is not).

## Current artwork — 2026-11-04

- **Canonical thumbnail**: `input/thumb.jpg`, actual JPEG 3840×2160, Wavvy logo at top left and the brown serif brand sentence at bottom left (no title heading). 젠 corrected the location: 「썸네일은 원래 input 폴더에 있어야해.」. Exported from the lossless final with ImageMagick JPEG quality95, 4:4:4 sampling; dimensions unchanged. Its current hash/size are in `production/artwork-final/artwork.json`.
- **Lossless selected image**: `input/thumb.png`, SHA256 `c23e92bf5d7f8fada854ca2e002888e0784082ded89e93a293f804691593134c`. 젠 asked 「하단의 Lo-fi Groove 텍스트 없애줘.」, so the `Lo-fi Groove` title was removed. Current composition = Wavvy logo + brown serif brand footer. Method: the full-width band y1880–2035 was restored from the text-free `scene-original-4k.png`; the prior title area was [128,1939,597,2000]. Pixel checks: the restored band has no difference from the text-free original, PNG changes versus the previous PNG are confined to [128,1939,597,2000], and the size is 3840×2160. The footer remains the exact `wavvy.md` brand sentence in brown Baskerville Regular54pt at x128/y2040, and the logo, footer, scene and text-free originals are unchanged. The final4K JPEG (SHA256 matches the earlier footer-only JPEG) was delivered as Telegram 56035 with configured recipient verified. The previous Baskerville Bold700 title details are preserved in `production/artwork-final/artwork.json` under `removed_title`; the removal record is `title_removal`.
- **Final unbranded illustration originals**: `production/artwork-final/scene-original-native.png` (1672×941, SHA256 `f0a9aa28cb85769f3e6216c4f636fcfa8b1fd754538c3b89c6b01cea6622b9db`) and `scene-original-4k.png` (3840×2160, SHA256 `861513fa8f868bb51b79c7c83865181e530f0e7916f1e5011c865af16ba47559`). Both have no logo/text. The 4K original is a Lanczos enlargement, not native 4K generation. The originals and small `artwork.json` are the only three files in that production folder.
- **Requested cleanup completed**: 젠 said 「최종버전 말고 작업중 과정 프롬프트나 결과 이미지, 폴더 싹 지워.」. Deleted 147 process files totaling 109,614,589 bytes and 8 empty directories: previous drafts/composites, handwritten title resources/prompts/results, previews, process scripts/reviews/receipts, thumbnail plan, exact matching generation-cache copies, and obsolete record-shop inputs/contract/review. Scoped independent Sol 6.1 high pre-deletion review CLEAN; final/protected file checks passed after deletion. Evidence and subsequent thumbnail relocation: `.ai/cleanup/2026-11-04-2300-artwork-cleanup.json` at repository root. Deleted process artifacts were not restored.
- **Video background (2026-11-04)**: `input/video-background.png`, 3840×2160 RGB PNG, SHA256 `e3be204639a1d2cd0e593366cb7e5e3ab81e948a526488bb644631198344d03f`. 현재 `input/thumb.png`에서 전체 폭 띠 y2035–2100을 글자 없는 `production/artwork-final/scene-original-4k.png`로 복원해 만들었다(사전 확인: 그 띠 안의 thumb↔장면 차이 bbox = [128,2040,2787,2092]). 사후 측정: 새 배경↔장면 원본 차이는 로고 영역 [128,96,728,449] 안뿐(82,177픽셀)이고, 하단·제목 영역은 장면 원본과 같다. thumb.png와는 하단 문장 영역 [128,2040,2787,2092]만 다르고, thumb.jpg와는 해시·디코드 픽셀이 다르다. 직접 이미지를 열어(Claude Read, view_image) 로고만 있고 제목·BPM·다른 문구가 없음을 확인했다. 기록: `production/video-artwork-review.json`, `input/video-artwork.json`(`origin: generated_scene`). 장면은 1672×941 일러스트의 Lanczos 확대본이며 네이티브 4K 생성이 아니다. 최종 영상의 앞·2회차·끝 프레임에서도 로고만 보였다. 썸네일(`input/thumb.jpg`)은 그대로다.
- **Boundary of the earlier thumbnail path correction (historical; superseded by the video background above)**: only the thumbnail has been placed in input. No video background/role contract was created in this path correction. The footer was composed as a separate local font layer, and the requested heading was removed by restoring the band from the text-free 4K original; no new scene generation, audio/source change, render, upload, commit or push. Audio, lyrics, order, numbering and machine phase unchanged.

## Historical 20-song draft — deleted

옛 20곡 초안 자료는 2026-11-04 젠 「지우기」로 삭제, 복원은 git 커밋 `791bea1` 이전 기록.

## Source Records

- Earlier 20-song source txt files: moved to `input/source-history/` on 2026-11-04, then deleted by the post-upload cleanup (젠 「지우기」; Local Retention section). Restore from git commit `791bea1` or earlier.
- Current 17-song source txt files: `input/tracks/NN_<제목>.txt`, bound to the selected Suno IDs by `input/suno-current-sources-2026-11-04.json`; builder and checks in `input/validation/2026-11-04-final-sources/`.
- Observation: the earlier read-only ego lite observation of the nine existing remixes (`.ai/research/2026-11-01-2300-nine-tracks/`) was deleted with the earlier 20-song material (Local Retention section). The current 17 songs' Suno UI evidence is `production/browser-capture-20261104/suno-ui/`.
- Displayed styles and lyrics are not proof of the exact generation input. Durations differ by one second between the list and the play bar for some songs, so none is recorded here. Audio was not measured.
- Only 물결 showed Weirdness 20% and Style Influence 80% (it is a Cover). The other eight did not display those fields, which does not prove they are unset.

## YouTube Metadata (2026-11-04 — 제목·설명·태그·고정 댓글 젠 승인 · 챕터는 렌더 보고서 기준)

**승인 기록 (모두 2026-11-04).**

- **제목**: 젠 「확정. R&B 포함.」 — 이 승인과 아래 전체 제목(85자, `### 제목` 블록)은 오케스트레이터가 전달했다. 장르 칸 `LO-FI POP · R&B`와 용도 칸 `노동요 · 카페 · 매장 · 작업`도 이 승인 제목으로 정해졌다. 앞서 쓴 97자 초안(`보랏빛 창가에서 숨 돌리는 밤 🌙 | ALT R&B · LO-FI R&B | …`)을 대체한 제목이다.
- **설명·태그·해시태그**: 오케스트레이터가 채팅으로 보여 준 설명·태그 문안을 젠이 승인했다. 승인 원문은 「좋아. 업로드 하자. 바로 등록」이다(오케스트레이터 전달). 이전 단계의 설명·태그 초안(`커피 향 사이로 밤바람이 지나가는 시간` 등)은 이 승인 문안으로 대체됐다. Track List 자리는 `output/report.json`의 실제 시작 시각(1회차 17 + 2회차 17)이며 `output/upload.csv`와 같다.
- **고정 댓글**: 오케스트레이터가 아래 3줄을 보여 준 뒤 젠이 「확정」이라고 답했다(오케스트레이터 전달). 젠은 앞서 「고정 댓글도 달아줘」라고 요청했다. 게시와 고정은 다음 업로드 단계에서 하며, 이번 단계(시간 자막 준비)에서는 YouTube를 건드리지 않았다. 앞 단계에서 쓴 2줄 초안은 이 승인 문안으로 대체했다.

장르 표기는 확인된 음악 사실만 쓴다(17곡의 현재 스타일 기록: Lo-fi modern indie R&B, Korean indie alt-R&B 계열). 실제 전곡 BPM 측정이나 청취 품질 승인을 뜻하지 않는다.

### Context Mode

Settling — 23:00의 가라앉힘. 느긋한 Lo-fi Pop · R&B. 허용 어휘: 차분한, 느긋한. 신나는 표현은 쓰지 않는다.

### 제목

```
Playlist | 커피, 바람, 밤, Groove ☕ | LO-FI POP · R&B | 노동요 · 카페 · 매장 · 작업 | Wavvy | 23:00
```

### 설명

```
☕ 23:00, 커피 한 잔과 바람, 그리고 밤의 그루브
우리말 가사의 Lo-fi Pop과 R&B - Wavvy

늦은 밤 커피를 한 잔 내리고,
창문을 조금 열어 선선한 바람을 들이고,
턴테이블 위 음악에 맞춰 고개를 까딱이며
남은 일을 하나씩 정리해 가는 시간.

가게 문을 닫기 전 마지막 손님을 배웅하고,
불 켜진 창밖 도시를 잠깐 바라보다
다시 키보드 위로 손을 올리는 밤.

느긋하게 흔들리는 그루브를 따라
오늘의 남은 시간이 조금 더 가볍게 흘러가길 바라요.

──────────────
🎵 Track List
00:00 - 1. 작은 빛
03:37 - 2. 돛
06:55 - 3. 한 잔만 더
10:34 - 4. 이름
14:08 - 5. 비가 그쳤네
17:53 - 6. 마음 밖
21:00 - 7. 손 잡아도 될까
24:30 - 8. 먼지
27:49 - 9. 지금 가는 길
31:10 - 10. 산책
33:42 - 11. 나도 네가 신경 쓰여
36:54 - 12. 숨
40:28 - 13. 자꾸 네가 신경쓰여
43:57 - 14. 물안개
46:14 - 15. 약속
49:48 - 16. 골목
53:14 - 17. 물결

🔁 Repeat
55:27 - 1. 작은 빛 (반복)
59:04 - 2. 돛 (반복)
01:02:22 - 3. 한 잔만 더 (반복)
01:06:01 - 4. 이름 (반복)
01:09:34 - 5. 비가 그쳤네 (반복)
01:13:19 - 6. 마음 밖 (반복)
01:16:26 - 7. 손 잡아도 될까 (반복)
01:19:57 - 8. 먼지 (반복)
01:23:16 - 9. 지금 가는 길 (반복)
01:26:36 - 10. 산책 (반복)
01:29:09 - 11. 나도 네가 신경 쓰여 (반복)
01:32:20 - 12. 숨 (반복)
01:35:54 - 13. 자꾸 네가 신경쓰여 (반복)
01:39:23 - 14. 물안개 (반복)
01:41:41 - 15. 약속 (반복)
01:45:15 - 16. 골목 (반복)
01:48:41 - 17. 물결 (반복)

──────────────
Music for your space, 24 hours a day.
All tracks feature Korean lyrics.

🎵 Music: Wavvy
Copyright Ⓒ Wavvy. All rights reserved.

──────────────
#lofipop #rnb #노동요 #카페음악 #매장음악 #한국어가사
#playlist #플리 #wavvy #웨이비
```

### 태그

```
lofi pop, lo-fi pop, rnb, r&b, lofi rnb, korean rnb, korean lofi, late night playlist, night cafe music, cafe music, work music, store music, 노동요, 카페음악, 매장음악, 작업음악, 밤플리, 로파이, 알앤비, 한국어가사, korean lyrics, playlist, 플리, wavvy, 웨이비, 23:00
```

### 고정 댓글

```
☕ 커피, 바람, 밤, 그리고 Groove
오늘 밤, 이 플리는 어디에서 듣고 계신가요?
마음에 남은 곡 번호나 제목도 댓글로 남겨주세요.
```

## Upload Status

- YouTube upload: completed
- 공개 영상: Wavvy24(@wavvy24, 채널 ID `UC4R4NGwp19Y4lbdNs2HQVcg`), https://youtu.be/wbJQ2WgfJn4, 2026-11-04 21:54 KST 즉시 공개(YouTube 게시 시각 2026-11-04T04:54:31-08:00). 정상 UI 파일 제출은 **1회**다(`output/final.mkv`, SHA-256 `e2da2e859488aa90cea4570daa54c1483fd57163358e661ae85b286c38a38ebc`, 958,208,576바이트, 3840×2160 H.264 + FLAC 6654초). 제출 전 콘텐츠 목록에 같은 제목의 초안은 없었고, 새 영상을 중복 생성하지 않았다.
- 업로드 화면은 채널의 업로드 기본값 때문에 이전 영상의 제목(`[Playlist] [10:00] soomshuim | 조용히 몰입하는 시간, Chillhop`)·설명·태그 17개를 미리 채워 두었다. 승인된 `output/upload.csv` 제목·설명·태그로 덮어쓰고 기본 태그는 모두 지웠다. 다음 업로드에서도 제출 직후 이 세 칸을 확인해야 한다.
- 비공개 저장 뒤 다시 연 편집 화면에서 제목(85자)·설명(끝 줄바꿈 1개를 빼면 정확히 같음)·태그 26개(정확히 같음)·썸네일 `input/thumb.jpg`·아동용 아님·AI 사용 `예`·유료 프로모션 없음·카테고리 음악·댓글 켜짐·동영상 언어 한국어를 확인했다. 공개로 저장한 뒤 새로 불러온 편집 화면에서 공개 상태 선택이 `공개`였고, 로그인하지 않은 요청에서도 `isPrivate=false`·`playabilityStatus=OK`·길이 6654초·채널 `UC4R4NGwp19Y4lbdNs2HQVcg`가 나왔다.
- 직접 한국어 자막: `input/subtitles.json`이 가리키는 시간 포함 SRT(1,490구간, SHA-256 `ad40da726de76d79baca9d340164372a3c6b13866647dd1146ad045552047fe9`)를 Studio `수동 업로드 > 타이밍 포함`으로 올려 한 번 게시했다(`한국어 자막이 게시되었습니다.`). 자동 자막 생성이 끝난 뒤 Studio 언어 상자에서 `수동 자막 · 수동 · 게시됨`과 별도 `자동 자막 · 자동 · 게시됨`을 확인했다. 공개 시청 페이지 자막 메뉴는 `한국어`(수동) 선택 상태이고 `한국어 (자동 생성됨)`이 별도 항목이다. 첫 큐(00:13.96)·중간 큐(30:00)·2회차 큐(1:04:59)·마지막 큐(1:50:21)에서 SRT와 같은 글자가 보였다. Studio에서 내려받은 수동 SRT는 검증 파일과 끝 줄바꿈 한 바이트만 다르며 1,490구간의 글자·시각이 같다. 자동 자막·부분 음향 자료로 맞춘 읽기용 시간표이며 전곡 청취 판정은 아니다.
- 처리·검토: 2026-11-04 22:29 KST Studio 편집 화면의 `표준 화질 완료`·`고화질 완료`·`4K 완료` 표시를 확인했다(실제 4K 스트림 재생 인증은 아니다). 업로드 대화상자의 검토 단계는 `SD 처리가 완료될 때까지 검토가 실행되지 않습니다`로 대기 상태였다. 2026-11-04 22:00 KST 소유권 주장 화면은 `동영상에서 소유권 주장이 발견되지 않았습니다`였고 Studio 알림은 `—`였다. 이는 그 시각의 관찰이며 저작권 최종 판정을 별도로 포착했다고 주장하지 않는다.
- 공개 시청 페이지: 승인 제목 일치, 재생 시간 1:50:54, 설명의 Track List·Repeat 표시와 플레이어 챕터 마커 34개, 제목 아래 `AI` 표시를 확인했다. 설명 첫 줄의 `23:00`은 YouTube가 23분 지점으로 이동하는 시각 링크로 바꿔 보여 준다.
- 고정 댓글: 댓글 0개를 먼저 확인한 뒤 승인된 3줄을 한 번 게시했고(댓글 ID `UgyFpV0asefwfilJ-wt4AaABAg`) 고정했다. 시청 페이지를 다시 불러온 뒤에도 `@wavvy24님이 고정함`과 같은 3줄이 보였다.
- 결과 및 원시 UI 근거: [공개 기록](production/youtube-upload-20261104.json), [UI 근거 폴더](production/youtube-upload-ui-20261104/), [자막 게시 근거](input/validation/2026-11-04-timed-subtitles/publication/). 로컬 `final.mkv`·`preview.mp4`·`input/tracks/*.wav`는 업로드 후 삭제한다(Local Retention 절). `upload.csv`·`output/report.json`·썸네일은 보존한다.

## Local Retention

젠이 2026-11-04에 「작업에 쓰인 원본 영상등, 과정 파일들도 다 삭제」라고 지시했고(오케스트레이터 전달), 11/1~11/2에 에이전트가 만들었다가 채택되지 않은 옛 20곡 초안도 「지우기」로 답했다. 음원 WAV는 젠이 「검사 도구 고치고 삭제」를 택해 하네스를 고친 뒤 정리 대상에 넣었다(`MASTER/SSOT.md` Phase Contract). 범위·고정 목록·검사 기록은 `.ai/cleanup/2026-11-04-2300-post-upload-cleanup-*-v2.*`에서 확인한다.

- **지운 것**: 업로드한 영상 `output/final.mkv`와 `output/preview.mp4`, 컷 WAV `input/tracks/*.wav` 17개, 녹음 작업 폴더 `work/2026-11-04-2300-browser-capture/`(원본·가드 녹음·탐침·진단 실행 파일·로그)와 `SERIES/23-00/work/`(pack 임시), 옛 20곡 초안 자료(`input/source-history/`, `input/suno-candidates.json`, `input/validation/2026-11-01-generation/`·`2026-11-02-regeneration/`, `.ai/lyrics/2026-11-01_23-00_*`, `.ai/research/2026-11-01-2300-nine-tracks/`, 옛 초안 계획·검증 기록), 실패·대체된 검사 기록·중복 자막 사본·적용 끝난 패치 diff·완료된 단기 계획 4개(커밋 `791bea1`에 있음), 세션 임시 파일.
- **보존**: 최종 썸네일(`input/thumb.jpg`·`thumb.png`)·영상 배경(`input/video-background.png`·`video-artwork.json`)·`production/artwork-final/`, 가사·스타일 원문(`input/tracks/NN_*.txt`, 아래 Final Track Sources), 선택·녹음·렌더 기록(`input/suno-current-sources-2026-11-04.json`·`suno-final-selection-2026-11-04.json`·`download-manifest.json`, `production/browser-capture-20261104/`의 출처 기록, `production/video-production-20261104/`의 PASS 기록·컷 검증), 게시 근거(`production/youtube-upload-*`, `input/subtitles.json`과 `input/validation/2026-11-04-*`), `output/upload.csv`·`report.json`·`provenance.md`와 두 자막 파일.
- **음원과 하네스**: WAV를 지워도 Final Track Sources가 곡별 `Filename`과 `SHA-256`을 남기고 `output/report.json`과 일치해, uploaded 단계에서 음원 0개를 `audio_source: deleted_after_upload`로 본다. `pack`·`preview`를 다시 돌리려면 음원을 먼저 복원해야 한다.
- **옛 언급**: Series Status·Source Records·Upload Status 절의 옛 20곡 자료, `work/` 경로, `final.mkv` 안내는 삭제 전에 쓴 기록이다. 옛 초안 절(Historical 20-song draft 아래 옛 결정·Type Styles·Original Styles·Track Map)은 한 줄 안내로 교체했다.
- **실행 결과**: 2026-11-04 젠 「빨리 지워.」(오케스트레이터 전달)로 고정 목록 v2를 실행했다. 파일 1,496개 7,641,810,884 B(미디어 219개 7,557,230,274 B, 옛 20곡 초안 1,063개, 과정 파일 17개, 세션 임시 197개)와 빈 폴더 119개를 지웠고, 지키기로 한 4,055개는 해시·stat이 그대로다. 지운 뒤 `gate --stage uploaded`·`state --check`(revision 106, `audio_source: deleted_after_upload`)·`verify-subtitles` prepared/published가 PASS다. 마감 기록: `.ai/cleanup/2026-11-04-2300-post-upload-cleanup-v2-closeout.json`.

## Final Track Sources

> Generated by `wavvy.py finalize-upload` at 2026-11-04T21:08:24.
> Source origin: `filesystem`. `Source Checksum` is SHA-256 of the source txt content.

### 01. 작은 빛

- Timestamp: 00:00
- Repeat Timestamp: 55:27
- Filename: `01__작은 빛__Relax__Lo-fi R&B__NA.wav`
- Title: 작은 빛
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 218.29 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `085f11e1d986a7d08ebc5a1b2cf540c66616af90a74334d5a7b2c3e4f0b7650b`
- Source Title: 작은 빛 (Lo-Fi Remix)
- Source Checksum: `515b530175d2a9a089182a1e802211f1e3f243a156519998376387f2f69955c6`

#### STYLE

```text
Articulation, Korean Bedroom R&B, 72 BPM, Db Major, felt piano-led, warm Rhodes chords, soft brush kit, rim-click, warm bass groove, subtle strings in chorus, Male vocal: Warm, Intimate, Chest voice, Dry, articulation, warm baritone, conversational phrasing, gentle sustained chorus hook, chorus builds with emotional swell, tender vocal intensity, aching warmth, cozy intimate mix, wide stereo, warm low-end, moderate reverb, bedroom ambience, EQ balanced sound, clean mix, Lead vocal remains single and dominant throughout, No stacked or choir-like harmonies, Vocal line may intensify dynamically (gentle lift, higher register), but no additional vocal layers, Chorus vocal may be delivered with tender intensity or gentle sustained note, Higher register emphasis is allowed, Natural vocal warmth encouraged

Lo-fi modern R&B, Korean indie alt-R&B, 72 BPM half-time pocket, intimate felt-piano motif over warm Rhodes voicings, soft brushed drums and rim-click with a rounded understated bass groove; begin sparse, add muted electronic texture through the pre-chorus, widen gently with subtle strings in each chorus, then strip back for a close, vulnerable bridge and instrumental outro, Single warm baritone lead in a dry conversational chest voice, crisp Korean diction and deliberate articulation, natural breath and phrasing, sustained tender chorus notes with a restrained dynamic rise, Cozy close-miked vocal, balanced clean mix, warm low end, moderate room ambience, no layered vocals
```

#### EXCLUDE

```text
autotune heavy, vocoder, EDM drops, big room, choir, stacked harmonies, backing vocal layers, doubled vocals, powerful belt, aggressive dynamics, heavy bass drops, trap hi-hats, 808 slides, drill bass, upbeat, energetic, hype, party
```

#### LYRICS

```text
[Verse 1]
잠든 네 볼에
숨결만 살짝 닿아도
세상이 조용해
시계 소리도 멈춘 밤

아주 작은 코
올라갔다 내려오는 숨
이 방 가득한
기적 같은 너의 꿈

[Pre-Chorus]
밤새 지친 마음도
너를 보면 풀려가
말로 못 한 모든 걱정
이 순간에 사라져

[Chorus]
작은 손에 걸린 세상
little light
네 손가락 사이에 나의 하루가
살며시 또 웃는다
little light
이렇게만 있어 줘
아무 말도 말고
작은 손에 걸린 세상
little light

[Verse 2]
내 손가락을
꼭 쥔 채 잠이 들었지
빠질까 봐서
놓치지 않으려는 듯

내 어지러운
하루의 끝에 선 너는
한 번의 숨결로
모든 걸 다 비추는 불

[Chorus]
작은 손에 걸린 세상
little light
네 손가락 사이에 나의 하루가
살며시 또 웃는다
little light
이렇게만 있어 줘
아무 말도 말고
작은 손에 걸린 세상
little light

[Bridge]
울컥해지는 가슴
조용히 혼잣말해
“고마워
고마워”
내 전부가 되어 준 너

혹시 깰까 봐
숨소리도 낮춰 보며
다짐해
다짐해
이 손 절대 놓지 않겠다고

[Chorus]
작은 손에 걸린 세상
little light
네 손가락 사이에 나의 하루가
살며시 또 웃는다
little light
이렇게만 있어 줘
아무 말도 말고
작은 손에 걸린 세상
little light

[Outro]
[Instrumental]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 1406e9df-89fb-4daa-a46b-0c019d2dc7ab (https://suno.com/song/1406e9df-89fb-4daa-a46b-0c019d2dc7ab)
Suno title after numbering: 1. 작은 빛 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 10. 작은 빛 (Little light) (https://suno.com/song/8eda4384-1e3c-4386-941e-f914a77d7f4c)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 d923e0f75280a0b42e48ea53ae9d019f579db5354fd6043fd1f896c1c6b85af2); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/1406e9df-89fb-4daa-a46b-0c019d2dc7ab.json (sha256 4323d7f78070e843bfa8edb8e624cd7deeb9b3b2f53da433bfd021507ce9e76e); style-provenance.json tracks[capture 9]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 02. 돛

- Timestamp: 03:37
- Repeat Timestamp: 59:04
- Filename: `02__돛__Relax__Lo-fi R&B__NA.wav`
- Title: 돛
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 198.77 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `ccd1653941a9789a3cb0417ed72c1401da7dd9bdde342bb621ba4720ea4087a4`
- Source Title: 돛 (Lo-Fi Remix)
- Source Checksum: `5522ed05efe31bd2f71e1675a715723ffba08b0b2db6178a70ef372948a72fe5`

#### STYLE

```text
*Articulation, Major-key groovy R&B, 90 BPM, “ocean view” warm horizon vibe, Bass-forward pocket: round melodic bassline upfront, kick locked to bass, crisp rim/snare, soft hats, subtle perc, Rhodes/e-piano chords, light guitar arps, airy pads; very low wave ambience, Organic live-band feel, no EDM, Male vocal: soulful, intimate, natural; minimal runs in verses, no belting, minimal pitch correction, Verse1 & Verse2 share the same topline melody, Chorus lyrics repeat exactly each time, but the 2nd/final chorus is more emotional with natural higher mix/head notes and only a few short controlled riffs on the last two lines, Light backing harmonies in chorus; drums+bass push harder for catharsis, Form: intro–v1–chorus–v2–bridge (build + brief drop)–final chorus–outro quiet fade-out (strip to Rhodes + bass tail + pads, soft vocal, wave ambience fading), Avoid heavy autotune, excessive melisma, synth drops, sidechain pumping, k-pop

Korean indie R&B with lo-fi intimacy, slow laid-back half-time pocket, softened dusty drum texture, deep rounded bass, sparse Rhodes chords and restrained guitar details, Keep the arrangement spacious and understated; let verses sit close and dry, then widen the chorus gently without a dramatic lift, Direct, intimate male Korean vocal with natural chest-voice articulation, restrained emotion, minimal runs, subtle room ambience, warm muted mix and bittersweet late-afternoon feel
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[intro]

[verse1]
한낮의 빛이 숨을 삼키고
미지근한 향이 남아
눈꺼풀은 자꾸 내려오는데
저쪽이 이상하게 선명해
모니터 밖 하얀 빈칸, 어딘가
이름 없는 꿈을 향해

[chorus] [Hook]
멀어도 (멀어도)
또렷해지지 않아도 (않아도)
잠결이 길을 바꿔 놓아도 (놓아도)
눈이 먼저 잠깐 내려와도
빛은 사라지지 않아
눈을 감아도 남아

[verse2]
낮바람이 창끝을 머금고
하얀빛이 입술에 번져
눈꺼풀은 다시 내려오는데
저기는 이유 없이 선명해
모니터 밖 하얀 칸, 어딘가
이름 없는 쪽을 향해

[bridge]
누가 부르면 고개를 다시 들고
빛이 번지면 눈을 더 감고
누가 부르면 고개를 다시 들고
빛이 번지면 눈을 더 감고
잠깐 흐려져도 감각은 남아
손끝이 닿는 감촉으로 지금 붙들고
조금 더 천천히

[chorus]
멀어도 (멀어도)
또렷해지지 않아도 (않아도)
잠결이 길을 바꿔 놓아도 (놓아도)
눈이 먼저 잠깐 내려와도
빛은 사라지지 않아
눈을 감아도 남아

[outro]
깨어남은 아직 멀고
숨결은 계속 이어져

[outro]
깨어남은 아직 멀고
숨결은 계속 이어져

[ending]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 5bb566bd-ac12-4943-bf04-7ff9ac03c75b (https://suno.com/song/5bb566bd-ac12-4943-bf04-7ff9ac03c75b)
Suno title after numbering: 2. 돛 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 5. 돛 (https://suno.com/song/6ec3459c-cf47-40d2-9c44-2f290c1cf814)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 1b69bebb5429c739390f37884710d04654d28fbe5afd3bc8c2436952158b040a); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/5bb566bd-ac12-4943-bf04-7ff9ac03c75b.json (sha256 df08d497ad234707f83c5fcee40a329018cc3b4682a832490c6c6e03c3c99709); style-provenance.json tracks[capture 7]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 03. 한 잔만 더

- Timestamp: 06:55
- Repeat Timestamp: 01:02:22
- Filename: `03__한 잔만 더__Relax__Lo-fi R&B__NA.wav`
- Title: 한 잔만 더
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 219.81 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `1c18abb874465bb9fbbe393a7592b81259cd3cb68289da72bd4d629726d7da5a`
- Source Title: 한 잔만 더 (Lo-Fi Remix)
- Source Checksum: `a4d9892ea93e0ee05aac6d7c6f4c319f634d2762d53a73bfd30b8af28fe62857`

#### STYLE

```text
Lo-fi R&B, neo-soul with subtle city-pop touches; subtle tape wobble and vinyl texture on instruments, wide stereo Rhodes, tight low end, warm modern mix, Short D Major Rhodes 7th and 9th chord intro, then deep rounded kick, dry rimshot, shuffled hi-hats, warm bouncy bass, sparse muted guitar accents, 96 BPM, easy head-nodding pocket, warm, upbeat, relaxed but lively; sparse verses, gentle pre-chorus lift, fuller chorus, stripped-back bridge, Korean male midrange, intimate, clear warm close-miked dry centered lead, conversational behind-beat verses, crisp diction; catchy melodic chorus, fuller natural full-voice lift, playful syncopation, easy repeated hook
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro]
instrumental

[Verse 1]
겨우 날짜 맞춰 놓고
오랜만에 모인 자리
처음엔 일 얘기하다
이제 좀 재밌어지는데

몇 시냐고 묻는 말에
다들 휴대폰을 꺼내
난 못 들은 척하면서
남은 안주를 뒤적여

[Pre-Chorus]
아내가 기다린다며
슬슬 가봐야겠다는 너
벌써 시간이 그랬나
괜히 벽시계를 봐

[Chorus]
한 잔만 더 할까
아직 할 얘기가 남아
너희는 시간을 보고
나는 남은 잔을 봐

한 잔만 더 할까
그냥 한번 물어봤어
먼저 가, 난 천천히
마저 마시고 갈게

[Instrumental Break]

[Verse 2]
애인이랑 보기로 했대
늦게라도 얼굴 봐야지
아까부터 옷을 챙기던
네 옆자리가 먼저 비어

아이 재울 시간이라며
다른 친구도 일어나
요즘 자기 없인 안 잔대
웃으며 사진을 보여줘

[Pre-Chorus]
다들 그럴 만한 이유
나도 알아, 이해가 돼
붙잡을 말은 없는데
금방 일어나긴 싫어

[Chorus]
한 잔만 더 할까
아직 할 얘기가 남아
너희는 시간을 보고
나는 남은 잔을 봐

한 잔만 더 할까
그냥 한번 물어봤어
먼저 가, 난 천천히
마저 마시고 갈게

[Bridge]
다음엔 길게 보자고
누가 먼저 말을 꺼내
그러자고 대답하고
겉옷을 건네줬어

돌아가면 불을 켜고
혼자 뭘 좀 보겠지
오늘 들은 얘기들을
전해줄 사람도 없이

[Final Chorus]
한 잔만 더 할까
끝내 다시 묻진 않아
너희는 내일을 얘기해
나는 오늘이 좀 아쉬워

한 잔만 더 할까
그냥 한번 물어봤어
먼저 가, 난 천천히
마저 마시고 갈게

[Outro]
먼저들 들어가
난 조금 있다 갈게
집이 가까워서
걸어가면 돼
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 15d1eaaf-2450-4314-8252-cc9aede23fc8 (https://suno.com/song/15d1eaaf-2450-4314-8252-cc9aede23fc8)
Suno title after numbering: 3. 한 잔만 더 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 2e5b7f1b68f0cfd80a7f56857a5aff4194b706d643b457be63426f0334892266); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/15d1eaaf-2450-4314-8252-cc9aede23fc8.json (sha256 e1bc2ece6eb2de2ea6e3893957f21f9c08e213e01a171951b3915b884e48fc4e); style-provenance.json tracks[capture 3]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 04. 이름

- Timestamp: 10:34
- Repeat Timestamp: 01:06:01
- Filename: `04__이름__Relax__Lo-fi R&B__NA.wav`
- Title: 이름
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 213.97 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `2c693a2f03b8fd6a56064d3b972d6e924829f8ceee67859cdb48e5a0c4920712`
- Source Title: 이름 (Lo-Fi Remix)
- Source Checksum: `daec594dd1b61e28b527de4aebd192137018f07be12fcd707588057e79ca3710`

#### STYLE

```text
Korean Neo-soul R&B, 100 BPM, G minor Rhodes-led, electric bass very dry, layback groove, rim-click, NO 808, Male vocal, Raw, Direct, Dry, Simple melody, Chest voice dominant, No falsetto, no runs, no melisma, Precise articulation, Light room reverb, Clean mix, Verse1: Rhodes chords, sparse bass, confessional, gentle phrasing, Verse2: same contour; last 2 lines rise in intensity, Chorus: catchy singable hook, repeat identical; simple memorable melody, chest voice, Chorus2: bigger by arrangement only; no new vocal layers, Bridge: Rhodes + voice only, builds every bar, Outro: Rhodes fades, synth pad sustain, Single lead vocal throughout, No harmonies, no doubles

Lo-fi indie R&B, relaxed half-time pocket with soft swung drums, muted electric piano chords, rounded bass, faint tape hiss and intimate close-miked Korean lead vocal, Keep consonants crisp and syllables clearly separated, use measured chest-voice phrasing with natural breaths, Begin sparse, add warm guitar and subtle harmonic color through the chorus, pull back for the bridge, then return with a gently fuller final chorus and an understated outro, Soft saturation, dry vocal up front, narrow warm mix
```

#### EXCLUDE

```text
Autotune, Vocoder, Choir, Backing vocals, Runs, Melisma, Ad-libs, Rap, Hip-hop, Bright
```

#### LYRICS

```text
[Intro]
조용히 네 이름을 부르면
하루가 제자리로 돌아와

[Verse 1]
웃고 들어와도 눈이 먼저 말해
오늘이 쉽지 않았다는 걸
나도 모르게 마음이 메말라서
괜찮다는 말만 아껴 두었지
그때 너는 묻지 않고 다가와
내 숨부터 고르게 해줬어

[Chorus]
힘든 날에 잠시 기대도 될까
내가 무너지지 않게
서로가 서로의 곁을 지키는 일
그걸 우리 사랑이라 부르자
오르막 같은 하루 끝에서도
발 맞춰 걷는 우리
너만 있으면
너만 있으면

[Verse 2]
외로움이 문득 크게 들릴 때
세상에 나만 남은 것 같을 때
너는 작은 등불처럼 앉아
내 마음에 길을 밝혀줬지
말보다는 오래된 온도로
괜찮다는 말을 해준 사람
나도 이제는 네 하루를
내 두 손으로 감싸고 싶어

[Bridge]
우리도 가끔은 서툴겠지
마음이 앞서서 다칠 때도 있겠지
그래도 한 걸음만 늦춰서
서로를 다시 바라보자
손 놓치 말자
그 한마디면 돼
길이 더 가팔라져도
길이 보이지 않아도
같이 걷자
지금처럼

[Chorus]
힘든 날에 잠시 기대도 될까
내가 무너지지 않게
서로가 서로의 곁을 지키는 일
그걸 우리 사랑이라 부르자
오르막 같은 하루 끝에서도
발 맞춰 걷는 우리
너만 있으면
너만 있으면

[Outro]
고마워
오늘도 여기 있어줘서
내일도 우리 천천히
걸어가자
고마워
오늘도 여기 있어줘서
내일도 우리 천천히
걸어가자

[Ending]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 4708df3d-6f0a-4602-bea4-ccb734cf03db (https://suno.com/song/4708df3d-6f0a-4602-bea4-ccb734cf03db)
Suno title after numbering: 4. 이름 (Lo-Fi Remix)
Lineage status: confirmed_prior_suno_parent_link — original song link confirmed (prior Suno parent link observed)
Original song (Suno): 9. 이름 (https://suno.com/song/73330746-1b39-4cc4-8ff5-f2d3d06aa882)
Style record status: confirmed_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 dfddc87b1b08ad4019757aa31afcb5b41414f8f9c1feb3162979921b9dafebf9); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/4708df3d-6f0a-4602-bea4-ccb734cf03db.json (sha256 36f5ca7b831bf702e4012bb14f77c2d268f95838ab3c887946cf21fd733644cb); style-provenance.json tracks[capture 13]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 05. 비가 그쳤네

- Timestamp: 14:08
- Repeat Timestamp: 01:09:34
- Filename: `05__비가 그쳤네__Relax__Lo-fi R&B__NA.wav`
- Title: 비가 그쳤네
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 225.97 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `93e96b19697cc767208912150cd274ed4c058b602b02b547c5863b5b38ed51d4`
- Source Title: 비가 그쳤네 (Lo-Fi Remix)
- Source Checksum: `187b9ff546d81a562eeac7b5cf697f98aae5a30f01eb2e5c7987cbbbf248051d`

#### STYLE

```text
Lo-fi modern indie R&B ballad, intimate Korean female lead with clear conversational diction and grounded chest voice, mellow Rhodes chords over a relaxed half-time groove, soft dusty kick and brushed snare, restrained swung hats, rounded bass, sparse clean-guitar details, subtle tape warmth and gently blurred keyboard texture, Begin with a short, softened instrumental opening; keep verses close and understated, let the pre-chorus widen subtly, and lift the chorus with longer sustained notes and fuller low end, Strip back the bridge, then return to a warm, spacious final chorus and a quiet reflective outro; close dry vocal, uncluttered mix, gentle dynamics
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro]
instrumental

[Verse 1]
우산을 두고
창가에 앉아
늘 마시던 걸
한 잔 시켰어

흐린 창밖에
버스가 멈춰
몇 사람 내리고
다시 출발해

[Pre-Chorus]
커피가 나오기 전에
물을 한 모금 마셔
여긴 컵도 테이블도
그때 쓰던 그대로네

[Chorus]
비가 그쳤네
언제 그친 걸까
밖을 보고 있었는데
다른 생각을 했나 봐

커피는 다 마셨고
일어나면 되는데
늘 마주 앉던 쪽으로
한 번 더 눈이 가

[Instrumental Break]

[Verse 2]
넌 앉자마자
젖은 소매를 접어
난 냅킨 몇 장
네 앞에 놓았지

왜 말 안 했어
어깨도 젖었네
넌 한번 보더니
금방 마른댔어

[Pre-Chorus]
내 옷은 젖지도 않고
신발도 멀쩡했지
우산이 작다던 말에
그냥 그런 줄 알았어

[Chorus]
비가 그쳤네
언제 그친 걸까
밖을 보고 있었는데
다른 생각을 했나 봐

커피는 다 마셨고
일어나면 되는데
늘 마주 앉던 쪽으로
한 번 더 눈이 가

[Bridge]
비 오는 날 나가면서
내 신발부터 보던 너
그거 물이 잘 샌다며
다른 걸 신고 오랬지

오늘도 현관 앞에서
신발을 한번 바꿨어
누가 뭐라 한 것도 아닌데
비가 온다길래

[Final Chorus]
비가 그쳤네
길은 아직 젖었네
유리창에 비친 내가
소매 끝을 내려

커피는 다 마셨고
가방도 챙겼는데
늘 마주 앉던 쪽으로
마지막으로 눈이 가

[Outro]
문 옆에 둔 우산을
챙겨 밖으로 나와
물 고인 데를 피해
천천히 걸었어
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 3c9cb777-7397-4daa-bc46-a0516be1db8f (https://suno.com/song/3c9cb777-7397-4daa-bc46-a0516be1db8f)
Suno title after numbering: 5. 비가 그쳤네 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 778288ff40876859d0e030985f7e2765f45085de116ec98edb6021c61437654a); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/3c9cb777-7397-4daa-bc46-a0516be1db8f.json (sha256 7360aa7d45772b1502d101ac479d4a6f5ab9b08055e2650e2f994a59a5ab640a); style-provenance.json tracks[capture 1]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 06. 마음 밖

- Timestamp: 17:53
- Repeat Timestamp: 01:13:19
- Filename: `06__마음 밖__Relax__Lo-fi R&B__NA.wav`
- Title: 마음 밖
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 187.57 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `ab168b13399ed948d70d29a1eb3b620ffe9c4029de7ebde086224b05c3abdb87`
- Source Title: 마음 밖 (Lo-Fi Remix)
- Source Checksum: `a9f0006bb8c60dd3a0e4facd19196ac9326d4eda3cc769e2512b41ee2bbb45c9`

#### STYLE

```text
articulation, Korean R&B/pop ballad, 96–106 BPM, key color like A♭, Piano/Rhodes-led, cinematic but restrained, Warm keys upfront, soft supportive bass, tight understated kick (present, not huge), rim/snare light, simple hats, no rolls, Subtle strings/pads in choruses only, never dramatic, Verse intimate and sparse; chorus opens slightly wider with more harmony, not more rhythm, Final chorus adds a gentle “major-color” lift via chords/strings, not belting, Female vocal very forward and dry/close-mic: warm husky tone, clear Korean diction, conversational phrasing, controlled vibrato, natural breaths, minimal pitch correction, Melody understated (no big leaps, no catchy hook), Outro instrumental fade

Korean indie R&B, lo-fi remix, relaxed half-time pocket with softened kick and dry rim clicks, rounded subdued bass, muted Rhodes and dusty piano fragments, gentle tape saturation and restrained room texture, Keep verses close and sparse, let the choruses widen subtly with filtered keys and soft pad support, then ease into a worn instrumental fade, Forward intimate female lead, warm husky chest voice, clear Korean articulation, conversational phrasing, natural breaths, restrained vibrato; dry close vocal with minimal pitch correction
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro: Instrumental]
오늘은 묻지 않아
표정이 먼저 말해

[Verse 1]
네 말이 짧아
눈이 멀어
거리만 늘어
줄어드는 건
소리도 없어

[Bridge]
나도 이제
말을 접어
붙잡을수록
늦을까 봐

[Chorus]
끝을 아는 사람은
숨을 먼저 세어
나는 여기서 멈춰
너의 마음 밖
나는 여기서 멈춰
너의 마음 밖

[Verse 2]
우리 안에서
나는 혼자
웃는 연습도
멈춰버려
더 조용해

[Bridge]
흔들리면
돌아갈까 봐
기억을 접어
미워지기 전

[Chorus]
끝을 아는 사람은
숨을 먼저 세어
나는 여기서 멈춰
너의 마음 밖

[Chorus]
끝을 아는 사람은
숨을 먼저 세어
나는 여기서 멈춰
너의 마음 밖
나는 여기서 멈춰
너의 마음 밖

[Outro: Instrumental fade out]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 17a24019-4412-4443-b4e7-6d305d539958 (https://suno.com/song/17a24019-4412-4443-b4e7-6d305d539958)
Suno title after numbering: 6. 마음 밖 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 1. 마음 밖 (https://suno.com/song/d9a92230-a384-4077-9e9b-8ce9f7bb2159)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 2951bd3929f09351a80dcb75a8e0759817b754ad0c6742c0148f472696674148); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/17a24019-4412-4443-b4e7-6d305d539958.json (sha256 35433d9039342ef2dcf1adfba9c9d1d3b2fe6b130adc1f535af3ee3aa341c870); style-provenance.json tracks[capture 14]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 07. 손 잡아도 될까

- Timestamp: 21:00
- Repeat Timestamp: 01:16:26
- Filename: `07__손 잡아도 될까__Relax__Lo-fi R&B__NA.wav`
- Title: 손 잡아도 될까
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 211.61 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `f28225adeb1e1aa9c8d6f86e304ef6d271cd8d6344b17cdc6e578bc8d85ed376`
- Source Title: 손 잡아도 될까 (Lo-Fi Remix)
- Source Checksum: `f3f28d4968f956594e95b7419c3869262ef8354fce6dc973b816530b54630f0c`

#### STYLE

```text
Modern indie R&B with lo-fi neo-soul color: relaxed syncopated pocket, softened dusty Rhodes chords, rounded sub-bass, restrained kick and dry rim clicks, delicate shuffled hats, occasional muted guitar and finely chopped digital-key textures, Keep verses intimate and spacious with conversational low-mid male chest-voice delivery; let the pre-chorus open slightly, then give the chorus a warm, memorable lift without crowding it, A stripped bridge builds gently into the final chorus, followed by a soft close, Close-miked centered lead vocal, clean diction, restrained processing, subtle tape softness on instruments, clear contemporary mix and controlled low end
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro]
instrumental

[Verse 1]
저녁 먹고 나와
나란히 걷다
이야길 나누다가
살짝 스친 우리 손

괜리 민망해져서
주머니에 손을 넣어
넌 하던 말을 이어가
대답은 조금 늦어져

[Pre-Chorus]
무슨 생각 하느냐며
고개를 돌려 보는 너
아냐, 듣고 있었다고
괜히 말끝을 흐려

[Chorus]
손 잡아도 될까
몇 번을 생각하다
너는 앞을 보는데
나는 네 손을 봐

손 잡아도 될까
그냥 먼저 물어볼까
말은 못 하고 나란히
말은 못 하고 나란히

[Instrumental Break]

[Verse 2]
집에 가긴 좀 이르대
한 바퀴만 더 걷자고
아까부터 생각했던
그 말을 꺼낼까

좁은 길을 지날 때면
네가 조금 더 가까워
스치듯 가까운 손에
대답은 조금 늦어져

[Pre-Chorus]
이쯤이면 괜찮을까
나만 이렇게 떨리나
주머니 속 손을 꺼내
너와 거리를 좁혀

[Chorus]
손 잡아도 될까
몇 번을 생각하다
너는 앞을 보는데
나는 네 손을 봐

손 잡아도 될까
그냥 먼저 물어볼까
말은 못 하고 나란히
말은 못 하고 나란히

[Bridge]
이쪽으로 가자면서
네가 내 소매를 당겨
그러자고 대답하고
잠깐 걸음을 멈춰

손을 잡아도 되냐고
겨우 작게 물었더니
너는 대답하는 대신
내 손을 먼저 잡아

[Final Chorus]
손 잡아도 될까
한참 고민했는데
너는 내 얼굴을 봐
나는 괜히 웃음이 나

손 잡아도 될까
먼저 물어보길 잘했어
잡은 손은 그대로
네 걸음에 맞춰

[Outro]
조금 더 걸을까
아까 그 길로 돌아
집에 데려다줄게
천천히 가자
천천히 가자
```

#### META

```text
=== SOURCE RECORD ===
Suno song: f182958f-51dc-4d1e-9e1a-1b407d7abb33 (https://suno.com/song/f182958f-51dc-4d1e-9e1a-1b407d7abb33)
Suno title after numbering: 7. 손 잡아도 될까 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 c994b14258f9a68375fc6843242eb6c32fff91c2f6ffc9a31472620b00467185); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/f182958f-51dc-4d1e-9e1a-1b407d7abb33.json (sha256 d620d6bd8b108e7e46d4ce43ee435f1af8c9e6d44057a4c6da8d04fd4f0b9544); style-provenance.json tracks[capture 2]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 08. 먼지

- Timestamp: 24:30
- Repeat Timestamp: 01:19:57
- Filename: `08__먼지__Relax__Lo-fi R&B__NA.wav`
- Title: 먼지
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 199.89 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `699890877a7b3a25659f64c70ee5b5b5f344ce1151fa24d483e208ad11d5880a`
- Source Title: 먼지 (Lo-Fi Remix)
- Source Checksum: `d0ecb8a0a194ec40ccfe02bcadc9401f072d844cc85fee720ae6a8a0037efac7`

#### STYLE

```text
Korean Soft R&B, 74 BPM, Eb Major Vibraphone-led, supportive R&B groove, laid-back brush rhythm, warm afternoon texture, Male vocal, Natural, intimate, Raw, Solid, Direct, Dry, Chest voice dominant, No falsetto, Minimal vibrato, Verse1: vibraphone melody, sparse drums, drifting feel, Verse2: kick enters steady, groove locks in, vocal forward, Last line: natural strain allowed, breath audible, Chorus: solid kick and snare, melodic bass, pad widens, Vocal confident, slight belt on held notes, Final chorus: soulful ad-libs permitted, Bridge: vibraphone and voice only, gentle build, Outro: gradual fade, vibraphone restates motif softly, Single lead vocal, No harmony, no backing vocals

Lo-fi modern R&B, Korean indie alt-R&B, relaxed half-time pocket, dusty brushed drums with muted kick and rim-snare, warm rounded bass, softened vibraphone motif, hazy electric-piano chords and subtle tape texture, Keep the opening sparse and drifting, let the groove settle in during the second verse, widen the chorus with restrained pads and melodic bass, strip back to voice and vibraphone in the bridge, then return for a fuller final chorus and soft instrumental fade, Intimate natural male chest-voice lead, dry and close, minimal vibrato, no falsetto, understated melodic phrasing with a gentle held-note lift, Warm, slightly grainy, spacious mix with subdued highs and a steady low-end
```

#### EXCLUDE

```text
Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Intense, Dramatic
```

#### LYRICS

```text
[Intro]
[Instrumental]

[Verse 1]
[Relaxed male vocal, no harmony]
창가에 빛이 쏟아져
먼지가 천천히 떠다녀
커튼이 바람에 흔들려
나는 그 속에 서 있어

[Bridge 1]
[Chest voice, intimate]
마루에 눕는 오후 햇살
시계 소리마저 멈춘 듯해
이대로 흘러가도 돼

[Chorus]
[Soft belt, no backing vocals]
햇살이 번져가
먼지가 떠다녀
이 순간 여기 머물러
시간은 조용히 가

[Verse 2]
[Groove settles, subtle lift]
바닥에 시간이 내려앉아
그림자가 천천히 길어져
숨결이 피부에 스며들어
조금만 더 가면 무너질 것 같아

[Bridge 2]
[Chest voice, intimate]
손등 위에 남은 오후 햇살
아무 말도 필요 없는 순간
이대로 흘러가도 돼

[Chorus]
[Soft belt, no backing vocals]
햇살이 번져가
먼지가 떠다녀
이 순간 여기 머물러
시간은 조용히 가

[Final Chorus]
[Confident lift, restrained ad-libs, no backing vocals]
햇살이 번져가
먼지가 떠다녀
이 순간 여기 머물러
시간은 조용히 가

[Outro]
[Instrumental, vibraphone motif fades]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 2bdaaa83-7145-4808-b57f-f0b98f7788f0 (https://suno.com/song/2bdaaa83-7145-4808-b57f-f0b98f7788f0)
Suno title after numbering: 8. 먼지 (Lo-Fi Remix)
Lineage status: confirmed_prior_suno_parent_link — original song link confirmed (prior Suno parent link observed)
Original song (Suno): 9. 먼지 (https://suno.com/song/5dd96371-52f1-404b-a7d3-883a59c047c0)
Style record status: confirmed_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 fa54fa6a92f7e23bc36896a34167c42d305a7f3df777342469c4db9fea59cf07); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/2bdaaa83-7145-4808-b57f-f0b98f7788f0.json (sha256 11ab74860c329e420ff13cc447bd203531fbcebb36936f0f61bcfe4cb0064dd9); style-provenance.json tracks[capture 10]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 09. 지금 가는 길

- Timestamp: 27:49
- Repeat Timestamp: 01:23:16
- Filename: `09__지금 가는 길__Relax__Lo-fi R&B__NA.wav`
- Title: 지금 가는 길
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 200.97 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `de257d454d61a3a0dffeb680dac16ba55c7142b68dc3a13a519a968fdcfb6fea`
- Source Title: 지금 가는 길 (Lo-Fi Remix)
- Source Checksum: `438d5140338691f2f79e9076d9f0c428ae67c8214ce514e36be55aa55c0847a3`

#### STYLE

```text
Lo-fi Korean indie R&B, 80BPM, slightly slower head-nodding groove, intimate dusty Rhodes seventh and ninth chords, gentle tape wobble, subtle vinyl texture, deep rounded kick, dry rim-click snare, lightly shuffled hats, warm melodic bass, Begin with a clearly instrumental intro before the original Korean female lead enters; keep verses sparse, let the hooks open wider, and finish with a soft reflective fade, Conversational chest-voice delivery, clear diction, dry upfront vocal, restrained reverb, warm wide mix
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro]
instrumental

[Verse 1]
씻고 누우려던 참에
친구한테 전화가 와
벌써 다들 모였다고
잠깐 얼굴이나 보자고

의자에 걸친 재킷
주머니 속 이어폰
문밖으로 나오니
생각보다 괜찮은 밤

[Pre-Chorus]
이어폰 한쪽을 끼고
듣던 노래를 틀어
서두를 건 없지만
걸음이 조금 빨라져

[Chorus]
나 지금 가는 길
먼저 들어가 있어
맨날 보는 얼굴인데
오늘도 할 말이 많아

나 지금 가는 길
내 자리 하나 남겨
별일 없이 보낸 하루
너희한테 풀어놓게

[Instrumental Break]

[Verse 2]
편의점 앞을 지나다
뭐 좀 사 갈까 물어
아무것도 필요 없대
너나 빨리 오라네

신호를 기다리다가
건너편 창을 보니
누가 먼저 날 봤는지
크게 손을 흔들어

[Pre-Chorus]
이어폰을 빼서 넣고
짧게 답장을 보내
이제 문 앞이라고
전화는 안 해도 돼

[Chorus]
나 지금 가는 길
먼저 들어가 있어
맨날 보는 얼굴인데
오늘도 할 말이 많아

나 지금 가는 길
내 자리 하나 남겨
별일 없이 보낸 하루
너희한테 풀어놓게

[Bridge]
요즘 어떻게 지내
난 뭐, 늘 똑같지
별로 할 말 없다가도
하나씩 생각이 나

누가 먼저 꺼낸 얘긴지
한참 다른 데로 새고
시간 한번 확인하다
휴대폰을 뒤집어 놔

[Final Chorus]
나 지금 가는 길
먼저 들어가 있어
맨날 보는 얼굴인데
오늘도 할 말이 많아

나 지금 가는 길
내 자리 하나 남겨
별일 없이 보낸 하루
너희한테 풀어놓게

[Outro]
아직 괜찮아
조금 더 있다 갈게
그래서 아까 그 얘기
어떻게 됐는데
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 7b0944f7-dddf-483b-b41c-beae8d5fe3ee (https://suno.com/song/7b0944f7-dddf-483b-b41c-beae8d5fe3ee)
Suno title after numbering: 9. 지금 가는 길 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 38d6f86ca3d54647f5dad120527062dec4b127821e8846ecfdca99a2c0fa8de6); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/7b0944f7-dddf-483b-b41c-beae8d5fe3ee.json (sha256 ea97d02b75906b79ecf89d5ec2c35aa82cf7b778dcad55e48194d2102b3535b3); style-provenance.json tracks[capture 4]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 10. 산책

- Timestamp: 31:10
- Repeat Timestamp: 01:26:36
- Filename: `10__산책__Relax__Lo-fi R&B__NA.wav`
- Title: 산책
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 153.09 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `cc7e4c598f25cd0d5b1a0eb93a6cd9c09ffbf0d8ce580cb1905730464a108b2b`
- Source Title: 산책 (Lo-Fi Remix)
- Source Checksum: `a716247ea85596aa19d662ac0c6960c530d6c6c8c53949831a6b1f281aadc654`

#### STYLE

```text
Articulation, Korean Indie Alt R&B, 74 BPM, Eb Major, Clean Electric Guitar-led, supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest voice dominant, No falsetto, Straight tone only, No vibrato, no ad-libs, High register chest voice preferred over falsetto, Tone is nonchalant and effortless, never dramatic, Vocal articulation is critical: clear consonant attack, precise syllable separation, no slurring, no breathy phrasing, Verse2 builds clear tension, Chorus contains a single, unavoidable high-note focal point: short, decisive high register chest note, straight tone, not sustained belting, If the chorus does not reach a high register chest note, the emotional intent is considered failed, Chorus hook-first, repeated identically, Later choruses grow only by arrangement density, Bridge builds every bar, Outro guitar fades, Lead vocal remains single and dominant

Lo-Fi Remix, Modern R&B, clear voice, precise articulation, laidback, Korean Indie Alt R&B, 74 BPM, Eb Major, Clean electric guitar-led, supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle, Male vocal: solid, direct, raw, dry; chest voice dominant, straight tone, no vibrato or ad-libs; nonchalant and effortless, never dramatic, Clear consonant attack and precise syllable separation, Verse 2 builds clear tension, Chorus is hook-first with a short, decisive high-register chest note, not sustained belting; repeated choruses grow only by arrangement density, Single dominant lead vocal, Bridge builds every bar; outro guitar fades
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[intro]
[instrumental]

[verse1]
[Direct male vocal, No harmony]
길가를 거닐어
발끝이 천천히 옮겨가
잎새가 흔들려
나는 그 길에 머물러

[bridge1]
[Chest voice, Intimate]
길가에 내려온 오후 햇살
발끝 소리마저 잦아든 듯해
이대로 걸어가도 돼

[chorus]
[High register chest voice, Straight tone]
발끝이 느려져
걸음은 고르게
이 순간 조금 더 나아가자
발끝은 천천히 가

[verse2]
[Groove locks in, Vocal forward]
신발끈 매어봐
햇살이 조용히 따라 와요
발끝이 길 위에 머물러
나도 이대로 나아가자

[bridge2]
[Chest voice, Intimate]
손등에 남은 작은 먼지알
어떤 길도 끝이 없는 산책
이대로 걸어가도 돼

[chorus]
발끝이 느려져
걸음은 고르게
이 순간 조금 더 나아가자
발끝은 천천히 가

[chorus]
발끝이 느려져
걸음은 고르게
이 순간 조금 더 나아가자
발끝은 천천히 가

[outro]
[instrumental]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 9fe398d7-ed43-4e77-8489-9c3d67a0d657 (https://suno.com/song/9fe398d7-ed43-4e77-8489-9c3d67a0d657)
Suno title after numbering: 10. 산책 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 3. 산책 (https://suno.com/song/9bacafcc-f867-4996-80b8-f34eb797025f)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 379414c238684abd2f665223b5dd5fe34935887369ea4a36fdceb185bcd1eebe); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/9fe398d7-ed43-4e77-8489-9c3d67a0d657.json (sha256 1f7b86fc97fa1f2690660b0d27ac097a97319489242a65f811cbedc1affb4f5f); style-provenance.json tracks[capture 11]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 11. 나도 네가 신경 쓰여

- Timestamp: 33:42
- Repeat Timestamp: 01:29:09
- Filename: `11__나도 네가 신경 쓰여__Relax__Lo-fi R&B__NA.wav`
- Title: 나도 네가 신경 쓰여
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 192.49 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `299cc8ff27b5d073d5cc57e3c9e79b4f474990304a1074f2743d46c99cac52e3`
- Source Title: 나도 네가 신경 쓰여 (Lo-Fi Remix)
- Source Checksum: `7a4502f696ea7b1d9970ccff648ce0d6b71191d95f979924da5eb27fdffbf775`

#### STYLE

```text
Contemporary lo-fi R&B in B Major; clean, centered, upfront female low-chest lead with natural breath detail, close-miked and gently compressed; laid-back, slightly behind-the-beat pocket with subtle swing and imperfect drums; dusty Rhodes 7th and 9th chords with gentle pitch drift, deep rounded kick, dry snare, delicate rim clicks, warm restrained bass; mellow tape wobble, softened highs, subtle vinyl crackle and sampler grit on instruments only, wide stereo keys and tight mono low end; sparse verses, richer harmony and heavier kick in a smooth wider chorus, stripped-back bridge, fuller final chorus
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Verse 1]
무슨 말을 하려던 건지
몇 번이나 나를 보길래
먼저 물어볼까 하다가
네 얘기를 기다렸어

[Pre-Chorus]
여럿이서 얘기할 때도
네 쪽을 보게 되더라
별로 웃긴 말도 아닌데
네가 웃는지 궁금해서

[Chorus]
나도 네가 신경 쓰여
너는 아직 모르는 것 같아
별말 없이 헤어진 날
나도 조금 아쉬웠어

나도 네가 신경 쓰여
집에 와서야 인정했어
오늘 어땠냐고 물으면
난 좀 더 있고 싶었어

[Verse 2]
내가 말한 영화 봤다며
어느 장면이 좋았는지
그 얘기도 듣고 싶지만
기억해 준 게 더 좋았어

[Pre-Chorus]
먼저 연락할까 하다
휴대폰을 내려놨어
네 이름이 화면에 뜨면
반가운 티가 날 것 같아

[Chorus]
나도 네가 신경 쓰여
너는 아직 모르는 것 같아
별말 없이 헤어진 날
나도 조금 아쉬웠어

나도 네가 신경 쓰여
집에 와서야 인정했어
오늘 어땠냐고 물으면
난 좀 더 있고 싶었어

[Bridge]
그냥 편한 사이라기엔
네 앞에선 말을 고르게 돼
괜히 의미 두지 말자 해도
다음에 볼 날을 생각해

[Chorus]
나도 네가 신경 쓰여
너는 아직 모르는 것 같아
별말 없이 헤어진 날
나도 조금 아쉬웠어

나도 네가 신경 쓰여
집에 와서야 인정했어
오늘 어땠냐고 물으면
난 좀 더 있고 싶었어

[Final Chorus]
나도 네가 신경 쓰여
이젠 조금 티를 내도 될까
별일 없는 하루 얘기도
네 얘기라 듣고 싶어

나도 네가 신경 쓰여
네 연락에 한참 웃었어
이번 주는 토요일이 좋아
밥 먹고 커피도 마시자
```

#### META

```text
=== SOURCE RECORD ===
Suno song: c3903598-814e-476d-95a0-f721d2307233 (https://suno.com/song/c3903598-814e-476d-95a0-f721d2307233)
Suno title after numbering: 11. 나도 네가 신경 쓰여 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 73740307c4a99587593557252a2c45da691ae64945a892c04b4d24b38ef91fa9); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/c3903598-814e-476d-95a0-f721d2307233.json (sha256 95155837419c6bf79099a114e1b78df51d79d066da784cb8b3c5297e2c76a0aa); style-provenance.json tracks[capture 5]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 12. 숨

- Timestamp: 36:54
- Repeat Timestamp: 01:32:20
- Filename: `12__숨__Relax__Lo-fi R&B__NA.wav`
- Title: 숨
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 214.81 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `b8ac408883570b2a52104e1bed48e74b9e9454eb40c109c3872d1b483ea46f9e`
- Source Title: 숨 (Lo-Fi Remix)
- Source Checksum: `26d5d84985a5a139c03545e3817a4d53df7f723071cc7c7ef35b44aefbe96585`

#### STYLE

```text
Korean Soft R&B, 76 BPM, Ab Major Rhodes-led, warm synth pad underneath, supportive Soft brush kit, gentle pulse, warm bass Clean mix, intimate atmosphere Female vocal, Soft, Gentle, Chest voice dominant Catchy melodic hook, singable melody Simple but memorable topline Precise articulation, clear consonants Verse: Rhodes + pad, intimate, gentle Pre-Chorus: slight build, anticipation Chorus: catchy melodic hook, repeat identical, easy to hum Bridge: Rhodes and voice only, tender Breakdown: music stops completely, silence, audible breath Outro: short phrase, Rhodes + pad sustain fade Single lead vocal throughout No harmonies, no doubles, no backing vocals Moderate reverb, warm room ambience EQ balanced sound, clean mix

Korean indie R&B, lo-fi bedroom production, slow relaxed pocket, Rhodes-led chords with soft tape-worn texture, warm understated synth pad and rounded bass, brushed minimal drums with a gentle pulse, Keep the verses sparse and close; let the pre-chorus add a subtle lift, then open the chorus into a memorable, hummable hook, Bridge strips back to Rhodes and lead voice, followed by a full-stop breath breakdown and a brief sustained Rhodes outro, Single intimate female chest-voice lead, gentle phrasing, precise Korean consonants, clear articulation, moderate room reverb, soft saturation, warm balanced mix
```

#### EXCLUDE

```text
Rap, Hip-hop, Spoken word, Whisper, Harmonies, Backing vocals, Doubles, Choir, Ad-libs, Runs, Melisma, Falsetto, Bright, Upbeat, Energetic, Fast
```

#### LYRICS

```text
[Intro]
[instrumental — Rhodes + warm pad, 8 bars]

[Verse 1]
[Female, Soft, Chest voice, No harmony]
문 앞에 서면
발걸음이 멈춰져
가방을 내려놓고
숨을 한번 쉬어

[Verse 2]
[Female, Soft, Chest voice, No harmony]
어깨가 무거웠어
하루가 길었어
여기까지 왔으니
이제 괜찮아

[Pre-Chorus]
[Gentle, Building]
번호 누르기 전에
잠깐만 서 있을게

[Chorus]
[Soft belt, Chest voice, No harmony]
숨을 고르면
하루가 내려가
문 앞에 서면
마음이 놓여

숨을 고르면
어깨가 가벼워져
문 열기 전에
잠깐 쉬어갈게

[Interlude]
[instrumental — Rhodes + pad, 8 bars]

[Verse 3]
[Female, Soft, Intimate, Chest voice, No harmony]
안에서 소리가 나
누가 기다려
발소리를 들었나봐
문이 열리려 해

[Verse 4]
[Female, Soft, Chest voice, No harmony]
웃음소리가 들려
따뜻한 냄새가 나
여기가 내 자리야
드디어 왔어

[Pre-Chorus]
[Gentle, Building]
들어가기 전에
한 번만 숨 쉴게

[Chorus]
[Soft belt, Chest voice, No harmony]
숨을 고르면
하루가 내려가
문 앞에 서면
마음이 놓여

숨을 고르면
어깨가 가벼워져
문 열기 전에
잠깐 쉬어갈게

[Bridge]
[Sparse, Warm]
오늘도 수고했어
이제 다 왔어
힘들었던 하루도
여기서 끝이야

[instrumental — Rhodes only, 4 bars]

[Breakdown]
[Music stops — silence]
(deep breath)
후...

[Final Chorus]
[Soft belt, Chest voice, No harmony]
숨을 고르면
하루가 내려가
문 앞에 서면
마음이 놓여

숨을 고르면
어깨가 가벼워져
문 열기 전에
잠깐 쉬어갈게

[Outro]
[Female, Soft, Fading]
문이 열려

[instrumental — Rhodes + pad fades slowly, 8 bars]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 36d296ff-f0af-4b44-a5ad-0bc7cfef0982 (https://suno.com/song/36d296ff-f0af-4b44-a5ad-0bc7cfef0982)
Suno title after numbering: 12. 숨 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 8. 숨 (https://suno.com/song/8ef9a05d-8e05-4e37-a4b6-b6da1e9b2cb0)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 713158dec0280735f58090b06db1afa15787a50f42ed7e6cb0877cf30a98f7da); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/36d296ff-f0af-4b44-a5ad-0bc7cfef0982.json (sha256 8a981a1e390a79e8b23dc66d61dde5b20ba8f812eefe26dab4744a8c63a6d45d); style-provenance.json tracks[capture 12]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 13. 자꾸 네가 신경쓰여

- Timestamp: 40:28
- Repeat Timestamp: 01:35:54
- Filename: `13__자꾸 네가 신경쓰여__Relax__Lo-fi R&B__NA.wav`
- Title: 자꾸 네가 신경쓰여
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 209.89 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `32bf980e612301bfb59074398d72e617bb0aca855c3da1271e652134ea54fff4`
- Source Title: 자꾸 네가 신경쓰여 (Lo-Fi Remix)
- Source Checksum: `d8f4220772e0334bd14eb9799bb3c04589ff36146c57899406be7e85fefe8090`

#### STYLE

```text
Modern indie R&B with a hushed, late-night pocket: muted electric piano voicings over a soft swung beat, rounded sub-bass, crisp close rim clicks, and faint granular room texture, Keep the verses sparse and intimate, let the pre-chorus gain a little harmonic lift, then open the chorus with a wider synth bed and steady bass movement, Strip back to keys and voice for the bridge, then return with a subtly fuller final chorus, Low-chest male Korean croon, relaxed legato phrasing, close-miked and dry with natural breath, gentle tape warmth, restrained reverb, wide instrumental stereo and centered lead vocal
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Verse 1]
너한테 할 말이 있었는데
막상 보면 생각이 안 나
오늘 뭐 했냐는 말 하나
고르다 때를 놓쳐

[Pre-Chorus]
다른 얘기를 하다가도
네 목소리는 잘 들려
나한테 한 말도 아닌데
괜히 고개를 돌려

[Chorus]
자꾸 네가 신경 쓰여
말 걸까 말까 고민하다
별말 없이 헤어지면
그때 할 말이 생겨

자꾸 네가 신경 쓰여
별말 아닌데 또 생각나
너는 어땠는지 궁금해
오늘 나랑 있을 때

[Verse 2]
네가 말한 영화 하나
어젯밤에 찾아봤어
어땠냐고 물어보면
이번엔 할 말이 있어

[Pre-Chorus]
먼저 연락해 볼까
그 정도는 괜찮겠지
짧게 몇 자 적어놓고
한참 그대로 뒀어

[Chorus]
자꾸 네가 신경 쓰여
말 걸까 말까 고민하다
별말 없이 헤어지면
그때 할 말이 생겨

자꾸 네가 신경 쓰여
별말 아닌데 또 생각나
너는 어땠는지 궁금해
오늘 나랑 있을 때

[Bridge]
너는 별생각 없을 수도
그냥 편한 사이일 수도
혼자 앞서가긴 싫은데
다음에 또 보고 싶어

[Chorus]
자꾸 네가 신경 쓰여
말 걸까 말까 고민하다
별말 없이 헤어지면
그때 할 말이 생겨

자꾸 네가 신경 쓰여
별말 아닌데 또 생각나
너는 어땠는지 궁금해
오늘 나랑 있을 때

[Final Chorus]
자꾸 네가 신경 쓰여
이젠 먼저 말을 걸까
별일 없는 하루 얘기도
너랑 조금 더 하고 싶어

자꾸 네가 신경 쓰여
집에 가는 길에 연락해
이번 주에 시간 괜찮으면
우리 둘이 밥이나 먹자
```

#### META

```text
=== SOURCE RECORD ===
Suno song: a1c4a6f1-9773-435c-875d-6a01de45d746 (https://suno.com/song/a1c4a6f1-9773-435c-875d-6a01de45d746)
Suno title after numbering: 13. 자꾸 네가 신경쓰여 (Lo-Fi Remix)
Lineage status: user_declared_direct_creation — made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style
Style record status: user_created_current_style_recorded; assembly mode: current_display_style_for_user_created_song
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (current displayed style of the song 젠 made directly). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 d147155300478dace456e93fb328c1ad045700d773008db15d7fdf0a99c14d9a); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/a1c4a6f1-9773-435c-875d-6a01de45d746.json (sha256 78f7c4e29c6d19bab6ee1be22726321db9b169e91b5d9bfd32122a7d72614f89); style-provenance.json tracks[capture 6]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 14. 물안개

- Timestamp: 43:57
- Repeat Timestamp: 01:39:23
- Filename: `14__물안개__Relax__Lo-fi R&B__NA.wav`
- Title: 물안개
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 138.41 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `9823381af4baf21a0c950b782a9f41a26561bf612879af5875b96531abd989e0`
- Source Title: 물안개 (Lo-Fi Remix)
- Source Checksum: `b99fbf950de3b3a798e447ef8af17653837cecf6652d1d6c8affc8a74b616e1e`

#### STYLE

```text
articulation, Korean Lo-fi R&B, 80 BPM, Eb Major, felt piano-led, soft shaker, hazy ambient pad, cinematic but restrained, wide stereo, Raw vocal, Powerful, Solid, Direct, Dry, Unprocessed, Deep male vocal, mature voice, Chest voice dominant throughout, No falsetto, Strong vocal attack, Verse2 adds tension with stronger dynamics; chorus hits peak with powerful belting and controlled vibrato, Lead vocal remains single and dominant, No harmony, no backing vocals, no doubles, Final chorus adds warmth via piano/pad only; outro felt piano fades into silence

Lo-fi Korean R&B, muted Rhodes chords and softened electric piano, dusty swung drums with brushed snare and subdued kick, warm restrained bass, faint tape hiss and gentle wow, conversational chest-voice lead kept forward and intimate, sparse verses opening into a fuller but still understated chorus, reflective instrumental gaps, mellow filtered mix with rounded transients
```

#### EXCLUDE

```text
Airy, Falsetto, Harmonized, Backing vocals, Whisper, Auto-tune, doubled vocals, choir, vocal layers
```

#### LYRICS

```text
[Intro]
[Instrumental]

[Verse 1]
[Direct vocal, no harmony]
가로등이 번져
젖은 바닥 위로
발자국만 남아
흐린 길의 끝에

[Bridge 1]
[Chest voice]
코트 깃을 세워도
스며드는 안개 속
걸음마다 젖어가
번져버린 발자국

[Chorus]
[Powerful belt, no backing vocals]
가로등이 번져
물안개 속 혼자
지워지지 않아
젖은 밤의 흔적

[Verse 2]
[Direct vocal, no harmony]
차가움이 번져
젖은 소매 위로
입김만이 남아
떨리는 숨 끝에

[Bridge 2]
[Chest voice]
주머니에 손 넣어도
스며드는 냉기 속
가슴까지 젖어와
번져버린 발자국

[Chorus]
[Powerful belt, no backing vocals]
가로등이 번져
물안개 속 혼자
지워지지 않아
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 0908a587-be93-46c5-a8e6-46428f3efba5 (https://suno.com/song/0908a587-be93-46c5-a8e6-46428f3efba5)
Suno title after numbering: 14. 물안개 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 4. 물안개 (https://suno.com/song/014ca2e3-c959-44a4-a372-aad1956acccb)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 00f9aa4babcffb57a7122bf7011054f671f6bee5046b6c84add48fbec81c14a9); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/0908a587-be93-46c5-a8e6-46428f3efba5.json (sha256 a8729132a55c3a19748f021a5bb572e3815d6caa03fe794c18d7ee46168ab00e); style-provenance.json tracks[capture 15]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 15. 약속

- Timestamp: 46:14
- Repeat Timestamp: 01:41:41
- Filename: `15__약속__Relax__Lo-fi R&B__NA.wav`
- Title: 약속
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 214.81 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `d0d301b9c235f9a4604736a95f13b38892e158b52b15f99d9326e06cd7898a05`
- Source Title: 약속 (Lo-Fi Remix)
- Source Checksum: `da9cee948576bea072417556ed2c85cabadb9eb40f0bb478f0b33dd9b4f4e14b`

#### STYLE

```text
Korean Neo-soul R&B, 100 BPM, G minor Rhodes-led, electric bass very dry, layback groove, rim-click, NO 808, Male vocal, Raw, Direct, Dry, Simple melody, Chest voice dominant, No falsetto, no runs, no melisma, Precise articulation, Light room reverb, Clean mix, Verse1: Rhodes chords, sparse bass, confessional, gentle phrasing, Verse2: same contour; last 2 lines rise in intensity, Chorus: catchy singable hook, repeat identical; simple memorable melody, chest voice, Chorus2: bigger by arrangement only; no new vocal layers, Bridge: Rhodes + voice only, builds every bar, Outro: Rhodes fades, synth pad sustain, Single lead vocal throughout, No harmonies, no doubles

Lo-fi Korean indie R&B, gently slowed and deeply laid-back pocket, warm Rhodes chords with softened tape-worn edges, rounded dry electric bass, restrained rim-click and dusty minimal percussion, Preserve the source’s Korean neo-soul character and recognizable melody; intimate, direct, chest-led and unhurried lead vocal, Sparse verses, subtle low-end and texture lift into the repeated hook, bridge strips back to Rhodes and voice before a restrained final chorus, then a soft sustained-pad fade, Close, warm, slightly grainy production with clean vocal focus
```

#### EXCLUDE

```text
Autotune, Vocoder, Choir, Backing vocals, Runs, Melisma, Ad-libs, Rap, Hip-hop, Bright
```

#### LYRICS

```text
[intro]
[instrumental]

[verse1]
[Chest voice, No harmony]
퇴근 알람이 울려
주머니 속 폰을 꺼내
연락처를 내려봐
누구한테 먼저 할까

[pre-chorus]
[Direct vocal, Dry voice]
엄지가 멈칫해
화면만 밝아져
읽씹만 쌓여가는
오늘도 그런 저녁

[chorus]
[Soft belt, Chest voice, No harmony]
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야

[interlude]
[instrumental]

[verse2]
[Chest voice, No harmony]
답장 알림이 울려
괜히 먼저 폰을 열어
미안 오늘은 안 돼
왜 다들 연락이 안 돼

[pre-chorus]
[Direct vocal, Dry voice]
한숨이 새어나
거리만 어두워
읽씹만 쌓여가는
오늘도 그런 저녁

[chorus]
[Soft belt, Chest voice, No harmony]
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야

[bridge]
[Building, sparse]
그래도 내일은 또
누군가 시간 나겠지

[chorus]
[Powerful belt, Chest voice, No harmony]
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야
야 오늘 뭐해, 시간 돼?
한잔 하자 연락 좀 해
다들 바빠 나만 한가해
혼자 걷는 퇴근길이야

[outro]
[instrumental]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 2b2a7a3b-eb6f-4497-a470-2c9133a543eb (https://suno.com/song/2b2a7a3b-eb6f-4497-a470-2c9133a543eb)
Suno title after numbering: 15. 약속 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 2. 약속 (https://suno.com/song/47589b50-571d-4817-abe1-fe907fde4d75)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 c8b46c03835c766bf922ee6de10bd6ad41ba7a93e7755cb47146d5d54faadeee); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/2b2a7a3b-eb6f-4497-a470-2c9133a543eb.json (sha256 139d6299413c337c299c6613121ef9cbb3e009d61ef9ad681f0bcdbbe6647b04); style-provenance.json tracks[capture 8]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 16. 골목

- Timestamp: 49:48
- Repeat Timestamp: 01:45:15
- Filename: `16__골목__Relax__Lo-fi R&B__NA.wav`
- Title: 골목
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 206.77 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `f47287ddb07010b83a7022204b0d831bf0fdd1d366289d6efb50c4a1b9f859fb`
- Source Title: 골목 (Lo-Fi Remix)
- Source Checksum: `0c4a320b3efe7a311448849175b5e77c50f07ea027480b94b8a2504757fdc7bb`

#### STYLE

```text
Korean Slow R&B Ballad, 67 BPM, Db Major Male vocal, Raw, Dry, Unprocessed, Chest voice dominant No falsetto, No runs, No melisma Speech-like phrasing, Narrow melodic range Precise articulation, clear consonants supportive, warm pad texture Minimal drums or drumless verses Soft bass, low presence Moderate reverb, EQ balanced sound, clean mix Verse2 subtle intensity increase by vocal weight only Chorus: longer sustain on hook phrase, no belt Bridge: single guitar line, no solo flourish No harmony, no backing vocals, no doubles Lead vocal remains single and dominant throughout

Lo-fi Korean indie R&B, unhurried pocket groove with softened boom-bap drums and restrained low end; mellow Rhodes chords, muted guitar accents, subtle tape hiss and gentle saturation, Keep the original song’s melodic contour and section flow, with intimate dry chest-voice Korean lead, no harmony layers, Let the arrangement open sparsely, warm gradually through the chorus, dip into a short instrumental passage, then return to the chorus and settle into an understated instrumental outro, Close, soft-edged mix with rounded transients and a lived-in room feel
```

#### EXCLUDE

```text
None
```

#### LYRICS

```text
[Intro]
[Instrumental]

[Verse]
[Chest voice, No harmony]
해가 지고 나면 골목을 걸어요
익숙한 길인데 오늘은 낯설죠

[Verse]
[Direct vocal, Dry voice]
담벼락 그림자가 길어질 때쯤
발자국 소리만 골목에 울려요

[Verse]
[Chest voice]
아무 생각 없이 걷다 보면 좋아요
가로등 불빛이 하나둘 켜지죠

[Verse]
[Direct vocal]
모퉁이를 돌면 바람이 불어와
코끝이 시려와 주머니에 손을 넣어요

[Pre-Chorus]
[Chest voice, No falsetto]
어디로 가는지 몰라도 괜찮아요
그냥 이렇게 걷는 게 좋은 밤이에요

[Chorus]
[Chest voice, No harmony]
천천히 천천히 걸어가요
서두를 것 없이 흘러가요
저 모퉁이 끝에 뭐가 있을까
오늘 밤은 조금 멀리 가볼까요

[Verse]
[Direct vocal, Dry voice]
문 닫은 가게 앞 의자가 보여요
누군가 앉았던 온기가 남았을까요

[Verse]
[Chest voice]
골목 끝 편의점 불빛이 새어나와
잠깐 들를까 하다가 그냥 지나쳐요

[Instrumental]

[Chorus]
[Chest voice, No harmony]
천천히 천천히 걸어가요
서두를 것 없이 흘러가요
저 모퉁이 끝에 뭐가 있을까
오늘 밤은 조금 멀리 가볼까요

[Outro]
[Instrumental]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: aca55231-9e58-469d-b0ce-c29cb767eaa5 (https://suno.com/song/aca55231-9e58-469d-b0ce-c29cb767eaa5)
Suno title after numbering: 16. 골목 (Lo-Fi Remix)
Lineage status: inferred_from_title_and_lyrics — original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)
Original song (Suno): 7. 골목 (https://suno.com/song/d6fc300a-d0d3-4265-aa1c-bb1325283d60)
Style record status: provisional_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 72a6367246a0f0d4511be570543f0508667a69d44796bebf7120e55b2f805c2a); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/aca55231-9e58-469d-b0ce-c29cb767eaa5.json (sha256 1dfd0f46555d20bd036bc2076fedb735b87b96e1920604a40e949143ab64f8a3); style-provenance.json tracks[capture 16]
Audio BPM/key/vocal were not measured; STYLE wording only.
```

### 17. 물결

- Timestamp: 53:14
- Repeat Timestamp: 01:48:41
- Filename: `17__물결__Relax__Lo-fi R&B__NA.wav`
- Title: 물결
- Mood: Relax
- Genre: Lo-fi R&B
- Type: Lo-Fi Remix (see SOURCE RECORD for lineage)
- BPM: unknown
- Key: unknown
- Length: 133.17 s (cut WAV, output/report.json)
- Vocal: unknown (not measured; vocal wording appears only inside STYLE)
- SHA-256: `0e8092270ffdfcf33894a5ff76c20d5b9df4c85e87c7e3277f3ba9baaf00982d`
- Source Title: 물결 (Lo-Fi Remix)
- Source Checksum: `b35070424f7d94907f8d294dbe42e89ff6eecdb6b2df1e7284061c4d1a50e776`

#### STYLE

```text
Korean Indie Alt R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal

Modern Indie R&B, Lo-fi Remastered, Articulation
```

#### EXCLUDE

```text
Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled
```

#### LYRICS

```text
[intro]
[instrumental]

[verse1]
[Direct male vocal, No harmony, Speech-like]
물 위에 떠 있어
햇살이 눈부셔 눈 감아
바람이 불어와
그냥 이대로 있고 싶어

[bridge1]
[Chest voice, Intimate]
물가에 앉아 있어
아무 생각 없이
이대로 괜찮아

[chorus]
[High register chest voice, Straight tone]
물결이 퍼져가
햇살이 번져가
눈 감아도 돼
시간은 천천히 가

[verse2]
[Groove locks in, Vocal forward]
손끝을 담가봐
차갑지 않아 괜찮아
숨을 내쉬어봐
나도 천천히 가라앉아

[bridge2]
[Chest voice, Intimate]
손등에 물방울
말 안 해도 알아
이대로 괜찮아

[chorus] [Chest voice]
물결이 퍼져가
햇살이 번져가
눈 감아도 돼
시간은 천천히 가

[chorus] [Chest voice]
물결이 퍼져가
햇살이 번져가
눈 감아도 돼
시간은 천천히 가

[outro]
[instrumental]
```

#### META

```text
=== SOURCE RECORD ===
Suno song: 5654d747-4921-416f-9b72-755bf27d734a (https://suno.com/song/5654d747-4921-416f-9b72-755bf27d734a)
Suno title after numbering: 17. 물결 (Lo-Fi Remix)
Lineage status: confirmed_suno_parent_link — original song link confirmed (Suno parent link observed)
Original song (Suno): 6. 물결 (https://suno.com/song/480ba65e-5910-4116-b1fd-5d671461b185)
Style record status: confirmed_reconstruction; assembly mode: original_plus_remix
Actual generation input verified: false
STYLE/EXCLUDE above are the recorded Suno display text (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix). They are a documentation reconstruction, not proof of the exact text submitted to Suno.
LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 c439458fea7c4f764bff42c2dae3fd905f531a7d604680ec49660249303c785b); no word or line was edited.
Evidence: SERIES/23-00/production/browser-capture-20261104/suno-ui/5654d747-4921-416f-9b72-755bf27d734a.json (sha256 08025a7635c77497e937e95ad6f5a3865133efa1319b916f0f0d867601dd8303); style-provenance.json tracks[capture 17]
Audio BPM/key/vocal were not measured; STYLE wording only.
```
