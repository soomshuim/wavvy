"""Cross-series context builder (M3 lite)."""

from __future__ import annotations

from pathlib import Path


def build_cross_series_context(project_root: Path, target_series: str, mode: str) -> str:
    if mode == "off":
        return ""

    series_root = project_root / "SERIES"
    snippets: list[str] = []
    for concept in series_root.glob("*/concept.md"):
        series_name = concept.parent.name
        if series_name == target_series:
            continue
        text = concept.read_text(encoding="utf-8")
        snippets.append(f"[{series_name}]\n{text[:800]}")
        if mode == "lite" and len(snippets) >= 3:
            break
    return "\n\n".join(snippets)

