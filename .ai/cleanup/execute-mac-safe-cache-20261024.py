#!/usr/bin/env python3
"""Frozen, file-only cleanup of idle Atlas caches, updater downloads and old Adobe logs."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import time

HOME = Path.home()
BASE = Path(__file__).resolve().parent / 'mac-safe-cache-20261024'
MANIFEST = BASE / 'manifest.jsonl.gz'
CACHE = HOME / 'Library/Caches'
LOGS = HOME / 'Library/Logs'
ATLAS = CACHE / 'com.openai.atlas/browser-data/host'
UPDATERS = ('pencil-updater', 'cherrystudio-updater', 'notion-updater')
APP_MARKERS = {
    'atlas': ('/applications/atlas.app/', '/applications/chatgpt atlas.app/', '/com.openai.atlas/'),
    'pencil-updater': ('/applications/pencil.app/', '/library/caches/pencil-updater/'),
    'cherrystudio-updater': ('/applications/cherry studio.app/', '/applications/cherrystudio.app/', '/library/caches/cherrystudio-updater/'),
    'notion-updater': ('/applications/notion.app/', '/library/caches/notion-updater/'),
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def identity(s):
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def runtime():
    ps = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,comm='], text=True)
    processes = []
    for line in ps.splitlines():
        fields = line.strip().split(None, 2)
        if len(fields) == 3:
            processes.append({'pid': int(fields[0]), 'ppid': int(fields[1]), 'command': fields[2]})
    active = {k: [p for p in processes if any(m in p['command'].lower() for m in markers)]
              for k, markers in APP_MARKERS.items()}
    opened = subprocess.run(['lsof', '-nP', '-Fpcfn'], text=True, capture_output=True, timeout=30)
    if opened.returncode != 0 or opened.stderr:
        raise RuntimeError('Open-file inventory incomplete: ' + opened.stderr[:1000])
    names = set()
    cds = []
    pid = command = fd = None
    for line in opened.stdout.splitlines():
        if line.startswith('p'): pid = line[1:]
        elif line.startswith('c'): command = line[1:]
        elif line.startswith('f'): fd = line[1:]
        elif line.startswith('n'):
            name = line[1:]
            names.add(name)
            if fd == 'cwd' and name == str(HOME / 'Project/CDS'):
                cds.append({'pid': pid, 'command': command, 'cwd': name})
    return {'captured_at': now(), 'active_candidate_apps': active, 'cds_processes': cds}, names


def allowed(path, group):
    if not path.is_absolute() or '..' in path.parts:
        return False
    if group == 'atlas':
        try:
            rel = path.relative_to(ATLAS)
        except ValueError:
            return False
        return len(rel.parts) >= 3 and rel.parts[1] in ('Cache', 'Code Cache')
    if group in UPDATERS:
        try:
            rel = path.relative_to(CACHE / group)
        except ValueError:
            return False
        return str(rel) == 'update.zip' or (len(rel.parts) == 2 and rel.parts[0] == 'pending'
                 and (rel.name == 'update-info.json' or rel.suffix == '.zip'))
    if group == 'old_adobe_logs':
        try:
            rel = path.relative_to(LOGS)
        except ValueError:
            return False
        return len(rel.parts) >= 2 and rel.parts[0] in ('Adobe', 'CreativeCloud', 'NGL') and bool(
            re.search(r'\.log(?:[.-]\d+)?(?:\.gz)?$', rel.name, re.I))
    return False


def parent_fd(path):
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.parent.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def inventory():
    BASE.mkdir(exist_ok=False)
    rt, opened = runtime()
    roots = [(p / leaf, 'atlas') for p in ATLAS.iterdir() if p.is_dir() and not p.is_symlink()
             for leaf in ('Cache', 'Code Cache') if (p / leaf).is_dir()]
    roots += [(CACHE / n, n) for n in UPDATERS]
    roots += [(LOGS / n, 'old_adobe_logs') for n in ('Adobe', 'CreativeCloud', 'NGL')]
    counts = {}
    skipped = []
    cutoff_days = {'atlas': 7, 'old_adobe_logs': 30, **{n: 14 for n in UPDATERS}}
    cutoffs = {g: time.time() - days * 86400 for g, days in cutoff_days.items()}
    with gzip.open(MANIFEST, 'xt', encoding='utf-8') as output:
        for root, group in roots:
            if rt['active_candidate_apps'].get(group):
                skipped.append({'path': str(root), 'reason': 'owner app active'})
                continue
            for directory, dirs, files in os.walk(root, followlinks=False):
                dirs[:] = [n for n in dirs if not (Path(directory) / n).is_symlink()]
                for name in files:
                    p = Path(directory) / name
                    s = p.lstat()
                    if not allowed(p, group) or not stat.S_ISREG(s.st_mode) or p.parent.resolve() != p.parent:
                        continue
                    if s.st_mtime >= cutoffs[group] or s.st_ctime >= cutoffs[group] or str(p) in opened:
                        skipped.append({'path': str(p), 'reason': 'recent or open'})
                        continue
                    row = {'path': str(p), 'group': group, 'identity': identity(s)}
                    output.write(json.dumps(row, separators=(',', ':')) + '\n')
                    c = counts.setdefault(group, {'files': 0, 'logical_bytes': 0, 'allocated_bytes': 0})
                    c['files'] += 1
                    c['logical_bytes'] += s.st_size
                    c['allocated_bytes'] += s.st_blocks * 512
    report = {'created_at': now(), 'authorization': '좋아 정리 가능한건 정리해줘. cds 작업 지장 안미치는 선에서',
              'scope': 'Only enumerated regular cache/download files and closed old Adobe logs; no directories removed.',
              'protected': ['~/Project (except this Wavvy evidence)', '~/.claude', '~/.codex', '/private/tmp',
                            '~/Library/Application Support', 'active app caches', 'build/package caches', 'system files', 'Trash'],
              'runtime': rt, 'age_days_minimum': cutoff_days, 'cutoffs': cutoffs, 'groups': counts,
              'skipped': skipped, 'manifest_sha256': digest(MANIFEST)}
    (BASE / 'inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('skipped', 'runtime')}, ensure_ascii=False))


def execute(apply, expected):
    assert expected and digest(MANIFEST) == expected
    inv = json.loads((BASE / 'inventory.json').read_text())
    assert inv['manifest_sha256'] == expected
    rt, opened = runtime()
    with gzip.open(MANIFEST, 'rt') as f:
        rows = [json.loads(line) for line in f]
    assert len({r['path'] for r in rows}) == len(rows)
    assert len(rows) == sum(c['files'] for c in inv['groups'].values())
    report = {'started_at': now(), 'mode': 'apply' if apply else 'dry-run', 'manifest_sha256': expected,
              'script_sha256': digest(Path(__file__)), 'runtime_before': rt, 'groups': {}, 'skipped': []}
    target = BASE / ('result.json' if apply else 'dry-run.json')
    free_before = os.statvfs(HOME).f_bavail * os.statvfs(HOME).f_frsize
    with target.open('x') as result, gzip.open(BASE / ('deleted.jsonl.gz' if apply else 'checked.jsonl.gz'), 'xt') as journal:
        try:
            for i, row in enumerate(rows):
                if i and i % 5000 == 0:
                    rt, opened = runtime()
                p, group = Path(row['path']), row['group']
                assert allowed(p, group), p
                if rt['active_candidate_apps'].get(group) or str(p) in opened:
                    report['skipped'].append({'path': str(p), 'reason': 'app active or file open'})
                    continue
                # No parent traversal through links, no recursive deletion.
                fd = parent_fd(p)
                try:
                    s = os.stat(p.name, dir_fd=fd, follow_symlinks=False)
                    if not stat.S_ISREG(s.st_mode) or identity(s) != row['identity']:
                        report['skipped'].append({'path': str(p), 'reason': 'changed after inventory'})
                        continue
                    assert s.st_mtime < inv['cutoffs'][group] and s.st_ctime < inv['cutoffs'][group]
                    if apply:
                        os.unlink(p.name, dir_fd=fd)
                    journal.write(json.dumps(row, separators=(',', ':')) + '\n')
                    c = report['groups'].setdefault(group, {'files': 0, 'logical_bytes': 0, 'allocated_bytes': 0})
                    c['files'] += 1
                    c['logical_bytes'] += s.st_size
                    c['allocated_bytes'] += s.st_blocks * 512
                finally:
                    os.close(fd)
            report['status'] = 'applied' if apply else 'dry_run_pass'
        except BaseException as error:
            report['status'] = 'partial_or_stopped'
            report['error'] = repr(error)
            raise
        finally:
            report['runtime_after'], _ = runtime()
            report['free_bytes_before'] = free_before
            report['free_bytes_after'] = os.statvfs(HOME).f_bavail * os.statvfs(HOME).f_frsize
            report['observed_free_bytes_delta'] = report['free_bytes_after'] - free_before
            report['allocation_note'] = 'File-size totals and live free-space change differ due to APFS shared storage and concurrent work.'
            report['finished_at'] = now()
            json.dump(report, result, ensure_ascii=False, indent=2)
            result.write('\n')
    print(json.dumps({k: v for k, v in report.items() if not k.startswith('runtime') and k != 'skipped'}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--expected-manifest-sha256')
    args = parser.parse_args()
    if args.inventory:
        assert not args.apply
        inventory()
    else:
        execute(args.apply, args.expected_manifest_sha256)
