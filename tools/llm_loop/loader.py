"""Context loader for llm_loop."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from llm_loop.config import RunConfig


@dataclass(frozen=True)
class SeriesContext:
    series_dir: Path
    concept_path: Path
    has_concept: bool
    concept_excerpt: str
    track_section: str
    rules_excerpt: dict[str, str]


def load_series_context(cfg: RunConfig) -> SeriesContext:
    series_dir = cfg.project_root / "SERIES" / cfg.series
    concept_path = series_dir / "concept.md"
    concept_text = concept_path.read_text(encoding="utf-8") if concept_path.exists() else ""
    track_section = _extract_track_section(concept_text, cfg.track)
    return SeriesContext(
        series_dir=series_dir,
        concept_path=concept_path,
        has_concept=concept_path.exists(),
        concept_excerpt=concept_text[:6000],
        track_section=track_section[:3000],
        rules_excerpt=_load_rules_excerpt(cfg.project_root),
    )


def _extract_track_section(concept_text: str, track: int) -> str:
    if not concept_text:
        return ""
    marker = rf"###\s*Track\s*{track:02d}\b"
    match = re.search(marker, concept_text)
    if not match:
        return ""
    start = match.start()
    tail = concept_text[start:]
    next_match = re.search(r"\n###\s*Track\s*\d{2}\b", tail[1:])
    end = start + 1 + next_match.start() if next_match else len(concept_text)
    return concept_text[start:end].strip()


def _load_rules_excerpt(project_root: Path) -> dict[str, str]:
    master = project_root / "MASTER"
    files = {
        "roles": master / "ROLES.md",
        "manager": master / "MANAGER.md",
        "lyrics": master / "LYRICS.md",
        "style": master / "STYLE.md",
    }
    out: dict[str, str] = {}
    for key, path in files.items():
        if path.exists():
            out[key] = path.read_text(encoding="utf-8")[:5000]
        else:
            out[key] = ""
    return out
