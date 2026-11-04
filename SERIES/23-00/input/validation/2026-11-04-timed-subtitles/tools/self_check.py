#!/usr/bin/env python3
"""Independent self-check of the candidate timed SRT (does not import the harness validators).

Reads: candidate SRT, output/report.json, the timing map, the retained Whisper probes.
Writes: self-check-result.json next to the timing map.
"""
import hashlib
import json
import re
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO = Path.home() / "Project/wavvy"
SP = Path(__file__).resolve().parent  # scratch layout: probe-raw/, probe-clips/, patched/ were scratch folders; retained copies live in ../audio-probe/
SERIES = REPO / "SERIES/23-00"
VAL = SERIES / "input/validation/2026-11-04-timed-subtitles"
srt_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SP / "candidate.srt"

report = json.loads((SERIES / "output/report.json").read_text(encoding="utf-8"))
tmap = json.loads((VAL / "all-tracks-timed-checked.json").read_text(encoding="utf-8"))
raw = srt_path.read_text(encoding="utf-8")
blocks = [b for b in raw.strip().split("\n\n")]
TS = re.compile(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})")


def ms(h, m, s, f):
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(f)


cues = []
errors = []
for k, b in enumerate(blocks, 1):
    lines = b.split("\n")
    if lines[0] != str(k):
        errors.append(f"cue {k}: number {lines[0]!r}")
    m = TS.fullmatch(lines[1])
    if not m:
        errors.append(f"cue {k}: bad time line {lines[1]!r}")
        continue
    s, e = ms(*m.groups()[:4]), ms(*m.groups()[4:])
    cues.append((k, s, e, lines[2:]))

D = lambda x: Decimal(str(x))  # noqa: E731
fade = D(report["processing_params"]["fade"])
durs = [D(t["duration"]) for t in report["tracks"]]
video_ms = int((sum(durs) * 2 - fade * (len(durs) * 2 - 1)).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 1000) // 1000
video_ms = int(((sum(durs) * 2 - fade * (len(durs) * 2 - 1)) * 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
pass_offset = int(((sum(durs) - fade * len(durs)) * 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

res = {"srt": str(srt_path.name), "srt_sha256": hashlib.sha256(srt_path.read_bytes()).hexdigest(), "cues": len(cues)}
prev_end = -1
overlaps = [k for (k, s, e, _) in cues if False]
for k, s, e, _ in cues:
    if s < prev_end:
        overlaps.append(k)
    if e <= s:
        errors.append(f"cue {k}: non-positive length")
    prev_end = e
res["numbering_consecutive"] = all(c[0] == i for i, c in enumerate(cues, 1))
res["overlapping_cues"] = overlaps
res["video_duration_ms_from_report"] = video_ms
res["last_cue_end_ms"] = cues[-1][2]
res["inside_video"] = cues[-1][2] <= video_ms and cues[0][1] >= 0
lens = [e - s for _, s, e, _ in cues]
res["cue_length_ms"] = {"min": min(lens), "median": int(statistics.median(lens)), "max": max(lens),
                        "under_700ms": sum(1 for x in lens if x < 700), "under_900ms": sum(1 for x in lens if x < 900),
                        "over_6000ms": sum(1 for x in lens if x > 6000), "over_8000ms": sum(1 for x in lens if x > 8000)}
gaps = [cues[i + 1][1] - cues[i][2] for i in range(len(cues) - 1)]
res["min_gap_between_cues_ms"] = min(gaps)
res["max_lines_per_cue"] = max(len(c[3]) for c in cues)

# second pass equals first pass shifted by the actual repeat offset
half = len(cues) // 2
same_text = all(cues[i][3] == cues[i + half][3] for i in range(half)) and len(cues) == 2 * half
shifts = {cues[i + half][1] - cues[i][1] for i in range(half)} | {cues[i + half][2] - cues[i][2] for i in range(half)}
res["second_pass"] = {"first_pass_cues": half, "same_text_as_first_pass": same_text,
                      "start_end_shift_ms_set": sorted(shifts), "report_repeat_offset_ms": pass_offset,
                      "shift_equals_report_offset": shifts == {pass_offset}}
# the report's actual second-pass start of track 1 (also confirmed by audio match in concept.md: 3326.668 s)
res["second_pass"]["report_track1_second_pass_start_s"] = float(sum(durs) - fade * len(durs))

# text check: every displayed line is an approved line (or its approved repeat), in approved order per track
sys.path.insert(0, str(REPO))
from wavvy_harness.subtitles import _source_lines  # noqa: E402

concept = (SERIES / "concept.md").read_text(encoding="utf-8")
LINES = _source_lines(concept, [t["order"] for t in report["tracks"]])
per_track = []
text_errors = []
idx = 0
for item in tmap["tracks"]:
    n = item["track"]
    approved = LINES[n]
    unsung = {u["source_line"] for u in item.get("unsung_source_lines", [])}
    shown = [o for c in item["cues"] for o in c["source_line_occurrences"]]
    firsts = [o["source_line"] for o in shown if o["occurrence"] == 1]
    extras = [o for o in shown if o["occurrence"] > 1]
    ok_order = firsts == [i for i in range(1, len(approved) + 1) if i not in unsung]
    ok_text = all(o["text"] == approved[o["source_line"] - 1] for o in shown)
    n_cues = len(item["cues"])
    # same text in the SRT
    srt_texts = [c[3] for c in cues[idx: idx + n_cues]]
    map_texts = [c["texts"] for c in item["cues"]]
    if srt_texts != map_texts:
        text_errors.append(f"track {n}: SRT texts differ from timing map")
    idx += n_cues
    per_track.append({"track": n, "title": item["title"], "approved_lines": len(approved), "unsung_lines": sorted(unsung),
                      "cues": n_cues, "extra_sung_repeat_lines": len(extras), "approved_order_kept": ok_order,
                      "text_equals_approved": ok_text})
    if not ok_order or not ok_text:
        text_errors.append(f"track {n}: order/text check failed")
res["tracks"] = per_track
res["text_errors"] = text_errors
res["total_extra_repeat_lines_per_pass"] = sum(t["extra_sung_repeat_lines"] for t in per_track)

# independent re-recognition agreement: compare cue starts (full pass) with each short-window probe
sys.path.insert(0, str(SP))
import align as A  # noqa: E402

agree = []
probe_dir = VAL / "audio-probe"
for p in sorted(probe_dir.glob("check-*-whisper.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    off = float(d["clip_start_s"])
    n = int(p.name.split("-")[1])
    item = next(t for t in tmap["tracks"] if t["track"] == n)
    chars, _ = A.asr_chars(d)
    chars = [(c, s + off, e + off, w) for c, s, e, w in chars]
    lo, hi = off, float(d["clip_end_s"])
    lines_in = []
    for c in item["cues"]:
        for o in c["source_line_occurrences"]:
            ev = next((e for e in c["line_evidence"] if e["line"] == o["source_line"] and e["occurrence"] == o["occurrence"]), None)
            if ev and ev["source"] == "full_pass" and lo + 3 <= ev["relative_start_ms"] / 1000 <= hi - 5 and ev["asr_char_coverage"] >= 0.8:
                lines_in.append((o["source_line"], o["text"], ev["relative_start_ms"]))
    if not lines_in:
        continue
    t_lo = min(st for _, _, st in lines_in) / 1000 - 3
    t_hi = max(st for _, _, st in lines_in) / 1000 + 12
    chars = [c for c in chars if t_lo <= c[1] <= t_hi]
    lyr = [(ch, ln) for ln, text, _ in lines_in for ch in A.norm_chars(text)]
    matches = A.align(lyr, chars)
    first = {}
    for li, aj, s in matches:
        if s > 0 and lyr[li][1] not in first:
            first[lyr[li][1]] = chars[aj][1]
    deltas = [abs(first[ln] * 1000 - st) for ln, _, st in lines_in if ln in first]
    if deltas:
        agree.append({"probe": p.name, "track": n, "lines_compared": len(deltas),
                      "median_onset_delta_ms": int(statistics.median(deltas)), "max_onset_delta_ms": int(max(deltas))})
res["clip_vs_full_pass_onset_agreement"] = agree
allm = [a["median_onset_delta_ms"] for a in agree]
res["clip_vs_full_pass_summary"] = {"probes_compared": len(agree), "lines_compared": sum(a["lines_compared"] for a in agree),
                                    "median_of_probe_medians_ms": int(statistics.median(allm)) if allm else None,
                                    "max_onset_delta_ms": max((a["max_onset_delta_ms"] for a in agree), default=None)}
res["errors"] = errors
res["result"] = "PASS" if (not errors and not text_errors and not overlaps and res["inside_video"]
                             and res["numbering_consecutive"] and same_text and res["second_pass"]["shift_equals_report_offset"]) else "FAIL"
res["scope"] = ("structure, approved text/order, retained hashes, repeat offset and cue readability; timing is ASR-derived and "
                "was not verified by human listening or full acoustic verification")
out = VAL / "self-check-result.json"
out.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: res[k] for k in res if k not in ("tracks", "clip_vs_full_pass_onset_agreement")}, ensure_ascii=False, indent=1))
print("agreement probes:", len(agree), "max delta:", max((a["max_onset_delta_ms"] for a in agree), default=None))
