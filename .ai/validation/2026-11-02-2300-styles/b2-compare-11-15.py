#!/usr/bin/env python3
"""B2 step 6: compare the applied txt/record of tracks 11-15 with the final-styles json and the preserved previous versions.

Writes NN-apply-compare.json per track and prints a one-line verdict per track. Read-only on the repo.
Checks per track:
  C1 txt STYLE sha256 == json style_sha256 (and the text is equal to json style and to the concept.md ## Original Styles text block)
  C2 txt EXCLUDE items == json exclude (same order)
  C3 txt LYRICS == record Draft
  C4 txt headers: BPM/Key/Vocal == json *_header, Style Type, Style Source, Suno Params == json suno_params, Status, no Exclude Source
  C5 txt Target Duration/Section Bars header == record target_duration_seconds/section_bars (+ bar sum and estimate)
  C6 record Draft differs from the preserved previous Draft only by the expected line replacements
  C7 preserved copies exist and their sha256 equal the b2-preserve json
  C8 record Source SHA256 == sha256 of the current Draft
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path.home() / "Project/wavvy"
sys.path.insert(0, str(ROOT))
from wavvy_harness.gate import _extract_section, _field_lines  # read-only helpers used by the gates
from wavvy_harness.source import parse_track_source_fields

V = ROOT / ".ai/validation/2026-11-02-2300-styles"
HIST = ROOT / "SERIES/23-00/input/source-history/2026-11-02-before-original-style"
FINAL = {e["order"]: e for e in json.loads((ROOT / ".ai/plans/2026-11-02-2300-final-styles.json").read_text(encoding="utf-8"))["entries"]}
PRES = json.loads((V / "b2-preserve-11-15.json").read_text(encoding="utf-8"))
CONCEPT = (ROOT / "SERIES/23-00/concept.md").read_text(encoding="utf-8")
SONGS = {11: "라디오", 12: "스웨터", 13: "편지", 14: "기타", 15: "노을"}
STATUS = "full-lyric-draft (template lyrics + original style — 젠 2026-11-02); regeneration pending"
EXPECTED_FIXES = {
    11: {"낮은 목소리가 사연을": "낮은 목소리 사연 하나", "읽고 나면 잡음 속에서": "끝나고 나면 잡음 속에", "틀린 가사 신나게 부르던": "틀린 가사 신나게 부른 너"},
    12: {},
    13: {"“잘 있어": "“따뜻해", "잘 있어”": "따뜻해”", "또 올게": "또 볼게"},
    14: {},
    15: {"해 지는 쪽부터 주황빛": "서쪽 하늘이 물들어 가"},
}


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def nonempty(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def concept_block(style_type):
    m = re.search(r"^## Original Styles\s*$(.*?)(?=^## )", CONCEPT, re.MULTILINE | re.DOTALL)
    section = m.group(1)
    heads = list(re.finditer(r"^###[ \t]+(.+?)[ \t]*$", section, re.MULTILINE))
    entry = [h for h in heads if h.group(1) == style_type]
    assert len(entry) == 1
    nxt = next((h for h in heads if h.start() > entry[0].start()), None)
    body = section[entry[0].end(): nxt.start() if nxt else len(section)]
    block = re.search(r"^```text[ \t]*\n(.*?)\n```[ \t]*$", body, re.MULTILINE | re.DOTALL)
    excl = re.findall(r"^[ \t]*[-*+][ \t]+EXCLUDE[ \t]*:[ \t]*(.*?)[ \t]*$", body, re.MULTILINE)
    return block.group(1).strip(), excl


def main():
    pres = {(r["track"], r["kind"]): r for r in PRES["rows"]}
    all_ok = True
    for n, title in SONGS.items():
        e = FINAL[n]
        txt_path = ROOT / f"SERIES/23-00/input/tracks/{n:02d}_{title}.txt"
        rec_path = ROOT / f".ai/lyrics/2026-11-01_23-00_{n}_{title}-full-draft.md"
        old_rec_path = ROOT / pres[(n, "record")]["dst"]
        old_txt_path = ROOT / pres[(n, "txt")]["dst"]
        meta, sec = parse_track_source_fields(txt_path.read_text(encoding="utf-8"))
        rec = rec_path.read_text(encoding="utf-8")
        draft = _extract_section(rec, "Draft")
        cf = _extract_section(rec, "Constraint Freeze")
        old_draft = _extract_section(old_rec_path.read_text(encoding="utf-8"), "Draft")
        c_style, c_excl = concept_block(e["type"])
        checks = []

        def chk(name, ok, detail):
            checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

        style = sec["STYLE"]
        chk("C1_txt_style_sha256_equals_json", sha_text(style) == e["style_sha256"] and style == e["style"],
            f"txt={sha_text(style)} json={e['style_sha256']} chars={len(style)}")
        chk("C1b_txt_style_equals_concept_original_styles_block", style == c_style, f"concept block sha256={sha_text(c_style)}")
        txt_excl = [t.strip() for t in sec["EXCLUDE"].split(",") if t.strip()]
        chk("C2_txt_exclude_items_equal_json", txt_excl == e["exclude"] and sec["EXCLUDE"] == ", ".join(e["exclude"]),
            f"txt={txt_excl} json={e['exclude']}")
        chk("C2b_txt_exclude_equals_concept_exclude_line", txt_excl == ([t.strip() for t in c_excl[0].split(",") if t.strip()] if c_excl else []),
            f"concept={c_excl}")
        chk("C3_txt_lyrics_equal_record_draft", sec["LYRICS"].strip() == draft.strip(), f"draft_sha256={sha_text(draft)}")
        want_header = {"BPM": e["bpm_header"], "Key": e["key_header"], "Vocal": e["vocal_header"], "Style Type": e["type"],
                       "Style Source": "user-supplied original style", "Status": STATUS, "Order": str(n), "Track": title}
        bad = {k: (meta.get(k), v) for k, v in want_header.items() if meta.get(k) != v}
        chk("C4_txt_headers", not bad and "Exclude Source" not in meta and json.loads(meta["Suno Params"]) == e["suno_params"],
            f"mismatch={bad}; Exclude Source present={'Exclude Source' in meta}; Suno Params={meta.get('Suno Params')}")
        bars_text = _field_lines(cf, "section_bars")[0]
        parts = [p.strip() for p in bars_text.split(";")]
        total_bars = sum(int(p.rsplit("=", 1)[1]) for p in parts)
        target = int(_field_lines(cf, "target_duration_seconds")[0])
        rec_bpm = int(re.match(r"^(\d+)", _field_lines(cf, "bpm")[0]).group(1))
        txt_bpm = int(re.match(r"^(\d+)", meta["BPM"]).group(1))
        estimate = round(total_bars * 4 * 60 / rec_bpm, 1)
        chk("C5_header_bars_and_target_match_record", meta["Section Bars"].startswith(bars_text) and rec_bpm == txt_bpm and estimate >= target
            and f"{total_bars} bars" in meta["Section Bars"] and f"about {estimate} seconds at {rec_bpm} BPM" in meta["Section Bars"],
            f"bars={total_bars}; record_bpm={rec_bpm}; txt_bpm={txt_bpm}; estimate={estimate}; target={target}; header_target='{meta['Target Duration']}'")
        old_lines, new_lines = nonempty(old_draft), nonempty(draft)
        expected = [EXPECTED_FIXES[n].get(line, line) for line in old_lines]
        changed = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
        chk("C6_draft_differs_from_previous_only_by_expected_fixes", new_lines == expected and len(old_lines) == len(new_lines),
            f"changed_rows={len(changed)}; rows={changed}")
        old_txt_lines = nonempty(parse_track_source_fields(old_txt_path.read_text(encoding='utf-8'))[1]["LYRICS"])
        chk("C6b_txt_lyrics_differ_from_previous_txt_only_by_expected_fixes", nonempty(sec["LYRICS"]) == [EXPECTED_FIXES[n].get(l, l) for l in old_txt_lines],
            f"previous txt rows={len(old_txt_lines)}")
        pres_ok = all(
            (ROOT / pres[(n, k)]["dst"]).is_file() and hashlib.sha256((ROOT / pres[(n, k)]["dst"]).read_bytes()).hexdigest() == pres[(n, k)]["src_sha256"]
            for k in ("txt", "record"))
        chk("C7_preserved_copies_intact", pres_ok, f"{pres[(n, 'txt')]['dst']}; {pres[(n, 'record')]['dst']}")
        claimed = _field_lines(_extract_section(rec, "Self-Gate"), "Source SHA256")
        chk("C8_record_source_sha256_equals_current_draft", claimed == [sha_text(draft)], f"claimed={claimed} actual={sha_text(draft)}")
        ok = all(c["status"] == "PASS" for c in checks)
        all_ok &= ok
        (V / f"{n}-apply-compare.json").write_text(json.dumps({"track": n, "title": title, "type": e["type"], "result": "PASS" if ok else "FAIL",
                                                              "checks": checks}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(n, title, "PASS" if ok else "FAIL", [c["name"] for c in checks if c["status"] != "PASS"])
    sys.exit(0 if all_ok else 1)


main()
