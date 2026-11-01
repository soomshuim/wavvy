#!/usr/bin/env python3
"""Verify SERIES/23-00 remix txt files and concept Type Styles against the read-only observation.

Run from repo root:  python3 .ai/validation/2026-11-01-2300-foundation/verify-sources.py
Exit code 0 only when every check passes.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from wavvy_harness.gate import _exclude_terms, _user_type_exclude_exception  # noqa: E402
from wavvy_harness.source import parse_track_source_fields  # noqa: E402
from wavvy_harness.state import _markdown_section  # noqa: E402

DATA = json.loads((REPO / ".ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json").read_text(encoding="utf-8"))
ORDER = ["먼지", "산책", "숨", "이름", "마음 밖", "물안개", "골목", "물결", "작은 빛"]
TRACKS = {t["matched_name"]: t for t in DATA["tracks"]}
SERIES = REPO / "SERIES/23-00"
failures: list[str] = []


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail else ""))
    if not ok:
        failures.append(label)


print("== A. nine remix txt vs nine-tracks.json (STYLE / LYRICS) ==")
tracks_dir = SERIES / "input/tracks"
check("input/tracks holds exactly 9 txt files and nothing else", sorted(p.name for p in tracks_dir.iterdir()) == sorted(f"{i:02d}_{n} (Lo-Fi Remix).txt" for i, n in enumerate(ORDER, 1)))
for index, name in enumerate(ORDER, 1):
    track = TRACKS[name]
    path = tracks_dir / f"{index:02d}_{name} (Lo-Fi Remix).txt"
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    metadata, sections = parse_track_source_fields(text)
    style, lyrics = track["style_full"], track["lyrics_full"]
    check(f"{index:02d} {name}: STYLE section == style_full (exact)", sections["STYLE"] == style, f"{len(style)} chars, sha256 {sha(sections['STYLE'])[:16]}")
    check(f"{index:02d} {name}: STYLE sha256 == JSON style_sha256", sha(sections["STYLE"]) == track["style_sha256"])
    check(f"{index:02d} {name}: STYLE UTF-8 bytes appear verbatim in file", style.encode("utf-8") in raw)
    check(f"{index:02d} {name}: LYRICS section == lyrics_full (outer whitespace stripped by parser)", sections["LYRICS"] == lyrics.strip(), f"{len(lyrics.strip())} chars")
    check(f"{index:02d} {name}: LYRICS bytes appear verbatim in file", lyrics.strip().encode("utf-8") in raw)
    if lyrics == lyrics.strip():
        check(f"{index:02d} {name}: LYRICS sha256 == JSON lyrics_sha256", sha(sections["LYRICS"]) == track["lyrics_sha256"])
    else:
        check(f"{index:02d} {name}: LYRICS sha256 == JSON lyrics_sha256 after re-adding the one trailing newline", sha(sections["LYRICS"] + "\n") == track["lyrics_sha256"], "JSON text ends with one newline; parser strips it")
    check(f"{index:02d} {name}: EXCLUDE section present and empty", sections.get("EXCLUDE") == "")
    check(f"{index:02d} {name}: header Track/Order/Status", metadata["Track"] == f"{name} (Lo-Fi Remix)" and metadata["Order"] == f"{index:02d}" and track["id"] in metadata["Status"] and track["url"] in metadata["Status"] and "audio not measured" in metadata["Status"], f"BPM={metadata['BPM']} | Key={metadata['Key']} | Vocal={metadata['Vocal']}")
    check(f"{index:02d} {name}: no new-song edit leaked into the record", not (name == "골목" and "Intimate dry chest-voice Korean lead" in sections["STYLE"]) and (name != "산책" or sections["STYLE"].startswith("Lo-Fi Remix, ")) and (name != "마음 밖" or "lo-fi remix," in sections["STYLE"]))

print("\n== B. concept.md ## Type Styles ==")
concept = (SERIES / "concept.md").read_text(encoding="utf-8")
section = _markdown_section(concept, "Type Styles")
check("Type Styles section found", bool(section))
headings = list(re.finditer(r"^###[ \t]+(.+?)[ \t]*$", section, re.MULTILINE))
check("nine ### type headings in the expected order", [h.group(1) for h in headings] == ORDER, ", ".join(h.group(1) for h in headings))

facts = json.loads((REPO / ".ai/validation/2026-11-01-2300-foundation/02-type-styles-facts.json").read_text(encoding="utf-8"))
EDITS = {"골목": ("Keep the original song’s melodic contour and section flow, with intimate dry chest-voice Korean lead, no harmony layers", "Intimate dry chest-voice Korean lead, no harmony layers"),
         "산책": ("Lo-Fi Remix, ", "Lo-Fi, "), "마음 밖": ("lo-fi remix,", "lo-fi,")}
for position, heading in enumerate(headings):
    name = heading.group(1)
    end = headings[position + 1].start() if position + 1 < len(headings) else len(section)
    body = section[heading.end():end]
    blocks = re.findall(r"```text\n(.*?)\n```", body, re.DOTALL)
    check(f"{name}: two STYLE code blocks (a) and (b)", len(blocks) == 2)
    a, b = blocks
    meta = re.findall(r"\*\*\((a|b)\) [^*]+\*\* — (\d+)자, sha256 `([0-9a-f]{64})`", body)
    check(f"{name}: recorded (a)/(b) char counts and sha256 match the code blocks", meta == [("a", str(len(a)), sha(a)), ("b", str(len(b)), sha(b))], f"(a) {len(a)} {sha(a)[:12]} | (b) {len(b)} {sha(b)[:12]}")
    check(f"{name}: facts file agrees", (facts[name]["original_chars"], facts[name]["original_sha256"], facts[name]["new_song_chars"], facts[name]["new_song_sha256"]) == (len(a), sha(a), len(b), sha(b)))
    if name != "물결":
        check(f"{name}: (a) == workspace style_full verbatim", a == TRACKS[name]["style_full"])
    if name in EDITS:
        old, new = EDITS[name]
        check(f"{name}: (b) == (a) with exactly the one instructed edit", a.count(old) == 1 and b == a.replace(old, new), f"{len(a)} -> {len(b)} chars")
        check(f"{name}: edit and 젠 basis written under (b)", f"`{old}` → `{new}`" in body and "원곡이 없는데 넣는게 뭔 소용이야" in body)
    else:
        check(f"{name}: (b) == (a) (no edit)", a == b)
    exclude_lines = re.findall(r"^[ \t]*[-*+][ \t]+EXCLUDE[ \t]*:[ \t]*(.*?)[ \t]*$", body, re.MULTILINE)
    check(f"{name}: exactly one '- EXCLUDE:' line", len(exclude_lines) == 1)
    expected_exclude = facts[name]["exclude"]
    check(f"{name}: EXCLUDE terms == {len(expected_exclude)} expected", _exclude_terms(exclude_lines[0]) == expected_exclude)

print("\n== C. 물결 type style ==")
mul = next(h for h in headings if h.group(1) == "물결")
mul_body = section[mul.end():]
a = re.findall(r"```text\n(.*?)\n```", mul_body, re.DOTALL)[0]
negatives = TRACKS["물결"]["inline_negative_terms"]
check("물결 STYLE ends with the three words Zen specified", a.endswith(", Modern Indie R&B, Lo-fi Remastered, Articulation"))
check("물결 STYLE contains no U+2011 minus items", "‑" not in a)
check("물결 STYLE is ASCII", a.isascii())
check("물결 STYLE length is 677", len(a) == 677)
exclude13 = [t[1:] for t in negatives]
check("물결 EXCLUDE has 13 items equal to the observed U+2011 items without the symbol", len(exclude13) == 13 and facts["물결"]["exclude"] == exclude13)
print(f"물결 STYLE: {len(a)} chars, sha256 {sha(a)}")
print("물결 EXCLUDE (13): " + ", ".join(exclude13))

print("\n== D. gate helper against the REAL concept.md (no scratch series) ==")
header = {"Style Type": "물결", "Exclude Source": "user-supplied type style"}
check("물결 + exact 13 items -> exception granted", _user_type_exclude_exception(concept, header, exclude13) == ("물결", ""))
swapped = [exclude13[1], exclude13[0]] + exclude13[2:]
check("물결 + two items swapped -> refused", _user_type_exclude_exception(concept, header, swapped)[0] == "")
check("물결 + one item dropped -> refused", _user_type_exclude_exception(concept, header, exclude13[:-1])[0] == "")
check("type not listed -> refused", _user_type_exclude_exception(concept, {**header, "Style Type": "없는타입"}, exclude13)[0] == "")
check("other listed type with the 13 items -> refused (its recorded EXCLUDE is empty)", _user_type_exclude_exception(concept, {**header, "Style Type": "골목"}, exclude13)[0] == "")
check("missing Exclude Source -> refused", _user_type_exclude_exception(concept, {"Style Type": "물결"}, exclude13)[0] == "")

print("\n== E. Track Map ==")
track_map = _markdown_section(concept, "Track Map (numbers are temporary)")
rows = [line for line in track_map.splitlines() if re.match(r"^\| \d{2} \|", line)]
check("Track Map has 20 rows 01-20", [r[2:4] for r in rows] == [f"{i:02d}" for i in range(1, 21)])
check("rows 10-20 are placeholders", all("새 곡 — 설계표 젠 확인 대기" in r for r in rows[9:]))
check("rows 01-09 carry the workspace Suno IDs in order", all(TRACKS[n]["id"] in rows[i] for i, n in enumerate(ORDER)))

print("\nTOTAL FAILURES:", len(failures))
for item in failures:
    print(" -", item)
sys.exit(1 if failures else 0)
