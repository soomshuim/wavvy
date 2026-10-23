"""Validate timed lyric subtitles and separate their preparation from publication."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


MANIFEST = Path("input/subtitles.json")
DEFAULT_SRT = Path("output/youtube_subtitles_ko_timed_estimated.srt")


class SubtitleError(ValueError):
    pass


def _json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise SubtitleError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SubtitleError(f"Expected JSON object: {path}")
    return value


def _sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise SubtitleError(f"Cannot read {path}: {exc}") from exc


def _bound(series: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise SubtitleError(f"Invalid series-relative path: {relative!r}")
    root = series.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise SubtitleError(f"Path escapes series: {relative}")
    return path


def _verified_file(series: Path, record: dict) -> Path:
    if not isinstance(record, dict):
        raise SubtitleError("Expected file path and sha256 record")
    path = _bound(series, record.get("path"))
    digest = record.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SubtitleError(f"Invalid sha256 for {path}")
    if _sha(path) != digest:
        raise SubtitleError(f"sha256 mismatch: {path}")
    return path


def _ms(seconds: object) -> int:
    try:
        value = Decimal(str(seconds)) * 1000
        if not value.is_finite() or value < 0:
            raise ValueError
        return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except (ValueError, TypeError, ArithmeticError) as exc:
        raise SubtitleError(f"Invalid duration: {seconds!r}") from exc


def _stamp(ms: int) -> str:
    hours, rem = divmod(ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def _sample_position(label: str, index: int, cue_count: int, watch_ms: int, repeat: int, pass_offset: int) -> bool:
    if label == "first":
        return index == 1
    if label == "middle":
        return 1 < index < cue_count and (repeat == 1 or watch_ms < pass_offset)
    if label == "repeat":
        return repeat > 1 and pass_offset <= watch_ms < pass_offset * 2
    if label == "ending":
        return index == cue_count
    return False


def _source_lines(concept: str, orders: list[int]) -> dict[int, list[str]]:
    heading = re.search(r"^## Final Track Sources\s*$", concept, re.MULTILINE)
    if not heading:
        raise SubtitleError("Final Track Sources archive missing")
    tail = concept[heading.end():]
    end = re.search(r"^## ", tail, re.MULTILINE)
    archive = tail[:end.start()] if end else tail
    result = {}
    for order in orders:
        block = re.search(rf"^### {order:02d}\. .*$([\s\S]*?)(?=^### \d{{2}}\. |\Z)", archive, re.MULTILINE)
        if not block:
            raise SubtitleError(f"Track {order:02d} source block missing")
        lyrics = re.search(r"^#### LYRICS\s*\n\s*```(?:text)?\s*\n([\s\S]*?)\n```", block.group(0), re.MULTILINE)
        if not lyrics:
            raise SubtitleError(f"Track {order:02d} lyrics block missing")
        lines = []
        for raw in lyrics.group(1).splitlines():
            line = raw.strip()
            if not line or re.fullmatch(r"\(instrumental[^)]*\)", line, re.IGNORECASE):
                continue
            sung = re.sub(r" {2,}", " ", re.sub(r"\[[^\]\n]+\]", "", line)).strip()
            if sung:
                lines.append(sung)
        if not lines:
            raise SubtitleError(f"Track {order:02d} has no sung lines")
        result[order] = lines
    return result


def _layout(report: dict) -> tuple[list[dict], list[int], int, int, int]:
    tracks = report.get("tracks")
    params = report.get("processing_params")
    if not isinstance(tracks, list) or not tracks or not all(isinstance(track, dict) for track in tracks) or not isinstance(params, dict):
        raise SubtitleError("Malformed render report")
    try:
        repeat = int(params["repeat"])
        fade_ms = _ms(params["fade"])
        if repeat < 1 or repeat != params["repeat"]:
            raise ValueError
        orders = [int(t["order"]) for t in tracks]
        if orders != list(range(1, len(tracks) + 1)):
            raise ValueError
        lengths = [_ms(t["duration"]) for t in tracks]
        if min(lengths) <= fade_ms:
            raise ValueError
        if any(not isinstance(t.get("title"), str) or not t["title"] for t in tracks):
            raise ValueError
    except (KeyError, ValueError, TypeError, IndexError) as exc:
        raise SubtitleError("Invalid report tracks, repeat, or fade") from exc
    starts, cursor = [], 0
    for duration in lengths:
        starts.append(cursor)
        cursor += duration - fade_ms
    pass_offset = cursor
    final_duration = sum(lengths) * repeat - fade_ms * (len(tracks) * repeat - 1)
    summary = report.get("summary")
    if not isinstance(summary, dict) or _ms(summary.get("final_duration")) != final_duration:
        raise SubtitleError("Report final duration differs from track/fade calculation")
    return tracks, starts, repeat, pass_offset, final_duration


def _occurrences(cues: list[dict], lines: list[str], allowed: dict[int, int], track: int) -> None:
    expected = [(n, 1, text) for n, text in enumerate(lines, 1)]
    observed = []
    for cue in cues:
        if not isinstance(cue, dict):
            raise SubtitleError(f"Track {track}: malformed cue")
        occurrences = cue.get("source_line_occurrences")
        if not isinstance(occurrences, list) or not 1 <= len(occurrences) <= 2:
            raise SubtitleError(f"Track {track}: malformed source_line_occurrences")
        for item in occurrences:
            try:
                line, occurrence, text = item["source_line"], item["occurrence"], item["text"]
                if type(line) is not int or type(occurrence) is not int or not 1 <= line <= len(lines) or occurrence < 1:
                    raise ValueError
            except (KeyError, ValueError, TypeError) as exc:
                raise SubtitleError(f"Track {track}: invalid source occurrence") from exc
            if text != lines[line - 1]:
                raise SubtitleError(f"Track {track} line {line}: source lyric changed")
            observed.append((line, occurrence, text))
    counts = Counter((line, occurrence) for line, occurrence, _ in observed)
    if any(value != 1 for value in counts.values()):
        raise SubtitleError(f"Track {track}: duplicate source occurrence")
    for line, count in allowed.items():
        expected.extend((line, occurrence, lines[line - 1]) for occurrence in range(2, count + 2))
    if sorted(observed) != sorted(expected):
        raise SubtitleError(f"Track {track}: missing or unauthorized sung occurrence")
    first = [line for line, occurrence, _ in observed if occurrence == 1]
    if first != list(range(1, len(lines) + 1)):
        raise SubtitleError(f"Track {track}: source lyric order changed")
    for line in allowed:
        occurrences = [occurrence for source_line, occurrence, _ in observed if source_line == line]
        if occurrences != sorted(occurrences):
            raise SubtitleError(f"Track {track}: repeated lyric order changed")


def _observed_anchor(series: Path, evidence_dir: Path, record: dict, cues: list[dict], evidence: dict[str, str]) -> None:
    """Re-read retained word timing; never compare a cue only with itself."""
    try:
        rel = record["evidence"]
        digest = evidence[rel]
        path = _bound(series, str(evidence_dir.relative_to(series) / rel))
        if _sha(path) != digest:
            raise SubtitleError(f"Observed anchor evidence changed: {rel}")
        data = _json(path)
        words = [word for segment in data["transcription"]["segments"] for word in segment["words"]]
        matching = [word for word in words if word["word"].strip() == record["first_word"]]
        if len(matching) != 1:
            raise SubtitleError(f"Observed anchor word ambiguous: {rel}")
        observed_ms = int(record["clip_start_ms"]) + _ms(matching[0]["start"])
        target = [cue for cue in cues if cue["track"] == record["track"] and any(
            o["source_line"] == record["source_line"] and o["occurrence"] == record["occurrence"]
            for o in cue["source_line_occurrences"]
        )]
        if len(target) != 1 or abs(target[0]["relative_start_ms"] - observed_ms) > int(record["max_onset_delta_ms"]):
            raise SubtitleError(f"Track {record['track']} line {record['source_line']}: onset outside retained observation")
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        if isinstance(exc, SubtitleError):
            raise
        raise SubtitleError("Malformed observed anchor check") from exc


def _prepare(series: Path, manifest: dict, creating: bool = False) -> tuple[str, Path, dict]:
    timing_path = _verified_file(series, manifest.get("timing_map"))
    report_path = _verified_file(series, manifest.get("report"))
    if report_path != series.resolve() / "output" / "report.json":
        raise SubtitleError("Subtitle report must be output/report.json")
    report = _json(report_path)
    tracks, starts, repeat, offset, duration = _layout(report)
    if duration <= 0:
        raise SubtitleError("Invalid video duration")
    source = _source_lines((series / "concept.md").read_text(encoding="utf-8"), [int(t["order"]) for t in tracks])
    timing = _json(timing_path)
    if timing.get("schema") not in (None, "wavvy.subtitle-timing.v1"):
        raise SubtitleError("Unsupported timing map schema")
    untimed = "\n\n".join("\n".join(source[int(track["order"])]) for track in tracks)
    untimed = "\n\n".join([untimed] * repeat) + "\n"
    source_digest = hashlib.sha256(untimed.encode("utf-8")).hexdigest()
    source_digests = [digest for digest in (timing.get("original_source_sha256"), manifest.get("source_sha256")) if digest is not None]
    approved_source_digest = source_digests[0] if source_digests else None
    if not creating and not approved_source_digest:
        raise SubtitleError("Approved lyric source hash missing")
    if any(source_digest != digest for digest in source_digests):
        raise SubtitleError("Current Final Track Sources differ from approved lyric source hash")
    if timing.get("repeat_offset_ms") is not None and timing["repeat_offset_ms"] != offset:
        raise SubtitleError("Timing map repeat offset differs from report")
    mapped = timing.get("tracks")
    output = timing.get("output_cues")
    if not isinstance(mapped, list) or len(mapped) != len(tracks) or not all(isinstance(item, dict) for item in mapped) or (output is not None and not isinstance(output, list)):
        raise SubtitleError("Timing map tracks/output_cues malformed")
    evidence = timing.get("audio_evidence_sha256")
    if not isinstance(evidence, dict) or not evidence:
        raise SubtitleError("Audio evidence hashes missing")
    for rel, digest in evidence.items():
        if not isinstance(rel, str) or not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) or _sha(_bound(series, str(timing_path.parent.relative_to(series) / rel))) != digest:
            raise SubtitleError(f"Audio evidence missing or changed: {rel}")
    approved = manifest.get("required_extra_occurrences", {})
    if not isinstance(approved, dict) or approved != timing.get("allowed_added_source_lines_per_pass", {}):
        raise SubtitleError("Approved sung repeats differ from timing map")
    extras: dict[int, dict[int, int]] = {int(t["order"]): {} for t in tracks}
    for key, count in approved.items():
        match = re.fullmatch(r"(\d+):(\d+)(?:-(\d+))?", key)
        if not match or type(count) is not int or count < 1:
            raise SubtitleError(f"Invalid approved repeat: {key}")
        track, first, last = int(match[1]), int(match[2]), int(match[3] or match[2])
        if track not in extras or first < 1 or last > len(source[track]):
            raise SubtitleError(f"Invalid approved repeat range: {key}")
        span = last - first + 1
        if count % span:
            raise SubtitleError(f"Approved repeat count does not cover full range: {key}")
        for line in range(first, last + 1):
            if line in extras[track]:
                raise SubtitleError(f"Duplicate repeat approval: {key}")
            extras[track][line] = count // span
    approvals = manifest.get("repeat_evidence", {})
    if not isinstance(approvals, dict) or set(approvals) != set(approved):
        raise SubtitleError("Every sung repeat needs retained evidence")
    for key, paths in approvals.items():
        if not isinstance(paths, list) or not paths or any(path not in evidence for path in paths):
            raise SubtitleError(f"Repeat {key} has no hashed audio evidence")
    first_pass = []
    for i, item in enumerate(mapped):
        number = int(tracks[i]["order"])
        if (item.get("track") != number or
            ("title" in item and item["title"] != tracks[i]["title"]) or
            ("start_ms" in item and item["start_ms"] != starts[i]) or
            ("source_lines" in item and item["source_lines"] != len(source[number]))):
            raise SubtitleError(f"Track {number}: timing map/report/source identity differs")
        local = item.get("cues")
        if not isinstance(local, list) or not local:
            raise SubtitleError(f"Track {number}: no timed cues")
        _occurrences(local, source[number], extras[number], number)
        previous_end = -1
        for cue in local:
            begin, end = cue.get("relative_start_ms"), cue.get("relative_end_ms")
            if type(begin) is not int or type(end) is not int or begin < 0 or begin < previous_end or end <= begin or end > _ms(tracks[i]["duration"]):
                raise SubtitleError(f"Track {number}: cue outside positive non-overlapping track time")
            anchor_end = cue.get("last_asr_end_ms")
            labels = cue.get("anchor_classes")
            if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
                raise SubtitleError(f"Track {number}: malformed anchor classes")
            if anchor_end is not None and (type(anchor_end) is not int or end > anchor_end):
                raise SubtitleError(f"Track {number}: cue extends beyond observed ASR end")
            if anchor_end is None and not any(
                marker in label for label in labels
                for marker in ("estimated", "interpolated", "independent_whisper")
            ):
                raise SubtitleError(f"Track {number}: missing observed bound without estimate label")
            occurrences = cue["source_line_occurrences"]
            text = "\n".join(o["text"] for o in occurrences)
            if cue.get("texts") != [o["text"] for o in occurrences]:
                raise SubtitleError(f"Track {number}: cue text differs from source")
            first_pass.append((number, starts[i] + begin, starts[i] + end, text, occurrences))
            previous_end = end
    anchors = manifest.get("observed_anchor_checks", [])
    if not isinstance(anchors, list):
        raise SubtitleError("Observed anchor checks malformed")
    for anchor in anchors:
        _observed_anchor(series, timing_path.parent, anchor, [{**cue, "track": t["track"]} for t in mapped for cue in t["cues"]], evidence)
    expected_count = len(first_pass) * repeat
    if output is not None and len(output) != expected_count:
        raise SubtitleError("Timing map output cue count differs from report repeat")
    if timing.get("srt_cues") is not None and timing["srt_cues"] != expected_count:
        raise SubtitleError("Timing map SRT cue count differs from report repeat")
    expected = []
    for pass_number in range(1, repeat + 1):
        for track, start, end, text, occurrences in first_pass:
            expected.append((pass_number, track, start + (pass_number - 1) * offset, end + (pass_number - 1) * offset, text, occurrences))
    rendered = []
    prior_end = -1
    for index, (pass_number, track, start, end, value, occurrences) in enumerate(expected, 1):
        if output is not None:
            actual = output[index - 1]
            if not isinstance(actual, dict) or any(actual.get(k) != v for k, v in {
                "number": index, "pass": pass_number, "track": track, "start_ms": start, "end_ms": end,
                "text": value, "source_line_occurrences": occurrences,
            }.items()):
                raise SubtitleError(f"Output cue {index} differs from source, report, or repeat offset")
        if start < prior_end or end <= start or end > duration:
            raise SubtitleError(f"Output cue {index} overlaps or lies outside video")
        if len(value.splitlines()) > 2 or not value.strip():
            raise SubtitleError(f"Output cue {index} unreadable line layout")
        rendered.append(f"{index}\n{_stamp(start)} --> {_stamp(end)}\n{value}\n")
        prior_end = end
    content = "\n".join(rendered)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    srt_record = manifest.get("srt")
    if not isinstance(srt_record, dict) or (timing.get("srt_sha256") is not None and digest != timing["srt_sha256"]):
        raise SubtitleError("Rendered SRT hash differs from approved timing map/manifest")
    if not creating and not srt_record.get("sha256"):
        raise SubtitleError("Approved SRT hash missing")
    if srt_record.get("sha256") is not None and digest != srt_record["sha256"]:
        raise SubtitleError("Rendered SRT hash differs from approved timing map/manifest")
    destination = _bound(series, srt_record.get("path"))
    if destination != series.resolve() / DEFAULT_SRT:
        raise SubtitleError("SRT destination must be output/youtube_subtitles_ko_timed_estimated.srt")
    return content, destination, {
        "cues": expected_count, "duration_ms": duration, "sha256": digest, "source_sha256": source_digest,
        "timing_scope": "structure, source text, retained hashes and selected observed anchors; not full acoustic verification",
    }


def manifest_for(series: Path) -> dict:
    data = _json(series / MANIFEST)
    if data.get("schema") != "wavvy.subtitles.v1":
        raise SubtitleError("Unsupported subtitle manifest schema")
    return data


def prepare_timed(series: Path, timing_map: Path) -> dict:
    series = series.resolve()
    manifest = manifest_for(series)
    approved = _verified_file(series, manifest.get("timing_map"))
    if timing_map.resolve() != approved:
        raise SubtitleError("Selected timing map differs from approved manifest")
    content, destination, summary = _prepare(series, manifest, creating=True)
    if destination.exists():
        if destination.read_bytes() != content.encode("utf-8"):
            raise SubtitleError(f"Existing timed SRT differs from approved source: {destination}")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content.encode("utf-8"))
    if manifest["srt"].get("sha256") is None or ("original_source_sha256" not in _json(approved) and manifest.get("source_sha256") is None):
        manifest["srt"]["sha256"] = summary["sha256"]
        manifest["source_sha256"] = summary["source_sha256"]
        (series / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"result": "PASS", "stage": "prepared", "srt": str(destination), **summary}


def verify_prepared(series: Path) -> dict:
    series = series.resolve()
    manifest = manifest_for(series)
    content, destination, summary = _prepare(series, manifest)
    _verified_file(series, manifest.get("srt"))
    if destination.read_bytes() != content.encode("utf-8"):
        raise SubtitleError("Prepared SRT content differs from validated timing map")
    return {"result": "PASS", "stage": "prepared", "srt": str(destination), **summary}


def verify_published(series: Path) -> dict:
    prepared = verify_prepared(series)
    manifest = manifest_for(series)
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise SubtitleError("Manual subtitle publication evidence missing")
    observation_path = _verified_file(series, publication.get("observation"))
    observation = _json(observation_path)
    video_id = publication.get("video_id")
    if not isinstance(video_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) or observation.get("video_id") != video_id:
        raise SubtitleError("Published subtitle target video identity missing or mismatched")
    concept = (series / "concept.md").read_text(encoding="utf-8")
    upload_section = re.search(r"^## Upload Status\s*$([\s\S]*?)(?=^## |\Z)", concept, re.MULTILINE)
    if not upload_section or not re.search(rf"(?:youtube\.com/watch\?v=|youtu\.be/){re.escape(video_id)}\b", upload_section.group(0)):
        raise SubtitleError("Published subtitle video ID differs from concept upload target")
    menu = observation.get("public_caption_menu")
    if observation.get("studio_manual_korean") != "게시됨" or not isinstance(menu, str) or "수동 한국어 checked" not in menu:
        raise SubtitleError("Studio/public manual Korean publication not observed")
    studio_raw = _verified_file(series, publication.get("studio_raw")).read_text(encoding="utf-8")
    menu_raw = _verified_file(series, publication.get("public_menu_raw")).read_text(encoding="utf-8")
    if f"/video/{video_id}/translations" not in studio_raw or "게시됨" not in studio_raw:
        raise SubtitleError("Retained Studio raw observation lacks target/manual status")
    if f"watch?v={video_id}" not in menu_raw or not re.search(r'menuitemradio "한국어"[^\n]*\[checked\]', menu_raw):
        raise SubtitleError("Retained public raw observation lacks manual Korean selection")
    samples = observation.get("public_watch_samples")
    report = _json(series / "output" / "report.json")
    _, _, repeat, pass_offset, _ = _layout(report)
    required_labels = {"first", "middle", "ending"}
    if repeat > 1:
        required_labels.add("repeat")
    if not isinstance(samples, list) or not all(isinstance(sample, dict) and isinstance(sample.get("label"), str) for sample in samples) or not required_labels.issubset({sample["label"] for sample in samples}):
        raise SubtitleError("Public manual lyric samples missing")
    sample_files = publication.get("sample_files")
    if not isinstance(sample_files, dict):
        raise SubtitleError("Publication sample file records missing")
    srt = (series / DEFAULT_SRT).read_text(encoding="utf-8")
    blocks = srt.strip().split("\n\n")
    for sample in samples:
        cue = sample.get("source_cue")
        if not isinstance(cue, dict):
            raise SubtitleError("Malformed public subtitle sample cue")
        index = cue.get("index")
        if type(index) is not int or not 1 <= index <= len(blocks):
            raise SubtitleError("Invalid public subtitle sample cue")
        lines = blocks[index - 1].splitlines()
        if lines[0] != str(index) or lines[1] != f"{cue.get('start')} --> {cue.get('end')}" or "\n".join(lines[2:]) != cue.get("text") or sample.get("observed_caption") != cue.get("text"):
            raise SubtitleError("Public sample differs from source SRT")
        watch_ms = _ms(sample.get("observed_watch_time_s"))
        start_s, end_s = cue.get("start"), cue.get("end")
        def parse_stamp(value: str) -> int:
            if not isinstance(value, str):
                raise SubtitleError("Malformed sampled SRT time")
            match = re.fullmatch(r"(\d+):(\d\d):(\d\d),(\d{3})", value)
            if not match:
                raise SubtitleError("Malformed sampled SRT time")
            return ((int(match[1]) * 60 + int(match[2])) * 60 + int(match[3])) * 1000 + int(match[4])
        if not parse_stamp(start_s) <= watch_ms <= parse_stamp(end_s) + 1000:
            raise SubtitleError("Public sample lies outside cue time")
        label = sample.get("label")
        if not _sample_position(label, index, len(blocks), watch_ms, repeat, pass_offset):
            raise SubtitleError(f"Public sample {label} is outside its actual lyric/pass position")
        records = sample_files.get(label)
        if not isinstance(records, dict):
            raise SubtitleError("Public sample evidence record missing")
        raw = _verified_file(series, records.get("raw_snapshot")).read_text(encoding="utf-8")
        if f"watch?v={video_id}" not in raw or any(f'generic "{line}"' not in raw for line in cue["text"].splitlines()):
            raise SubtitleError("Retained public raw sample lacks target visible lyric")
        for key in ("raw_snapshot", "screenshot"):
            _verified_file(series, records.get(key))
    _verified_file(series, publication.get("studio_capture"))
    _verified_file(series, publication.get("public_menu_capture"))
    download_record = publication.get("studio_download")
    if download_record is not None:
        downloaded = _verified_file(series, download_record).read_bytes()
        prepared_bytes = (series / DEFAULT_SRT).read_bytes()
        if downloaded.rstrip(b"\n") != prepared_bytes.rstrip(b"\n"):
            raise SubtitleError("Official downloaded manual SRT differs in timing/text")
    return {
        **prepared, "stage": "published", "video_id": video_id, "samples": len(samples),
        "studio_download_compared": download_record is not None,
        "publication_scope": "manual Korean Studio status, public selection and samples, official SRT when available",
    }


def subtitle_status(series: Path, instrumental: bool = False) -> dict:
    if instrumental:
        return {"prepared": "exempt_instrumental", "published": "exempt_instrumental"}
    try:
        verify_prepared(series)
    except (SubtitleError, OSError, UnicodeError, KeyError, TypeError):
        return {"prepared": "unverified", "published": "unverified"}
    try:
        verify_published(series)
    except (SubtitleError, OSError, UnicodeError, KeyError, TypeError):
        return {"prepared": "verified", "published": "unverified"}
    return {"prepared": "verified", "published": "verified"}


def needs_timed_subtitles(series: Path, instrumental: bool = False) -> bool:
    if instrumental:
        return False
    try:
        report = _json(series / "output" / "report.json")
        return _ms(report.get("summary", {}).get("final_duration")) > 3_600_000
    except SubtitleError:
        return False
