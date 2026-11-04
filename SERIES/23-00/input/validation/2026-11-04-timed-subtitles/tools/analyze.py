#!/usr/bin/env python3
"""Per-track alignment report: python3 analyze.py [track numbers...]"""
import json
import sys
from pathlib import Path

REPO = Path.home() / "Project/wavvy"
SP = Path(__file__).resolve().parent  # scratch layout: probe-raw/, probe-clips/, patched/ were scratch folders; retained copies live in ../audio-probe/
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(SP))
from wavvy_harness.subtitles import _source_lines  # noqa: E402
import align as A  # noqa: E402

SERIES = REPO / "SERIES/23-00"
report = json.loads((SERIES / "output/report.json").read_text(encoding="utf-8"))
tracks = report["tracks"]
concept = (SERIES / "concept.md").read_text(encoding="utf-8")
lines_by_track = _source_lines(concept, [t["order"] for t in tracks])


def fmt(t):
    return f"{int(t // 60):02d}:{t % 60:04.1f}"


def analyze(order, probe_dir=SP / "probe-raw", quiet=False):
    t = tracks[order - 1]
    stem = t["filename"].rsplit(".", 1)[0]
    data = json.loads((probe_dir / f"{stem}-whisper.json").read_text(encoding="utf-8"))
    asr, words = A.asr_chars(data)
    lines = lines_by_track[order]
    lyr = []
    for ln, text in enumerate(lines, 1):
        for ch in A.norm_chars(text):
            lyr.append((ch, ln))
    matches = A.align(lyr, asr)
    per = {ln: [] for ln in range(1, len(lines) + 1)}
    used = set()
    for li, aj, s in matches:
        if s > 0:
            per[lyr[li][1]].append((li, aj, s))
            used.add(aj)
    rows = []
    for ln, text in enumerate(lines, 1):
        total = len(A.norm_chars(text))
        ms = per[ln]
        cov = len(ms) / total if total else 0
        if ms:
            st = asr[ms[0][1]][1]
            en = asr[ms[-1][1]][2]
        else:
            st = en = None
        rows.append((ln, text, total, len(ms), cov, st, en))
    # unmatched ASR runs
    runs, cur = [], []
    for j, a in enumerate(asr):
        if j in used:
            if cur:
                runs.append(cur)
                cur = []
        else:
            cur.append(j)
    if cur:
        runs.append(cur)
    out = []
    out.append(f"=== {order:02d} {t['title']} dur={t['duration']:.2f}s lines={len(lines)} asr_chars={len(asr)}")
    for ln, text, total, k, cov, st, en in rows:
        flag = "" if cov >= 0.7 else (" WEAK" if cov >= 0.35 else " MISSING")
        when = f"{fmt(st)}-{fmt(en)}" if st is not None else "      --      "
        out.append(f"  {ln:3d} {when} cov={cov:4.2f} ({k}/{total}){flag}  {text}")
    out.append("  -- unmatched ASR runs (>=4 chars):")
    for r in runs:
        if len(r) >= 4:
            txt = "".join(asr[j][0] for j in r)
            out.append(f"     {fmt(asr[r[0]][1])}-{fmt(asr[r[-1]][2])} {txt}")
    if not quiet:
        print("\n".join(out))
    return rows, runs, asr, data


if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or list(range(1, 18))
    for n in nums:
        analyze(n)
