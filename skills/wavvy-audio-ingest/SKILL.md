---
name: wavvy-audio-ingest
description: Collect selected Suno recordings as verified WAV inputs for a Wavvy series. Use after listener selection or when a completed series needs its WAV files downloaded and matched to the track list. For writing prompts use wavvy-suno-batch or wavvy-lyricist.
---

# Wavvy Audio Ingest

Trigger: model-invoked after selected recordings are known. This is separate from generation because a candidate's title alone does not prove that it is the approved audio.

## Steps

1. Read the target series concept, selected candidate record if present, current state, and the `MASTER/WORKFLOWS.md` WAV naming rule. Confirm the approved order and title for every track. A missing selection is a visible stop for that track.
2. Download the selected source as WAV through the browser product and connection method 젠 chose. A user-supplied WAV is equally valid. If a service also creates M4A files, leave them out of the package and report them separately.
3. Probe every WAV's real codec, channels, sample rate, and duration; calculate its SHA-256. Copy it to `SERIES/[series]/input/tracks/` with the project's numbered filename convention. Do not infer measured BPM or key from prompt text; use `NA` when BPM is not known.
4. Write `SERIES/[series]/input/download-manifest.json` with the exact `workspace` used in `suno-candidates.json` and one `tracks` entry per approved order. Each entry has `order`, `approved_title`, `input_filename`, `duration_seconds`, `sha256`, `download_actor`, audio format, and `candidate_id` equal to the selected candidate's stable ID. For a user-supplied WAV with no Suno candidate record, record that source and omit `candidate_id`. Compare the packaged file's hash with the downloaded source. `wavvy-release` runs `validate` after artwork exists and `source-final` after `pack` creates the report; `verify-release` checks this manifest against the actual WAVs, report, and candidate decisions.

## Boundary

Do not replace an approved WAV merely because a same-named candidate exists. Do not delete files from Downloads or original sources as part of ingest. A manifest proves file identity and technical properties, not musical quality or listener approval.
