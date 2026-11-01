#!/usr/bin/env python3
"""Build .ai/plans/2026-11-02-2300-final-styles.json from the original-styles survey.

Final STYLE = `Lo-fi Remix, ` + the original STYLE, with only the edits listed per song.
Every edit is an exact substring operation (old -> new) applied in order, so the final
STYLE can be reproduced from the original STYLE and edits[] alone (a2-check.py does that).
Original STYLE text is re-read from the source concept.md files (not re-typed).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SURVEY = ROOT / ".ai/plans/2026-11-02-2300-original-styles.json"
OUT = ROOT / ".ai/plans/2026-11-02-2300-final-styles.json"

PREFIX = "Lo-fi Remix, "
Q_PREFIX = "공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외"
Q_SAFE = "Lo-fi remix는 붙여야해 안전빵이야"
Q_HYPHEN = "- 붙은 스타일은 exclude인거 알지?"
Q_JUDGE = "그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야"
Q_TEMPO = "원곡 BPM 그대로"
Q_MALE = "원곡대로 남성"

# survey type name -> txt header / concept heading type name (header uses a space)
TYPE_NAME = {"마음밖": "마음 밖"}

# Suno parameters recorded in the original concepts (values re-verified against the cited lines).
SUNO_RECORDED = {
    "먼지": (20, 80, "SERIES/14-00/concept.md:976-980"),
    "산책": (25, 75, "SERIES/14-00/concept.md:361-365"),
    "물결": (20, 80, "SERIES/14-00/concept.md:673-677"),
}
SUNO_UNRECORDED_NOTE = {
    "마음밖": "SERIES/04-00/concept.md에 Weirdness·Style Influence 기록 없음",
    "작은 빛": "SERIES/22-00/concept.md에 Weirdness·Style Influence 기록 없음",
    "물안개": "SERIES/04-00/concept.md에 Weirdness·Style Influence 기록 없음",
    "골목": "SERIES/18-00/concept.md:1113-1118에 숫자 대신 `기존 싱글`",
    "이름": "SERIES/18-00/concept.md:1416-1421에 숫자 대신 `기존 싱글`",
}

# gate.py regexes (wavvy_harness/gate.py), copied so this script has no import dependency.
KEY_MODE_RE = re.compile(r"(?<![A-Za-z])([A-G](?:#|b|♯|♭)?)\s+(Major|Minor)\b", re.IGNORECASE)
STYLE_BPM_RE = re.compile(r"(?<!\d)(\d{1,3})\s*BPM\b", re.IGNORECASE)
STYLE_BPM_RANGE_RE = re.compile(r"(?<!\d)\d{1,3}\s*(?:[-–—~]|to)\s*\d{1,3}\s*BPM\b", re.IGNORECASE)
VOCAL_GENDER_RE = re.compile(r"(?<![A-Za-z])(female|male)(?![A-Za-z])|여성|남성", re.IGNORECASE)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_lines(rel: str, span: str) -> str:
    a, b = (int(x) for x in span.split("-"))
    lines = (ROOT / rel).read_text(encoding="utf-8").split("\n")
    return "\n".join(lines[a - 1 : b])


def only_line(style: str, startswith: str) -> str:
    hits = [ln for ln in style.split("\n") if ln.startswith(startswith)]
    assert len(hits) == 1, (startswith, hits)
    return hits[0]


def build_edits(entry: dict, original: str) -> tuple[list[dict], list[str], dict]:
    """Return (edits, moved_inline_items, bookkeeping)."""
    edits: list[dict] = []
    moved: list[str] = []
    book: dict = {}
    order = entry["order"]

    edits.append({
        "id": "E-prefix",
        "kind": "prepend_lofi_remix",
        "old": "",
        "new": PREFIX,
        "reason": "common style = Lo-fi Remix only (safe-bet prefix)",
        "quote": [Q_PREFIX, Q_SAFE],
    })

    if entry["removed_words"]:
        # 14 기타 / 15 노을: `Korean Indie Alt R&B` -> `Korean Indie R&B`
        assert order in (14, 15), order
        assert original.count("Indie Alt R&B") == 1
        edits.append({
            "id": "E-alt",
            "kind": "remove_genre_word",
            "old": "Indie Alt R&B",
            "new": "Indie R&B",
            "removed_word": "Alt",
            "reason": "alternative / Alt / Modern R&B genre words are dropped; nothing else in the phrase changes",
            "quote": [Q_PREFIX],
        })

    inline = entry["inline_exclude_in_style"]
    if inline:
        line = only_line(original, "Exclude Style:" if order == 11 else "EXCLUDE:")
        assert line == inline["text"], (order, line, inline["text"])
        assert original.endswith("\n\n" + line), order
        edits.append({
            "id": "E-inline-exclude",
            "kind": "move_inline_exclude_line_to_EXCLUDE",
            "old": "\n\n" + line,
            "new": "",
            "removed_line": line,
            "moved_items": list(inline["items"]),
            "reason": "an exclusion line inside STYLE belongs in the EXCLUDE field; the blank separator line before it goes with it",
            "quote": [Q_HYPHEN],
        })
        moved = list(inline["items"])

    if order in (18, 19):
        bridge3 = only_line(original, "Bridge3:")
        last = only_line(original, 'Last "')
        assert last.startswith('Last "괜찮아":'), last
        edits.append({
            "id": "E-bridge3",
            "kind": "remove_lyric_bound_line",
            "old": bridge3 + "\n",
            "new": "",
            "removed_line": bridge3,
            "reason": (
                "the 이름 template lyrics (nine-tracks.json 이름 lyrics_full) have a single [Bridge] tag, so a third bridge does not exist "
                "in the new songs; the whole line is the smallest unit that removes the reference (it only describes that section)"
            ),
            "quote": [Q_JUDGE],
        })
        edits.append({
            "id": "E-last-gwaenchana",
            "kind": "remove_lyric_bound_line",
            "old": last + "\n",
            "new": "",
            "removed_line": last,
            "reason": (
                "the line points at the original lyrics' word 괜찮아 ('longest sustain in entire track ... This single note'); "
                "neither new song's lyrics have that word or such a note, and both clauses of the line depend on it, so the whole line goes. "
                "Narrower alternative considered and rejected: deleting only `Last \"괜찮아\": ` would leave "
                "'longest sustain in entire track, This single note defines the emotional peak' pointing at no note."
            ),
            "quote": [Q_JUDGE],
        })

    return edits, moved, book


def apply_edits(original: str, edits: list[dict]) -> str:
    s = original
    for e in edits:
        if e["kind"] == "prepend_lofi_remix":
            s = e["new"] + s
        else:
            assert s.count(e["old"]) == 1, (e["id"], e["old"])
            s = s.replace(e["old"], e["new"], 1)
    return s


def read_headers(order: int, style: str, entry: dict) -> tuple[str, str, str, dict]:
    bpm_range = STYLE_BPM_RANGE_RE.search(style)
    bpm_nums = [int(m.group(1)) for m in STYLE_BPM_RE.finditer(style)]
    key_match = KEY_MODE_RE.search(style)
    genders = {
        "female" if m.group().lower() in {"female", "여성"} else "male" for m in VOCAL_GENDER_RE.finditer(style)
    }
    assert len(genders) == 1, (order, genders)
    vocal = genders.pop()
    assert vocal == entry["vocal_gender"]["original"], (order, vocal)

    if order == 12:
        # STYLE keeps its own wording (brief: BPM/Key text is not changed)
        assert bpm_range and bpm_range.group().startswith("96–106"), bpm_range
        assert key_match is None and "key color like A♭" in style
        bpm_header = "96–106 (original STYLE wording; release file 90)"
        key_header = 'A♭ (original wording "key color like A♭"; mode not stated)'
        read = {"bpm": "range 96–106 BPM (not a single number)", "key": "not readable (no `X Major|Minor`)", "vocal": vocal}
    else:
        assert not bpm_range and len(bpm_nums) == 1, (order, bpm_nums)
        assert bpm_nums[0] == entry["bpm"]["original"], (order, bpm_nums, entry["bpm"]["original"])
        assert key_match, order
        key_header = f"{key_match.group(1)} {key_match.group(2).capitalize()}"
        assert key_header == entry["key"]["original"], (order, key_header, entry["key"]["original"])
        bpm_header = str(bpm_nums[0])
        read = {"bpm": bpm_nums[0], "key": key_header, "vocal": vocal}
    return bpm_header, key_header, vocal, read


def main() -> int:
    survey = json.loads(SURVEY.read_text(encoding="utf-8"))
    entries_out = []
    for entry in survey["entries"]:
        order = entry["order"]
        src = entry["source"]

        # independent re-read of the original STYLE from the source concept
        original = read_lines(src["path"], src["lines"])
        assert original == entry["original_style"], (order, "original STYLE differs from source lines")
        assert len(original) == entry["measures"]["chars_original_style"], order
        # independent re-read of the separate EXCLUDE block where one exists
        block_empty = False
        if src["exclude_lines"]:
            items_line = read_lines(src["path"], src["exclude_lines"]).strip()
            block_empty = items_line == "(없음)"
            terms = [] if block_empty else [t.strip() for t in items_line.split(",") if t.strip()]
            assert terms == entry["original_exclude"], (order, terms, entry["original_exclude"])
        else:
            assert entry["original_exclude"] == [], order

        edits, moved, _ = build_edits(entry, original)
        final = apply_edits(original, edits)
        assert final == final.strip(), (order, "final STYLE has outer whitespace")
        assert len(re.findall(r"lo-fi remix", final, re.IGNORECASE)) == 1, order
        assert not re.search(r"\balt\b|alternative|modern\s*r&b|얼터너티브|모던", final, re.IGNORECASE), order
        assert not re.search(r"(?im)^\s*(exclude(\s+style)?)\s*:", final), (order, "exclude line left in STYLE")

        exclude = list(entry["original_exclude"])
        dup = [m for m in moved if m in exclude]
        exclude += [m for m in moved if m not in exclude]
        assert len(set(exclude)) == len(exclude), order
        if moved:
            for e in edits:
                if e["id"] == "E-inline-exclude":
                    e["duplicates_dropped"] = dup
                    e["items_added_to_EXCLUDE"] = [m for m in moved if m not in entry["original_exclude"]]

        bpm_header, key_header, vocal_header, read = read_headers(order, final, entry)

        stype = TYPE_NAME.get(entry["type"], entry["type"])
        if entry["type"] in SUNO_RECORDED:
            w, i, where = SUNO_RECORDED[entry["type"]]
            assert entry["suno_params"]["weirdness"] == w and entry["suno_params"]["style_influence"] == i
            suno = {"weirdness": w, "style_influence": i, "source": where}
        else:
            suno = {
                "weirdness": "default",
                "style_influence": "default",
                "source": "원곡에 숫자 기록 없음: " + SUNO_UNRECORDED_NOTE[entry["type"]],
            }

        entries_out.append({
            "order": order,
            "title": entry["title"],
            "type": stype,
            "style": final,
            "style_chars": len(final),
            "style_sha256": sha(final),
            "exclude": exclude,
            "suno_params": suno,
            "bpm_header": bpm_header,
            "key_header": key_header,
            "vocal_header": vocal_header,
            "header_values_read_from_style": read,
            "edits": edits,
            "original_style_chars": len(original),
            "original_style_sha256": sha(original),
            "source": {
                "path": src["path"],
                "heading": src["heading"],
                "style_lines": src["lines"],
                "exclude_lines": src["exclude_lines"],
                "exclude_origin": (
                    "separate Exclude Style block says (없음)" if block_empty
                    else "separate Exclude Style block" if src["exclude_lines"]
                    else ("inline line moved out of STYLE" if moved else "none in the original")
                ),
            },
        })

    out = {
        "schema": "wavvy.final_styles.v1",
        "generated": "2026-11-02",
        "brief": ".ai/plans/2026-11-02-2300-style-apply-a-brief.md",
        "input": ".ai/plans/2026-11-02-2300-original-styles.json",
        "젠_원문": [
            Q_PREFIX, Q_TEMPO, Q_MALE, Q_HYPHEN, Q_JUDGE, Q_SAFE,
        ],
        "rule": (
            "STYLE = `Lo-fi Remix, ` + original STYLE. Edits only: (a) alternative/Alt/Modern R&B genre words, "
            "(b) inline Exclude lines moved to EXCLUDE, (c) lines that only make sense for the original lyrics. "
            "BPM numbers, Key, gender and all other wording stay as in the original. EXCLUDE = original EXCLUDE + moved items "
            "(order kept, duplicates dropped and recorded). Suno params: recorded values, otherwise `default`."
        ),
        "entries": entries_out,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    for e in entries_out:
        print(e["order"], e["title"], e["type"], e["style_chars"], len(e["exclude"]), [x["id"] for x in e["edits"]],
              e["bpm_header"], "|", e["key_header"], "|", e["vocal_header"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
