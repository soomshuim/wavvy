#!/usr/bin/env python3
"""Frozen 23:00 post-upload cleanup (series 23-00, YouTube wbJQ2WgfJn4). Dry-run is the default and changes nothing;
--apply unlinks exactly the frozen candidate files, one exact path at a time (never recursive, never following symlinks),
then rmdir's only the listed directories that are empty at that moment."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

ROOT = Path('/Users/zenkim_office/Project/wavvy')
BASE = ROOT / '.ai/cleanup'
PREFIX = '2026-11-04-2300-post-upload-cleanup'
SERIES = 'SERIES/23-00'
VIDEO_ID = 'wbJQ2WgfJn4'
SCRATCH = Path('/private/tmp/claude-501/-Users-zenkim-office-Project-wavvy/9f0bef40-3db1-46d4-9c34-092b5b9edf95/scratchpad')
CAPTIONS = Path('/Users/zenkim_office/Downloads/captions.srt')
MANIFESTS = {
    'candidates': 'acbfcd1dd159d10968f675b25f01b0bfda8acd7eb095ce7324e90ac98a46e587',
    'protected': '50540fbb60f0fec626d7507bd05001eae240923c7f47ef94900802887577f171',
}
EXPECT = {'candidates': 867, 'candidate_bytes': 7639588582, 'protected': 4296}
REPO_ALLOWED = [ROOT / p for p in (
    'SERIES/23-00', 'work/2026-11-04-2300-browser-capture', '.ai/lyrics', '.ai/research/2026-11-01-2300-nine-tracks', '.ai/plans')]
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
SANDBOX_RECORD = BASE / f'{PREFIX}-dry-run-sandbox.json'


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def parent_fd(path):
    assert path.is_absolute() and '..' not in path.parts and '.git' not in path.parts and '.venv' not in path.parts
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


def expected_of(row):
    return (row['device'], row['inode'], row['bytes'], row['mtime_ns'], row['nlink'])


def got_of(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_nlink)


def checked(row):
    """Open without following links, compare dev/inode/size/mtime/nlink and sha256, return the open descriptors."""
    path = Path(row['path'])
    fd = parent_fd(path)
    file_fd = None
    try:
        file_fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        info = os.fstat(file_fd)
        assert stat.S_ISREG(info.st_mode), path
        assert got_of(info) == expected_of(row), ('stat differs', str(path), got_of(info), expected_of(row))
        with os.fdopen(os.dup(file_fd), 'rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == row['sha256'], ('sha256 differs', str(path))
        again = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
        assert stat.S_ISREG(again.st_mode) and got_of(again) == expected_of(row), ('stat changed while hashing', str(path))
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


def parse_lsof(text):
    entries = []
    pid = command = fd = access = None
    for line in text.splitlines():
        if line.startswith('p'):
            pid, command = line[1:], None
        elif line.startswith('c'):
            command = line[1:]
        elif line.startswith('f'):
            fd, access = line[1:], None
        elif line.startswith('a'):
            access = line[1:]
        elif line.startswith('n'):
            entries.append({'pid': pid, 'command': command, 'fd': fd, 'access': access, 'path': line[1:]})
    return entries


def open_snapshot(paths):
    """One full lsof pass. Any open descriptor on a candidate blocks the run: there is no read-only exception."""
    run = subprocess.run(['lsof', '-nP', '-Fpcfan'], capture_output=True, text=True, timeout=90)
    assert run.returncode == 0 and not run.stderr.strip(), ('lsof could not establish candidate usage', run.returncode, run.stderr[:200])
    readers = [e for e in parse_lsof(run.stdout) if e['path'] in paths]
    assert not readers, ('candidate file is open', readers[:5])
    return {'observed_at_utc': now(), 'command': ['lsof', '-nP', '-Fpcfan'], 'exit_code': run.returncode,
            'open_candidate_descriptors': 0, 'total_lines': len(run.stdout.splitlines())}


def open_single(path):
    """Fresh targeted lsof for the one file about to be unlinked. Exit 1 with no output means nobody has it open."""
    run = subprocess.run(['lsof', '-nP', '-Fpcfan', '--', str(path)], capture_output=True, text=True, timeout=30)
    assert run.returncode in (0, 1) and not run.stderr.strip(), ('lsof failed for', str(path), run.returncode, run.stderr[:200])
    assert not run.stdout.strip(), ('candidate file is open at unlink time', str(path), run.stdout[:200])


def run_json(args, expect_rc=(0,)):
    run = subprocess.run([sys.executable, 'wavvy.py', *args], cwd=ROOT, capture_output=True, text=True, env=ENV, check=False)
    try:
        data = json.loads(run.stdout)
    except ValueError:
        data = {'unparsed_stdout': run.stdout[:400], 'stderr': run.stderr[:400]}
    return run.returncode, data


def release_checks():
    """uploaded gate, prepared/published subtitle checks and state --check; each must be PASS with exit 0."""
    results = {}
    rc, data = run_json(['gate', SERIES, '--stage', 'uploaded', '--json'])
    assert rc == 0 and data.get('result') == 'PASS' and not data.get('blockers'), ('uploaded gate', rc, data)
    results['uploaded_gate'] = {'exit': rc, 'result': data['result'], 'checks': [(c['name'], c['status']) for c in data['checks']],
                                'warnings': data.get('warnings'), 'blockers': data.get('blockers')}
    for stage in ('prepared', 'published'):
        rc, data = run_json(['verify-subtitles', SERIES, '--stage', stage, '--json'])
        assert rc == 0 and data.get('result') == 'PASS', (f'verify-subtitles {stage}', rc, data)
        results[f'verify_subtitles_{stage}'] = {'exit': rc, 'result': data['result'], 'cues': data.get('cues'), 'sha256': data.get('sha256')}
    rc, data = run_json(['state', SERIES, '--check', '--json'])
    assert rc == 0 and data.get('result') == 'PASS' and not data.get('blockers'), ('state --check', rc, data)
    results['state_check'] = {'exit': rc, 'result': data['result'], 'revision': data['state']['revision'], 'phase': data['state']['phase'],
                              'blockers': data.get('blockers')}
    return results


def free_bytes():
    return shutil.disk_usage(ROOT).free


def tree_digest(top):
    h = hashlib.sha256()
    count = size = 0
    for dirpath, dirnames, filenames in os.walk(top, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames) + sorted(d for d in dirnames if os.path.islink(os.path.join(dirpath, d))):
            full = os.path.join(dirpath, name)
            info = os.lstat(full)
            rel = os.path.relpath(full, top)
            if stat.S_ISLNK(info.st_mode):
                h.update(f'L\0{rel}\0{os.readlink(full)}\n'.encode())
            else:
                h.update(f'F\0{rel}\0{info.st_size}\0{info.st_mtime_ns}\n'.encode())
                size += info.st_size
            count += 1
    return {'entries': count, 'bytes': size, 'stat_digest_sha256': h.hexdigest()}


def verify_external(external):
    for key in ('venv_tree', 'whisper_model_cache'):
        item = external[key]
        now_digest = tree_digest(item['path'])
        assert now_digest == {k: item[k] for k in ('entries', 'bytes', 'stat_digest_sha256')}, (key, now_digest)
    head = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    assert head == external['git']['head'], ('git HEAD moved', head)


def load():
    records = {}
    for kind, expected in MANIFESTS.items():
        path = BASE / f'{PREFIX}-{kind}.json'
        assert digest(path) == expected, ('manifest hash differs', kind)
        records[kind] = json.loads(path.read_text(encoding='utf-8'))
    cand, prot = records['candidates'], records['protected']
    assert cand['video_id'] == VIDEO_ID and prot['video_id'] == VIDEO_ID
    candidates, protected = cand['files'], prot['files']
    assert len(candidates) == cand['count'] == EXPECT['candidates'] and sum(r['bytes'] for r in candidates) == cand['bytes'] == EXPECT['candidate_bytes']
    assert len(protected) == prot['count'] == EXPECT['protected']
    paths = [r['path'] for r in candidates]
    assert len(set(paths)) == len(paths) and set(paths).isdisjoint(r['path'] for r in protected)
    assert set(paths).isdisjoint(r['path'] for r in prot['mutable_documents'])
    for row in candidates:
        p = Path(row['path'])
        assert p.is_absolute() and '..' not in p.parts and '.git' not in p.parts and '.venv' not in p.parts, p
        ok = p == CAPTIONS or p.is_relative_to(SCRATCH) or any(p.is_relative_to(a) for a in REPO_ALLOWED)
        assert ok, ('candidate outside the frozen allowlist', str(p))
        assert row['class'] in 'ABCD', p
    for row in cand['directories_remove_if_empty']:
        p = Path(row['path'])
        assert p.is_absolute() and '..' not in p.parts and p not in (ROOT, SCRATCH, ROOT / 'SERIES', ROOT / 'work', ROOT / '.ai')
        assert p.is_relative_to(SCRATCH) or any(p.is_relative_to(a) for a in REPO_ALLOWED), p
    return cand, prot


def preconditions():
    upload = json.loads((ROOT / 'SERIES/23-00/production/youtube-upload-20261104.json').read_text(encoding='utf-8'))
    assert upload.get('video_id') == VIDEO_ID, upload.get('video_id')
    concept = (ROOT / 'SERIES/23-00/concept.md').read_text(encoding='utf-8')
    assert '- YouTube upload: completed' in concept and f'youtu.be/{VIDEO_ID}' in concept
    return {'video_id': upload['video_id'], 'upload_record_status': upload.get('status')}


def main(apply):
    cand, prot = load()
    candidates, protected = cand['files'], prot['files']
    mutable = prot['mutable_documents']
    paths = {r['path'] for r in candidates}
    facts = preconditions()
    before = release_checks()
    sandbox = None
    if apply:
        assert SANDBOX_RECORD.is_file(), 'virtual-deletion record is required before --apply'
        sandbox = json.loads(SANDBOX_RECORD.read_text(encoding='utf-8'))
        assert sandbox.get('result') == 'PASS' and sandbox.get('candidates_manifest_sha256') == MANIFESTS['candidates'], 'virtual-deletion record is not a PASS for these manifests'
    verify_external(prot['external'])
    for row in protected + candidates:
        verify(row)
    mutable_start = {}
    for row in mutable:
        assert os.path.isfile(row['path']) and not os.path.islink(row['path']), row['path']
        mutable_start[row['path']] = digest(row['path'])
    process_snapshot = open_snapshot(paths)
    free_before = free_bytes()
    by_class = {}
    for row in candidates:
        c = by_class.setdefault(row['class'], {'count': 0, 'bytes': 0})
        c['count'] += 1
        c['bytes'] += row['bytes']
    report = {'schema': 'wavvy.post_upload_cleanup_execution.v1', 'mode': 'apply' if apply else 'dry_run', 'started_at_utc': now(),
              'manifest_sha256': MANIFESTS, 'script_sha256': digest(__file__), 'candidate_count': len(candidates),
              'candidate_bytes': sum(r['bytes'] for r in candidates), 'candidates_by_class': by_class, 'protected_count': len(protected),
              'mutable_document_count': len(mutable), 'directory_rows': len(cand['directories_remove_if_empty']), 'preconditions': facts,
              'release_checks_before': before, 'process_snapshot': process_snapshot, 'free_bytes_before': free_before,
              'space_note': 'Logical bytes are separate from the actual free-space change (APFS, other activity).', 'deleted': []}
    if not apply:
        report.update(status='dry_run_pass', all_protected_unchanged=True, external_unchanged=True, deleted_count=0, finished_at_utc=now(),
                      free_bytes_after=free_bytes())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    report['virtual_deletion_record'] = {'path': str(SANDBOX_RECORD), 'sha256': digest(SANDBOX_RECORD)}
    output = BASE / f'{PREFIX}-apply.json'
    # Exclusive creation prevents silently repeating a partial execution or overwriting evidence.
    with output.open('x') as stream:
        try:
            with (BASE / f'{PREFIX}-apply.events.jsonl').open('x') as journal:
                def log(event):
                    journal.write(json.dumps(event, ensure_ascii=False) + '\n')
                    journal.flush()
                    os.fsync(journal.fileno())
                log({'event': 'start', 'at': now(), 'candidates': len(candidates)})
                for index, row in enumerate(candidates, 1):
                    path = Path(row['path'])
                    fd, file_fd = checked(row)
                    try:
                        os.close(file_fd)
                        file_fd = None
                        open_single(path)
                        current = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
                        assert stat.S_ISREG(current.st_mode) and got_of(current) == expected_of(row), ('changed before unlink', str(path))
                        log({'event': 'delete_intent', 'n': index, 'path': str(path)})
                        os.unlink(path.name, dir_fd=fd)
                        report['deleted'].append({'path': str(path), 'bytes': row['bytes'], 'class': row['class']})
                        log({'event': 'deleted', 'n': index, 'path': str(path)})
                    finally:
                        if file_fd is not None:
                            os.close(file_fd)
                        os.close(fd)
                removed, skipped = [], []
                for row in cand['directories_remove_if_empty']:
                    path = Path(row['path'])
                    if not os.path.lexists(path):
                        skipped.append({'path': str(path), 'reason': 'absent'})
                        continue
                    fd = parent_fd(path)
                    try:
                        try:
                            os.rmdir(path.name, dir_fd=fd)
                            removed.append(str(path))
                            log({'event': 'rmdir', 'path': str(path)})
                        except OSError as error:
                            skipped.append({'path': str(path), 'reason': repr(error)})
                            log({'event': 'rmdir_skipped', 'path': str(path), 'error': repr(error)})
                    finally:
                        os.close(fd)
                report['directories_removed'] = removed
                report['directories_skipped'] = skipped
            for row in protected:
                verify(row)
            verify_external(prot['external'])
            for path, start in mutable_start.items():
                assert digest(path) == start, ('mutable document changed during the run', path)
            assert all(not os.path.lexists(r['path']) for r in candidates)
            report.update(status='applied', all_protected_unchanged=True, external_unchanged=True, all_targets_absent=True,
                          release_checks_after=release_checks())
        except BaseException as error:
            report.update(status='partial_or_stopped', error=repr(error))
            raise
        finally:
            report['deleted_count'] = len(report['deleted'])
            report['deleted_logical_bytes'] = sum(r['bytes'] for r in report['deleted'])
            report['free_bytes_after'] = free_bytes()
            report['free_bytes_delta'] = report['free_bytes_after'] - free_before
            report['finished_at_utc'] = now()
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    print(json.dumps({k: v for k, v in report.items() if k != 'deleted'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    main(parser.parse_args().apply)
