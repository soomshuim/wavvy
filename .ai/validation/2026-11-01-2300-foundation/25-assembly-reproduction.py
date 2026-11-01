#!/usr/bin/env python3
"""Re-assemble the 11 new-song STYLEs from SERIES/23-00/concept.md and compare with the plan json.

Run from the repo root:  python3 -I .ai/validation/2026-11-01-2300-foundation/25-assembly-reproduction.py

Inputs (read-only):
  SERIES/23-00/concept.md                                   -> `### <type>` (b) blocks, assembly table, Track Map rows 10-20
  .ai/plans/2026-11-01-2300-new-song-styles.json            -> expected style / chars / sha256 / appended / prefix flag

Rules re-implemented here (concept.md `## New Song Style Assembly`):
  1. start from the type's (b) STYLE
  2. if `lo-fi remix` (case-insensitive) is absent, prepend `Lo-fi Remix, `
  3. append only the missing items, in order: `, NN BPM`, `, X Major|Minor`, `, male|female vocal`
Exit code 0 only if all 11 songs match on every check.
"""
import hashlib
import json
import re
import sys

CONCEPT = "SERIES/23-00/concept.md"
PLAN = ".ai/plans/2026-11-01-2300-new-song-styles.json"

BPM_RE = re.compile(r"\b(\d{2,3})\s*BPM\b", re.I)
KEY_RE = re.compile(r"\b([A-G][b#]?\s+(?:Major|Minor))\b")
GENDER_RE = re.compile(r"\b((?:fe)?male)\b", re.I)

fails = []


def check(ok, label):
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        fails.append(label)
    return ok


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def section(text, name):
    m = re.search(rf"^## {re.escape(name)}.*$", text, flags=re.M)
    nxt = re.search(r"^## ", text[m.end():], flags=re.M)
    return text[m.end(): m.end() + nxt.start() if nxt else len(text)]


concept = open(CONCEPT, encoding="utf-8").read()
plan = json.load(open(PLAN, encoding="utf-8"))

# ---- Type Styles: parse (a)/(b) per type ----
ts = section(concept, "Type Styles")
heads = list(re.finditer(r"^### (.+?)\s*$", ts, flags=re.M))
types = {}
for i, h in enumerate(heads):
    body = ts[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(ts)]
    entry = {"append_line": re.search(r"^- 새 곡 STYLE 끝에 덧붙일 항목.*?: (.*)$", body, flags=re.M).group(1)}
    for tag in ("a", "b"):
        m = re.search(rf"\*\*\({tag}\) [^\n]*?\*\* — (\d+)자, sha256 `([0-9a-f]{{64}})`", body)
        j = body.index("```text", m.end())
        k = body.index("```", j + 7)
        txt = body[j + 8: k].rstrip("\n")
        entry[tag] = {"claimed_chars": int(m.group(1)), "claimed_sha": m.group(2), "text": txt}
    types[h.group(1)] = entry

print("== A. concept (a)/(b) blocks: claimed chars/sha256 == measured ==")
for name, e in types.items():
    for tag in ("a", "b"):
        x = e[tag]
        check(len(x["text"]) == x["claimed_chars"] and sha(x["text"]) == x["claimed_sha"],
              f"{name} ({tag}) claimed {x['claimed_chars']}자 {x['claimed_sha'][:12]} == measured {len(x['text'])}자 {sha(x['text'])[:12]}")
print()
print("== B. which types still have an edit (b) != (a) ==")
for name, e in types.items():
    print(f"INFO {name}: (b) {'== (a)' if e['b']['text'] == e['a']['text'] else '!= (a) (edit recorded)'}")
for name in ("산책", "마음 밖"):
    check(types[name]["b"]["text"] == types[name]["a"]["text"], f"{name} (b) == (a) (earlier removal cancelled)")
check(types["산책"]["b"]["text"].startswith("Lo-Fi Remix, "), "산책 (b) keeps leading `Lo-Fi Remix, `")
check("lo-fi remix," in types["마음 밖"]["b"]["text"], "마음 밖 (b) keeps `lo-fi remix,`")

print()
print("== C. re-assemble 11 songs from the (b) blocks and compare with the plan json ==")
asm_rows = {}
for r in plan:
    n, typ = r["order"], r["type"]
    b = types[typ]["b"]["text"]
    s = b
    has_prefix = re.search(r"lo-fi remix", b, flags=re.I) is not None
    if not has_prefix:
        s = "Lo-fi Remix, " + s
    bm, km, gm = BPM_RE.search(b), KEY_RE.search(b), GENDER_RE.search(b)
    derived = []
    kinds = []
    if not bm:
        derived.append(f"{r['bpm']} BPM"); kinds.append("bpm")
    if not km:
        derived.append(r["key"]); kinds.append("key")
    if not gm:
        derived.append(f"{r['gender']} vocal"); kinds.append("gender")
    for item in derived:
        s += ", " + item
    asm_rows[n] = (s, derived)
    check(s == r["style"], f"[{n} {r['title']} / {typ}] assembled STYLE == json style")
    check(len(s) == r["chars"], f"[{n}] chars assembled {len(s)} == json {r['chars']}")
    check(sha(s) == r["sha256"], f"[{n}] sha256 assembled {sha(s)[:16]} == json {r['sha256'][:16]}")
    check(r["lofi_remix_prefixed"] == (not has_prefix), f"[{n}] prefix flag json={r['lofi_remix_prefixed']} derived={not has_prefix}")
    check(derived == r["appended"], f"[{n}] appended items json={r['appended']} derived={derived}")
    # values already inside the type text must agree with the song's declared values
    check((not bm) or int(bm.group(1)) == r["bpm"], f"[{n}] BPM inside (b) agrees with json bpm {r['bpm']}")
    check((not km) or km.group(1) == r["key"], f"[{n}] key inside (b) agrees with json key {r['key']}")
    check((not gm) or gm.group(1).lower() == r["gender"], f"[{n}] gender word inside (b) agrees with json gender {r['gender']}")
    # concept per-type "덧붙일 항목" line (written before this assembly) must name the same kinds
    line = types[typ]["append_line"]
    want = []
    if "NN BPM" in line: want.append("bpm")
    if "X Major|Minor" in line: want.append("key")
    if "male|female vocal" in line: want.append("gender")
    check(want == kinds, f"[{n}] concept `### {typ}` 덧붙일 항목 kinds {want} == derived {kinds}")
print()
ok_rows = sum(1 for r in plan if asm_rows[r["order"]][0] == r["style"] and sha(asm_rows[r["order"]][0]) == r["sha256"])
print(f"RESULT assembled==json (style and sha256): {ok_rows}/{len(plan)}")
check(ok_rows == len(plan) == 11, "11/11 songs reproduce json style + sha256")

print()
print("== D. concept `## New Song Style Assembly` table == json ==")
sec = section(concept, "New Song Style Assembly")
trows = {}
for line in sec.splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if line.startswith("|") and c[0].isdigit():
        trows[int(c[0])] = c
check(sorted(trows) == list(range(10, 21)), f"table has rows 10..20 (found {sorted(trows)})")
for r in plan:
    c = trows.get(r["order"])
    if not c:
        continue
    app = [a.strip("` ") for a in c[7].split(",")] if c[7] != "없음" else []
    exp = (r["title"], r["type"], r["gender"], str(r["bpm"]), r["key"],
           "예" if r["lofi_remix_prefixed"] else "아니오", r["appended"], str(r["chars"]), r["sha256"])
    got = (c[1], c[2], c[3], c[4], c[5], c[6].split(" ")[0], app, c[8], c[9].strip("`"))
    check(exp == got, f"[{r['order']}] table row == json (title,type,vocal,bpm,key,prefix,appended,chars,sha256)")

print()
print("== E. concept Track Map rows 10-20 == json ==")
tm = section(concept, "Track Map")
mrows = {}
for line in tm.splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if line.startswith("|") and c[0].isdigit():
        mrows[int(c[0])] = c
for r in plan:
    c = mrows.get(r["order"])
    check(c is not None, f"[{r['order']}] Track Map row present")
    if not c:
        continue
    role = f"새 곡 · {r['gender']} vocal · {r['key']} · {r['bpm']} BPM · 원고 작성 중 — 생성 전"
    exp = (r["title"], role, "—", r["type"], f"`input/tracks/{r['order']}_{r['title']}.txt`")
    check(tuple(c[1:6]) == exp, f"[{r['order']}] Track Map row == json (title, vocal/key/BPM/status, type, path)")

print()
print("TOTAL FAILS:", len(fails))
sys.exit(1 if fails else 0)
