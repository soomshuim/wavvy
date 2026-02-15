"""Hard rule checks for llm_loop."""

from __future__ import annotations

from dataclasses import dataclass
import re

from llm_loop.config import RunConfig


@dataclass(frozen=True)
class HardRuleRow:
    rule: str
    status: str
    notes: str


@dataclass(frozen=True)
class HardRuleResult:
    rows: list[HardRuleRow]

    @property
    def passed(self) -> bool:
        return all(row.status == "PASS" for row in self.rows)

    @property
    def fail_items(self) -> list[str]:
        return [f"{row.rule}: {row.notes}" for row in self.rows if row.status != "PASS"]


def run_hard_rules(cfg: RunConfig, lyrics: str, style: str, exclude: str) -> HardRuleResult:
    rows: list[HardRuleRow] = []

    style_len = len(style)
    rows.append(
        HardRuleRow(
            rule=f"Style length <= {cfg.style_char_limit}",
            status="PASS" if style_len <= cfg.style_char_limit else "FAIL",
            notes=f"len={style_len}",
        )
    )

    has_structure = bool(re.search(r"\[(verse1|chorus)\]", lyrics, flags=re.IGNORECASE))
    rows.append(
        HardRuleRow(
            rule="Lyrics has core structure tags",
            status="PASS" if has_structure else "FAIL",
            notes="requires [verse1] and/or [chorus]",
        )
    )

    chorus_count = len(re.findall(r"\[chorus\]", lyrics, flags=re.IGNORECASE))
    rows.append(
        HardRuleRow(
            rule="Lyrics has repeated chorus section",
            status="PASS" if chorus_count >= 2 else "FAIL",
            notes=f"chorus_count={chorus_count}",
        )
    )

    forbidden = _find_forbidden_in_lyrics(lyrics)
    rows.append(
        HardRuleRow(
            rule="Lyrics pure-input (no arrangement directives)",
            status="PASS" if not forbidden else "FAIL",
            notes="none" if not forbidden else ", ".join(forbidden),
        )
    )

    has_korean = bool(re.search(r"[가-힣]", lyrics))
    rows.append(
        HardRuleRow(
            rule="Lyrics contains Korean characters",
            status="PASS" if has_korean else "FAIL",
            notes="requires at least one Hangul character",
        )
    )

    has_vocal_persona = bool(
        re.search(
            r"\b(male|female|mixed|baritone|alto|tenor|contralto|mezzo)\b",
            style,
            flags=re.IGNORECASE,
        )
    )
    rows.append(
        HardRuleRow(
            rule="Style includes vocal persona",
            status="PASS" if has_vocal_persona else "FAIL",
            notes="gender/tone/delivery marker required",
        )
    )

    has_raw_baseline = bool(
        re.search(r"\b(raw|direct|solid)\b", style, flags=re.IGNORECASE)
    )
    rows.append(
        HardRuleRow(
            rule="Style includes vocal baseline marker",
            status="PASS" if has_raw_baseline else "FAIL",
            notes="expected one of raw/direct/solid",
        )
    )

    exclude_items = [part.strip() for part in exclude.split(",") if part.strip()]
    rows.append(
        HardRuleRow(
            rule="Exclude list size <= 8",
            status="PASS" if 0 < len(exclude_items) <= 8 else "FAIL",
            notes=f"items={len(exclude_items)}",
        )
    )

    mandatory_exclude_hits = _count_mandatory_exclude_terms(exclude)
    rows.append(
        HardRuleRow(
            rule="Exclude includes mandatory harmony guards",
            status="PASS" if mandatory_exclude_hits >= 2 else "FAIL",
            notes=f"mandatory_hits={mandatory_exclude_hits} (need >=2)",
        )
    )

    return HardRuleResult(rows=rows)


def _find_forbidden_in_lyrics(lyrics: str) -> list[str]:
    forbidden_patterns = [
        "kick",
        "snare",
        "808",
        "compressor",
        "eq",
        "reverb",
        "arrangement",
        "mixing",
        "mastering",
    ]
    lower = lyrics.lower()
    return [p for p in forbidden_patterns if p in lower]


def _count_mandatory_exclude_terms(exclude: str) -> int:
    lower = exclude.lower()
    terms = ["backing vocals", "choir", "doubled vocals", "harmonized", "falsetto"]
    return sum(1 for term in terms if term in lower)
