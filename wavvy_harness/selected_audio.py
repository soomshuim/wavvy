"""Evidence gate for an explicitly declared instrumental final-audio archive."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

MANIFEST = "input/final-selected-audio-sources.json"


def _read_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain an object")
    return data


def _safe_file(series_path: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"unsafe evidence path: {relative!r}")
    path = (series_path / relative).resolve()
    if not path.is_relative_to(series_path.resolve()) or not path.is_file():
        raise ValueError(f"evidence file missing or outside series: {relative}")
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _timestamp(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, sec = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"


def _source_bindings(input_dir: Path) -> dict[str, set[tuple[str, str]]]:
    bindings: dict[str, set[tuple[str, str]]] = {}
    for path in sorted(input_dir.glob("suno-*.json")):
        if path.name.startswith("suno-final-selection"):
            continue
        try:
            data = _read_json(path)
        except (OSError, ValueError):
            continue
        for track in data.get("tracks", []):
            if not isinstance(track, dict) or not track.get("source_txt") or not track.get("source_sha256"):
                continue
            for candidate in track.get("candidates", []):
                candidate_id = candidate.get("id") if isinstance(candidate, dict) else candidate
                if isinstance(candidate_id, str):
                    bindings.setdefault(candidate_id, set()).add((track["source_txt"], track["source_sha256"]))
    return bindings


def _observation_matches(value: object, candidate_id: str, description: str) -> bool:
    """Require the observed style in the same song record as its candidate ID."""
    if isinstance(value, list):
        return any(_observation_matches(item, candidate_id, description) for item in value)
    if not isinstance(value, dict):
        return False
    if (value.get("id") == candidate_id or value.get("candidate_id") == candidate_id) and (
        value.get("style_description_ui") == description
        or value.get("observed_style_description") == description
    ):
        return True
    return any(_observation_matches(item, candidate_id, description) for item in value.values())


def check_selected_audio(series_path: Path) -> tuple[bool, list[str]]:
    """Return (opted in, errors). Presence of either contract half opts in."""
    series_path = series_path.resolve()
    concept = (series_path / "concept.md").read_text(encoding="utf-8") if (series_path / "concept.md").exists() else ""
    heading = re.search(r"(?m)^## Final Selected Audio Sources\s*$", concept)
    manifest_path = series_path / MANIFEST
    opted_in = bool(heading or manifest_path.exists())
    if not opted_in:
        return False, []
    errors: list[str] = []
    if not heading:
        errors.append("concept.md needs ## Final Selected Audio Sources for instrumental opt-in")
    else:
        tail = concept[heading.end():]
        next_heading = re.search(r"(?m)^## ", tail)
        section = tail[:next_heading.start()] if next_heading else tail
        if MANIFEST not in section:
            errors.append(f"Final Selected Audio Sources must point to {MANIFEST}")
    if not re.search(r"(?im)^[-*] \*\*Final vocal direction[^\n]*Instrumental|^[-*] \*\*Vocal mode[^\n]*Instrumental|^[-*] \*\*Vocal[^\n]*Instrumental", concept):
        errors.append("concept.md must explicitly declare the final vocal direction Instrumental")
    try:
        archive = _read_json(manifest_path)
        report = _read_json(series_path / "output/report.json")
        download = _read_json(series_path / "input/download-manifest.json")
        selection_paths = sorted((series_path / "input").glob("suno-final-selection*.json"))
        if len(selection_paths) != 1:
            raise ValueError("exactly one final selection manifest is required")
        selection = _read_json(selection_paths[0])
    except (OSError, ValueError) as error:
        return True, errors + [f"Final Selected Audio Sources evidence missing/invalid: {error}"]
    if archive.get("schema") != "wavvy.final_selected_audio.v1" or archive.get("vocal_mode") != "instrumental":
        errors.append("selected audio schema/vocal_mode must be wavvy.final_selected_audio.v1/instrumental")
    workspace = archive.get("workspace")
    if not workspace or workspace != selection.get("workspace") or workspace != download.get("workspace"):
        errors.append("selected audio workspace differs from final selection/download manifest")
    lists = [archive.get("tracks"), report.get("tracks"), download.get("tracks"), selection.get("tracks")]
    if any(not isinstance(items, list) for items in lists):
        return True, errors + ["selected audio/report/download/selection tracks must be arrays"]
    archive_tracks, report_tracks, download_tracks, selection_tracks = lists
    n = len(report_tracks)
    if n == 0 or any(len(items) != n for items in lists):
        return True, errors + ["selected audio/report/download/selection track counts differ"]
    bindings = _source_bindings(series_path / "input")
    offset = 0.0
    try:
        fade = float(report.get("processing_params", {}).get("fade", 0) or 0)
    except (TypeError, ValueError):
        fade = -1
    if fade < 0:
        errors.append("report fade is invalid")
    ids: set[str] = set()
    for index, (entry, rendered, downloaded, selected) in enumerate(zip(*lists), start=1):
        if not all(isinstance(item, dict) for item in (entry, rendered, downloaded, selected)):
            errors.append(f"track {index:02d}: entry must be an object")
            continue
        label = f"track {index:02d}"
        if any(item.get("order") != index for item in (entry, rendered, downloaded, selected)):
            errors.append(f"{label}: order differs across final evidence")
        if not (entry.get("title") == rendered.get("title") == downloaded.get("approved_title") == selected.get("title")):
            errors.append(f"{label}: title differs across final evidence")
        candidate_id = entry.get("candidate_id")
        if not candidate_id or candidate_id != downloaded.get("candidate_id") or candidate_id != selected.get("candidate_id") or candidate_id in ids:
            errors.append(f"{label}: selected candidate ID missing, duplicate, or mismatched")
        ids.add(candidate_id)
        sha = entry.get("wav_sha256")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha) or sha != rendered.get("sha256") or sha != downloaded.get("sha256"):
            errors.append(f"{label}: WAV SHA differs across final evidence")
        try:
            audio_path = _safe_file(series_path, "input/tracks/" + rendered["filename"])
            if _sha256(audio_path) != sha or downloaded.get("input_filename") != rendered["filename"]:
                errors.append(f"{label}: WAV file/hash differs from report or download")
        except (KeyError, OSError, ValueError) as error:
            errors.append(f"{label}: WAV evidence invalid: {error}")
        if entry.get("start_time") != _timestamp(offset):
            errors.append(f"{label}: start_time differs from report-derived timestamp {_timestamp(offset)}")
        try:
            duration = float(rendered["duration"])
            if duration <= 0:
                raise ValueError("duration must be positive")
            offset += duration - (fade if index < n else 0)
        except (KeyError, TypeError, ValueError):
            errors.append(f"{label}: report duration invalid")
        status = entry.get("raw_prompt_status")
        if status not in {"confirmed", "unverified"}:
            errors.append(f"{label}: raw_prompt_status must be confirmed or unverified")
        if status == "confirmed":
            source = entry.get("source_txt")
            source_sha = entry.get("source_sha256")
            if not isinstance(source, str) or not isinstance(source_sha, str) or (source, source_sha) not in bindings.get(candidate_id, set()):
                errors.append(f"{label}: confirmed raw prompt lacks candidate-to-source binding")
            else:
                try:
                    if _sha256(_safe_file(series_path, source)) != source_sha:
                        errors.append(f"{label}: confirmed source txt hash differs")
                except (OSError, ValueError) as error:
                    errors.append(f"{label}: source txt invalid: {error}")
        elif entry.get("source_txt") or entry.get("source_sha256"):
            errors.append(f"{label}: unverified raw prompt cannot claim source txt/hash")
        description, reference = entry.get("observed_style_description"), entry.get("observation_ref")
        if (description is None) != (reference is None):
            errors.append(f"{label}: observed description and evidence reference must appear together")
        elif description is not None:
            if not isinstance(description, str) or not description.strip() or not isinstance(reference, str):
                errors.append(f"{label}: observed style evidence invalid")
            else:
                try:
                    observation = _read_json(_safe_file(series_path, reference))
                    if not _observation_matches(observation, candidate_id, description):
                        errors.append(f"{label}: observed style is not bound to candidate in evidence file")
                except (OSError, ValueError) as error:
                    errors.append(f"{label}: observed style evidence invalid: {error}")
    return True, errors
