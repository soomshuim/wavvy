#!/usr/bin/env python3
"""Reproduce the independent review's two short-tempo false verdicts."""

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "analyze.py"
spec = importlib.util.spec_from_file_location("bpm_audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

cases = [
    ("brief-190-tempo", 176, 190, 58, 62),
    ("outside-with-inside-patch", 180, 176, 56, 65),
]
for name, base_bpm, replacement_bpm, start, stop in cases:
    audio = audit.synth(base_bpm, 190, "rock")
    replacement = audit.synth(replacement_bpm, stop - start + 1, "rock")
    audio[start * audit.SAMPLE_RATE:stop * audit.SAMPLE_RATE] = (
        replacement[:(stop - start) * audit.SAMPLE_RATE]
    )
    result = audit.analyze_audio(audio, name, {
        "kind": "synthetic-independent-review-reproduction",
        "sha256_float32_audio": hashlib.sha256(audio.tobytes()).hexdigest(),
        "analyze_py_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        "recipe": {
            "base_bpm": base_bpm, "length_seconds": 190, "style": "rock",
            "replacement_bpm": replacement_bpm,
            "start_seconds": start, "stop_seconds": stop,
        },
    })
    if result["classification"] != "uncertain":
        raise AssertionError(f"{name}: expected uncertain, got {result['classification']}")
    output = HERE / f"regression-{name}.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "case": name, "classification": result["classification"],
        "reasons": result["reasons"], "output": str(output),
    }, ensure_ascii=False))
