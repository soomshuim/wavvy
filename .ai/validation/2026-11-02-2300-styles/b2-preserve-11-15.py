#!/usr/bin/env python3
"""B2 step 1: preserve the current txt and lyric record of tracks 11-15 before the original-style apply.

Copies to SERIES/23-00/input/source-history/2026-11-02-before-original-style/ (txt) and its lyrics-records/ (record),
refuses to overwrite, and compares sha256 of source and copy (fail-closed: empty or missing file is a failure).
Writes the raw result to b2-preserve-11-15.json.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path.home() / "Project/wavvy"
HIST = ROOT / "SERIES/23-00/input/source-history/2026-11-02-before-original-style"
TRACKS = ROOT / "SERIES/23-00/input/tracks"
LYRICS = ROOT / ".ai/lyrics"
OUT = ROOT / ".ai/validation/2026-11-02-2300-styles/b2-preserve-11-15.json"
SONGS = {11: "라디오", 12: "스웨터", 13: "편지", 14: "기타", 15: "노을"}


def sha(path):
    data = path.read_bytes()
    if not data:
        raise SystemExit(f"empty file: {path}")
    return hashlib.sha256(data).hexdigest()


def main():
    (HIST / "lyrics-records").mkdir(parents=True, exist_ok=True)
    rows, failed = [], False
    for n, title in SONGS.items():
        pairs = [
            ("txt", TRACKS / f"{n:02d}_{title}.txt", HIST / f"{n:02d}_{title}.txt"),
            ("record", LYRICS / f"2026-11-01_23-00_{n}_{title}-full-draft.md",
             HIST / "lyrics-records" / f"2026-11-01_23-00_{n}_{title}-full-draft.md"),
        ]
        for kind, src, dst in pairs:
            if not src.is_file():
                raise SystemExit(f"missing source: {src}")
            if dst.exists():
                raise SystemExit(f"refuse to overwrite: {dst}")
            before = sha(src)
            shutil.copy2(src, dst)
            after = sha(dst)
            ok = before == after and len(before) == 64
            failed |= not ok
            rows.append({"track": n, "kind": kind, "src": str(src.relative_to(ROOT)), "dst": str(dst.relative_to(ROOT)),
                         "src_sha256": before, "dst_sha256": after, "match": ok})
    OUT.write_text(json.dumps({"result": "FAIL" if failed else "PASS", "rows": rows}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"result": "FAIL" if failed else "PASS", "rows": len(rows)}, ensure_ascii=False))
    for r in rows:
        print(r["track"], r["kind"], r["src_sha256"], "MATCH" if r["match"] else "MISMATCH")
    sys.exit(1 if failed else 0)


main()
