#!/usr/bin/env python3
"""One-shot, exact six-file post-upload cleanup; default is read-only."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path('/Users/zenkim_office/Project/wavvy')
HERE = ROOT / '.ai/cleanup'
MANIFEST = HERE / '2026-10-24-0630-post-upload-cleanup-manifest.json'
MANIFEST_SHA = 'aa07494f49f29c004db8181dc55bc71db469250082aab70352616e834298c138'
STAGE = Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-24_7Co4pQl3pAQ3I2Wd/artifacts/wavvy-0630')
spec = importlib.util.spec_from_file_location('previous_cleanup', HERE / 'execute-2026-10-24.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def checked(row):
    p = old.checked_path(row['path'])
    actual, mismatch = old.compare_stat(row, p.lstat())
    if mismatch:
        raise ValueError(f'Frozen stat changed: {p}: {mismatch}')
    with p.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    if digest != row['sha256']:
        raise ValueError(f'Frozen SHA-256 changed: {p}')
    return {'path': str(p), 'sha256': digest, 'stat': actual, 'ok': True}


def run(apply):
    raw = MANIFEST.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise ValueError('Frozen manifest changed')
    m = json.loads(raw)
    delete, keep = m['delete'], m['protected'] + m['controls']
    paths = [r['path'] for r in delete]
    if len(delete) != 6 or len(set(paths)) != 6 or set(paths) & {r['path'] for r in keep}:
        raise ValueError('Six unique, disjoint deletion paths required')
    for p in map(Path, paths):
        if not (p.is_relative_to(ROOT / 'SERIES/06-30/output') or p == STAGE / 'final-0630-4k-v2.mp4'):
            raise ValueError(f'Path outside exact scope: {p}')
        if p.suffix not in {'.mp4', '.m4a'}:
            raise ValueError('Only declared audio/video files may be removed')
    observed = json.loads((ROOT / 'SERIES/06-30/production/youtube-public-followup-20261024.json').read_text())
    upload = json.loads((ROOT / 'SERIES/06-30/production/youtube-upload-20261024.json').read_text())
    if observed['videoId'] != 'FUBJ6OBTzoI' or observed['visibility'] != 'public' or set(observed['processing'].values()) != {'complete'}:
        raise ValueError('Upload/processing condition not recorded')
    report_path = HERE / ('2026-10-24-0630-post-upload-cleanup-apply.json' if apply else '2026-10-24-0630-post-upload-cleanup-dry-run.json')
    report = {'schema': 'wavvy.post-upload-cleanup-run.v1', 'mode': 'apply' if apply else 'dry_run',
              'manifest_sha256': MANIFEST_SHA, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'started_at_utc': old.utc_now(), 'deleted': [], 'status': 'preflight',
              'retained_upload_evidence': upload, 'retained_public_evidence': observed}
    with old.new_output(report_path) as output:
        try:
            report['preflight'] = [checked(r) for r in delete + keep]
            report['storage_before'] = old.storage_snapshot()
            if apply:
                with old.new_output(report_path.with_suffix('.events.jsonl')) as journal:
                    old.emit_event(journal, {'event': 'preflight_pass', 'manifest_sha256': MANIFEST_SHA})
                    for row in delete:
                        p = Path(row['path'])
                        parent = old.open_parent_without_links(p)
                        try:
                            fd = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
                            with os.fdopen(fd, 'rb') as f:
                                _, mismatch = old.compare_stat(row, os.fstat(f.fileno()))
                                if mismatch or hashlib.file_digest(f, 'sha256').hexdigest() != row['sha256']:
                                    raise ValueError(f'Immediate file identity mismatch: {p}')
                                _, mismatch = old.compare_stat(row, os.stat(p.name, dir_fd=parent, follow_symlinks=False))
                                if mismatch:
                                    raise ValueError(f'Immediate path identity mismatch: {p}')
                                old.emit_event(journal, {'event': 'delete_intent', 'path': str(p)})
                                os.unlink(p.name, dir_fd=parent)
                                report['deleted'].append(row)
                                old.emit_event(journal, {'event': 'deleted', 'path': str(p)})
                        finally:
                            os.close(parent)
            report['protected_and_controls_after'] = [checked(r) for r in keep]
            if apply and any(os.path.lexists(r['path']) for r in delete):
                raise ValueError('A declared deleted path still exists')
            report['status'] = 'applied' if apply else 'dry_run_pass'
        except Exception as exc:
            report['status'] = 'partial_or_failed' if report['deleted'] else 'blocked_no_deletion'
            report['error'] = str(exc)
        finally:
            report['deleted_file_count'] = len(report['deleted'])
            report['deleted_logical_bytes'] = sum(r['expected']['bytes'] for r in report['deleted'])
            report['storage_after'] = old.storage_snapshot()
            report['physical_storage_note'] = m['physical_storage_note']
            report['finished_at_utc'] = old.utc_now()
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
    print(json.dumps({k: report[k] for k in ('status', 'deleted_file_count', 'deleted_logical_bytes')}))
    return 0 if report['status'] in {'applied', 'dry_run_pass'} else 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    sys.exit(run(parser.parse_args().apply))
