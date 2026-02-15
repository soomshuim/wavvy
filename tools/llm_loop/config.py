"""Config contract for llm_loop M1."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import click


@dataclass(frozen=True)
class RunConfig:
    project_root: Path
    series: str
    track: int
    provider: str
    model: str
    max_iterations: int
    cross_series_mode: str
    dry_run: bool
    temperature: float
    seed: str
    output_dir: Path
    verbose: bool
    prompt_dir: Path
    style_char_limit: int = 900
    openai_api_key: str = ""


def validate_config(cfg: RunConfig) -> None:
    if not cfg.series.strip():
        raise click.ClickException("--series is required.")
    if cfg.track < 1 or cfg.track > 99:
        raise click.ClickException("--track must be in range 1..99.")
    if cfg.max_iterations < 1 or cfg.max_iterations > 5:
        raise click.ClickException("--max-iterations must be in range 1..5.")
    if cfg.temperature < 0.0 or cfg.temperature > 1.0:
        raise click.ClickException("--temperature must be in range 0.0..1.0.")
    series_dir = cfg.project_root / "SERIES" / cfg.series
    if not series_dir.exists():
        raise click.ClickException(f"Series not found: {series_dir}")
    if cfg.output_dir.exists() and not cfg.output_dir.is_dir():
        raise click.ClickException(f"--output-dir must be a directory: {cfg.output_dir}")
    if not cfg.prompt_dir.exists():
        raise click.ClickException(f"Prompt dir not found: {cfg.prompt_dir}")


def resolve_openai_api_key() -> str:
    return os.getenv("OPENAI_API_KEY", "").strip()
