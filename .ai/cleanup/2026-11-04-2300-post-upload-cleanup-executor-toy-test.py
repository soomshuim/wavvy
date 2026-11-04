#!/usr/bin/env python3
"""Exercise the executor's apply path on a throw-away toy tree (never on the real repository).

Loads the real executor file, repoints its module constants at cleanup-work/toy/, stubs only the wavvy release checks / tree digests,
and checks guards (missing or failing virtual-deletion record, changed candidate, open candidate, repeat run) plus the real unlink/rmdir path.
The toy tree is removed again at the end; nothing else is written.
"""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import contextlib
import sys

WORK = Path('/private/tmp/claude-501/-Users-zenkim-office-Project-wavvy/9f0bef40-3db1-46d4-9c34-092b5b9edf95/scratchpad/cleanup-work')
EXEC = Path('/Users/zenkim_office/Project/wavvy/.ai/cleanup/execute-2300-post-upload-cleanup-20261104.py')
T = WORK / 'toy'
results = []


def check(name, ok, detail=''):
    results.append({'test': name, 'ok': bool(ok), 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name, detail)


def rows_for(paths, cls_map):
    rows = []
    for p in paths:
        info = os.lstat(p)
        with open(p, 'rb') as f:
            sha = hashlib.file_digest(f, 'sha256').hexdigest()
        rows.append({'path': str(p), 'bytes': info.st_size, 'sha256': sha, 'device': info.st_dev, 'inode': info.st_ino,
                     'mtime_ns': info.st_mtime_ns, 'nlink': info.st_nlink, 'class': cls_map[str(p)], 'reason': 'toy', 'group': 'toy',
                     'git_tracked': False})
    return rows


def build():
    for d in ('repo/SERIES/23-00/sub', 'repo/.ai/plans', 'repo/SERIES/23-00/keepdir', 'scratch/dir', 'base'):
        (T / d).mkdir(parents=True, exist_ok=True)
    files = {
        'repo/SERIES/23-00/a.bin': (b'A' * 1000, 'A'), 'repo/SERIES/23-00/sub/b.txt': (b'bee', 'B'), 'repo/.ai/plans/c.md': (b'cee', 'C'),
        'scratch/d1.txt': (b'd1', 'D'), 'scratch/dir/d2.txt': (b'd2', 'D'),
    }
    cls = {}
    for rel, (data, c) in files.items():
        (T / rel).write_bytes(data)
        cls[str(T / rel)] = c
    (T / 'repo/SERIES/23-00/keepdir/p.txt').write_bytes(b'protected')
    (T / 'repo/mutable.md').write_bytes(b'mutable v1')
    cand_paths = [T / r for r in files]
    protected_paths = [T / 'repo/SERIES/23-00/keepdir/p.txt']
    cand = {'schema': 'toy', 'video_id': 'VID', 'count': len(cand_paths), 'bytes': 0, 'files': rows_for(cand_paths, cls),
            'directories_remove_if_empty': [{'path': str(T / 'repo/SERIES/23-00/sub'), 'class': 'B'}, {'path': str(T / 'scratch/dir'), 'class': 'D'},
                                            {'path': str(T / 'repo/SERIES/23-00/keepdir'), 'class': 'X'}]}
    cand['bytes'] = sum(r['bytes'] for r in cand['files'])
    info = os.lstat(T / 'repo/mutable.md')
    prot = {'schema': 'toy', 'video_id': 'VID', 'count': 1, 'bytes': 9, 'files': rows_for(protected_paths, {str(protected_paths[0]): 'P'}),
            'mutable_documents': [{'path': str(T / 'repo/mutable.md'), 'bytes': info.st_size, 'sha256': 'baseline'}],
            'external': {}}
    for kind, doc in (('candidates', cand), ('protected', prot)):
        (T / 'base' / f'2026-11-04-2300-post-upload-cleanup-{kind}.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    return cand, prot


def load_exec():
    spec = importlib.util.spec_from_file_location('toy_exec', EXEC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def configure(mod, cand, prot):
    mod.ROOT = T / 'repo'
    mod.BASE = T / 'base'
    mod.SCRATCH = T / 'scratch'
    mod.CAPTIONS = T / 'no-captions.srt'
    mod.REPO_ALLOWED = [T / 'repo/SERIES/23-00', T / 'repo/.ai/plans']
    mod.SANDBOX_RECORD = T / 'base' / 'sandbox.json'
    mod.VIDEO_ID = 'VID'
    base = T / 'base'
    mod.MANIFESTS = {k: hashlib.sha256((base / f'{mod.PREFIX}-{k}.json').read_bytes()).hexdigest() for k in ('candidates', 'protected')}
    mod.EXPECT = {'candidates': cand['count'], 'candidate_bytes': cand['bytes'], 'protected': prot['count']}
    mod.preconditions = lambda: {'toy': True}
    mod.release_checks = lambda: {'stub': 'PASS'}
    mod.verify_external = lambda external: None


def run_main(mod, apply):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            mod.main(apply)
        return None, buf.getvalue()
    except BaseException as error:
        return error, buf.getvalue()


def wipe():
    for dirpath, dirnames, filenames in os.walk(T, topdown=False):
        assert dirpath == str(T) or dirpath.startswith(str(T) + '/')
        for n in filenames:
            os.unlink(os.path.join(dirpath, n))
        for n in dirnames:
            os.rmdir(os.path.join(dirpath, n))
    os.rmdir(T)


def main():
    assert not T.exists()
    T.mkdir()
    try:
        cand, prot = build()
        mod = load_exec()
        configure(mod, cand, prot)
        # 1 dry run changes nothing
        err, out = run_main(mod, False)
        check('dry-run succeeds', err is None and json.loads(out)['status'] == 'dry_run_pass', repr(err))
        check('dry-run deletes nothing', all(os.path.exists(r['path']) for r in cand['files']))
        # 2 apply without virtual-deletion record
        err, _ = run_main(mod, True)
        check('apply refused without virtual-deletion record', isinstance(err, AssertionError) and 'virtual-deletion record is required' in str(err), repr(err)[:80])
        check('... and nothing deleted / no report written', all(os.path.exists(r['path']) for r in cand['files']) and not (T / 'base/2026-11-04-2300-post-upload-cleanup-apply.json').exists())
        # 3 apply with a FAIL record
        (T / 'base/sandbox.json').write_text(json.dumps({'result': 'FAIL', 'candidates_manifest_sha256': mod.MANIFESTS['candidates']}), encoding='utf-8')
        err, _ = run_main(mod, True)
        check('apply refused with a FAIL virtual-deletion record', isinstance(err, AssertionError) and 'not a PASS' in str(err), repr(err)[:80])
        check('... nothing deleted', all(os.path.exists(r['path']) for r in cand['files']))
        # 4 PASS record for another manifest
        (T / 'base/sandbox.json').write_text(json.dumps({'result': 'PASS', 'candidates_manifest_sha256': 'x' * 64}), encoding='utf-8')
        err, _ = run_main(mod, True)
        check('apply refused when the PASS record belongs to other manifests', isinstance(err, AssertionError), repr(err)[:80])
        (T / 'base/sandbox.json').write_text(json.dumps({'result': 'PASS', 'candidates_manifest_sha256': mod.MANIFESTS['candidates']}), encoding='utf-8')
        # 5 changed candidate content (same size) blocks before any deletion
        victim = T / 'repo/.ai/plans/c.md'
        original = victim.read_bytes()
        os.utime(victim, ns=(os.lstat(victim).st_atime_ns, os.lstat(victim).st_mtime_ns))
        with open(victim, 'r+b') as f:
            f.write(b'CEE')
        err, _ = run_main(mod, True)
        check('apply refused when a candidate changed', isinstance(err, AssertionError), repr(err)[:100])
        check('... nothing deleted', all(os.path.exists(r['path']) for r in cand['files']))
        # restore the exact bytes and mtime recorded in the manifest
        with open(victim, 'r+b') as f:
            f.write(original)
        row = [r for r in cand['files'] if r['path'] == str(victim)][0]
        os.utime(victim, ns=(row['mtime_ns'], row['mtime_ns']))
        # 6 an open candidate blocks
        holder = open(T / 'scratch/d1.txt', 'rb')
        err, _ = run_main(mod, True)
        holder.close()
        check('apply refused while a candidate is open', isinstance(err, AssertionError) and 'open' in str(err), repr(err)[:100])
        check('... nothing deleted', all(os.path.exists(r['path']) for r in cand['files']))
        # 7 a mutable document and the protected file stay untouched; real apply
        before_protected = (T / 'repo/SERIES/23-00/keepdir/p.txt').read_bytes()
        err, out = run_main(mod, True)
        check('apply succeeds on the toy tree', err is None, repr(err))
        check('all candidate files deleted', all(not os.path.lexists(r['path']) for r in cand['files']))
        check('protected file and mutable doc untouched', (T / 'repo/SERIES/23-00/keepdir/p.txt').read_bytes() == before_protected and (T / 'repo/mutable.md').read_bytes() == b'mutable v1')
        report = json.loads((T / 'base/2026-11-04-2300-post-upload-cleanup-apply.json').read_text(encoding='utf-8'))
        check('report status applied, counts match', report['status'] == 'applied' and report['deleted_count'] == len(cand['files']) and report['all_targets_absent'], report['status'])
        check('emptied directories removed', not (T / 'repo/SERIES/23-00/sub').exists() and not (T / 'scratch/dir').exists(), str(report.get('directories_removed')))
        check('non-empty directory in the list is kept, not emptied', (T / 'repo/SERIES/23-00/keepdir').is_dir() and (T / 'repo/SERIES/23-00/keepdir/p.txt').exists(),
              str([s['reason'][:40] for s in report.get('directories_skipped', [])]))
        events = (T / 'base/2026-11-04-2300-post-upload-cleanup-apply.events.jsonl').read_text(encoding='utf-8').splitlines()
        check('journal has intent+deleted for every file', sum('"delete_intent"' in e for e in events) == len(cand['files']) == sum('"deleted"' in e for e in events), str(len(events)))
        # 8 a repeat run cannot overwrite the evidence
        err, _ = run_main(mod, True)
        check('repeat apply cannot overwrite evidence', err is not None, type(err).__name__ if err else 'none')
    finally:
        wipe()
    print(json.dumps({'all_ok': all(r['ok'] for r in results), 'tests': len(results)}))
    sys.exit(0 if all(r['ok'] for r in results) else 1)


if __name__ == '__main__':
    main()
