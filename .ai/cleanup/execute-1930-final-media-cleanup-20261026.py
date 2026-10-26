#!/usr/bin/env python3
"""Frozen19:30 final media cleanup under the new explicit user request. Dry-run default; never recurse on deletion."""
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
PREFIX = '2026-10-26-1930-final-media-cleanup'
MANIFESTS = {
    'candidates': '242a58889b40b313998a1a287d4173e7da292383719d57acccf01eb1a717060c',
    'protected': '51d50f880707bf8ba553482c67286bc0262ab7051fa7702a2c818717d2c057ab',
}
SCOPES = [ROOT / p for p in (
    'SERIES/19-30', 'work/2026-10-25-1930-wish',
    'work/2026-10-26-1930-current20-capture', 'work/mix-170-20261026', 'work/mix-160-20261026')]
READ_ONLY_PREVIEW = '/Users/zenkim_office/Project/wavvy/SERIES/19-30/output/mix-170-20261026/continuous-mix-1930-repeat2.wav'
READ_ONLY_PREVIEW_INODE = 475818468



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



def open_readers(paths):
    """Block all open candidates except the controller's exact read-only preview exception."""
    opened = subprocess.run(['lsof', '-nP', '-Fpcfain'], capture_output=True, text=True, timeout=30)
    assert opened.returncode == 0 and not opened.stderr, 'lsof could not establish candidate usage'
    readers = []
    pid = command = fd = access = inode = None
    for line in opened.stdout.splitlines():
        if line.startswith('p'):
            pid, command = line[1:], None
        elif line.startswith('c'):
            command = line[1:]
        elif line.startswith('f'):
            fd, access, inode = line[1:], None, None
        elif line.startswith('a'):
            access = line[1:]
        elif line.startswith('i'):
            inode = line[1:]
        elif line.startswith('n') and line[1:] in paths:
            reader = dict(path=line[1:], pid=pid, command=command, fd=fd, access=access, inode=inode)
            assert (reader['path'] == READ_ONLY_PREVIEW
                    and command == 'QuickLookUIService' and access == 'r'
                    and inode == str(READ_ONLY_PREVIEW_INODE)), ('candidate file is open without exact read-only exception', reader)
            readers.append(reader)
    return dict(observed_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                command=['lsof', '-nP', '-Fpcfain'], exit_code=opened.returncode,
                stderr_bytes=len(opened.stderr.encode()), allowed_read_only_readers=readers)


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
    assert len(candidates) == 29 and sum(r['bytes'] for r in candidates) == 6738666640
    paths = {r['path'] for r in candidates}
    assert len(paths) == len(candidates) and paths.isdisjoint(r['path'] for r in protected)
    for row in candidates:
        path = Path(row['path'])
        assert any(path.is_relative_to(scope) for scope in SCOPES), path
        assert path.suffix.lower() in {'.wav', '.m4a', '.mp4'}, path
    upload = json.loads((ROOT / 'SERIES/19-30/production/youtube-upload-20261026.json').read_text())
    assert upload['video_id'] == 's5pY5cqvbS8' and upload['status'] == 'completed_public_comment_pinned'
    before = gate()
    for row in protected + candidates:
        verify(row)
    process_snapshot = open_readers(paths)
    report = {'schema': 'wavvy.final_media_cleanup_execution.v1', 'mode': 'apply' if apply else 'dry_run',
              'started_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'manifest_sha256': MANIFESTS,
              'script_sha256': digest(Path(__file__)), 'candidate_count': len(candidates),
              'candidate_bytes': sum(r['bytes'] for r in candidates), 'protected_count': len(protected),
              'uploaded_gate_before': before, 'process_snapshot': process_snapshot,
              'space_note': 'POSIX unlink removes the path; QuickLook may retain read-only data until its descriptor closes. Logical bytes are separate from actual free-space change.', 'deleted': []}
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
                        # Our hash-reading descriptor is closed before observing external usage.
                        os.close(file_fd)
                        file_fd = None
                        # Reobserve immediately before each exact unlink; a new writer/reader stops execution.
                        current_readers = open_readers(paths)
                        current = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
                        assert stat.S_ISREG(current.st_mode)
                        assert (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns) == (
                            row['device'], row['inode'], row['bytes'], row['mtime_ns']), path
                        if current_readers['allowed_read_only_readers']:
                            journal.write(json.dumps({'event': 'read_only_open_exception', **current_readers}) + '\n')
                            journal.flush(); os.fsync(journal.fileno())
                        journal.write(json.dumps({'event': 'delete_intent', 'path': str(path)}) + '\n')
                        journal.flush(); os.fsync(journal.fileno())
                        os.unlink(path.name, dir_fd=fd)
                        report['deleted'].append({'path': str(path), 'bytes': row['bytes']})
                        journal.write(json.dumps({'event': 'deleted', 'path': str(path)}) + '\n')
                        journal.flush(); os.fsync(journal.fileno())
                    finally:
                        if file_fd is not None:
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
