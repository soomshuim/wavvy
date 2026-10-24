#!/usr/bin/env python3
"""Render the approved 07:00 premix without rebuilding or repeating audio.

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
SERIES = ROOT / "SERIES/07-00"
PRODUCTION = SERIES / "production"
OUTPUT = SERIES / "output/video-user-thumbnail-20261024"
IMAGE = SERIES / "input/thumb.jpg"
AUDIO = SERIES / "output/continuous-180-20261024/continuous-mix-0700-repeat2.m4a"
SOURCE_MANIFEST = PRODUCTION / "continuous-180-20261024/manifest.json"
RECORD = PRODUCTION / "video-user-thumbnail-20261024.json"
EXPECTED_IMAGE = "93b63f208ff89c81c705ef64b53fd299911a55d7f65d8a3386bd65fa8feb4944"
EXPECTED_AUDIO = "69304f102a2455446252661fb1696afad94579ebcfab2cde8b559038b53a5afe"


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
        raise SystemExit("Usage: render-user-thumbnail-20261024.py preview|full")
    stage = sys.argv[1]
    before = {relative(path): sha256(path) for path in (IMAGE, AUDIO)}
    assert before[relative(IMAGE)] == EXPECTED_IMAGE, "Approved JPG changed; stop"
    assert before[relative(AUDIO)] == EXPECTED_AUDIO, "Approved premix changed; stop"
    image_probe = probe(IMAGE)
    image_stream = image_probe["streams"][0]
    assert (image_stream["width"], image_stream["height"]) == (2532, 1424)
    audio_probe = probe(AUDIO)
    duration = float(audio_probe["format"]["duration"])
    assert duration == 6722.859
    source = json.loads(SOURCE_MANIFEST.read_text())
    assert source["audio_sha256"] == EXPECTED_AUDIO
    entries = source["timeline"]["track_entries"]
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
        "scope": "Approved JPG upscaled only; existing two-cycle AAC copied once; no shared harness/source-gate substitution",
        "image": {"path": relative(IMAGE), "sha256": EXPECTED_IMAGE,
                  "file_bytes": IMAGE.stat().st_size, "width": 2532, "height": 1424},
        "audio": {"path": relative(AUDIO), "sha256": EXPECTED_AUDIO,
                  "file_bytes": AUDIO.stat().st_size, "duration_seconds": duration,
                  "cycles_already_in_source": 2, "extra_repetitions": 0},
        "source_manifest": {"path": relative(SOURCE_MANIFEST), "sha256": sha256(SOURCE_MANIFEST)},
        "chapter_entries": entries,
        "chapter_meaning": "Retained incoming fade/beat-grid starts; not newly certified first audible samples. MP4 chapter timestamps are rounded to milliseconds.",
        "image_processing": "scale=3840:2160:flags=lanczos,setsar=1; no crop, overlay, shadow, new text, or color-grading filter",
        "runs": {},
    }
    if stage == "full":
        assert record["runs"].get("preview", {}).get("exit_code") == 0, "Preview must complete first"
    target = OUTPUT / ("preview-30s-4k.mp4" if stage == "preview" else "final-0700-4k.mp4")
    assert not target.exists(), f"Refusing to overwrite {target}"
    command = ["ffmpeg", "-hide_banner", "-nostdin", "-n",
               "-loop", "1", "-framerate", "1", "-i", str(IMAGE),
               "-i", str(AUDIO)]
    if stage == "full":
        metadata = OUTPUT / "chapters.ffmetadata"
        lines = [";FFMETADATA1"]
        for index, entry in enumerate(entries):
            end_sample = starts[index + 1] if index + 1 < len(starts) else round(duration * 48000)
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
        "-t", "30" if stage == "preview" else f"{duration:.6f}",
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
