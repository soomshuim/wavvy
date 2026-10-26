"""Separate the logo-only video scene from the typographic YouTube thumbnail."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps

MANIFEST = "input/video-artwork.json"
BACKGROUND_PATHS = {f"input/video-background.{ext}" for ext in ("png", "jpg", "jpeg")}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError(detail)


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"{path.name} must contain an object")
    return value


def _bound(series: Path, ref: dict) -> Path:
    value, digest = ref["path"], ref["sha256"]
    _require(isinstance(value, str) and not Path(value).is_absolute(), "artwork path must be series-relative")
    path = (series / value).resolve()
    _require(path.is_relative_to(series), "artwork path escapes series")
    _require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
             "artwork SHA-256 is invalid")
    _require(path.is_file() and file_sha256(path) == digest, f"artwork file/hash differs: {value}")
    return path


def check_video_artwork(series: Path, *, image_path: Path | None = None,
                        report: dict | None = None) -> tuple[dict, list[str]]:
    """Check actual 4K pixels and hash-bound visual observations before rendering.

    There is deliberately no legacy switch here. Historical uploaded inspection
    is handled by its caller; every new static render must pass this contract.
    """
    series = series.resolve()
    try:
        manifest_path = series / MANIFEST
        manifest = _json(manifest_path)
        _require(manifest.get("schema") == "wavvy.video_artwork.v1", "unsupported video artwork schema")
        background, thumbnail = manifest["video_background"], manifest["thumbnail"]
        _require(background.get("role") == "video_background" and background.get("origin") == "generated_scene"
                 and background.get("path") in BACKGROUND_PATHS,
                 "video background must be a generated scene at input/video-background.png|jpg|jpeg")
        _require(thumbnail.get("role") == "youtube_thumbnail" and thumbnail.get("path") == "input/thumb.jpg",
                 "YouTube thumbnail must have its separate input/thumb.jpg role/path")
        image, thumb = _bound(series, background), _bound(series, thumbnail)
        _require(image != thumb and background["sha256"] != thumbnail["sha256"],
                 "video background cannot be the YouTube thumbnail or its renamed copy")
        if image_path is not None:
            _require(image_path.resolve() == image, "render image differs from declared video background")
        with Image.open(image) as opened:
            scene = ImageOps.exif_transpose(opened).convert("RGBA")
            _require(scene.size == (3840, 2160), "video background must be actual 3840x2160 pixels")
            _require(getattr(opened, "n_frames", 1) == 1, "video background must be a single static image")
        with Image.open(thumb) as opened:
            thumbnail_pixels = ImageOps.exif_transpose(opened).convert("RGBA")
            _require(scene.size != thumbnail_pixels.size or scene.tobytes() != thumbnail_pixels.tobytes(),
                     "video background and YouTube thumbnail have identical decoded pixels")
        review = _json(_bound(series, manifest["visual_review"]))
        _require(review.get("schema") == "wavvy.video_artwork_review.v1"
                 and review.get("image") == {"path": background["path"], "sha256": background["sha256"]},
                 "visual review must bind the exact video background path/hash")
        _require(review.get("method") == "view_image" and isinstance(review.get("reviewer"), str)
                 and bool(review["reviewer"].strip()) and isinstance(review.get("evidence"), str)
                 and bool(review["evidence"].strip()), "visual review requires view_image, reviewer, and observed evidence")
        reviewed_at = datetime.fromisoformat(review["reviewed_at"].replace("Z", "+00:00"))
        _require(reviewed_at.tzinfo is not None, "visual review timestamp requires a timezone")
        observations = review["observations"]
        _require(observations.get("wavvy_logo_present") is True
                 and all(observations.get(key) is False for key in
                         ("title_text_present", "bpm_text_present", "other_overlay_text_present")),
                 "visual review must confirm Wavvy logo present and title/BPM/other overlay text absent")
        binding = {"path": MANIFEST, "sha256": file_sha256(manifest_path)}
        if report is not None:
            _require(report.get("processing_params", {}).get("video_artwork") == binding,
                     "render report must bind the current video artwork manifest path/hash")
        return {"image": image, "thumbnail": thumb, "manifest": manifest, "binding": binding}, []
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        return {}, [f"Video artwork: {error}"]
