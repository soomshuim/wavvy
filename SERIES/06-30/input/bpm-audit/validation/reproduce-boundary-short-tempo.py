#!/usr/bin/env python3
"""Reproduce the 175.35 BPM track with a 12-second 174.6 BPM passage."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument("--expect", choices=("inside", "out", "uncertain"), required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

script = Path(__file__).resolve().parents[1] / "analyze.py"
spec = importlib.util.spec_from_file_location("bpm_audit", script)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

rate = audit.SAMPLE_RATE
audio = np.zeros(190 * rate, dtype=np.float32)
t = .25
while t < 189.8:
    bpm = 174.6 if 55 <= t < 67 else 175.35
    index = round(t * rate)
    local = np.arange(3000) / rate
    kick = .6 * np.sin(2 * np.pi * (60 * local - 30 * local * local)) * np.exp(-local * 45)
    click = .25 * np.exp(-local * 600)
    audio[index:index + 3000] += (kick + click).astype(np.float32)
    t += 60 / bpm

audio_sha = hashlib.sha256(audio.tobytes()).hexdigest()
assert audio_sha == "13beafd257d39deaf5149af2333109de60e71e6ad9a037b9dca2a64d5aacd228"
report = audit.analyze_audio(audio, "boundary-short-tempo", {
    "kind": "synthetic-independent-review-reproduction",
    "sha256_float32_audio": audio_sha,
    "analyze_py_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    "recipe": {"base_bpm": 175.35, "replacement_bpm": 174.6,
               "start_seconds": 55, "stop_seconds": 67, "length_seconds": 190},
})
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"classification": report["classification"],
                  "interval": report.get("conservative_bpm_interval"),
                  "reasons": report["reasons"], "audio_sha256": audio_sha,
                  "analyze_py_sha256": report["source"]["analyze_py_sha256"]},
                 ensure_ascii=False))
assert report["classification"] == args.expect
