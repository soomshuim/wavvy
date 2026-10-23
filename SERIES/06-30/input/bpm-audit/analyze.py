#!/usr/bin/env python3
"""Conservative, audio-based BPM audit for 06:30 Suno candidates.

Run in the isolated Essentia environment; this tool never deletes candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import essentia
import essentia.standard as es
import numpy as np
from scipy import ndimage, optimize, signal


SAMPLE_RATE = 44_100
ONSET_RATE = SAMPLE_RATE // 4
HOP = 128
BOUNDARY_MARGIN_BPM = 0.20  # Deliberate minimum error allowance, not an expanded pass range.


def ffprobe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)["format"]


def decode(path: Path) -> np.ndarray:
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(SAMPLE_RATE), "-f", "f32le", "pipe:1"],
        check=True, capture_output=True,
    )
    return np.frombuffer(result.stdout, dtype="<f4").copy()


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def finite(number: float | None, digits: int = 5) -> float | None:
    if number is None or not math.isfinite(number):
        return None
    return round(float(number), digits)


def onset_envelopes(audio: np.ndarray) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    reduced = signal.resample_poly(audio, 1, 4)
    freqs, times, spectrum = signal.stft(
        reduced, fs=ONSET_RATE, nperseg=1024, noverlap=1024 - HOP,
        boundary=None, padded=False,
    )
    log_magnitude = np.log1p(np.abs(spectrum) * 50)
    flux = np.maximum(np.diff(log_magnitude, axis=1), 0)
    times = times[1:]
    bands = {
        "low": (freqs >= 35) & (freqs < 250),
        "high": (freqs >= 700) & (freqs < 5000),
        "broad": (freqs >= 35) & (freqs < 5000),
    }
    envelopes = {}
    for name, mask in bands.items():
        values = np.mean(flux[mask], axis=0)
        values = np.maximum(values - ndimage.uniform_filter1d(values, size=87), 0)
        scale = float(np.percentile(values, 99))
        envelopes[name] = values / scale if scale > 1e-8 else values
    envelopes["combined"] = (
        .45 * envelopes["low"] + .45 * envelopes["high"] + .10 * envelopes["broad"]
    )
    return times, envelopes


def spectrum_candidates(
    times: np.ndarray, envelope: np.ndarray, start: float, stop: float,
) -> list[dict]:
    mask = (times >= start) & (times < stop)
    values = envelope[mask]
    if len(values) < 100 or float(np.max(values)) < 1e-8:
        return []
    values = (values - np.mean(values)) * np.hanning(len(values))
    nfft = 1 << (int(len(values) * 8) - 1).bit_length()
    sample_rate = ONSET_RATE / HOP
    spectrum = abs(np.fft.rfft(values, n=nfft))
    frequencies = np.fft.rfftfreq(nfft, 1 / sample_rate)
    lo = np.searchsorted(frequencies, 60 / 60)
    hi = np.searchsorted(frequencies, 220 / 60)
    local, _ = signal.find_peaks(spectrum[lo:hi])
    if not len(local):
        return []
    ranked = local[np.argsort(spectrum[lo + local])[::-1]] + lo
    selected = []
    for index in ranked:
        if any(abs(frequencies[index] - item["frequency"]) < .055 for item in selected):
            continue
        left = frequencies[max(index - 2, lo)]
        right = frequencies[min(index + 2, hi - 1)]
        # Continuous-frequency peak, not the nearest FFT bin.
        sample_times = np.arange(len(values), dtype=np.float64) / sample_rate
        def strength(freq: float) -> float:
            phase = np.exp(-2j * np.pi * freq * sample_times)
            return float(abs(np.dot(values, phase)))
        refined = optimize.minimize_scalar(
            lambda freq: -strength(freq), bounds=(left, right), method="bounded",
            options={"xatol": 1e-8},
        )
        selected.append({
            "frequency": float(refined.x),
            "bpm": float(refined.x * 60),
            "strength": float(-refined.fun),
        })
        if len(selected) == 5:
            break
    selected.sort(key=lambda item: item["strength"], reverse=True)
    maximum = selected[0]["strength"]
    for item in selected:
        item["relative_strength"] = item.pop("strength") / maximum
        item.pop("frequency")
        item["bpm"] = finite(item["bpm"])
        item["relative_strength"] = finite(item["relative_strength"], 4)
    return selected


def tick_fit(ticks: np.ndarray, start: float, stop: float) -> dict:
    selected = ticks[(ticks >= start) & (ticks < stop)]
    if len(selected) < 16:
        return {"bpm": None, "beats": int(len(selected)), "reason": "too_few_ticks"}
    intervals = np.diff(selected)
    base = float(np.median(intervals))
    steps = np.rint(intervals / base).astype(int)
    if np.any(steps < 1):
        return {"bpm": None, "beats": int(len(selected)), "reason": "subdivision_ticks"}
    index = np.r_[0, np.cumsum(steps)]
    slope, intercept = np.polyfit(index, selected, 1)
    residual = selected - (slope * index + intercept)
    coverage = (selected[-1] - selected[0]) / max(stop - start, 1)
    return {
        "bpm": finite(60 / slope),
        "beats": int(len(selected)),
        "median_interval_bpm": finite(60 / base),
        "missed_step_fraction": finite(float(np.sum(steps > 1)) / len(steps), 4),
        "residual_p95_ms": finite(float(np.percentile(abs(residual), 95)) * 1000, 2),
        "coverage": finite(coverage, 4),
    }


def pulse_grid(
    times: np.ndarray, low_envelope: np.ndarray, start: float, stop: float, bpm: float,
) -> dict:
    """Fit observed low-frequency attacks to a tempo grid without inventing beats."""
    mask = (times >= start) & (times < stop)
    local_times = times[mask]
    local_envelope = low_envelope[mask]
    if len(local_times) < 100 or float(np.max(local_envelope)) < .05:
        return {"bpm": None, "coverage": 0, "reason": "weak_low_band"}
    peak_indices, properties = signal.find_peaks(
        local_envelope, distance=round(.23 * ONSET_RATE / HOP), prominence=.11,
    )
    if len(peak_indices) < 12:
        return {"bpm": None, "coverage": 0, "reason": "few_low_attacks"}
    peak_times = local_times[peak_indices]
    amplitudes = properties["prominences"]
    period = 60 / bpm
    phases = np.mod(peak_times[np.argsort(amplitudes)[-40:]], period)
    best = None
    for phase in phases:
        first = phase + math.ceil((start - phase) / period) * period
        expected = np.arange(first, stop, period)
        if len(expected) < 12:
            continue
        right = np.searchsorted(peak_times, expected)
        left = np.clip(right - 1, 0, len(peak_times) - 1)
        right = np.clip(right, 0, len(peak_times) - 1)
        nearest = np.where(
            abs(peak_times[left] - expected) <= abs(peak_times[right] - expected),
            left, right,
        )
        errors = abs(peak_times[nearest] - expected)
        matched = errors < .065
        coverage = float(np.mean(matched))
        strength = float(np.mean(amplitudes[nearest[matched]])) if np.any(matched) else 0
        score = (coverage, strength)
        if best is None or score > best[0]:
            best = (score, expected, nearest, matched)
    if best is None:
        return {"bpm": None, "coverage": 0, "reason": "no_grid"}
    (_, expected, nearest, matched) = best
    beat_numbers = np.flatnonzero(matched)
    attack_times = peak_times[nearest[matched]]
    if len(beat_numbers) < 12:
        return {"bpm": None, "coverage": finite(float(np.mean(matched)), 4),
                "reason": "few_grid_matches"}
    slope, intercept = np.polyfit(beat_numbers, attack_times, 1)
    residual = attack_times - (slope * beat_numbers + intercept)
    return {
        "bpm": finite(60 / slope),
        "coverage": finite(float(np.mean(matched)), 4),
        "matched_attacks": int(len(beat_numbers)),
        "detected_low_attacks": int(len(peak_times)),
        "residual_p95_ms": finite(float(np.percentile(abs(residual), 95)) * 1000, 2),
    }


def intervals(duration: float) -> list[tuple[str, float, float]]:
    window = min(55.0, duration * .78)
    return [
        ("sample", 0.0, duration),
        ("head", 0.0, window),
        ("middle", max(0.0, (duration - window) / 2), min(duration, (duration + window) / 2)),
        ("tail", max(0.0, duration - window), duration),
    ]


def short_intervals(duration: float) -> list[tuple[float, float]]:
    """Overlapping eight-second checks cover the entire recording without gaps."""
    length = 8.0
    starts = list(np.arange(0, max(0, duration - length) + 1e-6, 4.0))
    starts.append(max(0.0, duration - length))
    return [(float(start), float(min(duration, start + length)))
            for start in sorted(set(starts))]


def analyze_audio(audio: np.ndarray, candidate_id: str, source: dict) -> dict:
    duration = len(audio) / SAMPLE_RATE
    report = {
        "candidate_id": candidate_id,
        "source": source,
        "duration_seconds": finite(duration, 3),
        "methods": {
            "essentia": "RhythmExtractor2013 multifeature; broad tempo 60-220",
            "independent": "SciPy multi-band spectral-flux continuous-frequency peaks",
            "local_change_check": "Overlapping 8-second low-attack beat grids, 4-second stride",
            "boundary_margin_bpm": BOUNDARY_MARGIN_BPM,
            "note": "Margin is uncertainty allowance, not an extended acceptable BPM range.",
            "scope": "Observed audio sample only; no unobserved-song tempo guarantee.",
        },
    }
    if duration < 30 or not np.all(np.isfinite(audio)):
        report.update({"classification": "uncertain", "reasons": ["short_or_nonfinite_audio"]})
        return report
    one_second = SAMPLE_RATE
    chunks = [audio[i:i + one_second] for i in range(0, len(audio), one_second)]
    silent = [float(np.sqrt(np.mean(c * c))) < 1e-4 for c in chunks]
    report["silence_fraction"] = finite(sum(silent) / len(silent), 4)
    report["rms"] = finite(float(np.sqrt(np.mean(audio * audio))), 7)
    if report["silence_fraction"] > .15 or report["rms"] < 1e-5:
        report.update({"classification": "uncertain", "reasons": ["silence_or_weak_audio"]})
        return report
    tracker = es.RhythmExtractor2013(method="multifeature", minTempo=60, maxTempo=220)
    reported_bpm, beat_ticks, confidence, _, _ = tracker(audio.astype("float32"))
    ticks = np.array(beat_ticks, dtype=float)
    report["essentia_version"] = essentia.__version__
    report["tracker_reported_bpm"] = finite(float(reported_bpm))
    report["tracker_confidence"] = finite(float(confidence))
    times, envelopes = onset_envelopes(audio)
    report["windows"] = []
    for name, start, stop in intervals(duration):
        peaks = spectrum_candidates(times, envelopes["combined"], start, stop)
        low = spectrum_candidates(times, envelopes["low"], start, stop)
        high = spectrum_candidates(times, envelopes["high"], start, stop)
        pulse = pulse_grid(times, envelopes["low"], start, stop, peaks[0]["bpm"]) if peaks else None
        report["windows"].append({
            "name": name, "start_seconds": finite(start, 3), "stop_seconds": finite(stop, 3),
            "tick_fit": tick_fit(ticks, start, stop),
            "combined_peaks": peaks,
            "low_peaks": low[:3], "high_peaks": high[:3],
            "low_attack_grid": pulse,
        })
    full_peaks = report["windows"][0]["combined_peaks"]
    reference_bpm = full_peaks[0]["bpm"] if full_peaks else None
    report["short_windows"] = []
    if reference_bpm is not None:
        for start, stop in short_intervals(duration):
            report["short_windows"].append({
                "start_seconds": finite(start, 3), "stop_seconds": finite(stop, 3),
                "low_attack_grid": pulse_grid(
                    times, envelopes["low"], start, stop, reference_bpm,
                ),
            })
    report.update(classify(report))
    return report


def classify(report: dict) -> dict:
    reasons = []
    values = []
    local_values = []
    for index, window in enumerate(report["short_windows"]):
        pulse = window["low_attack_grid"]
        if pulse["bpm"] is None:
            reasons.append(f"short_{index}:missing_local_pulse")
        elif pulse["coverage"] < .80 or pulse["residual_p95_ms"] > 35:
            reasons.append(f"short_{index}:local_tempo_change_or_weak_pulse")
        else:
            local_values.append(pulse["bpm"])
    for window in report["windows"]:
        tick = window["tick_fit"]
        peaks = window["combined_peaks"]
        pulse = window["low_attack_grid"]
        if tick["bpm"] is None or not peaks or pulse is None or pulse["bpm"] is None:
            reasons.append(f"{window['name']}:missing_method")
            continue
        if tick.get("missed_step_fraction", 1) > .08 or tick.get("residual_p95_ms", 1000) > 35:
            reasons.append(f"{window['name']}:unstable_beat_grid")
        if tick.get("coverage", 0) < .65:
            reasons.append(f"{window['name']}:weak_beat_coverage")
        spectral = peaks[0]["bpm"]
        if pulse["coverage"] < .80 or pulse["residual_p95_ms"] > 35:
            reasons.append(f"{window['name']}:weak_full_speed_pulse")
        if abs(spectral - pulse["bpm"]) > .35:
            reasons.append(f"{window['name']}:spectral_pulse_disagreement")
        # A tracker at exactly half-time is not itself evidence for full time.
        # Only dense observed low attacks and their independent grid fit may resolve it.
        tracker_half = abs(2 * tick["bpm"] - spectral) <= .35
        if not tracker_half and abs(spectral - tick["bpm"]) > .35:
            reasons.append(f"{window['name']}:tracker_disagreement")
        values.extend((pulse["bpm"], spectral))
        if not tracker_half:
            values.append(tick["bpm"])
        for other in peaks[1:]:
            if other["relative_strength"] >= .75 and (
                abs(other["bpm"] * 2 - spectral) < 1 or
                abs(other["bpm"] - 2 * spectral) < 1
            ):
                reasons.append(f"{window['name']}:half_double_ambiguity")
                break
    if len(values) < 8:
        reasons.append("incomplete_sample_evidence")
    values.extend(local_values)
    if values:
        span = max(values) - min(values)
        lower = min(values) - BOUNDARY_MARGIN_BPM
        upper = max(values) + BOUNDARY_MARGIN_BPM
        report_interval = {"lower": finite(lower), "upper": finite(upper)}
        if span > .55:
            reasons.append("tempo_drift_or_disagreement")
    else:
        report_interval = None
    if reasons:
        classification = "uncertain"
    elif report_interval["lower"] >= 175 and report_interval["upper"] <= 177:
        classification = "inside"
    elif report_interval["upper"] < 175 or report_interval["lower"] > 177:
        classification = "out"
    else:
        classification = "uncertain"
        reasons.append("boundary_interval_overlap")
    return {"classification": classification, "reasons": sorted(set(reasons)),
            "conservative_bpm_interval": report_interval}


def synth(bpm: float, seconds: int = 70, style: str = "click", drift: bool = False) -> np.ndarray:
    rng = np.random.default_rng(33)
    audio = np.zeros(seconds * SAMPLE_RATE, dtype=np.float32)
    t = .25
    beat = 0
    while t < seconds - .2:
        instant_bpm = bpm + (8 * t / seconds if drift else 0)
        index = round(t * SAMPLE_RATE)
        n = 3000
        local = np.arange(n) / SAMPLE_RATE
        kick = (.6 * np.sin(2 * np.pi * (60 * local - 30 * local * local))
                * np.exp(-local * 45))
        click = .25 * np.exp(-local * 600)
        audio[index:index + n] += (kick + click).astype(np.float32)
        if style in ("rock", "breakbeat"):
            # Backbeat and syncopation can make half/double-time interpretations attractive.
            if beat % 4 in (1, 3):
                noise = rng.normal(0, 1, n) * np.exp(-local * 25) * .22
                audio[index:index + n] += noise.astype(np.float32)
            if style == "breakbeat" and beat % 4 in (0, 2):
                offset = round(.37 * (60 / instant_bpm) * SAMPLE_RATE)
                if index + offset + n <= len(audio):
                    audio[index + offset:index + offset + n] += (
                        rng.normal(0, 1, n) * np.exp(-local * 60) * .13
                    ).astype(np.float32)
            for subdivision in (0.5,):
                hat_index = index + round(subdivision * (60 / instant_bpm) * SAMPLE_RATE)
                if hat_index + n <= len(audio):
                    audio[hat_index:hat_index + n] += (
                        rng.normal(0, 1, n) * np.exp(-local * 130) * .045
                    ).astype(np.float32)
        beat += 1
        t += 60 / instant_bpm
    return audio


def self_test() -> dict:
    cases = [(str(bpm), synth(bpm)) for bpm in
             (174.5, 175, 176, 177, 177.5, 160, 180, 87.5)]
    cases += [("rock_176", synth(176, 80, "rock")),
              ("breakbeat_176", synth(176, 80, "breakbeat")),
              ("drift_175_to_183", synth(175, 90, "rock", drift=True)),
              ("silence", np.zeros(70 * SAMPLE_RATE, dtype=np.float32))]
    results = []
    expected = {
        "174.5": "out", "175": "uncertain", "176": "inside",
        "177": "uncertain", "177.5": "out", "160": "out",
        "180": "out", "87.5": "uncertain", "rock_176": "inside",
        "breakbeat_176": "inside", "drift_175_to_183": "uncertain",
        "silence": "uncertain",
    }
    for name, audio in cases:
        result = analyze_audio(audio, name, {"kind": "synthetic", "sha256": None})
        results.append(result)
        print(f"{name}: {result['classification']} {result.get('conservative_bpm_interval')} {result['reasons']}",
              file=sys.stderr)
        if result["classification"] != expected[name]:
            raise AssertionError(
                f"{name}: expected {expected[name]}, got {result['classification']}"
            )
    return {"fixture_count": len(results), "assertions_passed": len(results),
            "expected": expected, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", nargs="?", type=Path)
    parser.add_argument("--candidate-id")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        if args.audio is None or args.candidate_id is None:
            parser.error("audio and --candidate-id are required outside --self-test")
        if not args.audio.is_file():
            parser.error(f"audio file does not exist: {args.audio}")
        probe = ffprobe(args.audio)
        result = analyze_audio(
            decode(args.audio), args.candidate_id,
            {"kind": "recording", "path": str(args.audio), "sha256": digest(args.audio),
             "ffprobe_duration_seconds": finite(float(probe["duration"]), 3)},
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
