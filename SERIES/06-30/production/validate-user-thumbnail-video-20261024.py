#!/usr/bin/env python3
"""Retain direct stream, audio-packet, chapter and decode evidence for the MP4."""

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT / "SERIES/06-30"
OUT = SERIES / "output/video-user-thumbnail-20261024"
FINAL = OUT / "final-0630-4k-v2.mp4"
RECORD = SERIES / "production/video-user-thumbnail-20261024.json"
VALIDATION = SERIES / "production/video-user-thumbnail-20261024-validation.json"


def sha256(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def run(command, name):
    started = time.monotonic()
    result = subprocess.run(command, capture_output=True, text=True)
    (OUT / f"validation-{name}.stdout.txt").write_text(result.stdout)
    (OUT / f"validation-{name}.stderr.txt").write_text(result.stderr)
    evidence = {"command": command, "exit_code": result.returncode,
                "elapsed_seconds": time.monotonic() - started,
                "stdout_path": str((OUT / f"validation-{name}.stdout.txt").relative_to(ROOT)),
                "stderr_path": str((OUT / f"validation-{name}.stderr.txt").relative_to(ROOT))}
    assert result.returncode == 0, evidence
    return result.stdout, evidence


def packet_summary(path, name):
    # Encoded packet bytes and sample-based positions must both survive the remux.
    command = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
               "-show_data_hash", "sha256", "-show_entries",
               "packet=pts,dts,duration,size,data_hash:packet_side_data=side_data_type,skip_samples,discard_padding",
               "-of", "compact=p=0:nk=0", str(path)]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    digest = hashlib.sha256()
    count = 0
    first = []
    last = []
    for line in result.stdout:
        digest.update(line)
        text = line.decode().rstrip()
        if text.startswith("pts="):
            count += 1
            if len(first) < 2:
                first.append(text)
            last = (last + [text])[-2:]
    error = result.stderr.read().decode()
    exit_code = result.wait()
    assert exit_code == 0, error
    summary = {"command": command, "exit_code": exit_code, "packet_count": count,
               "packet_payload_and_timing_sha256": digest.hexdigest(),
               "first_two": first, "last_two": last, "stderr": error}
    (OUT / f"validation-{name}-packet-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main():
    record = json.loads(RECORD.read_text())
    assert record["runs"]["full"]["exit_code"] == 0
    checks = {}
    sources = {}
    for key in ("image", "audio"):
        item = record[key]
        actual = sha256(ROOT / item["path"])
        assert actual == item["sha256"]
        sources[key] = {"path": item["path"], "sha256": actual, "unchanged": True}
    checks["source_hashes"] = sources
    retained = json.loads((SERIES / "production/continuous-mix-20261024-repeat2.json").read_text())
    retained_checks = []
    source_entries = record["chapter_entries"]
    for order in (6, 11):
        path = ROOT / next(entry["source_path"] for entry in source_entries if entry["order"] == order)
        expected = next(entry["expected"] for entry in retained["source_hashes"] if entry["order"] == order)
        actual = sha256(path)
        assert actual == expected
        retained_checks.append({"path": str(path.relative_to(ROOT)), "sha256": actual, "unchanged": True})
    checks["retained_6_and_11"] = retained_checks
    actual_final_sha = sha256(FINAL)
    assert actual_final_sha == record["runs"]["full"]["output_sha256"]
    checks["final_file_sha256"] = actual_final_sha
    raw, evidence = run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                         "-show_chapters", "-of", "json", str(FINAL)], "probe")
    probe = json.loads(raw)
    streams = probe["streams"]
    video = [stream for stream in streams if stream["codec_type"] == "video"]
    audio = [stream for stream in streams if stream["codec_type"] == "audio"]
    assert len(video) == len(audio) == 1
    video, audio = video[0], audio[0]
    assert video["codec_name"] == "h264" and (video["width"], video["height"]) == (3840, 2160)
    assert video["avg_frame_rate"] == video["r_frame_rate"] == "1/1"
    assert audio["codec_name"] == "aac" and audio["sample_rate"] == "48000" and audio["channels"] == 2
    assert audio["start_time"] == "0.000000"
    assert float(audio["duration"]) == record["audio"]["duration_seconds"]
    video_tail = float(video["duration"]) - float(audio["duration"])
    assert 0 <= video_tail < 1
    checks["probe"] = {"evidence": evidence, "streams": streams,
                       "format": probe["format"], "video_frame_rounding_tail_seconds": video_tail}
    chapters = probe["chapters"]
    assert len(chapters) == 40
    chapter_checks = []
    for actual, expected in zip(chapters, source_entries):
        difference = float(actual["start_time"]) - expected["mix_entry_sample"] / 48000
        assert abs(difference) <= 0.000501
        assert actual["tags"]["title"] == f"{expected['order']:02d}. {expected['title']} (cycle {expected['cycle']})"
        chapter_checks.append({"cycle": expected["cycle"], "order": expected["order"],
                               "source_start_sample": expected["mix_entry_sample"],
                               "actual_start_seconds": float(actual["start_time"]),
                               "rounding_seconds": difference})
    checks["chapters"] = {"count": len(chapters), "source_sample_starts_retained": True,
                          "mp4_maximum_rounding_seconds": max(abs(e["rounding_seconds"]) for e in chapter_checks),
                          "entries": chapter_checks}
    source_packets = packet_summary(ROOT / record["audio"]["path"], "source")
    final_packets = packet_summary(FINAL, "final")
    assert source_packets["packet_count"] == final_packets["packet_count"]
    assert source_packets["packet_payload_and_timing_sha256"] == final_packets["packet_payload_and_timing_sha256"]
    checks["audio_packets"] = {"all_identical": True, "source": source_packets, "final": final_packets}
    _, evidence = run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-xerror",
                       "-err_detect", "explode", "-i", str(FINAL), "-map", "0:v:0",
                       "-map", "0:a:0", "-f", "null", "-"], "full-video-audio-decode")
    checks["full_video_audio_decode"] = evidence
    checks["frames"] = []
    for label, second in (("begin", 0), ("middle", 3785), ("end", 7570)):
        frame = OUT / f"final-frame-{label}.png"
        _, evidence = run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "error", "-n",
                           "-ss", str(second), "-i", str(FINAL), "-map", "0:v:0",
                           "-frames:v", "1", str(frame)], f"frame-{label}")
        assert frame.exists()
        checks["frames"].append({"position_seconds": second, "path": str(frame.relative_to(ROOT)),
                                 "sha256": sha256(frame), "evidence": evidence})
    result = {"schema": "wavvy.series_local_premix_video_validation.v1",
              "completed_utc": datetime.now(timezone.utc).isoformat(),
              "checks": checks, "technical_assertions_passed": True,
              "scope": "Direct final MP4 checks; does not assert legacy source-final gate pass, listening approval, title approval or YouTube upload",
              "visual_inspection_status": "pending_worker_view_of_three_frames"}
    VALIDATION.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"technical_assertions_passed": True, "final_sha256": actual_final_sha,
                      "audio_packets_identical": True, "chapter_count": 40,
                      "duration_seconds": audio["duration"], "video_tail_seconds": video_tail,
                      "validation": str(VALIDATION.relative_to(ROOT))}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
