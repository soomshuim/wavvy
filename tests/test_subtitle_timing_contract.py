"""Timing-map contract tests: exact layout rounding and declared unsung source lines.

Every fixture is a fake series built in a temporary folder; nothing here reads a real series.
"""

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from wavvy_harness.subtitles import MANIFEST, SubtitleError, _layout, _ms, prepare_timed, verify_prepared


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _report(durations, final_duration, fade=0.8, repeat=2):
    return {
        "processing_params": {"fade": fade, "repeat": repeat},
        "summary": {"final_duration": final_duration},
        "tracks": [{"order": i, "title": f"T{i}", "duration": d} for i, d in enumerate(durations, 1)],
    }


# Real unrounded track durations of the 23:00 report (six decimals) and its report total.
REAL_DURATIONS = [
    218.288667, 198.768792, 219.808688, 213.968708, 225.968688, 187.568625, 211.608813, 199.888688,
    200.96875, 153.088792, 192.488729, 214.808625, 209.888646, 138.408771, 214.80875, 206.768729, 133.168854,
]


class LayoutRoundingTests(unittest.TestCase):
    def test_sub_millisecond_durations_are_summed_exactly_then_rounded_once(self):
        durations = [100.0004] * 4  # each rounds down to 100.000 s; the exact total is 3.2 ms longer
        exact_final = 794.4032      # (4 * 100.0004 * 2 - 0.8 * 7) s -> 794403 ms
        per_track_final = sum(_ms(d) for d in durations) * 2 - 800 * 7
        self.assertEqual(per_track_final, 794400)  # the old per-track rounding disagrees by 3 ms
        tracks, starts, repeat, offset, final = _layout(_report(durations, exact_final))
        self.assertEqual((repeat, final), (2, 794403))
        self.assertEqual(starts, [0, 99200, 198401, 297601])  # exact cursor 99200.4 / 198400.8 / 297601.2, rounded once
        self.assertEqual(offset, 396802)                     # exact 396801.6, rounded once

    def test_real_23_00_durations_pass_within_one_millisecond(self):
        per_track_final = sum(_ms(d) for d in REAL_DURATIONS) * 2 - 800 * 33
        self.assertEqual(per_track_final, 6654146)  # what the old check compared against
        _, _, _, offset, final = _layout(_report(REAL_DURATIONS, 6654.136625))
        self.assertEqual((offset, final), (3326668, 6654137))

    def test_one_millisecond_is_accepted_and_two_are_rejected(self):
        durations = [100.0004] * 4  # exact final 794403 ms
        for report_seconds in (794.402, 794.403, 794.404):
            with self.subTest(report_seconds=report_seconds):
                self.assertEqual(_layout(_report(durations, report_seconds))[4], 794403)
        for report_seconds in (794.401, 794.405, 794.400, 794.409):
            with self.subTest(report_seconds=report_seconds):
                with self.assertRaisesRegex(SubtitleError, "Report final duration differs"):
                    _layout(_report(durations, report_seconds))

    def test_whole_millisecond_reports_still_need_the_exact_total(self):
        _layout(_report([197.16, 200.0, 189.2], 1168.72))  # 2 * 586.36 - 0.8 * 5
        with self.assertRaisesRegex(SubtitleError, "Report final duration differs"):
            _layout(_report([197.16, 200.0, 189.2], 1168.722))

    def test_missing_or_malformed_report_still_fails_closed(self):
        with self.assertRaisesRegex(SubtitleError, "Malformed render report"):
            _layout({"tracks": [], "processing_params": {}})
        broken = _report([10.0, 10.0], 18.4)
        broken["summary"] = None
        with self.assertRaisesRegex(SubtitleError, "Report final duration differs"):
            _layout(broken)


CONCEPT = """# Fake series

## Final Track Sources

### 01. One

#### LYRICS

```text
[Intro]
instrumental

[Verse]
first line
second line
third line
```

### 02. Two

#### LYRICS

```text
[Verse]
only line
```
"""
EVIDENCE = "audio-probe/one.json"
MAP_PATH = "input/validation/map/timing.json"


def _cue(line, start, end, text, occurrence=1):
    return {
        "relative_start_ms": start, "relative_end_ms": end, "last_asr_end_ms": end + 100,
        "anchor_classes": ["direct_cue"], "texts": [text],
        "source_line_occurrences": [{"source_line": line, "occurrence": occurrence, "text": text}],
    }


def _timing(unsung=True):
    track_one = {
        "track": 1, "title": "T1", "start_ms": 0, "source_lines": 4,
        "cues": [_cue(2, 1000, 3000, "first line"), _cue(3, 3500, 5500, "second line"), _cue(4, 6000, 8000, "third line")],
    }
    if unsung:
        track_one["unsung_source_lines"] = [{
            "source_line": 1, "text": "instrumental", "reason": "direction line under [Intro], not sung",
            "evidence": [EVIDENCE],
        }]
    track_two = {"track": 2, "title": "T2", "start_ms": 59200, "source_lines": 1, "cues": [_cue(1, 1000, 3000, "only line")]}
    return {"schema": "wavvy.subtitle-timing.v1", "audio_evidence_sha256": {}, "allowed_added_source_lines_per_pass": {},
            "tracks": [track_one, track_two]}


def _build(root, mutate=None, extras=None):
    """Write a fake series (concept, report, evidence, timing map, manifest) under ``root``."""
    root = Path(root)
    (root / "output").mkdir(parents=True)
    (root / "concept.md").write_text(CONCEPT, encoding="utf-8")
    report = _report([60.0, 50.0], 217.6)
    (root / "output/report.json").write_text(json.dumps(report), encoding="utf-8")
    evidence = root / "input/validation/map" / EVIDENCE
    evidence.parent.mkdir(parents=True)
    evidence.write_text('{"fake": "word timing"}', encoding="utf-8")
    timing = _timing()
    timing["audio_evidence_sha256"] = {EVIDENCE: _sha(evidence)}
    manifest_extra = {}
    if extras:
        timing["allowed_added_source_lines_per_pass"] = extras
        manifest_extra = {"required_extra_occurrences": extras, "repeat_evidence": {key: [EVIDENCE] for key in extras}}
    if mutate:
        mutate(timing)
    map_file = root / MAP_PATH
    map_file.write_text(json.dumps(timing, ensure_ascii=False), encoding="utf-8")
    manifest = {
        "schema": "wavvy.subtitles.v1",
        "report": {"path": "output/report.json", "sha256": _sha(root / "output/report.json")},
        "timing_map": {"path": MAP_PATH, "sha256": _sha(map_file)},
        "srt": {"path": "output/youtube_subtitles_ko_timed_estimated.srt"},
        **manifest_extra,
    }
    (root / MANIFEST).parent.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    return root, map_file


class UnsungSourceLineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

    def prepare(self, mutate=None, extras=None):
        root = Path(tempfile.mkdtemp(dir=self.temp.name))  # a fresh fake series per call
        series, map_file = _build(root / "series", mutate, extras)
        return series, prepare_timed(series, map_file)

    def test_valid_declaration_removes_only_that_line_from_the_expected_list(self):
        series, result = self.prepare()
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["cues"], (3 + 1) * 2)  # three sung lines + one in track 2, two passes
        srt = (series / "output/youtube_subtitles_ko_timed_estimated.srt").read_text(encoding="utf-8")
        self.assertNotIn("instrumental", srt)
        self.assertEqual(srt.count("first line"), 2)
        # the approved-source hash still covers every approved line, including the unsung one
        untimed = "\n\n".join(["\n".join(["instrumental", "first line", "second line", "third line"]), "only line"])
        expected = hashlib.sha256(("\n\n".join([untimed] * 2) + "\n").encode("utf-8")).hexdigest()
        self.assertEqual(result["source_sha256"], expected)
        self.assertEqual(verify_prepared(series)["result"], "PASS")

    def test_undeclared_missing_line_is_still_rejected(self):
        def drop_declaration(timing):
            del timing["tracks"][0]["unsung_source_lines"]
        with self.assertRaisesRegex(SubtitleError, "missing or unauthorized sung occurrence"):
            self.prepare(drop_declaration)

    def test_other_missing_line_is_rejected_even_when_one_line_is_declared(self):
        def drop_cue(timing):
            timing["tracks"][0]["cues"].pop(1)  # "second line" vanishes without a declaration
        with self.assertRaisesRegex(SubtitleError, "missing or unauthorized sung occurrence"):
            self.prepare(drop_cue)

    def test_declared_line_must_not_also_be_timed(self):
        def time_it(timing):
            timing["tracks"][0]["cues"].insert(0, _cue(1, 100, 900, "instrumental"))
        with self.assertRaisesRegex(SubtitleError, "missing or unauthorized sung occurrence"):
            self.prepare(time_it)

    def test_evidence_must_be_a_hashed_audio_evidence_entry(self):
        def unknown_ref(timing):
            timing["tracks"][0]["unsung_source_lines"][0]["evidence"] = ["audio-probe/not-hashed.json"]
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(unknown_ref)

    def test_evidence_list_must_not_be_empty(self):
        def no_ref(timing):
            timing["tracks"][0]["unsung_source_lines"][0]["evidence"] = []
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(no_ref)

    def test_declared_text_must_equal_the_approved_text(self):
        def other_text(timing):
            timing["tracks"][0]["unsung_source_lines"][0]["text"] = "instrumental fade"
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(other_text)

    def test_reason_is_required(self):
        def blank_reason(timing):
            timing["tracks"][0]["unsung_source_lines"][0]["reason"] = "  "
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(blank_reason)

    def test_line_number_must_exist_and_be_declared_once(self):
        def out_of_range(timing):
            timing["tracks"][0]["unsung_source_lines"][0]["source_line"] = 9
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(out_of_range)

        def twice(timing):
            record = timing["tracks"][0]["unsung_source_lines"][0]
            timing["tracks"][0]["unsung_source_lines"].append(copy.deepcopy(record))
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(twice)

    def test_a_line_cannot_be_both_unsung_and_an_approved_sung_repeat(self):
        with self.assertRaisesRegex(SubtitleError, "invalid unsung source line declaration"):
            self.prepare(extras={"1:1": 1})

    def test_declaring_every_line_of_a_track_is_rejected(self):
        def all_unsung(timing):
            timing["tracks"][1]["unsung_source_lines"] = [{
                "source_line": 1, "text": "only line", "reason": "claimed unsung", "evidence": [EVIDENCE],
            }]
        with self.assertRaisesRegex(SubtitleError, "every source line declared unsung"):
            self.prepare(all_unsung)

    def test_malformed_declaration_container_fails_closed(self):
        def not_a_list(timing):
            timing["tracks"][0]["unsung_source_lines"] = {"source_line": 1}
        with self.assertRaisesRegex(SubtitleError, "malformed unsung_source_lines"):
            self.prepare(not_a_list)


if __name__ == "__main__":
    unittest.main()
