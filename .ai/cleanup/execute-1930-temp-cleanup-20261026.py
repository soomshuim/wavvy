#!/usr/bin/env python3
"""Frozen 19:30 temporary-file cleanup. Dry-run default; never recurse on deletion."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path('/Users/zenkim_office/Project/wavvy')
BASE = ROOT / '.ai/cleanup'
PREFIX = '2026-10-26-1930-temp-cleanup'
MANIFESTS = {
    'candidates': '22775c7e80ad1f3c2b65ed800037799b5716df147a67ff0e49d3de00298696cd',
    'protected': 'c9e495f4f9528410a920b7373adefa31001f6b73c63da8dde301ae07d727d6eb',
}
SCOPES = [ROOT / p for p in (
    'SERIES/19-30', 'work/2026-10-25-1930-wish',
    'work/2026-10-26-1930-current20-capture', 'work/mix-170-20261026', 'work/mix-160-20261026')]
EXTERNAL = {
    Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_tYLTJIA1RjuM3NRG/artifacts/yt1930/final-1930-4k.mp4'),
    Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_tYLTJIA1RjuM3NRG/artifacts/yt1930/thumb.jpg'),
}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def parent_fd(path):
    assert path.is_absolute() and '..' not in path.parts and '.git' not in path.parts
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for name in path.parent.parts[1:]:
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def checked(row):
    path = Path(row['path'])
    fd = parent_fd(path)
    file_fd = None
    try:
        file_fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        info = os.fstat(file_fd)
        assert stat.S_ISREG(info.st_mode), path
        expected = (row['device'], row['inode'], row['bytes'], row['mtime_ns'])
        assert (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) == expected, path
        with os.fdopen(os.dup(file_fd), 'rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == row['sha256'], path
        again = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
        assert stat.S_ISREG(again.st_mode), path
        assert (again.st_dev, again.st_ino, again.st_size, again.st_mtime_ns) == expected, path
        return fd, file_fd
    except BaseException:
        if file_fd is not None:
            os.close(file_fd)
        os.close(fd)
        raise


def verify(row):
    fd, file_fd = checked(row)
    os.close(file_fd)
    os.close(fd)


def gate():
    run = subprocess.run([sys.executable, 'wavvy.py', 'gate', 'SERIES/19-30', '--stage', 'uploaded', '--json'],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    data = json.loads(run.stdout)
    assert run.returncode == 0 and data['result'] == 'PASS' and not data['blockers'], run.stderr
    return data


def main(apply):
    records = {}
    for kind, expected in MANIFESTS.items():
        path = BASE / f'{PREFIX}-{kind}.json'
        assert digest(path) == expected
        data = json.loads(path.read_text())
        assert data['video_id'] == 's5pY5cqvbS8' and len(data['files']) == data['count']
        assert sum(r['bytes'] for r in data['files']) == data['bytes']
        records[kind] = data
    candidates, protected = records['candidates']['files'], records['protected']['files']
    assert len(candidates) == 167 and sum(r['bytes'] for r in candidates) == 5908319615
    paths = {r['path'] for r in candidates}
    assert len(paths) == len(candidates) and paths.isdisjoint(r['path'] for r in protected)
    for row in candidates:
        path = Path(row['path'])
        assert path in EXTERNAL or any(path.is_relative_to(scope) for scope in SCOPES), path
        assert path.suffix.lower() not in {'.json', '.jsonl', '.py', '.md', '.txt', '.csv', '.npz', '.png', '.psd'}, path
    upload = json.loads((ROOT / 'SERIES/19-30/production/youtube-upload-20261026.json').read_text())
    assert upload['video_id'] == 's5pY5cqvbS8' and upload['status'] == 'completed_public_comment_pinned'
    assert {Path(r['session_copy']) for r in upload['session_upload_copies']} == EXTERNAL
    opened = subprocess.run(['lsof', '-nP', '-Fpn'], capture_output=True, text=True, timeout=30)
    assert opened.returncode == 0
    assert not paths.intersection(line[1:] for line in opened.stdout.splitlines() if line.startswith('n')), 'candidate file is open'
    before = gate()
    for row in protected + candidates:
        verify(row)
    report = {'schema': 'wavvy.temp_cleanup_execution.v1', 'mode': 'apply' if apply else 'dry_run',
              'started_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'manifest_sha256': MANIFESTS,
              'script_sha256': digest(Path(__file__)), 'candidate_count': len(candidates),
              'candidate_bytes': sum(r['bytes'] for r in candidates), 'protected_count': len(protected),
              'uploaded_gate_before': before, 'deleted': []}
    if not apply:
        report.update(status='dry_run_pass', all_protected_unchanged=True, deleted_count=0)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    output = BASE / f'{PREFIX}-apply.json'
    # Exclusive creation prevents silently repeating a partial execution or overwriting evidence.
    with output.open('x') as stream:
        try:
            with (BASE / f'{PREFIX}-apply.events.jsonl').open('x') as journal:
                for row in candidates:
                    path = Path(row['path'])
                    fd, file_fd = checked(row)
                    try:
                        journal.write(json.dumps({'event': 'delete_intent', 'path': str(path)}) + '\n')
                        journal.flush(); os.fsync(journal.fileno())
                        os.unlink(path.name, dir_fd=fd)
                        report['deleted'].append({'path': str(path), 'bytes': row['bytes']})
                        journal.write(json.dumps({'event': 'deleted', 'path': str(path)}) + '\n')
                        journal.flush(); os.fsync(journal.fileno())
                    finally:
                        os.close(file_fd)
                        os.close(fd)
            for row in protected:
                verify(row)
            assert all(not os.path.lexists(row['path']) for row in candidates)
            report.update(status='applied', all_protected_unchanged=True, all_targets_absent=True,
                          uploaded_gate_after=gate())
        except BaseException as error:
            report.update(status='partial_or_stopped', error=repr(error))
            raise
        finally:
            report['deleted_count'] = len(report['deleted'])
            report['deleted_logical_bytes'] = sum(r['bytes'] for r in report['deleted'])
            report['finished_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({k: v for k, v in report.items() if k != 'deleted'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
