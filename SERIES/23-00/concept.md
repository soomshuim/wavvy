# 23:00 Relax Alternative R&B / Lo-fi R&B

Version: 0.2
Last Updated: 2026-11-02

## Series Status

- **Status**: Listening selection in progress. 11 of 20 are decided: the nine existing Lo-Fi Remixes plus 10 귤 (candidate B, 「귤 통과」「귤은 B」) and 20 포근히 (candidate B, 「포근히 통과」「포근히 B」), both from the first generation round. Tracks 11–19 were rewritten (type-original lyric template + original song style + `Lo-fi Remix`) and regenerated once each on 2026-11-02 (round 2, 18 candidates, all complete). Their round-1 candidates are kept in the ledger. No audio file, artwork, or upload exists yet. Exact candidate IDs and decisions: `input/suno-candidates.json`.
- **Time Slot**: 23:00.
- **Genre Lanes**: relax alternative R&B, lo-fi R&B.
- **Track Count**: 20 songs: nine existing Lo-Fi Remixes made by 젠 from earlier songs and 11 new songs.
- **Numbering**: temporary. 젠: 「넘버링은 나중에 일괄로 할게」. The Track Map numbers and txt file numbers change when 젠 numbers all 20 songs at once.
- **Suno workspace**: `[23:00]` (`f578d3c2-f43f-462e-8e05-44d022edd480`) — https://suno.com/create?wid=f578d3c2-f43f-462e-8e05-44d022edd480
- **Waiting for 젠**: listening results for the round-2 candidates of Tracks 11–19 (젠 2026-11-02: 「나는 내일 검수결과 알려줄게」). For each track: keep A, keep B, or reject (rejects are rewritten and regenerated only for that track).
- **Unexplained**: Suno credits were 646 after round 1 and 636 at the start of round 2; no agent submission accounts for that 10-credit use (observed, not attributed).
- **Current artifacts**: this file; 20 track sources in `input/tracks/` (earlier drafts in `input/source-history/`); candidate ledger `input/suno-candidates.json`; generation evidence `input/validation/2026-11-01-generation/` and `input/validation/2026-11-02-regeneration/`; lyric records `.ai/lyrics/2026-11-01_23-00_*`; workspace observation `.ai/research/2026-11-01-2300-nine-tracks/`; original-style research `.ai/plans/2026-11-02-2300-original-styles.{json,md}` and final values `.ai/plans/2026-11-02-2300-final-styles.json`.

## Confirmed Decisions (젠, 2026-11-01)

- **Song plan**: 20 songs = the nine existing lo-fi remixes + 11 new songs. 젠: 「url에서 9곡의 가사 컨셉과 특징, 스타일 프롬프트(그대로 활용)를 각 타입 별로 참고해서 나머지 11곡을 새로 만들어야해.」 The nine styles all differ, so each remix is one type (nine types, see `## Type Styles`).
- **물결 type**: 젠: 「물결만 원본 트랙의 스타일 프롬프트 + Modern Indie R&B, Lo-fi Remastered, Articulation 를 붙여줘.」 and 「- 붙은 스타일은 exclude인거 알지?」 The `‑` items of the supplied original are therefore EXCLUDE, not STYLE.
- **Thirteen EXCLUDE items**: asked whether to keep all 13 despite the 8-item budget, 젠 chose 「13개 모두 유지 (추천)」. The track-prompt gate records this as a source-bound exception (`## Series Overrides`).
- **Missing tempo, key, vocal gender**: 젠 chose 「선례처럼 끝에 덧붙이기」. A new song's STYLE is its type's new-song STYLE (b) plus, only for the items the type text lacks, `, NN BPM, X Major|Minor, male|female vocal` at the end. Precedent: `.ai/lyrics/2026-10-02_17-00_12_서점-full-draft.md` Source Map.
- **Reuse with judgment**: 젠: 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」 — words that only make sense for a remix are removed from the new-song STYLE (b). The original text (a) is kept verbatim beside it. Edits are listed per type.
- **Reference**: the nine existing remixes in the workspace are the reference. No external reference song was supplied.
- **Language**: Korean lyrics.
- **Lyric direction for new songs**: warm longing — more faint and warm than sad, a relaxing comfort drawn from old memories, concrete mood and sensory detail. Titles are one Korean word (noun, adjective, or adverb).
- **Browser**: ego lite through the `ego-browser` CLI (`MASTER/ai/RUNTIME_RULES.md` Browser Connection).

## Series Overrides

- **EXCLUDE budget (type-scoped)**: `MASTER/style/STYLE.md` §3 caps EXCLUDE at 8 items. The 물결 type keeps the 13 items 젠 supplied. A new-song txt may exceed 8 only with the header lines `Style Type: 물결` and `Exclude Source: user-supplied type style`, and only when its EXCLUDE matches the 물결 `- EXCLUDE:` line below in items and order. Every other type has an empty EXCLUDE and stays within the budget.
- **Vocal and language defaults**: no override of the channel defaults in `wavvy.md` is declared. If a type style conflicts with a channel default when a new song is designed, record a track-scoped exception at that time.
- **Remix source records**: `input/tracks/01`–`09` keep the workspace display text unedited, including wording that only makes sense for a remix. They are records of existing songs; the new-song edits in `## Type Styles` do not apply to them, and the new-prompt gate is not applied retroactively to them (`MASTER/WORKFLOWS.md` §1).
- **New-song lyric criterion (젠, 2026-11-01) — 대체됨 (2026-11-02, see `Lyric template` below; kept as history)**: 새 곡 가사: 한 줄 약 5~8글자, 후렴은 짧은 훅을 되풀이(원곡 방식). Rows above 10 syllables are rare; the Chorus opens and closes on the hook and returns in the same shape each time. 젠: 「원곡들 가사를 보면, 후렴은 반복적이고 전체적으호 문장이 길지 않아」. The Chorus hook should be easy to sing after one hearing (parallel rows, matching endings, repeated words, the title word, 3-4 syllable beats). 젠: 「전반적으로 후렴이 중독성이 약하네」. A new song that 젠 rejects after listening (예: 「라디오 탈락」) is rewritten to this criterion and regenerated; the earlier version is kept in `input/source-history/2026-11-01-before-short-lyrics/`.
- **Lyric template (젠, 2026-11-02)**: Tracks 11–19 are rewritten on the lyrics of their type's original song (`.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → the type's `lyrics_full`): the same number of non-blank lines in the same order, the same section-tag lines word for word, the same syllable count on every sung line, and the same repeated lines; only the content changes. 젠: 「아니 ㅜㅜㅜㅜ 야 기존 곡 가사 글자 수 그대로 내용만 바꿔」. This replaces the earlier short-line criterion above. The earlier versions are kept under `input/source-history/`. Tool: `.ai/plans/2026-11-01-2300-template-check.py`.
- **Original style (젠, 2026-11-02)**: Tracks 11–19 use the original song's STYLE, not the 23:00 assembly in `## New Song Style Assembly` (that section now applies to Tracks 10 and 20 only). STYLE = `Lo-fi Remix, ` + the original STYLE verbatim; only three kinds of edits are allowed and each is listed per type in `## Original Styles`: (a) the genre words alternative / Alt / Modern R&B are removed, (b) an exclusion line inside the original STYLE is moved to EXCLUDE, (c) an instruction that only makes sense for the original lyrics is removed (smallest range, original and edited text both kept). Tempo, key and vocal gender stay as in the original (여름밤·벚꽃·그네 = male), and EXCLUDE is the original's list. 젠: 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」, 「템포도 좀 쳐져」 → 「원곡 BPM 그대로」, 「원곡대로 남성」, 「- 붙은 스타일은 exclude인거 알지?」, 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」, 「Lo-fi remix는 붙여야해 안전빵이야」. A txt in this mode declares `Style Type: <type>` and `Style Source: user-supplied original style`; `gate --stage track-prompt` then skips the 900-character STYLE and 8-item EXCLUDE budgets only when STYLE and EXCLUDE equal that type's `## Original Styles` entry (`MASTER/style/STYLE.md` §3). The 물결 `Exclude Source: user-supplied type style` exception above stays unchanged for manuscripts that were already generated and for reproducing their history.

## Type Styles

Each type has two STYLE entries. **(a) 원문 STYLE** is the workspace display text exactly as observed (for 물결, 젠's original plus the three words he specified). **(b) 새 곡용 STYLE** is what a new song of that type starts from; only the edits listed under it were made. Character counts are Unicode characters including spaces. The `- EXCLUDE:` line is read by the track-prompt gate: keep exactly one per type and keep the heading text equal to the type name.

Values are display text from 2026-11-01, not proof of the exact generation input. The workspace did not show an Exclude field for any song.

### 먼지

- Suno ID (작업공간 Lo-Fi Remix): `2bdaaa83-7145-4808-b57f-f0b98f7788f0` — https://suno.com/song/2bdaaa83-7145-4808-b57f-f0b98f7788f0
- 화면에 표시된 원곡: Remix of "9. 먼지" (`5dd96371-52f1-404b-a7d3-883a59c047c0`) — https://suno.com/song/5dd96371-52f1-404b-a7d3-883a59c047c0
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `먼지`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 male
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`

**(a) 원문 STYLE** — 694자, sha256 `51b2076990d879df87e27b5f7d79a9f3f8356cf1f9f9be5cfa7b681fb2e87246`

```text
Lo-fi modern R&B, Korean indie alt-R&B, relaxed half-time pocket, dusty brushed drums with muted kick and rim-snare, warm rounded bass, softened vibraphone motif, hazy electric-piano chords and subtle tape texture, Keep the opening sparse and drifting, let the groove settle in during the second verse, widen the chorus with restrained pads and melodic bass, strip back to voice and vibraphone in the bridge, then return for a fuller final chorus and soft instrumental fade, Intimate natural male chest-voice lead, dry and close, minimal vibrato, no falsetto, understated melodic phrasing with a gentle held-note lift, Warm, slightly grainy, spacious mix with subdued highs and a steady low-end
```

**(b) 새 곡용 STYLE** — 694자, sha256 `51b2076990d879df87e27b5f7d79a9f3f8356cf1f9f9be5cfa7b681fb2e87246`

편집 없음 (원문 (a)와 같다).

```text
Lo-fi modern R&B, Korean indie alt-R&B, relaxed half-time pocket, dusty brushed drums with muted kick and rim-snare, warm rounded bass, softened vibraphone motif, hazy electric-piano chords and subtle tape texture, Keep the opening sparse and drifting, let the groove settle in during the second verse, widen the chorus with restrained pads and melodic bass, strip back to voice and vibraphone in the bridge, then return for a fuller final chorus and soft instrumental fade, Intimate natural male chest-voice lead, dry and close, minimal vibrato, no falsetto, understated melodic phrasing with a gentle held-note lift, Warm, slightly grainy, spacious mix with subdued highs and a steady low-end
```

### 산책

- Suno ID (작업공간 Lo-Fi Remix): `9fe398d7-ed43-4e77-8489-9c3d67a0d657` — https://suno.com/song/9fe398d7-ed43-4e77-8489-9c3d67a0d657
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `산책`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 74 · 조성 Eb Major · 성별 male
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): 없음 (BPM·조성·성별이 모두 STYLE에 있음)

**(a) 원문 STYLE** — 659자, sha256 `9d4ea3c73134fe61679382dc6ce62bda49413e7093de270d61692194c2c80a93`

```text
Lo-Fi Remix, Modern R&B, clear voice, precise articulation, laidback, Korean Indie Alt R&B, 74 BPM, Eb Major, Clean electric guitar-led, supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle, Male vocal: solid, direct, raw, dry; chest voice dominant, straight tone, no vibrato or ad-libs; nonchalant and effortless, never dramatic, Clear consonant attack and precise syllable separation, Verse 2 builds clear tension, Chorus is hook-first with a short, decisive high-register chest note, not sustained belting; repeated choruses grow only by arrangement density, Single dominant lead vocal, Bridge builds every bar; outro guitar fades
```

**(b) 새 곡용 STYLE** — 659자, sha256 `9d4ea3c73134fe61679382dc6ce62bda49413e7093de270d61692194c2c80a93`

편집 없음 — 젠 2026-11-01 「Lo-fi remix는 붙여야해 안전빵이야. 현재버전들이 잘나온 이유로 보고있어」로 앞선 제거(`Lo-Fi Remix, ` → `Lo-Fi, `)를 취소했다 (원문 (a)와 같다).

```text
Lo-Fi Remix, Modern R&B, clear voice, precise articulation, laidback, Korean Indie Alt R&B, 74 BPM, Eb Major, Clean electric guitar-led, supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle, Male vocal: solid, direct, raw, dry; chest voice dominant, straight tone, no vibrato or ad-libs; nonchalant and effortless, never dramatic, Clear consonant attack and precise syllable separation, Verse 2 builds clear tension, Chorus is hook-first with a short, decisive high-register chest note, not sustained belting; repeated choruses grow only by arrangement density, Single dominant lead vocal, Bridge builds every bar; outro guitar fades
```

### 숨

- Suno ID (작업공간 Lo-Fi Remix): `36d296ff-f0af-4b44-a5ad-0bc7cfef0982` — https://suno.com/song/36d296ff-f0af-4b44-a5ad-0bc7cfef0982
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `숨`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 female
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`

**(a) 원문 STYLE** — 609자, sha256 `5edc24b267878bcf0287214315c8ce75f2046654dcd1c15ce1584999511ea4f2`

```text
Korean indie R&B, lo-fi bedroom production, slow relaxed pocket, Rhodes-led chords with soft tape-worn texture, warm understated synth pad and rounded bass, brushed minimal drums with a gentle pulse, Keep the verses sparse and close; let the pre-chorus add a subtle lift, then open the chorus into a memorable, hummable hook, Bridge strips back to Rhodes and lead voice, followed by a full-stop breath breakdown and a brief sustained Rhodes outro, Single intimate female chest-voice lead, gentle phrasing, precise Korean consonants, clear articulation, moderate room reverb, soft saturation, warm balanced mix
```

**(b) 새 곡용 STYLE** — 609자, sha256 `5edc24b267878bcf0287214315c8ce75f2046654dcd1c15ce1584999511ea4f2`

편집 없음 (원문 (a)와 같다).

```text
Korean indie R&B, lo-fi bedroom production, slow relaxed pocket, Rhodes-led chords with soft tape-worn texture, warm understated synth pad and rounded bass, brushed minimal drums with a gentle pulse, Keep the verses sparse and close; let the pre-chorus add a subtle lift, then open the chorus into a memorable, hummable hook, Bridge strips back to Rhodes and lead voice, followed by a full-stop breath breakdown and a brief sustained Rhodes outro, Single intimate female chest-voice lead, gentle phrasing, precise Korean consonants, clear articulation, moderate room reverb, soft saturation, warm balanced mix
```

### 이름

- Suno ID (작업공간 Lo-Fi Remix): `4708df3d-6f0a-4602-bea4-ccb734cf03db` — https://suno.com/song/4708df3d-6f0a-4602-bea4-ccb734cf03db
- 화면에 표시된 원곡: Remix of "9. 이름" (`73330746-1b39-4cc4-8ff5-f2d3d06aa882`) — https://suno.com/song/73330746-1b39-4cc4-8ff5-f2d3d06aa882
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `이름`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 없음
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`, `male|female vocal`

**(a) 원문 STYLE** — 505자, sha256 `e997aca91688c8de6e812f44855266b4356c65e2ab002ff42036421fec63b494`

```text
Lo-fi indie R&B, relaxed half-time pocket with soft swung drums, muted electric piano chords, rounded bass, faint tape hiss and intimate close-miked Korean lead vocal, Keep consonants crisp and syllables clearly separated, use measured chest-voice phrasing with natural breaths, Begin sparse, add warm guitar and subtle harmonic color through the chorus, pull back for the bridge, then return with a gently fuller final chorus and an understated outro, Soft saturation, dry vocal up front, narrow warm mix
```

**(b) 새 곡용 STYLE** — 505자, sha256 `e997aca91688c8de6e812f44855266b4356c65e2ab002ff42036421fec63b494`

편집 없음 (원문 (a)와 같다).

```text
Lo-fi indie R&B, relaxed half-time pocket with soft swung drums, muted electric piano chords, rounded bass, faint tape hiss and intimate close-miked Korean lead vocal, Keep consonants crisp and syllables clearly separated, use measured chest-voice phrasing with natural breaths, Begin sparse, add warm guitar and subtle harmonic color through the chorus, pull back for the bridge, then return with a gently fuller final chorus and an understated outro, Soft saturation, dry vocal up front, narrow warm mix
```

### 마음 밖

- Suno ID (작업공간 Lo-Fi Remix): `17a24019-4412-4443-b4e7-6d305d539958` — https://suno.com/song/17a24019-4412-4443-b4e7-6d305d539958
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `마음 밖`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 female
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`

**(a) 원문 STYLE** — 539자, sha256 `5273a4afb7c36b8dd3a78683ca4948f88812e25369cb2d3fc07a7f75b9de2536`

```text
Korean indie R&B, lo-fi remix, relaxed half-time pocket with softened kick and dry rim clicks, rounded subdued bass, muted Rhodes and dusty piano fragments, gentle tape saturation and restrained room texture, Keep verses close and sparse, let the choruses widen subtly with filtered keys and soft pad support, then ease into a worn instrumental fade, Forward intimate female lead, warm husky chest voice, clear Korean articulation, conversational phrasing, natural breaths, restrained vibrato; dry close vocal with minimal pitch correction
```

**(b) 새 곡용 STYLE** — 539자, sha256 `5273a4afb7c36b8dd3a78683ca4948f88812e25369cb2d3fc07a7f75b9de2536`

편집 없음 — 젠 2026-11-01 「Lo-fi remix는 붙여야해 안전빵이야. 현재버전들이 잘나온 이유로 보고있어」로 앞선 제거(`lo-fi remix,` → `lo-fi,`)를 취소했다 (원문 (a)와 같다).

```text
Korean indie R&B, lo-fi remix, relaxed half-time pocket with softened kick and dry rim clicks, rounded subdued bass, muted Rhodes and dusty piano fragments, gentle tape saturation and restrained room texture, Keep verses close and sparse, let the choruses widen subtly with filtered keys and soft pad support, then ease into a worn instrumental fade, Forward intimate female lead, warm husky chest voice, clear Korean articulation, conversational phrasing, natural breaths, restrained vibrato; dry close vocal with minimal pitch correction
```

### 물안개

- Suno ID (작업공간 Lo-Fi Remix): `0908a587-be93-46c5-a8e6-46428f3efba5` — https://suno.com/song/0908a587-be93-46c5-a8e6-46428f3efba5
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `물안개`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 없음
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`, `male|female vocal`

**(a) 원문 STYLE** — 374자, sha256 `76ce8dc13459fd15fa0e47c177ba0f1dd944da1b2daf4a284ad8c9c613af737f`

```text
Lo-fi Korean R&B, muted Rhodes chords and softened electric piano, dusty swung drums with brushed snare and subdued kick, warm restrained bass, faint tape hiss and gentle wow, conversational chest-voice lead kept forward and intimate, sparse verses opening into a fuller but still understated chorus, reflective instrumental gaps, mellow filtered mix with rounded transients
```

**(b) 새 곡용 STYLE** — 374자, sha256 `76ce8dc13459fd15fa0e47c177ba0f1dd944da1b2daf4a284ad8c9c613af737f`

편집 없음 (원문 (a)와 같다).

```text
Lo-fi Korean R&B, muted Rhodes chords and softened electric piano, dusty swung drums with brushed snare and subdued kick, warm restrained bass, faint tape hiss and gentle wow, conversational chest-voice lead kept forward and intimate, sparse verses opening into a fuller but still understated chorus, reflective instrumental gaps, mellow filtered mix with rounded transients
```

### 골목

- Suno ID (작업공간 Lo-Fi Remix): `aca55231-9e58-469d-b0ce-c29cb767eaa5` — https://suno.com/song/aca55231-9e58-469d-b0ce-c29cb767eaa5
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `골목`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 없음 · 조성 없음 · 성별 없음
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `NN BPM`, `X Major|Minor`, `male|female vocal`
- 메모: 원문 STYLE에 `Keep the original song’s melodic contour and section flow`가 있다. 원문(a)은 그대로 두고, 새 곡용(b)에서만 뺀다.

**(a) 원문 STYLE** — 562자, sha256 `694b092d5f2cdcf92e366ed8fa21245276e19647c248d7668f5e2d852ad21b89`

```text
Lo-fi Korean indie R&B, unhurried pocket groove with softened boom-bap drums and restrained low end; mellow Rhodes chords, muted guitar accents, subtle tape hiss and gentle saturation, Keep the original song’s melodic contour and section flow, with intimate dry chest-voice Korean lead, no harmony layers, Let the arrangement open sparsely, warm gradually through the chorus, dip into a short instrumental passage, then return to the chorus and settle into an understated instrumental outro, Close, soft-edged mix with rounded transients and a lived-in room feel
```

**(b) 새 곡용 STYLE** — 498자, sha256 `92201adc347d5adfe49b0c74bea7129c06775fde05333c559b86b0f3124cd1cc`

편집: `Keep the original song’s melodic contour and section flow, with intimate dry chest-voice Korean lead, no harmony layers` → `Intimate dry chest-voice Korean lead, no harmony layers`. 다른 단어·순서는 바꾸지 않았다. 근거: 젠 2026-11-01 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」.

```text
Lo-fi Korean indie R&B, unhurried pocket groove with softened boom-bap drums and restrained low end; mellow Rhodes chords, muted guitar accents, subtle tape hiss and gentle saturation, Intimate dry chest-voice Korean lead, no harmony layers, Let the arrangement open sparsely, warm gradually through the chorus, dip into a short instrumental passage, then return to the chorus and settle into an understated instrumental outro, Close, soft-edged mix with rounded transients and a lived-in room feel
```

### 물결

- Suno ID (작업공간 Lo-Fi Remix): `5654d747-4921-416f-9b72-755bf27d734a` — https://suno.com/song/5654d747-4921-416f-9b72-755bf27d734a
- 화면에 표시된 원곡: Cover of "6. 물결" (`480ba65e-5910-4116-b1fd-5d671461b185`) — https://suno.com/song/480ba65e-5910-4116-b1fd-5d671461b185
- 출처: 젠이 채팅에 붙여 준 원본 스타일에서 `‑` 항목 13개를 뺀 앞부분 + `, Modern Indie R&B, Lo-fi Remastered, Articulation` (젠 지시). 작업공간 표시 스타일(185자: `Modern Indie R&B, Lo-fi Remastered, Articulation` + `‑` 항목 13개)과 다르다.
- 원문에 적힌 BPM·조성·성별: BPM 74 · 조성 A Major · 성별 male
- EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): 없음 (BPM·조성·성별이 모두 STYLE에 있음)
- 메모: 새 곡 중 이 타입을 쓰는 txt는 머리말에 `Style Type: 물결`과 `Exclude Source: user-supplied type style`을 적는다. `gate --stage track-prompt`는 이때만 EXCLUDE 8개 초과를 통과시키며, 위 `- EXCLUDE:` 줄과 항목·순서가 정확히 같아야 한다 (`MASTER/style/STYLE.md` §3).

**(a) 원문 STYLE** — 677자, sha256 `dbdb3ee1f7ce2c64b687df191c8a9c740dd35b330e67712ff4ea645e95b0f217`

```text
Korean Indie Alt R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal, Modern Indie R&B, Lo-fi Remastered, Articulation
```

**(b) 새 곡용 STYLE** — 677자, sha256 `dbdb3ee1f7ce2c64b687df191c8a9c740dd35b330e67712ff4ea645e95b0f217`

편집 없음. 젠이 직접 붙이라고 한 `Lo-fi Remastered`와 나머지 3단어는 그대로 둔다 (원문 (a)와 같다).

```text
Korean Indie Alt R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal, Modern Indie R&B, Lo-fi Remastered, Articulation
```

### 작은 빛

- Suno ID (작업공간 Lo-Fi Remix): `1406e9df-89fb-4daa-a46b-0c019d2dc7ab` — https://suno.com/song/1406e9df-89fb-4daa-a46b-0c019d2dc7ab
- 화면에 표시된 원곡: 화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)
- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `작은 빛`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)
- 원문에 적힌 BPM·조성·성별: BPM 72 · 조성 없음 · 성별 없음
- EXCLUDE:
- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): `X Major|Minor`, `male|female vocal`
- 메모: STYLE에 male/female 단어가 없다. 성별 쪽 표현은 `Single warm baritone lead`뿐이다.

**(a) 원문 STYLE** — 681자, sha256 `ae59fe9fbec0121fde265000b1163fd7e3f1fa719415a198dbba72c984c1a857`

```text
Lo-fi modern R&B, Korean indie alt-R&B, 72 BPM half-time pocket, intimate felt-piano motif over warm Rhodes voicings, soft brushed drums and rim-click with a rounded understated bass groove; begin sparse, add muted electronic texture through the pre-chorus, widen gently with subtle strings in each chorus, then strip back for a close, vulnerable bridge and instrumental outro, Single warm baritone lead in a dry conversational chest voice, crisp Korean diction and deliberate articulation, natural breath and phrasing, sustained tender chorus notes with a restrained dynamic rise, Cozy close-miked vocal, balanced clean mix, warm low end, moderate room ambience, no layered vocals
```

**(b) 새 곡용 STYLE** — 681자, sha256 `ae59fe9fbec0121fde265000b1163fd7e3f1fa719415a198dbba72c984c1a857`

편집 없음 (원문 (a)와 같다).

```text
Lo-fi modern R&B, Korean indie alt-R&B, 72 BPM half-time pocket, intimate felt-piano motif over warm Rhodes voicings, soft brushed drums and rim-click with a rounded understated bass groove; begin sparse, add muted electronic texture through the pre-chorus, widen gently with subtle strings in each chorus, then strip back for a close, vulnerable bridge and instrumental outro, Single warm baritone lead in a dry conversational chest voice, crisp Korean diction and deliberate articulation, natural breath and phrasing, sustained tender chorus notes with a restrained dynamic rise, Cozy close-miked vocal, balanced clean mix, warm low end, moderate room ambience, no layered vocals
```

## Original Styles

2026-11-02: 재생성 9곡(Track 11–19)의 STYLE은 새로 조립한 23:00 버전(`## New Song Style Assembly`)이 아니라 **젠의 원곡 Suno 스타일 프롬프트**다. 젠: 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외」, 템포는 「원곡 BPM 그대로」, 여름밤·벚꽃·그네의 보컬은 「원곡대로 남성」.

규칙 (모든 곡 공통):

1. 최종 STYLE = `Lo-fi Remix, ` + 원곡 STYLE 원문(줄바꿈 그대로). 근거: 젠 「Lo-fi remix는 붙여야해 안전빵이야」.
2. 원문에서 바꾸는 것은 세 가지뿐이고 항목마다 아래에 적는다. (a) 장르 낱말 alternative/Alt/Modern R&B 삭제. (b) STYLE 안에 있던 제외 줄(`Exclude Style:`/`EXCLUDE:`)을 EXCLUDE 칸으로 옮김 — 젠 「- 붙은 스타일은 exclude인거 알지?」. (c) 새 곡 가사에서 뜻이 없는 원곡 가사 전용 지시만 최소 삭제 — 젠 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」.
3. BPM 숫자·Key·성별 낱말·나머지 문구는 원곡 그대로다. 곡의 보컬 성별도 원곡을 따른다(여름밤·벚꽃·그네 = 남성).
4. 최종 EXCLUDE = 원곡 EXCLUDE + (b)에서 옮긴 항목(순서 유지, 겹치는 항목은 한 번만).
5. Suno 파라미터는 원곡 concept에 숫자가 기록된 곡만 그 값(먼지 W20/I80, 산책 W25/I75, 물결 W20/I80), 나머지는 `default`다.

검사 방식: txt 머리말에 `Style Type: <타입>`과 `Style Source: user-supplied original style`이 있고, txt STYLE이 이 절 해당 `###` 항목의 첫 `text` 코드 블록과 줄바꿈까지 글자 그대로 같고, txt EXCLUDE가 그 항목의 `- EXCLUDE:` 줄과 항목·순서까지 같을 때만 `gate --stage track-prompt`가 900자·EXCLUDE 8개 예산을 막지 않는다(`MASTER/style/STYLE.md` §3). 이 절에서는 `###` 제목을 타입 이름과 같게, 항목마다 EXCLUDE 줄을 한 줄만 둔다. 같은 타입을 쓰는 곡은 한 항목을 함께 쓴다.

기계 판독본은 `.ai/plans/2026-11-02-2300-final-styles.json`(곡별 `style`·`exclude`·`edits[]`)이고 이 절의 STYLE 블록과 바이트 단위로 같다 (대조: `.ai/validation/2026-11-02-2300-styles/a2-check.json`). 원곡 조사 원본: `.ai/plans/2026-11-02-2300-original-styles.json`·`.md`.

### 먼지

- 쓰이는 곡: Track 11 라디오 (txt 머리말 `Style Type: 먼지`)
- 출처: `SERIES/14-00/concept.md` `### Track 09: 먼지` — STYLE 본문 1040–1062행 · 별도 Exclude Style 블록 1067행 (원곡 STYLE 705자, sha256 `14b6988b1d89ccc8ad43c9387de237c24e9a8d16505afac74d66dd86290b9b5e`)
- 머리말 값: BPM `72` · Key `Eb Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: Weirdness 20 · Style Influence 80 (`SERIES/14-00/concept.md:976-980`)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
  2. STYLE 끝의 `Exclude Style: Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Intense, Dramatic` 줄과 그 앞 빈 줄을 STYLE에서 뺐다. 별도 EXCLUDE 블록에 이미 있어 추가된 항목은 없다(겹친 8개 기록).
- 메모: 원곡 절 안에서 STYLE 속 `Exclude Style:` 줄(8개)과 별도 Exclude Style 블록(10개, `Cold`·`Dark` 추가)이 다르다. 젠 지시(제외 항목은 EXCLUDE 칸)에 따라 별도 블록 10개를 최종 EXCLUDE로 쓰고, STYLE 속 8개는 모두 그 안에 있어 추가되는 항목이 없다.
- EXCLUDE: Airy, Falsetto, Whisper, Harmonized, Backing vocals, Choir, Cold, Dark, Intense, Dramatic

**최종 STYLE** — 624자, sha256 `0121afa45e50cea44d284b49c75ae002cc6f768c20905cabdad9efaefea975c8`

```text
Lo-fi Remix, Korean Soft R&B, 72 BPM, Eb Major

Vibraphone-led, supportive R&B groove,
laid-back brush rhythm, warm afternoon texture.

Male vocal. Natural, intimate.
Raw, Solid, Direct, Dry.
Chest voice dominant. No falsetto. Minimal vibrato.

Verse1: vibraphone melody, sparse drums, drifting feel.
Verse2: soft kick enters, groove locks in.
Lift through rhythm, not volume.

Chorus: kick and snare present, melodic bass,
pad widens gently.

Bridge: vibraphone and voice only, gentle build.
Outro: gradual fade, vibraphone restates motif softly.

Single lead vocal throughout.
Chorus expansion by arrangement density only.
```

### 마음 밖

- 쓰이는 곡: Track 12 스웨터 (txt 머리말 `Style Type: 마음 밖`)
- 출처: `SERIES/04-00/concept.md` `## Track 01 (Seed)` — STYLE 본문 135–135행 · 별도 Exclude Style 블록(140행)은 `(없음)` (원곡 STYLE 707자, sha256 `5123ec3f7791171df659de8957d9bb535a158b96b6e132d3614a042f944f8001`)
- 머리말 값: BPM `96–106 (original STYLE wording; release file 90)` · Key `A♭ (original wording "key color like A♭"; mode not stated)` · Vocal `female` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: 기본값 `default` (원곡에 숫자 기록 없음 — SERIES/04-00/concept.md에 Weirdness·Style Influence 기록 없음)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
- 메모: STYLE의 BPM이 범위(`96–106 BPM`, 발매 파일명은 90)이고 Key에 Major/Minor가 없다(`key color like A♭`). 원문 그대로 두었고 머리말은 원문 표현을 쓴다(검사 도구는 이런 표기를 STYLE과 대조하지 않고 머리말이 비어 있는지만 본다).
- EXCLUDE:

**최종 STYLE** — 720자, sha256 `56729ee045a4b12a1ed26f2825c735ad263886d148b8872895756b3dd418447b`

```text
Lo-fi Remix, articulation, Korean R&B/pop ballad, 96–106 BPM, key color like A♭, Piano/Rhodes-led, cinematic but restrained, Warm keys upfront, soft supportive bass, tight understated kick (present, not huge), rim/snare light, simple hats, no rolls, Subtle strings/pads in choruses only, never dramatic, Verse intimate and sparse; chorus opens slightly wider with more harmony, not more rhythm, Final chorus adds a gentle "major-color" lift via chords/strings, not belting, Female vocal very forward and dry/close-mic: warm husky tone, clear Korean diction, conversational phrasing, controlled vibrato, natural breaths, minimal pitch correction, Melody understated (no big leaps, no catchy hook), Outro instrumental fade
```

### 작은 빛

- 쓰이는 곡: Track 13 편지 (txt 머리말 `Style Type: 작은 빛`)
- 출처: `SERIES/22-00/concept.md` `### 10. 작은 손 (Tiny Hand)` — STYLE 본문 1095–1106행 (원곡 STYLE 809자, sha256 `e4a8ddac20c318504e0795ad91f54fa8070fd05cba3ea0bec505d04e0eec1dd7`)
- 머리말 값: BPM `72` · Key `Db Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: 기본값 `default` (원곡에 숫자 기록 없음 — SERIES/22-00/concept.md에 Weirdness·Style Influence 기록 없음)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
- 메모: 22-00 Track Map은 `작은 빛`, 상세 제목줄은 `작은 손 (Tiny Hand)`이다. 발매 파일명(`SERIES/RNB-BEST/concept.md:272`)이 `작은 빛`이라 같은 곡으로 본다. 22-00의 시리즈 공통 Exclude Template(84–92행)은 이 곡 절에 없어 EXCLUDE는 비어 있다.
- EXCLUDE:

**최종 STYLE** — 822자, sha256 `84370501a8cd3c2917ed618f0b87262e2d663836c3586d046b70702b63b0c666`

```text
Lo-fi Remix, Articulation. Korean Chill R&B, 72 BPM, Db Major,
felt piano-led, warm Rhodes chords, soft brush kit,
rim-click, warm bass groove, subtle strings in chorus,
Male vocal: Warm, Intimate, Chest voice, Dry, articulation,
warm baritone, conversational phrasing, gentle sustained chorus hook,
chorus builds with emotional swell, tender vocal intensity, aching warmth,
cozy intimate mix, wide stereo, warm low-end,
moderate reverb, intimate ambience, EQ balanced sound, clean mix.
Lead vocal remains single and dominant throughout. No stacked or choir-like harmonies.
Vocal line may intensify dynamically (gentle lift, higher register), but no additional vocal layers.
Chorus vocal may be delivered with tender intensity or gentle sustained note.
Higher register emphasis is allowed. Natural vocal warmth encouraged.
```

### 산책

- 쓰이는 곡: Track 14 기타 (txt 머리말 `Style Type: 산책`)
- 출처: `SERIES/14-00/concept.md` `### Track 03: 산책` — STYLE 본문 423–449행 · 별도 Exclude Style 블록 454행 (원곡 STYLE 946자, sha256 `eac143553f763e30e0c8c301510ca2eb3a774d1a740284518433cf2a4c8807a3`)
- 머리말 값: BPM `74` · Key `Eb Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: Weirdness 25 · Style Influence 75 (`SERIES/14-00/concept.md:361-365`)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
  2. `Indie Alt R&B` → `Indie R&B` (`Alt` 삭제, 그 밖은 그대로).
- 메모: 최종 STYLE이 900자를 넘는다(앞붙임만으로도 959자). 원곡 스타일 모드가 허용하는 값이며 `Alt` 삭제와 무관하다.
- EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, High-pitched belting, Harmonized, Backing vocals, Choir, Intense, Mumbled

**최종 STYLE** — 955자, sha256 `a1990eaaa31063dfc6149fa15a69a4f929e23b5c2c52cddaa1961f4761cfd17c`

```text
Lo-fi Remix, Articulation.
Korean Indie R&B, 74 BPM, Eb Major.
Clean Electric Guitar-led, supportive R&B groove,
rim-click, warm afternoon texture, subtle vinyl crackle.

Male vocal: Solid, Direct, Raw, Dry.
Chest voice dominant. No falsetto.
Straight tone only. No vibrato, no ad-libs.
High register chest voice preferred over falsetto.
Tone is nonchalant and effortless, never dramatic.

Vocal articulation is critical:
clear consonant attack, precise syllable separation,
no slurring, no breathy phrasing.

Verse2 builds clear tension.
Chorus contains a single, unavoidable high-note focal point:
short, decisive high register chest note,
straight tone, not sustained belting.
If the chorus does not reach a high register chest note,
the emotional intent is considered failed.

Chorus hook-first, repeated identically.
Later choruses grow only by arrangement density.
Bridge builds every bar.
Outro guitar fades.
Lead vocal remains single and dominant.
```

### 물결

- 쓰이는 곡: Track 15 노을 (txt 머리말 `Style Type: 물결`)
- 출처: `SERIES/14-00/concept.md` `### Track 06: 물결` — STYLE 본문 735–735행 · 별도 Exclude Style 블록 740행 (원곡 STYLE 627자, sha256 `b54db2b5da5ed420bad860ed28fea2dcacb2d91f923ee13c80e60f12a2d522ff`)
- 머리말 값: BPM `74` · Key `A Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: Weirdness 20 · Style Influence 80 (`SERIES/14-00/concept.md:673-677`)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
  2. `Indie Alt R&B` → `Indie R&B` (`Alt` 삭제, 그 밖은 그대로).
- 메모: 23:00 시리즈에서 덧붙였던 `Modern Indie R&B, Lo-fi Remastered, Articulation`은 쓰지 않는다(젠 「23:00버전이 아닌 원곡 스타일」). EXCLUDE 13개는 위 `## Type Styles` 물결 항목의 EXCLUDE와 항목·순서가 같다.
- EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Growl, Vibrato, Opera, Dramatic, Harmonized, Backing vocals, Choir, Intense, Mumbled

**최종 STYLE** — 636자, sha256 `3926d154576a0f1e7fda2f68bf30f2f6ef3157ef03184bb4dc14cf2afad0262f`

```text
Lo-fi Remix, Korean Indie R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal
```

### 물안개

- 쓰이는 곡: Track 16 여름밤 (txt 머리말 `Style Type: 물안개`)
- 출처: `SERIES/04-00/concept.md` `## Track 04` — STYLE 본문 349–356행 · 별도 Exclude Style 블록 361행 (원곡 STYLE 753자, sha256 `ca0588aa5e211168eb31aba52b0e7f651b9be199f21606374f5f3de659cb72ee`)
- 머리말 값: BPM `80` · Key `Eb Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: 기본값 `default` (원곡에 숫자 기록 없음 — SERIES/04-00/concept.md에 Weirdness·Style Influence 기록 없음)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
- 메모: 소제목은 `Style Prompt (제로 베이스라인 v2)`. STYLE이 소문자 `articulation,`로 시작하는 것도 원문이다.
- EXCLUDE: choir, gospel choir, stacked harmonies, vocal harmonies, harmony stack, ensemble vocals, doubled vocals, vocoder, vocal chop, hard tune, pitchy EDM lead, hyperpop vocal, autotune heavy, EDM drops, big room, festival, supersaw lead, sidechain pumping

**최종 STYLE** — 766자, sha256 `15de4017908364fd4b5a15b1e0a4ac1feebbcc20987630ebfb047fefd9a26d9d`

```text
Lo-fi Remix, articulation, Korean Lo-fi R&B, 80 BPM, key Eb Major, Felt Piano-led, soft shaker, hazy ambient pad, cinematic but restrained.
Male vocal: warm soulful tone, dry close-mic, slightly breathy, straight delivery, minimal vibrato, minimal autotune.
No backing vocals, no harmonies, no doubles, no choir.
Lead vocal only throughout; absolutely no vocal layers in chorus (no doubles, no unison, no octaves).
Chorus hook-first, repeat identical; Chorus2 bigger only by arrangement density and stereo width, vocals unchanged.
Verse2 same melodic contour as verse1; last 2 lines stronger dynamics and slightly higher register, minimal runs.
Bridge builds every bar with instrumental layers; no energy drop into chorus.
Outro felt piano notes fading into silence.
```

### 골목

- 쓰이는 곡: Track 17 막차 (txt 머리말 `Style Type: 골목`)
- 출처: `SERIES/18-00/concept.md` `## 10. Track 07 "골목" — 혼자 걷는 골목길 (기존 싱글)` — STYLE 본문 1091–1110행 (원곡 STYLE 731자, sha256 `039e4094445803a30240597324c4996da47896c4997a2d490949cef62c381d04`)
- 머리말 값: BPM `67` · Key `Db Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: 기본값 `default` (원곡에 숫자 기록 없음 — SERIES/18-00/concept.md:1113-1118에 숫자 대신 `기존 싱글`)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
  2. STYLE 끝의 `EXCLUDE: Rap, Hip-hop, Spoken word, Harmonies, Backing vocals, Doubles, Choir, Ad-libs, Runs, Melisma, Falsetto, Bright, Upbeat, Energetic, Fast` 줄과 그 앞 빈 줄을 STYLE에서 뺐다. 15개 항목을 EXCLUDE로 옮겼다.
- EXCLUDE: Rap, Hip-hop, Spoken word, Harmonies, Backing vocals, Doubles, Choir, Ad-libs, Runs, Melisma, Falsetto, Bright, Upbeat, Energetic, Fast

**최종 STYLE** — 598자, sha256 `ebc71cedfefd6b33a4e3f3a08620517feecfba7a11d2f1522dfa2f4f2ce6b95a`

```text
Lo-fi Remix, Korean Slow R&B Ballad, 67 BPM, Db Major

Male vocal, Raw, Dry, Unprocessed, Chest voice dominant
No falsetto, No runs, No melisma
Speech-like phrasing, Narrow melodic range
Precise articulation, clear consonants

supportive, warm pad texture
Minimal drums or drumless verses
Soft bass, low presence
Moderate reverb, EQ balanced sound, clean mix

Verse2 subtle intensity increase by vocal weight only
Chorus: longer sustain on hook phrase, no belt
Bridge: single guitar line, no solo flourish

No harmony, no backing vocals, no doubles
Lead vocal remains single and dominant throughout
```

### 이름

- 쓰이는 곡: Track 18 벚꽃 · Track 19 그네 (txt 머리말 `Style Type: 이름`)
- 출처: `SERIES/18-00/concept.md` `## 12. Track 09 "이름" — 문 열림, 이름 불려짐 (기존 싱글)` — STYLE 본문 1393–1413행 (원곡 STYLE 843자, sha256 `5a871a19dbb538e456469b014bbb702c75e8c0fc2be882c2d1237185b3149f64`)
- 머리말 값: BPM `72` · Key `Ab Major` · Vocal `male` (STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)
- Suno 파라미터: 기본값 `default` (원곡에 숫자 기록 없음 — SERIES/18-00/concept.md:1416-1421에 숫자 대신 `기존 싱글`)
- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):
  1. 맨 앞에 `Lo-fi Remix, ` 를 더했다.
  2. STYLE 끝의 `EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled` 줄과 그 앞 빈 줄을 STYLE에서 뺐다. 11개 항목을 EXCLUDE로 옮겼다.
  3. `Bridge3: sparse, tension rising, emotional commitment` 줄 삭제 — 새 곡 가사 틀(이름)에는 `[Bridge]`가 하나뿐이라 세 번째 브리지가 없다.
  4. `Last "괜찮아": longest sustain in entire track, This single note defines the emotional peak` 줄 삭제 — 새 곡 가사에 그 낱말·그 음이 없고 줄의 두 구절이 모두 그 낱말에 기대고 있다.
- 메모: Track 18 벚꽃과 Track 19 그네가 이 한 항목을 쓴다(STYLE·EXCLUDE 같음).
- EXCLUDE: Falsetto, Airy, Whisper, Breathiness, Vibrato, Harmonized, Backing vocals, Choir, Intense, Dramatic, Mumbled

**최종 STYLE** — 594자, sha256 `4a12b72669796fa36f505e3011efcf8778daf20a16c360902fac7d87edb6675b`

```text
Lo-fi Remix, Korean Soft R&B, 72 BPM, Ab Major

Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture

Male vocal: Natural, laid-back, Raw, Solid, Direct, Dry
Chest voice dominant, No falsetto, Straight tone, No vibrato, no ad-libs
Precise articulation, clear consonants

Verse1: synth pad, sparse drums, drifting
Verse2: kick steady, groove deepens
Verse2 last 2 lines: higher register, tighter rhythm, vocal push
Bridge1/2: pad and voice, intimate
Final Chorus: chest belt pushed, high register climax
Outro: short fade, pad sustain

Single lead vocal
Density expansion only
```

## New Song Style Assembly

10·20만 해당(1차 생성 원고). 11~19는 `## Original Styles`로 대체 — 2026-11-02

새 곡 11곡(Track 10–20)의 최종 STYLE을 만드는 규칙과 곡별 결과다. 최종 STYLE 전문은 `.ai/plans/2026-11-01-2300-new-song-styles.json`의 `style`이 가진다(여기에 복제하지 않는다). 아래 표의 글자 수·sha256은 그 전문과 같아야 한다. 갱신된 `## Type Styles`의 (b) 블록에서 아래 규칙으로 11곡을 다시 조립해 json의 `style`·`sha256`과 대조한 결과는 `.ai/validation/2026-11-01-2300-foundation/25-assembly-reproduction.txt`(스크립트 `25-assembly-reproduction.py`)에 있다.

1. **시작점**: 곡이 쓰는 타입의 `(b) 새 곡용 STYLE`을 그대로 쓴다. 근거: 젠 2026-11-01 「url에서 9곡의 가사 컨셉과 특징, 스타일 프롬프트(그대로 활용)를 각 타입 별로 참고해서 나머지 11곡을 새로 만들어야해.」
2. **Lo-fi Remix 앞붙임**: (b)에 `lo-fi remix`(대소문자 무관)가 없으면 STYLE 맨 앞에 `Lo-fi Remix, `를 붙인다. 이미 있으면(산책: 맨 앞 `Lo-Fi Remix, `, 마음 밖: 둘째 항목 `lo-fi remix,`) 원문 위치 그대로 두고 더하지 않는다. 근거: 젠 2026-11-01 「Lo-fi remix는 붙여야해 안전빵이야. 현재버전들이 잘나온 이유로 보고있어」, 이어 「'Lo-fi Remix' 표시를 새 11곡 중 어디에 붙일까요?」에 「새 11곡 모두 (추천)」 — 11곡 스타일 맨 앞에 모두 'Lo-fi Remix,'를 붙임. 산책·마음 밖은 원문 위치 그대로, 나머지 7개 타입 곡은 맨 앞에 더함.
3. **끝에 덧붙이기**: STYLE에 없는 것만 끝에 `, NN BPM`, `, X Major|Minor`, `, male|female vocal` 순서로 덧붙인다(BPM·조성·성별 중 이미 STYLE에 있는 것은 덧붙이지 않는다). 근거: 젠 「선례처럼 끝에 덧붙이기」. 선례: `.ai/lyrics/2026-10-02_17-00_12_서점-full-draft.md` Source Map.

| # | 제목 | 타입 | 보컬 | BPM | 조성 | Lo-fi Remix 앞붙임 | 끝에 덧붙인 항목 | 글자 수 | sha256 |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 귤 | 숨 | female | 68 | D Major | 예 (맨 앞에 `Lo-fi Remix, `) | `68 BPM`, `D Major` | 639 | `93827f09289b7741209cf51de5ba339f2cd502ed18cb5eaa31fca1b0761da523` |
| 11 | 라디오 | 먼지 | male | 70 | F Major | 예 (맨 앞에 `Lo-fi Remix, `) | `70 BPM`, `F Major` | 724 | `7aba864bcebbe073926676d8610354f431fc5507cda6bb6c4b89c12a01dbfd2e` |
| 12 | 스웨터 | 마음 밖 | female | 72 | Ab Major | 아니오 (원문에 이미 있음) | `72 BPM`, `Ab Major` | 557 | `16644e527b4fb75dd797efff05f4935d53da839e6624aa2e65f321e2cf428e0e` |
| 13 | 편지 | 작은 빛 | male | 72 | Db Major | 예 (맨 앞에 `Lo-fi Remix, `) | `Db Major`, `male vocal` | 716 | `0336054893862b323738f954a6c9ac79456f0b272bb55667a8430273649c8e12` |
| 14 | 기타 | 산책 | male | 74 | Eb Major | 아니오 (원문에 이미 있음) | 없음 | 659 | `9d4ea3c73134fe61679382dc6ce62bda49413e7093de270d61692194c2c80a93` |
| 15 | 노을 | 물결 | male | 74 | A Major | 예 (맨 앞에 `Lo-fi Remix, `) | 없음 | 690 | `00b0cd745ccf775f7582ba276e027a7fc0d8a8871701394807d9d3c8f420ec9e` |
| 16 | 여름밤 | 물안개 | female | 76 | G Major | 예 (맨 앞에 `Lo-fi Remix, `) | `76 BPM`, `G Major`, `female vocal` | 418 | `51bec87b8e1403cb0a2dcd96def733387068d0ba94a2cf33475d436276a41092` |
| 17 | 막차 | 골목 | male | 80 | E Major | 예 (맨 앞에 `Lo-fi Remix, `) | `80 BPM`, `E Major`, `male vocal` | 540 | `6e4bdf3d7ec691295b7ec626082c13e7021517049424d458fe86b430aa7defcd` |
| 18 | 벚꽃 | 이름 | female | 78 | C Major | 예 (맨 앞에 `Lo-fi Remix, `) | `78 BPM`, `C Major`, `female vocal` | 549 | `88b6412102b5ebf78b1b5c20b8fd7236f666454aafe9192bafc400450f7fad0b` |
| 19 | 그네 | 이름 | female | 70 | E Minor | 예 (맨 앞에 `Lo-fi Remix, `) | `70 BPM`, `E Minor`, `female vocal` | 549 | `d4258ede1b52343d189228ef610146f82fa08852c9f822ab2080496516551380` |
| 20 | 포근히 | 숨 | female | 66 | Bb Major | 예 (맨 앞에 `Lo-fi Remix, `) | `66 BPM`, `Bb Major` | 640 | `28ff0607d225f9a91b2a8a16e4b1514f176b0dbfe3f7d9f11a9857abb7d986f7` |

앞붙임 9곡(10·11·13·15·16·17·18·19·20), 원문 위치 유지 2곡(12 스웨터·14 기타). 14 기타는 앞붙임과 덧붙임이 모두 없어 산책 (a)·(b)와 글자 수·sha256이 같다. 15 노을(물결 타입)은 BPM·조성·성별이 이미 STYLE에 있어 앞붙임만 더해진다. 13 편지(작은 빛 타입)는 STYLE에 성별 단어가 없어(`Single warm baritone lead`뿐) `male vocal`을 덧붙인다.

## Track Map (numbers are temporary)

| # | Title | Role | Suno ID | Type | Source text |
|---|---|---|---|---|---|
| 01 | 먼지 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `2bdaaa83-7145-4808-b57f-f0b98f7788f0` | 먼지 | `input/tracks/01_먼지 (Lo-Fi Remix).txt` |
| 02 | 산책 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `9fe398d7-ed43-4e77-8489-9c3d67a0d657` | 산책 | `input/tracks/02_산책 (Lo-Fi Remix).txt` |
| 03 | 숨 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `36d296ff-f0af-4b44-a5ad-0bc7cfef0982` | 숨 | `input/tracks/03_숨 (Lo-Fi Remix).txt` |
| 04 | 이름 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `4708df3d-6f0a-4602-bea4-ccb734cf03db` | 이름 | `input/tracks/04_이름 (Lo-Fi Remix).txt` |
| 05 | 마음 밖 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `17a24019-4412-4443-b4e7-6d305d539958` | 마음 밖 | `input/tracks/05_마음 밖 (Lo-Fi Remix).txt` |
| 06 | 물안개 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `0908a587-be93-46c5-a8e6-46428f3efba5` | 물안개 | `input/tracks/06_물안개 (Lo-Fi Remix).txt` |
| 07 | 골목 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `aca55231-9e58-469d-b0ce-c29cb767eaa5` | 골목 | `input/tracks/07_골목 (Lo-Fi Remix).txt` |
| 08 | 물결 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `5654d747-4921-416f-9b72-755bf27d734a` | 물결 | `input/tracks/08_물결 (Lo-Fi Remix).txt` |
| 09 | 작은 빛 (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `1406e9df-89fb-4daa-a46b-0c019d2dc7ab` | 작은 빛 | `input/tracks/09_작은 빛 (Lo-Fi Remix).txt` |
| 10 | 귤 | 새 곡 · female vocal · D Major · 68 BPM · 확정 — 후보 B (젠 「귤 통과」「귤은 B」) | `9053be56-1eaa-4a16-a8ab-e018a3c9b0c7` | 숨 | `input/tracks/10_귤.txt` |
| 11 | 라디오 | 새 곡 · male vocal · Eb Major · 72 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 먼지 | `input/tracks/11_라디오.txt` |
| 12 | 스웨터 | 새 곡 · female vocal · A♭ (mode not stated) · 96–106 BPM (STYLE wording; release file 90) · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 마음 밖 | `input/tracks/12_스웨터.txt` |
| 13 | 편지 | 새 곡 · male vocal · Db Major · 72 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 작은 빛 | `input/tracks/13_편지.txt` |
| 14 | 기타 | 새 곡 · male vocal · Eb Major · 74 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 산책 | `input/tracks/14_기타.txt` |
| 15 | 노을 | 새 곡 · male vocal · A Major · 74 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 물결 | `input/tracks/15_노을.txt` |
| 16 | 여름밤 | 새 곡 · male vocal · Eb Major · 80 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 물안개 | `input/tracks/16_여름밤.txt` |
| 17 | 막차 | 새 곡 · male vocal · Db Major · 67 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 골목 | `input/tracks/17_막차.txt` |
| 18 | 벚꽃 | 새 곡 · male vocal · Ab Major · 72 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 이름 | `input/tracks/18_벚꽃.txt` |
| 19 | 그네 | 새 곡 · male vocal · Ab Major · 72 BPM · 재생성 대기 (원곡 가사 틀 + 원곡 스타일) | — | 이름 | `input/tracks/19_그네.txt` |
| 20 | 포근히 | 새 곡 · female vocal · Bb Major · 66 BPM · 확정 — 후보 B (젠 「포근히 통과」「포근히 B」) | `8e10bd3d-897a-45e8-b2cc-d70577ae5b80` | 숨 | `input/tracks/20_포근히.txt` |

Order of Tracks 01–09 follows the workspace list order given for this series. Tracks 10–20 are the new songs. Tracks 10 and 20 keep their first-generation design from `.ai/plans/2026-11-01-2300-new-song-styles.json` (`## New Song Style Assembly`) and 젠 chose candidate B for both on 2026-11-02 (the Suno ID column holds the chosen candidate; evidence in `input/suno-candidates.json`). Tracks 11–19 are being regenerated (2026-11-02): vocal, key, and BPM come from each type's original song (`## Original Styles`), and the lyrics follow the type original's lyric template (`## Series Overrides`). Status `재생성 대기` means the txt manuscript is being rewritten and nothing has been regenerated in Suno yet; the first-generation candidates stay in `input/suno-candidates.json`.

## Source Records

- Observation: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json`, `styles-verbatim.txt`, and `raw/` (ego lite, read-only; no playback, generation, edit, or download). Treat these as read-only evidence.
- Displayed styles and lyrics are not proof of the exact generation input. Durations differ by one second between the list and the play bar for some songs, so none is recorded here. Audio was not measured.
- Only 물결 showed Weirdness 20% and Style Influence 80% (it is a Cover). The other eight did not display those fields, which does not prove they are unset.

## Upload Status

- YouTube upload: not uploaded yet
