# 07:00 running series production

Date: 2026-10-03
Status (2026-10-06): 기존 7곡(02·03·04·13·14·18·19), 1차 선택 9곡(01·05·07·08·12·15·16·17·20), 2차 11B는 보존한다. 젠이 직접 다시 만든 06·09·10은 `My Workspace`의 새 후보이며 채택 미정이다. 현재 WAV 6개(02–07) 중 현행 보존곡에 맞는 것은 02·03·04뿐이다. 전 구간 180 BPM은 미측정이고 phase는 `track_source_draft`다. 다운로드부터 이후 제작은 한도 회복과 젠의 재개 요청 전까지 보류한다.

## 2026-10-06 hold after user remakes

- 11의 현재 보존 ID는 2차 B `ee96c338-2a08-4248-827d-82fc44da3de6`(3:00)이다. 젠이 직접 만든 새 후보는 06 `6155c557-6cc3-448d-a38c-e608401624fc`(2:04), 09 `54688321-7ea2-479f-8e5e-0bf7c94bd2b3`(3:22), 10 `a851a574-8836-40dd-8616-ee6549d3e4a1`(2:25)이다. 세 후보의 STYLE 입력 원문·별도 EXCLUDE·채택·실제 박자는 확인되지 않았다. 과거 10B 삭제는 젠의 보고로만 기록했으며 UI 재조회는 하지 않았다. 자세한 관측은 `input/suno-user-remakes-2026-10-06.json`과 `input/user-remakes-review-2026-10-06.md`에 있다.
- 젠이 다운로드부터 이후 과정은 다운로드 한도가 돌아온 뒤 진행하기로 했다. 한도 회복과 젠의 재개 요청 전에는 브라우저 다운로드·WAV ingest·Final Track Sources 확정·편집/렌더·업로드/릴리스를 자동 시작하지 않는다. 재개 시 현재 선택 ID와 새 세 후보의 위치·채택을 먼저 확인해 그때 범위를 정한다. 업로드에는 별도 명시적 `-wavvy-release` 경계가 적용된다.

## 2026-10-06 latest user decisions and round 2

- 선례: 1차 재지 정글 13의 빠른 쪼개진 드럼·재즈 화성은 사용자가 좋아한 방향이고, 1차 06·09·11 드릴은 사용자가 대체로 마음에 들지 않는다고 했다. 1차 10은 록으로 생성했으나 젠이 재즈로 재요청했다. 1차 기록·원문은 유지한다.
- `[07:00]` UI에서 1차 생존 ID를 조회해 9개 슬롯 01·05·07·08·12·15·16·17·20에 각 한 곡만 남았고 그 ID가 1차 후보 기록과 일치함을 확인했다. 사용자 선택을 기록한 것이며 실제 180 BPM을 인증한 것은 아니다. 06·09·11의 1차 후보는 보이지 않았고, 10B는 남아 있었다. 10B를 임의 삭제하지 않고 10의 결정은 재생성으로 기록했다. 보존 7곡 ID도 UI와 옛 기록이 일치했다.
- 젠이 확정한 이번 새 스타일: 06 빠른 개러지 록, 09 재지 정글, 10 강한 어쿠스틱 재즈/하드 밥, 11 베이스·기타 펑크(funk) 록. 각 STYLE 맨 앞에 엄격한 180 BPM 지속 문장을 넣고 `[Instrumental]`, 신시사이저·808 드릴·90 BPM 하프타임 배제를 지시했다. 새 txt 네 개는 `input/remakes/*_redirection-round2-2026-10-06.txt`; 원본 13개는 불변이다. 4개 `track-prompt` 게이트 PASS는 입력 형식·내용 검사이며 실제 오디오 품질·템포 판정이 아니다.
- Suno Custom Create에서 각 한 번씩 제출했다. UI의 Duration 입력은 네 곡 모두 Custom 3:00, 표시 모델은 V6, 크레딧은 976→936, 작업공간 곡 수는 17→25였다. 새 A/B 여덟 개의 실제 링크·표시 길이는 `input/redirection-round2-review-2026-10-06.md`, 제출 intent·소스 SHA·UI 관측은 `input/suno-redirection-round2-2026-10-06.json`에 있다. 11A는 화면에 2:59로 표시된다. 새 8개는 청취·채택 대기이며 WAV 다운로드·삭제는 없었다. 최종 채택 전 보존 7곡을 포함한 실제 음원이 180 BPM을 전 구간 지속하는지 확인해야 한다. 템포 변화나 90 BPM 하프타임 후보는 채택하지 않는다.

## 2026-10-06 current redirection

- 선례: `SERIES/07-00/input/remakes/13_호흡.txt`의 빠른 쪼개진 드럼·재즈 화성은 젠이 좋아한 방향이다. 그 원문은 신스 베이스·키보드 선율도 담고 있으므로 13 선택 음원은 그대로 두되 신규 jungle 네 곡에서는 피아노·색소폰·비브라폰·기타 선율로 갈라 놓는다. `input/remakes/03_첫 바퀴_round3.txt`는 느린 체감 문제 뒤 연속 러닝 박자를 명시한 선례다. `MASTER/WORKFLOWS.md` §0과 `MASTER/cli/SPEC.md`는 새 txt와 track-prompt 검사를 요구한다.
- 젠이 직접 보존한 7곡은 선택 ID·기존 txt·WAV·manifest를 변경하지 않는다. 교체 번호는 01·05·06·07·08·09·10·11·12·15·16·17·20이다.
- 교체곡 4 jazzy jungle / 4 drill / 5 rock 분배와 슬롯 배치는 이번 생성에 젠이 승인한 배치이며 최종 채택 분포는 아직 미확정이다. 13곡의 STYLE 첫 문장은 엄격한 180 BPM 및 중단 없는 러닝 박자 지시다. 최종 채택은 보존 7곡까지 포함해 실제 음원의 180 BPM 전 구간 지속을 확인한 뒤 판정한다. 미측정을 수치 PASS로 쓰지 않고 템포 변화·90 BPM 하프타임 후보는 채택하지 않는다. 보존 7곡 선택은 확정이나 수치 템포 확인은 미완료다. 신디사이저가 없는 악기 설계와 서로 다른 선율 움직임은 index에 곡별로 적었다.
- 게이트 실측: `input/redirection-2026-10-06/` 하위 폴더의 첫 txt는 내용 검사 전부 PASS였지만 경로 계약 때문에 FAIL했다. 기존 `input/remakes/*.txt` 선례와 게이트 허용 경로에 맞춰 새 파일만 `input/remakes/NN_제목_redirection-2026-10-06.txt`로 옮겼다. 게이트 코드는 변경하지 않았다.
- 젠의 명시 승인 뒤 기존 Suno `[07:00]`에서 교체 13곡을 각 한 번씩 생성해 A/B 후보 26개의 고유 ID·제목·표시 길이·V6를 확인했다. 제출 전 intent와 소스 해시, 제출 뒤 UI 결과는 `input/suno-redirection-2026-10-06.json`에 기록했다. 듣기 링크는 `input/redirection-review-2026-10-06.md`에 있다. 새 음원 다운로드·삭제는 하지 않았다. 02–07 WAV 여섯 개는 그대로 존재하고, 현행 보존 번호에 속하는 WAV는 02·03·04뿐이다. 새 음원 청취·선택과 실제 180 BPM 확인 전에는 Final Track Sources를 확정할 수 없다. 프롬프트 게이트 PASS는 실제 180 BPM 측정이 아니다.

## 2026-10-03 confirmed direction (historical)

- Trigger: explicit `-wavvy-produce` from 젠.
- Time: 07:00, 젠's own exercise hour. Suno workspace must be exactly `[07:00]`.
- Sound: 180 BPM Korean indie electronic for running. Bright synths and quick drums lead; some tracks add firm bass and larger hooks, without turning the full set into dark club music.
- Final vocal direction (2026-10-03 listening correction): instrumental. The earlier sparse Korean lyrics were used for the first 20 submissions, but 젠 heard those songs and decided the running playlist works better without lyrics. Preserve their txt files and candidate IDs as initial-generation history. 젠의 **“2 완료”** 신호 뒤 **03·05·07·08·11·12·15·16·18·20**의 생존 원본 ID를 대조하고 각 원본에서 Suno `... → Remix → Cover`를 실행했다. 각 요청의 가사 칸은 정확히 `[Instrumental]`이었다. 01은 이 요청 밖이다.
- Reference direction: [Paw&Power 180 BPM metronome-synced mix](https://youtu.be/A3psJJwkdSY) for steady step pulse; [달리런 180 BPM running playlist](https://youtu.be/u2eyM-tS6QI) for uninterrupted 20-track momentum, firm low end, and occasional big hook. These descriptions were verified from YouTube metadata; the audio itself has not yet been independently measured. Borrow only broad production principles, never melodies or lyrics.
- No further reference song required: 젠 provided two video references.
- Tempo acceptance (젠의 최종 결정): 180 BPM 러닝감은 젠이 전곡을 귀로 확인해 PASS했다. 숫자 BPM 실측은 필수 조건으로 남기지 않는다. 프롬프트의 180을 실제 측정값으로 표기하지 않는다.
- Listening correction: 젠 found repeated indie dance-pop grooves too loose and asked for stronger moments without breaking the bright 07:00 series identity. Remake 02, 04, 06, 09, 10, 13, 14, 17, and 19 as instrumentals with distinct fast-rhythm lanes; the nine source txt files are under `input/remakes/` and passed `track-prompt`. Immediately before the remakes, `[07:00]` displayed 11 surviving original songs and none of these nine numbers. Do not delete any original without 젠's direction.

## Precedent

- `SERIES/06-00/concept.md`: 110–130 BPM fast lo-fi, instrumental-first morning running; the new series uses indie electronic and an explicitly faster quarter-note pulse. Its first submissions had Korean vocals; final direction is instrumental.
- `SERIES/20-00/concept.md`: after-hours hip-hop workout with hard low end; the new series stays brighter and indie electronic.
- `wavvy.md` 07:00 station says “기상 / 시작, 담담”; target concept must record the energetic running override.
- `MASTER/WORKFLOWS.md` §0.1 and `skills/wavvy-suno-batch/SKILL.md` authorize 20 txt-first drafts and one initial Suno submission per track after this direction feedback.

## Execution (steps 1–4 completed for the initial vocal submissions)

1. Write the `SERIES/07-00/concept.md` brief with explicit 07:00 station override, reference boundary, 20-track arc, and proposed vocal/genre variation. Keep draft track sources out of Final Track Sources.
2. Write 20 distinct `input/tracks/NN_Title.txt` sources. Apply `wavvy-lyricist` to sparse Korean full lyrics, and make Style/Exclude and section cues appropriate to each song. Use short verses, repeating mantras, and extended instrumental passages. Avoid forced lyrical ambition, juvenile slogans, and generic story plots.
3. Write a full-song lyric review artifact for each source, bind its hash and planned bars to the txt, run `track-prompt` and `lyrics-review` gates on all 20, then correct failures and spot-check natural Korean.
4. Before browser use: log user/browser connection choice; use Aside CLI, refresh its guide, verify the active `[07:00]` Suno workspace before every submission. Submit exactly once per track; record each returned candidate's stable ID and observed status in `input/suno-candidates.json`. Stop visibly on an uncertain or failed submission rather than silently retrying.
5. **Completed:** Submitted the nine requested instrumental remakes from `input/remakes/` in `[07:00]`. One Create action per number returned two song IDs, all 18 recorded under `input/suno-remakes.json` with listening links in `input/remake-review.md`. The original 40-ID history remains separate. The STYLEs diversify fast guitar, piano breakbeat, synth-punk, liquid drum and bass, motorik electroclash, jazzy jungle, bass-led breakbeat, melodic electronic post-rock, and guitar-led breakbeat. Every source targets an audible continuous 180-step pulse.
6. **Completed:** At 젠's direction, made **only 02** again with 10's motorik electroclash pulse. `input/remakes/02_파란불_round2.txt` passed `track-prompt`; a single Create action in `[07:00]` used ten credits and returned two rows named `2. 파란불 (2차)`. Both IDs are in `input/suno-remakes-round2.json`, with links in `input/remake-review.md`. The initial 02 pair and all eight other remakes remain unchanged. The first immediate link lookup timed out, so the action was not retried; a later UI snapshot resolved both links.
7. **Completed by listener decision:** 젠이 최종 20곡의 러닝 박자를 귀로 확인하고 번호별 한 곡씩 남겼다. 수치 BPM은 측정하지 않았으므로 178–182 BPM 실측 통과라고 표기하지 않는다.
8. **Completed:** After 젠 said “2 완료,” used Aside CLI in `[07:00]` to verify the current surviving source ID for **03·05·07·08·11·12·15·16·18·20**. Opened each source's `... → Remix → Cover`, overwrote the prior form with that source, replaced lyrics with exactly `[Instrumental]`, and clicked Create once per number. Each produced two V6 COVER rows. The source-to-cover IDs are in `input/suno-covers.json`; listening links are in `input/cover-review.md`. No source or candidate was deleted. Only chosen eligible instrumentals enter audio ingest and final source archiving. `-wavvy-release` is a separate later command.
9. **Completed:** After 젠 reported the workspace at 20 songs, verified the Suno `[07:00]` page displayed exactly one title for each number 1–20. At 젠's next request, wrote a stronger 03 source in `input/remakes/03_첫 바퀴.txt`; `track-prompt` passed. Submitted it once with `[Instrumental]` in `[07:00]`, received two V6 links, and recorded both in `input/suno-remakes-03.json`. Workspace count became 22 because Suno creates an A/B pair. Do not treat the old 03 Cover PASS as acceptance of these new candidates.
10. **Completed:** 젠이 03 2차를 “느려”라고 판정했다. 10번의 빠른 모토릭 드럼 방향을 써서 `input/remakes/03_첫 바퀴_round3.txt`를 작성하고 `track-prompt` PASS 뒤 `[07:00]`에서 Create를 한 번 실행했다. 새 V6 A/B ID는 `input/suno-remakes-03-round3.json`에 기록했다. 젠은 “3통과”로 3차 버전을 청취 PASS했고, A (`fad9fc49-9b35-4f10-aa76-f62ddd9cf10c`)를 남기고 B를 삭제했다. 03 실제 WAV 길이는 2:23.72로 3분 목표보다 짧지만 최종 채택곡이다. 수치 BPM은 측정하지 않았다.

## Verification and limits

- Prompt and lyric gates check source contracts and review evidence, not generated sound.
- Suno currently creates two songs by default for one submission; this occurred on all 20 initial requests. Record both IDs under one submission, and inspect how many results each later Cover action returns.
- Source BPM is a target. Do not claim a measured 178–182 BPM result until inspecting audio.
- The ten Cover requests were submitted in Cover mode with source art/name, `[Instrumental]` in the lyrics box, and Save to `[07:00]` shown before each click. Their 20 links were reconciled by excluding the ten original IDs from same-title search results. 젠은 10곡의 Cover 결과 전체를 청취 PASS했다. 번호별 A/B 최종 선택 및 자동 무가사·길이·178–182 BPM 측정은 하지 않았다. 03 A는 Suno 직접 페이지에 약 1:01로 표시되어 길이 목표에 못 미친다.
- No commit or push without an explicit record request.
- Browser selection check: 젠's carried choice is Aside / CLI; actual entry tool is `aside repl` for direct Suno DOM and screenshot inspection. `aside --update`, `aside guide`, and `aside guide repl` were run on 2026-10-03; no different browser connection is authorized. First Suno call and created tab IDs must be logged with candidate work.
- First browser call: `aside repl` attached the pre-existing Suno tab `54FF6C5F730DA60A84CB230EECC957E7`. Created and selected `[07:00]` in that tab. Observed URL `https://suno.com/create?wid=dee79f9f-f6d1-47be-8d91-2a88fafaa265`, Save to `[07:00]`, and `No songs found` before submission.
- Completed 20 distinct, preflight-checked Create actions in that workspace. Each returned two unique `/song/` links; all 40 IDs are recorded immediately under `SERIES/07-00/input/suno-candidates.json`. One initial submission per track, no credit-using retry. The first two submissions each showed a 10-credit drop; the final balance was not checked.
- Audio selection is complete for 01–20 in `input/suno-selected.json`. The Suno download dialog displayed 7 Pro downloads remaining before this pass. 젠이 01을 MP3/M4A로 다운로드하고 Codex가 02–07을 WAV로 받았다. 02–07은 선택 ID·48 kHz 16-bit PCM stereo·원본/복사본 SHA-256을 `input/download-manifest.json`에 기록했다. 01 및 08–20 WAV 수집은 남아 있다. Suno's official policy says one distinct song uses one download regardless of format: https://help.suno.com/en/articles/13926209 .
- A download-free browser playback probe captured candidate 20B's 30–42 second low-frequency envelope and suggested approximately 92–94 BPM; it is a provisional warning, not a full-song tempo verdict. Two attempts to navigate and capture a second candidate failed (`[role=tablist]` not yet present, then Aside `Cannot find context with specified id`). Following the anti-spiral rule, automated tempo probing stopped pending a revised method/decision. No candidate is marked 180 BPM eligible.
