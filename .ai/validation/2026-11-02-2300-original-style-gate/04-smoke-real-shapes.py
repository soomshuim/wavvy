#!/usr/bin/env python3
"""Smoke: run the real track-prompt gate on the 9 assembled original styles (read-only input, temp series).

Reads .ai/plans/2026-11-02-2300-original-styles.json, builds a throw-away series whose concept.md has a
`## Original Styles` section (one `### <type>` entry per distinct type), writes one txt per entry with the
header values the original style itself states, and prints the gate result. SERIES/23-00 is not touched.
"""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from wavvy import cli  # noqa: E402

data = json.loads((REPO / ".ai/plans/2026-11-02-2300-original-styles.json").read_text(encoding="utf-8"))
entries = data["entries"]


def exclude_line(entry):
    return ", ".join(entry["proposed_exclude"])


def block(entry):
    return entry["proposed_style"]


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    series = root / "SERIES" / "smoke"
    (series / "input" / "tracks").mkdir(parents=True)
    seen = {}
    for entry in entries:
        seen.setdefault(entry["type"], entry)
    body = "".join(f"### {t}\n\n- EXCLUDE: {exclude_line(e)}\n\n```text\n{block(e)}\n```\n\n" for t, e in seen.items())
    (series / "concept.md").write_text(f"# Smoke\n\n## Original Styles\n\n{body}## Track Map\n", encoding="utf-8")
    failures = 0
    for entry in entries:
        key_header = entry["key"]["original"].split(" (")[0]
        vocal = entry["vocal_gender"]["original"]
        header = f"Track: {entry['title']}\nBPM: {entry['bpm']['original']}\nKey: {key_header}\nVocal: {vocal} lead\nStyle Type: {entry['type']}\nStyle Source: user-supplied original style\n"
        txt = series / "input" / "tracks" / f"{entry['order']}_{entry['title']}.txt"
        txt.write_text(f"{header}\n=== STYLE ===\n{block(entry)}\n\n=== EXCLUDE ===\n{exclude_line(entry)}\n\n=== LYRICS ===\n[Verse 1]\nsmoke\n", encoding="utf-8")
        with patch("wavvy.git_repo_root", return_value=root):
            result = CliRunner().invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(txt), "--json"])
        payload = json.loads(result.output)
        checks = {c["name"]: c for c in payload["checks"]}
        print(f"{entry['order']} {entry['title']} ({entry['type']}): exit={result.exit_code} result={payload['result']}")
        for name in ("style_character_limit", "exclude_budget", "bpm_metadata_matches_style", "key_metadata_matches_style", "vocal_gender_metadata_matches_style"):
            print(f"    {checks[name]['status']} {name}: {checks[name]['detail']}")
        for blocker in payload["blockers"]:
            print(f"    BLOCKER {blocker}")
        failures += result.exit_code != 0
    print(f"\nfailures={failures}/{len(entries)}")
    sys.exit(1 if failures else 0)
