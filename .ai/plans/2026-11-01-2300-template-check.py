#!/usr/bin/env python3
"""23:00 template lyric check: a new song must keep its type original's lyric shape.

젠 2026-11-01: 「기존 곡 가사 글자 수 그대로 내용만 바꿔」.
Rule checked line by line against the type original's Suno lyrics
(.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json):
  1. Same number of non-empty lines, same order of tag lines vs sung lines.
  2. Tag lines (only [ ... ] groups) are identical to the template.
  3. Each sung line has the same syllable count (Hangul syllables; an English word in the
     template counts its vowel groups, e.g. "little light" = 3). New sung lines are Korean only.
  4. Where the template repeats a sung line, the new lyric repeats the same new line.
Usage: template-check.py <track-number> [--json-out PATH]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NINE = ROOT / ".ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json"
STYLES = ROOT / ".ai/plans/2026-11-01-2300-new-song-styles.json"
TRACKS = ROOT / "SERIES/23-00/input/tracks"
TAG_LINE = re.compile(r"^(\[[^\]]*\]\s*)+$")


def lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def syllables(line):
    hangul = len(re.findall(r"[가-힣]", line))
    english = sum(max(1, len(re.findall(r"[aeiouy]+", word.lower()))) for word in re.findall(r"[A-Za-z]+", line))
    return hangul + english


def main():
    order = int(sys.argv[1])
    out = sys.argv[sys.argv.index("--json-out") + 1] if "--json-out" in sys.argv else None
    plan = {item["order"]: item for item in json.loads(STYLES.read_text(encoding="utf-8"))}[order]
    template_track = next(t for t in json.loads(NINE.read_text(encoding="utf-8"))["tracks"]
                          if t["title_ui"].split(" (")[0] == plan["type"])
    txt = next(TRACKS.glob(f"{order:02d}_*.txt")).read_text(encoding="utf-8")
    new = lines(re.split(r"(?m)^===\s*[A-Z]+\s*===\s*$", txt.split("=== LYRICS ===", 1)[1], maxsplit=1)[0])
    tpl = lines(template_track["lyrics_full"])
    errors, rows = [], []
    if len(new) != len(tpl):
        errors.append(f"line count differs: template {len(tpl)} vs new {len(new)}")
    for i, (t, n) in enumerate(zip(tpl, new), 1):
        t_tag, n_tag = bool(TAG_LINE.match(t)), bool(TAG_LINE.match(n))
        row = {"line": i, "template": t, "new": n}
        if t_tag or n_tag:
            ok = t == n
            row["kind"] = "tag"
            if not ok:
                errors.append(f"line {i}: tag line must equal template: {t!r} vs {n!r}")
        else:
            ts, ns = syllables(t), syllables(n)
            row.update(kind="sung", template_syllables=ts, new_syllables=ns)
            if re.search(r"[A-Za-z]", n):
                errors.append(f"line {i}: new sung line must be Korean only: {n!r}")
            if ts != ns:
                errors.append(f"line {i}: syllables {ns} != template {ts}: {n!r} (template {t!r})")
        rows.append(row)
    for i in range(min(len(tpl), len(new))):
        for j in range(i + 1, min(len(tpl), len(new))):
            if not TAG_LINE.match(tpl[i]) and tpl[i] == tpl[j] and new[i] != new[j]:
                errors.append(f"lines {i+1}/{j+1}: template repeats {tpl[i]!r}, new must repeat too ({new[i]!r} vs {new[j]!r})")
    result = {"track": order, "title": plan["title"], "type": plan["type"], "template_id": template_track["id"],
              "result": "FAIL" if errors else "PASS", "errors": errors, "rows": rows}
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("track", "title", "type", "result", "errors")}, ensure_ascii=False, indent=1))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
