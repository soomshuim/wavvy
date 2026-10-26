"""Retained capture → 170 two-cycle master → uniform 160 delivery evidence.

This is a source-evidence contract, not an artwork/render check or a new DSP run.
Historical listening flags and pulse ambiguities are not rewritten by this gate.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

import ffmpeg

ARCHIVE_SCHEMA = "wavvy.final_integrated_premixed_audio.v1"
MIX_SCHEMA = "wavvy.integrated_170_to_160_delivery.v1"
RATE = 48000


def _scaled(sample: int) -> int:
    # Producer contract: nearest sample, exact .5 rounded upward, globally.
    return (sample * 17 + 8) // 16


def _require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(f"integrated premix: {message}")


def _integer(value: object, *, positive: bool = False) -> bool:
    return type(value) is int and (value > 0 if positive else value >= 0)


def _finite(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def _path(parent: Path, value: str) -> Path:
    _require(isinstance(value, str) and bool(value) and not Path(value).is_absolute(), "unsafe evidence path")
    path = (parent / value).resolve()
    _require(path.is_relative_to(parent.resolve()), f"evidence path escapes parent: {value}")
    return path


class _Evidence:
    def __init__(self, repo: Path, allow_missing_media: bool):
        self.repo = repo
        self.allow_missing_media = allow_missing_media
        self.hashes: dict[Path, str] = {}

    def bound(self, ref: dict, *, parent: Path | None = None, media: bool = False) -> Path:
        path = _path(parent or self.repo, ref["path"])
        digest = ref.get("sha256")
        _require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
                 f"invalid SHA256: {path.name}")
        if not path.exists() and media and self.allow_missing_media:
            return path
        _require(path.is_file(), f"evidence file missing: {path}")
        if path not in self.hashes:
            result = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    result.update(chunk)
            self.hashes[path] = result.hexdigest()
        _require(self.hashes[path] == digest, f"evidence file/hash differs: {path}")
        return path

    def record(self, ref: dict, *, parent: Path | None = None) -> dict:
        path = self.bound(ref, parent=parent)
        data = json.loads(path.read_text(encoding="utf-8"))
        _require(isinstance(data, dict), f"record must contain an object: {path}")
        return data

    def named(self, data: dict, key: str, *, media: bool = False) -> Path:
        return self.bound({"path": data[f"{key}_path"], "sha256": data[f"{key}_sha256"]}, media=media)

    def wav(self, path: Path, frames: int) -> None:
        _require(_integer(frames, positive=True), f"invalid media frame count: {path.name}")
        if not path.exists() and self.allow_missing_media:
            return
        streams = ffmpeg.probe(str(path)).get("streams", [])
        _require(len(streams) == 1, f"WAV must contain one audio stream: {path.name}")
        stream = streams[0]
        actual = Fraction(stream["duration_ts"]) * Fraction(stream["time_base"]) * RATE
        _require(stream.get("codec_name", "").startswith("pcm_")
                 and int(stream.get("sample_rate", 0)) == RATE and stream.get("channels") == 2
                 and actual == frames, f"actual WAV rate/channels/frame count differs: {path.name}")


def _ref(data: dict, key: str) -> dict:
    return {"path": data[f"{key}_path"], "sha256": data[f"{key}_sha256"]}


def _identity(data: dict) -> tuple:
    return data.get("song_id"), data.get("title")


def _timeline(entries: list, transitions: list, sources: list, samples: int) -> None:
    _require(_integer(samples, positive=True) and len(entries) == 40 and len(transitions) == 39,
             "timeline requires 40 entries and 39 transitions")
    for index, entry in enumerate(entries):
        order, cycle = index % 20 + 1, index // 20 + 1
        source = sources[order - 1]
        start, end = entry["mix_start_sample"], entry["mix_end_sample"]
        _require((entry.get("entry"), entry.get("cycle"), entry.get("order")) == (index + 1, cycle, order)
                 and _identity(entry) == _identity(source), "timeline cycle/order/ID/title differs")
        _require(_integer(start) and _integer(end, positive=True) and start < end <= samples
                 and entry.get("samples") == end - start
                 and (index != 0 or start == 0)
                 and (index == 0 or entries[index - 1]["mix_start_sample"] < start),
                 "timeline entry sample extent differs")
        _require(all(_finite(entry.get(key)) and abs(entry[key] - value / RATE) < 1 / RATE
                     for key, value in (("mix_start_seconds", start), ("mix_end_seconds", end))),
                 "timeline sample/seconds differ")
    _require(entries[-1]["mix_end_sample"] == samples, "timeline natural final end differs")
    for index, transition in enumerate(transitions):
        outgoing, incoming = entries[index:index + 2]
        start, end = incoming["mix_start_sample"], outgoing["mix_end_sample"]
        _require((transition.get("number"), transition.get("outgoing_entry"), transition.get("incoming_entry"))
                 == (index + 1, index + 1, index + 2)
                 and transition.get("repeat_boundary_20_to_1") is (index == 19)
                 and (transition.get("start_sample"), transition.get("end_sample")) == (start, end)
                 and end > start and transition.get("overlap_samples") == end - start
                 and _finite(transition.get("overlap_seconds"))
                 and abs(transition["overlap_seconds"] - (end - start) / RATE) < 1 / RATE,
                 "timeline transition adjacency/overlap differs")


def _sources(files: _Evidence, series: Path, archive: dict, plan: dict, upstream: dict) -> list:
    chosen = files.record(archive["selection_basis"], parent=series)
    captures = files.record(archive["capture_manifest"], parent=series)
    catalog = files.record({"path": captures["source_catalog"], "sha256": captures["source_catalog_sha256"]})
    selected, recorded, public, sources = chosen["tracks"], captures["songs"], catalog["songs"], plan["sources"]
    _require(chosen.get("schema") == "wavvy.1930.final_sequence.v1"
             and all(isinstance(items, list) and len(items) == 20 for items in (selected, recorded, public, sources)),
             "selection/capture/production must contain exactly 20 sources")
    selected_ids = [item["song_id"] for item in selected]
    recorded_by_id = {item["song_id"]: item for item in recorded}
    public_by_id = {item["id"]: item for item in public}
    _require(len(set(selected_ids)) == len(recorded_by_id) == len(public_by_id) == 20
             and set(selected_ids) == set(recorded_by_id) == set(public_by_id)
             and chosen.get("first_track_fixed") == selected_ids[0] and selected[0].get("title") == "Goodbye",
             "selected 20 IDs/first Goodbye differ")
    independent = upstream["independent_output_measurements"]
    _require(len(independent) == 20, "independent corrected-source measurements missing")
    for order, (source, selection, measure) in enumerate(zip(sources, selected, independent), 1):
        capture = recorded_by_id[selection["song_id"]]
        published = public_by_id[selection["song_id"]]
        _require(source.get("schema") == "wavvy.capture_170_rubberband_corrected_source.v1"
                 and source.get("order") == selection.get("position") == measure.get("order") == order
                 and _identity(source) == _identity(selection) == _identity(capture)
                 and source["song_id"] == published["id"] and source["title"] == published["title"],
                 f"source {order}: selected ID/title/order differs")
        _require(capture.get("capture_verified") is True and capture.get("raw_closed") is True
                 and capture.get("write_error") == "none" and capture.get("zero_signal") is False
                 and capture.get("source_playback_rate") == 1 and capture.get("unexpected_pause_events") == []
                 and capture.get("pts_frame_offset_gaps") == capture.get("pts_gap_over_one_sample_count") == 0,
                 f"source {order}: capture completeness evidence differs")
        _require(source["raw_sha256"] == capture["raw_sha256"] == selection["raw_sha256"]
                 and source["raw_path"] == capture["raw_path"], f"source {order}: raw capture identity differs")
        raw = files.named(source, "raw", media=True)
        files.wav(raw, round(capture["raw_duration_seconds"] * RATE))
        start = round(capture["estimated_source_raw_start_seconds"] * RATE)
        length = round(capture["source_duration_seconds"] * RATE)
        _require(source.get("source_valid_frames") == [start, start + length]
                 and start >= 0 and length > 0 and start + length <= round(capture["raw_duration_seconds"] * RATE)
                 and source.get("source_duration_seconds") == capture["source_duration_seconds"]
                 and source.get("source_start_preserved") is True and source.get("source_end_preserved") is True
                 and source.get("target_bpm") == 170,
                 f"source {order}: full valid source range differs")
        _require(source.get("producer_script_sha256") in {r["sha256"] for r in upstream["producer_code"]},
                 f"source {order}: correction producer code identity differs")
        time_map = files.record(_ref(source, "source_time_map"))
        _require(time_map.get("schema") == "wavvy.capture_170_rubberband_time_map.v1"
                 and _identity(time_map) == _identity(source) and time_map.get("order") == order
                 and time_map.get("raw_valid_frames") == source["source_valid_frames"]
                 and time_map.get("raw_path") == source["raw_path"] and time_map.get("raw_sha256") == source["raw_sha256"]
                 and time_map.get("pitch_semitones") == 0 and time_map.get("input_frames") == length
                 and time_map.get("output_frames") == source["output_samples"]
                 and time_map.get("input_source0_through_natural_end") is True,
                 f"source {order}: correction time-map identity differs")
        x, y = time_map["complete_map_input"], time_map["complete_map_output"]
        _require(len(x) == len(y) >= 3 and x[0] == y[0] == 0 and x[-1] == length and y[-1] == source["output_samples"]
                 and all(_integer(v) for v in x + y)
                 and all(a < b for values in (x, y) for a, b in zip(values, values[1:])),
                 f"source {order}: correction map omits/reorders source extent")
        beats = time_map["key_frames_output"]
        _require(len(beats) == source["grid_beat_count"] >= 2 and beats == y[1:-1]
                 and beats[0] == source["first_grid_beat_sample"]
                 and all(abs(beat - beats[0] - round(Fraction(n * RATE * 60, 170))) <= 1
                         for n, beat in enumerate(beats)), f"source {order}: 170 sample grid differs")
        valid = files.named(time_map, "valid_source", media=True)
        files.wav(valid, length)
        original_map = files.record(_ref(time_map, "source_time_map"))
        _require(original_map.get("raw_sha256") == source["raw_sha256"]
                 and original_map.get("raw_valid_frames") == source["source_valid_frames"]
                 and original_map.get("valid_source_path") == time_map["valid_source_path"]
                 and original_map.get("valid_source_sha256") == time_map["valid_source_sha256"]
                 and original_map.get("musical_source_trimmed") is False,
                 f"source {order}: extracted source evidence differs")
        files.named(original_map, "source_analysis")
        output = files.named(source, "output", media=True)
        files.wav(output, source["output_samples"])
        qa = files.record(_ref(source, "output_qa"))
        _require(qa.get("schema") == "wavvy.rubberband_output_numerical_check.v1" and qa.get("passed") is True
                 and qa.get("expected_output_frames") == qa.get("actual_output_frames") == source["output_samples"]
                 and qa.get("finite") is True and qa.get("pitch", {}).get("passed") is True,
                 f"source {order}: corrected-source numerical QA differs")
        beat_record = files.record(measure)
        _require(beat_record.get("schema") == "wavvy.rubberband_independent_output_beats.v1"
                 and _identity(beat_record) == _identity(source) and beat_record.get("order") == order
                 and beat_record.get("audio_path") == source["output_path"]
                 and beat_record.get("audio_sha256") == source["output_sha256"],
                 f"source {order}: independent output identity differs")
        files.bound({"path": measure["alias_diagnosis_path"], "sha256": measure["alias_diagnosis_sha256"]})
    return sources


def validate_integrated_premix(series: Path, archive: dict, mix: dict, *, allow_uploaded_cleanup: bool = False
                               ) -> tuple[list, int, int, list, dict]:
    """Return sources/rate/samples/chapter entries/audio ref; raise on bad evidence.

    Archive paths are series-relative; existing producer paths are repo-relative.
    Cleanup relaxation applies only to media after the caller verifies upload.
    Every retained file is still hashed, including during uploaded inspection.
    """
    series = series.resolve()
    files = _Evidence(series.parent.parent, allow_uploaded_cleanup)
    _require(archive.get("schema") == ARCHIVE_SCHEMA and mix.get("schema") == MIX_SCHEMA,
             "unsupported archive/producer schema")
    _require(archive.get("raw_prompt_status") == "unverified", "unknown prompts must remain unverified")
    _require(mix.get("target_bpm") == 160 and mix.get("sample_rate") == RATE and mix.get("channels") == 2
             and mix.get("ratio_numerator") == 17 and mix.get("ratio_denominator") == 16
             and all(d.get("repeat_count") == 2 and d.get("additional_repeats") == 0 for d in (archive, mix))
             and mix.get("entry_count") == 40 and mix.get("transition_count") == 39
             and mix.get("whole_integrated_master_stretched_once") is True
             and mix.get("original_twenty_sources_rerendered") is False and mix.get("pitch_semitones") == 0,
             "160 transform/repeat contract differs")
    upstream = files.record(_ref(mix, "source_170_manifest"))
    plan = files.record(_ref(upstream, "mix_plan"))
    _require(upstream.get("schema") == "wavvy.capture_170_whole_source_repeat2.v1"
             and plan.get("schema") == "wavvy.capture_170_whole_source_repeat2_plan.v1"
             and upstream.get("series") == series.name and upstream.get("source_count") == 20
             and all(d.get("target_bpm") == 170 and d.get("sample_rate") == RATE
                     and d.get("repeat_count") == 2 and d.get("additional_repeats") == 0
                     and d.get("musical_source_trimmed") is False for d in (upstream, plan))
             and upstream.get("entries") == plan.get("entries") and upstream.get("transitions") == plan.get("transitions")
             and upstream.get("samples") == plan.get("samples"), "upstream 170 production contract differs")
    for ref in upstream["producer_code"]:
        files.bound(ref)
    sources = _sources(files, series, archive, plan, upstream)
    _timeline(plan["entries"], plan["transitions"], sources, plan["samples"])
    for entry in plan["entries"]:
        source = sources[entry["order"] - 1]
        _require(entry.get("corrected_source_frames") == [0, source["output_samples"]]
                 and entry.get("samples") == source["output_samples"]
                 and entry.get("corrected_path") == source["output_path"]
                 and entry.get("corrected_sha256") == source["output_sha256"],
                 "170 entry omits or substitutes a corrected source")
    master170 = files.named(upstream, "wav", media=True)
    files.wav(master170, plan["samples"])
    _require(_path(files.repo, mix["source_170_path"]) == master170
             and mix["source_170_sha256"] == upstream["wav_sha256"] and mix.get("source_170_preserved") is True,
             "160 input is not the retained 170 master")
    qa170 = files.record(_ref(upstream, "validation"))
    encode170 = files.record(_ref(upstream, "encode_record"))
    _require(qa170.get("schema") == "wavvy.capture_170_repeat2_technical_validation.v1" and qa170.get("passed") is True
             and qa170.get("planned_samples") == qa170.get("decoded_samples", {}).get("wav") == plan["samples"]
             and encode170.get("wav_sha256") == upstream["wav_sha256"], "170 master validation/encoding differs")
    _require([(s.get("song_id"), s.get("sha256"), s.get("unchanged")) for s in qa170["source_hash_checks"]]
             == [(s["song_id"], s["raw_sha256"], True) for s in sources], "170 raw source hash checks differ")
    proofs, proof_refs = {}, {}
    for ref in mix["evidence"]:
        path = files.bound(ref)
        _require(path.name not in proof_refs, "duplicate named 160 evidence")
        proof_refs[path.name] = ref
        if path.suffix == ".json":
            proofs[path.name] = files.record(ref)
    _require({"render-160.py", "loudnorm-replay-qa.py"} <= proof_refs.keys(), "160 producer/QA code refs missing")
    transform, encode = proofs["transform-record.json"], proofs["encode-record.json"]
    timeline, validation = proofs["timeline.json"], proofs["final-technical-validation.json"]
    samples = _scaled(plan["samples"])
    _require(_integer(mix.get("samples"), positive=True) and mix["samples"] == samples
             and _finite(mix.get("duration_seconds")) and abs(mix["duration_seconds"] - samples / RATE) < 1 / RATE
             and timeline.get("schema") == "wavvy.integrated_160_timeline.v1" and timeline.get("ratio") == [17, 16]
             and timeline.get("samples") == samples and timeline.get("entries") == mix["entries"]
             and timeline.get("transitions") == mix["transitions"]
             and _ref(timeline, "source_170_plan") == _ref(upstream, "mix_plan"), "160 timeline/length binding differs")
    _timeline(mix["entries"], mix["transitions"], sources, samples)
    for old, new in zip(plan["entries"], mix["entries"]):
        _require(new.get("upstream_170_entry") == old
                 and new.get("upstream_170_mix_frames") == [old["mix_start_sample"], old["mix_end_sample"]]
                 and all(new.get(k) == _scaled(old[k])
                         for k in ("mix_start_sample", "mix_end_sample", "first_grid_beat_sample_global"))
                 and all(new.get(k) == old[k] for k in ("corrected_source_frames", "corrected_sha256", "corrected_path")),
                 "160 entry is not the globally rounded 17/16 upstream entry")
    for old, new in zip(plan["transitions"], mix["transitions"]):
        _require(new.get("upstream_170_frames") == [old["start_sample"], old["end_sample"]]
                 and all(new.get(k) == _scaled(old[k]) for k in ("start_sample", "end_sample")),
                 "160 transition is not the globally rounded upstream overlap")
    _require(transform.get("schema") == "wavvy.integrated_170_to_160_transform.v1"
             and transform.get("input_path") == mix["source_170_path"] and transform.get("input_sha256") == mix["source_170_sha256"]
             and transform.get("input_frames") == plan["samples"] and transform.get("output_frames") == samples
             and transform.get("ratio_numerator") == 17 and transform.get("ratio_denominator") == 16
             and transform.get("pitch_semitones") == 0 and transform.get("whole_input_preserved") is True
             and transform.get("original_170_unchanged") is True, "uniform transform evidence differs")
    intermediate = files.named(transform, "output", media=True)
    files.wav(intermediate, samples)
    wav, aac = files.named(mix, "wav", media=True), files.named(mix, "aac", media=True)
    files.wav(wav, samples)
    _require(encode.get("schema") == "wavvy.integrated_160_encode.v1"
             and _ref(encode, "input") == _ref(transform, "output")
             and _ref(encode, "wav") == _ref(mix, "wav") and _ref(encode, "aac") == _ref(mix, "aac")
             and encode.get("same_final_pcm_split") is True and encode.get("aac_encode_generations") == 1,
             "final encoding is not bound to the transformed PCM")
    replay = proofs["loudnorm-replay-qa.json"]
    _require(replay.get("schema") == "wavvy.exact_loudnorm_replay_qa.v1" and replay.get("passed") is True
             and _ref(replay, "source_intermediate") == _ref(transform, "output")
             and _ref(replay, "final_wav") == _ref(mix, "wav") and replay.get("final_aac_sha256") == mix["aac_sha256"]
             and _ref(replay, "encode_record") == proof_refs["encode-record.json"]
             and replay.get("full_stream_frames") == samples
             and _finite(replay.get("maximum_absolute_pcm_difference"))
             and 0 <= replay["maximum_absolute_pcm_difference"] <= 2 * 2 ** -23,
             "exact normalization replay identity/residual differs")
    expected_windows = [("transition", n) for n in range(1, 40)] + [("body", n) for n in (1, 4, 11, 16, 20, 21, 40)]
    _require([(w.get("kind"), w.get("number")) for w in replay["windows"]] == expected_windows
             and all(w.get("replay_to_final_lag_samples") == 0
                     and _finite(w.get("replay_to_final_mono_correlation"))
                     and w["replay_to_final_mono_correlation"] > .999999 for w in replay["windows"]),
             "exact normalization replay window coverage/alignment differs")
    packets = proofs["aac-packet-validation.json"]
    _require(packets.get("gaps") == [] and packets.get("stream_end_sample") == samples
             and _integer(packets.get("packet_count"), positive=True)
             and packets["first_packet"]["pts"] == -1024
             and packets["first_packet"]["side_data_list"][0].get("skip_samples") == 1024
             and packets["last_packet"]["pts"] + packets["last_packet"]["duration"] == samples,
             "final AAC packet extent/continuity differs")
    numerical = proofs["numerical-checks.json"]
    _require(numerical.get("schema") == "wavvy.integrated_160_numerical_checks.v1" and numerical.get("passed") is True
             and [(w.get("kind"), w.get("number")) for w in numerical["checks"]] == expected_windows[:44]
             and all(w.get("attack_alignment", {}).get("passed") is True
                     and w["output_160_frames"] == [_scaled(n) for n in w["source_170_frames"]]
                     and (w["kind"] != "body" or w.get("pitch", {}).get("passed") is True)
                     for w in numerical["checks"]), "160 independent transform timing/pitch QA differs")
    _require(validation.get("schema") == "wavvy.integrated_160_technical_validation.v1"
             and validation.get("passed") is True and validation.get("source_170_unchanged") is True
             and validation.get("source_170_sha256") == mix["source_170_sha256"]
             and validation.get("expected_samples") == validation.get("actual_wav_samples") == samples
             and _integer(validation.get("aac_padding_samples")) and validation["aac_padding_samples"] < 1024
             and validation.get("actual_aac_decoded_samples") == samples + validation["aac_padding_samples"]
             and validation.get("entry_count") == 40 and validation.get("transition_count") == 39
             and validation.get("repeat_boundary_count") == 1 and validation.get("exact_sequence_twice") is True
             and _ref(validation, "exact_loudnorm_replay") == proof_refs["loudnorm-replay-qa.json"],
             "final technical validation binding differs")
    for key, ref in (("wav", _ref(mix, "wav")), ("m4a", _ref(mix, "aac"))):
        level = validation["final_loudness"][key]
        _require(level.get("source_sha256") == ref["sha256"]
                 and _finite(level.get("integrated_lufs")) and abs(level["integrated_lufs"] + 14) <= .2
                 and _finite(level.get("true_peak_dbtp")) and level["true_peak_dbtp"] <= -1,
                 f"final {key} loudness/peak/hash differs")
    # Preserve every producer field so the video record can bind exact chapters.
    entries = [{**entry, "mix_entry_sample": entry["mix_start_sample"], "mix_entry_seconds": entry["mix_start_seconds"]}
               for entry in mix["entries"]]
    return sources, RATE, samples, entries, _ref(mix, "aac")
