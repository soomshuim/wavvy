#!/usr/bin/env python3
"""B2 step 2-4: apply the lyric corrections, the original STYLE/EXCLUDE/headers and the record updates to tracks 11-15.

Brief: .ai/plans/2026-11-02-2300-style-apply-b-brief.md
Input values: .ai/plans/2026-11-02-2300-final-styles.json (copied byte for byte).
Safety: refuses to run unless the current txt/record are byte-identical to the preserved copies from
b2-preserve-11-15.json, so a second run cannot double-apply. Every replacement asserts its match count.
Writes b2-apply-11-15.json with the per-track change summary.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path.home() / "Project/wavvy"
sys.path.insert(0, str(ROOT))
from wavvy_harness.gate import _extract_section  # read-only: same Draft extraction the gate uses

FINAL = json.loads((ROOT / ".ai/plans/2026-11-02-2300-final-styles.json").read_text(encoding="utf-8"))
OLD_STYLES = {e["order"]: e for e in json.loads((ROOT / ".ai/plans/2026-11-01-2300-new-song-styles.json").read_text(encoding="utf-8"))}
PRESERVE = json.loads((ROOT / ".ai/validation/2026-11-02-2300-styles/b2-preserve-11-15.json").read_text(encoding="utf-8"))
HIST = "SERIES/23-00/input/source-history/2026-11-02-before-original-style"
OUT = ROOT / ".ai/validation/2026-11-02-2300-styles/b2-apply-11-15.json"
ENTRIES = {e["order"]: e for e in FINAL["entries"]}

STATUS = "full-lyric-draft (template lyrics + original style — 젠 2026-11-02); regeneration pending"

# Per-track values. txt-only and record-only pieces are kept separate on purpose.
CFG = {
    11: {
        "title": "라디오",
        "genre": "Lo-fi Remix, Korean Soft R&B, vibraphone-led supportive R&B groove, laid-back brush rhythm, warm afternoon texture (먼지 original STYLE)",
        "section_bars_header": None,  # same list; only the estimate text changes (see header_replace)
        "header_replace": [("about 205.7 seconds at 70 BPM", "about 200.0 seconds at 72 BPM")],
        "lyric_fixes": [
            ("\n낮은 목소리가 사연을\n", "\n낮은 목소리 사연 하나\n", 1),
            ("\n읽고 나면 잡음 속에서\n", "\n끝나고 나면 잡음 속에\n", 1),
            ("\n틀린 가사 신나게 부르던\n", "\n틀린 가사 신나게 부른 너\n", 1),
        ],
        "fix_summary": "`낮은 목소리가 사연을` -> `낮은 목소리 사연 하나`; `읽고 나면 잡음 속에서` -> `끝나고 나면 잡음 속에`; `틀린 가사 신나게 부르던` -> `틀린 가사 신나게 부른 너`. Applied once each in this Draft and in the txt LYRICS (3 corrections, 3 rows)",
        "rec_lines": {
            "- genre_lane:": "- genre_lane: Korean Soft R&B, vibraphone-led supportive R&B groove, laid-back brush rhythm, warm afternoon texture (the 먼지 original STYLE with the `Lo-fi Remix, ` prefix).",
            "- bpm:": "- bpm: 72, the 먼지 original STYLE's own BPM (`72 BPM`), kept as in the original per 젠 「원곡 BPM 그대로」; no audio measured.",
            "- key:": "- key: Eb Major, the 먼지 original STYLE's own key (`Eb Major`); no audio measured.",
            "- vocal_identity:": "- vocal_identity: one male lead, natural and intimate: raw, solid, direct, dry, chest voice dominant, no falsetto, minimal vibrato, a single lead vocal throughout (from the original 먼지 STYLE; audio not verified).",
            "- duration_plan:": "- duration_plan: 60 bars in 4/4 at 72 BPM estimate 200.0 seconds toward a 200-second target (the 먼지 original runs 3:20; the estimate meets the target exactly). This does not measure or guarantee generated audio.",
            "- Series DNA:": "- Series DNA: PASS | Relaxed 72 BPM Korean Soft R&B groove with a vibraphone lead and a laid-back brush rhythm (the 먼지 original STYLE); faint warm longing built from sound instead of statement, as the 23:00 direction asks; the Chorus repeats like the 먼지 original and the rows stay short.",
        },
        "rec_phrases": [
            ("the low voice reading letters, the static and then a familiar intro coming out of it",
             "the low voice and one listener's story, then, once it ends, the static and a familiar intro coming out of it", 1),
        ],
        "meta": None,
    },
    12: {
        "title": "스웨터",
        "genre": "Lo-fi Remix, Korean R&B/pop ballad, Piano/Rhodes-led, cinematic but restrained (마음 밖 original STYLE)",
        "section_bars_header": "Intro: Instrumental=4; Verse 1=10; Bridge=6; Chorus=10; Verse 2=10; Bridge=6; Chorus=10; Chorus=12; Outro: Instrumental fade out=8 (76 bars, about 190.0 seconds at 96 BPM, the low end of the original STYLE's 96–106 BPM; arrangement estimate only)",
        "header_replace": [],
        "lyric_fixes": [],
        "fix_summary": None,
        "rec_lines": {
            "- genre_lane:": "- genre_lane: Korean R&B/pop ballad, Piano/Rhodes-led, cinematic but restrained (the 마음 밖 original STYLE with the `Lo-fi Remix, ` prefix).",
            "- bpm:": "- bpm: 96–106 (the original STYLE says `96–106 BPM`; the txt header reads `96–106 (original STYLE wording; release file 90)`); the duration estimate uses the first number, 96, the low end; no audio measured.",
            "- key:": "- key: A♭ (the original STYLE says `key color like A♭`; mode not stated); no audio measured.",
            "- vocal_identity:": "- vocal_identity: one forward, dry, close-mic female lead: warm husky tone, clear Korean diction, conversational phrasing, controlled vibrato, natural breaths, minimal pitch correction (from the original 마음 밖 STYLE; audio not verified).",
            "- section_bars:": "- section_bars: Intro: Instrumental=4; Verse 1=10; Bridge=6; Chorus=10; Verse 2=10; Bridge=6; Chorus=10; Chorus=12; Outro: Instrumental fade out=8",
            "- density_and_breath:": "- density_and_breath: rows follow the template's short 4-7 syllable lengths; Verses are five rows in 10 bars, Bridges four rows in 6 bars, Chorus six rows in 10 bars (the middle Chorus four rows in 10 bars, the final Chorus six rows in 12 bars); a row break alone is not counted as a breath, so the Intro and Outro bars and the held bars after each Chorus pair carry the rests.",
            "- duration_plan:": "- duration_plan: 76 bars in 4/4 at 96 BPM (the low end of the original STYLE's 96–106 BPM; the gate reads the first number) estimate 190.0 seconds toward a 188-second target (the 마음 밖 original runs 3:08); the same 76 bars at 106 BPM would run about 172.1 seconds. This does not measure or guarantee generated audio.",
            "- Series DNA:": "- Series DNA: PASS | Korean R&B/pop ballad at the original's 96–106 BPM with a Piano/Rhodes lead, cinematic but restrained (the 마음 밖 original STYLE); faint warm longing built from touch and smell instead of statement, as the 23:00 direction asks; rows are short and the Chorus repeats like the 마음 밖 original.",
            "- Wavvy Identity:": "- Wavvy Identity: PASS | Korean sung rows only and one female lead (warm husky, close and dry); no harmony, backing vocal, falsetto or choir is needed.",
        },
        "rec_phrases": [],
        "meta": None,
    },
    13: {
        "title": "편지",
        "genre": "Lo-fi Remix, Korean Chill R&B, felt piano-led with warm Rhodes chords, soft brush kit, warm bass groove (작은 빛 original STYLE)",
        "section_bars_header": None,
        "header_replace": [],
        "lyric_fixes": [
            ("\n“잘 있어\n잘 있어”\n", "\n“따뜻해\n따뜻해”\n", 1),
            ("\n또 올게\n또 올게\n", "\n또 볼게\n또 볼게\n", 1),
        ],
        "fix_summary": "`“잘 있어 / 잘 있어”` (the two quote-split rows, quote marks kept in place) -> `“따뜻해 / 따뜻해”`; `또 올게` (both rows) -> `또 볼게`. Applied once each in this Draft and in the txt LYRICS (2 corrections, 4 rows)",
        "rec_lines": {
            "- genre_lane:": "- genre_lane: Korean Chill R&B, felt piano-led with warm Rhodes chords, soft brush kit and a warm bass groove (the 작은 빛 original STYLE with the `Lo-fi Remix, ` prefix).",
            "- bpm:": "- bpm: 72, the 작은 빛 original STYLE's own BPM (`72 BPM`), kept as in the original per 젠 「원곡 BPM 그대로」; no audio measured.",
            "- key:": "- key: Db Major, the 작은 빛 original STYLE's own key (`Db Major`); no audio measured.",
            "- vocal_identity:": "- vocal_identity: one warm baritone male lead: warm, intimate, dry chest voice with conversational phrasing; the lead stays single, no stacked or choir-like harmonies (from the original 작은 빛 STYLE; audio not verified).",
            "- Series DNA:": "- Series DNA: PASS | 72 BPM Korean Chill R&B with a felt-piano lead and warm Rhodes chords (the 작은 빛 original STYLE); faint warm longing built from touch, sound and smell instead of statement, as the 23:00 direction asks; the Chorus repeats unchanged like the 작은 빛 original.",
        },
        "rec_phrases": [
            ("the Bridge is folding it again, saying a soft goodbye to it, and putting it back.",
             "the Bridge is folding it again along the old creases, murmuring that it is warm, promising to see it again, and putting it back in the drawer.", 1),
            ("to the careful folding and the promise to come back;",
             "to the careful folding and the promise to see it again;", 1),
            ("is the repeated `또 올게`; the template's two quote-split rows are the quote-split `잘 있어`.",
             "is the repeated `또 볼게`; the template's two quote-split rows are the quote-split `따뜻해`.", 1),
        ],
        "meta": None,
    },
    14: {
        "title": "기타",
        "genre": "Lo-fi Remix, Korean Indie R&B, clean electric guitar-led supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle (산책 original STYLE)",
        "section_bars_header": None,
        "header_replace": [],
        "lyric_fixes": [],
        "fix_summary": None,
        "rec_lines": {
            "- genre_lane:": "- genre_lane: Korean Indie R&B, clean electric guitar-led supportive R&B groove, rim-click, warm afternoon texture, subtle vinyl crackle (the 산책 original STYLE with the `Lo-fi Remix, ` prefix; `Alt` removed from `Indie Alt R&B`).",
            "- bpm:": "- bpm: 74, the 산책 original STYLE's own BPM (`74 BPM`), kept as in the original per 젠 「원곡 BPM 그대로」; no audio measured.",
            "- key:": "- key: Eb Major, the 산책 original STYLE's own key (`Eb Major`); no audio measured.",
            "- vocal_identity:": "- vocal_identity: one male lead: solid, direct, raw, dry chest voice, straight tone, no vibrato or ad-libs, a single dominant lead vocal (from the original 산책 STYLE; audio not verified).",
        },
        "rec_phrases": [],
        "meta": "Track 14 of the 23:00 series (temporary number). The STYLE is the user-supplied original 산책 style with the `Lo-fi Remix, ` prefix and the one other edit recorded in SERIES/23-00/concept.md ## Original Styles (the genre word `Alt` removed from `Indie Alt R&B`), declared by `Style Type: 산책` and `Style Source: user-supplied original style`. EXCLUDE holds the 14 original 산책 items. The lyric is original wording on the 산책 original's lyric frame (row count, tag lines, per-row syllable counts and repeat positions kept; every word new). No generated audio exists in this repository for duration, tempo, key, vocal, or arrangement verification.",
    },
    15: {
        "title": "노을",
        "genre": "Lo-fi Remix, Korean Indie R&B, neo-soul chords (M9, m7), clean electric guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle (물결 original STYLE)",
        "section_bars_header": None,
        "header_replace": [],
        "lyric_fixes": [
            ("\n해 지는 쪽부터 주황빛\n", "\n서쪽 하늘이 물들어 가\n", 1),
        ],
        "fix_summary": "`해 지는 쪽부터 주황빛` -> `서쪽 하늘이 물들어 가`. Applied once in this Draft and in the txt LYRICS (1 correction, 1 row)",
        "rec_lines": {
            "- genre_lane:": "- genre_lane: Korean Indie R&B, neo-soul chords (M9, m7), clean electric guitar-led supportive groove, rim-click, warm texture, subtle vinyl crackle (the 물결 original STYLE with the `Lo-fi Remix, ` prefix; `Alt` removed from `Indie Alt R&B`).",
            "- bpm:": "- bpm: 74, the 물결 original STYLE's own BPM (`74 BPM`), kept as in the original per 젠 「원곡 BPM 그대로」; no audio measured.",
            "- key:": "- key: A Major, the 물결 original STYLE's own key (`A Major`); no audio measured.",
            "- vocal_identity:": "- vocal_identity: one male lead: solid, direct, raw, dry, chest-dominant voice, straight tone, no vibrato or ad-libs, narrow range with a speech-like rhythm, a single lead vocal (from the original 물결 STYLE; audio not verified).",
            "- Wavvy Identity:": "- Wavvy Identity: PASS | Korean sung rows only; one male chest-voice lead; no harmony, backing vocal, falsetto, ad-lib or English hook; the txt keeps `Style Type: 물결`, declares `Style Source: user-supplied original style` and holds the 13 original EXCLUDE items in concept.md order.",
        },
        "rec_phrases": [
            ("while the orange starts where the sun goes down;", "while the western sky begins to take on colour;", 1),
            ('- Longest Sung Line: PASS | "해 지는 쪽부터 주황빛" |', '- Longest Sung Line: PASS | "서쪽 하늘이 물들어 가" |', 1),
        ],
        "meta": "Track 15 of the 23:00 series (temporary number). The STYLE is the user-supplied original 물결 style with the `Lo-fi Remix, ` prefix and the one other edit recorded in SERIES/23-00/concept.md ## Original Styles (the genre word `Alt` removed from `Indie Alt R&B`), declared by `Style Type: 물결` and `Style Source: user-supplied original style`. EXCLUDE holds the 13 original 물결 items in concept.md order. The lyric is original wording on the 물결 original's lyric frame (row count, tag lines, per-row syllable counts and repeat positions kept; every word new). No generated audio exists in this repository for duration, tempo, key, vocal, or arrangement verification.",
    },
}


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_line(text, prefix, new_line):
    lines = text.split("\n")
    idx = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(idx) == 1, f"prefix {prefix!r} matched {len(idx)} lines"
    lines[idx[0]] = new_line
    return "\n".join(lines)


def replace_exact(text, old, new, count=1):
    found = text.count(old)
    assert found == count, f"{old!r} found {found} times, expected {count}"
    return text.replace(old, new)


def edit_phrase(edit):
    kind = edit["kind"]
    if kind == "prepend_lofi_remix":
        return "`Lo-fi Remix, ` prepended"
    if kind == "remove_genre_word":
        return f"genre word `{edit['removed_word']}` removed (`{edit['old']}` -> `{edit['new']}`)"
    if kind == "move_inline_exclude_line_to_EXCLUDE":
        added = edit["items_added_to_EXCLUDE"]
        tail = "no item had to be added to EXCLUDE (all were already in the separate Exclude Style block)" if not added else "items added to EXCLUDE: " + ", ".join(added)
        return f"the inline line `{edit['removed_line']}` and the blank line before it moved out of STYLE ({tail})"
    raise AssertionError(f"unknown edit kind {kind}")


def suno_phrase(params):
    if isinstance(params["weirdness"], int):
        return f"Weirdness {params['weirdness']} / Style Influence {params['style_influence']} (from `{params['source']}`)"
    return f"Weirdness default / Style Influence default ({params['source']})"


def style_bullets(n, entry, cfg):
    src = entry["source"]
    old = OLD_STYLES[n]
    exclude_line = (f"EXCLUDE {len(entry['exclude'])} items" if entry["exclude"] else "EXCLUDE empty")
    lines_ref = f"STYLE lines {src['style_lines']}; " + (f"separate Exclude block line {src['exclude_lines']}" if src["exclude_lines"] else src["exclude_origin"])
    edits = "; ".join(edit_phrase(ed) for ed in entry["edits"])
    quotes = " / ".join(f"「{q}」" for q in FINAL["젠_원문"]) + " / 「기존 곡 가사 글자 수 그대로 내용만 바꿔」 / 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」"
    first = (
        f"- STYLE and EXCLUDE (original style, 젠 2026-11-02): the user's original {entry['type']} Suno style prompt, not the 23:00 assembly. "
        f"Final values: `.ai/plans/2026-11-02-2300-final-styles.json` order {n} (STYLE {entry['style_chars']} characters, sha256 `{entry['style_sha256']}`; {exclude_line}), "
        f"the same bytes as `SERIES/23-00/concept.md` `## Original Styles` `### {entry['type']}`. "
        f"Original source: `{src['path']}` `{src['heading']}` ({lines_ref}; original STYLE {entry['original_style_chars']} characters, sha256 `{entry['original_style_sha256']}`). "
        f"Suno parameters: {suno_phrase(entry['suno_params'])}. "
        f"Edits to the original (all of them): {edits}. "
        f"The txt declares `Style Type: {entry['type']}` and `Style Source: user-supplied original style`. "
        f"젠 원문 (2026-11-02): {quotes}. "
        f"The 23:00-assembly STYLE this replaces (`.ai/plans/2026-11-01-2300-new-song-styles.json` order {n}, {old['chars']} characters, sha256 `{old['sha256']}`) survives only in the preserved previous version."
    )
    if cfg["fix_summary"]:
        second = (
            "- Lyric corrections at the original-style step (2026-11-02; orchestrator table, each new row has the same Hangul syllable count as the row it replaces; "
            "젠 「가사 확인 받지 말고 검수할 때 어색하거나 ai스러운 표현만 교정하고 바로 곡 만들어」): " + cfg["fix_summary"] + "."
        )
    else:
        second = "- Lyric corrections at the original-style step (2026-11-02): none; the orchestrator table has no entry for this track, so Draft and txt LYRICS are unchanged."
    return first + "\n" + second


def previous_version_bullet(line, n, title, pres):
    rec_name = f"2026-11-01_23-00_{n}_{title}-full-draft.md"
    txt_sha = pres[(n, "txt")]
    rec_sha = pres[(n, "record")]
    addition = (
        f"(3) template-lyric version with the 23:00-assembly STYLE, before the original-style apply (2026-11-02): "
        f"txt `{HIST}/{n:02d}_{title}.txt` (sha256 `{txt_sha}`) and record `{HIST}/lyrics-records/{rec_name}` (sha256 `{rec_sha}`)."
    )
    assert line.rstrip().endswith("."), line[-40:]
    line = line.rstrip()[:-1] + "; " + addition
    if "Previous versions (two; both preserved before this overwrite, byte-compared by sha256):" in line:
        line = line.replace("Previous versions (two; both preserved before this overwrite, byte-compared by sha256):",
                            "Previous versions (three; each preserved before it was overwritten, byte-compared by sha256):")
    elif "Previous versions (both kept, then overwritten):" in line:
        line = line.replace("Previous versions (both kept, then overwritten):", "Previous versions (three kept, then overwritten):")
    else:
        raise AssertionError("unknown previous-versions wording")
    return line


def section_slice(text, start_marker, end_marker):
    """Return (before, middle, after) around the span from start_marker to end_marker (end exclusive)."""
    s = text.index(start_marker)
    e = text.index(end_marker, s)
    return text[:s], text[s:e], text[e:]


def main():
    pres = {(r["track"], r["kind"]): r["src_sha256"] for r in PRESERVE["rows"]}
    summary = {}
    for n, cfg in CFG.items():
        title, entry = cfg["title"], ENTRIES[n]
        assert entry["title"] == title and entry["order"] == n
        txt_path = ROOT / f"SERIES/23-00/input/tracks/{n:02d}_{title}.txt"
        rec_path = ROOT / f".ai/lyrics/2026-11-01_23-00_{n}_{title}-full-draft.md"
        # refuse a second run
        assert sha_file(txt_path) == pres[(n, "txt")], f"{txt_path} differs from the preserved copy"
        assert sha_file(rec_path) == pres[(n, "record")], f"{rec_path} differs from the preserved copy"
        txt = txt_path.read_text(encoding="utf-8")
        rec = rec_path.read_text(encoding="utf-8")

        # ---------- lyric corrections (txt LYRICS and record Draft, same fixes, same counts) ----------
        txt_pre, txt_ly, txt_post = section_slice(txt, "=== LYRICS ===", "=== META ===") if "=== META ===" in txt else (txt[: txt.index("=== LYRICS ===")], txt[txt.index("=== LYRICS ==="):], "")
        rec_pre, rec_dr, rec_post = section_slice(rec, "\n## Draft\n", "\n## Self-Gate\n")
        for old, new, count in cfg["lyric_fixes"]:
            txt_ly = replace_exact(txt_ly, old, new, count)
            rec_dr = replace_exact(rec_dr, old, new, count)

        # ---------- txt: header, STYLE, EXCLUDE, META ----------
        header_end = txt_pre.index("=== STYLE ===")
        old_header = txt_pre[:header_end].rstrip("\n").split("\n")
        old_vals = {}
        for line in old_header:
            m = re.match(r"^([A-Za-z][A-Za-z0-9 _/-]*):\s*(.*)$", line)
            if m:
                old_vals[m.group(1)] = m.group(2)
        assert old_vals["Track"] == title and old_vals["Order"] == str(n)
        section_bars = cfg["section_bars_header"] or old_vals["Section Bars"]
        for old, new in cfg["header_replace"]:
            section_bars = replace_exact(section_bars, old, new, 1)
        exclude_line = ", ".join(entry["exclude"])
        status_line = (
            f"STYLE and EXCLUDE are the user-supplied original {entry['type']} style: STYLE = `Lo-fi Remix, ` + the original STYLE with the edits listed in "
            f"SERIES/23-00/concept.md ## Original Styles ### {entry['type']} ({entry['style_chars']} characters, sha256 {entry['style_sha256']}); "
            f"EXCLUDE = {len(entry['exclude'])} items from the same entry" + ("" if entry["exclude"] else " (none, blank)")
            + f"; values from .ai/plans/2026-11-02-2300-final-styles.json order {n}"
        )
        new_header = [
            f"Track: {title}",
            f"Order: {n}",
            f"Status: {STATUS}",
            f"Draft Scope: {old_vals['Draft Scope']}",
            f"Genre: {cfg['genre']}",
            f"BPM: {entry['bpm_header']}",
            f"Key: {entry['key_header']}",
            f"Vocal: {entry['vocal_header']}",
            f"Target Duration: {old_vals['Target Duration']}",
            f"Meter: {old_vals['Meter']}",
            f"Section Bars: {section_bars}",
            f"Style/Exclude Status: {status_line}",
            f"Style Type: {entry['type']}",
            "Style Source: user-supplied original style",
            f"Suno Params: {json.dumps(entry['suno_params'], ensure_ascii=False)}",
        ]
        assert old_vals["Style Type"] == entry["type"]
        meta_block = ""
        if "=== META ===" in txt:
            assert cfg["meta"], f"{n} has META but no new META text"
            meta_block = "=== META ===\n" + cfg["meta"] + "\n"
        else:
            assert cfg["meta"] is None
        assert txt_post == "" or txt_post.startswith("=== META ===")
        new_txt = (
            "\n".join(new_header) + "\n\n"
            "=== STYLE ===\n" + entry["style"] + "\n\n"
            "=== EXCLUDE ===\n" + exclude_line + "\n\n"
            + txt_ly.rstrip("\n") + "\n"
            + ("\n" + meta_block if meta_block else "")
        )

        # ---------- record ----------
        new_rec = rec_pre + rec_dr + rec_post
        new_rec = replace_line(new_rec, "- Previous versions (", previous_version_bullet(
            next(l for l in new_rec.split("\n") if l.startswith("- Previous versions (")), n, title, pres))
        new_rec = replace_line(new_rec, "- STYLE: ", style_bullets(n, entry, cfg))
        for prefix, new_line in cfg["rec_lines"].items():
            new_rec = replace_line(new_rec, prefix, new_line)
        for old, new, count in cfg["rec_phrases"]:
            new_rec = replace_exact(new_rec, old, new, count)
        draft_body = _extract_section(new_rec, "Draft")
        draft_sha = sha_text(draft_body)
        new_rec = re.sub(r"(?m)^- Source SHA256: [0-9a-f]{64}$", f"- Source SHA256: {draft_sha}", new_rec)
        assert new_rec.count(f"- Source SHA256: {draft_sha}") == 1

        # the txt LYRICS body and the record Draft must be the same text (gate: full_song_track_source_matches_draft)
        lyrics_body = txt_ly.split("=== LYRICS ===", 1)[1].strip()
        assert lyrics_body == draft_body.strip(), f"track {n}: txt LYRICS differs from record Draft"

        txt_path.write_text(new_txt, encoding="utf-8")
        rec_path.write_text(new_rec, encoding="utf-8")
        summary[n] = {
            "title": title,
            "lyric_fix_rows": sum(c for _, _, c in cfg["lyric_fixes"]),
            "lyric_fix_entries": len(cfg["lyric_fixes"]),
            "draft_sha256": draft_sha,
            "txt_sha256_new": sha_file(txt_path),
            "record_sha256_new": sha_file(rec_path),
        }
    OUT.write_text(json.dumps({"result": "APPLIED", "tracks": summary}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


main()
