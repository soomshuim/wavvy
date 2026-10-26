"""Synthetic files for exercising the artwork evidence contract."""

import json
from pathlib import Path

from PIL import Image

from wavvy_harness.video_artwork import MANIFEST, file_sha256


def make_artwork(series: Path) -> dict:
    (series / "input").mkdir(parents=True, exist_ok=True)
    (series / "production").mkdir(parents=True, exist_ok=True)
    image = series / "input/video-background.png"
    thumbnail = series / "input/thumb.jpg"
    Image.new("RGB", (3840, 2160), "navy").save(image)
    if not thumbnail.exists():
        Image.new("RGB", (64, 36), "orange").save(thumbnail)
    background = {"path": "input/video-background.png", "sha256": file_sha256(image)}
    review_path = series / "production/video-artwork-review.json"
    review = {"schema": "wavvy.video_artwork_review.v1", "image": background.copy(),
              "method": "view_image", "reviewer": "Synthetic test fixture", "reviewed_at": "2026-10-26T17:00:00+09:00",
              "observations": {"wavvy_logo_present": True, "title_text_present": False,
                               "bpm_text_present": False, "other_overlay_text_present": False},
              "evidence": "Synthetic observations test evidence binding, not visual quality."}
    review_path.write_text(json.dumps(review), encoding="utf-8")
    manifest = {"schema": "wavvy.video_artwork.v1",
                "video_background": dict(background, role="video_background", origin="generated_scene"),
                "thumbnail": {"path": "input/thumb.jpg", "sha256": file_sha256(thumbnail), "role": "youtube_thumbnail"},
                "visual_review": {"path": "production/video-artwork-review.json", "sha256": file_sha256(review_path)}}
    (series / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    return manifest
