#!/usr/bin/env python3
"""Build the 17 current-selection source txt files and the current-source binding manifest.

Run from the repository root:  python3 -I SERIES/23-00/input/validation/2026-11-04-final-sources/build-final-sources.py
Inputs (read only): input/suno-final-selection-2026-11-04.json, output/report.json,
production/browser-capture-20261104/style-provenance.json (Suno song-detail records).
Lyrics are copied byte-for-byte from tracks[].remix.lyrics_raw (surrounding whitespace of the whole
block is stripped by the harness parser; the raw hash is recorded). Nothing is invented or edited.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SERIES = Path("SERIES/23-00")
sys.path.insert(0, ".")
from wavvy_harness.source import parse_track_source_fields  # noqa: E402

selection = json.loads((SERIES / "input/suno-final-selection-2026-11-04.json").read_text(encoding="utf-8"))
report = json.loads((SERIES / "output/report.json").read_text(encoding="utf-8"))
prov = json.loads((SERIES / "production/browser-capture-20261104/style-provenance.json").read_text(encoding="utf-8"))
by_id = {t["song_id"]: t for t in prov["tracks"]}
report_tracks = {int(t["order"]): t for t in report["tracks"]}

LINEAGE = {
    "confirmed_suno_parent_link": "original song link confirmed (Suno parent link observed)",
    "confirmed_prior_suno_parent_link": "original song link confirmed (prior Suno parent link observed)",
    "inferred_from_title_and_lyrics": "original song candidate matched by title and lyrics (PROVISIONAL, not a confirmed parent)",
    "user_declared_direct_creation": "made directly by 젠 (reply 「이건 직접 만든거야.」, 2026-11-04), current displayed style recorded; no separate original style",
}

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

tracks_out = []
for row in selection["tracks"]:
    order = int(row["order"])
    rt = report_tracks[order]
    t = by_id[row["candidate_id"]]
    assert rt["title"] == row["title"], (order, rt["title"], row["title"])
    remix = t["remix"]
    raw = remix["lyrics_raw"]
    assert sha256_text(raw) == remix["lyrics_raw_sha256"], order
    style = t["combined_style"]
    assert sha256_text(style) == t["combined_style_sha256"], order
    exclude = ", ".join(t["combined_exclude"])
    lineage = t["lineage"]["status"]
    original = t["original"]
    safe_title = re.sub(r"[/:]+", "-", rt["title"]).strip()
    name = f"{order:02d}_{safe_title}.txt"
    record = [
        f"Suno song: {remix['song_id']} ({remix['url']})",
        f"Suno title after numbering: {t['suno_title_after_numbering']}",
        f"Lineage status: {lineage} — {LINEAGE[lineage]}",
    ]
    if original:
        record.append(f"Original song (Suno): {original['title']} ({original['url']})")
    record += [
        f"Style record status: {t['style_record_status']}; assembly mode: {t['assembly_mode']}",
        f"Actual generation input verified: {str(t['actual_generation_input_verified']).lower()}",
        "STYLE/EXCLUDE above are the recorded Suno display text"
        + (" (original STYLE + two LF newlines + remix STYLE; EXCLUDE = minus-prefixed items, original then remix)" if t["assembly_mode"] == "original_plus_remix" else " (current displayed style of the song 젠 made directly)")
        + ". They are a documentation reconstruction, not proof of the exact text submitted to Suno.",
        f"LYRICS above are the Suno song-detail lyrics verbatim (raw sha256 {remix['lyrics_raw_sha256']}); no word or line was edited.",
        f"Evidence: {remix['ui_evidence']} (sha256 {remix['ui_evidence_sha256']}); style-provenance.json tracks[capture {t['capture_index_provisional']}]",
        "Audio BPM/key/vocal were not measured; STYLE wording only.",
    ]
    content = "\n".join([
        f"Track: {remix['title']}",
        f"Order: {order:02d}",
        f"Status: current 17-song selection (2026-11-04); Suno ID {remix['song_id']}; style record {t['style_record_status']}; lineage {lineage}; actual generation input verified: {str(t['actual_generation_input_verified']).lower()}",
        "Type: Lo-Fi Remix (see SOURCE RECORD for lineage)",
        "BPM: unknown",
        "Key: unknown",
        f"Length: {rt['duration']:.2f} s (cut WAV, output/report.json)",
        "Vocal: unknown (not measured; vocal wording appears only inside STYLE)",
        "",
        "=== STYLE ===",
        style,
        "",
        "=== EXCLUDE ===",
        exclude,
        "",
        "=== LYRICS ===",
        raw,
        "",
        "=== SOURCE RECORD ===",
        "\n".join(record),
        "",
    ])
    path = SERIES / "input/tracks" / name
    assert not path.exists(), path
    path.write_text(content, encoding="utf-8")
    metadata, sections = parse_track_source_fields(content)
    assert sections["LYRICS"] == raw.strip(), order
    assert sections["STYLE"] == style.strip(), order
    tracks_out.append({
        "order": order,
        "title": rt["title"],
        "source_txt": f"input/tracks/{name}",
        "source_sha256": sha256_text(content),
        "candidates": [{"id": remix["song_id"], "url": remix["url"]}],
        "lineage_status": lineage,
        "style_record_status": t["style_record_status"],
        "actual_generation_input_verified": t["actual_generation_input_verified"],
        "lyrics_raw_sha256": remix["lyrics_raw_sha256"],
        "lyrics_block_equals_raw_after_strip": sections["LYRICS"] == raw.strip(),
        "lyrics_raw_had_surrounding_whitespace": raw != raw.strip(),
    })

manifest = {
    "schema": "wavvy.current_sources.v1",
    "workspace": "[23:00]",
    "date": "2026-11-04",
    "purpose": "Binds each selected Suno recording in input/suno-final-selection-2026-11-04.json to its current source txt (so finalize-upload can archive it). Not a new selection decision.",
    "selection_ref": "input/suno-final-selection-2026-11-04.json",
    "provenance_ref": "production/browser-capture-20261104/style-provenance.json",
    "builder": "input/validation/2026-11-04-final-sources/build-final-sources.py",
    "tracks": tracks_out,
}
(SERIES / "input/suno-current-sources-2026-11-04.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", len(tracks_out), "txt files + suno-current-sources-2026-11-04.json")
