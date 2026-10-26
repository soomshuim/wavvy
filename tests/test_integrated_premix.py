"""The integrated gate binds real files and rejects independently altered links."""

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.artwork_fixture import make_artwork
from wavvy_harness.integrated_premix import ARCHIVE_SCHEMA, validate_integrated_premix
from wavvy_harness.premixed_audio import MANIFEST, check_premixed_audio


class IntegratedPremixTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.series = self.repo / "SERIES/19-30"
        self.prod = "SERIES/19-30/production/"
        self.shapes = {}
        self.sources, self.selected, self.captures, self.catalog, self.independent = [], [], [], [], []
        for order in range(1, 21):
            identity = {"song_id": f"selected-id-{order}", "title": "Goodbye" if order == 1 else f"Song {order}"}
            raw = self.media(f"work/raw/{order}.wav", 60000)
            valid = self.media(f"work/source/{order}.wav", 48000)
            corrected = self.media(f"work/corrected/{order}.wav", 40000 + order)
            analysis = self.write(f"work/analysis/{order}.json", {"original_modified": False})
            original_map = self.write(f"{self.prod}source-map-{order}.json", {
                "raw_sha256": raw["sha256"], "raw_valid_frames": [100, 48100],
                **self.flat(valid, "valid_source"), "musical_source_trimmed": False,
                **self.flat(analysis, "source_analysis")})
            time_map = self.write(f"{self.prod}time-map-{order}.json", {
                "schema": "wavvy.capture_170_rubberband_time_map.v1", **identity, "order": order,
                **self.flat(raw, "raw"), "raw_valid_frames": [100, 48100], "pitch_semitones": 0,
                "input_frames": 48000, "output_frames": 40000 + order,
                "input_source0_through_natural_end": True,
                "complete_map_input": [0, 1000, 20000, 40000, 48000],
                "complete_map_output": [0, 1000, 17941, 34882, 40000 + order],
                "key_frames_output": [1000, 17941, 34882],
                **self.flat(valid, "valid_source"), **self.flat(original_map, "source_time_map")})
            qa = self.write(f"{self.prod}qa-{order}.json", {
                "schema": "wavvy.rubberband_output_numerical_check.v1", "passed": True,
                "expected_output_frames": 40000 + order, "actual_output_frames": 40000 + order,
                "finite": True, "pitch": {"passed": True}})
            beat = self.write(f"{self.prod}beat-{order}.json", {
                "schema": "wavvy.rubberband_independent_output_beats.v1", **identity, "order": order,
                **self.flat(corrected, "audio")})
            alias = self.write(f"{self.prod}alias-{order}.json", {"raw_model_family": "mixed; preserved"})
            self.independent.append({**beat, "order": order, **self.flat(alias, "alias_diagnosis")})
            self.sources.append({"schema": "wavvy.capture_170_rubberband_corrected_source.v1", **identity,
                "order": order, **self.flat(raw, "raw"), "source_valid_frames": [100, 48100],
                "source_duration_seconds": 1, **self.flat(time_map, "source_time_map"),
                **self.flat(corrected, "output"), "output_samples": 40000 + order,
                "first_grid_beat_sample": 1000, "grid_beat_count": 3,
                "source_start_preserved": True, "source_end_preserved": True, "target_bpm": 170,
                **self.flat(qa, "output_qa")})
            self.selected.append({**identity, "position": order, "raw_sha256": raw["sha256"]})
            self.captures.append({**identity, **self.flat(raw, "raw"), "raw_duration_seconds": 60000/48000,
                "source_duration_seconds": 1, "estimated_source_raw_start_seconds": 100/48000,
                "capture_verified": True, "raw_closed": True, "write_error": "none", "zero_signal": False,
                "source_playback_rate": 1, "unexpected_pause_events": [], "pts_frame_offset_gaps": 0,
                "pts_gap_over_one_sample_count": 0})
            self.catalog.append({"id": identity["song_id"], "title": identity["title"]})
        catalog_ref = self.write(f"{self.prod}catalog.json", {"songs": self.catalog})
        capture_ref = self.write(f"{self.prod}captures.json", {"songs": self.captures,
            "source_catalog": catalog_ref["path"], "source_catalog_sha256": catalog_ref["sha256"]})
        selection_ref = self.write(f"{self.prod}selection.json", {"schema": "wavvy.1930.final_sequence.v1",
            "tracks": self.selected, "first_track_fixed": self.selected[0]["song_id"]})
        entries, transitions, cursor = [], [], 0
        for index in range(40):
            source = self.sources[index % 20]
            start = 0 if index == 0 else cursor - 1000
            cursor = start + source["output_samples"]
            entry = {"entry": index + 1, "cycle": index // 20 + 1, "order": index % 20 + 1,
                "song_id": source["song_id"], "title": source["title"], "mix_start_sample": start,
                "mix_end_sample": cursor, "samples": cursor-start, "mix_start_seconds": start/48000,
                "mix_end_seconds": cursor/48000, "corrected_source_frames": [0, source["output_samples"]],
                "corrected_path": source["output_path"], "corrected_sha256": source["output_sha256"],
                "first_grid_beat_sample_global": start+1000}
            entries.append(entry)
            if index:
                transitions.append({"number": index, "outgoing_entry": index, "incoming_entry": index+1,
                    "repeat_boundary_20_to_1": index == 20, "start_sample": start,
                    "end_sample": start+1000, "overlap_samples": 1000, "overlap_seconds": 1000/48000})
        self.plan = {"schema": "wavvy.capture_170_whole_source_repeat2_plan.v1", "target_bpm": 170,
            "sample_rate": 48000, "repeat_count": 2, "additional_repeats": 0,
            "musical_source_trimmed": False, "sources": self.sources, "entries": entries,
            "transitions": transitions, "samples": cursor}
        plan_ref = self.write(f"{self.prod}plan170.json", self.plan)
        master = self.media("work/master170.wav", cursor)
        encode170 = self.write(f"{self.prod}encode170.json", {"wav_sha256": master["sha256"]})
        qa170 = self.write(f"{self.prod}qa170.json", {
            "schema": "wavvy.capture_170_repeat2_technical_validation.v1", "passed": True,
            "planned_samples": cursor, "decoded_samples": {"wav": cursor}, "source_hash_checks": [
                {"song_id": s["song_id"], "sha256": s["raw_sha256"], "unchanged": True} for s in self.sources]})
        producer = self.write(f"{self.prod}producer.py", "retained producer", raw=True)
        for source in self.sources:
            source["producer_script_sha256"] = producer["sha256"]
        plan_ref = self.write(f"{self.prod}plan170.json", self.plan)
        upstream = {**{k:v for k,v in self.plan.items() if k != "sources"},
            "schema": "wavvy.capture_170_whole_source_repeat2.v1", "series": "19-30", "source_count": 20,
            **self.flat(plan_ref, "mix_plan"), **self.flat(master, "wav"),
            **self.flat(encode170, "encode_record"), **self.flat(qa170, "validation"),
            "producer_code": [producer], "independent_output_measurements": self.independent}
        upstream_ref = self.write(f"{self.prod}upstream.json", upstream)
        scale = lambda x: (x*17+8)//16
        samples = scale(cursor)
        self.entries = [{**e, "mix_start_sample": scale(e["mix_start_sample"]),
            "mix_end_sample": scale(e["mix_end_sample"]),
            "samples": scale(e["mix_end_sample"])-scale(e["mix_start_sample"]),
            "mix_start_seconds": scale(e["mix_start_sample"])/48000,
            "mix_end_seconds": scale(e["mix_end_sample"])/48000,
            "first_grid_beat_sample_global": scale(e["first_grid_beat_sample_global"]),
            "upstream_170_entry": copy.deepcopy(e),
            "upstream_170_mix_frames": [e["mix_start_sample"], e["mix_end_sample"]]} for e in entries]
        trans = [{**t, "start_sample": scale(t["start_sample"]), "end_sample": scale(t["end_sample"]),
            "overlap_samples": scale(t["end_sample"])-scale(t["start_sample"]),
            "overlap_seconds": (scale(t["end_sample"])-scale(t["start_sample"]))/48000,
            "upstream_170_frames": [t["start_sample"], t["end_sample"]]} for t in transitions]
        intermediate = self.media("work/uniform160.wav", samples)
        self.wav = self.media("SERIES/19-30/output/final.wav", samples)
        self.aac = self.write("SERIES/19-30/output/final.m4a", "one AAC generation", raw=True)
        transform = self.write(f"{self.prod}transform-record.json", {
            "schema": "wavvy.integrated_170_to_160_transform.v1", **self.flat(master, "input"),
            **self.flat(intermediate, "output"), "input_frames": cursor, "output_frames": samples,
            "ratio_numerator": 17, "ratio_denominator": 16, "pitch_semitones": 0,
            "whole_input_preserved": True, "original_170_unchanged": True})
        encode = self.write(f"{self.prod}encode-record.json", {
            "schema": "wavvy.integrated_160_encode.v1", **self.flat(intermediate, "input"),
            **self.flat(self.wav, "wav"), **self.flat(self.aac, "aac"), "same_final_pcm_split": True,
            "aac_encode_generations": 1})
        timeline = self.write(f"{self.prod}timeline.json", {"schema": "wavvy.integrated_160_timeline.v1",
            "ratio": [17, 16], "samples": samples, "entries": self.entries, "transitions": trans,
            **self.flat(plan_ref, "source_170_plan")})
        windows = [{"kind": kind, "number": n, "replay_to_final_lag_samples": 0,
            "replay_to_final_mono_correlation": .99999999} for kind,n in
            [("transition", n) for n in range(1,40)] + [("body", n) for n in (1,4,11,16,20,21,40)]]
        replay = self.write(f"{self.prod}loudnorm-replay-qa.json", {
            "schema": "wavvy.exact_loudnorm_replay_qa.v1", "passed": True,
            **self.flat(intermediate, "source_intermediate"), **self.flat(self.wav, "final_wav"),
            "final_aac_sha256": self.aac["sha256"], **self.flat(encode, "encode_record"),
            "full_stream_frames": samples, "maximum_absolute_pcm_difference": 1e-7, "windows": windows})
        packets = self.write(f"{self.prod}aac-packet-validation.json", {"gaps": [], "stream_end_sample": samples,
            "packet_count": 100, "first_packet": {"pts": -1024, "side_data_list": [{"skip_samples": 1024}]},
            "last_packet": {"pts": samples-1024, "duration": 1024}})
        numerical = self.write(f"{self.prod}numerical-checks.json", {
            "schema": "wavvy.integrated_160_numerical_checks.v1", "passed": True,
            "checks": [{"kind": w["kind"], "number": w["number"],
                "attack_alignment": {"passed": True}, "source_170_frames": [100, 200],
                "output_160_frames": [scale(100), scale(200)], "pitch": {"passed": True}} for w in windows[:44]]})
        render_code = self.write(f"{self.prod}render-160.py", "160 producer", raw=True)
        replay_code = self.write(f"{self.prod}loudnorm-replay-qa.py", "replay QA", raw=True)
        levels = {k: {"source_sha256": r["sha256"], "integrated_lufs": -14.0, "true_peak_dbtp": -1.3}
            for k,r in (("wav",self.wav),("m4a",self.aac))}
        validation = self.write(f"{self.prod}final-technical-validation.json", {
            "schema": "wavvy.integrated_160_technical_validation.v1", "passed": True,
            "source_170_unchanged": True, "source_170_sha256": master["sha256"],
            "expected_samples": samples, "actual_wav_samples": samples,
            "aac_padding_samples": 4, "actual_aac_decoded_samples": samples+4,
            "entry_count": 40, "transition_count": 39, "repeat_boundary_count": 1,
            "exact_sequence_twice": True, **self.flat(replay, "exact_loudnorm_replay"), "final_loudness": levels})
        self.mix = {"schema": "wavvy.integrated_170_to_160_delivery.v1", "target_bpm": 160,
            "sample_rate": 48000, "channels": 2, "ratio_numerator": 17, "ratio_denominator": 16,
            "repeat_count": 2, "additional_repeats": 0, "entry_count": 40, "transition_count": 39,
            "whole_integrated_master_stretched_once": True, "original_twenty_sources_rerendered": False,
            "pitch_semitones": 0, **self.flat(master, "source_170"), "source_170_preserved": True,
            **self.flat(upstream_ref, "source_170_manifest"), "samples": samples,
            "duration_seconds": samples/48000, "entries": self.entries, "transitions": trans,
            **self.flat(self.wav, "wav"), **self.flat(self.aac, "aac"),
            "evidence": [transform,encode,timeline,replay,packets,numerical,validation,render_code,replay_code]}
        self.mix_ref = self.write(f"{self.prod}mix.json", self.mix)
        self.archive = {"schema": ARCHIVE_SCHEMA, "raw_prompt_status": "unverified", "vocal_mode": "instrumental",
            "repeat_count": 2, "additional_repeats": 0, "capture_manifest": self.series_ref(capture_ref),
            "selection_basis": self.series_ref(selection_ref), "mix_manifest": self.series_ref(self.mix_ref),
            "audio": self.series_ref(self.aac)}
        self.probe_mock = patch("wavvy_harness.integrated_premix.ffmpeg.probe", side_effect=self.probe)
        self.probe_mock.start()
        self.addCleanup(self.probe_mock.stop)

    def write(self, name, value, *, raw=False):
        path = self.repo/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if raw else json.dumps(value), encoding="utf-8")
        return {"path":name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}

    def media(self, name, frames):
        ref = self.write(name, f"media:{name}:{frames}", raw=True)
        self.shapes[str((self.repo/name).resolve())] = frames
        return ref

    def flat(self, ref, prefix):
        return {f"{prefix}_path": ref["path"], f"{prefix}_sha256": ref["sha256"]}

    def series_ref(self, ref):
        return {"path":str((self.repo/ref["path"]).relative_to(self.series)), "sha256":ref["sha256"]}

    def probe(self, path, **kwargs):
        if Path(path).resolve() == (self.repo/self.aac["path"]).resolve():
            return {"streams":[{"codec_name":"aac","sample_rate":"48000","channels":2,
                "duration": str(self.mix["samples"]/48000)}]}
        return {"streams":[{"codec_name":"pcm_f32le","sample_rate":"48000","channels":2,
            "duration_ts":self.shapes[str(Path(path).resolve())],"time_base":"1/48000"}]}

    def check(self, **kwargs):
        return validate_integrated_premix(self.series, self.archive, self.mix, **kwargs)

    def alter_proof(self, filename, change):
        ref = next(r for r in self.mix["evidence"] if Path(r["path"]).name == filename)
        value = json.loads((self.repo/ref["path"]).read_text())
        change(value)
        ref.update(self.write(ref["path"], value))

    def test_valid_chain_and_exact_chapter_normalization(self):
        sources, rate, samples, entries, audio = self.check()
        self.assertEqual((len(sources),rate,samples,len(entries)), (20,48000,self.mix["samples"],40))
        self.assertEqual(audio,self.aac)
        self.assertEqual(entries[20]["cycle"],2)
        self.assertEqual(entries,[{**e,"mix_entry_sample":e["mix_start_sample"],
            "mix_entry_seconds":e["mix_start_seconds"]} for e in self.entries])

    def test_changed_raw_bytes_rejected(self):
        (self.repo/self.sources[4]["raw_path"]).write_bytes(b"different recording")
        with self.assertRaisesRegex(ValueError,"file/hash differs"):
            self.check()

    def test_actual_corrected_frame_count_checked(self):
        self.shapes[str((self.repo/self.sources[0]["output_path"]).resolve())] += 1
        with self.assertRaisesRegex(ValueError,"actual WAV.*frame count"):
            self.check()

    def test_selection_order_swap_rejected(self):
        self.mix["entries"][1]["song_id"] = self.mix["entries"][2]["song_id"]
        with self.assertRaisesRegex(ValueError,"timeline/length|cycle/order/ID/title"):
            self.check()

    def test_second_cycle_relabel_rejected(self):
        self.mix["entries"][20]["cycle"] = 1
        self.alter_proof("timeline.json", lambda d:d["entries"][20].update(cycle=1))
        with self.assertRaisesRegex(ValueError,"cycle/order/ID/title"):
            self.check()

    def test_globally_retimed_entry_required(self):
        self.mix["entries"][0]["first_grid_beat_sample_global"] += 1
        self.alter_proof("timeline.json",lambda d:d["entries"][0].update(
            first_grid_beat_sample_global=self.mix["entries"][0]["first_grid_beat_sample_global"]))
        with self.assertRaisesRegex(ValueError,"globally rounded"):
            self.check()

    def test_missing_raw_blocks_pending_release(self):
        (self.repo/self.sources[0]["raw_path"]).unlink()
        with self.assertRaisesRegex(ValueError,"file missing"):
            self.check()
        self.assertEqual(len(self.check(allow_uploaded_cleanup=True)[0]),20)

    def test_cleanup_does_not_hide_changed_retained_media(self):
        (self.repo/self.sources[0]["raw_path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError,"file/hash differs"):
            self.check(allow_uploaded_cleanup=True)

    def test_path_escape_rejected_even_with_matching_file_hash(self):
        self.archive["selection_basis"]["path"] = "../../outside.json"
        with self.assertRaisesRegex(ValueError,"escapes parent"):
            self.check()

    def test_unknown_prompts_cannot_be_promoted(self):
        self.archive["raw_prompt_status"] = "confirmed"
        with self.assertRaisesRegex(ValueError,"unknown prompts"):
            self.check()

    def test_transform_ratio_and_pitch_are_required(self):
        for field,value in (("ratio_numerator",16),("pitch_semitones",1)):
            with self.subTest(field=field):
                original=self.mix[field]; self.mix[field]=value
                with self.assertRaisesRegex(ValueError,"transform/repeat"):
                    self.check()
                self.mix[field]=original

    def test_self_reported_pass_cannot_hide_replay_error(self):
        self.alter_proof("loudnorm-replay-qa.json",lambda d:d.update(maximum_absolute_pcm_difference=.01))
        with self.assertRaisesRegex(ValueError,"replay identity/residual"):
            self.check()

    def test_nan_loudness_rejected(self):
        self.alter_proof("final-technical-validation.json",lambda d:d["final_loudness"]["m4a"].update(integrated_lufs=float("nan")))
        with self.assertRaisesRegex(ValueError,"loudness/peak/hash"):
            self.check()

    def test_aac_gap_rejected(self):
        self.alter_proof("aac-packet-validation.json",lambda d:d.update(gaps=[{"at":100}]))
        with self.assertRaisesRegex(ValueError,"packet extent/continuity"):
            self.check()

    def test_repeat_boundary_cannot_disappear(self):
        self.mix["transitions"][19]["repeat_boundary_20_to_1"] = False
        self.alter_proof("timeline.json",lambda d:d["transitions"][19].update(repeat_boundary_20_to_1=False))
        with self.assertRaisesRegex(ValueError,"transition adjacency"):
            self.check()

    def test_new_schema_uses_existing_audio_and_separate_artwork_check(self):
        make_artwork(self.series)
        image = self.series/"input/video-background.png"
        render = self.series/"output/final.mp4"
        render.write_bytes(b"unrendered source-only fixture")
        self.archive.update(image={"path":"input/video-background.png","sha256":hashlib.sha256(image.read_bytes()).hexdigest()},
            render={"path":"output/final.mp4"})
        self.write("SERIES/19-30/"+MANIFEST,self.archive)
        (self.series/"concept.md").write_text(f"## Final Premixed Audio\n\n- Manifest: `{MANIFEST}`\n"
            "- **Final vocal direction**: Instrumental.\n")
        active,data,errors=check_premixed_audio(self.series)
        self.assertTrue(active)
        self.assertEqual(errors,[])
        self.assertEqual(data["entries"][20]["mix_entry_sample"],self.entries[20]["mix_start_sample"])
        self.assertNotEqual(data["image"],data["thumbnail"])
        self.assertIsNotNone(data["artwork"])

    def test_legacy_archive_cannot_dispatch_integrated_mix(self):
        self.archive["schema"]="wavvy.final_premixed_audio.v1"
        with self.assertRaisesRegex(ValueError,"unsupported archive/producer schema"):
            self.check()


if __name__ == "__main__":
    unittest.main()
