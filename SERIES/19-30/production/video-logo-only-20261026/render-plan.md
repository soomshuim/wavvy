# 19:30 logo-only video render plan — 2026-10-26

Status: controller resumed video execution after160 independent review CLEAN. Image-role guard passes. Run30-second preview and inspect it before full render.

## User direction and input roles

- Latest user correction: “지난번에도 실수 했는데 영상에는 썸네일을 그대로 쓰지마. 생성한 4K 이미지를 써” and “wavvy 로고만 박힌 버전을 써.” This corrects the controller’s earlier mistaken interpretation that thumb.jpg should be the video input; that was not a user instruction.
- Controller directly viewed and confirmed the existing r4 logo-only image. `input/video-background.png` is an exact copy of `production/thumbnail-revision-20261026-r4/thumb-editable.png`: RGB3840×2160;3,314,371bytes;SHA256`8c8a7583db186719cd9f07f13b1756299096a69be12049821609bb1f516bf78e`. Background, runner and upper-left Wavvy logo remain; Running Mix/BPM text is absent. No new image synthesis or editing.
- Video image: `SERIES/19-30/input/video-background.png` only.
- YouTube thumbnail: user-owned `SERIES/19-30/input/thumb.jpg`; editable user source `input/thumb.psd`. These are preserved separately and are not video inputs.
- User “이건 규칙으로 하네스에 박아둬.” is assigned to a separate worker; this production task does not modify MASTER or wavvy_harness.

## Planned render contract

Precedent: `SERIES/07-00/production/render-user-thumbnail-20261024.py` and its actual validated video record. Use the closed final160 AAC `SERIES/19-30/output/mix-160-20261026/continuous-mix-1930-160-repeat2.m4a`, SHA256`35aa3d44f9c7d50e0a994664e819c3ae34ce9dbe7aa6fbcb098e69c7c7b9f0f7`, with the40-entry `production/mix-160-20261026/timeline.json`. Actual PCM extent reported by the audio worker is318,568,444samples/6,636.842583333s. Existing20-track sequence already runs twice; additional repeats0. The user said “160 통과. 영상 만들어”.

Execution:30-second preview, then full static4K H.264 video (3840×2160,libx264 medium,CRF18,stillimage,1fps), final AAC copied once without re-encoding, mixing or normalization. Do not crop, add text, overlay the thumbnail, or change the approved image. Retain40 actual timeline chapter starts. Keep separate production commands, source/output SHA values, logs and validation; do not relabel160/capture evidence as the180/reacquisition contract.

Validation: input hashes unchanged; full AAC packet payload and timing identical; one H.264 video stream and one AAC48kHz stereo stream;40 chapter titles/start times match the actual timeline within0.5ms; final video frame rounding less than1frame; full A/V decode; beginning/middle/end frames visually checked against the video background. Source audio length is preserved, except video-only final-frame rounding.

Title is finalized by the latest user Electronica wording; the worker prepares description/CSV, and the controller owns upload. No upload, staging, commit or push in this video task.

## Final render status — 2026-10-26

30초 미리보기와 로고 전용 본편을 완료했다. 본편은 3840×2160 H.264·1 fps, 6,637초다. 최종 160 AAC를 패킷 변경 없이 복사했고 40개 챕터·전체 디코딩·시작/중간/끝 실제 프레임 확인을 완료했다. 추가 반복·새 이미지 합성은 없다. 정식 release 검사와 독립 검토 뒤 업로드는 컨트롤러가 실행한다.
