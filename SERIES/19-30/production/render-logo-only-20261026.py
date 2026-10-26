#!/usr/bin/env python3
"""Render the approved19:30 final160 premix without rebuilding or repeating audio.

This is a series-local production record, not a replacement for source gates.
Run from the repository root with one argument: preview or full.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT / "SERIES/19-30"
PRODUCTION = SERIES / "production"
OUTPUT = SERIES / "output/video-logo-only-20261026"
IMAGE = SERIES / "input/video-background.png"
AUDIO = SERIES / "output/mix-160-20261026/continuous-mix-1930-160-repeat2.m4a"
SOURCE_MANIFEST = PRODUCTION / "mix-160-20261026/manifest.json"
RECORD = PRODUCTION / "video-logo-only-20261026/video-record.json"
EXPECTED_IMAGE = "8c8a7583db186719cd9f07f13b1756299096a69be12049821609bb1f516bf78e"
EXPECTED_AUDIO = "35aa3d44f9c7d50e0a994664e819c3ae34ce9dbe7aa6fbcb098e69c7c7b9f0f7"


def sha256(path):
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-show_chapters", "-of", "json", str(path),
    ]))


def save(record):
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


def main():
    if sys.argv[1:] not in (["preview"], ["full"]):
        raise SystemExit("Usage: render-logo-only-20261026.py preview|full")
    stage = sys.argv[1]
    sys.path.insert(0, str(ROOT))
    from wavvy_harness.video_artwork import check_video_artwork
    artwork, errors = check_video_artwork(SERIES, image_path=IMAGE)
    guard = {"passed": not errors, "errors": errors, "binding": artwork.get("binding")}
    (RECORD.parent / f"artwork-guard-{stage}.json").write_text(json.dumps(guard, indent=2) + "\n")
    assert not errors, errors
    before = {relative(path): sha256(path) for path in (IMAGE, AUDIO)}
    assert before[relative(IMAGE)] == EXPECTED_IMAGE, "Approved JPG changed; stop"
    assert before[relative(AUDIO)] == EXPECTED_AUDIO, "Approved premix changed; stop"
    image_probe = probe(IMAGE)
    image_stream = image_probe["streams"][0]
    assert (image_stream["width"], image_stream["height"]) == (3840, 2160)
    audio_probe = probe(AUDIO)
    duration = float(audio_probe["format"]["duration"])
    source = json.loads(SOURCE_MANIFEST.read_text())
    pcm_extent_duration = source["duration_seconds"]
    duration = float(audio_probe["format"]["duration"])
    assert source["samples"] == 318568444 and source["target_bpm"] == 160
    assert source["aac_sha256"] == EXPECTED_AUDIO
    assert source["repeat_count"] == 2 and source["additional_repeats"] == 0
    assert abs(float(next(v for v in audio_probe["streams"] if v["codec_type"] == "audio")["duration"]) - pcm_extent_duration) <= 0.001
    entries = [{**e, "mix_entry_sample": e["mix_start_sample"], "mix_entry_seconds": e["mix_start_seconds"]} for e in source["entries"]]
    assert len(entries) == 40
    assert [(e["cycle"], e["order"]) for e in entries] == [
        (cycle, order) for cycle in (1, 2) for order in range(1, 21)
    ]
    starts = [e["mix_entry_sample"] for e in entries]
    assert starts[0] == 0 and all(a < b for a, b in zip(starts, starts[1:]))
    free_bytes = shutil.disk_usage(OUTPUT.parent).free
    assert free_bytes > 3 * 1024**3, "Less than 3 GiB free"
    OUTPUT.mkdir(exist_ok=True)
    record = json.loads(RECORD.read_text()) if RECORD.exists() else {
        "schema": "wavvy.series_local_premix_video.v1",
        "processing_params": {"video_artwork": artwork["binding"]},
        "video_artwork": artwork["binding"],
        "producer_script": {"path": relative(Path(__file__)), "sha256": sha256(Path(__file__))},
        "scope": "Approved logo-only4K generated scene; final160 two-cycle AAC copied once; separate YouTube thumbnail; no additional repeats or source-gate substitution",
        "image": {"path": relative(IMAGE), "sha256": EXPECTED_IMAGE,
                  "file_bytes": IMAGE.stat().st_size, "width": 3840, "height": 2160},
        "audio": {"path": relative(AUDIO), "sha256": EXPECTED_AUDIO,
                  "file_bytes": AUDIO.stat().st_size, "duration_seconds": duration,
                  "cycles_already_in_source": 2, "extra_repetitions": 0,
                  "pcm_extent_samples": source["samples"], "pcm_extent_duration_seconds": pcm_extent_duration,
                  "container_vs_pcm_difference_samples": round((pcm_extent_duration-duration)*48000)},
        "source_manifest": {"path": relative(SOURCE_MANIFEST), "sha256": sha256(SOURCE_MANIFEST)},
        "chapter_entries": entries,
        "chapter_meaning": "Retained incoming fade/beat-grid starts; not newly certified first audible samples. MP4 chapter timestamps are rounded to milliseconds.",
        "image_processing": "scale=3840:2160:flags=lanczos,setsar=1; no crop, overlay, shadow, new text, or color-grading filter",
        "runs": {},
    }
    assert record["processing_params"]["video_artwork"] == artwork["binding"], "Artwork binding changed after preview"
    assert record["source_manifest"]["sha256"] == sha256(SOURCE_MANIFEST), "Audio production manifest changed"
    if stage == "full":
        assert record["runs"].get("preview", {}).get("exit_code") == 0, "Preview must complete first"
        preview_validation = json.loads((RECORD.parent / "preview-validation.json").read_text())
        assert preview_validation["technical_assertions_passed"] and preview_validation["visual_inspection_passed"], "Preview must pass technical and visual inspection"
    target = OUTPUT / ("preview-30s-4k.mp4" if stage == "preview" else "final-1930-4k.mp4")
    assert not target.exists(), f"Refusing to overwrite {target}"
    command = ["ffmpeg", "-hide_banner", "-nostdin", "-n",
               "-loop", "1", "-framerate", "1", "-i", str(IMAGE),
               "-i", str(AUDIO)]
    if stage == "full":
        metadata = OUTPUT / "chapters.ffmetadata"
        lines = [";FFMETADATA1"]
        for index, entry in enumerate(entries):
            end_sample = starts[index + 1] if index + 1 < len(starts) else source["samples"]
            title = f"{entry['order']:02d}. {entry['title']} (cycle {entry['cycle']})"
            for original, escaped in (("\\", "\\\\"), ("=", "\\="), (";", "\\;"), ("#", "\\#"), ("\n", "\\\n")):
                title = title.replace(original, escaped)
            lines.extend(["[CHAPTER]", "TIMEBASE=1/48000",
                          f"START={entry['mix_entry_sample']}", f"END={end_sample}", f"title={title}"])
        metadata.write_text("\n".join(lines) + "\n")
        command.extend(["-f", "ffmetadata", "-i", str(metadata), "-map_chapters", "2"])
    command.extend([
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", "scale=3840:2160:flags=lanczos,setsar=1",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-tune", "stillimage",
        "-pix_fmt", "yuv420p", "-r", "1", "-c:a", "copy",
        "-t", "30" if stage == "preview" else f"{pcm_extent_duration:.9f}",
        "-movflags", "+faststart", "-progress", str(OUTPUT / f"{stage}-progress.txt"),
        "-nostats", str(target),
    ])
    run = {"started_utc": datetime.now(timezone.utc).isoformat(), "command": command,
           "output": relative(target), "free_bytes_before": free_bytes,
           "log": relative(OUTPUT / f"{stage}-ffmpeg.log"), "status": "running"}
    if stage in record["runs"]:
        record.setdefault("diagnostic_runs", []).append(record["runs"][stage])
    record["runs"][stage] = run
    save(record)
    print(json.dumps({"stage": stage, "status": "running", "record": relative(RECORD),
                      "output": relative(target)}, ensure_ascii=False), flush=True)
    started = time.monotonic()
    with (OUTPUT / f"{stage}-ffmpeg.log").open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    run.update({"exit_code": result.returncode, "elapsed_seconds": time.monotonic() - started,
                "finished_utc": datetime.now(timezone.utc).isoformat(),
                "status": "rendered_pending_validation" if result.returncode == 0 else "failed"})
    if result.returncode == 0:
        run.update({"output_sha256": sha256(target), "file_bytes": target.stat().st_size,
                    "probe": probe(target)})
    after = {relative(path): sha256(path) for path in (IMAGE, AUDIO)}
    run["source_hashes_after"] = after
    run["sources_unchanged"] = before == after
    save(record)
    assert result.returncode == 0, f"FFmpeg failed; see {run['log']}"
    assert before == after, "Source changed during rendering"
    print(json.dumps({"stage": stage, "exit_code": result.returncode,
                      "elapsed_seconds": run["elapsed_seconds"], "file_bytes": run["file_bytes"],
                      "probe_duration": run["probe"]["format"]["duration"]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
