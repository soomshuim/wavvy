#!/usr/bin/env python3
"""Build SERIES/23-00 foundation files from the read-only workspace observation.

Run from the repo root:  python3 .ai/validation/2026-11-01-2300-foundation/build-foundation.py
Writes: SERIES/23-00/concept.md, SERIES/23-00/input/tracks/01..09 txt,
        .ai/validation/2026-11-01-2300-foundation/02-type-styles-facts.json
Reads only: .ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from wavvy_harness.gate import KEY_MODE_RE, STYLE_BPM_RE, _key_mode, _vocal_genders  # noqa: E402

RESEARCH = REPO / ".ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json"
SERIES = REPO / "SERIES/23-00"
VALIDATION = REPO / ".ai/validation/2026-11-01-2300-foundation"

WORKSPACE_ID = "f578d3c2-f43f-462e-8e05-44d022edd480"
ORDER = ["먼지", "산책", "숨", "이름", "마음 밖", "물안개", "골목", "물결", "작은 빛"]
JEN_EDIT_BASIS = "젠 2026-11-01 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」"

# 새 곡용 STYLE 편집(젠 지시). 그 밖의 단어·순서는 바꾸지 않는다.
NEW_SONG_EDITS = {
    "골목": ("Keep the original song’s melodic contour and section flow, with intimate dry chest-voice Korean lead, no harmony layers",
             "Intimate dry chest-voice Korean lead, no harmony layers"),
    "산책": ("Lo-Fi Remix, ", "Lo-Fi, "),
    "마음 밖": ("lo-fi remix,", "lo-fi,"),
}

# 젠이 채팅에 붙여 준 물결 원본 스타일(터미널 줄바꿈만 빈칸 하나로 이은 것, ‑ 는 U+2011).
ZEN_MULGYEOL_ORIGINAL = (
    "Korean Indie Alt R&B, 74 BPM, A Major, Neo-soul chords (M9, m7), Clean Electric Guitar-led supportive groove, "
    "rim-click, warm texture, subtle vinyl crackle, Male vocal: Solid, Direct, Raw, Dry, Chest dominant, No falsetto, "
    "Straight tone, No vibrato, no ad-libs, Narrow range, stepwise melody, speech-like rhythm, High chest voice over "
    "falsetto, Nonchalant tone, never dramatic, Articulation: clear consonants, precise syllables, no slurring, "
    "Verse2 tension builds, Chorus hook-first, high-note focal: short chest note, straight, not sustained, Choruses "
    "grow by density only, Bridge sparse, Outro guitar fades, Single lead vocal, ‑Falsetto, ‑Airy, ‑Whisper, "
    "‑Breathiness, ‑Growl, ‑Vibrato, ‑Opera, ‑Dramatic, ‑Harmonized, ‑Backing vocals, ‑Choir, ‑Intense, ‑Mumbled"
)
MULGYEOL_ADDED = "Modern Indie R&B, Lo-fi Remastered, Articulation"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    data = json.loads(RESEARCH.read_text(encoding="utf-8"))
    by_name = {track["matched_name"]: track for track in data["tracks"]}
    assert list(by_name) == ORDER or set(by_name) == set(ORDER), "unexpected track set"

    # ---- 물결 type style (젠 원본 + 3 words), EXCLUDE 13 ----
    marker = ", ‑Falsetto"
    front, tail = ZEN_MULGYEOL_ORIGINAL.split(marker, 1)
    neg_items = ["‑Falsetto" if i == 0 else item for i, item in enumerate((marker + tail)[2:].split(", "))]
    assert neg_items == by_name["물결"]["inline_negative_terms"], "typed negatives differ from observed U+2011 items"
    assert front.isascii()
    mulgyeol_style = f"{front}, {MULGYEOL_ADDED}"
    mulgyeol_exclude = [item[1:] for item in neg_items]  # drop U+2011
    assert all(item and item[0] != "‑" for item in mulgyeol_exclude) and len(mulgyeol_exclude) == 13

    types: dict[str, dict] = {}
    for name in ORDER:
        track = by_name[name]
        if name == "물결":
            original = mulgyeol_style
            new_song = mulgyeol_style
            edit = None
            exclude: list[str] = mulgyeol_exclude
        else:
            original = track["style_full"]
            exclude = []
            edit = NEW_SONG_EDITS.get(name)
            if edit:
                assert original.count(edit[0]) == 1, f"edit phrase not unique in {name}"
                new_song = original.replace(edit[0], edit[1])
            else:
                new_song = original
        bpms = sorted({int(m.group(1)) for m in STYLE_BPM_RE.finditer(new_song)})
        keys = sorted({m.group() for m in KEY_MODE_RE.finditer(new_song)})  # literal wording, e.g. "Eb Major"
        assert len({_key_mode(key) for key in keys}) == len(keys), name
        genders = sorted(_vocal_genders(new_song))
        types[name] = {
            "id": track["id"], "url": track["url"], "lineage": track.get("lineage") or {},
            "original": original, "new_song": new_song, "edit": edit, "exclude": exclude,
            "bpms": bpms, "keys": keys, "genders": genders,
        }

    # ---- per-type markdown ----
    def append_note(info: dict) -> str:
        missing = []
        if not info["bpms"]:
            missing.append("`NN BPM`")
        if not info["keys"]:
            missing.append("`X Major|Minor`")
        if not info["genders"]:
            missing.append("`male|female vocal`")
        return ", ".join(missing) if missing else "없음 (BPM·조성·성별이 모두 STYLE에 있음)"

    def written(info: dict) -> str:
        bpm = ", ".join(str(b) for b in info["bpms"]) or "없음"
        key = ", ".join(info["keys"]) or "없음"
        gender = ", ".join(info["genders"]) or "없음"
        return f"BPM {bpm} · 조성 {key} · 성별 {gender}"

    sections = []
    for name in ORDER:
        info = types[name]
        lin = info["lineage"]
        if lin.get("source_id"):
            origin = f"{lin['relation_ui']} \"{lin['source_title_ui']}\" (`{lin['source_id']}`) — {lin['source_url']}"
        else:
            origin = "화면에 Remix of / Cover of 표시 없음 (원곡이 없다는 증거는 아님)"
        lines = [
            f"### {name}",
            "",
            f"- Suno ID (작업공간 Lo-Fi Remix): `{info['id']}` — {info['url']}",
            f"- 화면에 표시된 원곡: {origin}",
        ]
        if name == "물결":
            lines.append(f"- 출처: 젠이 채팅에 붙여 준 원본 스타일에서 `‑` 항목 13개를 뺀 앞부분 + `, {MULGYEOL_ADDED}` (젠 지시). 작업공간 표시 스타일({len(by_name['물결']['style_full'])}자: `{MULGYEOL_ADDED}` + `‑` 항목 13개)과 다르다.")
        else:
            lines.append(f"- 출처: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json` → `{name}`의 `style_full` (작업공간 화면 원문, 2026-11-01 관측)")
        lines += [
            f"- 원문에 적힌 BPM·조성·성별: {written(info)}",
            "- EXCLUDE:" + (" " + ", ".join(info["exclude"]) if info["exclude"] else ""),
            f"- 새 곡 STYLE 끝에 덧붙일 항목(젠 「선례처럼 끝에 덧붙이기」, 없는 것만): {append_note(info)}",
        ]
        if name == "골목":
            lines.append("- 메모: 원문 STYLE에 `Keep the original song’s melodic contour and section flow`가 있다. 원문(a)은 그대로 두고, 새 곡용(b)에서만 뺀다.")
        if name == "작은 빛":
            lines.append("- 메모: STYLE에 male/female 단어가 없다. 성별 쪽 표현은 `Single warm baritone lead`뿐이다.")
        if name == "물결":
            lines.append("- 메모: 새 곡 중 이 타입을 쓰는 txt는 머리말에 `Style Type: 물결`과 `Exclude Source: user-supplied type style`을 적는다. `gate --stage track-prompt`는 이때만 EXCLUDE 8개 초과를 통과시키며, 위 `- EXCLUDE:` 줄과 항목·순서가 정확히 같아야 한다 (`MASTER/style/STYLE.md` §3).")
        lines += ["", f"**(a) 원문 STYLE** — {len(info['original'])}자, sha256 `{sha(info['original'])}`", "", "```text", info["original"], "```", ""]
        if info["edit"]:
            lines.append(f"**(b) 새 곡용 STYLE** — {len(info['new_song'])}자, sha256 `{sha(info['new_song'])}`")
            lines.append("")
            lines.append(f"편집: `{info['edit'][0]}` → `{info['edit'][1]}`. 다른 단어·순서는 바꾸지 않았다. 근거: {JEN_EDIT_BASIS}.")
        elif name == "물결":
            lines.append(f"**(b) 새 곡용 STYLE** — {len(info['new_song'])}자, sha256 `{sha(info['new_song'])}`")
            lines.append("")
            lines.append("편집 없음. 젠이 직접 붙이라고 한 `Lo-fi Remastered`와 나머지 3단어는 그대로 둔다 (원문 (a)와 같다).")
        else:
            lines.append(f"**(b) 새 곡용 STYLE** — {len(info['new_song'])}자, sha256 `{sha(info['new_song'])}`")
            lines.append("")
            lines.append("편집 없음 (원문 (a)와 같다).")
        lines += ["", "```text", info["new_song"], "```", ""]
        sections.append("\n".join(lines))
    type_styles_body = "\n".join(sections)

    # ---- Track Map ----
    rows = []
    for index, name in enumerate(ORDER, start=1):
        info = types[name]
        txt = f"{index:02d}_{name} (Lo-Fi Remix).txt"
        rows.append(f"| {index:02d} | {name} (Lo-Fi Remix) | 젠 기존 곡의 lo-fi 리믹스 | `{info['id']}` | {name} | `input/tracks/{txt}` |")
    for index in range(10, 21):
        rows.append(f"| {index:02d} | — | 새 곡 — 설계표 젠 확인 대기 | — | 미정 | — |")
    track_map = "\n".join(rows)

    concept = f"""# 23:00 Relax Alternative R&B / Lo-fi R&B

Version: 0.1
Last Updated: 2026-11-01

## Series Status

- **Status**: Foundation only. The concept, the nine existing Lo-Fi Remix source records, and the type-style table are recorded. No new-song design table, new-song lyric, new-song Suno generation, audio file, artwork, or upload exists yet.
- **Time Slot**: 23:00.
- **Genre Lanes**: relax alternative R&B, lo-fi R&B.
- **Track Count**: 20 songs: nine existing Lo-Fi Remixes made by 젠 from earlier songs and 11 new songs.
- **Numbering**: temporary. 젠: 「넘버링은 나중에 일괄로 할게」. The Track Map numbers and txt file numbers change when 젠 numbers all 20 songs at once.
- **Suno workspace**: `[23:00]` (`{WORKSPACE_ID}`) — https://suno.com/create?wid={WORKSPACE_ID}
- **Waiting for 젠**: the 11-song design table (which type each new song uses, its Korean one-word title, and its lyric concept). Nothing for Tracks 10–20 is drafted.
- **Current artifacts**: this file, the nine remix source records in `input/tracks/`, and the read-only workspace observation in `.ai/research/2026-11-01-2300-nine-tracks/` (`nine-tracks.json`, `styles-verbatim.txt`, `raw/`).

## Confirmed Decisions (젠, 2026-11-01)

- **Song plan**: 20 songs = the nine existing lo-fi remixes + 11 new songs. 젠: 「url에서 9곡의 가사 컨셉과 특징, 스타일 프롬프트(그대로 활용)를 각 타입 별로 참고해서 나머지 11곡을 새로 만들어야해.」 The nine styles all differ, so each remix is one type (nine types, see `## Type Styles`).
- **물결 type**: 젠: 「물결만 원본 트랙의 스타일 프롬프트 + Modern Indie R&B, Lo-fi Remastered, Articulation 를 붙여줘.」 and 「- 붙은 스타일은 exclude인거 알지?」 The `‑` items of the supplied original are therefore EXCLUDE, not STYLE.
- **Thirteen EXCLUDE items**: asked whether to keep all 13 despite the 8-item budget, 젠 chose 「13개 모두 유지 (추천)」. The track-prompt gate records this as a source-bound exception (`## Series Overrides`).
- **Missing tempo, key, vocal gender**: 젠 chose 「선례처럼 끝에 덧붙이기」. A new song's STYLE is its type's new-song STYLE (b) plus, only for the items the type text lacks, `, NN BPM, X Major|Minor, male|female vocal` at the end. Precedent: `.ai/lyrics/2026-10-02_17-00_12_서점-full-draft.md` Source Map.
- **Reuse with judgment**: 젠: 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」 — words that only make sense for a remix are removed from the new-song STYLE (b). The original text (a) is kept verbatim beside it. Edits are listed per type.
- **Reference**: the nine existing remixes in the workspace are the reference. No external reference song was supplied.
- **Language**: Korean lyrics.
- **Lyric direction for new songs**: warm longing — more faint and warm than sad, a relaxing comfort drawn from old memories, concrete mood and sensory detail. Titles are one Korean word (noun, adjective, or adverb).
- **Browser**: ego lite through the `ego-browser` CLI (`MASTER/ai/RUNTIME_RULES.md` Browser Connection).

## Series Overrides

- **EXCLUDE budget (type-scoped)**: `MASTER/style/STYLE.md` §3 caps EXCLUDE at 8 items. The 물결 type keeps the 13 items 젠 supplied. A new-song txt may exceed 8 only with the header lines `Style Type: 물결` and `Exclude Source: user-supplied type style`, and only when its EXCLUDE matches the 물결 `- EXCLUDE:` line below in items and order. Every other type has an empty EXCLUDE and stays within the budget.
- **Vocal and language defaults**: no override of the channel defaults in `wavvy.md` is declared. If a type style conflicts with a channel default when a new song is designed, record a track-scoped exception at that time.
- **Remix source records**: `input/tracks/01`–`09` keep the workspace display text unedited, including wording that only makes sense for a remix. They are records of existing songs; the new-song edits in `## Type Styles` do not apply to them, and the new-prompt gate is not applied retroactively to them (`MASTER/WORKFLOWS.md` §1).

## Type Styles

Each type has two STYLE entries. **(a) 원문 STYLE** is the workspace display text exactly as observed (for 물결, 젠's original plus the three words he specified). **(b) 새 곡용 STYLE** is what a new song of that type starts from; only the edits listed under it were made. Character counts are Unicode characters including spaces. The `- EXCLUDE:` line is read by the track-prompt gate: keep exactly one per type and keep the heading text equal to the type name.

Values are display text from 2026-11-01, not proof of the exact generation input. The workspace did not show an Exclude field for any song.

{type_styles_body}
## Track Map (numbers are temporary)

| # | Title | Role | Suno ID | Type | Source text |
|---|---|---|---|---|---|
{track_map}

Order of Tracks 01–09 follows the workspace list order given for this series. 10–20 are placeholders only.

## Source Records

- Observation: `.ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json`, `styles-verbatim.txt`, and `raw/` (ego lite, read-only; no playback, generation, edit, or download). Treat these as read-only evidence.
- Displayed styles and lyrics are not proof of the exact generation input. Durations differ by one second between the list and the play bar for some songs, so none is recorded here. Audio was not measured.
- Only 물결 showed Weirdness 20% and Style Influence 80% (it is a Cover). The other eight did not display those fields, which does not prove they are unset.

## Upload Status

- YouTube upload: not uploaded yet
"""
    SERIES.mkdir(parents=True, exist_ok=True)
    (SERIES / "concept.md").write_text(concept, encoding="utf-8")

    # ---- nine remix source txt ----
    tracks_dir = SERIES / "input" / "tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(ORDER, start=1):
        track = by_name[name]
        style_full, lyrics_full = track["style_full"], track["lyrics_full"]
        bpms = sorted({int(m.group(1)) for m in STYLE_BPM_RE.finditer(style_full)})
        keys = sorted({_key_mode(m.group()) for m in KEY_MODE_RE.finditer(style_full)})
        genders = sorted(_vocal_genders(style_full))
        assert len(bpms) <= 1 and len(keys) <= 1 and len(genders) <= 1, name
        bpm = f"{bpms[0]} (prompt wording; not measured)" if bpms else "unknown"
        key_value = next((m.group() for m in KEY_MODE_RE.finditer(style_full)), "")
        key = f"{key_value} (prompt wording; not measured)" if key_value else "unknown"
        lyric_genders = sorted(_vocal_genders(lyrics_full))  # section tags such as [Direct male vocal, ...]
        if genders:
            vocal = f"{genders[0]} (prompt wording; not measured)"
        elif len(lyric_genders) == 1:
            vocal = f"{lyric_genders[0]} (lyrics tag wording; STYLE has no male/female word; not measured)"
        else:
            vocal = "unknown"
        lin = track.get("lineage") or {}
        lineage = (f"Workspace page showed: {lin['relation_ui']} \"{lin['source_title_ui']}\" ({lin['source_id']})."
                   if lin.get("source_id") else
                   "Workspace page showed no Remix of / Cover of block (not proof that no source exists).")
        meta = [
            "User-provided lo-fi remix of an earlier song, observed in the Suno workspace [23:00] on 2026-11-01 (read-only, ego lite).",
            "STYLE and LYRICS are the workspace display text, unedited. The Exclude field was not displayed. Displayed text is not proof of the exact generation input. Model shown: V6. Audio not measured.",
            lineage,
            "The file number is temporary; 젠 numbers all 20 songs later.",
            f"Evidence: .ai/research/2026-11-01-2300-nine-tracks/nine-tracks.json (track {name}).",
        ]
        if name == "물결":
            meta.append("This record keeps the 185-character display STYLE. The 물결 type style in concept.md ## Type Styles is 젠's supplied original plus Modern Indie R&B, Lo-fi Remastered, Articulation, and its 13 `‑` items are that type's EXCLUDE.")
        status = (f"user-provided lo-fi remix source; Suno ID {track['id']}; audio not measured; "
                  f"Suno URL {track['url']}")
        text = (
            f"Track: {name} (Lo-Fi Remix)\n"
            f"Order: {index:02d}\n"
            f"Status: {status}\n"
            f"BPM: {bpm}\n"
            f"Key: {key}\n"
            f"Vocal: {vocal}\n"
            "\n=== STYLE ===\n"
            f"{style_full}\n"
            "\n=== EXCLUDE ===\n"
            "\n=== LYRICS ===\n"
            f"{lyrics_full.rstrip(chr(10))}\n"
            "\n=== META ===\n"
            + "\n".join(meta) + "\n"
        )
        (tracks_dir / f"{index:02d}_{name} (Lo-Fi Remix).txt").write_text(text, encoding="utf-8")

    facts = {
        name: {
            "id": info["id"],
            "original_chars": len(info["original"]), "original_sha256": sha(info["original"]),
            "new_song_chars": len(info["new_song"]), "new_song_sha256": sha(info["new_song"]),
            "edit": info["edit"], "exclude": info["exclude"],
            "bpms": info["bpms"], "keys": info["keys"], "genders": info["genders"],
        }
        for name, info in types.items()
    }
    (VALIDATION / "02-type-styles-facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("built", SERIES / "concept.md", "and", len(ORDER), "txt files")


if __name__ == "__main__":
    main()
