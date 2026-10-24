#!/usr/bin/env python3
"""Frozen Wavvy exact-file cleanup. Default: dry-run; --apply is explicit.

Inventories are immutable inputs. This script cannot include the three held audio
files, expand the allowlist, remove directories, or update state/source documents.
"""

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
CLEANUP = ROOT / '.ai/cleanup'
INVENTORIES = {
    'media': (CLEANUP / '2026-10-24-wavvy-media-inventory.json',
              'f78c0a9e9004050c2566cd5b7f5353fc0259372e5120d73812164598f1977517'),
    'thumbnail': (CLEANUP / '2026-10-24-wavvy-thumbnail-inventory.json',
                  'd30b1421d71acd30c544e528e0fd5886d27446f037cef2c779c649768703d578'),
}
HELD_AUDIO = {
    ROOT / 'SERIES/06-30/input/tracks/06__다리의 불꽃__Driven__Hardcore Punk Rock__NA.wav',
    ROOT / 'SERIES/06-30/input/tracks/11__계속 앞으로__Driven__Hardcore Punk Rock__NA.wav',
    ROOT / 'SERIES/06-30/output/continuous-mix-20261024/repeat2/continuous-mix-0630-repeat2.m4a',
}
EXACT_TMP = Path('/private/tmp/wavvy-0630-bpm-cli-smoke.wav')
GENERATED_ROOT = Path('/Users/zenkim_office/.codex/generated_images/01a16b8f-8df2-7470-9784-a394c44b28ec')
EXACT_GENERATED = {
    GENERATED_ROOT / name for name in (
        'exec-40f4629f-bdd5-4fa9-874b-1d8a3c894580.png',
        'exec-9dee2185-b804-4000-af7d-f6effb7a3ec4.png',
        'exec-ca51007e-33ee-4d1e-b0c5-1a53bce34150.png',
        'exec-e2753c4d-0bae-4b46-8c2b-e8f34abf6b48.png',
        'exec-e53d479f-b5d9-41cd-8872-3c65e6743932.png',
    )
}
SELECTED_GENERATED = GENERATED_ROOT / 'exec-25232fa8-ccd9-4104-8f90-de3d79c179ae.png'
THUMB_DOCUMENT_EXCEPTIONS = {
    ROOT / 'SERIES/06-30/production' / name for name in (
        'thumbnail-draft-hip-20261024-v2.json',
        'thumbnail-draft-hip-20261024-v3.json',
        'thumbnail-draft-hip-20261024.json',
        'thumbnail-draft-runningwear-20261024.json',
        'thumbnail-draft-runningwear-headband-20261024.json',
        'thumbnail-layout-rejected-headband-20261024.json',
        'thumbnail-layout.json',
        'thumbnail-tiedhair-swift-paused-20261024.json',
    )
}
EXACT_THUMB_REPO = THUMB_DOCUMENT_EXCEPTIONS | {
    ROOT / relative for relative in (
        'SERIES/06-30/input/thumbnail-draft-runningwear-20261024.png',
        'SERIES/06-30/production/compose-thumbnail-20261024.py',
        'SERIES/06-30/production/compose-thumbnail-tiedhair-20261024.swift',
        'SERIES/06-30/production/thumbnail-phone-preview-20261024.jpg',
        'SERIES/06-30/production/thumbnail-phone-rejected-headband-20261024.jpg',
        'SERIES/06-30/production/thumbnail-rejected-headband-20261024.jpg',
        'SERIES/06-30/production/thumbnail-tiedhair-swift-font-failure-20261024.log',
        'SERIES/07-00/input/art-draft-2026-10-12.png',
    )
}
MEDIA_EXTENSIONS = set(('.wav .wave .mp3 .m4a .aac .flac .aif .aiff .aifc .ogg .oga .opus '
                        '.wma .alac .ac3 .amr .caf .ape .mka .mp4 .mkv .mov .m4v .webm '
                        '.avi .flv .m2ts .mts .wmv .mpeg .mpg .ts .3gp .ogv .pcm .raw '
                        '.f32 .f32le .f64 .f64le .s16le .s24le .s32le .u8 .s16 .s24 .s32').split())


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def checked_path(raw):
    p = Path(raw)
    if not p.is_absolute() or str(p) != raw or p.resolve(strict=True) != p:
        raise ValueError(f'Noncanonical or symlink path: {raw}')
    if '.git' in p.parts or 'node_modules' in p.parts:
        raise ValueError(f'Forbidden path component: {raw}')
    return p


def normalize(row, origin, protected=False):
    is_media = origin == 'media'
    raw_path = row['path'] if is_media else row['absolute_path']
    expected = {
        'device': row['device'], 'inode': row['inode'],
        'bytes': row['bytes'] if is_media else row['statbytes'],
        'mtime_ns': row['mtime_ns'],
        'link_count': row['link_count'] if is_media else row['nlink'],
        'allocated_bytes': row['allocated_bytes_stat'] if is_media else row['allocated_bytes'],
    }
    if is_media:
        expected['ctime_ns'] = row['ctime_ns']
    elif row['present'] is not True or row['file_type'] != 'regular_file':
        raise ValueError(f'Thumbnail entry is not an existing regular file: {raw_path}')
    if not all(type(v) is int and v >= 0 for v in expected.values()):
        raise ValueError(f'Invalid frozen stat fields: {raw_path}')
    p = Path(raw_path)
    if not p.is_absolute() or str(p) != raw_path:
        raise ValueError(f'Inventory path is not absolute/canonical: {raw_path}')
    if protected:
        if not (p.is_relative_to(ROOT) or p == SELECTED_GENERATED):
            raise ValueError(f'Protected path outside exact scope: {raw_path}')
    elif is_media:
        if not (p.is_relative_to(ROOT) or p == EXACT_TMP):
            raise ValueError(f'Media path outside exact scope: {raw_path}')
        if p.suffix.lower() not in MEDIA_EXTENSIONS:
            raise ValueError(f'Nonmedia path in media deletion set: {raw_path}')
        if '/SERIES/06-30/' in raw_path and row['media_kind'] == 'video':
            raise ValueError('Current 06:30 video cannot be deleted before YouTube upload')
    elif p not in EXACT_THUMB_REPO | EXACT_GENERATED:
        raise ValueError(f'Thumbnail path outside exact allowlist: {raw_path}')
    if not protected and p in HELD_AUDIO:
        raise ValueError(f'Held audio cannot enter deletion set: {raw_path}')
    if '.git' in p.parts or 'node_modules' in p.parts:
        raise ValueError(f'Forbidden path component: {raw_path}')
    return {'path': raw_path, 'origin': origin, 'protected': protected, 'expected': expected}


def load_allowlist():
    loaded = {}
    for name, (path, expected_hash) in INVENTORIES.items():
        checked_path(str(path))
        data = path.read_bytes()
        if sha256(data) != expected_hash:
            raise ValueError(f'Frozen {name} inventory SHA mismatch')
        loaded[name] = json.loads(data)
    media, thumb = loaded['media'], loaded['thumbnail']
    media_candidates = [r for r in media['files'] if r['decision_status'] == 'authorized_scope_candidate_not_deleted']
    media_protected = [r for r in media['files'] if r['decision_status'] == 'temporarily_protected_pending_user_decision']
    thumb_candidates = [r for r in thumb['entries'] if r['classification'] == 'delete_candidate']
    thumb_protected = [r for r in thumb['entries'] if r['classification'] == 'protected']
    if (len(media_candidates), len(thumb_candidates), len(media_protected), len(thumb_protected)) != (1277, 21, 3, 59):
        raise ValueError('Frozen candidate/protected counts do not match')
    if {Path(r['path']) for r in media_protected} != HELD_AUDIO:
        raise ValueError('Exactly three fixed audio protections are required')
    if {Path(r['absolute_path']) for r in thumb_candidates} != EXACT_THUMB_REPO | EXACT_GENERATED:
        raise ValueError('Exact thumbnail allowlist mismatch')
    candidates = [normalize(r, 'media') for r in media_candidates] + [normalize(r, 'thumbnail') for r in thumb_candidates]
    protected = [normalize(r, 'media', True) for r in media_protected] + [normalize(r, 'thumbnail', True) for r in thumb_protected]
    candidate_paths = [r['path'] for r in candidates]
    protected_paths = [r['path'] for r in protected]
    if len(candidate_paths) != len(set(candidate_paths)) or len(protected_paths) != len(set(protected_paths)):
        raise ValueError('Duplicate frozen paths')
    if set(candidate_paths) & set(protected_paths):
        raise ValueError('Candidate/protected path intersection')
    candidate_inodes = {(r['expected']['device'], r['expected']['inode']) for r in candidates}
    protected_inodes = {(r['expected']['device'], r['expected']['inode']) for r in protected}
    if len(candidate_inodes) != len(candidates) or candidate_inodes & protected_inodes:
        raise ValueError('Duplicate candidate inode or protected inode intersection')
    if sum(r['expected']['bytes'] for r in candidates) != 52_534_148_348:
        raise ValueError('Frozen deletion logical-byte total mismatch')
    return sorted(candidates, key=lambda r: r['path']), sorted(protected, key=lambda r: r['path']), media


def stat_fields(s):
    return {'device': s.st_dev, 'inode': s.st_ino, 'bytes': s.st_size,
            'mtime_ns': s.st_mtime_ns, 'ctime_ns': s.st_ctime_ns,
            'link_count': s.st_nlink, 'allocated_bytes': s.st_blocks * 512}


def compare_stat(row, s):
    actual = stat_fields(s)
    mismatches = {k: {'expected': v, 'actual': actual[k]}
                  for k, v in row['expected'].items() if actual[k] != v}
    if not stat.S_ISREG(s.st_mode):
        mismatches['file_type'] = {'expected': 'regular_file', 'actual_mode': s.st_mode}
    return actual, mismatches


def check_file(row):
    result = {'path': row['path'], 'origin': row['origin'], 'expected': row['expected']}
    try:
        p = checked_path(row['path'])
        actual, mismatches = compare_stat(row, p.lstat())
        result.update(actual=actual, mismatches=mismatches, ok=not mismatches)
    except (OSError, ValueError) as exc:
        result.update(ok=False, error=str(exc))
    return result


def check_control_files(media):
    results = []
    for raw_path, expected_hash in media['preflight']['small_file_sha256'].items():
        try:
            p = checked_path(raw_path)
            if not p.is_relative_to(ROOT):
                raise ValueError('Control file outside repository')
            actual = sha256(p.read_bytes())
            results.append({'path': raw_path, 'expected_sha256': expected_hash,
                            'actual_sha256': actual, 'ok': actual == expected_hash})
        except (OSError, ValueError) as exc:
            results.append({'path': raw_path, 'ok': False, 'error': str(exc)})
    return results


def storage_snapshot():
    result = {'at_utc': utc_now(), 'statvfs': {}}
    for p in (ROOT, EXACT_TMP.parent, GENERATED_ROOT):
        try:
            s = os.statvfs(p)
            result['statvfs'][str(p)] = {
                'block_size': s.f_frsize, 'blocks': s.f_blocks,
                'free_bytes': s.f_bfree * s.f_frsize,
                'available_bytes': s.f_bavail * s.f_frsize,
            }
        except OSError as exc:
            result['statvfs'][str(p)] = {'error': str(exc)}
    command = ['df', '-k', '/System/Volumes/Data']
    r = subprocess.run(command, capture_output=True, text=True, check=False)
    result['df'] = {'command': command, 'exit_code': r.returncode,
                    'stdout': r.stdout, 'stderr': r.stderr}
    return result


def open_parent_without_links(path):
    """Pin each parent directory without following any symlink component."""
    descriptor = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for name in path.parent.parts[1:]:
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def emit_event(journal, event):
    journal.write(json.dumps({'at_utc': utc_now(), **event}, ensure_ascii=False) + '\n')
    journal.flush()
    os.fsync(journal.fileno())


def new_output(path):
    if not path.is_absolute() or path.parent != CLEANUP or path.parent.resolve(strict=True) != CLEANUP:
        raise ValueError('Reports must be exact files directly under the canonical cleanup directory')
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    return os.fdopen(descriptor, 'w', encoding='utf-8')


def run(args):
    mode = 'apply' if args.apply else 'dry_run'
    report_path = Path(args.report) if args.report else CLEANUP / f'2026-10-24-wavvy-cleanup-{mode.replace("_", "-")}.json'
    if report_path.suffix != '.json':
        raise ValueError('Summary report must end in .json')
    journal_path = report_path.with_suffix('.events.jsonl')
    report = {'schema': 'wavvy.exact-cleanup-run.v1', 'mode': mode, 'started_at_utc': utc_now(),
              'status': 'preflight', 'deleted_file_count': 0, 'deleted_logical_bytes': 0,
              'inventory_sha256': {k: h for k, (_, h) in INVENTORIES.items()},
              'script_sha256': sha256(Path(__file__).read_bytes()),
              'report_path': str(report_path), 'journal_path': str(journal_path) if args.apply else None,
              'three_audio_files_permanently_protected_by_this_script': sorted(map(str, HELD_AUDIO)),
              'allocation_limit': 'Logical deleted bytes differ from observed free-space change; APFS clones/snapshots may share storage.'}
    with new_output(report_path) as output:
        protected, media = [], None
        try:
            if ROOT.resolve(strict=True) != ROOT or Path(__file__).resolve(strict=True) != CLEANUP / 'execute-2026-10-24.py':
                raise ValueError('Script/repository root identity mismatch')
            candidates, protected, media = load_allowlist()
            report.update(candidate_file_count=len(candidates), protected_file_count=len(protected),
                          candidate_logical_bytes=sum(r['expected']['bytes'] for r in candidates),
                          frozen_allowlist=candidates,
                          allowlist_sha256=sha256(json.dumps(candidates, sort_keys=True, ensure_ascii=False).encode()))
            checks = [check_file(row) for row in candidates]
            protection_before = [check_file(row) for row in protected]
            controls_before = check_control_files(media)
            report['preflight'] = {'candidates': checks, 'protected': protection_before, 'control_files': controls_before}
            if not all(r['ok'] for r in checks + protection_before + controls_before):
                raise ValueError('At least one frozen candidate/protected/control file changed; nothing may be deleted')
            report['storage_before'] = storage_snapshot()
            deleted = []
            report['file_results'] = deleted
            if args.apply:
                with new_output(journal_path) as journal:
                    emit_event(journal, {'event': 'preflight_pass', 'candidate_count': len(candidates),
                                         'allowlist_sha256': report['allowlist_sha256']})
                    for row in candidates:
                        descriptor = None
                        item = {'path': row['path'], 'bytes': row['expected']['bytes']}
                        try:
                            p = checked_path(row['path'])
                            descriptor = open_parent_without_links(p)
                            actual, mismatches = compare_stat(row, os.stat(p.name, dir_fd=descriptor, follow_symlinks=False))
                            if mismatches:
                                raise ValueError(f'Immediate pre-unlink stat mismatch: {mismatches}')
                            report['active_delete_intent'] = item.copy()
                            emit_event(journal, {'event': 'delete_intent', **item, 'actual_stat': actual})
                            os.unlink(p.name, dir_fd=descriptor)
                            item['status'] = 'deleted'
                            deleted.append(item)
                            report['deleted_file_count'] += 1
                            report['deleted_logical_bytes'] += item['bytes']
                            emit_event(journal, {'event': 'deleted', **item})
                            try:
                                os.stat(p.name, dir_fd=descriptor, follow_symlinks=False)
                            except FileNotFoundError:
                                item['absent_immediately_after'] = True
                            else:
                                raise ValueError('Target path exists immediately after unlink; stopped')
                            report['active_delete_intent'] = None
                        except (OSError, ValueError) as exc:
                            report['operation_error'] = {'path': row['path'], 'error': str(exc)}
                            emit_event(journal, {'event': 'stopped_on_error', **report['operation_error'],
                                                 'deleted_file_count': report['deleted_file_count']})
                            break
                        finally:
                            if descriptor is not None:
                                os.close(descriptor)
            if 'operation_error' in report:
                report['status'] = 'partial' if deleted else 'stopped_before_deletion'
            else:
                report['status'] = 'applied' if args.apply else 'dry_run_pass'
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            report['error'] = str(exc)
            report['status'] = 'partial' if report['deleted_file_count'] else 'blocked_no_deletion'
        except KeyboardInterrupt:
            report['error'] = 'Interrupted; consult flushed journal delete_intent/deleted events'
            report['status'] = ('interrupted_with_unconfirmed_intent' if report.get('active_delete_intent')
                                else 'partial_interrupted' if report['deleted_file_count'] else 'interrupted_no_deletion')
        finally:
            if protected:
                checks_after = [check_file(row) for row in protected]
                controls_after = check_control_files(media)
                report['postflight'] = {'protected': checks_after, 'control_files': controls_after}
                if not all(r['ok'] for r in checks_after + controls_after):
                    report['status'] = ('partial_protection_or_control_changed' if report['deleted_file_count']
                                        else 'blocked_protection_or_control_changed')
            if 'storage_before' in report:
                report['storage_after'] = storage_snapshot()
                a = report['storage_before']['statvfs'][str(ROOT)].get('available_bytes')
                b = report['storage_after']['statvfs'][str(ROOT)].get('available_bytes')
                report['observed_available_bytes_delta'] = b - a if a is not None and b is not None else None
            report['finished_at_utc'] = utc_now()
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
    print(json.dumps({k: report[k] for k in ('mode', 'status', 'deleted_file_count', 'deleted_logical_bytes', 'report_path')}, ensure_ascii=False))
    return 0 if report['status'] in {'dry_run_pass', 'applied'} else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--dry-run', action='store_true', help='Explicitly perform checks only; also the default')
    modes.add_argument('--apply', action='store_true', help='Unlink only frozen authorized candidates after all preflight checks pass')
    parser.add_argument('--report', help='New absolute .json report path directly inside .ai/cleanup; existing files are never overwritten')
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'execution_error_outcome_not_inferred', 'error': str(exc),
                          'action': 'Read the exact report and flushed events; do not infer deletion count from this exception'},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
