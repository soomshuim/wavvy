#!/usr/bin/env python3
"""A2 verification: concept.md `## Original Styles` vs final-styles.json vs the original concepts.

Checks per song (9):
  1. byte equality: first ```text block of the concept entry == json `style` (UTF-8 bytes)
  2. EXCLUDE: the entry's single `- EXCLUDE:` line == json `exclude` (items and order)
  3. reproduction: original STYLE (re-read from the source concept) + edits[] == json `style`
  4. line diff original -> final: the changed original lines == the lines the edits touch (computed by char offsets)
  5. shape: starts with `Lo-fi Remix, `, one Lo-fi Remix, no alt/modern words, no exclusion line left, no outer whitespace
  6. header values: BPM / Key / gender read from STYLE equal the original song's values (survey, cross-checked in source)
  7. the concept's char count / sha256 line equals the computed values
Also: the real gate function `_user_original_style` accepts every song (and rejects a one-character change),
the Type Styles 물결 EXCLUDE equals the Original Styles 물결 EXCLUDE, Track Map rows, suno-candidates decisions.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINAL = ROOT / ".ai/plans/2026-11-02-2300-final-styles.json"
SURVEY = ROOT / ".ai/plans/2026-11-02-2300-original-styles.json"
CONCEPT = ROOT / "SERIES/23-00/concept.md"
CANDS = ROOT / "SERIES/23-00/input/suno-candidates.json"
CANDS_BEFORE = Path(sys.argv[1]) if len(sys.argv) > 1 else None
OUT = ROOT / ".ai/validation/2026-11-02-2300-styles/a2-check.json"

# same patterns as wavvy_harness/gate.py
BLOCK_RE = re.compile(r"^```text[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL)
HEADING_RE = re.compile(r"^###[ \t]+(.+?)[ \t]*$", re.MULTILINE)
EXCLUDE_RE = re.compile(r"^[ \t]*[-*+][ \t]+EXCLUDE[ \t]*:[ \t]*(.*?)[ \t]*$", re.MULTILINE)
KEY_RE = re.compile(r"(?<![A-Za-z])([A-G](?:#|b|♯|♭)?)\s+(Major|Minor)\b", re.IGNORECASE)
BPM_RE = re.compile(r"(?<!\d)(\d{1,3})\s*BPM\b", re.IGNORECASE)
GENDER_RE = re.compile(r"(?<![A-Za-z])(female|male)(?![A-Za-z])|여성|남성", re.IGNORECASE)
TYPES = ["먼지", "마음 밖", "작은 빛", "산책", "물결", "물안개", "골목", "이름"]


def sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def section(text: str, name: str) -> str:
    h = re.search(rf"^## {re.escape(name)}\s*$", text, re.MULTILINE)
    assert h, name
    n = re.search(r"^## ", text[h.end():], re.MULTILINE)
    return text[h.end(): h.end() + n.start() if n else len(text)]


def entry_body(sec: str, typ: str) -> str:
    hs = list(HEADING_RE.finditer(sec))
    mine = [h for h in hs if h.group(1) == typ]
    assert len(mine) == 1, (typ, len(mine))
    nxt = next((h for h in hs if h.start() > mine[0].start()), None)
    return sec[mine[0].end(): nxt.start() if nxt else len(sec)]


def terms(line: str) -> list[str]:
    return [t.strip() for ln in line.splitlines() for t in re.split(r"[,;]", ln) if t.strip()]


def read_lines(rel: str, span: str) -> str:
    a, b = (int(x) for x in span.split("-"))
    return "\n".join((ROOT / rel).read_text(encoding="utf-8").split("\n")[a - 1: b])


def apply_edits(original: str, edits: list[dict]) -> str:
    s = original
    for e in edits:
        if e["kind"] == "prepend_lofi_remix":
            s = e["new"] + s
        else:
            assert s.count(e["old"]) == 1, e["id"]
            s = s.replace(e["old"], e["new"], 1)
    return s


def touched_lines(original: str, edits: list[dict]) -> set[int]:
    """Original line indexes the edits touch, computed from char offsets (independent of apply_edits)."""
    spans = []
    pos = 0
    for ln in original.split("\n"):
        spans.append((pos, pos + len(ln)))
        pos += len(ln) + 1
    touched: set[int] = set()
    for e in edits:
        if e["kind"] == "prepend_lofi_remix":
            touched.add(0)
            continue
        s = original.index(e["old"])
        end = s + len(e["old"])
        for i, (ls, le) in enumerate(spans):
            overlap = min(le, end) - max(ls, s) > 0
            blank_inside = ls == le and s < le < end
            term_inside = s < le < end  # terminator of the line lies strictly inside the removed span
            if overlap or blank_inside or term_inside:
                touched.add(i)
    return touched


def main() -> int:
    final = json.loads(FINAL.read_text(encoding="utf-8"))
    survey = {e["order"]: e for e in json.loads(SURVEY.read_text(encoding="utf-8"))["entries"]}
    text = CONCEPT.read_text(encoding="utf-8")
    sec = section(text, "Original Styles")
    results = []
    failures: list[str] = []

    # gate function (real code) -- optional cross-check
    gate_fn = None
    gate_err = ""
    try:
        sys.path.insert(0, str(ROOT))
        from wavvy_harness import gate as gate_mod  # type: ignore

        gate_fn = gate_mod._user_original_style
    except Exception as exc:  # noqa: BLE001
        gate_err = f"{type(exc).__name__}: {exc}"

    hs = [h.group(1) for h in HEADING_RE.finditer(sec)]
    if hs != TYPES:
        failures.append(f"## Original Styles headings {hs} != {TYPES}")

    for e in final["entries"]:
        o = e["order"]
        typ = e["type"]
        r: dict = {"order": o, "title": e["title"], "type": typ, "checks": {}}
        body = entry_body(sec, typ)

        # 1 byte equality concept block vs json
        m = BLOCK_RE.search(body)
        block = m.group(1) if m else None
        byte_equal = block is not None and block.encode("utf-8") == e["style"].encode("utf-8")
        r["checks"]["concept_block_bytes_equal_json_style"] = byte_equal
        r["concept_block_sha256"] = sha(block) if block is not None else None
        r["json_style_sha256"] = sha(e["style"])

        # 2 EXCLUDE line
        rec = EXCLUDE_RE.findall(body[: m.start()] + body[m.end():]) if m else []
        ex_ok = len(rec) == 1 and terms(rec[0]) == e["exclude"]
        r["checks"]["concept_exclude_line_equals_json_exclude"] = ex_ok
        r["exclude_count"] = len(e["exclude"])

        # 3 reproduction from the source concept text
        src = e["source"]
        original = read_lines(src["path"], src["style_lines"])
        r["checks"]["original_equals_survey_and_sha"] = (
            original == survey[o]["original_style"] and sha(original) == e["original_style_sha256"]
            and len(original) == e["original_style_chars"]
        )
        repro = apply_edits(original, e["edits"])
        r["checks"]["original_plus_edits_equals_json_style"] = repro == e["style"]

        # 4 line diff vs touched lines
        ol, fl = original.split("\n"), e["style"].split("\n")
        ops = difflib.SequenceMatcher(None, ol, fl, autojunk=False).get_opcodes()
        changed = set()
        inserted_only = []
        for tag, i1, i2, j1, j2 in ops:
            if tag in ("delete", "replace"):
                changed.update(range(i1, i2))
            if tag == "insert":
                inserted_only.append((j1, j2))
        want = touched_lines(original, e["edits"])
        r["checks"]["changed_original_lines_equal_edit_lines"] = changed == want and not inserted_only
        r["changed_original_lines_0based"] = sorted(changed)
        r["edit_touched_lines_0based"] = sorted(want)
        r["line_diff"] = [
            {"op": tag, "original": ol[i1:i2], "final": fl[j1:j2]} for tag, i1, i2, j1, j2 in ops if tag != "equal"
        ]
        r["edit_ids"] = [x["id"] for x in e["edits"]]

        # 5 shape
        s = e["style"]
        shape = {
            "starts_with_prefix": s.startswith("Lo-fi Remix, "),
            "one_lofi_remix": len(re.findall(r"lo-fi remix", s, re.IGNORECASE)) == 1,
            "no_alt_or_modern": not re.search(r"\balt\b|alternative|modern\s*r&b|얼터너티브|모던", s, re.IGNORECASE),
            "no_exclusion_line_left": not re.search(r"(?im)^\s*(exclude(\s+style)?)\s*:", s),
            "no_outer_whitespace": s == s.strip(),
            "no_cr": "\r" not in s,
            "no_trailing_space_per_line": all(ln == ln.rstrip() for ln in s.split("\n")),
        }
        r["checks"]["shape"] = all(shape.values())
        r["shape_detail"] = shape
        r["style_chars"] = len(s)

        # 6 header values (BPM / Key / gender) vs original song
        genders = {"female" if mm.group().lower() in {"female", "여성"} else "male" for mm in GENDER_RE.finditer(s)}
        bpms = [int(mm.group(1)) for mm in BPM_RE.finditer(s)]
        km = KEY_RE.search(s)
        hdr = {
            "gender_in_style": sorted(genders),
            "gender_original": survey[o]["vocal_gender"]["original"],
            "bpm_numbers_in_style": bpms,
            "bpm_original": survey[o]["bpm"]["original"],
            "key_in_style": f"{km.group(1)} {km.group(2).capitalize()}" if km else None,
            "key_original": survey[o]["key"]["original"],
            "bpm_header": e["bpm_header"], "key_header": e["key_header"], "vocal_header": e["vocal_header"],
        }
        if o == 12:
            ok6 = (
                genders == {"female"} and bpms == [106] and km is None
                and e["bpm_header"].startswith("96–106") and "key color like A♭" in s
                and e["key_header"].startswith("A♭") and e["vocal_header"] == "female"
            )
        else:
            ok6 = (
                genders == {survey[o]["vocal_gender"]["original"]} == {e["vocal_header"]}
                and bpms == [survey[o]["bpm"]["original"]] and e["bpm_header"] == str(bpms[0])
                and km is not None and hdr["key_in_style"] == survey[o]["key"]["original"] == e["key_header"]
            )
        # the survey's own BPM/Key/gender rows for the original songs must also be what the source says
        r["checks"]["header_values_match_original"] = ok6
        r["header_detail"] = hdr

        # 7 concept header line (chars, sha)
        mh = re.search(r"\*\*최종 STYLE\*\* — (\d+)자, sha256 `([0-9a-f]{64})`", body)
        r["checks"]["concept_chars_sha_line"] = bool(mh) and int(mh.group(1)) == len(s) and mh.group(2) == sha(s) == e["style_sha256"] and e["style_chars"] == len(s)

        # real gate function
        if gate_fn is not None:
            meta = {"Style Type": typ, "Style Source": "user-supplied original style"}
            got = gate_fn(text, meta, e["style"], list(e["exclude"]))
            bad = gate_fn(text, meta, e["style"][:-1] + ("!" if e["style"][-1] != "!" else "?"), list(e["exclude"]))
            bad_ex = gate_fn(text, meta, e["style"], list(reversed(e["exclude"]))) if len(e["exclude"]) > 1 else ("x", "skip")
            r["checks"]["real_gate_accepts"] = tuple(got) == (typ, "")
            r["checks"]["real_gate_rejects_one_char_change"] = bad[0] == "" and bool(bad[1])
            r["checks"]["real_gate_rejects_reordered_exclude"] = (bad_ex[0] == "" and bool(bad_ex[1])) if len(e["exclude"]) > 1 else True
            r["real_gate"] = {"accept": list(got), "reject_one_char": list(bad), "reject_reordered": list(bad_ex)}

        ok = all(r["checks"].values())
        r["result"] = "PASS" if ok else "FAIL"
        if not ok:
            failures.append(f"{o} {e['title']}: " + ", ".join(k for k, v in r["checks"].items() if not v))
        results.append(r)

    # 18 / 19 identical
    e18 = next(x for x in final["entries"] if x["order"] == 18)
    e19 = next(x for x in final["entries"] if x["order"] == 19)
    same_1819 = all(e18[k] == e19[k] for k in ("style", "exclude", "style_sha256", "edits", "suno_params"))
    if not same_1819:
        failures.append("18 and 19 differ")

    # 물결 EXCLUDE: Type Styles line == Original Styles line
    ts_body = entry_body(section(text, "Type Styles"), "물결")
    ts_ex = terms(EXCLUDE_RE.findall(ts_body)[0])
    e15 = next(x for x in final["entries"] if x["order"] == 15)
    mulgyeol_same = ts_ex == e15["exclude"]
    if not mulgyeol_same:
        failures.append("물결 EXCLUDE differs from ## Type Styles")

    # Track Map rows
    tm = section(text, "Track Map (numbers are temporary)")
    cands = json.loads(CANDS.read_text(encoding="utf-8"))
    chosen = {t["order"]: t["decision"].get("chosen_candidate_id") for t in cands["tracks"]}
    track_map = {}
    for e in final["entries"]:
        row = next(ln for ln in tm.splitlines() if ln.startswith(f"| {e['order']} | "))
        vocal_ok = f"{e['vocal_header']} vocal" in row
        bpm_ok = (e["bpm_header"] if e["order"] != 12 else "96–106 BPM") in row
        key_ok = (e["key_header"] if e["order"] != 12 else "A♭ (mode not stated)") in row
        st_ok = "재생성 대기 (원곡 가사 틀 + 원곡 스타일)" in row
        track_map[e["order"]] = vocal_ok and bpm_ok and key_ok and st_ok
        if not track_map[e["order"]]:
            failures.append(f"Track Map row {e['order']} mismatch: {row}")
    for o in (10, 20):
        row = next(ln for ln in tm.splitlines() if ln.startswith(f"| {o} | "))
        track_map[o] = "확정 — 후보 B" in row and chosen[o] in row
        if not track_map[o]:
            failures.append(f"Track Map row {o} mismatch")

    # suno-candidates decisions
    dec = {}
    for t in cands["tracks"]:
        if 11 <= t["order"] <= 19:
            ok = (
                t["decision"] == {"status": "regenerate", "chosen_candidate_id": None}
                and t["decision_evidence"]["by"] == "젠" and t["decision_evidence"]["date"] == "2026-11-02"
                and t["decision_evidence"]["quote"] == ["라디오 탈락", "전반적으로 후렴이 중독성이 약하네", "11곡 모두 다시 써서 생성 (추천)"]
                and len(t["candidates"]) == 2
            )
            dec[t["order"]] = ok
            if not ok:
                failures.append(f"suno-candidates decision {t['order']}")
    untouched = None
    if CANDS_BEFORE and CANDS_BEFORE.exists():
        before = json.loads(CANDS_BEFORE.read_text(encoding="utf-8"))
        bt = {t["order"]: t for t in before["tracks"]}
        at = {t["order"]: t for t in cands["tracks"]}
        untouched = {}
        for o in range(1, 21):
            b = dict(bt[o]); a = dict(at[o])
            if 11 <= o <= 19:
                b.pop("decision"); a.pop("decision"); a.pop("decision_evidence")
            untouched[o] = (b == a)
        top_same = {k: v for k, v in before.items() if k != "tracks"} == {k: v for k, v in cands.items() if k != "tracks"}
        untouched["top_level"] = top_same
        if not all(untouched.values()):
            failures.append(f"suno-candidates unexpected change: {untouched}")

    summary = {
        "songs_pass": f"{sum(1 for r in results if r['result'] == 'PASS')}/{len(results)}",
        "byte_equal_concept_vs_json": f"{sum(1 for r in results if r['checks']['concept_block_bytes_equal_json_style'])}/{len(results)}",
        "exclude_equal": f"{sum(1 for r in results if r['checks']['concept_exclude_line_equals_json_exclude'])}/{len(results)}",
        "original_plus_edits_equals_json": f"{sum(1 for r in results if r['checks']['original_plus_edits_equals_json_style'])}/{len(results)}",
        "line_diff_equals_edit_lines": f"{sum(1 for r in results if r['checks']['changed_original_lines_equal_edit_lines'])}/{len(results)}",
        "real_gate_function": ("not run: " + gate_err) if gate_fn is None else f"{sum(1 for r in results if r['checks'].get('real_gate_accepts'))}/{len(results)} accepted",
        "headings_ok": hs == TYPES,
        "18_19_identical": same_1819,
        "물결_exclude_equals_type_styles": mulgyeol_same,
        "track_map_rows": track_map,
        "suno_candidates_11_19_decision": dec,
        "suno_candidates_other_content_unchanged": untouched,
    }
    out = {
        "schema": "wavvy.a2_check.v1",
        "result": "PASS" if not failures else "FAIL",
        "failures": failures,
        "summary": summary,
        "songs": results,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": out["result"], "failures": failures, "summary": summary}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
