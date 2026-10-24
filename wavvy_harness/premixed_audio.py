"""Explicit retained-premix release evidence; individual-WAV gates stay separate."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path

import ffmpeg

MANIFEST = "production/final-premixed-audio.json"
HEADING = "Final Premixed Audio"


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain an object")
    return value


def _require(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError(detail)


def _digest(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _hash(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def _path(parent: Path, value: str) -> Path:
    _require(isinstance(value, str) and bool(value) and not Path(value).is_absolute(), "unsafe premix evidence path")
    path = (parent / value).resolve()
    _require(path.is_relative_to(parent.resolve()), f"premix evidence path escapes parent: {value}")
    return path


def _bound(parent: Path, ref: dict) -> Path:
    path = _path(parent, ref["path"])
    _require(_digest(ref.get("sha256")) and path.is_file() and _hash(path) == ref["sha256"],
             f"premix evidence file/hash differs: {ref.get('path')}")
    return path


def _section(text: str) -> str | None:
    heading = re.search(rf"(?m)^## {HEADING}\s*$", text)
    if not heading:
        return None
    tail = text[heading.end():]
    end = re.search(r"(?m)^## ", tail)
    return tail[:end.start()] if end else tail


def premixed_opt_in(series: Path) -> bool:
    concept = series / "concept.md"
    return (series / MANIFEST).exists() or (concept.is_file() and _section(concept.read_text(encoding="utf-8")) is not None)


def _producer_ref(repo: Path, data: dict, key: str) -> Path:
    return _bound(repo, {"path": data[f"{key}_path"], "sha256": data[f"{key}_sha256"]})


def check_premixed_audio(series: Path, *, allow_uploaded_cleanup: bool = False) -> tuple[bool, dict, list[str]]:
    """Validate retained source evidence only. This never requires a video or CSV."""
    series = series.resolve()
    if not premixed_opt_in(series):
        return False, {}, []
    data: dict = {}
    try:
        concept = (series / "concept.md").read_text(encoding="utf-8")
        section = _section(concept)
        _require(section is not None and MANIFEST in section, f"concept.md ## {HEADING} must reference {MANIFEST}")
        _require(re.search(r"(?im)^[-*] \*\*Final vocal direction\*\*:\s*Instrumental\b", section) is not None,
                 "premix concept must explicitly declare Final vocal direction: Instrumental")
        _require("## Final Selected Audio Sources" not in concept and "## Final Track Sources" not in concept,
                 "premix cannot also declare an individual-WAV final-source archive")
        archive = _json(series / MANIFEST)
        _require(archive.get("schema") == "wavvy.final_premixed_audio.v1" and archive.get("vocal_mode") == "instrumental",
                 "unsupported premix schema/vocal_mode")
        _require(archive.get("raw_prompt_status") == "unverified", "premix retained historical prompts must remain unverified")
        _require(type(archive.get("repeat_count")) is int and archive["repeat_count"] == 2
                 and type(archive.get("additional_repeats")) is int and archive["additional_repeats"] == 0,
                 "premix must contain exactly two cycles and zero additional repeats")
        repo = series.parent.parent
        mix = _json(_bound(series, archive["mix_manifest"]))
        repeat = _json(_producer_ref(repo, mix, "configuration"))
        _producer_ref(repo, mix, "script")
        baseline_path = _producer_ref(repo, mix, "baseline_manifest")
        baseline = _json(baseline_path)
        config_path = _bound(repo, repeat["base_config"])
        config = _json(config_path)
        _require(_bound(repo, repeat["base_manifest"]) == baseline_path, "premix baseline manifests differ")
        _require(_producer_ref(repo, baseline, "configuration") == config_path, "premix baseline configuration differs")
        _bound(repo, repeat["base_script"])
        download_path = _bound(series, archive["download_manifest"])
        download = _json(download_path)
        basis_path = _bound(series, archive["selection_basis"])
        basis = _json(basis_path)
        ledger = _json(_bound(series, archive["source_ledger"]))
        _require(_producer_ref(repo, download, "selection_basis") == basis_path, "premix selection basis differs")
        ledger_workspace = ledger.get("workspace")
        if isinstance(ledger_workspace, dict):
            ledger_workspace = ledger_workspace.get("name")
        _require(download.get("workspace") == basis.get("workspace") == ledger_workspace
                 and bool(download.get("workspace")), "premix selection workspaces differ")
        _require(ledger.get("settings", {}).get("lyrics_marker") == "[Instrumental]", "premix lacks retained instrumental source evidence")
        sources, downloaded, selected, candidates = config["sources"], download["tracks"], basis["tracks"], ledger["tracks"]
        before, after = repeat["source_hashes"], mix["source20_hashes_after"]
        _require(all(isinstance(items, list) and len(items) == 20 for items in (sources, downloaded, selected, candidates, before, after)),
                 "premix requires exactly 20 distinct selected sources and before/after hash records")
        ids = set()
        for order, (source, item, chosen, candidate, pre, post) in enumerate(zip(sources, downloaded, selected, candidates, before, after), 1):
            _require(all(type(entry.get("order")) is int and entry["order"] == order for entry in (source, item, chosen, candidate, pre, post)),
                     f"premix source {order}: source evidence order differs")
            identity = source["candidate_id"]
            _require(bool(identity) and identity not in ids and identity == item.get("candidate_id") == chosen.get("candidate_id")
                     == candidate.get("decision", {}).get("chosen_candidate_id"), f"premix source {order}: candidate ID differs")
            ids.add(identity)
            _require(source["title"] == item.get("approved_title") == chosen.get("approved_title"), f"premix source {order}: title differs")
            sha = source["sha256"]
            _require(_digest(sha) and sha == item.get("sha256") == pre.get("expected") == pre.get("actual")
                     == post.get("expected") == post.get("actual"), f"premix source {order}: historical WAV hash differs")
            _require(Path(source["path"]).name == item.get("input_filename"), f"premix source {order}: source filename differs")
        entries = mix["timeline"]["track_entries"]
        _require(mix.get("repeat_count") == repeat.get("repeat_count") == 2
                 and mix.get("track_occurrences") == repeat.get("track_occurrences") == 40
                 and mix.get("transition_occurrences") == repeat.get("transition_occurrences") == 39
                 and mix.get("transition_acceptance", {}).get("all39_accepted") is True,
                 "premix retained production must contain 40 accepted entries/39 transitions")
        rate = repeat["sample_rate_hz"]
        samples = repeat["expected_samples"]
        _require(type(rate) is int and rate == 48000 and type(samples) is int and samples > 0
                 and mix["timeline"]["expected_samples"] == samples
                 and mix["lossless_pcm_stream_validation"]["total_samples"] == samples,
                 "premix production sample count/rate differs")
        duration = samples / rate
        _require(math.isfinite(duration) and abs(float(mix["timeline"]["expected_seconds"]) - duration) <= 1 / rate,
                 "premix production duration differs")
        _require(isinstance(entries, list) and len(entries) == 40, "premix timeline must contain 40 entries")
        previous = -1
        for index, entry in enumerate(entries):
            order, cycle = index % 20 + 1, index // 20 + 1
            sample = entry["mix_entry_sample"]
            _require((entry["cycle"], entry["order"]) == (cycle, order), "premix timeline cycle/order differs")
            _require(type(sample) is int and previous < sample < samples and (index != 0 or sample == 0)
                     and abs(float(entry["mix_entry_seconds"]) - sample / rate) < 1 / rate,
                     "premix timeline start sample/time differs")
            _require((entry["title"], entry["source_path"]) == (sources[order - 1]["title"], sources[order - 1]["path"]),
                     "premix timeline source/title differs")
            previous = sample
        audio = _path(series, archive["audio"]["path"])
        _require(audio == _path(repo, mix["listening_copy"]["path"])
                 and _digest(archive["audio"].get("sha256")) and archive["audio"]["sha256"] == mix["listening_copy"]["sha256"],
                 "premix audio differs from production manifest")
        if audio.is_file():
            _bound(series, archive["audio"])
            probe = ffmpeg.probe(str(audio))
            streams = probe.get("streams", [])
            _require(len(streams) == 1 and streams[0].get("codec_name") == "aac"
                     and int(streams[0].get("sample_rate", 0)) == rate and streams[0].get("channels") == 2,
                     "premix must be the retained 48kHz stereo AAC source")
            _require(abs(float(streams[0]["duration"]) - duration) <= 0.001, "premix audio duration differs")
        else:
            _require(allow_uploaded_cleanup and _digest(archive.get("render", {}).get("sha256")),
                     "premix audio missing before recorded upload completion")
        image = _bound(series, archive["image"])
        _require(image == (series / "input/thumb.jpg").resolve(), "premix image must identify current input/thumb.jpg")
        from PIL import Image
        with Image.open(image) as opened:
            _require(opened.width > 0 and opened.height > 0, "premix JPG is invalid")
        data = {"archive": archive, "mix": mix, "entries": entries, "duration": duration,
                "audio": audio, "image": image, "render_path": _path(series, archive["render"]["path"])}
        return True, data, []
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, ffmpeg.Error) as error:
        return True, data, [f"Final Premixed Audio: {error}"]


def audio_packet_fingerprint(path: Path) -> str:
    """Hash every AAC packet's payload hash, length and original time coordinates."""
    command = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets", "-show_data_hash", "sha256",
               "-show_entries", "packet=pts,dts,duration,size,data_hash", "-of", "compact=p=0:nk=0", str(path)]
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        result = hashlib.sha256()
        count = 0
        for line in process.stdout:
            result.update(line)
            count += 1
        error = process.stderr.read().decode("utf-8", errors="replace")
        _require(process.wait() == 0 and count > 0, f"premix packet probe failed: {error}")
    return result.hexdigest()


def chapter_timestamp(seconds: float) -> str:
    total = int(round(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, second = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{second:02d}" if hours else f"{minutes:02d}:{second:02d}"


def check_premixed_render(series: Path, data: dict, *, metadata: dict | None = None,
                          require_csv: bool = False, allow_uploaded_cleanup: bool = False) -> list[str]:
    """Validate the retained premix's current video, with independent audio identity."""
    try:
        series = series.resolve()
        archive, entries = data["archive"], data["entries"]
        render = archive["render"]
        record = _json(_bound(series, render["record"]))
        repo = series.parent.parent
        _require(record.get("schema") == "wavvy.series_local_premix_video.v1", "premix render record schema differs")
        for key in ("image", "audio"):
            _require(_path(repo, record[key]["path"]) == _path(series, archive[key]["path"])
                     and record[key]["sha256"] == archive[key]["sha256"], f"premix render {key} differs")
        _require(record["audio"].get("cycles_already_in_source") == 2 and record["audio"].get("extra_repetitions") == 0,
                 "premix render must copy exactly one already-two-cycle audio input")
        _require(record.get("chapter_entries") == entries, "premix render recorded chapter entries differ")
        _require(_path(repo, record["source_manifest"]["path"]) == _path(series, archive["mix_manifest"]["path"])
                 and record["source_manifest"]["sha256"] == archive["mix_manifest"]["sha256"], "premix render production manifest differs")
        run = record["runs"]["full"]
        video = data["render_path"]
        _require(run.get("status") == "validated" and run.get("exit_code") == 0 and run.get("sources_unchanged") is True
                 and _path(repo, run["output"]) == video and _digest(render.get("sha256"))
                 and run.get("output_sha256") == render["sha256"], "premix full render completion/hash differs")
        validation = _json(_bound(repo, run["validation"]))
        _require(run["validation"].get("technical_assertions_passed") is True
                 and validation.get("technical_assertions_passed") is True, "premix direct render validation is incomplete")
        command = run["command"]
        _require(command.count("-i") == 3 and command[command.index("-c:a") + 1] == "copy"
                 and command[command.index("-vf") + 1] == "scale=3840:2160:flags=lanczos,setsar=1"
                 and "-filter_complex" not in command and "-af" not in command and "-stream_loop" not in command,
                 "premix render command must upscale the JPG and copy its audio once")
        inputs = [command[index + 1] for index, token in enumerate(command) if token == "-i"]
        _require(Path(inputs[0]).resolve() == data["image"] and Path(inputs[1]).resolve() == data["audio"],
                 "premix render command inputs differ from declared JPG/audio")
        if video.is_file():
            _bound(series, render)
            probe = ffmpeg.probe(str(video), show_chapters=None)
            videos = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
            audios = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
            _require(len(videos) == len(audios) == 1, "premix video requires exactly one video/audio stream")
            v, a = videos[0], audios[0]
            _require(v.get("codec_name") == "h264" and v.get("width") == 3840 and v.get("height") == 2160
                     and a.get("codec_name") == "aac" and int(a.get("sample_rate", 0)) == 48000 and a.get("channels") == 2,
                     "premix video must be 3840x2160 H.264 with 48kHz stereo AAC")
            if data["audio"].is_file():
                source_probe = ffmpeg.probe(str(data["audio"]))
                source_audio = source_probe["streams"][0]
                _require(a.get("time_base") == source_audio.get("time_base") and a.get("duration_ts") == source_audio.get("duration_ts")
                         and a.get("start_pts") == source_audio.get("start_pts"), "premix video audio duration/start differs from source")
                _require(audio_packet_fingerprint(video) == audio_packet_fingerprint(data["audio"]), "premix video AAC packet identity differs from source")
            else:
                _require(allow_uploaded_cleanup, "premix source audio missing for video comparison")
            frame = 1 / float(Fraction(v["avg_frame_rate"]))
            tail = float(probe["format"]["duration"]) - float(a["duration"])
            _require(0 <= tail <= frame + 0.001 and frame <= 1, "premix video duration exceeds one final-frame rounding interval")
            chapters = probe.get("chapters", [])
            _require(len(chapters) == 40, "premix embedded chapter count must be 40")
            for chapter, entry in zip(chapters, entries):
                _require(abs(float(chapter["start_time"]) - entry["mix_entry_seconds"]) <= 0.0011
                         and chapter.get("tags", {}).get("title") == f"{entry['order']:02d}. {entry['title']} (cycle {entry['cycle']})",
                         "premix embedded chapter start/title differs")
        else:
            _require(allow_uploaded_cleanup, "premix video missing before recorded upload completion")
        if require_csv:
            csv_path = series / "output/upload.csv"
            if not csv_path.is_file():
                _require(allow_uploaded_cleanup, "premix output/upload.csv missing")
                return []
            with csv_path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            _require(len(rows) == 1, "premix upload.csv must have exactly one row")
            selected = Path(rows[0].get("video_path", ""))
            resolved = [selected.resolve()] if selected.is_absolute() else [(_parent / selected).resolve() for _parent in (series, series / "output", repo)]
            _require(bool(rows[0].get("video_path")) and video in resolved, "premix CSV video_path differs from declared render")
            thumbnail = Path(rows[0].get("thumbnail_path", ""))
            thumb_paths = [thumbnail.resolve()] if thumbnail.is_absolute() else [(_parent / thumbnail).resolve() for _parent in (series, series / "output", repo)]
            _require(bool(rows[0].get("thumbnail_path")) and data["image"] in thumb_paths, "premix CSV thumbnail_path differs from approved JPG")
            if metadata is not None:
                _require(all(metadata.get(key) and rows[0].get(key) == metadata[key] for key in ("title", "description", "tags")),
                         "premix YouTube title/description/tags differ between concept.md and upload.csv")
                chapters = re.findall(r"(?m)^[^\n]*?(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2})\.\s+([^\n]+)$", metadata["description"])
                expected = [(chapter_timestamp(e["mix_entry_seconds"]), e["order"], e["title"]) for e in entries]
                actual = [(time, int(order), title.removesuffix(" (반복)")) for time, order, title in chapters]
                _require(actual == expected, "premix YouTube 40 chapter starts/order/title differ from actual production timeline")
        return []
    except (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, ZeroDivisionError, ffmpeg.Error) as error:
        return [f"Final Premixed Audio render: {error}"]
