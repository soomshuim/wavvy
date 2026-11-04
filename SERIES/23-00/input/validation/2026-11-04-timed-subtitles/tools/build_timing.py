#!/usr/bin/env python3
"""Build the 23:00 timed-subtitle timing map from retained Whisper word times.

Approved lyric lines are the only text used.  Recognized text only places those
lines on the time axis (ASR estimate, not human listening).

Run (system python3, from anywhere):  python3 -I build_timing.py [--write]
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path.home() / "Project/wavvy"
SP = Path(__file__).resolve().parent  # scratch layout: probe-raw/, probe-clips/, patched/ were scratch folders; retained copies live in ../audio-probe/
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(SP))
import align as A  # noqa: E402
from wavvy_harness.subtitles import _source_lines  # noqa: E402

SERIES = REPO / "SERIES/23-00"
VAL = SERIES / "input/validation/2026-11-04-timed-subtitles"
report = json.loads((SERIES / "output/report.json").read_text(encoding="utf-8"))
tracks = report["tracks"]
concept = (SERIES / "concept.md").read_text(encoding="utf-8")
LINES = _source_lines(concept, [t["order"] for t in tracks])

FULL = lambda n: f"{tracks[n-1]['filename'].rsplit('.', 1)[0]}-whisper.json"  # noqa: E731
PROBE_RAW = SP / "probe-raw"
PROBE_CLIPS = SP / "probe-clips"

# ---------------------------------------------------------------- decisions
# Approved lines that are not sung in the audio (evidence in comments / notes).
UNSUNG = {
    2: {21: "second 누가/빛이 pair of the bridge is not sung (the audio sings the pair once)",
        22: "second 누가/빛이 pair of the bridge is not sung (the audio sings the pair once)"},
    3: {1: "bare direction line 'instrumental' under [Intro]"},
    5: {1: "bare direction line 'instrumental' under [Intro]"},
    7: {1: "bare direction line 'instrumental' under [Intro]"},
    9: {1: "bare direction line 'instrumental' under [Intro]"},
    12: {41: "stage direction '(deep breath)' under [Breakdown]; no speech recognized in the 145.6-166.5 s breakdown window while music continues (about -15 dB)",
         42: "'후...' under [Breakdown]; no speech recognized in the 145.6-166.5 s breakdown window while music continues (about -15 dB)"},
}
# Re-recognized short windows replace the full-pass placement of weak lines.
# (track, clip stem, [t0, t1] absolute seconds of ASR words to use, lines)
RECHECK = [
    (15, "check-15-verse2-missing-75-115", (88.0, 105.3), [17, 18, 19, 20, 21, 22]),
    (15, "check-15-verse2-missing-b-105-145", (105.0, 114.45), [23, 24, 25]),
    (15, "check-15-weak-line5-15-50", (29.9, 33.6), [5]),
    (6, "check-06-weak-line36-125-160", (130.0, 140.0), [35, 36]),
    (5, "check-05-weak-line29-80-110", (89.0, 93.0), [28, 29]),
    (9, "check-09-weak-line43-120-150", (128.0, 132.4), [42, 43]),
    (13, "check-13-weak-final-chorus-140-175", (148.0, 152.0), [41]),
    (13, "check-13-weak-final-chorus-140-175", (160.6, 165.9), [44, 45]),
    (2, "check-02-bridge-weak-95-135", (129.9, 133.6), [28]),
]
# Sung repeats beyond the approved text: (track, [lines], occurrence, clip stem, (t0,t1))
EXTRAS = [
    (8, [22], 1, "check-08-extra-repeat-a-100-135", (123.0, 125.76)),   # occurrence 1 (first copy)
    (8, [22], 2, "check-08-extra-repeat-a-100-135", (125.76, 130.5)),   # occurrence 2
    (8, [26], 1, "check-08-extra-repeat-b-140-175", (170.0, 172.8)),
    (8, [26], 2, "check-08-extra-repeat-b-140-175", (172.8, 176.0)),
    (10, [23, 24, 25, 26], 2, "check-10-extra-chorus-85-153", (123.5, 137.5)),
    (16, [19, 20, 21, 22], 2, "check-16-extra-chorus-165-206", (179.0, 203.5)),
]
# These (track, line) primary placements come from EXTRAS windows instead of the DP.
PRIMARY_FROM_EXTRAS = {(8, 22), (8, 26)}

MIN_MS = 700
GAP_MS = 100


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def clip_chars(stem, t0, t1):
    data = load_json(PROBE_CLIPS / f"{stem}-whisper.json")
    off = float(data["clip_start_s"])
    chars, _ = A.asr_chars(data)
    out = [(c, s + off, e + off, w) for c, s, e, w in chars if t0 <= s + off <= t1 + 0.001]
    return out


def place_lines(lines, asr, tail_rate_default=0.3):
    """lines: list[(line_no, text)]; asr: chars with absolute times.  -> {line: info}"""
    lyr = [(ch, ln) for ln, text in lines for ch in A.norm_chars(text)]
    matches = A.align(lyr, asr) if lyr and asr else []
    per = {ln: [] for ln, _ in lines}
    for li, aj, s in matches:
        if s > 0:
            per[lyr[li][1]].append((li, aj, s))
    out = {}
    pos = 0
    first_idx = {}
    for ln, text in lines:
        n = len(A.norm_chars(text))
        first_idx[ln] = (pos, n)
        pos += n
    for ln, text in lines:
        base, n = first_idx[ln]
        ms = per[ln]
        if not ms:
            out[ln] = None
            continue
        st_obs, en_obs = asr[ms[0][1]][1], asr[ms[-1][1]][2]
        k0 = ms[0][0] - base            # index of first matched char within line
        k1 = ms[-1][0] - base           # index of last matched char
        span_chars = max(k1 - k0 + 1, 1)
        rate = (en_obs - st_obs) / span_chars if en_obs > st_obs else tail_rate_default
        start = st_obs - k0 * rate
        end = en_obs + (n - 1 - k1) * rate
        out[ln] = dict(line=ln, text=text, matched=len(ms), total=n, cov=len(ms) / n,
                       obs_start=st_obs, obs_end=en_obs, start=start, end=end,
                       lead_extrapolated_chars=k0, tail_extrapolated_chars=n - 1 - k1)
    return out


def main(write=False):
    result = {}
    warnings = []
    evidence_used = {}  # rel path -> kind
    for t in tracks:
        n = int(t["order"])
        lines = [(ln, text) for ln, text in enumerate(LINES[n], 1) if ln not in UNSUNG.get(n, {})]
        data = load_json(PROBE_RAW / FULL(n))
        asr, _ = A.asr_chars(data)
        placed = place_lines(lines, asr)
        evidence_used[f"audio-probe/{FULL(n)}"] = "full-track"
        entries = []  # one per (line, occurrence)
        for ln, text in lines:
            if (n, ln) in PRIMARY_FROM_EXTRAS:
                continue
            info = placed.get(ln)
            entries.append(dict(info or dict(line=ln, text=text, cov=0.0, start=None, end=None), occ=1,
                                evidence=f"audio-probe/{FULL(n)}", source="full_pass"))
        # weak-line re-recognition
        for (tn, stem, (t0, t1), ls) in RECHECK:
            if tn != n:
                continue
            sub = [(ln, LINES[n][ln - 1]) for ln in ls]
            win = place_lines(sub, clip_chars(stem, t0, t1))
            ev = f"audio-probe/{stem}-whisper.json"
            evidence_used[ev] = "weak-line-recheck"
            for e in entries:
                if e["line"] in ls and e["occ"] == 1 and win.get(e["line"]):
                    e.update(win[e["line"]])
                    e.update(evidence=ev, source="clip_recheck")
        # extras / explicit windows
        for (tn, ls, occ, stem, (t0, t1)) in EXTRAS:
            if tn != n:
                continue
            sub = [(ln, LINES[n][ln - 1]) for ln in ls]
            win = place_lines(sub, clip_chars(stem, t0, t1))
            ev = f"audio-probe/{stem}-whisper.json"
            evidence_used[ev] = "sung-repeat" if occ > 1 else "explicit-window"
            for ln in ls:
                if win.get(ln) is None:
                    warnings.append(f"track {n} line {ln} occ {occ}: no match in window")
                    continue
                entries.append(dict(win[ln], occ=occ, evidence=ev, source="clip_extra" if occ > 1 else "clip_explicit"))
        entries.sort(key=lambda e: (e["start"] if e["start"] is not None else 1e9, e["line"]))
        # sanity: monotone starts, line order for occ==1
        firsts = [e["line"] for e in entries if e["occ"] == 1]
        if firsts != sorted(firsts):
            warnings.append(f"track {n}: first-occurrence line order not monotone: {firsts}")
        missing = [e["line"] for e in entries if e["start"] is None]
        if missing:
            warnings.append(f"track {n}: lines without placement: {missing}")
        result[n] = entries
    return result, warnings, evidence_used


if __name__ == "__main__" and "--cues" not in sys.argv:
    res, warns, ev = main()
    for n, entries in res.items():
        print(f"--- {n:02d} {tracks[n-1]['title']}")
        for e in entries:
            s = e.get("start")
            print(f"  L{e['line']:2d}.{e['occ']} {s if s is None else round(s,2)}-{e.get('end') if e.get('end') is None else round(e['end'],2)} cov={e.get('cov',0):.2f} {e['source']} {e['text']}")
    print("WARNINGS", warns)


# ------------------------------------------------------------------ cues
def classes_for(e):
    cls = []
    src = e["source"]
    weak = e.get("cov", 0) < 0.7
    if src == "full_pass":
        cls.append("weak_asr_match" if weak else "direct_cue")
    elif src in ("clip_recheck", "clip_explicit"):
        cls.append("clip_recheck")
        if weak:
            cls.append("weak_asr_match")
    elif src == "clip_extra":
        cls.append("sung_repeat_clip")
    if e.get("lead_extrapolated_chars", 0):
        cls.append("opening_chars_extrapolated")
    if e.get("tail_extrapolated_chars", 0):
        cls.append("ending_chars_extrapolated")
    if e.get("boundary_estimated"):
        cls.append("boundary_estimated")
    return cls


def make_cues(entries, duration_ms, warnings, track_no):
    ents = sorted(entries, key=lambda e: (e["start"], e["line"], e["occ"]))
    # Extrapolated edges (unmatched opening/ending characters) never cross the neighbouring
    # observed ASR times; residual overlap is split at the midpoint and labelled.
    for k, e in enumerate(ents):
        lo = ents[k - 1]["obs_end"] if k else 0.0
        hi_end = ents[k + 1]["obs_start"] if k + 1 < len(ents) else duration_ms / 1000
        e["start_c"] = min(max(e["start"], lo), e["obs_start"])
        e["end_c"] = max(min(e["end"], hi_end), e["obs_end"])
        e["boundary_estimated"] = False
    for k in range(len(ents) - 1):
        a, b = ents[k], ents[k + 1]
        if b["start_c"] < a["end_c"]:
            mid = (b["start_c"] + a["end_c"]) / 2
            a["end_c"], b["start_c"] = mid, mid
            a["boundary_estimated"] = b["boundary_estimated"] = True
    for e in ents:
        e["s_ms"] = max(0, round(e["start_c"] * 1000))
        e["e_ms"] = round(e["end_c"] * 1000)
    groups, i = [], 0
    while i < len(ents):
        grp = [ents[i]]
        reason = None
        while len(grp) < 2 and i + len(grp) < len(ents):
            nxt = ents[i + len(grp)]
            cur = grp[-1]
            if (cur["e_ms"] - cur["s_ms"]) < MIN_MS and (nxt["s_ms"] - cur["s_ms"]) < 1600:
                reason = "short_spacing"
                grp.append(nxt)
            else:
                break
        groups.append((grp, reason))
        i += len(grp)
    cues = []
    for gi, (grp, reason) in enumerate(groups):
        start = grp[0]["s_ms"]
        obs_end = max(g["e_ms"] for g in grp)
        next_start = groups[gi + 1][0][0]["s_ms"] if gi + 1 < len(groups) else duration_ms
        end = min(obs_end, next_start - GAP_MS)
        cls = []
        for g in grp:
            for c in classes_for(g):
                if c not in cls:
                    cls.append(c)
        last_bound = obs_end
        if end - start < MIN_MS:
            ext = min(start + MIN_MS, next_start - GAP_MS)
            if ext > end:
                end = ext
            if end > obs_end:
                last_bound = None
                cls.append("estimated_min_display")
        if reason:
            cls.append(reason)
        if end - start < 500:
            warnings.append(f"track {track_no}: very short cue {start}-{end} {[g['line'] for g in grp]}")
        if end - start > 9000:
            warnings.append(f"track {track_no}: long cue {start}-{end} {[g['line'] for g in grp]}")
        cues.append(dict(
            first_line=grp[0]["line"], last_line=grp[-1]["line"],
            texts=[g["text"] for g in grp],
            relative_start_ms=start, relative_end_ms=end,
            last_asr_end_ms=last_bound,
            anchor_classes=cls or ["direct_cue"],
            grouping_reason=reason,
            line_evidence=[dict(line=g["line"], occurrence=g["occ"], text=g["text"], asr_char_coverage=round(g.get("cov", 0), 3),
                                relative_start_ms=g["s_ms"], observed_end_ms=g["e_ms"], source=g["source"],
                                evidence=g["evidence"]) for g in grp],
            source_line_occurrences=[dict(source_line=g["line"], occurrence=g["occ"], text=g["text"]) for g in grp],
            reading_duration_ms=end - start,
            track=track_no, title=tracks[track_no - 1]["title"], warnings=[],
        ))
    return cues


def build_all():
    res, warns, ev = main()
    out = {}
    for t in tracks:
        n = int(t["order"])
        dur_ms = round(t["duration"] * 1000)
        out[n] = make_cues(res[n], dur_ms, warns, n)
    return out, warns, ev


if __name__ == "__main__" and "--cues" in sys.argv:
    cues, warns, ev = build_all()
    for n, cs in cues.items():
        print(f"=== {n:02d} {tracks[n-1]['title']} cues={len(cs)}")
        for k, c in enumerate(cs, 1):
            lines = "/".join(f"{o['source_line']}.{o['occurrence']}" for o in c["source_line_occurrences"])
            print(f"  {k:2d} {c['relative_start_ms']/1000:7.2f}-{c['relative_end_ms']/1000:7.2f} ({c['reading_duration_ms']/1000:4.1f}s) L{lines:7s} {' | '.join(c['texts'])}   {','.join(c['anchor_classes'])}")
    print("WARNINGS", warns)
