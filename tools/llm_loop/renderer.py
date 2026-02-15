"""Prompt renderer utilities."""

from __future__ import annotations

from pathlib import Path


def load_template(prompt_dir: Path, name: str) -> str:
    path = prompt_dir / name
    return path.read_text(encoding="utf-8")


def render_template(template: str, values: dict[str, object]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{key}}}", str(value))
    return rendered

