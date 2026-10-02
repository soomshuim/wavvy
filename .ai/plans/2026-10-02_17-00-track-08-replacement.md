# 17:00 Track 08 — 취향 (user-supplied replacement)

Date: 2026-10-02
Scope: Replace Tracks 08 and 09 with the user's new STYLE and LYRICS, and correct Wavvy's section-cue guidance and lyric checker. Preserve the 2026-10-01 approved versions as history.

## 선례

- `SERIES/17-00/input/tracks/08_네 취향.txt` and `.ai/lyrics/2026-10-01_17-00_08_네-취향-full-draft.md`: the previously approved source and bound lyric record. The new user lyric retains its sung lines but adds inline singer tags and a new STYLE/tempo.
- `SERIES/17-00/concept.md`: Track 08 alone allows alternating female/male verses and two-part Chorus harmony. The new user STYLE and lyric tags preserve that exception.
- `MASTER/WORKFLOWS.md` §0: update the txt before syncing concept. User delivery of the replacement text authorizes its capture; do not call it an explicit new PASS.
- `SERIES/17-00/input/tracks/09_한 곡만 더.txt`: earlier 122 BPM/D Major acoustic R&B source. The user-supplied replacement switches STYLE to indie acoustic rock while retaining the lyric body; the earlier tempo, key, and EXCLUDE are not inherited.
- `MASTER/lyrics/LYRICS.md` §2 and `skills/wavvy-lyricist/SKILL.md`: previous blanket rule moved vocal/production cues to Style. Suno's official release notes show Lyrics structure labels and a bracketed vocal cue; the user's Track 08 generation reportedly separated the voices when section cues were added. Instrument/chord cue syntax has no official success guarantee.

## Plan

1. Save the user-provided source under `SERIES/17-00/input/tracks/08_취향.txt`, preserving STYLE and LYRICS characters and tag spacing. Set 100 BPM from STYLE. Mark key and EXCLUDE as not supplied in this replacement; do not carry forward the old E Major or six EXCLUDE terms.
2. Replace Track 09 STYLE and LYRICS with the exact user-provided text. Mark BPM, key, and EXCLUDE as unsupplied. Compare the lyric body to the earlier approved source.
3. Update `MASTER/lyrics/LYRICS.md`, `MASTER/style/STYLE.md`, the lyric skill/spec, and the style evidence reference: allow concise section-specific bracket cues while keeping whole-song direction in Style. Preserve the user's Track 08 cue spelling and spacing. Update the local full-song checker to count sections with trailing bracket cues, and test it.
4. Keep a current review-only record for Track 08, since this is user-provided text and the 84-bar plan is only provisional. Retain the old record as history. Run source, lyric, and state checks. Sync the two replacements and guidance change to concept/session/handoff.

## Current boundary

- These are user-supplied replacement sources, not newly generated songs or measured recordings. Track 08 has a 100 BPM STYLE and no key/EXCLUDE; Track 09 has no BPM/key/EXCLUDE. The track-prompt gate must report missing values without changing the source. The user reports that Track 08's bracketed voice cues fixed a prior generation problem; the agent has not heard that audio.
