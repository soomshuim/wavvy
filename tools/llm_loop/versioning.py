"""Versioning and output paths for llm_loop M1."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import click


TRACK_KINDS = ("lyrics", "style", "exclude", "qc")


@dataclass(frozen=True)
class ArtifactPaths:
    version: int
    lyrics: Path
    style: Path
    exclude: Path
    qc: Path


def _next_version(series_dir: Path, track: int) -> int:
    """
    Find next version considering both plain and _llm files.
    Example:
      track07_lyrics_v2.txt + track07_lyrics_v3_llm.txt -> next is v4
    """
    prefix = f"track{track:02d}_"
    version_re = re.compile(rf"^track{track:02d}_(lyrics|style|exclude|qc)_v(\d+)(?:_llm)?\.(?:txt|md)$")
    max_version = 0
    for path in series_dir.glob(f"{prefix}*"):
        match = version_re.match(path.name)
        if match:
            max_version = max(max_version, int(match.group(2)))
    return max_version + 1


def build_artifact_paths(series_dir: Path, track: int) -> ArtifactPaths:
    version = _next_version(series_dir, track)
    return ArtifactPaths(
        version=version,
        lyrics=series_dir / f"track{track:02d}_lyrics_v{version}_llm.txt",
        style=series_dir / f"track{track:02d}_style_v{version}_llm.txt",
        exclude=series_dir / f"track{track:02d}_exclude_v{version}_llm.txt",
        qc=series_dir / f"track{track:02d}_qc_v{version}_llm.md",
    )


def ensure_no_overwrite(paths: ArtifactPaths) -> None:
    for path in (paths.lyrics, paths.style, paths.exclude, paths.qc):
        if path.exists():
            raise click.ClickException(f"Refusing overwrite: {path}")

