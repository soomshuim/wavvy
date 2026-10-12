"""Validate a CSV-selected MP4 upload copy against its render report."""

from __future__ import annotations

import csv
from pathlib import Path

import ffmpeg


def check_upload_copy(series_path: Path, report: dict, require_4k: bool) -> tuple[bool, list[dict], list[str]]:
    """Return active/checks/errors; older series without an MP4 keep their flow."""
    series_path = series_path.resolve()
    output = series_path / "output"
    copy = output / "final.mp4"
    csv_path = output / "upload.csv"
    if not csv_path.is_file():
        return False, [], []
    try:
        with csv_path.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
    except (OSError, UnicodeError) as error:
        return True, [], [f"upload.csv cannot be read: {error}"]
    if len(rows) != 1:
        return True, [], ["upload.csv must contain exactly one upload row"]
    video_value = rows[0].get("video_path") or ""
    active = require_4k or copy.is_file() or Path(video_value).suffix.lower() == ".mp4"
    if not active:
        return False, [], []
    checks: list[dict] = []
    errors: list[str] = []

    csv_video = Path(video_value)
    candidates = [csv_video] if csv_video.is_absolute() else [
        series_path / csv_video,
        output / csv_video,
        series_path.parents[1] / csv_video,
    ]
    path_ok = bool(video_value) and any(path.resolve() == copy for path in candidates)
    checks.append({"name": "upload_copy_csv_path", "status": "PASS" if path_ok else "FAIL", "detail": video_value})
    if not path_ok:
        errors.append("upload.csv video_path must identify output/final.mp4 upload copy")
    if not copy.is_file():
        checks.append({"name": "upload_copy_file_present", "status": "FAIL", "detail": str(copy)})
        errors.append("upload.csv selects output/final.mp4 but that upload file is missing")
        return True, checks, errors
    checks.append({"name": "upload_copy_file_present", "status": "PASS", "detail": str(copy)})

    try:
        probe = ffmpeg.probe(str(copy))
        streams = probe.get("streams", [])
        video = next((item for item in streams if item.get("codec_type") == "video"), None)
        audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
        streams_ok = bool(video and audio)
        checks.append({"name": "upload_copy_streams", "status": "PASS" if streams_ok else "FAIL",
                       "detail": f"video={video.get('codec_name') if video else None} audio={audio.get('codec_name') if audio else None}"})
        if not streams_ok:
            errors.append("output/final.mp4 requires video and audio streams")
        if require_4k:
            spec_ok = bool(video and audio and video.get("codec_name") == "h264" and audio.get("codec_name") == "aac"
                           and int(video.get("width", 0)) >= 3840 and int(video.get("height", 0)) >= 2160)
            checks.append({"name": "upload_copy_4k_h264_aac", "status": "PASS" if spec_ok else "FAIL",
                           "detail": f"{video.get('width') if video else None}x{video.get('height') if video else None}"
                           f" {video.get('codec_name') if video else None}/{audio.get('codec_name') if audio else None}"})
            if not spec_ok:
                errors.append("output/final.mp4 must be at least 3840x2160 H.264 video with AAC audio for this packaging contract")
        expected_duration = float(report["summary"]["final_duration"])
        actual_duration = float(probe["format"]["duration"])
        duration_ok = abs(actual_duration - expected_duration) <= 1.0
        checks.append({"name": "upload_copy_duration", "status": "PASS" if duration_ok else "FAIL",
                       "detail": f"actual={actual_duration:.2f}s report={expected_duration:.2f}s"})
        if not duration_ok:
            errors.append("output/final.mp4 duration differs from report by more than 1 second")
    except (ffmpeg.Error, OSError, KeyError, TypeError, ValueError) as error:
        checks.append({"name": "upload_copy_probe", "status": "FAIL", "detail": str(error)})
        errors.append(f"output/final.mp4 probe failed: {error}")
    return True, checks, errors
