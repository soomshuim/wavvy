#!/usr/bin/env python3
"""Write the `## Original Styles` section of SERIES/23-00/concept.md from final-styles.json.

The STYLE blocks and EXCLUDE lines are generated from the json (not re-typed). The section is
inserted before `## New Song Style Assembly`, or replaced in place if it already exists.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINAL = ROOT / ".ai/plans/2026-11-02-2300-final-styles.json"
CONCEPT = ROOT / "SERIES/23-00/concept.md"

TYPE_ORDER = ["먼지", "마음 밖", "작은 빛", "산책", "물결", "물안개", "골목", "이름"]

MEMO = {
    "먼지": [
        "원곡 절 안에서 STYLE 속 `Exclude Style:` 줄(8개)과 별도 Exclude Style 블록(10개, `Cold`·`Dark` 추가)이 다르다. 젠 지시(제외 항목은 EXCLUDE 칸)에 따라 별도 블록 10개를 최종 EXCLUDE로 쓰고, STYLE 속 8개는 모두 그 안에 있어 추가되는 항목이 없다.",
    ],
    "마음 밖": [
        "STYLE의 BPM이 범위(`96–106 BPM`, 발매 파일명은 90)이고 Key에 Major/Minor가 없다(`key color like A♭`). 원문 그대로 두었고 머리말은 원문 표현을 쓴다(검사 도구는 이런 표기를 STYLE과 대조하지 않고 머리말이 비어 있는지만 본다).",
    ],
    "작은 빛": [
        "22-00 Track Map은 `작은 빛`, 상세 제목줄은 `작은 손 (Tiny Hand)`이다. 발매 파일명(`SERIES/RNB-BEST/concept.md:272`)이 `작은 빛`이라 같은 곡으로 본다. 22-00의 시리즈 공통 Exclude Template(84–92행)은 이 곡 절에 없어 EXCLUDE는 비어 있다.",
    ],
    "산책": [
        "최종 STYLE이 900자를 넘는다(앞붙임만으로도 959자). 원곡 스타일 모드가 허용하는 값이며 `Alt` 삭제와 무관하다.",
    ],
    "물결": [
        "23:00 시리즈에서 덧붙였던 `Modern Indie R&B, Lo-fi Remastered, Articulation`은 쓰지 않는다(젠 「23:00버전이 아닌 원곡 스타일」). EXCLUDE 13개는 위 `## Type Styles` 물결 항목의 EXCLUDE와 항목·순서가 같다.",
    ],
    "물안개": [
        "소제목은 `Style Prompt (제로 베이스라인 v2)`. STYLE이 소문자 `articulation,`로 시작하는 것도 원문이다.",
    ],
    "골목": [],
    "이름": [
        "Track 18 벚꽃과 Track 19 그네가 이 한 항목을 쓴다(STYLE·EXCLUDE 같음).",
    ],
}


def edit_line(e: dict) -> str:
    kind = e["kind"]
    if kind == "prepend_lofi_remix":
        return "맨 앞에 `Lo-fi Remix, ` 를 더했다."
    if kind == "remove_genre_word":
        return f"`{e['old']}` → `{e['new']}` (`{e['removed_word']}` 삭제, 그 밖은 그대로)."
    if kind == "move_inline_exclude_line_to_EXCLUDE":
        added = e["items_added_to_EXCLUDE"]
        dup = e["duplicates_dropped"]
        tail = (
            f"별도 EXCLUDE 블록에 이미 있어 추가된 항목은 없다(겹친 {len(dup)}개 기록)."
            if not added else f"{len(added)}개 항목을 EXCLUDE로 옮겼다."
        )
        return f"STYLE 끝의 `{e['removed_line']}` 줄과 그 앞 빈 줄을 STYLE에서 뺐다. {tail}"
    if kind == "remove_lyric_bound_line":
        why = {
            "E-bridge3": "새 곡 가사 틀(이름)에는 `[Bridge]`가 하나뿐이라 세 번째 브리지가 없다",
            "E-last-gwaenchana": "새 곡 가사에 그 낱말·그 음이 없고 줄의 두 구절이 모두 그 낱말에 기대고 있다",
        }[e["id"]]
        return f"`{e['removed_line']}` 줄 삭제 — {why}."
    raise AssertionError(kind)


def source_line(e: dict) -> str:
    s = e["source"]
    span = s["style_lines"].replace("-", "–")
    parts = [f"`{s['path']}` `{s['heading']}` — STYLE 본문 {span}행"]
    if s["exclude_lines"] and s["exclude_origin"] == "separate Exclude Style block":
        parts.append(f"별도 Exclude Style 블록 {s['exclude_lines'].split('-')[0]}행")
    elif s["exclude_origin"] == "separate Exclude Style block says (없음)":
        parts.append(f"별도 Exclude Style 블록({s['exclude_lines'].split('-')[0]}행)은 `(없음)`")
    return " · ".join(parts) + f" (원곡 STYLE {e['original_style_chars']}자, sha256 `{e['original_style_sha256']}`)"


def suno_line(e: dict) -> str:
    p = e["suno_params"]
    if p["weirdness"] == "default":
        return f"기본값 `default` (원곡에 숫자 기록 없음 — {p['source'].removeprefix('원곡에 숫자 기록 없음: ')})"
    return f"Weirdness {p['weirdness']} · Style Influence {p['style_influence']} (`{p['source']}`)"


def build_section(final: dict) -> str:
    by_type: dict[str, list[dict]] = {}
    for e in final["entries"]:
        by_type.setdefault(e["type"], []).append(e)
    assert list(by_type) == TYPE_ORDER, list(by_type)

    out: list[str] = []
    out.append("## Original Styles")
    out.append("")
    out.append(
        "2026-11-02: 재생성 9곡(Track 11–19)의 STYLE은 새로 조립한 23:00 버전(`## New Song Style Assembly`)이 아니라 "
        "**젠의 원곡 Suno 스타일 프롬프트**다. 젠: 「공통 스타일은 Lo-fi Remix만 쓰고 23:00버전이 아닌 원곡 스타일에 Lo-fi Remix만 남기자 "
        "얼터너티브나 모던 알앤비는 제외」, 템포는 「원곡 BPM 그대로」, 여름밤·벚꽃·그네의 보컬은 「원곡대로 남성」."
    )
    out.append("")
    out.append("규칙 (모든 곡 공통):")
    out.append("")
    out.append("1. 최종 STYLE = `Lo-fi Remix, ` + 원곡 STYLE 원문(줄바꿈 그대로). 근거: 젠 「Lo-fi remix는 붙여야해 안전빵이야」.")
    out.append(
        "2. 원문에서 바꾸는 것은 세 가지뿐이고 항목마다 아래에 적는다. (a) 장르 낱말 alternative/Alt/Modern R&B 삭제. "
        "(b) STYLE 안에 있던 제외 줄(`Exclude Style:`/`EXCLUDE:`)을 EXCLUDE 칸으로 옮김 — 젠 「- 붙은 스타일은 exclude인거 알지?」. "
        "(c) 새 곡 가사에서 뜻이 없는 원곡 가사 전용 지시만 최소 삭제 — 젠 「그대로 활용 원칙이 유도리가 있어야지. 원곡이 없는데 넣는게 뭔 소용이야」."
    )
    out.append("3. BPM 숫자·Key·성별 낱말·나머지 문구는 원곡 그대로다. 곡의 보컬 성별도 원곡을 따른다(여름밤·벚꽃·그네 = 남성).")
    out.append("4. 최종 EXCLUDE = 원곡 EXCLUDE + (b)에서 옮긴 항목(순서 유지, 겹치는 항목은 한 번만).")
    out.append("5. Suno 파라미터는 원곡 concept에 숫자가 기록된 곡만 그 값(먼지 W20/I80, 산책 W25/I75, 물결 W20/I80), 나머지는 `default`다.")
    out.append("")
    out.append(
        "검사 방식: txt 머리말에 `Style Type: <타입>`과 `Style Source: user-supplied original style`이 있고, txt STYLE이 이 절 해당 `###` 항목의 "
        "첫 `text` 코드 블록과 줄바꿈까지 글자 그대로 같고, txt EXCLUDE가 그 항목의 `- EXCLUDE:` 줄과 항목·순서까지 같을 때만 "
        "`gate --stage track-prompt`가 900자·EXCLUDE 8개 예산을 막지 않는다(`MASTER/style/STYLE.md` §3). "
        "이 절에서는 `###` 제목을 타입 이름과 같게, 항목마다 EXCLUDE 줄을 한 줄만 둔다. 같은 타입을 쓰는 곡은 한 항목을 함께 쓴다."
    )
    out.append("")
    out.append(
        "기계 판독본은 `.ai/plans/2026-11-02-2300-final-styles.json`(곡별 `style`·`exclude`·`edits[]`)이고 이 절의 STYLE 블록과 바이트 단위로 같다 "
        "(대조: `.ai/validation/2026-11-02-2300-styles/a2-check.json`). 원곡 조사 원본: `.ai/plans/2026-11-02-2300-original-styles.json`·`.md`."
    )
    out.append("")

    for t in TYPE_ORDER:
        rows = by_type[t]
        first = rows[0]
        for r in rows[1:]:
            for k in ("style", "exclude", "suno_params", "bpm_header", "key_header", "vocal_header", "source"):
                assert r[k] == first[k], (t, k)
        songs = " · ".join(f"Track {r['order']} {r['title']}" for r in rows)
        out.append(f"### {t}")
        out.append("")
        out.append(f"- 쓰이는 곡: {songs} (txt 머리말 `Style Type: {t}`)")
        out.append(f"- 출처: {source_line(first)}")
        out.append(
            f"- 머리말 값: BPM `{first['bpm_header']}` · Key `{first['key_header']}` · Vocal `{first['vocal_header']}` "
            "(STYLE에서 읽을 수 있으면 그 값, 아니면 원문 표현)"
        )
        out.append(f"- Suno 파라미터: {suno_line(first)}")
        out.append("- 편집 (원곡 STYLE → 최종 STYLE, 이것이 전부):")
        for n, e in enumerate(first["edits"], 1):
            out.append(f"  {n}. {edit_line(e)}")
        for m in MEMO[t]:
            out.append(f"- 메모: {m}")
        out.append("- EXCLUDE: " + ", ".join(first["exclude"]) if first["exclude"] else "- EXCLUDE:")
        out.append("")
        out.append(f"**최종 STYLE** — {first['style_chars']}자, sha256 `{first['style_sha256']}`")
        out.append("")
        out.append("```text")
        out.append(first["style"])
        out.append("```")
        out.append("")
    return "\n".join(out)


def main() -> int:
    final = json.loads(FINAL.read_text(encoding="utf-8"))
    section = build_section(final)
    text = CONCEPT.read_text(encoding="utf-8")
    existing = re.search(r"^## Original Styles\s*$", text, re.MULTILINE)
    if existing:
        nxt = re.search(r"^## ", text[existing.end():], re.MULTILINE)
        end = existing.end() + nxt.start() if nxt else len(text)
        new = text[: existing.start()] + section + "\n" + text[end:]
        mode = "replaced"
    else:
        anchor = re.search(r"^## New Song Style Assembly\s*$", text, re.MULTILINE)
        assert anchor, "anchor `## New Song Style Assembly` not found"
        new = text[: anchor.start()] + section + "\n" + text[anchor.start():]
        mode = "inserted"
    CONCEPT.write_text(new, encoding="utf-8")
    print(f"{mode} ## Original Styles in {CONCEPT.relative_to(ROOT)} ({len(section.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
