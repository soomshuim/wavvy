"""Regression tests for timed lyric preparation and manual publication evidence."""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wavvy_harness.subtitles import (
    MANIFEST, SubtitleError, _sample_position, prepare_timed, subtitle_status, verify_prepared, verify_published,
)


SOURCE = Path(__file__).resolve().parents[1] / "SERIES" / "17-30"
EVIDENCE = SOURCE / "input/validation/2026-10-23-timed-subtitles"
TRACKED_REPORT = EVIDENCE / "report-at-subtitle-preparation.json"
TRACKED_SRT = EVIDENCE / "all-tracks-timed-checked.srt"


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _clone(destination):
    manifest = json.loads((SOURCE / MANIFEST).read_text(encoding="utf-8"))
    map_path = Path(manifest["timing_map"]["path"])
    mapping = json.loads((SOURCE / map_path).read_text(encoding="utf-8"))
    paths = {
        Path("concept.md"), MANIFEST, Path(manifest["report"]["path"]),
        Path(manifest["srt"]["path"]), map_path,
    }
    paths.update(map_path.parent / name for name in mapping["audio_evidence_sha256"])
    publication = manifest["publication"]
    paths.update(Path(publication[key]["path"]) for key in (
        "observation", "studio_capture", "public_menu_capture", "studio_download", "studio_raw", "public_menu_raw",
    ))
    for sample in publication["sample_files"].values():
        paths.update(Path(sample[key]["path"]) for key in ("raw_snapshot", "screenshot"))
    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        source = TRACKED_REPORT if relative == Path(manifest["report"]["path"]) else (
            TRACKED_SRT if relative == Path(manifest["srt"]["path"]) else SOURCE / relative
        )
        shutil.copyfile(source, target)
    return manifest, mapping


def _write_map(series, manifest, mapping):
    path = series / manifest["timing_map"]["path"]
    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["timing_map"]["sha256"] = _sha(path)
    (series / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class SubtitleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.series = Path(self.temp.name) / "17-30"
        self.manifest, self.mapping = _clone(self.series)

    def test_approved_series_prepared_and_published(self):
        prepared = verify_prepared(self.series)
        published = verify_published(self.series)
        self.assertEqual(prepared["cues"], 1270)
        self.assertEqual(prepared["sha256"], "29543de1cbf964fb4a6a8bbeeb0f5d9b5040f11610035aea7fb405cb69dd9226")
        self.assertEqual(published["video_id"], "3HorT4OoDhg")
        self.assertTrue(published["studio_download_compared"])

    def test_missing_repeat_fails_even_with_updated_timing_map_hash(self):
        track = self.mapping["tracks"][8]
        track["cues"] = [cue for cue in track["cues"] if not any(
            item["source_line"] == 14 and item["occurrence"] == 2
            for item in cue["source_line_occurrences"]
        )]
        _write_map(self.series, self.manifest, self.mapping)
        with self.assertRaisesRegex(SubtitleError, "missing or unauthorized sung occurrence"):
            verify_prepared(self.series)

    def test_wrong_second_pass_offset_fails(self):
        self.mapping["output_cues"][635]["start_ms"] += 1000
        _write_map(self.series, self.manifest, self.mapping)
        with self.assertRaisesRegex(SubtitleError, "repeat offset"):
            verify_prepared(self.series)

    def test_late_cue_fails_against_independent_word_observation(self):
        target = next(cue for cue in self.mapping["tracks"][15]["cues"] if cue["first_line"] == 21)
        target["relative_start_ms"] += 400
        _write_map(self.series, self.manifest, self.mapping)
        with self.assertRaisesRegex(SubtitleError, "onset outside retained observation"):
            verify_prepared(self.series)

    def test_silent_gap_extension_fails(self):
        self.mapping["tracks"][0]["cues"][0]["relative_end_ms"] = 12000
        _write_map(self.series, self.manifest, self.mapping)
        with self.assertRaisesRegex(SubtitleError, "observed ASR end"):
            verify_prepared(self.series)

    def test_report_and_lyrics_changes_fail(self):
        report_path = self.series / "output/report.json"
        report_path.write_text(report_path.read_text() + " ")
        with self.assertRaisesRegex(SubtitleError, "sha256 mismatch"):
            verify_prepared(self.series)
        shutil.copyfile(TRACKED_REPORT, report_path)
        concept = self.series / "concept.md"
        concept.write_text(concept.read_text().replace("하루가 다 지나갈 때", "하루가 다시 지나갈 때"))
        with self.assertRaisesRegex(SubtitleError, "lyric source hash"):
            verify_prepared(self.series)

    def test_existing_srt_is_never_overwritten(self):
        srt = self.series / self.manifest["srt"]["path"]
        original = srt.read_bytes() + b"changed"
        srt.write_bytes(original)
        with self.assertRaisesRegex(SubtitleError, "Existing timed SRT differs"):
            prepare_timed(self.series, self.series / self.manifest["timing_map"]["path"])
        self.assertEqual(srt.read_bytes(), original)

    def test_publication_is_independent_of_preparation(self):
        self.manifest.pop("publication")
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        self.assertEqual(subtitle_status(self.series), {"prepared": "verified", "published": "unverified"})
        with self.assertRaisesRegex(SubtitleError, "publication evidence missing"):
            verify_published(self.series)

    def test_wrong_public_video_identity_fails(self):
        observation_path = self.series / self.manifest["publication"]["observation"]["path"]
        observation = json.loads(observation_path.read_text())
        observation["video_id"] = "WrongVideo1"
        observation_path.write_text(json.dumps(observation))
        self.manifest["publication"]["observation"]["sha256"] = _sha(observation_path)
        self.manifest["publication"]["video_id"] = "WrongVideo1"
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(SubtitleError, "concept upload target"):
            verify_published(self.series)

    def test_downloaded_manual_srt_text_mismatch_fails(self):
        download = self.series / self.manifest["publication"]["studio_download"]["path"]
        download.write_bytes(download.read_bytes().replace("하루가".encode(), "다른날".encode(), 1))
        self.manifest["publication"]["studio_download"]["sha256"] = _sha(download)
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(SubtitleError, "differs in timing/text"):
            verify_published(self.series)

    def test_identical_official_download_is_accepted(self):
        download = self.series / self.manifest["publication"]["studio_download"]["path"]
        download.write_bytes((self.series / self.manifest["srt"]["path"]).read_bytes())
        self.manifest["publication"]["studio_download"]["sha256"] = _sha(download)
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        self.assertEqual(verify_published(self.series)["result"], "PASS")

    def test_scalar_cue_and_sample_fail_closed(self):
        self.mapping["tracks"][0]["cues"][0] = 12
        _write_map(self.series, self.manifest, self.mapping)
        with self.assertRaisesRegex(SubtitleError, "malformed cue"):
            verify_prepared(self.series)
        shutil.copyfile(SOURCE / self.manifest["timing_map"]["path"], self.series / self.manifest["timing_map"]["path"])
        self.manifest["timing_map"]["sha256"] = _sha(self.series / self.manifest["timing_map"]["path"])
        observation_path = self.series / self.manifest["publication"]["observation"]["path"]
        observation = json.loads(observation_path.read_text())
        observation["public_watch_samples"] = [17]
        observation_path.write_text(json.dumps(observation))
        self.manifest["publication"]["observation"]["sha256"] = _sha(observation_path)
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(SubtitleError, "samples missing"):
            verify_published(self.series)

    def test_malformed_report_fails_closed(self):
        report_path = self.series / "output/report.json"
        report = json.loads(report_path.read_text())
        report["tracks"][0].pop("duration")
        report_path.write_text(json.dumps(report))
        self.manifest["report"]["sha256"] = _sha(report_path)
        (self.series / MANIFEST).write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(SubtitleError, "Invalid report tracks"):
            verify_prepared(self.series)


class NewSeriesSubtitleTests(unittest.TestCase):
    def test_first_and_last_actual_lyrics_allow_long_intro_and_outro(self):
        self.assertTrue(_sample_position("first", 1, 100, 180_000, 1, 3_600_000))
        self.assertTrue(_sample_position("ending", 100, 100, 3_000_000, 1, 3_600_000))
        self.assertFalse(_sample_position("first", 2, 100, 180_000, 1, 3_600_000))

    def test_prepare_creates_srt_and_manifest_hash_without_prior_output_cues(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = Path(tmp) / "12-00"
            (series / "input").mkdir(parents=True)
            (series / "output").mkdir()
            (series / "concept.md").write_text(
                "# New Series\n\n## Final Track Sources\n\n### 01. Song\n\n"
                "#### LYRICS\n\n```text\n[Verse]\n안녕 오늘\n```\n",
                encoding="utf-8",
            )
            report = {
                "processing_params": {"repeat": 2, "fade": 0.8},
                "summary": {"final_duration": 139.2},
                "tracks": [{"order": 1, "title": "Song", "duration": 70}],
            }
            report_path = series / "output/report.json"
            report_path.write_text(json.dumps(report))
            evidence_path = series / "input/observed-word.json"
            evidence_path.write_text(json.dumps({"transcription": {"segments": [{"words": [{"word": "안녕", "start": 1.0}]}]}}))
            mapping = {
                "schema": "wavvy.subtitle-timing.v1",
                "audio_evidence_sha256": {"observed-word.json": _sha(evidence_path)},
                "tracks": [{"track": 1, "cues": [{
                    "relative_start_ms": 1000, "relative_end_ms": 5000,
                    "last_asr_end_ms": 5000, "anchor_classes": ["direct_cue"],
                    "source_line_occurrences": [{"source_line": 1, "occurrence": 1, "text": "안녕 오늘"}],
                    "texts": ["안녕 오늘"],
                }]}],
            }
            map_path = series / "input/timing.json"
            map_path.write_text(json.dumps(mapping, ensure_ascii=False))
            manifest = {
                "schema": "wavvy.subtitles.v1",
                "report": {"path": "output/report.json", "sha256": _sha(report_path)},
                "timing_map": {"path": "input/timing.json", "sha256": _sha(map_path)},
                "srt": {"path": "output/youtube_subtitles_ko_timed_estimated.srt"},
                "observed_anchor_checks": [{
                    "track": 1, "source_line": 1, "occurrence": 1,
                    "evidence": "observed-word.json", "clip_start_ms": 0,
                    "first_word": "안녕", "max_onset_delta_ms": 100,
                }],
            }
            (series / MANIFEST).write_text(json.dumps(manifest))
            self.assertFalse((series / manifest["srt"]["path"]).exists())
            result = prepare_timed(series, map_path)
            self.assertEqual(result["cues"], 2)
            self.assertEqual(verify_prepared(series)["sha256"], result["sha256"])
            saved = json.loads((series / MANIFEST).read_text())
            self.assertEqual(saved["srt"]["sha256"], result["sha256"])
            self.assertEqual(saved["source_sha256"], result["source_sha256"])
            self.assertEqual(
                (series / manifest["srt"]["path"]).read_text(encoding="utf-8"),
                "1\n00:00:01,000 --> 00:00:05,000\n안녕 오늘\n\n"
                "2\n00:01:10,200 --> 00:01:14,200\n안녕 오늘\n",
            )
            concept = series / "concept.md"
            concept.write_text(concept.read_text(encoding="utf-8").replace("안녕 오늘", "다른 가사"), encoding="utf-8")
            with self.assertRaisesRegex(SubtitleError, "lyric source hash"):
                verify_prepared(series)


if __name__ == "__main__":
    unittest.main()
