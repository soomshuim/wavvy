---
name: wavvy-suno-batch
description: Propose the time and musical direction for a new Wavvy series, gather feedback and reference songs, then draft 20 song sources and generate Suno candidates. Use only after the explicit /wavvy-produce or -wavvy-produce command and its active continuation; an ordinary “새 시리즈 만들자” message does not start this workflow.
---

# Wavvy Suno Batch

Trigger: user-invoked through `/wavvy-produce` (Claude) or `-wavvy-produce` (Codex). The explicit command makes the credit-using workflow's start predictable. The command first starts a brief proposal, not Suno generation. Continue the same command after 젠's feedback; do not require a second command. Project load or an ordinary conversation is not a trigger.

## Steps

1. Read `.ai/state.json`, `MASTER/SSOT.md`, relevant completed series concepts, `MASTER/WORKFLOWS.md`, and any direction supplied with the command. Propose two or three compact options, each pairing a series time with main musical themes (for example acoustic, R&B, neo-soul, or indie). Recommend one with a short reason grounded in Wavvy's existing catalogue. Ask 젠 to choose or revise the direction. Do not draft all tracks or open Suno before this feedback.
2. Ask 젠 for two or three reference songs, unless already supplied. Record the artist and title, and which musical qualities to borrow as principles (groove, instrumentation, vocal approach, arrangement) without copying melody or lyrics. If 젠 has no references, record that choice and continue. Once time, theme, and reference direction are settled, write the series concept brief; do not archive unapproved final track sources there.
3. Read `MASTER/lyrics/LYRICS.md`, `MASTER/style/STYLE.md`, `MASTER/roles/ROLES.md`, and the target concept. Establish the 20-track arc, language, variation, and any remix sources. Draft all 20 numbered source txt files under `SERIES/[series]/input/tracks/`. For new lyrics use `wavvy-lyricist` and its full-song review contract. Keep each track's title, vocal direction, Style, Exclude, and Lyrics bound in its txt. Preserve supplied remix sources and explicit user tags. Prevent duplicate concepts and accidental source reuse by comparing the complete 20-track set.
4. Run the existing track-prompt and applicable lyrics-review gates on each new source. Fix failures before submission. These gates check source contracts and recorded review evidence; they do not prove that generated music will sound good.
5. In Suno, create or select the series' `[HH:MM]` folder/workspace (for example `[17:00]`) using the agreed series time. Confirm that workspace is active before submitting each track; stop rather than generate in the default or another series' workspace. Use the browser product and connection method chosen by 젠. Make one initial generation submission per track. Suno currently returns two songs by default for one submission; record both as separate candidates under that one submission, not as two submissions. Record the exact workspace name and returned candidate versions in `SERIES/[series]/input/suno-candidates.json`. Each track entry binds `order`, `title`, `source_txt` (path relative to the series, under `input/tracks/`), `source_sha256`, `candidates` (each with stable `id`, displayed name, and observed status), and `decision` as `{ "status": "pending|keep|regenerate", "chosen_candidate_id": null|"id" }`. Use a stable service ID or full candidate URL as `id`; the selected ID must exactly match a candidate in the list. Report any failed or unmatched submission visibly. Do not silently retry a credit-consuming generation.
6. Present the candidate audio to 젠 for listening selection. Record which version is kept or needs regeneration. Only approved selections move to `wavvy-audio-ingest` and then to the final source archive; rejected candidates remain candidates, not final tracks. Regenerate only the tracks 젠 selected for another pass.

## Boundary

The batch path is the explicit exception in `MASTER/WORKFLOWS.md` to the usual pre-Suno per-track PASS. It does not change the txt-first rule or certify audio quality from prompt gates.
