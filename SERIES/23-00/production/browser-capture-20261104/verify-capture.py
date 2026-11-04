#!/usr/bin/env python3
"""Verify one new closed capture; preserve raw audio and export a guarded range.

UI/media-clock to ScreenCaptureKit PTS alignment follows the 19:30 precedent.
Output latency is not calibrated. Retain 0.5 s before and 0.75 s after the
estimated source range; this is collection evidence, not a final edit or a
listener's musical-quality approval.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import warnings

import numpy as np
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parents[4]
PRODUCTION = Path(__file__).resolve().parent
WORK = ROOT / 'work/2026-11-04-2300-browser-capture'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('song_id')
    p.add_argument('--attempt', type=int, default=1)
    a = p.parse_args()
    row = next(r for r in read(PRODUCTION / 'source-catalog.json')['rows'] if r['song_id'] == a.song_id)
    folder = WORK / 'captures' / a.song_id / f'attempt-{a.attempt:02d}'
    metadata = read(folder / 'capture.json')
    assert metadata['status'] == 'capture_closed_unverified', metadata['status']
    timeline_path = PRODUCTION / 'browser-timelines' / f'{a.song_id}-attempt-{a.attempt:02d}.json'
    timeline = read(timeline_path)
    assert timeline['song_id'] == a.song_id and timeline['title'] == row['name']
    assert timeline['url'].split('?')[0] == row['url']
    assert timeline['done'] and timeline['ended_event']['ended']
    assert not timeline.get('unexpected_navigation', False)
    events = timeline['events']
    playing = next(e for e in events if e['type'] == 'playing')
    ended = timeline['ended_event']
    assert not any(e['type'] in {'error', 'ratechange', 'seeking'} and playing['unix_ms'] <= e['unix_ms'] < ended['unix_ms'] for e in events)
    assert not any(e['type'] == 'playing' and e['unix_ms'] > ended['unix_ms'] for e in events), 'Next song began output after natural end'
    duration = float(timeline['duration'])
    assert playing['currentTime'] < 0.25 and abs(ended['currentTime'] - duration) < 0.05
    active = [s for s in timeline['samples'] if not s['paused'] and 1 < s['currentTime'] < duration - 1]
    assert len(active) > duration, 'Insufficient browser clock samples'
    assert all(s['playbackRate'] == 1 and not s['muted'] and s['volume'] > 0 for s in active)
    assert not any(e['type'] in {'pause', 'waiting', 'stalled'} and not e['ended'] and playing['unix_ms'] < e['unix_ms'] < ended['unix_ms'] for e in events)
    wall_duration = (ended['performance_ms'] - playing['performance_ms']) / 1000
    assert abs(wall_duration - (duration - playing['currentTime'])) < 1.0, wall_duration
    raw = folder / 'raw.wav'
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', wavfile.WavFileWarning)
        rate, signal = wavfile.read(raw, mmap=True)
    assert rate == 48000 and signal.dtype == np.float32 and signal.ndim == 2 and signal.shape[1] == 2
    assert np.isfinite(signal).all()
    buffers = read(Path(str(raw) + '.timing.json'))['buffers']
    offsets = np.asarray([b['frame_offset'] for b in buffers])
    frames = np.asarray([b['frames'] for b in buffers])
    pts = np.asarray([b['pts_seconds'] for b in buffers])
    gaps = np.diff(pts) - frames[:-1] / rate
    assert frames.sum() == len(signal) and not np.any(np.diff(offsets) - frames[:-1])
    epoch_minus_uptime = float(np.median([b['callback_unix_seconds'] - b['callback_uptime_seconds'] for b in buffers]))
    raw_epoch = float(pts[0] + epoch_minus_uptime)
    origins = np.asarray([s['unix_ms'] / 1000 - s['currentTime'] for s in active])
    origin = float(np.median(origins))
    origin_spread = float(np.ptp(np.quantile(origins, [.01, .99])))
    assert origin_spread < 0.25, 'Unstable browser/source time alignment'
    source_pts_start = origin - epoch_minus_uptime
    source_pts_end = source_pts_start + duration
    discontinuities = []
    for i in np.flatnonzero(np.abs(gaps) > 1 / rate):
        previous_end = float(pts[i] + frames[i] / rate)
        following_start = float(pts[i + 1])
        assert max(previous_end, following_start) < source_pts_start or min(previous_end, following_start) > source_pts_end, 'Audio-buffer PTS discontinuity inside source playback'
        discontinuities.append({'buffer_after': int(i), 'gap_seconds': float(gaps[i]), 'relative_to_source_seconds': [previous_end - source_pts_start, following_start - source_pts_start], 'scope': 'outside_source_playback'})
    def frame_at_pts(value):
        index = int(np.searchsorted(pts, value, side='right') - 1)
        assert 0 <= index < len(buffers) and 0 <= value - pts[index] <= frames[index] / rate + 1 / rate, 'Source boundary falls outside captured PTS coverage'
        return int(offsets[index] + round((value - pts[index]) * rate))
    source_start_frame = frame_at_pts(source_pts_start)
    source_end_frame = frame_at_pts(source_pts_end)
    assert abs((source_end_frame - source_start_frame) / rate - duration) <= 1 / rate
    source_start = source_start_frame / rate
    source_end = source_end_frame / rate
    start = source_start_frame - round(.5 * rate)
    end = source_end_frame + round(.75 * rate)
    assert 0 <= start < end <= len(signal), 'Raw recording does not cover guarded source range'
    source_signal = signal[source_start_frame:source_end_frame]
    peak = float(np.max(np.abs(source_signal)))
    rms = float(np.sqrt(np.mean(source_signal.astype(np.float64) ** 2)))
    assert peak > 0 and rms > 0, 'All-zero source signal'
    zero = np.all(source_signal == 0, axis=1)
    edges = np.diff(np.r_[False, zero, False].astype(np.int8))
    runs = [(int(i), int(j)) for i, j in zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1))]
    interior_zero = [(i / rate, j / rate) for i, j in runs if j - i >= rate and i > rate and j < len(source_signal) - rate]
    bounded = folder / 'song-with-guards.wav'
    assert not bounded.exists(), 'Never overwrite a previous output'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n', '-i', str(raw), '-af', f'atrim=start_sample={start}:end_sample={end},asetpts=PTS-STARTPTS', '-c:a', 'pcm_f32le', str(bounded)], check=True)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', wavfile.WavFileWarning)
        out_rate, output = wavfile.read(bounded, mmap=True)
    assert out_rate == rate and np.array_equal(output, signal[start:end]), 'Export sample mismatch'
    result = {
        'song_id': a.song_id, 'title': row['name'], 'capture_index_provisional': row['capture_index_provisional'],
        'attempt': a.attempt, 'status': 'technical_capture_verified', 'browser': 'Aside MCP / first user Suno tab',
        'raw_path': str(raw.relative_to(ROOT)), 'raw_sha256': sha(raw), 'raw_duration_seconds': len(signal) / rate,
        'song_wav_path': str(bounded.relative_to(ROOT)), 'song_wav_sha256': sha(bounded),
        'sample_rate': rate, 'channels': 2, 'codec': 'pcm_f32le',
        'song_wav_duration_seconds': len(output) / rate, 'source_media_duration_seconds': duration,
        'source_range_raw_seconds_estimate': [source_start, source_end],
        'export_raw_sample_range': [start, end], 'boundary_guards_seconds': [0.5, 0.75],
        'boundary_caveat': 'Media clock / native PTS estimate; output latency uncalibrated. Guards retained; raw capture preserved. Not a final edit.',
        'source_started_at_zero': True, 'natural_end_observed': True, 'playback_rate': 1,
        'browser_clock_origin_p01_p99_spread_seconds': origin_spread,
        'browser_playing_to_ended_wall_seconds': wall_duration,
        'max_audio_pts_gap_seconds': float(np.max(np.abs(gaps))),
        'pts_discontinuities_outside_source': discontinuities,
        'source_audio_pts_continuous': True,
        'source_peak': peak, 'source_rms': rms,
        'interior_exact_zero_runs_at_least_1s': interior_zero,
        'listener_review_required_for_flagged_silence': bool(interior_zero),
        'musical_quality_approved': False, 'official_download': False,
        'timeline_path': str(timeline_path.relative_to(ROOT)), 'timeline_sha256': sha(timeline_path),
        'recorder_log': str((folder / 'capture.log').relative_to(ROOT)),
        'timing_path': str(Path(str(raw) + '.timing.json').relative_to(ROOT)),
        'timing_sha256': sha(Path(str(raw) + '.timing.json')),
    }
    write(folder / 'verification.json', result)
    destination = PRODUCTION / 'capture-verifications'
    destination.mkdir(exist_ok=True)
    write(destination / f'{a.song_id}-attempt-{a.attempt:02d}.json', result)
    manifest = read(PRODUCTION / 'capture-manifest.json')
    assert not any(t['song_id'] == a.song_id for t in manifest['recordings'])
    manifest['recordings'].append(result)
    manifest['recordings'].sort(key=lambda t: t['capture_index_provisional'])
    manifest['valid_full_song_recordings'] = len(manifest['recordings'])
    manifest['active_capture_song_id'] = None
    write(PRODUCTION / 'capture-manifest.json', manifest)
    print(json.dumps({k: result[k] for k in ['song_id', 'status', 'source_media_duration_seconds', 'song_wav_duration_seconds', 'source_peak', 'source_rms', 'interior_exact_zero_runs_at_least_1s']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
