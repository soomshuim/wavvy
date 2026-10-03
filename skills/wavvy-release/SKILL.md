---
name: wavvy-release
description: Coordinate a selected Wavvy series from verified WAVs through approved artwork, 4K packaging, and YouTube publication. Use after the explicit /wavvy-release or -wavvy-release command and its active continuation; automatically start a thumbnail draft and pause for its visual approval. For a new 20-song series use /wavvy-produce or -wavvy-produce first.
---

# Wavvy Release

Trigger: user-invoked through `/wavvy-release` (Claude) or `-wavvy-release` (Codex) for the full release pipeline. Continue after its visual approval without asking for another command. Project load or an ordinary discussion does not start rendering or publication. A direct request for one specific action can use its narrower skill without starting this full pipeline. This skill coordinates the shared skills and `wavvy.py`; it does not create another media pipeline.

## Steps

1. Read `.ai/state.json`, `MASTER/SSOT.md`, `MASTER/ai/RUNTIME_RULES.md`, `MASTER/cli/SPEC.md`, `MASTER/youtube/YOUTUBE.md`, and the target series `concept.md`. Check current gates and reuse approved sources, selected recordings, existing artwork, and completed outputs. Determine the next missing stage from evidence.
2. If selected audio is missing, use `wavvy-audio-ingest`. Check the approved order, source identity, file probes, and hashes. Do not package an unselected candidate or a failing source.
3. Automatically use `wavvy-thumbnail`: show a small scene draft, collect 젠's approval or revision, then make and inspect the final 4K background and typographic thumbnail. If the series already has approved final artwork, verify it and continue without regenerating it.
4. Draft the YouTube title, description, and tags in the concept before packaging so `pack` can populate `upload.csv`; leave chapter starts pending until the render report exists. Run `python3 wavvy.py validate SERIES/[series]`, then a 30-second preview with `python3 wavvy.py preview SERIES/[series] --sec 30` and inspect its visual and audio result. Run `python3 wavvy.py pack SERIES/[series] -y`, retaining the two-pass playlist required by `MASTER/cli/SPEC.md`. After the report exists, run `python3 wavvy.py finalize-upload SERIES/[series] --check`, then `python3 wavvy.py finalize-upload SERIES/[series] --keep-txt` to write the verified source archive while retaining txt. Run `python3 wavvy.py prepare-subtitles SERIES/[series]` to extract sung lines from that archive into the untimed YouTube subtitle file, repeating the lyrics as many times as the render report says; review the text before upload. An existing edited subtitle is preserved and a mismatch stops for review. Check the `source-final` and `render-final` gates. If YouTube requires a different container or audio codec, create an upload copy from the rendered master and verify its streams, dimensions, duration, and chapter starts; keep the master and upload copy distinct. Follow `MASTER/ai/RUNTIME_RULES.md` for media tools and artifact retention.
5. After finalizing the report-derived chapter list in the concept and `output/upload.csv`, run `python3 wavvy.py verify-release SERIES/[series] --json`; fix every mismatch before upload. Use `wavvy-youtube-publish` for metadata, upload-ready gate, private upload, scheduling or publication, and later public-page/comment verification. Chapter starts come from `output/report.json`, not target song durations.
6. Record actual state in the series concept, `.ai/state.json`, and the project session log. Keep pending processing, scheduled publication, and unposted comments separate from verified results. Report exact artifacts and the next real dependency.

## Boundary

The only planned human pause within an otherwise ready release is the visual draft approval or a genuinely missing publishing choice. Do not treat a source gate as listener approval, an approved thumbnail draft as a 4K artifact, or a scheduled upload as a published video.
