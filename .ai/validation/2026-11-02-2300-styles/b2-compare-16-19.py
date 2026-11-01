#!/usr/bin/env python3
"""B2 compare for tracks 16-19: writes .ai/validation/2026-11-02-2300-styles/NN-apply-compare.json (raw, one per track).

Independent of the harness gates: re-reads the txt, the record, the final-styles json, the concept.md `## Original Styles`
entry and the preserved pre-change copies, and checks the brief's compare items (txt STYLE sha256 == json style_sha256,
txt EXCLUDE items == json, txt LYRICS == record Draft) plus the lyric-correction counts, header/record agreement and
leftover female/woman wording.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from wavvy_harness import gate  # noqa: E402
from wavvy_harness.source import parse_track_source_fields  # noqa: E402

V = ROOT / ".ai/validation/2026-11-02-2300-styles"
HIST = ROOT / "SERIES/23-00/input/source-history/2026-11-02-before-original-style"
FINAL = {e["order"]: e for e in json.loads((ROOT / ".ai/plans/2026-11-02-2300-final-styles.json").read_text(encoding="utf-8"))["entries"]}
NAMES = {16: "16_여름밤", 17: "17_막차", 18: "18_벚꽃", 19: "19_그네"}
FIXES = {
    16: [],
    17: [("머리에서 나던 샴푸 냄새가 아직 나요", "그 샴푸 향기가 아직 코끝에 남았어요"), ("왠지 네가 앉아 있는 듯이 아늑해요", "네가 앉았던 것처럼 괜히 따뜻해요")],
    18: [("꽃잎들이 살짝 모여 쉬었네", "꽃잎 한 장이 사뿐히 앉았네"), ("봄 하나 얹고", "머리에 한 장")],
    19: [("내 몸이 먼저 기억을 하네", "두 다리가 먼저 흔들려 와")],
}
TARGET = {16: 138, 17: 207, 18: 214, 19: 214}
CONCEPT = (ROOT / "SERIES/23-00/concept.md").read_text(encoding="utf-8")


def sha(s):
    return hashlib.sha256(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def hangul(s):
    return len(re.findall(r"[가-힣]", s))


def concept_entry(style_type):
    sec = CONCEPT.split("\n## Original Styles\n", 1)[1]
    sec = re.split(r"\n## ", sec, maxsplit=1)[0]
    parts = re.split(r"(?m)^### ", sec)
    hit = [p for p in parts[1:] if p.split("\n", 1)[0].strip() == style_type]
    assert len(hit) == 1, (style_type, len(hit))
    body = hit[0]
    block = re.search(r"```text\n(.*?)\n```", body, re.S).group(1)
    ex = re.findall(r"(?m)^- EXCLUDE:\s*(.*)$", body)
    assert len(ex) == 1
    return block.strip(), [x.strip() for x in ex[0].split(",") if x.strip()]


def main():
    overall = []
    for order, name in NAMES.items():
        e = FINAL[order]
        checks = []

        def chk(label, ok, detail=""):
            checks.append({"check": label, "result": "PASS" if ok else "FAIL", "detail": detail})

        txt_path = ROOT / f"SERIES/23-00/input/tracks/{name}.txt"
        rec_path = ROOT / f".ai/lyrics/2026-11-01_23-00_{name}-full-draft.md"
        old_txt_path = HIST / f"{name}.txt"
        old_rec_path = HIST / "lyrics-records" / rec_path.name
        raw = txt_path.read_text(encoding="utf-8")
        meta, sec = parse_track_source_fields(raw)
        rec = rec_path.read_text(encoding="utf-8")
        draft = gate._extract_section(rec, "Draft")
        old_raw = old_txt_path.read_text(encoding="utf-8")
        _, old_sec = parse_track_source_fields(old_raw)

        # 1. STYLE
        chk("txt STYLE == json style (exact)", sec["STYLE"] == e["style"], f"chars={len(sec['STYLE'])}")
        chk("txt STYLE sha256 == json style_sha256", sha(sec["STYLE"]) == e["style_sha256"], f"{sha(sec['STYLE'])} vs {e['style_sha256']}")
        chk("txt STYLE chars == json style_chars", len(sec["STYLE"]) == e["style_chars"], f"{len(sec['STYLE'])} vs {e['style_chars']}")
        # 2. EXCLUDE
        terms = [t.strip() for t in sec["EXCLUDE"].split(",") if t.strip()]
        chk("txt EXCLUDE items == json exclude (order kept)", terms == e["exclude"], f"{len(terms)} items")
        chk("txt EXCLUDE is one line joined by ', '", sec["EXCLUDE"] == ", ".join(e["exclude"]) and "\n" not in sec["EXCLUDE"])
        # 3. concept.md Original Styles (independent parse)
        block, c_ex = concept_entry(e["type"])
        chk("txt STYLE == concept.md ## Original Styles text block", sec["STYLE"] == block, e["type"])
        chk("txt EXCLUDE items == concept.md '- EXCLUDE:' items", terms == c_ex, f"{len(c_ex)} items")
        # 4. LYRICS vs record Draft
        chk("txt LYRICS == record Draft (stripped)", sec["LYRICS"] == draft.strip(), f"sha256={sha(sec['LYRICS'])}")
        claimed = re.search(r"(?m)^- Source SHA256: (\w+)$", rec).group(1)
        chk("record Source SHA256 == sha256(Draft)", claimed == sha(draft), claimed)
        # 5. header
        chk("header BPM == json bpm_header", meta["BPM"] == e["bpm_header"], meta["BPM"])
        chk("header Key == json key_header", meta["Key"] == e["key_header"], meta["Key"])
        chk("header Vocal == json vocal_header", meta["Vocal"] == e["vocal_header"], meta["Vocal"])
        chk("header Style Type == json type", meta.get("Style Type") == e["type"], meta.get("Style Type", ""))
        chk("header Style Source == user-supplied original style", meta.get("Style Source") == "user-supplied original style")
        chk("header Suno Params JSON == json suno_params", json.loads(meta["Suno Params"]) == e["suno_params"])
        chk("header Status", meta["Status"] == "full-lyric-draft (template lyrics + original style — 젠 2026-11-02); regeneration pending")
        chk("header has no Exclude Source line", "Exclude Source" not in meta)
        # 6. lyric corrections
        old_lines = old_sec["LYRICS"].split("\n")
        new_lines = sec["LYRICS"].split("\n")
        draft_lines = draft.strip().split("\n")
        expect_changed = {}
        for o, n in FIXES[order]:
            cnt_old = old_lines.count(o)
            chk(f"preserved txt has old row once: {o}", cnt_old == 1, f"{cnt_old}")
            chk(f"new txt: old row gone / new row once: {n}", new_lines.count(o) == 0 and new_lines.count(n) == 1)
            chk(f"record Draft: old row gone / new row once: {n}", draft_lines.count(o) == 0 and draft_lines.count(n) == 1)
            chk(f"same Hangul syllables: {o} -> {n}", hangul(o) == hangul(n), f"{hangul(o)} vs {hangul(n)}")
            expect_changed[o] = n
        diff_idx = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
        chk("txt LYRICS differs from preserved only at corrected rows",
            len(old_lines) == len(new_lines) and sorted(old_lines[i] for i in diff_idx) == sorted(expect_changed) and all(new_lines[i] == expect_changed[old_lines[i]] for i in diff_idx),
            f"{len(diff_idx)} changed rows (expected {len(expect_changed)})")
        # 7. record vs txt
        cf = {k: v for k, v in re.findall(r"(?m)^- ([a-z_]+): (.*)$", rec.split("## Constraint Freeze", 1)[1].split("## Lyric Strategy", 1)[0])}
        bpm = int(e["bpm_header"])
        chk("record bpm == txt BPM", re.match(r"(\d+)", cf["bpm"]).group(1) == str(bpm), cf["bpm"][:60])
        chk("record key == json key_header", cf["key"].startswith(e["key_header"]), cf["key"][:60])
        chk("record target_duration_seconds", cf["target_duration_seconds"] == str(TARGET[order]), cf["target_duration_seconds"])
        bars = [p.strip() for p in cf["section_bars"].split(";")]
        total = sum(int(p.rsplit("=", 1)[1]) for p in bars)
        est = total * 4 * 60 / bpm
        chk("record section_bars total/4-4 estimate >= target", est >= TARGET[order], f"{total} bars, {est:.2f}s vs {TARGET[order]}s")
        txt_bars = meta["Section Bars"].split(" (")[0]
        chk("txt Section Bars list == record section_bars", txt_bars == cf["section_bars"])
        chk("record duration_plan states the same bars/BPM/estimate", f"{total} bars in 4/4 at {bpm} BPM estimate {est:.1f} seconds" in rec, f"{total}/{bpm}/{est:.1f}")
        chk("record vocal_identity says male", "one male lead" in cf["vocal_identity"], cf["vocal_identity"][:50])
        # 8. preserved copies & recorded shas
        chk("preserved txt sha256 recorded in record Source Map", sha(old_txt_path.read_bytes()) in rec, sha(old_txt_path.read_bytes()))
        chk("preserved record sha256 recorded in record Source Map", sha(old_rec_path.read_bytes()) in rec, sha(old_rec_path.read_bytes()))
        # 9. leftover female/woman wording outside historical lines
        hist_markers = ("Previous version", "Orchestrator design", "Previous versions", "Superseded STYLE")
        leftovers = []
        for i, line in enumerate(rec.split("\n"), 1):
            if re.search(r"(?i)\b(female|woman|women|herself)\b|\b(she|her|hers)\b", line) and not any(m in line for m in hist_markers):
                leftovers.append({"line": i, "text": line[:160]})
        # 17 legitimately speaks of the other person (`너`) as she/her
        chk("no leftover female/woman/she/her wording about the narrator (review hits)", order == 17 or not leftovers, f"{len(leftovers)} hit(s)")
        overall.append((order, all(c["result"] == "PASS" for c in checks)))
        out = {"track": order, "title": e["title"], "type": e["type"],
               "result": "PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL",
               "counts": {"PASS": sum(c["result"] == "PASS" for c in checks), "FAIL": sum(c["result"] == "FAIL" for c in checks)},
               "leftover_pronoun_hits": leftovers, "checks": checks}
        (V / f"{order}-apply-compare.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(order, out["result"], out["counts"], "leftover_pronoun_hits:", len(leftovers))
    sys.exit(0 if all(ok for _, ok in overall) else 1)


if __name__ == "__main__":
    main()
