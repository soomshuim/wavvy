#!/usr/bin/env python3
"""Per-song local recording wrapper. Browser playback remains with Aside MCP."""
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'work/2026-11-04-2300-browser-capture'
BINARY = BASE / 'capture-aside'
CATALOG = Path(__file__).resolve().parent / 'source-catalog.json'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['preflight', 'plan', 'record', 'status', 'stop'])
    parser.add_argument('--pid', type=int, help='Current Aside app process ID; never reuse a historical PID.')
    parser.add_argument('--song-id')
    parser.add_argument('--attempt', type=int, default=1)
    parser.add_argument('--catalog', type=Path, default=CATALOG)
    args = parser.parse_args()
    if args.action == 'preflight':
        return subprocess.run([str(BINARY), 'preflight'], check=False).returncode
    if not args.song_id or str(uuid.UUID(args.song_id)) != args.song_id or args.attempt < 1:
        parser.error('--song-id must be a canonical UUID and --attempt must be positive')
    folder = BASE / 'captures' / args.song_id / f'attempt-{args.attempt:02d}'
    metadata = folder / 'capture.json'
    marker = folder / 'stop.marker'
    if args.action == 'status':
        print(metadata.read_text() if metadata.exists() else json.dumps({'status': 'not_started', 'path': str(folder)}))
        return 0
    if args.action == 'stop':
        data = json.loads(metadata.read_text())
        if data['status'] != 'recording':
            raise RuntimeError('This attempt is not recording; no stop marker was written.')
        marker.touch(exist_ok=True)
        print(json.dumps({'stop_requested': True, 'path': str(marker)}))
        return 0
    if not args.pid or args.pid <= 0:
        parser.error('--pid is required for plan/record')
    catalog_bytes = args.catalog.read_bytes()
    catalog = json.loads(catalog_bytes)
    songs = [dict(id=row['song_id'], title=row['name'], duration_ui=row['duration_ui'], public='Published' in row['text']) for row in catalog['rows']]
    ids = [song['id'] for song in songs]
    if len(songs) != 17 or len(set(ids)) != 17:
        raise RuntimeError('The catalog must identify exactly 17 unique current songs.')
    song = next(song for song in songs if song['id'] == args.song_id)
    minutes, seconds = map(int, song['duration_ui'].split(':'))
    duration = minutes * 60 + seconds
    maximum = 450
    if not 0 < duration or duration + 35 > 450:
        raise RuntimeError('UI duration must fit the existing 450-second recorder limit.')
    all_public = all(song.get('public') is True for song in songs)
    command = [str(BINARY), 'record', str(args.pid), str(maximum), str(folder / 'raw.wav'), str(marker)]
    plan = {'song_id': args.song_id, 'title': song['title'], 'attempt': args.attempt,
            'ui_duration_seconds': duration, 'public_17_of_17': all_public,
            'catalog_path': str(args.catalog.resolve()), 'catalog_sha256': hashlib.sha256(catalog_bytes).hexdigest(),
            'command': command, 'output_directory': str(folder), 'capture_order': 'source-catalog provisional order',
            'remaining_capture_order': 'provisional; not the final album order',
            'browser_control': 'Aside MCP only, external to this wrapper',
            'scope': 'Aside application audio; other audible Aside tabs can contaminate capture',
            'microphone': False, 'source_playback_rate_required': 1.0}
    if args.action == 'plan':
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    if not all_public:
        raise RuntimeError('Recording blocked: the supplied current-song catalog does not show all 17 public.')
    permission = subprocess.run([str(BINARY), 'preflight'], check=True, capture_output=True, text=True)
    if 'screen_recording_preflight=true' not in permission.stdout:
        raise RuntimeError('Screen recording permission is unavailable; no permission request was attempted.')
    os.kill(args.pid, 0)
    with (BASE / '.recording.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        folder.mkdir(parents=True, exist_ok=False)
        (folder / 'catalog-source.json').write_bytes(catalog_bytes)
        plan.update(status='recording', wrapper_pid=os.getpid(), requested_at_utc=now(),
                    recorder_sha256=sha(BINARY), adapter_sha256=sha(Path(__file__)))
        save(metadata, plan)
        process = None
        def request_stop(signum, frame):
            marker.touch(exist_ok=True)
        old_handlers = {s: signal.signal(s, request_stop) for s in (signal.SIGINT, signal.SIGTERM)}
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, bufsize=1, start_new_session=True)
            plan['recorder_pid'] = process.pid
            save(metadata, plan)
            lines = []
            with (folder / 'capture.log').open('x') as log:
                for line in process.stdout:
                    lines.append(line)
                    log.write(line)
                    log.flush()
                    print(line, end='', flush=True)
            result = process.wait()
            closed = result == 0 and any('capture_stopped' in line and 'write_error=none' in line for line in lines)
            plan.update(status='capture_closed_unverified' if closed else 'capture_failed_retained',
                        closed_at_utc=now(), returncode=result,
                        timing_json_present=(folder / 'raw.wav.timing.json').exists(),
                        ui_completion_verified=False, listening_verified=False)
            save(metadata, plan)
            return 0 if closed else 1
        except BaseException:
            if process is not None and process.poll() is None:
                marker.touch(exist_ok=True)
                process.wait(timeout=15)
            plan.update(status='capture_failed_retained', closed_at_utc=now())
            save(metadata, plan)
            raise
        finally:
            for sig, handler in old_handlers.items():
                signal.signal(sig, handler)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, KeyError, StopIteration) as error:
        print(f'capture_adapter_error={error}', file=sys.stderr)
        sys.exit(2)
