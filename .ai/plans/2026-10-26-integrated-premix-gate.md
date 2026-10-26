# Integrated 160 premix source gate

Controller-authorized implementation: validate the retained capture → variable 170
correction → two-cycle 170 master → uniform 17/16 160 master → final AAC chain.
Precedent: `wavvy_harness/premixed_audio.py` retains separate legacy repeat and
180/reacquisition paths. Neither schema describes this production.

- Add `integrated_premix.py` with explicit archive schema
  `wavvy.final_integrated_premixed_audio.v1` and the existing producer schemas.
- Bind series-relative selection/capture refs and repository-relative producer
  refs to actual SHA256, selected IDs/titles, valid source frames, full source
  preservation, 40 entries/39 overlaps and exact global 17/16 sample rounding.
- Return sources/rate/samples/normalized chapter entries/audio_ref to the existing
  audio checker. Preserve its separate video-artwork/render checks and old paths.
- Exercise valid production plus mutation tests for identity, timing, hashes,
  missing media, evidence failures and legacy dispatch isolation.
- Read-only validation only: no audio changes, rendering, uploads or commits.

Formal review and release decisions belong to the controller.
