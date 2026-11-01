#!/usr/bin/env python3
"""Mutation check: each mutant of wavvy_harness/gate.py must make the intended new track-prompt test(s) FAIL.

Runs on throw-away copies of wavvy.py, wavvy_harness/ and tests/ under the scratchpad; the real files are not touched.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.gettempdir())

NEW_TESTS = {
    "T1_pass_over_budget": "test_track_prompt_gate_passes_user_supplied_original_style_over_budget",
    "T2_style_differs": "test_track_prompt_gate_rejects_original_style_when_style_differs_from_concept_record",
    "T3_concept_entry": "test_track_prompt_gate_rejects_original_style_without_one_matching_concept_entry",
    "T4_exclude_differs": "test_track_prompt_gate_rejects_original_style_when_exclude_differs_from_concept_record",
    "T5_no_style_source": "test_track_prompt_gate_rejects_original_style_without_style_source_header",
    "T6_readable_differs": "test_track_prompt_gate_rejects_readable_style_values_that_differ_from_header_in_original_style_mode",
    "T7_empty_header": "test_track_prompt_gate_rejects_empty_header_values_in_original_style_mode",
    "T8_mode_off_regression": "test_track_prompt_gate_keeps_existing_checks_when_original_style_mode_is_off",
}
PRECEDENT_TESTS = {
    "P1_type_exception_pass": "test_track_prompt_gate_passes_over_budget_exclude_recorded_as_user_type_style",
    "P2_type_exception_reject": "test_track_prompt_gate_rejects_over_budget_exclude_without_matching_type_record",
    "P3_budget_8_or_fewer": "test_track_prompt_gate_keeps_budget_behavior_at_eight_or_fewer_exclude_terms",
    "P4_unicode_budget": "test_track_prompt_gate_enforces_unicode_style_budget_and_exclude_items",
    "P5_mismatched_proposals": "test_track_prompt_gate_rejects_unknown_and_mismatched_proposals",
}

# (label, expected failing test keys, [(old, new)], note)
HEAD = 'def _user_original_style(concept_text: str, metadata: dict[str, str], style: str, exclude_terms: list[str]) -> tuple[str, str]:\n'
DOC_END = '    """\n    style_type = metadata.get("Style Type", "").strip()\n    if not style_type or metadata.get("Style Source"'
MUTANTS = [
    ("M01 original-style detector always true", ["T2_style_differs", "T3_concept_entry", "T4_exclude_differs", "T5_no_style_source", "T8_mode_off_regression"],
     [(DOC_END, '    """\n    return "산책", ""\n    style_type = metadata.get("Style Type", "").strip()\n    if not style_type or metadata.get("Style Source"')]),
    ("M02 original-style detector always false", ["T1_pass_over_budget", "T6_readable_differs", "T7_empty_header"],
     [(DOC_END, '    """\n    return "", "forced off"\n    style_type = metadata.get("Style Type", "").strip()\n    if not style_type or metadata.get("Style Source"')]),
    ("M03 STYLE equality not checked", ["T2_style_differs"],
     [('    if block.group(1).strip() != style:\n', '    if False:\n')]),
    ("M04 STYLE compared after collapsing whitespace", ["T2_style_differs"],
     [('    if block.group(1).strip() != style:\n', '    if " ".join(block.group(1).split()) != " ".join(style.split()):\n')]),
    ("M05 EXCLUDE equality not checked", ["T4_exclude_differs"],
     [('    if (_exclude_terms(recorded[0]) if recorded else []) != exclude_terms:\n', '    if False:\n')]),
    ("M06 EXCLUDE compared as a set (order ignored)", ["T4_exclude_differs"],
     [('    if (_exclude_terms(recorded[0]) if recorded else []) != exclude_terms:\n', '    if set(_exclude_terms(recorded[0]) if recorded else []) != set(exclude_terms):\n')]),
    ("M07 Style Source header not required", ["T5_no_style_source"],
     [('    if not style_type or metadata.get("Style Source", "").strip().casefold() != USER_ORIGINAL_STYLE_SOURCE:\n', '    if not style_type:\n')]),
    ("M08 exactly-one entry rule dropped (first of many)", ["T3_concept_entry"],
     [('    if len(entries) != 1:\n        return "", f"concept.md ## {section_name}', '    if len(entries) < 1:\n        return "", f"concept.md ## {section_name}')]),
    ("M09 record may live under Type Styles", ["T3_concept_entry"],
     [('_concept_style_entry(concept_text, "Original Styles", style_type)', '_concept_style_entry(concept_text, "Type Styles", style_type)')]),
    ("M10 BPM never compared in the mode", ["T6_readable_differs"],
     [('    bpm_comparable = not original_type or (bool(style_bpms) and not style_bpm_ranges)\n', '    bpm_comparable = not original_type\n')]),
    ("M11 BPM range still compared in the mode", ["T1_pass_over_budget"],
     [('    bpm_comparable = not original_type or (bool(style_bpms) and not style_bpm_ranges)\n', '    bpm_comparable = True\n')]),
    ("M12 Key never compared in the mode", ["T6_readable_differs"],
     [('    key_comparable = not original_type or bool(style_keys)\n', '    key_comparable = not original_type\n')]),
    ("M13 Key always compared in the mode", ["T1_pass_over_budget", "T7_empty_header"],
     [('    key_comparable = not original_type or bool(style_keys)\n', '    key_comparable = True\n')]),
    ("M14 empty Key header allowed when STYLE has none", ["T7_empty_header"],
     [('else bool(key_text.strip())\n', 'else True\n')]),
    ("M15 empty BPM header allowed when not comparable", ["T7_empty_header"],
     [('    bpm_ok = bpm is not None and bpm > 0 and (style_bpms == {bpm} if bpm_comparable else True)\n', '    bpm_ok = (bpm is not None and bpm > 0 and style_bpms == {bpm}) if bpm_comparable else True\n')]),
    ("M16 Vocal never compared in the mode", ["T6_readable_differs"],
     [('    gender_comparable = instrumental or not original_type or bool(style_genders)\n', '    gender_comparable = instrumental or not original_type\n')]),
    ("M17 empty Vocal header allowed when STYLE has no gender", ["T7_empty_header"],
     [('else (bool(vocal_text.strip()) and gender_known)\n', 'else gender_known\n')]),
    ("M18 style budget still enforced in the mode", ["T1_pass_over_budget"],
     [('    length_ok = style_length <= TRACK_PROMPT_STYLE_LIMIT or bool(original_type)\n', '    length_ok = style_length <= TRACK_PROMPT_STYLE_LIMIT\n')]),
    ("M19 exclude budget still enforced in the mode", ["T1_pass_over_budget"],
     [('        if original_type:\n            exclude_ok = True\n', '        if False:\n            exclude_ok = True\n')]),
    ("M20 900-char limit dropped for everyone", ["T8_mode_off_regression", "P4_unicode_budget"],
     [('    length_ok = style_length <= TRACK_PROMPT_STYLE_LIMIT or bool(original_type)\n', '    length_ok = True\n')]),
    ("M21 type-style exception removed", ["P1_type_exception_pass", "T8_mode_off_regression"],
     [('            exception_type, exception_reason = _user_type_exclude_exception(concept_text, metadata, exclude_terms)\n', '            exception_type, exception_reason = "", "removed"\n')]),
]


def run_tests(workdir: Path) -> dict[str, int]:
    proc = subprocess.run([sys.executable, "-m", "unittest", "tests.test_harness", "-k", "track_prompt"], cwd=workdir, capture_output=True, text=True)
    failing: dict[str, int] = {}
    for match in re.finditer(r"^(?:FAIL|ERROR): (test_\w+)", proc.stderr, re.MULTILINE):
        failing[match.group(1)] = failing.get(match.group(1), 0) + 1
    ran = re.search(r"Ran (\d+) tests", proc.stderr)
    failing["__ran__"] = int(ran.group(1)) if ran else -1
    failing["__rc__"] = proc.returncode
    return failing


def main() -> int:
    all_tests = {**NEW_TESTS, **PRECEDENT_TESTS}
    by_method = {method: key for key, method in all_tests.items()}
    ok = True
    for label, expected, edits in [("M00 real gate.py (no mutation)", [], [])] + MUTANTS:
        with tempfile.TemporaryDirectory(dir=SCRATCH) as tmp:
            work = Path(tmp)
            shutil.copy(REPO / "wavvy.py", work / "wavvy.py")
            shutil.copytree(REPO / "wavvy_harness", work / "wavvy_harness", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(REPO / "tests", work / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            gate = work / "wavvy_harness" / "gate.py"
            text = gate.read_text(encoding="utf-8")
            for old, new in edits:
                if text.count(old) != 1:
                    print(f"{label}: SETUP ERROR, pattern found {text.count(old)} times: {old[:70]!r}")
                    return 2
                text = text.replace(old, new)
            gate.write_text(text, encoding="utf-8")
            failing = run_tests(work)
        failed_keys = sorted(by_method[name] for name in failing if name in by_method)
        other = sorted(name for name in failing if not name.startswith("__") and name not in by_method)
        missing = [key for key in expected if key not in failed_keys]
        verdict = "OK" if not missing and (edits or not failed_keys) else "NOT DISCRIMINATED"
        if verdict != "OK":
            ok = False
        print(f"{label}\n    ran={failing['__ran__']} rc={failing['__rc__']} failing={failed_keys}{' other=' + str(other) if other else ''}\n    expected to fail: {expected}  -> {verdict}")
    print("\nALL MUTANTS DISCRIMINATED" if ok else "\nSOME MUTANT SURVIVED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
