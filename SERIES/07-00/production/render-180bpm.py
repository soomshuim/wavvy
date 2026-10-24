#!/usr/bin/env python3
"""Pitch-preserving local tempo correction for the approved 07:00 sources.

Adapted from continuous_mix_0630.py's guarded static-atempo and independent
waveform-anchor alignment. No 06:30 acceptance exceptions are inherited.
Only explicitly requested orders are rendered; source files are never changed.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import warnings

import numpy as np
from scipy import signal
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[3]
SERIES = ROOT/'SERIES/07-00'
SR = 48000
TARGET = 180
BLOCK_BEATS = 16
GUARD = .4
SEAM = .012
WORK = ROOT/'work/0700-remaster-20261024'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def read(path):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', wavfile.WavFileWarning)
        rate, audio = wavfile.read(path, mmap=True)
    assert rate == SR and audio.ndim == 2 and audio.shape[1] == 2
    return audio


def waveform_matches(source, raw, source_seconds, predicted):
    # A short original waveform is corroborating evidence independent of the
    # onset envelope and corrects atempo's signal-dependent temporal offset.
    # Long templates can cross atempo's overlap splice. Three shorter windows
    # must independently match strongly and agree in location; do not lower the
    # correlation threshold to accept a changed waveform across that splice.
    found = []
    for milliseconds in (8, 12, 16):
        half = milliseconds/2000
        a = max(0, round((source_seconds-half)*SR))
        b = min(len(source), round((source_seconds+half)*SR))
        template = source[a:b]
        origin = round((predicted-half)*SR)
        lo = max(0, origin-round(.08*SR))
        hi = min(len(raw), origin+len(template)+round(.08*SR))
        observed = raw[lo:hi]
        assert len(observed) >= len(template)
        cc = signal.correlate(observed, template, mode='valid', method='fft')
        norm = np.sqrt(np.convolve(observed*observed, np.ones(len(template)), mode='valid'))*np.linalg.norm(template)
        scores = cc/(norm+1e-30)
        k = int(np.argmax(scores))
        value = float(scores[k])
        found.append(((lo+k+round(source_seconds*SR)-a)/SR, value))
    return found


def locate(source, raw, source_seconds, predicted, matching_cache):
    source_mono = matching_cache['mono']
    raw_mono = raw.astype(float).mean(axis=1)
    found = waveform_matches(source_mono, raw_mono, source_seconds, predicted)
    assert min(x[1] for x in found) > .9, ('Unreliable source-waveform anchor', source_seconds, found)
    positions = [x[0] for x in found]
    evidence = {'method': 'full-band', 'positions_and_correlations': found}
    if np.ptp(positions) >= .0015:
        # A periodic bass waveform can have two nearly identical peaks several
        # milliseconds apart. Measure the same audio above 300 Hz to resolve
        # that alias. This affects matching only, never the rendered audio.
        sos = signal.butter(4, 300, btype='highpass', fs=SR, output='sos')
        if 'highpass_300' not in matching_cache:
            matching_cache['highpass_300'] = signal.sosfiltfilt(sos, source_mono)
        filtered_raw = signal.sosfiltfilt(sos, raw_mono)
        corroborated = waveform_matches(matching_cache['highpass_300'], filtered_raw,
                                        source_seconds, predicted)
        assert min(x[1] for x in corroborated) > .9, ('Unreliable high-pass anchor', source_seconds, corroborated)
        evidence = {'method': 'highpass-300Hz-corroboration',
                    'full_band_positions_and_correlations': found,
                    'positions_and_correlations': corroborated}
        found = corroborated
        positions = [x[0] for x in found]
    assert np.ptp(positions) < .0015, ('Inconsistent waveform locations', source_seconds, found)
    return float(np.median(positions)), min(x[1] for x in found), evidence


def render(order):
    analysis_path = SERIES/'production/tempo-analysis-20261024'/f'{order:02d}.json'
    a = json.loads(analysis_path.read_text())
    source_path = ROOT/a['source_path']
    assert sha(source_path) == a['source_sha256']
    source = read(source_path)
    assert source.dtype == np.int16
    matching_cache = {'mono': source.astype(float).mean(axis=1)}
    duration = len(source)/SR
    beats = np.asarray(a['quarter_beat_seconds'])
    indices = list(range(0, len(beats)-1, BLOCK_BEATS))
    if indices[-1] != len(beats)-1:
        indices.append(len(beats)-1)
    anchors = beats[indices]
    first_ratio = (anchors[1]-anchors[0])/((indices[1]-indices[0])*60/TARGET)
    first_target = anchors[0]/first_ratio
    target = first_target+np.asarray(indices)*60/TARGET
    estimated_total = target[-1]+(duration-anchors[-1])/first_ratio
    output = np.zeros((round((estimated_total+5)*SR), 2), dtype=np.float32)
    weight = np.zeros(len(output), dtype=np.float32)
    folder = WORK/f'track-{order:02d}'
    folder.mkdir(parents=True, exist_ok=True)
    blocks = []
    actual_end = 0
    for k, (sa, sb, ta, tb) in enumerate(zip(anchors[:-1], anchors[1:], target[:-1], target[1:])):
        ratio = float((sb-sa)/(tb-ta))
        ca = 0 if k == 0 else max(0, round((sa-GUARD)*SR))
        cb = len(source) if k == len(anchors)-2 else min(len(source), round((sb+GUARD)*SR))
        raw_path = folder/f'block-{k:03d}.wav'
        cmd = ['ffmpeg', '-hide_banner', '-v', 'error', '-nostdin', '-n', '-i', str(source_path),
               '-af', f'atrim=start_sample={ca}:end_sample={cb},asetpts=PTS-STARTPTS,atempo={ratio:.16f},asetpts=N/SR/TB',
               '-c:a', 'pcm_f32le', str(raw_path)]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr
        raw = read(raw_path)
        located_a, cc_a, evidence_a = locate(source, raw, float(sa), (sa-ca/SR)/ratio, matching_cache)
        located_b, cc_b, evidence_b = locate(source, raw, float(sb), (sb-ca/SR)/ratio, matching_cache)
        offset = round(ta*SR)-round(located_a*SR)
        end_error = located_b-located_a-(tb-ta)
        # A fail here is visible; no source-specific listening exception exists.
        assert abs(end_error) < .020, ('Block end error exceeds 20ms', order, k, end_error)
        left = 0 if k == 0 else round((ta-SEAM)*SR)
        right = offset+len(raw) if k == len(anchors)-2 else round((tb+SEAM)*SR)
        left = max(left, offset, 0)
        right = min(right, offset+len(raw), len(output))
        assert right > left
        t = np.arange(left, right)/SR
        w = np.ones(right-left)
        if k:
            phase = np.clip((t-(ta-SEAM))/(2*SEAM), 0, 1)
            w *= .5-.5*np.cos(np.pi*phase)
        if k < len(anchors)-2:
            phase = np.clip((t-(tb-SEAM))/(2*SEAM), 0, 1)
            w *= .5+.5*np.cos(np.pi*phase)
        output[left:right] += np.asarray(raw[left-offset:right-offset])*w[:, None]
        weight[left:right] += w
        actual_end = max(actual_end, right)
        blocks.append({'block': k, 'source_beat_indices': indices[k:k+2],
                       'source_anchors_seconds': [float(sa), float(sb)],
                       'target_anchors_seconds': [float(ta), float(tb)], 'tempo_factor': ratio,
                       'source_guard_samples': [ca, cb], 'output_offset_samples': offset,
                       'observed_raw_anchors_seconds': [located_a, located_b],
                       'waveform_correlations': [cc_a, cc_b],
                       'waveform_anchor_evidence': [evidence_a, evidence_b],
                       'observed_end_error_ms': end_error*1000,
                       'raw_sha256': sha(raw_path), 'ffmpeg_command': cmd})
        del raw
        # Only this run's own intermediate block is disposable; retain identity
        # and command in the producer record rather than hundreds of WAV copies.
        raw_path.unlink()
    output = output[:actual_end]
    weight = weight[:actual_end]
    covered = np.flatnonzero(weight > .01)
    assert len(covered) and covered[0] < .03*SR
    assert np.min(weight[covered[0]:]) > .99, 'Uncovered interior audio'
    output[covered[0]:] /= weight[covered[0]:, None]
    assert np.isfinite(output).all()
    peak = float(np.max(np.abs(output)))
    assert peak < 1.02, ('Unexpected peak', peak)
    destination = SERIES/'input/processed-180'/f'{order:02d}__{a["title"]}__180.wav'
    destination.parent.mkdir(exist_ok=True)
    assert not destination.exists(), f'Refusing to replace {destination}'
    wavfile.write(destination, SR, output)
    spec = importlib.util.spec_from_file_location('tempo_measure_0700', SERIES/'production/analyze-180bpm.py')
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    output_windows = measure.local_tempos(measure.envelopes(destination))
    values = np.array([w['median_bpm'] for w in output_windows])
    result = {'schema': 'wavvy.tempo_corrected_source.v1', 'order': order, 'title': a['title'],
              'candidate_id': a['candidate_id'], 'source_path': a['source_path'], 'source_sha256': a['source_sha256'],
              'analysis_path': str(analysis_path.relative_to(ROOT)), 'analysis_sha256': sha(analysis_path),
              'target_bpm': TARGET, 'block_quarter_beats': BLOCK_BEATS, 'guard_seconds': GUARD,
              'producer_script_sha256': sha(Path(__file__)),
              'internal_crossfade_seconds': SEAM*2, 'pitch_processing': 'FFmpeg static atempo, no pitch/resample rate change',
              'output_path': str(destination.relative_to(ROOT)), 'output_sha256': sha(destination),
              'source_duration_seconds': duration, 'output_duration_seconds': len(output)/SR,
              'output_peak_linear': peak, 'first_grid_beat_output_seconds': first_target,
              'grid_beat_count': len(beats), 'output_windows': output_windows,
              'output_window_bpm_p05_p50_p95': np.quantile(values, [.05, .5, .95]).tolist(),
              'leading_alignment_padding_samples': int(covered[0]), 'blocks': blocks,
              'status': 'prototype_requires_validation_and_listening',
              'listener_approved': False}
    record = SERIES/'production/tempo-corrected-20261024'/f'{order:02d}.json'
    record.parent.mkdir(exist_ok=True)
    record.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['order','title','output_duration_seconds',
                                          'output_window_bpm_p05_p50_p95','output_peak_linear']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--orders', type=int, nargs='+', required=True)
    args = parser.parse_args()
    for order in args.orders:
        render(order)
