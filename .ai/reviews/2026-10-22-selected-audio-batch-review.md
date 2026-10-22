# 17:30 selected audio batch review

Date: 2026-10-22
Reviewer: isolated Codex reviewer, gpt-6-astra / xhigh
Scope: final 20 selected WAV files, playback order, download manifest, original Downloads files for 1–3, and raw captures/UI evidence for 4–20. Read-only; no playback or file changes by reviewer.

Verdict: **CLEAN — confirmed Critical/High: 0.**

- All 20 input files matched the selected order, IDs, titles, SHA-256 values and actual durations. No pending inputs. Total duration: 3874.85 seconds.
- Official files 1–3 matched their original Downloads copies. Captures 4–20 matched raw/trim-source hashes and every sample in the specified raw slice.
- All inputs were 48 kHz stereo, with finite samples and no internal exact-zero runs of 50 ms or longer.
- Track 20 uses raw 1.28–200.85 seconds, preserves target signal 1.376–200.5847917 seconds, and ends before the next signal at 201.0985 seconds.
- Failed captures 10 and 17 remain separate; registered files use retry1. Track 17's registered file contains signal through the later portions.
- Eleven float samples exceeded absolute amplitude 1 across tracks 5, 12, 15, 16 and 20. Float over-unity alone was not classified as hard clipping.

Limitations: callback PTS was not recorded, so this review does not prove lossless callback continuity, identity to official Suno source waveforms, or subjective listening quality. User listening approval applies to the earlier approved samples and track 4, not automatically to all 20 tracks.

Reviewed manifest SHA-256: `0f268f916ded93bb15df6331504695b0b62a647c7514648e4b97da01ac105ccc`

Reviewed playback-order SHA-256: `39f6eae6d85633a3c770884032c9e18ac46247130ac456a50aa0621854cf055d`

Principle observations: none.
