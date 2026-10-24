#!/usr/bin/env python3
"""Measure reacquired 07:00 sources; estimates are not listener approval.

Uses the multiband attack envelopes established by continuous_mix_0630.py.
The quarter-note path is guided by local autocorrelation rather than a prompt
BPM. Source attack times remain estimates and require output/listening checks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from scipy import ndimage, signal
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT / 'SERIES/07-00'
ENV_RATE = 500
BANDS = {'low': (30, 180), 'mid': (180, 1800), 'high': (1800, 7000)}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def envelopes(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(path),
                                   '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'])
    mono = np.frombuffer(raw, dtype='<f4').astype(float)
    result = {}
    for name, limits in BANDS.items():
        y = signal.sosfiltfilt(signal.butter(4, limits, btype='bandpass', fs=16000, output='sos'), mono)
        e = np.sqrt(np.mean(y[:len(y)//32*32].reshape(-1, 32)**2, axis=1))
        e = ndimage.gaussian_filter1d(e, 1.5)
        attack = np.maximum(e - np.roll(e, 3), 0)
        attack[:3] = 0
        result[name] = attack
    return result


def local_tempos(envs):
    duration = min(map(len, envs.values())) / ENV_RATE
    windows = []
    # A running pulse near the selected sources' known range. This is not a
    # universal BPM detector: ambiguous and out-of-range sources must be flagged.
    lags = np.arange(int(ENV_RATE*60/220), int(ENV_RATE*60/145)+1)
    for center in np.arange(10, duration-5, 5):
        start = max(0, center-10)
        end = min(duration, center+10)
        estimates = []
        strengths = []
        for name, env in envs.items():
            x = env[round(start*ENV_RATE):round(end*ENV_RATE)]
            ac = signal.correlate(x, x, mode='full', method='fft')[len(x)-1:]
            ac /= np.maximum(1, len(x)-np.arange(len(x)))
            ac = ndimage.gaussian_filter1d(ac, 1)
            values = ac[lags] + .5*ac[2*lags] + .25*ac[4*lags]
            k = int(np.argmax(values))
            frac = 0.
            if 0 < k < len(values)-1:
                den = values[k-1] - 2*values[k] + values[k+1]
                if den < 0:
                    frac = float(np.clip(.5*(values[k-1]-values[k+1])/den, -.5, .5))
            estimates.append(float(60*ENV_RATE/(lags[k]+frac)))
            strengths.append(float(values[k]/max(ac[0], 1e-20)))
        windows.append({'center_seconds': float(center),
                        'band_bpm': dict(zip(envs, estimates)),
                        'band_strength': dict(zip(envs, strengths)),
                        'median_bpm': float(np.median(estimates)),
                        'band_spread_bpm': float(np.ptp(estimates))})
    assert windows, 'Source too short to measure'
    return windows


def quarter_path(envs, windows):
    combined = sum(e / max(np.percentile(e, 98), 1e-20) for e in envs.values()) / len(envs)
    combined = np.minimum(combined, 3)
    # Suppress isolated noisy estimates without flattening gradual source drift.
    centers = np.array([w['center_seconds'] for w in windows])
    bpms = ndimage.median_filter(np.array([w['median_bpm'] for w in windows]), size=3)
    bpm_t = np.interp(np.arange(len(combined))/ENV_RATE, centers, bpms)
    period = ENV_RATE*60/bpm_t
    cumulative = np.zeros(len(combined))
    backlink = np.full(len(combined), -1, dtype=np.int32)
    for t in range(len(combined)):
        nominal = period[t]
        lag = np.arange(max(1, round(nominal*.88)), round(nominal*1.12)+1)
        previous = t-lag
        valid = previous >= 0
        if not valid.any():
            cumulative[t] = combined[t]
            continue
        previous, lag = previous[valid], lag[valid]
        reward = cumulative[previous] - 180*np.log(lag/nominal)**2
        best = int(np.argmax(reward))
        cumulative[t] = combined[t] + reward[best]
        backlink[t] = previous[best]
    energy = ndimage.uniform_filter1d(combined, size=ENV_RATE)
    active = np.flatnonzero(energy > .07*np.percentile(energy, 95))
    assert len(active), 'No measurable attacks'
    last = int(active[-1])
    endpoint = max(0, last-round(period[last])) + int(np.argmax(cumulative[max(0, last-round(period[last])):last+1]))
    beats = []
    while endpoint >= 0:
        beats.append(endpoint/ENV_RATE)
        endpoint = int(backlink[endpoint])
    beats = np.array(beats[::-1])
    beats = beats[(beats >= active[0]/ENV_RATE-.1) & (beats <= active[-1]/ENV_RATE+.1)]
    assert len(beats) > 64, 'Insufficient beat path'
    # Per-beat locations contain groove and envelope latency. Do not call them
    # exact downbeats or silently quantize the original performance here.
    return beats, combined


def analyze(track):
    src = SERIES/'input/tracks'/track['input_filename']
    assert sha(src) == track['sha256'], 'Reacquired source identity changed'
    envs = envelopes(src)
    windows = local_tempos(envs)
    beats, combined = quarter_path(envs, windows)
    intervals = np.diff(beats)
    result = {'schema': 'wavvy.tempo_analysis.v1', 'order': track['order'],
              'title': track['approved_title'], 'candidate_id': track['candidate_id'],
              'source_path': str(src.relative_to(ROOT)), 'source_sha256': track['sha256'],
              'target_bpm': 180, 'measurement': 'multiband autocorrelation plus guided quarter-note path',
              'status': 'exploratory_requires_output_and_listening_validation',
              'windows': windows, 'quarter_beat_seconds': beats.tolist(),
              'quarter_interval_bpm_p10_p50_p90': (60/np.quantile(intervals, [.9, .5, .1])).tolist(),
              'estimated_beat_count': len(beats),
              'maximum_band_disagreement_bpm': max(w['band_spread_bpm'] for w in windows),
              'limitations': ['Beat phase and bar downbeats are not listener-confirmed.',
                             'A 145–220 BPM search range is a source-specific pulse prior, not a measured guarantee.',
                             'Sparse intros, fills and tails require separate treatment.']}
    out = SERIES/'production/tempo-analysis-20261024'/f'{track["order"]:02d}.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['order','title','estimated_beat_count',
          'quarter_interval_bpm_p10_p50_p90','maximum_band_disagreement_bpm']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--orders', type=int, nargs='+', required=True)
    args = parser.parse_args()
    records = json.loads((SERIES/'production/reacquisition-20261024.json').read_text())['tracks']
    for order in args.orders:
        track = next(t for t in records if t['order'] == order)
        analyze(track)
