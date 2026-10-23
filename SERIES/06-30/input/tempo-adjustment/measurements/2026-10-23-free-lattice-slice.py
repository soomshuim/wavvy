#!/usr/bin/env python3
"""Run the existing independent onset/lattice method on a chosen WAV slice.

Adapted from input/bpm-audit/validation/independent-review-remaining.py.
No target BPM is accepted or used for seed selection.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import ndimage, optimize, signal
from scipy.io import wavfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acpeaks(z, rate):
    z = z - z.mean()
    variance = np.var(z)
    if variance <= 0:
        return []
    ac = signal.correlate(z, z, mode="full", method="fft")[len(z)-1:]
    ac = ac / (np.arange(len(z), 0, -1) * variance)
    lo, hi = int(rate * .17), min(int(rate * 1.5), len(z)-1)
    idx, _ = signal.find_peaks(ac[lo:hi], distance=max(1, int(rate * .025)))
    idx = sorted(idx+lo, key=lambda k: ac[k], reverse=True)[:7]
    ans = []
    for k in idx:
        den = ac[k-1] - 2*ac[k] + ac[k+1]
        frac = .5*(ac[k-1]-ac[k+1])/den if den else 0
        ans.append([round(60*rate/(k+frac), 3), round(float(ac[k]), 4)])
    return ans


def spectrum(z, rate):
    z = z-z.mean()
    nfft = 131072
    power = abs(np.fft.rfft(z*np.hanning(len(z)), n=nfft))**2
    if power.max() <= 0:
        return []
    freqs = np.fft.rfftfreq(nfft, 1/rate)
    ix, _ = signal.find_peaks(power)
    ix = sorted([i for i in ix if .7 <= freqs[i] <= 8], key=lambda i: power[i], reverse=True)[:5]
    return [[round(freqs[i]*60, 3), round(float(power[i]/power.max()), 4)] for i in ix]


def measure(audio, sample_rate):
    x = audio.mean(axis=1) if audio.ndim > 1 else audio
    resampled = signal.resample_poly(x, 16000, sample_rate)
    bands = {}
    for name, band in (("low", (30, 180)), ("mid", (180, 1800)), ("high", (1800, 7000))):
        y = signal.sosfiltfilt(signal.butter(4, band, btype="bandpass", fs=16000, output="sos"), resampled)
        env = np.sqrt(np.mean(y[:len(y)//32*32].reshape(-1, 32)**2, axis=1))
        env = ndimage.gaussian_filter1d(env, 1.5)
        onset = np.maximum(env - np.roll(env, 3), 0)
        onset[:3] = 0
        onset /= np.percentile(onset, 99)+1e-12
        onset = np.minimum(onset, 3)
        peaks, _ = signal.find_peaks(onset, distance=60, prominence=.15)
        bands[name] = {
            "ac_full": acpeaks(onset, 500),
            "ac_parts": [acpeaks(part, 500)[:3] for part in np.array_split(onset, 3)],
            "spectrum_full": spectrum(onset, 500),
            "events_s": np.round(peaks/500, 3).tolist(),
            "event_strengths": np.round(onset[peaks], 2).tolist(),
        }
    seeds = []
    for name in ("high", "mid", "low"):
        values = bands[name]
        for bpm, _ in values["ac_full"][:4] + values["spectrum_full"][:1]:
            if not any(abs(bpm/known-1) < .012 for known in seeds):
                seeds.append(bpm)
    fits = []
    for seed in sorted(seeds):
        for name, values in bands.items():
            times = np.array(values["events_s"])
            weights = np.minimum(np.array(values["event_strengths"]), 1.5)
            if len(times) < 10 or not weights.sum():
                continue
            frequency = seed/60
            def coherence(f):
                return abs(np.sum(weights*np.exp(2j*np.pi*f*times)))/sum(weights)
            grid = np.linspace(frequency*.985, frequency*1.015, 101)
            initial = grid[np.argmax([coherence(f) for f in grid])]
            optimum = optimize.minimize_scalar(lambda f: -coherence(f), bounds=(initial-frequency*.0005, initial+frequency*.0005), method="bounded")
            fitted_frequency = optimum.x
            period = 1/fitted_frequency
            phase = np.angle(np.sum(weights*np.exp(2j*np.pi*fitted_frequency*times)))/(2*np.pi*fitted_frequency)
            numbers = np.round((times-phase)/period)
            good = abs(times-(phase+numbers*period)) < min(.035, period*.12)
            tt, nn, ww = times[good], numbers[good], weights[good]
            if len(tt) < 10:
                continue
            slope, intercept = np.polyfit(nn, tt, 1, w=np.sqrt(ww))
            chunks = []
            for start, stop in ((0, 10), (10, 20), (20, 30)):
                selected = (tt >= start) & (tt < stop)
                if sum(selected) > 6 and np.ptp(nn[selected]) > 3:
                    local_slope, _ = np.polyfit(nn[selected], tt[selected], 1, w=np.sqrt(ww[selected]))
                    chunks.append(round(60/local_slope, 3))
            if coherence(fitted_frequency) > .23:
                fits.append({
                    "seed": seed, "band": name, "bpm_fit": round(60/slope, 3),
                    "coherence": round(coherence(fitted_frequency), 3),
                    "inlier_count": len(tt), "span_s": round(float(np.ptp(tt)), 3),
                    "observed_10s_estimates": chunks,
                    "residual_p90_ms": round(float(np.quantile(abs(tt-(intercept+slope*nn)), .9)*1000), 2),
                    "first_actual_events_s": tt[:8].tolist(), "last_actual_events_s": tt[-5:].tolist(),
                })
    return {"measurements": bands, "lattice_fits": fits}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rate, samples = wavfile.read(args.audio, mmap=True)
    channels = 1 if samples.ndim == 1 else samples.shape[1]
    start = round(args.start*rate)
    stop = start+30*rate
    if start < 0 or stop > len(samples):
        raise ValueError("source does not contain the requested 30-second slice")
    data = samples[start:stop].astype(np.float64)
    if samples.dtype.kind in "iu":
        data /= np.iinfo(samples.dtype).max
    if not np.isfinite(data).all() or np.max(np.abs(data)) == 0:
        raise ValueError("nonfinite or silent source slice")
    result = {
        "scope": "free onset/lattice measurement of exactly one 30-second slice; not whole-song approval",
        "path": str(args.audio), "sha256": sha(args.audio),
        "sample_rate_hz": rate, "channels": channels,
        "full_file_duration_s": len(samples)/rate, "slice_start_s": args.start,
        "slice_duration_s": 30.0, "method_source": "SERIES/06-30/input/bpm-audit/validation/independent-review-remaining.py",
        **measure(data, rate),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "fits": len(result["lattice_fits"])}))


if __name__ == "__main__":
    main()
