#!/usr/bin/env python3
"""B2 apply: tracks 16 여름밤, 17 막차, 18 벚꽃, 19 그네 -> original STYLE + wording corrections (젠 2026-11-02).

Base files are the PRESERVED pre-change copies under
SERIES/23-00/input/source-history/2026-11-02-before-original-style/, so a re-run gives the same result.
Every replacement asserts its expected match count; any mismatch aborts before anything is written.
Writes only: SERIES/23-00/input/tracks/NN_*.txt and .ai/lyrics/2026-11-01_23-00_NN_*-full-draft.md (tracks 16-19).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from wavvy_harness import gate  # noqa: E402  (read-only use: _extract_section for the Draft hash)
from wavvy_harness.source import parse_track_source_fields  # noqa: E402

HIST = ROOT / "SERIES/23-00/input/source-history/2026-11-02-before-original-style"
TRACKS = ROOT / "SERIES/23-00/input/tracks"
LYRICS = ROOT / ".ai/lyrics"
FINAL = json.loads((ROOT / ".ai/plans/2026-11-02-2300-final-styles.json").read_text(encoding="utf-8"))
ENTRIES = {e["order"]: e for e in FINAL["entries"]}

QUOTE_LOFI = "공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 얼터너티브나 모던 알앤비는 제외"
QUOTE_BPM = "원곡 BPM 그대로"
QUOTE_MALE = "원곡대로 남성"

TRACK_NAMES = {16: "16_여름밤", 17: "17_막차", 18: "18_벚꽃", 19: "19_그네"}

# lyric corrections (오케스트레이터 교정표): old whole line -> new whole line
FIXES = {
    16: [],
    17: [("머리에서 나던 샴푸 냄새가 아직 나요", "그 샴푸 향기가 아직 코끝에 남았어요"),
         ("왠지 네가 앉아 있는 듯이 아늑해요", "네가 앉았던 것처럼 괜히 따뜻해요")],
    18: [("꽃잎들이 살짝 모여 쉬었네", "꽃잎 한 장이 사뿐히 앉았네"),
         ("봄 하나 얹고", "머리에 한 장")],
    19: [("내 몸이 먼저 기억을 하네", "두 다리가 먼저 흔들려 와")],
}

GENRE = {
    16: "Korean Lo-fi R&B, Felt Piano-led, soft shaker, hazy ambient pad, cinematic but restrained (original 물안개 STYLE wording)",
    17: "Korean Slow R&B Ballad, supportive warm pad texture, minimal drums or drumless verses, soft bass (original 골목 STYLE wording)",
    18: "Korean Soft R&B, Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture (original 이름 STYLE wording)",
    19: "Korean Soft R&B, Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture (original 이름 STYLE wording)",
}

# section bars: (old fragment, new fragment, occurrence selector) applied to the "Name=n; ..." list
def bars_16(s):
    head, last = s.rsplit("Chorus=7; Powerful belt, no backing vocals=1", 1)
    assert last == "", last
    assert s.count("Chorus=7; Powerful belt, no backing vocals=1") == 2
    return head + "Chorus=9; Powerful belt, no backing vocals=1"


def bars_17(s):
    assert s.count("Chest voice=3; Instrumental=11; Chorus=1") == 1
    s = s.replace("Chest voice=3; Instrumental=11; Chorus=1", "Chest voice=3; Instrumental=5; Chorus=1")
    assert s.endswith("Outro=2; Instrumental=8")
    return s[: -len("Instrumental=8")] + "Instrumental=3"


def bars_18(s):
    old = "Verse 1=10; Chorus=12; Verse 2=12; Bridge=10; Chorus=12; Outro=8; Ending=2"
    assert s.count(old) == 1
    return s.replace(old, "Verse 1=9; Chorus=11; Verse 2=11; Bridge=10; Chorus=11; Outro=8; Ending=1")


def bars_19(s):
    old = "Outro=6; Ending=1"
    assert s.endswith(old)
    return s[: -len(old)] + "Outro=7; Ending=2"


BARS = {16: bars_16, 17: bars_17, 18: bars_18, 19: bars_19}
EXPECT_BARS = {16: 46, 17: 58, 18: 65, 19: 65}
TARGET = {16: 138, 17: 207, 18: 214, 19: 214}


def sub1(text, old, new, n=1):
    c = text.count(old)
    assert c == n, f"expected {n} match(es), found {c}: {old[:90]!r}"
    return text.replace(old, new)


def line_set(text, prefix, new_line):
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, f"prefix {prefix!r}: {len(idx)} lines"
    lines[idx[0]] = new_line
    return "\n".join(lines)


def line_get(text, prefix):
    idx = [l for l in text.split("\n") if l.startswith(prefix)]
    assert len(idx) == 1, f"prefix {prefix!r}: {len(idx)} lines"
    return idx[0]


def append_clause(text, prefix, clause):
    line = line_get(text, prefix)
    assert line.endswith("."), line[-40:]
    return line_set(text, prefix, line[:-1] + "; " + clause + ".")


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()


def whole_line_replace(text, old, new, label):
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l == old]
    assert len(idx) == 1, f"{label}: whole line {old!r} found {len(idx)}x"
    lines[idx[0]] = new
    return "\n".join(lines)


def build_txt(order):
    e = ENTRIES[order]
    name = TRACK_NAMES[order]
    old_raw = (HIST / f"{name}.txt").read_text(encoding="utf-8")
    meta, sections = parse_track_source_fields(old_raw)
    assert set(sections) <= {"STYLE", "EXCLUDE", "LYRICS", "META"}, sections.keys()
    # old section bars / target duration pieces
    old_bars_line = meta["Section Bars"]
    bars_list, _, bars_tail = old_bars_line.partition(" (")
    new_list = BARS[order](bars_list)
    total = sum(int(x.rsplit("=", 1)[1]) for x in new_list.split("; "))
    assert total == EXPECT_BARS[order], (order, total)
    bpm = int(e["bpm_header"])
    est = total * 4 * 60 / bpm
    assert est >= TARGET[order], (order, est)
    tail = f"({total} bars, about {est:.1f} seconds at {bpm} BPM; arrangement estimate only"
    if order == 16:
        tail += "; each cue-only tag line takes 1 bar of its section; the last Chorus has 2 extra bars for the felt-piano fade (original STYLE: Outro felt piano notes fading into silence)"
    tail += ")"
    bars_line = f"{new_list} {tail}"

    style_type = e["type"]
    exclude_line = ", ".join(e["exclude"])
    status_line = (f"original {style_type} STYLE with the Lo-fi Remix prefix and its original EXCLUDE, from "
                   f".ai/plans/2026-11-02-2300-final-styles.json order {order} (STYLE {e['style_chars']} characters, "
                   f"sha256 {e['style_sha256']}; EXCLUDE {len(e['exclude'])} items), used unchanged; same as concept.md ## Original Styles")

    header = [
        f"Track: {meta['Track']}",
        f"Order: {meta['Order']}",
        "Status: full-lyric-draft (template lyrics + original style — 젠 2026-11-02); regeneration pending",
        f"Draft Scope: {meta['Draft Scope']}",
        f"Genre: {GENRE[order]}",
        f"BPM: {e['bpm_header']}",
        f"Key: {e['key_header']}",
        f"Vocal: {e['vocal_header']}",
        f"Target Duration: {meta['Target Duration']}",
        f"Meter: {meta['Meter']}",
        f"Section Bars: {bars_line}",
        f"Style/Exclude Status: {status_line}",
        f"Style Type: {style_type}",
        "Style Source: user-supplied original style",
        "Suno Params: " + json.dumps(e["suno_params"], ensure_ascii=False),
    ]
    assert str(order) == meta["Order"].strip().lstrip("0") or int(meta["Order"]) == order

    lyrics = sections["LYRICS"]
    for old, new in FIXES[order]:
        lyrics = whole_line_replace(lyrics, old, new, f"txt {order}")

    body = ["\n".join(header), "", "=== STYLE ===", e["style"], "", "=== EXCLUDE ===", exclude_line, "", "=== LYRICS ===", lyrics]
    out = "\n".join(body) + "\n"
    if order == 16:
        assert "META" in sections
        new_meta = ("Track 16 of the 23:00 series (temporary number). The STYLE is the original 물안개 song's STYLE with the Lo-fi Remix prefix, "
                    "and the EXCLUDE is its original list, both used byte for byte from the final-styles record "
                    "(concept.md ## Original Styles); BPM 80, Key Eb Major and the male vocal come from that original STYLE (젠: 「원곡 BPM 그대로」, 「원곡대로 남성」). "
                    "The lyric is original wording on the type original's lyric frame (row count, tag lines, per-row syllable counts and repeated rows); "
                    "the type's reference remix lyric supplied only that frame. "
                    "No generated audio exists in this repository for duration, tempo, key, vocal, or arrangement verification.")
        out += "\n=== META ===\n" + new_meta + "\n"
    else:
        assert "META" not in sections
    return out, total, est, meta, sections


def old_style_info(order):
    raw = (HIST / f"{TRACK_NAMES[order]}.txt").read_text(encoding="utf-8")
    meta, sections = parse_track_source_fields(raw)
    st = sections["STYLE"]
    return {"chars": len(st), "sha": sha(st), "bpm": meta["BPM"].split()[0], "key": meta["Key"].split(" (")[0],
            "vocal": meta["Vocal"].split()[0], "txt_sha": sha(raw.encode("utf-8"))}


def source_map_bullets(order, old_txt_sha, old_rec_sha, oi):
    e = ENTRIES[order]
    name = TRACK_NAMES[order]
    rec = f"2026-11-01_23-00_{name}-full-draft.md"
    src = e["source"]
    edits = "; ".join(f"`{x['id']}` {x['kind']}: {x['reason']}" for x in e["edits"])
    sp = e["suno_params"]
    fixes = FIXES[order]
    if fixes:
        fixtxt = "; ".join(f"`{o}` -> `{n}` (both {len(re.findall(r'[가-힣]', o))} Hangul syllables)" for o, n in fixes)
        fixline = (f"- Draft changes in this update (젠 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」, wording only, "
                   f"{len(fixes)} row{'s' if len(fixes) > 1 else ''}, each applied to the Draft and the txt LYRICS the same number of times): {fixtxt}.")
    else:
        fixline = "- Draft changes in this update: none (no wording correction was needed; the Draft is byte for byte the previous version's)."
    excl_origin = src.get("exclude_origin", "")
    if src.get("exclude_lines"):
        excl_origin += f" (lines {src['exclude_lines']})"
    bullets = [
        (f"- 젠 원문 (2026-11-02, original style, tempo and vocal — applied by this update): 「{QUOTE_LOFI}」; 「{QUOTE_BPM}」; 「{QUOTE_MALE}」; "
         "「- 붙은 스타일은 exclude인거 알지?」; 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」; 「Lo-fi remix는 붙여야해 안전빵이야」. "
         "The lyric frame stays under the earlier 「기존 곡 가사 글자 수 그대로 내용만 바꿔」."),
        (f"- Original style source: `.ai/plans/2026-11-02-2300-final-styles.json` entry order {order} (`{e['title']}`, type 「{e['type']}」; STYLE {e['style_chars']} characters, "
         f"sha256 `{e['style_sha256']}`; EXCLUDE {len(e['exclude'])} items), the same values as `SERIES/23-00/concept.md` `## Original Styles` `### {e['type']}`. "
         f"Origin of the original text: `{src['path']}` {src['heading']}, STYLE lines {src['style_lines']}; EXCLUDE: {excl_origin}. "
         f"Edits to the original text (from the json `edits`): {edits}. "
         f"Suno params: weirdness {sp['weirdness']}, style_influence {sp['style_influence']} ({sp['source']}). "
         f"Header values read from the STYLE: BPM {e['bpm_header']}, Key {e['key_header']}, Vocal {e['vocal_header']}."),
        (f"- Previous version before the original-style step (preserved 2026-11-02): txt `SERIES/23-00/input/source-history/2026-11-02-before-original-style/{name}.txt` "
         f"(sha256 `{old_txt_sha}`) and record `SERIES/23-00/input/source-history/2026-11-02-before-original-style/lyrics-records/{rec}` (sha256 `{old_rec_sha}`). "
         f"It carried the 23:00 new-song STYLE (`.ai/plans/2026-11-01-2300-new-song-styles.json`, {oi['chars']} characters, sha256 `{oi['sha']}`), "
         f"BPM {oi['bpm']}, Key {oi['key']}, {oi['vocal']} vocal, and the Draft before the wording corrections."),
        fixline,
    ]
    return "\n".join(bullets) + "\n"


STRATEGY_DURATION = {
    16: ("- duration_plan: 46 bars in 4/4 at 80 BPM estimate 138.0 seconds against a 138-second target (the type original's displayed 2:18). "
         "The tempo moved from 76 to the original's 80 BPM, so the last Chorus tag gets 2 more bars (Chorus 7 to 9) for the felt-piano fade that the original STYLE asks for, and no other section changed. "
         "This does not measure or guarantee generated audio; the first version's two clips displayed 3:22 and 3:30."),
    17: ("- duration_plan: 58 bars in 4/4 at 67 BPM estimate 207.8 seconds against the 207-second target (3:27, the 골목 original's length). "
         "The tempo moved from 80 to the original's 67 BPM, so the Instrumental dip went from 11 to 5 bars and the closing Instrumental from 8 to 3 bars, while every sung section kept its bars. "
         "This plan does not measure or guarantee generated audio; the earlier versions generated about 3:00."),
    18: ("- duration_plan: 65 bars in 4/4 at 72 BPM estimate 216.7 seconds toward the 214 second target (the type original's displayed 3:34). "
         "The tempo moved from 78 to the original's 72 BPM, so Verse 1 (10 to 9), both Choruses (12 to 11), Verse 2 (12 to 11) and the Ending (2 to 1) each lost bars while Intro, Bridge and Outro kept theirs; "
         "planned bars only, not measured audio. The first generation of this track ran 3:05 and 3:00 as audio."),
    19: ("- duration_plan: 65 bars in 4/4 at 72 BPM estimate 216.7 seconds toward the 214 second target (the type original's displayed 3:34). "
         "The tempo moved from 70 to the original's 72 BPM, so the Outro (6 to 7) and the Ending (1 to 2) each gained a bar and no other section changed; "
         "planned bars only, not measured audio. The first generation of this track ran 2:38 and 2:41 as audio."),
}

VOCAL_IDENTITY = {
    16: ("- vocal_identity: one male lead, warm soulful tone, dry close-mic, slightly breathy, straight delivery, minimal vibrato, no backing vocals or doubles, "
         "from the original 물안개 STYLE (`Male vocal`) — 젠 「원곡대로 남성」; audio not verified."),
    17: ("- vocal_identity: one male lead, raw dry chest voice, speech-like phrasing, no falsetto, runs or melisma, from the original 골목 STYLE (`Male vocal`); audio not verified."),
    18: ("- vocal_identity: one male lead, natural, laid-back, raw, solid, direct and dry, chest voice dominant, no falsetto, straight tone, no vibrato, no ad-libs, "
         "from the original 이름 STYLE (`Male vocal`) — 젠 「원곡대로 남성」; audio not verified."),
    19: ("- vocal_identity: one male lead, natural, laid-back, raw, solid, direct and dry, chest voice dominant, no falsetto, straight tone, no vibrato, no ad-libs, "
         "from the original 이름 STYLE (`Male vocal`) — 젠 「원곡대로 남성」; audio not verified."),
}

GENRE_LANE = {
    16: "- genre_lane: Korean Lo-fi R&B, Felt Piano-led, soft shaker, hazy ambient pad, cinematic but restrained, from the original 물안개 STYLE (with the Lo-fi Remix prefix).",
    17: "- genre_lane: Korean Slow R&B Ballad with a supportive warm pad, minimal drums or drumless verses and soft low bass, from the original 골목 STYLE (with the Lo-fi Remix prefix).",
    18: "- genre_lane: Korean Soft R&B, Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture, from the original 이름 STYLE (with the Lo-fi Remix prefix).",
    19: "- genre_lane: Korean Soft R&B, Soft Synth Pad-led, supportive groove, gentle pulse, warm shade texture, from the original 이름 STYLE (with the Lo-fi Remix prefix).",
}

OVERRIDE_CLAUSE = ("STYLE, EXCLUDE, BPM, Key and vocal gender follow the original song, with only the Lo-fi Remix prefix added and the edits listed in Source Map "
                   f"(젠 2026-11-02 「{QUOTE_LOFI}」, 「{QUOTE_BPM}」, 「{QUOTE_MALE}」)")


def build_record(order, new_txt_sections, total):
    e = ENTRIES[order]
    name = TRACK_NAMES[order]
    rec_name = f"2026-11-01_23-00_{name}-full-draft.md"
    old_text = (HIST / "lyrics-records" / rec_name).read_text(encoding="utf-8")
    text = old_text
    oi = old_style_info(order)
    old_txt_sha = oi["txt_sha"]
    old_rec_sha = sha(old_text.encode("utf-8"))

    # sanity: the old claimed hash matches the old Draft
    old_claim = line_get(old_text, "- Source SHA256: ").split(": ", 1)[1]
    assert old_claim == sha(gate._extract_section(old_text, "Draft")), "old Source SHA256 does not match old Draft"

    # --- Draft lyric corrections
    pre, rest = text.split("\n## Draft\n", 1)
    draft, post = rest.split("\n## Self-Gate\n", 1)
    for old, new in FIXES[order]:
        draft = whole_line_replace(draft, old, new, f"record {order} Draft")
    text = pre + "\n## Draft\n" + draft + "\n## Self-Gate\n" + post

    # --- Source Map: superseded STYLE bullet + new bullets
    text = {
        16: lambda t: sub1(t, "- STYLE: `.ai/plans/2026-11-01-2300-new-song-styles.json` order 16",
                           "- Superseded STYLE (the version before 2026-11-02; replaced by the original style recorded below): `.ai/plans/2026-11-01-2300-new-song-styles.json` order 16"),
        17: lambda t: sub1(t, "- STYLE source: `.ai/plans/2026-11-01-2300-new-song-styles.json` order 17",
                           "- Superseded STYLE source (the version before 2026-11-02; replaced by the original style recorded below): `.ai/plans/2026-11-01-2300-new-song-styles.json` order 17"),
        18: lambda t: sub1(t, "- Confirmed STYLE: `.ai/plans/2026-11-01-2300-new-song-styles.json` entry order 18",
                           "- Superseded STYLE (the version before 2026-11-02; replaced by the original style recorded below): `.ai/plans/2026-11-01-2300-new-song-styles.json` entry order 18"),
        19: lambda t: sub1(t, "- Confirmed STYLE: `.ai/plans/2026-11-01-2300-new-song-styles.json` entry order 19",
                           "- Superseded STYLE (the version before 2026-11-02; replaced by the original style recorded below): `.ai/plans/2026-11-01-2300-new-song-styles.json` entry order 19"),
    }[order](text)
    text = sub1(text, "\n- Authority: ", "\n" + source_map_bullets(order, old_txt_sha, old_rec_sha, oi) + "- Authority: ")

    # --- template-check result path (re-run on the corrected lyric)
    old_path = f".ai/validation/2026-11-01-2300-lyrics/{order}-template-check.json"
    n_old = text.count(old_path)
    if n_old:
        text = text.replace(old_path, f".ai/validation/2026-11-02-2300-styles/{order}-template-check.json")

    # --- Constraint Freeze
    text = line_set(text, "- genre_lane: ", GENRE_LANE[order])
    bpm = int(e["bpm_header"])
    key_text = {16: 'Eb Major, from the original 물안개 STYLE (`key Eb Major`)', 17: 'Db Major, from the original 골목 STYLE',
                18: 'Ab Major, from the original 이름 STYLE', 19: 'Ab Major, from the original 이름 STYLE'}[order]
    bpm_src = {16: "물안개", 17: "골목", 18: "이름", 19: "이름"}[order]
    text = line_set(text, "- bpm: ", f"- bpm: {bpm}, from the original {bpm_src} STYLE (`{bpm} BPM`); no audio measured.")
    text = line_set(text, "- key: ", f"- key: {key_text}; no audio measured.")
    text = line_set(text, "- vocal_identity: ", VOCAL_IDENTITY[order])
    # section_bars, target
    sb = line_get(text, "- section_bars: ").split(": ", 1)[1]
    text = line_set(text, "- section_bars: ", "- section_bars: " + BARS[order](sb))
    assert line_get(text, "- target_duration_seconds: ") == f"- target_duration_seconds: {TARGET[order]}"
    # explicit_overrides
    if order == 17:
        text = line_set(text, "- explicit_overrides: ",
                        "- explicit_overrides: original-style override (젠 2026-11-02): " + OVERRIDE_CLAUSE + "; the original's inline EXCLUDE line is the EXCLUDE field.")
    else:
        text = append_clause(text, "- explicit_overrides: ", OVERRIDE_CLAUSE)

    # --- per-track Constraint Freeze / Strategy / Self-Gate text
    if order == 16:
        text = sub1(text, "- mood: drowsy, warm, close longing; a night she does not want to end.", "- mood: drowsy, warm, close longing; a night he does not want to end.")
        text = sub1(text, "the listed bars add up to 44.", "the listed bars add up to 46 (the last Chorus tag carries 2 extra bars for the fade).")
        text = sub1(text, "one woman recalling a summer night", "one man recalling a summer night")
        text = sub1(text, "and her reluctance to sleep.", "and his reluctance to sleep.")
        text = sub1(text, "Bridge 2 cools her forehead", "Bridge 2 cools his forehead")
        text = sub1(text, "exactly how someone would say it with her mouth full.", "exactly how someone would say it with his mouth full.")
        text = sub1(text, "one female chest-voice lead;", "one male close-mic lead (dry, straight delivery);")
        text = sub1(text, "at 76 BPM over muted Rhodes;", "at 80 BPM over felt piano;")
        text = sub1(text, "a half-beat where the Rhodes can answer", "a half-beat where the felt piano can answer")
    if order == 17:
        text = sub1(text, "type, vocal, BPM, key and title are unchanged from the lyrics brief design table.",
                    "type, vocal and title are unchanged from the lyrics brief design table; BPM and key now come from the original 골목 STYLE (2026-11-02).")
        text = sub1(text, "Verse 4 the weight and the shampoo smell,", "Verse 4 the weight and the shampoo scent that lingers,")
        text = sub1(text, "Verse 5 the empty seat that feels cozy,", "Verse 5 the empty seat that feels warm as if you had sat there,")
        text = sub1(text, "the eleven-bar Instrumental dip", "the five-bar Instrumental dip", 2)
        text = sub1(text, "vocal rests for the Rhodes and muted guitar.", "vocal rests for the warm pad and a soft guitar line.")
        text = sub1(text, "dip with Rhodes and muted guitar follows", "dip with the warm pad and a soft guitar line follows")
        text = sub1(text, "lane at 80 BPM, in the 골목", "lane at 67 BPM, in the 골목")
        # Self-Gate quotes of changed rows
        text = sub1(text, '- Longest Sung Line: PASS | "머리에서 나던 샴푸 냄새가 아직 나요" |', '- Longest Sung Line: PASS | "그 샴푸 향기가 아직 코끝에 남았어요" |')
        text = sub1(text, '"빈 옆자리에 가방을 놓았는데 / 왠지 네가 앉아 있는 듯이 아늑해요"', '"빈 옆자리에 가방을 놓았는데 / 네가 앉았던 것처럼 괜히 따뜻해요"')
    if order == 18:
        text = sub1(text, "벚꽃 · 이름 · female · C Major · 78 — ",
                    "벚꽃 · 이름 · female · C Major · 78 (first-version design values; replaced 2026-11-02 by the original 이름 STYLE: male · Ab Major · 72) — ")
        text = sub1(text, "a woman under a cherry tree in a later spring; a petal lands on her head and she remembers the hand that once lifted petals out of her hair,",
                    "a man under a cherry tree in a later spring; a petal lands on his head and he remembers the hand that once lifted petals out of his hair,")
        text = sub1(text, "(40 of 50 sung rows are equal in chunk shape)", "(38 of 50 sung rows are equal in chunk shape)")
        text = sub1(text, "Chunk shape is equal on 40 of 50 sung rows;", "Chunk shape is equal on 38 of 50 sung rows (the two reworded rows, Verse 1 row 4 and Bridge row 5, group their words differently from the frame);")
        text = sub1(text, "one woman under a cherry tree in a later spring, talking to herself;", "one man under a cherry tree in a later spring, talking to himself;")
        text = sub1(text, "and a petal on her hair in the present", "and a petal on his hair in the present")
        text = sub1(text, "and ends with her catching a petal herself;", "and ends with him catching a petal himself;")
        text = sub1(text, "the Outro lands a petal on her head.", "the Outro lands a petal on his head.")
        text = sub1(text, "(`난 그저 웃고 있어`, `봄 하나 얹고`, `따뜻해`)", "(`난 그저 웃고 있어`, `머리에 한 장`, `따뜻해`)")
        text = sub1(text, "where `female vocal` is already appended.", "where `Male vocal` is already written by the original STYLE.")
        text = sub1(text, "one petal lands on her head, and the next rows", "one petal lands on his head, and the next rows")
        text = sub1(text, "The petal on her head leads straight", "The petal on his head leads straight")
        text = sub1(text, "being content as she is;", "being content as he is;")
        text = sub1(text, "one female chest-voice lead;", "one male chest-voice lead;")
        text = sub1(text, "Relaxed warm longing at 78 BPM in the 이름 lo-fi indie R&B lane;", "Relaxed warm longing at 72 BPM in the 이름 Soft R&B lane;")
        text = sub1(text, "while the electric piano answers.", "while the synth pad answers.")
        text = sub1(text, "while the piano holds its chord.", "while the pad holds its chord.")
    if order == 19:
        text = sub1(text, "그네 · 이름 · female · E Minor · 70 — ",
                    "그네 · 이름 · female · E Minor · 70 (first-version design values; replaced 2026-11-02 by the original 이름 STYLE: male · Ab Major · 72) — ")
        text = sub1(text, "remembered as a gentle rocking that her body still keeps.", "remembered as a gentle rocking that his body still keeps.")
        text = sub1(text, "- mood: warm, hushed and relaxed in a minor key: two swings", "- mood: warm, hushed and relaxed: two swings")
        text = sub1(text, "one woman remembering a night on two side-by-side swings, talking to herself;", "one man remembering a night on two side-by-side swings, talking to himself;")
        text = line_set(text, "- connection: ",
                        "- connection: the Intro sets two swings and the night wind; Verse 1 has `네` push off first and the narrator follow, and two different beats become one (two shadows overlap); "
                        "the Chorus lets him close his eyes and still feel the night air, the night spent side by side, the sway kept in his body and the lullaby-like chain sound; "
                        "Verse 2 climbs higher (wind on the cheek, the sky full, starlight on `네`'s profile, silence that was enough) and ends with his legs starting to swing first when he stands before a playground; "
                        "the Bridge lets the swing stop slowly while the chain's resonance stays and the night holds him; the Outro keeps starlight, a little sway and quiet.")
        text = sub1(text, "where `female vocal` is already appended.", "where `Male vocal` is already written by the original STYLE.")
        text = line_set(text, "- Connection: PASS | ",
                        '- Connection: PASS | "두 다리가 먼저 흔들려 와" | The Chorus\'s kept sway and the Verse 2 climb come together when he stands before a playground and his legs start to swing before he has thought of it.')
        text = sub1(text, "one female chest-voice lead;", "one male chest-voice lead;")
        text = sub1(text, "Relaxed warm longing at 70 BPM in the 이름 lo-fi indie R&B lane;", "Relaxed warm longing at 72 BPM in the 이름 Soft R&B lane;")
        text = sub1(text, "while the electric piano answers.", "while the synth pad answers.")
        text = sub1(text, "while the piano holds its chord.", "while the pad holds its chord.")
    text = line_set(text, "- duration_plan: ", STRATEGY_DURATION[order])

    # --- Source SHA256 of the (possibly corrected) Draft
    new_hash = sha(gate._extract_section(text, "Draft"))
    text = line_set(text, "- Source SHA256: ", f"- Source SHA256: {new_hash}")
    if not FIXES[order]:
        assert new_hash == old_claim, "Draft unchanged for track 16 but hash differs"
    return text, new_hash, {"old_txt_sha256": old_txt_sha, "old_record_sha256": old_rec_sha, "old_style": oi, "template_path_replacements": n_old}


def main():
    summary = {}
    outputs = {}
    for order in (16, 17, 18, 19):
        txt, total, est, meta, sections = build_txt(order)
        rec, rec_hash, info = build_record(order, sections, total)
        outputs[order] = (txt, rec)
        summary[order] = {"bars": total, "estimate_seconds": round(est, 2), "draft_sha256": rec_hash, **info}
    # all assertions passed -> write
    for order, (txt, rec) in outputs.items():
        name = TRACK_NAMES[order]
        (TRACKS / f"{name}.txt").write_text(txt, encoding="utf-8")
        (LYRICS / f"2026-11-01_23-00_{name}-full-draft.md").write_text(rec, encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
