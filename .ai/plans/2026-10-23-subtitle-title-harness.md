# Subtitle publication and title defaults

Date: 2026-10-23
Request: 젠 — “이번 제목 포맷과 더불어 반영해둬.” (자막 게시 하네스·스킬의 근본 원인 반영 요청에 이어짐)
Status: implementation, verification, isolated review, and work records complete

## Confirmed starting point

- `d00b891` added the subtitle skill procedure and recorded successful manual Korean captions on `3HorT4OoDhg`. It did not modify maintained harness code.
- `prepare-subtitles` only creates an untimed transcript. Upload-ready checks subtitle file presence; `uploaded` records video publication, not manual caption publication.
- The ignored one-off timing builder corrected missed sung repeats and one onset outside its acoustic evidence. Those checks were not reusable.
- The cause of YouTube's original untimed-draft error is unconfirmed. Successful timed upload establishes a working method, not a diagnosis of that service error.
- Precedent: `MASTER/youtube/YOUTUBE.md` already contains the approved 17:30 orange title as the default writing example. Preserve that structure and adapt the sensory hook, actual genres, and suitable uses for each series.

## Implementation

1. Add a maintained explicit timing-map → SRT path and prepared-subtitle verification. Preserve approved wording, source order, evidence-backed sung repeats, exact render/crossfade offsets, cue boundaries and original files. No ASR dependency or new media run.
2. Verify manual caption publication separately using target identity, retained Studio/public observations and official SRT round-trip evidence. Do not infer caption publication from video `uploaded` or file existence.
3. Require validated timed captions for vocal videos over one hour at upload-ready; retain instrumental exemption and existing video-upload semantics. Expose caption state separately.
4. Wire the existing title default into publishing guidance and relevant reusable checks without changing approved live titles or imposing the orange wording on other series.
5. Update CLI/workflow/skill docs, run meaningful regressions and the actual 17:30 stored-evidence path, then one isolated Astra xhigh review. Record verified outcomes and persist changes.

## Validation and scope

- Regression checks: omitted sung repeats, late onset outside observed support, wrong crossfade/repeat offsets, malformed SRT/evidence, source overwrite protection; title format/length and approved exceptions where applicable.
- Existing unit tests, compilation, doctor, series validation/state/uploaded gate, new prepared/published checks, skill validation, diff checks.
- Original published SRT hash must remain `29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226`; live YouTube/video/title/comments and original sources remain unchanged.
- Acoustic timing remains an estimate and retained UI observations are historical evidence, not a fresh live browser observation.
- Official references rechecked 2026-10-23: https://support.google.com/youtube/answer/2734796?hl=en (over-one-hour transcript synchronization not recommended); https://support.google.com/youtube/answer/2734698?hl=en (plain UTF-8 SRT supported).

## Results

- Maintained `prepare-subtitles SERIES --timing-map <checked.json>` creates and checks timed SRT from an explicit, evidence-backed map; `verify-subtitles SERIES --stage prepared|published --json` checks preparation and retained publication evidence separately. The >1-hour vocal `upload-ready` gate requires prepared PASS. `uploaded` still means video upload. This does not automate full-song listening or audio-to-lyrics alignment.
- Title writing defaults to six sections: `Playlist | sensory music hook | actual genres | varied suitable uses | Wavvy | time`. The 17:30 approved title remains unchanged; previously approved five-section and no-time compilation forms remain valid. Format/length checks do not replace editorial judgment about hook, genre, and use.
- Controller raw checks in `.ai/validation/2026-10-23-subtitle-title-harness/`: 86 unit tests PASS; 18 tests PASS in an isolated copy with no ignored output; all 17 existing series titles PASS; compilation, doctor, 17:30 validation, release verification, prepared/published verification, state, upload-ready/uploaded gates, skill validation, and diff checks PASS. Published PASS rechecks retained 2026-10-23 Studio/public observations and download; it is not a new browser check or republication.
- SHA-256 baseline recheck (`record-baseline-check.json`) confirms unchanged timed SRT `29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226` (1,270 cues/1,498 lyric lines), untimed source `29cd296a8c31bcf6629e2f468862698970931ca7ad50e36fd2f8f547c953ba18`, thumbnail `634cbb9ff89b2c39cf89a240100368b310c0e22bfaee60a0463170f25912e025`, and upload CSV `bd63238f876b01f8ee0f3a7e2b50ab59ed3f60bfd9b83e587a9f0573e0a99c5d`.
- [Isolated review](../reviews/2026-10-23-subtitle-title-harness-review.md) returned CLEAN: confirmed Critical/High 0 and no principle observations. The original YouTube untimed-draft error's cause remains unconfirmed. No implementation or validation work remains in this request.
