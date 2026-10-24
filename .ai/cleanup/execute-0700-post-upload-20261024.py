#!/usr/bin/env python3
"""Exact frozen 07:00 cleanup; dry-run by default, no directory recursion."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('/Users/zenkim_office/Project/wavvy')
SERIES = ROOT / 'SERIES/07-00'
BASE = ROOT / '.ai/cleanup'
INVENTORY = BASE / '2026-10-24-0700-post-upload-inventory.json'
EXPECTED = '63a21dec0e9b322a0a28149a8a601e79dd90d7c320b09fba9a4ee177e46ac13a'
PLAN = ROOT / '.ai/plans/2026-10-24-0700-180bpm-remaster.md'
BROWSER = Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-24_k25cxqx6HVLbmkXN/artifacts')
BROWSER_NAMES = {'youtube-0700-comments-before.json', 'youtube-0700-comments-after.json',
                 'youtube-0700-public-metadata.json', 'youtube-0700-upload-observations.json',
                 'youtube-0700-published-thumbnail.jpg', 'youtube-0700-public-watch.jpg'}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check(row):
    path = Path(row['path'])
    assert path.is_absolute() and path.resolve(strict=True) == path, path
    assert not any(part in {'.git', 'node_modules'} for part in path.parts), path
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and not path.is_symlink(), path
    assert (s.st_size, sha(path)) == (row['bytes'], row['sha256']), path
    if 'inode' in row:
        assert (s.st_dev, s.st_ino, s.st_mtime_ns) == (row['device'], row['inode'], row['mtime_ns']), path


def parent_fd(path):
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


def main(apply):
    assert ROOT.resolve(strict=True) == ROOT
    assert sha(INVENTORY) == EXPECTED
    data = json.loads(INVENTORY.read_text())
    candidates, protected = data['candidates'], data['protected']
    assert len(candidates) == data['candidate_count'] == 198
    assert sum(r['bytes'] for r in candidates) == data['candidate_bytes'] == 3864544687
    assert len(protected) == data['protected_count'] == 164
    paths = {r['path'] for r in candidates}
    assert len(paths) == len(candidates) and not paths.intersection(r['path'] for r in protected)
    downloads = {t['download_path'] for t in json.loads((SERIES / 'production/reacquisition-20261024.json').read_text())['tracks']}
    for row in candidates:
        p = Path(row['path'])
        assert p.is_relative_to(SERIES) or p == PLAN or (p.parent == BROWSER and p.name in BROWSER_NAMES) or str(p) in downloads
    upload = json.loads((SERIES / 'production/youtube-upload-20261024.json').read_text())
    assert upload['video_id'] == '7iVqqukk5WA' and upload['visibility']['observed_after_reload'] == 'public'
    assert upload['processing']['4k'] == 'complete'
    for row in candidates + protected:
        check(row)
    report = {'schema': 'wavvy.post_upload_cleanup.v1', 'mode': 'apply' if apply else 'dry_run',
              'inventory_sha256': EXPECTED, 'script_sha256': sha(Path(__file__)),
              'candidate_count': len(candidates), 'candidate_bytes': data['candidate_bytes'],
              'protected_count': len(protected), 'deleted': [], 'started_at_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    output = BASE / ('2026-10-24-0700-post-upload-cleanup.json' if apply else '2026-10-24-0700-post-upload-dry-run.json')
    free_before = os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize
    with output.open('x') as stream:
        try:
            if apply:
                journal_path = BASE / '2026-10-24-0700-post-upload-cleanup.events.jsonl'
                with journal_path.open('x') as journal:
                    for row in candidates:
                        check(row)
                        p = Path(row['path'])
                        fd = parent_fd(p)
                        try:
                            s = os.stat(p.name, dir_fd=fd, follow_symlinks=False)
                            assert stat.S_ISREG(s.st_mode) and (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns) == (row['device'],row['inode'],row['bytes'],row['mtime_ns'])
                            journal.write(json.dumps({'event': 'delete_intent', 'path': str(p)}, ensure_ascii=False) + '\n')
                            journal.flush(); os.fsync(journal.fileno())
                            os.unlink(p.name, dir_fd=fd)
                            report['deleted'].append({'path':str(p),'bytes':row['bytes']})
                            journal.write(json.dumps({'event': 'deleted', 'path': str(p)}, ensure_ascii=False) + '\n')
                            journal.flush(); os.fsync(journal.fileno())
                            assert not p.exists() and not p.is_symlink()
                        finally:
                            os.close(fd)
            for row in protected:
                check(row)
            report['all_protected_unchanged'] = True
            report['all_targets_absent'] = all(not Path(r['path']).exists() and not Path(r['path']).is_symlink() for r in candidates) if apply else None
            report['status'] = 'applied' if apply else 'dry_run_pass'
        except BaseException as error:
            report['status'] = 'partial_or_stopped'
            report['error'] = repr(error)
            raise
        finally:
            report['deleted_count'] = len(report['deleted'])
            report['deleted_logical_bytes'] = sum(r['bytes'] for r in report['deleted'])
            report['free_bytes_before'] = free_before
            report['free_bytes_after'] = os.statvfs(ROOT).f_bavail * os.statvfs(ROOT).f_frsize
            report['observed_free_bytes_delta'] = report['free_bytes_after'] - free_before
            report['allocation_note'] = 'Logical file sizes and observed free-space change differ; APFS storage sharing and other activity affect the latter.'
            report['finished_at_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
            json.dump(report, stream, ensure_ascii=False, indent=2); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({k:v for k,v in report.items() if k != 'deleted'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
