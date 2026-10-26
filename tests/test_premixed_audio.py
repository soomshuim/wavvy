"""Retained-premix checks must not weaken the individual-WAV contract."""

import copy
import csv
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from PIL import Image
from tests.artwork_fixture import make_artwork
from wavvy_harness.video_artwork import MANIFEST as ARTWORK_MANIFEST, check_video_artwork

from wavvy import ProjectPaths, cli, validate_project, verify_release_package
from wavvy_harness.gate import run_gate
from wavvy_harness.premixed_audio import audio_packet_fingerprint, MANIFEST, chapter_timestamp, check_premixed_audio, check_premixed_render
from wavvy_harness.state import build_state, check_state


class PremixedAudioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.series = self.root / "SERIES/20-00"
        (self.series / "input").mkdir(parents=True)
        (self.series / "output").mkdir()
        (self.series / "production").mkdir()
        self.audio = self.series / "output/mix.m4a"
        self.audio.write_bytes(b"retained-complete-two-cycle-aac")
        self.video = self.series / "output/final-premix.mp4"
        self.video.write_bytes(b"rendered-premix-video")
        make_artwork(self.series)
        image = self.series / "input/video-background.png"
        artwork = check_video_artwork(self.series)[0]
        self.sources = [{"order": i, "title": f"Song {i}", "candidate_id": f"id-{i}", "sha256": f"{i:064x}",
                         "path": f"SERIES/20-00/input/tracks/{i:02d}.wav"} for i in range(1, 21)]
        self.entries = [{"cycle": n // 20 + 1, "order": n % 20 + 1, "mix_entry_sample": n * 480000,
                         "mix_entry_seconds": n * 10, "title": self.sources[n % 20]["title"],
                         "source_path": self.sources[n % 20]["path"]} for n in range(40)]
        script = self.root / "scripts/mix.py"
        script.parent.mkdir()
        script.write_text("retained producer", encoding="utf-8")
        basis = self.write("input/basis.json", {"workspace": "[20:00]", "tracks": [
            {"order": s["order"], "approved_title": s["title"], "candidate_id": s["candidate_id"]} for s in self.sources]})
        download = self.write("input/download-manifest.json", {"workspace": "[20:00]", "selection_basis_path": self.repo_path(basis),
            "selection_basis_sha256": self.sha(basis), "tracks": [{"order": s["order"], "approved_title": s["title"],
                "candidate_id": s["candidate_id"], "sha256": s["sha256"], "input_filename": Path(s["path"]).name} for s in self.sources]})
        ledger = self.write("input/suno-candidates.json", {"workspace": {"name": "[20:00]", "id": "workspace-id"}, "settings": {"lyrics_marker": "[Instrumental]"},
            "tracks": [{"order": s["order"], "decision": {"chosen_candidate_id": s["candidate_id"]}} for s in self.sources]})
        config = self.write("production/base.json", {"sources": self.sources})
        baseline = self.write("production/baseline.json", {"configuration_path": self.repo_path(config), "configuration_sha256": self.sha(config)})
        hashes = [{"order": s["order"], "expected": s["sha256"], "actual": s["sha256"]} for s in self.sources]
        repeat = self.write("production/repeat.json", {"base_config": self.ref(config, self.root), "base_manifest": self.ref(baseline, self.root),
            "base_script": self.ref(script, self.root), "source_hashes": hashes, "repeat_count": 2, "track_occurrences": 40,
            "transition_occurrences": 39, "expected_samples": 19200000, "sample_rate_hz": 48000})
        mix = self.write("production/mix-manifest.json", {"configuration_path": self.repo_path(repeat), "configuration_sha256": self.sha(repeat),
            "script_path": self.repo_path(script), "script_sha256": self.sha(script), "baseline_manifest_path": self.repo_path(baseline),
            "baseline_manifest_sha256": self.sha(baseline), "repeat_count": 2, "track_occurrences": 40, "transition_occurrences": 39,
            "transition_acceptance": {"all39_accepted": True}, "source20_hashes_after": hashes,
            "timeline": {"track_entries": self.entries, "expected_samples": 19200000, "expected_seconds": 400},
            "lossless_pcm_stream_validation": {"total_samples": 19200000},
            "listening_copy": {"path": self.repo_path(self.audio), "sha256": self.sha(self.audio)}})
        validation = self.write("production/render-validation.json", {"technical_assertions_passed": True})
        self.record = self.write("production/render.json", {"schema": "wavvy.series_local_premix_video.v1", "video_artwork": artwork["binding"],
            "image": self.ref(image, self.root), "audio": dict(self.ref(self.audio, self.root), cycles_already_in_source=2, extra_repetitions=0),
            "source_manifest": self.ref(mix, self.root), "chapter_entries": self.entries,
            "runs": {"full": {"status": "validated", "exit_code": 0, "sources_unchanged": True,
                "validation": dict(self.ref(validation, self.root), technical_assertions_passed=True), "output": self.repo_path(self.video),
                "output_sha256": self.sha(self.video), "command": ["ffmpeg", "-i", str(image), "-i", str(self.audio),
                    "-i", str(self.series / "output/chapters.ffmetadata"), "-vf", "scale=3840:2160:flags=lanczos,setsar=1", "-c:a", "copy"]}}})
        self.archive = {"schema": "wavvy.final_premixed_audio.v1", "vocal_mode": "instrumental", "raw_prompt_status": "unverified",
            "repeat_count": 2, "additional_repeats": 0, "audio": self.ref(self.audio), "image": self.ref(image),
            "mix_manifest": self.ref(mix), "download_manifest": self.ref(download), "selection_basis": self.ref(basis),
            "source_ledger": self.ref(ledger), "render": dict(self.ref(self.video), record=self.ref(self.record))}
        self.save_archive()
        self.metadata = {"title": "Playlist | Run 🏃 | ROCK | Running | Wavvy | 20:00", "description": "\n".join(
            f"{chapter_timestamp(e['mix_entry_seconds'])} - {e['order']:02d}. {e['title']}" + (" (반복)" if e["cycle"] == 2 else "") for e in self.entries), "tags": "running,rock"}
        self.concept = (f"## Final Premixed Audio\n\n- Manifest: `{MANIFEST}`\n- **Final vocal direction**: Instrumental.\n\n"
                        "## YouTube Metadata\n\n" + "\n\n".join(f"### {key.title()}\n\n```text\n{value}\n```" for key, value in self.metadata.items()))
        (self.series / "concept.md").write_text(self.concept, encoding="utf-8")
        self.csv()
        self.audio_stream = {"codec_type": "audio", "codec_name": "aac", "sample_rate": "48000", "channels": 2,
                             "duration": "400", "duration_ts": 19200000, "time_base": "1/48000", "start_pts": 0}
        self.video_probe = {"streams": [{"codec_type": "video", "codec_name": "h264", "width": 3840, "height": 2160, "avg_frame_rate": "1/1"}, self.audio_stream],
            "format": {"duration": "400.34"}, "chapters": [{"start_time": e["mix_entry_seconds"],
                "tags": {"title": f"{e['order']:02d}. {e['title']} (cycle {e['cycle']})"}} for e in self.entries]}
        self.mock_probe = patch("wavvy_harness.premixed_audio.ffmpeg.probe", side_effect=self.probe)
        self.mock_probe.start()
        self.addCleanup(self.mock_probe.stop)
        self.mock_packets = patch("wavvy_harness.premixed_audio.audio_packet_fingerprint", return_value="identical-full-packets")
        self.mock_packets.start()
        self.addCleanup(self.mock_packets.stop)

    def sha(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def repo_path(self, path):
        return str(path.relative_to(self.root))

    def ref(self, path, parent=None):
        return {"path": str(path.relative_to(parent or self.series)), "sha256": self.sha(path)}

    def write(self, relative, data):
        path = self.series / relative
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def save_archive(self):
        self.write(MANIFEST, self.archive)

    def csv(self, **changes):
        row = dict(self.metadata, video_path=str(self.video), thumbnail_path=str(self.series / "input/thumb.jpg"))
        row.update(changes)
        with (self.series / "output/upload.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(row))
            writer.writeheader()
            writer.writerow(row)

    def probe(self, path, **kwargs):
        return copy.deepcopy(self.video_probe if Path(path).resolve() == self.video.resolve() else {"streams": [self.audio_stream]})

    def source(self):
        opted, data, errors = check_premixed_audio(self.series)
        self.assertTrue(opted)
        self.assertEqual(errors, [], errors)
        return data

    def test_valid_retained_premix_without_any_individual_wavs(self):
        self.source()
        self.assertTrue(validate_project(ProjectPaths(self.series)).is_valid)
        self.assertEqual(verify_release_package(ProjectPaths(self.series)), [])
        state = build_state(self.series, self.root)
        self.assertEqual(state["phase"], "upload_ready")
        self.assertEqual(state["artifact_status"]["audio_files"], 0)
        self.assertEqual(state["artifact_status"]["available_audio_files"], 1)
        self.assertEqual(state["artifact_status"]["final_mkv"], "missing")
        self.assertEqual(state["artifact_status"]["report_json"], "missing")
        self.assertIn("SERIES/20-00/" + MANIFEST, state["authoritative_docs"])
        self.assertNotIn("final.mkv", build_state(self.series, self.root, phase="render_final")["next_action"])
        gated = run_gate(self.series, self.root, "upload-ready", {"is_valid": True, "youtube_metadata": self.metadata})
        self.assertEqual(gated["result"], "PASS", gated["blockers"])

    def test_source_stage_does_not_require_render(self):
        self.video.unlink()
        self.record.unlink()
        (self.series / "output/upload.csv").unlink()
        self.source()
        self.assertEqual(check_state(self.series, self.root, {"phase": "source_final"})["result"], "PASS")
        gate = run_gate(self.series, self.root, "source-final", {"is_valid": True})
        self.assertEqual(gate["result"], "PASS", gate["blockers"])
        gate = run_gate(self.series, self.root, "render-final", {"is_valid": True, "youtube_metadata": self.metadata})
        self.assertEqual(gate["result"], "FAIL")

    def test_incomplete_opt_in_cannot_fall_back_to_wavs(self):
        (self.series / "concept.md").write_text(self.concept.replace("## Final Premixed Audio", "## Other"), encoding="utf-8")
        self.assertTrue(check_premixed_audio(self.series)[2])
        self.assertFalse(validate_project(ProjectPaths(self.series)).is_valid)
        self.assertTrue(verify_release_package(ProjectPaths(self.series)))

    def test_source_identity_repeat_timeline_and_provenance_mutations_fail(self):
        original = copy.deepcopy(self.archive)
        for key, value in [("additional_repeats", 1), ("repeat_count", 4), ("raw_prompt_status", "confirmed"), ("vocal_mode", "vocal")]:
            with self.subTest(key=key):
                self.archive = dict(original, **{key: value})
                self.save_archive()
                self.assertTrue(check_premixed_audio(self.series)[2])
        self.archive = original
        self.save_archive()
        mix_path = self.series / self.archive["mix_manifest"]["path"]
        original_mix = json.loads(mix_path.read_text())
        for field, value in [("order", 19), ("mix_entry_sample", -1), ("mix_entry_seconds", 11), ("title", "Wrong")]:
            with self.subTest(field=field):
                changed = copy.deepcopy(original_mix)
                changed["timeline"]["track_entries"][1][field] = value
                mix_path.write_text(json.dumps(changed), encoding="utf-8")
                self.archive["mix_manifest"] = self.ref(mix_path)
                self.save_archive()
                self.assertTrue(check_premixed_audio(self.series)[2])
        mix_path.write_text(json.dumps(original_mix), encoding="utf-8")
        self.archive["mix_manifest"] = self.ref(mix_path)
        self.save_archive()
        self.audio.write_bytes(b"replaced-mix")
        self.assertTrue(check_premixed_audio(self.series)[2])

    def test_candidate_id_and_historical_hash_drift_fail(self):
        download_path = self.series / self.archive["download_manifest"]["path"]
        original = json.loads(download_path.read_text())
        for key, value in [("candidate_id", "wrong"), ("sha256", "0" * 64)]:
            changed = copy.deepcopy(original)
            changed["tracks"][0][key] = value
            download_path.write_text(json.dumps(changed), encoding="utf-8")
            self.archive["download_manifest"] = self.ref(download_path)
            self.save_archive()
            self.assertTrue(check_premixed_audio(self.series)[2])

    def test_video_packet_chapter_codec_and_duration_mutations_fail(self):
        data = self.source()
        original = copy.deepcopy(self.video_probe)
        for mutate in [lambda p: p["streams"][0].update(width=1920),
                       lambda p: p["streams"][1].update(duration_ts=19100000),
                       lambda p: p["format"].update(duration="402"),
                       lambda p: p["chapters"][1].update(start_time=9)]:
            self.video_probe = copy.deepcopy(original)
            mutate(self.video_probe)
            self.assertTrue(check_premixed_render(self.series, data))
        self.video_probe = original
        with patch("wavvy_harness.premixed_audio.audio_packet_fingerprint", side_effect=lambda p: str(p)):
            self.assertTrue(any("packet identity" in e for e in check_premixed_render(self.series, data)))

    def test_csv_and_description_must_match_actual_forty_starts(self):
        data = self.source()
        self.csv(video_path="wrong.mp4")
        self.assertTrue(check_premixed_render(self.series, data, metadata=self.metadata, require_csv=True))
        self.csv()
        changed = dict(self.metadata, description=self.metadata["description"].replace("00:10", "00:11", 1))
        self.csv(description=changed["description"])
        self.assertTrue(check_premixed_render(self.series, data, metadata=changed, require_csv=True))

    def test_cleanup_is_only_valid_after_upload_completion_evidence(self):
        self.source()
        self.audio.unlink()
        self.video.unlink()
        (self.series / "output/upload.csv").unlink()
        self.assertTrue(check_premixed_audio(self.series)[2])
        gate = run_gate(self.series, self.root, "uploaded", {"is_valid": False})
        self.assertEqual(gate["result"], "FAIL")
        (self.series / "concept.md").write_text(self.concept + "\n\n## Upload Status\n\nYouTube upload completed\n", encoding="utf-8")
        gate = run_gate(self.series, self.root, "uploaded", {"is_valid": validate_project(ProjectPaths(self.series)).is_valid})
        self.assertEqual(gate["result"], "PASS", gate["blockers"])
        state = build_state(self.series, self.root)
        self.assertEqual(state["artifact_status"]["premixed_video"], "deleted_after_upload")
        self.assertNotIn("regenerated with pack", state["next_action"])

    def test_negative_upload_prose_does_not_open_uploaded_or_cleanup_gates(self):
        # This exact sentence triggered the production false positive. Keep it
        # outside Upload Status too, rather than rewriting it to hide the defect.
        negative = "\n실제 공개·업로드 완료 기록은 아니다.\n"
        concept = self.concept + negative + "\n## Upload Status\n\n- YouTube upload: not uploaded yet\n"
        for text in [self.concept + negative, concept]:
            with self.subTest(explicit_pending="## Upload Status" in text):
                (self.series / "concept.md").write_text(text, encoding="utf-8")
                state = build_state(self.series, self.root)
                self.assertEqual(state["artifact_status"]["youtube_upload"], "missing")
                self.assertEqual(state["phase"], "upload_ready")
                gate = run_gate(self.series, self.root, "uploaded", {"is_valid": True, "youtube_metadata": self.metadata})
                self.assertEqual(gate["result"], "FAIL")
        self.audio.unlink()
        self.video.unlink()
        (self.series / "output/upload.csv").unlink()
        self.assertFalse(validate_project(ProjectPaths(self.series)).is_valid)
        self.assertTrue(verify_release_package(ProjectPaths(self.series)))
        state = build_state(self.series, self.root)
        self.assertEqual(state["artifact_status"]["youtube_upload"], "missing")
        self.assertEqual(state["artifact_status"]["premixed_video"], "missing")
        for stage in ["source-final", "render-final", "upload-ready", "uploaded"]:
            with self.subTest(stage=stage):
                gate = run_gate(self.series, self.root, stage, {"is_valid": False, "youtube_metadata": self.metadata})
                self.assertEqual(gate["result"], "FAIL")

    def test_missing_video_is_not_uploaded_cleanup_before_upload(self):
        self.video.unlink()
        (self.series / "concept.md").write_text(self.concept + "\n## Upload Status\n\n- YouTube upload: not uploaded yet\n", encoding="utf-8")
        self.assertTrue(validate_project(ProjectPaths(self.series)).is_valid)
        self.assertTrue(verify_release_package(ProjectPaths(self.series)))
        self.assertEqual(build_state(self.series, self.root)["artifact_status"]["premixed_video"], "missing")
        for stage in ["render-final", "upload-ready", "uploaded"]:
            gate = run_gate(self.series, self.root, stage, {"is_valid": True, "youtube_metadata": self.metadata})
            self.assertEqual(gate["result"], "FAIL")

    def test_pack_refuses_to_merge_or_repeat_a_premix(self):
        result = CliRunner().invoke(cli, ["pack", str(self.series), "-y"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("already mixed/repeated", result.output)

    def test_pending_old_image_contract_cannot_bypass_artwork_rule(self):
        (self.series / ARTWORK_MANIFEST).unlink()
        self.archive["image"] = self.ref(self.series / "input/thumb.jpg")
        self.save_archive()
        self.assertTrue(any("Video artwork" in error for error in check_premixed_audio(self.series)[2]))

    def test_legacy_uploaded_artwork_requires_retained_render_identity(self):
        (self.series / ARTWORK_MANIFEST).unlink()
        self.archive["image"] = self.ref(self.series / "input/thumb.jpg")
        record = json.loads(self.record.read_text())
        record["image"] = self.ref(self.series / "input/thumb.jpg", self.root)
        record["runs"]["full"]["command"][2] = str(self.series / "input/thumb.jpg")
        self.record.write_text(json.dumps(record), encoding="utf-8")
        self.archive["render"]["record"] = self.ref(self.record)
        self.save_archive()
        (self.series / "concept.md").write_text(self.concept + "\n## Upload Status\n- YouTube upload: completed\n", encoding="utf-8")
        self.source()
        self.assertEqual(check_premixed_render(self.series, self.source(), require_csv=True), [])
        record["runs"]["full"]["output_sha256"] = "0" * 64
        self.record.write_text(json.dumps(record), encoding="utf-8")
        self.archive["render"]["record"] = self.ref(self.record)
        self.save_archive()
        self.assertTrue(any("legacy uploaded" in error for error in check_premixed_audio(self.series)[2]))

    def test_premix_render_and_csv_bind_separate_image_roles(self):
        data = self.source()
        self.csv(thumbnail_path=str(data["image"]))
        self.assertTrue(any("separate YouTube" in error for error in check_premixed_render(self.series, data, require_csv=True)))
        self.csv()
        record = json.loads(self.record.read_text())
        record.pop("video_artwork")
        self.record.write_text(json.dumps(record), encoding="utf-8")
        self.archive["render"]["record"] = self.ref(self.record)
        self.save_archive()
        self.assertTrue(any("video artwork manifest" in error for error in check_premixed_render(self.series, self.source())))


class CorrectedRepeatPremixTests(unittest.TestCase):
    # Reuse the complete release fixture while giving the current producer its
    # actual original-WAV -> correction-record -> corrected-WAV evidence chain.
    sha = PremixedAudioTests.sha
    repo_path = PremixedAudioTests.repo_path
    ref = PremixedAudioTests.ref
    write = PremixedAudioTests.write
    save_archive = PremixedAudioTests.save_archive
    csv = PremixedAudioTests.csv
    probe = PremixedAudioTests.probe
    source = PremixedAudioTests.source

    def setUp(self):
        PremixedAudioTests.setUp(self)
        (self.series / "input/originals").mkdir()
        (self.series / "input/corrected").mkdir()
        sources, acquired, selected = [], [], []
        for source in self.sources:
            order, title, identity = source["order"], source["title"], source["candidate_id"]
            original = self.series / f"input/originals/{order:02d}.wav"
            original.write_bytes(f"original-{order}".encode())
            corrected = self.series / f"input/corrected/{order:02d}.wav"
            corrected.write_bytes(f"corrected-{order}".encode())
            analysis = self.write(f"production/analysis-{order}.json", {"order": order})
            correction = self.write(f"production/correction-{order}.json", {
                "schema": "wavvy.tempo_corrected_source.v1", "order": order, "title": title,
                "candidate_id": identity, "target_bpm": 180,
                "source_path": self.repo_path(original), "source_sha256": self.sha(original),
                "output_path": self.repo_path(corrected), "output_sha256": self.sha(corrected),
                "analysis_path": self.repo_path(analysis), "analysis_sha256": self.sha(analysis)})
            beat = self.write(f"production/beats-{order}.json", {
                "schema": "wavvy.independent_corrected_beats.v1", "order": order, "title": title,
                "audio_path": self.repo_path(corrected), "audio_sha256": self.sha(corrected),
                "correction_record_sha256": self.sha(correction)})
            sources.append(dict(source, path=self.repo_path(corrected), sha256=self.sha(corrected),
                correction_record=self.repo_path(correction), correction_record_sha256=self.sha(correction),
                beat_record=self.repo_path(beat), beat_record_sha256=self.sha(beat)))
            acquired.append({"order": order, "approved_title": title, "candidate_id": identity,
                "input_filename": original.name, "sha256": self.sha(original)})
            selected.append({"order": order, "title": title, "candidate_id": identity})
        download = self.write("input/download-manifest.json", {"workspace": "[20:00]", "tracks": acquired})
        selection = self.write("input/selected-current.json", {"workspace": "[20:00]", "tracks": selected})
        ledger = self.write("production/reacquisition.json", {"schema": "wavvy.reacquisition.v1", "workspace": "[20:00]", "tracks": acquired})
        plan = self.write("production/plan-current.json", {"schema": "wavvy.continuous_180_plan.v1", "series": "20-00",
            "sources": sources, "failures": [], "target_bpm": 180, "repeat_count": 2, "additional_repeats": 0, "sample_rate": 48000})
        chunks = []
        cursor = 0
        for n in range(40):
            if n:
                chunks.append({"kind": "transition", "label": f"{(n - 1) % 20 + 1:02d}-{n % 20 + 1:02d}",
                    "samples": 48000, "mix_start_sample": cursor, "mix_end_sample": cursor + 48000})
                cursor += 48000
            count = 480000 if n == 0 else 432000
            chunks.append({"kind": "body", "cycle": n // 20 + 1, "order": n % 20 + 1,
                "samples": count, "mix_start_sample": cursor, "mix_end_sample": cursor + count})
            cursor += count
        # Incoming transition starts remain the actual chapter starts.
        self.entries = [dict(e, mix_entry_sample=(0 if n == 0 else n * 480000),
                             source_path=sources[n % 20]["path"]) for n, e in enumerate(self.entries)]
        mix_path = self.series / self.archive["mix_manifest"]["path"]
        mix = {"schema": "wavvy.continuous_mix.repeat2.v1", "series": "20-00", "plan_path": self.repo_path(plan),
            "plan_sha256": self.sha(plan), "producer_script_path": self.repo_path(self.root / "scripts/mix.py"),
            "producer_script_sha256": self.sha(self.root / "scripts/mix.py"), "sources": sources,
            "repeat_count": 2, "additional_repeats": 0, "sample_rate": 48000, "pcm_stream_samples": cursor,
            "audio_path": self.repo_path(self.audio), "audio_sha256": self.sha(self.audio),
            "timeline": {"expected_samples": cursor, "expected_seconds": cursor / 48000,
                         "track_entries": self.entries, "chunks": chunks},
            "transition_results": [{"label": f"{n:02d}-{n % 20 + 1:02d}", "technical_gate_pass": True} for n in range(1, 21)]}
        mix_path.write_text(json.dumps(mix))
        self.archive.update(mix_manifest=self.ref(mix_path), download_manifest=self.ref(download),
                            selection_basis=self.ref(selection), source_ledger=self.ref(ledger))
        record = json.loads(self.record.read_text())
        record["source_manifest"] = self.ref(mix_path, self.root)
        record["chapter_entries"] = self.entries
        self.record.write_text(json.dumps(record))
        self.archive["render"]["record"] = self.ref(self.record)
        self.save_archive()

    def test_original_and_corrected_hashes_are_distinct_valid_evidence(self):
        data = self.source()
        self.assertEqual(data["duration"], 400)
        self.assertEqual(check_premixed_render(self.series, data, metadata=self.metadata, require_csv=True), [])
        self.assertTrue(validate_project(ProjectPaths(self.series)).is_valid)

    def test_wrong_selected_id_order_and_reacquired_hash_fail(self):
        for name, key, value in [("selection_basis", "candidate_id", "wrong"),
                                 ("selection_basis", "order", 2),
                                 ("download_manifest", "sha256", "0" * 64)]:
            path = self.series / self.archive[name]["path"]
            original = path.read_text()
            changed = json.loads(original)
            changed["tracks"][0][key] = value
            path.write_text(json.dumps(changed))
            self.archive[name] = self.ref(path)
            self.save_archive()
            with self.subTest(name=name, key=key):
                self.assertTrue(check_premixed_audio(self.series)[2])
            path.write_text(original)
            self.archive[name] = self.ref(path)
            self.save_archive()

    def test_changed_corrected_wav_and_producer_script_fail(self):
        for path in [self.series / "input/corrected/01.wav", self.root / "scripts/mix.py"]:
            original = path.read_bytes()
            path.write_bytes(b"changed")
            self.assertTrue(check_premixed_audio(self.series)[2])
            path.write_bytes(original)

    def test_corrected_source_media_cleanup_requires_recorded_upload(self):
        for directory in ["input/originals", "input/corrected"]:
            for path in (self.series / directory).glob("*.wav"):
                path.unlink()
        self.audio.unlink()
        self.video.unlink()
        (self.series / "output/upload.csv").unlink()
        self.assertFalse(validate_project(ProjectPaths(self.series)).is_valid)
        self.assertEqual(run_gate(self.series, self.root, "uploaded", {"is_valid": False})["result"], "FAIL")
        (self.series / "concept.md").write_text(self.concept + "\n## Upload Status\n\n- YouTube upload: completed\n")
        self.assertTrue(validate_project(ProjectPaths(self.series)).is_valid)
        # Preparing another upload still requires the actual media package.
        self.assertTrue(verify_release_package(ProjectPaths(self.series)))
        gate = run_gate(self.series, self.root, "uploaded", {"is_valid": True, "youtube_metadata": self.metadata})
        self.assertEqual(gate["result"], "PASS", gate["blockers"])
        state = build_state(self.series, self.root)
        self.assertEqual(state["phase"], "uploaded")
        self.assertEqual(state["artifact_status"]["premixed_video"], "deleted_after_upload")
        self.assertEqual(state["artifact_status"]["available_audio_files"], 0)

    def test_uploaded_cleanup_still_rejects_present_media_hash_changes(self):
        (self.series / "concept.md").write_text(self.concept + "\n## Upload Status\n\n- YouTube upload: completed\n")
        for relative in ["input/originals/01.wav", "input/corrected/01.wav"]:
            path = self.series / relative
            original = path.read_bytes()
            path.write_bytes(b"changed-after-upload")
            with self.subTest(relative=relative):
                self.assertFalse(validate_project(ProjectPaths(self.series)).is_valid)
                self.assertTrue(check_premixed_audio(self.series, allow_uploaded_cleanup=True)[2])
            path.write_bytes(original)

    def test_uploaded_cleanup_still_requires_nonmedia_provenance(self):
        (self.series / "concept.md").write_text(self.concept + "\n## Upload Status\n\n- YouTube upload: completed\n")
        for relative in ["production/analysis-1.json", "production/correction-1.json", "production/beats-1.json", "production/plan-current.json"]:
            path = self.series / relative
            original = path.read_bytes()
            path.unlink()
            with self.subTest(relative=relative):
                self.assertTrue(check_premixed_audio(self.series, allow_uploaded_cleanup=True)[2])
            path.write_bytes(original)

    def test_forty_start_must_match_actual_transition_not_just_be_increasing(self):
        path = self.series / self.archive["mix_manifest"]["path"]
        original = path.read_text()
        for mutate in [lambda m: m["timeline"]["track_entries"].pop(),
                       lambda m: m["timeline"]["track_entries"][1].update(mix_entry_sample=528000, mix_entry_seconds=11),
                       lambda m: m["timeline"]["chunks"][1].update(label="20-01")]:
            changed = json.loads(original)
            mutate(changed)
            path.write_text(json.dumps(changed))
            self.archive["mix_manifest"] = self.ref(path)
            self.save_archive()
            self.assertTrue(check_premixed_audio(self.series)[2])

    def test_real_aac_payload_mutation_is_detected_without_changing_packet_timing(self):
        original = self.series / "output/real-aac.m4a"
        changed = self.series / "output/changed-aac.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-f", "lavfi", "-i",
                        "sine=frequency=997:sample_rate=48000:duration=0.1", "-ac", "2",
                        "-c:a", "aac", str(original)], check=True, capture_output=True)
        command = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
                   "-show_entries", "packet=pts,dts,duration,size,pos", "-of", "json"]
        packets = json.loads(subprocess.check_output(command + [str(original)]))["packets"]
        payload = bytearray(original.read_bytes())
        packet = packets[1]
        payload[int(packet["pos"]) + int(packet["size"]) // 2] ^= 1
        changed.write_bytes(payload)
        changed_packets = json.loads(subprocess.check_output(command + [str(changed)]))["packets"]
        self.assertEqual(packets, changed_packets)
        self.assertNotEqual(audio_packet_fingerprint(original), audio_packet_fingerprint(changed))

    def test_historical_individual_archive_does_not_override_current_premix(self):
        self.write("input/final-selected-audio-sources.json", {"schema": "historical", "tracks": []})
        (self.series / "concept.md").write_text(self.concept + "\n## Previous Selected Audio Sources — historical\n")
        result = check_state(self.series, self.root, {"phase": "source_final"})
        self.assertEqual(result["result"], "PASS", result["blockers"])
        self.assertEqual(result["state"]["artifact_status"]["selected_audio_sources"], "missing")
        self.assertEqual(result["state"]["artifact_status"]["premixed_audio"], "verified")

    def test_invalid_current_premix_cannot_fall_back_to_historical_archive(self):
        self.write("input/final-selected-audio-sources.json", {"schema": "historical", "tracks": []})
        self.archive["audio"]["sha256"] = "0" * 64
        self.save_archive()
        result = check_state(self.series, self.root, {"phase": "source_final"})
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("premix audio differs" in error for error in result["blockers"]), result["blockers"])
        self.assertEqual(result["state"]["artifact_status"]["premixed_audio"], "invalid")

    def test_two_current_final_source_declarations_fail_instead_of_picking_one(self):
        self.write("input/final-selected-audio-sources.json", {"schema": "historical", "tracks": []})
        (self.series / "concept.md").write_text(self.concept + "\n## Final Selected Audio Sources\n")
        result = check_state(self.series, self.root, {"phase": "source_final"})
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("cannot also declare" in error for error in result["blockers"]), result["blockers"])

    def test_changed_final_aac_payload_is_rejected_by_shared_render_check(self):
        data = self.source()
        with patch("wavvy_harness.premixed_audio.audio_packet_fingerprint", side_effect=lambda p: "changed" if Path(p).resolve() == self.video.resolve() else "original"):
            errors = check_premixed_render(self.series, data)
        self.assertTrue(any("AAC packet identity differs" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
