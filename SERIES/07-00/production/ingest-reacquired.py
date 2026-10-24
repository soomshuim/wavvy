#!/usr/bin/env python3
"""Ingest completed downloads whose exact candidate pages were observed.

--orders is an explicit list of completed browser download observations, not
an instruction to infer candidate identity by scanning the Downloads folder.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

SERIES = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024*1024), b''):
            h.update(data)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--orders', type=int, nargs='+', required=True)
    args = parser.parse_args()
    baseline = json.loads((SERIES/'production/pre-remaster-source-ledger-20261024.json').read_text())
    original = baseline['records']['download-manifest.json']['content']
    selected = json.loads((SERIES/'input/suno-final-selection-2026-10-12.json').read_text())
    path = SERIES/'production/reacquisition-20261024.json'
    result = json.loads(path.read_text())
    tracks = {t['order']: t for t in result['tracks']}
    for order in args.orders:
        t = next(t for t in original['tracks'] if t['order'] == order)
        # The normal UI-generated filenames below were returned by the browser.
        source = Path.home()/'Downloads'/f'{order}. {t["approved_title"]}.wav'
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
                                                    '-show_format', '-of', 'json', str(source)]))
        audio = [s for s in probe['streams'] if s['codec_type'] == 'audio']
        assert len(audio) == 1
        audio = audio[0]
        duration = float(probe['format']['duration'])
        assert (audio['codec_name'], int(audio['sample_rate']), audio['channels']) == ('pcm_s16le', 48000, 2)
        assert abs(duration-t['duration_seconds']) < .05, (order, duration, t['duration_seconds'])
        newhash = sha(source)
        destination = SERIES/'input/tracks'/t['input_filename']
        if destination.exists():
            assert sha(destination) == newhash, f'Refusing to overwrite different bytes: {destination}'
        else:
            destination.parent.mkdir(exist_ok=True)
            shutil.copyfile(source, destination)
        assert sha(destination) == newhash
        tracks[order] = {'order': order, 'approved_title': t['approved_title'],
                         'candidate_id': t['candidate_id'], 'candidate_url': t['candidate_url'],
                         'input_filename': t['input_filename'], 'download_path': str(source),
                         'duration_seconds': duration, 'sha256': newhash,
                         'historical_sha256': t['sha256'], 'historical_bytes_match': newhash == t['sha256'],
                         'codec': audio['codec_name'], 'sample_rate_hz': 48000, 'channels': 2,
                         'download_actor': 'Codex via Aside MCP normal WAV download',
                         'source': 'Exact approved candidate URL, title and completed WAV download observed 2026-10-24',
                         'note': 'Historical hashes are frozen in baseline; old media were deleted. Fresh bytes are separately identified.'}
        result['tracks'] = sorted(tracks.values(), key=lambda x: x['order'])
        result['status'] = 'wav_ingest_verified_20_of_20' if len(tracks) == 20 else 'in_progress'
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({'order': order, 'duration_seconds': duration, 'historical_bytes_match': newhash == t['sha256']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
