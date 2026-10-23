#!/usr/bin/env python3
"""One approved first-song adaptive atempo working render, never a final source."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.io import wavfile


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "SERIES/06-30/input/tempo-adjustment"
SOURCE = ROOT / "work/0630-tempo-full/24703f3f-c7ce-433f-a892-16d9330b41a9-working-source.wav"
RAW_CURVE = BASE / "measurements/track01-source-8s-free-curve-raw.json"
CURVE = BASE / "full-source/track01-adaptive-source-curve.json"
COMMANDS = BASE / "full-source/track01-adaptive-atempo-commands.txt"
OUTPUT = ROOT / "work/0630-tempo-adjustment-20261023/full/01-24703f3f-variable-target176-working.wav"
LOG = ROOT / "work/0630-tempo-adjustment-20261023/full/01-24703f3f-variable-target176-ffmpeg.log"
PROOF = BASE / "full-source/track01-adaptive-render-technical-check.json"


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def stats(path: Path) -> dict:
    rate, audio = wavfile.read(path, mmap=True)
    if audio.dtype != np.float32 or audio.ndim != 2 or audio.shape[1] != 2:
        raise ValueError("expected stereo float32 WAV")
    if not np.isfinite(audio).all():
        raise ValueError("nonfinite audio")
    amplitude = np.abs(audio)
    steps = np.abs(np.diff(audio, axis=0))
    return {
        "sha256": digest(path), "sample_rate_hz": rate, "channels": 2,
        "frames": len(audio), "duration_s": len(audio)/rate,
        "finite": True, "peak_abs": float(amplitude.max()),
        "clip_samples_abs_gte_1": int(np.count_nonzero(amplitude >= 1)),
        "rms": float(np.sqrt(np.mean(np.square(audio.astype(np.float64))))),
        "max_adjacent_frame_delta": float(steps.max()),
        "p999999_adjacent_frame_delta": float(np.quantile(steps, .999999)),
    }


def main() -> None:
    for path in (CURVE, COMMANDS, OUTPUT, LOG, PROOF):
        if path.exists():
            raise FileExistsError(f"single variant path already exists: {path}")
    source = stats(SOURCE)
    if source["sha256"] != "b1f9c36e5085786008d48f2385b537817f71835e4b54b3bf59e138c38733017a":
        raise ValueError("first-song source hash changed")
    raw = json.loads(RAW_CURVE.read_text())
    if raw["source_sha256"] != source["sha256"] or raw["window_s"] != 8 or raw["stride_s"] != 4:
        raise ValueError("raw curve does not match source/window plan")
    anchors = []
    weak = []
    mid_support = []
    for row in raw["windows"]:
        fits = [f for f in row["raw"]["lattice_fits"] if f["band"] == "high"]
        if not fits:
            weak.append({"start_s": row["start_s"], "reason": "missing high-band grid"})
            continue
        best = max(fits, key=lambda f: f["coherence"])
        if best["coherence"] < .7 or best["span_s"] < 5 or best["inlier_count"] < 25:
            weak.append({"start_s": row["start_s"], "reason": "insufficient free-grid coverage",
                         "fit": best})
            continue
        mid = [f for f in row["raw"]["lattice_fits"] if f["band"] == "mid"]
        harmonic_mid = [f for f in mid if abs(2*f["bpm_fit"]-best["bpm_fit"]) <= 1]
        if harmonic_mid:
            mid_support.append({"start_s": row["start_s"],
                                "high_half_bpm": best["bpm_fit"]/2,
                                "direct_mid_bpm": max(harmonic_mid, key=lambda f: f["coherence"])["bpm_fit"]})
        anchors.append({"window_start_s": row["start_s"], "center_source_s": row["start_s"]+4,
                        "high_grid_bpm": best["bpm_fit"], "coherence": best["coherence"],
                        "span_s": best["span_s"], "inlier_count": best["inlier_count"],
                        "source_pulse_hypothesis_bpm": best["bpm_fit"]/2,
                        "target176_factor": 176/(best["bpm_fit"]/2)})
    if len(raw["windows"]) != 49 or len(anchors) != 48 or [w["start_s"] for w in weak] != [190.4]:
        raise ValueError("unexpected weak/missing measurement coverage")
    if len(mid_support) < 30 or max(abs(r["high_half_bpm"]-r["direct_mid_bpm"]) for r in mid_support) > .5:
        raise ValueError("high-grid half-pulse family lacks direct mid support")
    bpm = [row["high_grid_bpm"] for row in anchors]
    if max(abs(b-a) for a, b in zip(bpm, bpm[1:])) > 6:
        raise ValueError("discontinuous source grid")
    if not all(330 < b < 420 for b in bpm):
        raise ValueError("source beat family changed dramatically")
    centers = np.array([a["center_source_s"] for a in anchors])
    factors = np.array([a["target176_factor"] for a in anchors])
    if not all(.5 < factor < 2 for factor in factors):
        raise ValueError("unsupported atempo range")
    duration = source["duration_s"]
    times = np.arange(.5, duration, .5)
    command_factors = np.interp(times, centers, factors)
    initial = float(factors[0])
    expected = 0.0
    previous = 0.0
    for boundary, factor in zip(times, np.r_[initial, command_factors[:-1]]):
        expected += (float(boundary)-previous)/float(factor)
        previous = float(boundary)
    expected += (duration-previous)/float(command_factors[-1])
    curve = {
        "scope": "one first-song adaptive working render only; not a final selection or quality approval",
        "source_path": str(SOURCE.relative_to(ROOT)), "source_sha256": source["sha256"],
        "raw_curve_path": str(RAW_CURVE.relative_to(ROOT)), "raw_curve_sha256": digest(RAW_CURVE),
        "measurement_selection": "Within each source-only 8s window, take the highest-coherence high-band free lattice; require coherence>=0.7, span>=5s, >=25 inliers, <=6 BPM jump across adjacent windows. The same half-grid family has direct mid-band support in 36 windows. No 176 target is used to find lattice seeds.",
        "anchors": anchors, "direct_mid_support": mid_support, "weak_windows": weak,
        "source_time_extrapolation_s": {"start": [0, 4], "end": [192, duration]},
        "target_bpm": 176, "factor_formula": "176 / (source high-grid BPM / 2)",
        "factor_interpolation": "linear by source-time window center; hold nearest anchor before 4s and after 192s; issue step commands every 0.5 source seconds",
        "initial_factor": initial, "command_interval_s": .5,
        "command_count": len(times), "expected_integral_duration_s": expected,
        "high_grid_range_bpm": [min(bpm), max(bpm)],
        "factor_range": [float(factors.min()), float(factors.max())],
        "final_selection": False,
    }
    CURVE.parent.mkdir(parents=True, exist_ok=True)
    with CURVE.open("x") as stream:
        json.dump(curve, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    lines = [f"{time:.3f} atempo tempo {factor:.12f}" for time, factor in zip(times, command_factors)]
    with COMMANDS.open("x") as stream:
        stream.write(";\n".join(lines)+"\n")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "debug", "-n",
               "-i", str(SOURCE), "-af", f"asendcmd=f={COMMANDS},atempo={initial:.12f}",
               "-c:a", "pcm_f32le", str(OUTPUT)]
    run = subprocess.run(command, capture_output=True, text=True)
    with LOG.open("x") as stream:
        stream.write(run.stderr)
    dispatched = run.stderr.count("Processing command #0 target:atempo command:tempo")
    if run.returncode or dispatched != len(times):
        raise RuntimeError(f"ffmpeg failed or command count mismatch: exit={run.returncode} dispatched={dispatched}/{len(times)}; preserve output/log and stop")
    after = stats(OUTPUT)
    if (after["sample_rate_hz"] != source["sample_rate_hz"] or
            after["channels"] != source["channels"] or
            after["clip_samples_abs_gte_1"] > source["clip_samples_abs_gte_1"] or
            after["max_adjacent_frame_delta"] > max(.8, source["max_adjacent_frame_delta"]*2)):
        raise ValueError("technical output validation failed; preserve output/log and stop")
    proof = {
        "scope": "one adaptive atempo first-song working render; output BPM and listening quality need independent checks",
        "curve_path": str(CURVE.relative_to(ROOT)), "curve_sha256": digest(CURVE),
        "commands_path": str(COMMANDS.relative_to(ROOT)), "commands_sha256": digest(COMMANDS),
        "ffmpeg_log_path": str(LOG.relative_to(ROOT)), "ffmpeg_log_sha256": digest(LOG),
        "ffmpeg_exit_code": run.returncode, "commands_dispatched": dispatched,
        "ffmpeg_command": command, "source": {"path": str(SOURCE.relative_to(ROOT)), **source},
        "output": {"path": str(OUTPUT.relative_to(ROOT)), **after},
        "expected_integral_duration_s": expected,
        "duration_difference_from_integral_s": after["duration_s"]-expected,
        "official_download": False, "final_selection": False,
    }
    with PROOF.open("x") as stream:
        json.dump(proof, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"source_s": duration, "expected_s": expected,
                      "output_s": after["duration_s"], "output_sha256": after["sha256"],
                      "commands": dispatched, "clip_samples": after["clip_samples_abs_gte_1"]}))


if __name__ == "__main__":
    main()
