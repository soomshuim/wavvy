"""State inference and validation for Wavvy series."""

from __future__ import annotations

import json
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


PHASES = ["concept_draft", "track_source_draft", "source_final", "render_final", "upload_ready", "uploaded"]
SOURCE_FINAL_PHASES = {"source_final", "render_final", "upload_ready", "uploaded"}
LOCAL_RENDER_PHASES = {"render_final"}

DEFAULT_NEXT_ACTION = (
    "No active blocker. Local final.mkv/upload.csv are disposable after upload "
    "and can be regenerated with pack if needed."
)

AUTHORITATIVE_DOCS = [
    "MASTER/SSOT.md",
    "MASTER/ai/RUNTIME_RULES.md",
    "MASTER/MANAGER.md",
    "MASTER/WORKFLOWS.md",
    "MASTER/cli/SPEC.md",
    "MASTER/youtube/YOUTUBE.md",
    "wavvy.md",
]
LYRIC_SKILL_EVIDENCE_REFS = [
    "MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md",
    "skills/wavvy-lyricist/SKILL.md",
    "skills/wavvy-lyricist/references/patterns.md",
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _load_report(report_path: Path) -> dict[str, Any]:
    try:
        with report_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _status(path: Path) -> str:
    return "present" if path.exists() else "missing"


def _concept_declares_compilation(concept_text: str) -> bool:
    return bool(re.search(r"\*\*Type\*\*:\s*Compilation\b", concept_text, flags=re.IGNORECASE))


def _compilation_source_map_entries(concept_text: str) -> list[dict[str, str]]:
    if not _concept_declares_compilation(concept_text):
        return []
    section = _markdown_section(concept_text, "Track Selection")
    if not section:
        return []

    entries: list[dict[str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 4 or not re.fullmatch(r"\d{2}", parts[0]):
            continue
        source_match = re.search(r"`([^`]+\.(?:mp3|wav))`", parts[2], flags=re.IGNORECASE)
        copied_match = re.search(r"`([^`]+\.(?:mp3|wav))`", parts[3], flags=re.IGNORECASE)
        if source_match and copied_match:
            entries.append(
                {
                    "order": parts[0],
                    "title": parts[1],
                    "source": source_match.group(1),
                    "copied_filename": copied_match.group(1),
                }
            )
    return entries


def _resolve_source_path(repo_root: Path, source: str) -> Path:
    path = Path(source)
    if path.is_absolute():
        return path
    return repo_root / path


def _metadata_present(concept_text: str) -> bool:
    heading = re.search(r"^## YouTube (?:Metadata|Draft).*$", concept_text, flags=re.MULTILINE)
    if not heading:
        return False
    section_start = heading.end()
    next_heading = re.search(r"^## ", concept_text[section_start:], flags=re.MULTILINE)
    section_end = section_start + next_heading.start() if next_heading else len(concept_text)
    section = concept_text[section_start:section_end]
    required = [
        r"^### (?:Title|제목)\s*$",
        r"^### (?:Description|설명)\s*$",
        r"^### (?:Tags|태그(?:\s*\([^)]*\))?)\s*$",
    ]
    return all(re.search(pattern, section, flags=re.MULTILINE) for pattern in required)


def _final_track_sources_count(concept_text: str) -> int:
    heading = re.search(r"^## Final Track Sources\s*$", concept_text, flags=re.MULTILINE)
    if not heading:
        return 0
    next_heading = re.search(r"^## ", concept_text[heading.end():], flags=re.MULTILINE)
    end = heading.end() + next_heading.start() if next_heading else len(concept_text)
    section = concept_text[heading.start():end]
    return len(re.findall(r"^### \d{2}\. .+$", section, flags=re.MULTILINE))


def _markdown_section(concept_text: str, heading_name: str) -> str:
    heading = re.search(rf"^## {re.escape(heading_name)}\s*$", concept_text, flags=re.MULTILINE)
    if not heading:
        return ""
    next_heading = re.search(r"^## ", concept_text[heading.end():], flags=re.MULTILINE)
    end = heading.end() + next_heading.start() if next_heading else len(concept_text)
    return concept_text[heading.end():end]


def _upload_completed(concept_text: str) -> bool:
    upload_status = _markdown_section(concept_text, "Upload Status")
    completion_patterns = [
        r"\bcompleted\b",
        r"YouTube upload completed",
        r"YouTube 업로드 완료",
        r"업로드 완료",
    ]
    if upload_status:
        negative_patterns = [
            r"\bnot\s+(?:uploaded|completed)\b",
            r"업로드\s*(?:전|미완료|안\s*됨)",
        ]
        if any(re.search(pattern, upload_status, flags=re.IGNORECASE) for pattern in negative_patterns):
            return False
        return any(re.search(pattern, upload_status, flags=re.IGNORECASE) for pattern in completion_patterns)

    if re.search(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/\S+", concept_text, flags=re.IGNORECASE):
        return True

    explicit_patterns = [
        r"YouTube upload completed",
        r"YouTube 업로드 완료",
        r"업로드 완료",
    ]
    return any(re.search(pattern, concept_text, flags=re.IGNORECASE) for pattern in explicit_patterns)


def _has_stale_final_todo(concept_text: str) -> bool:
    if "## Final Track Sources" not in concept_text:
        return False
    candidates = []
    for heading_pattern in [r"^## Series Status\s*$", r"^## 미해결 / 다음 라운드\s*$"]:
        heading = re.search(heading_pattern, concept_text, flags=re.MULTILINE)
        if heading:
            next_heading = re.search(r"^## ", concept_text[heading.end():], flags=re.MULTILINE)
            end = heading.end() + next_heading.start() if next_heading else len(concept_text)
            candidates.append(concept_text[heading.start():end])
    target_text = "\n".join(candidates) if candidates else concept_text
    stale_patterns = [
        r"\bDRAFT\b",
        r"\bdraft\b",
        r"Suno 생성/검수",
        r"12 PASS \+ 8 draft",
    ]
    return any(re.search(pattern, target_text) for pattern in stale_patterns)


def _infer_phase(artifact_status: dict[str, Any], concept_text: str, report: dict[str, Any]) -> str:
    txt_sources = artifact_status.get("txt_sources", 0)
    if artifact_status.get("youtube_upload") == "completed":
        return "uploaded"
    if (
        artifact_status.get("final_mkv") == "present"
        and artifact_status.get("upload_csv") == "present"
        and (artifact_status.get("subtitle_txt") == "present" or artifact_status.get("subtitle_srt") == "present")
    ):
        return "upload_ready"
    if artifact_status.get("final_mkv") == "present" and artifact_status.get("upload_csv") == "present":
        return "render_final"
    if "## Final Track Sources" in concept_text and report.get("tracks") and artifact_status.get("available_audio_files", 0) > 0:
        return "source_final"
    if (
        artifact_status.get("source_map") == "present"
        and artifact_status.get("source_map_missing") == []
        and artifact_status.get("youtube_metadata") == "present"
        and artifact_status.get("available_audio_files", 0) > 0
    ):
        return "source_final"
    if txt_sources:
        return "track_source_draft"
    return "concept_draft"


def _infer_next_action(phase: str, artifact_status: dict[str, Any]) -> str:
    if phase == "uploaded":
        return DEFAULT_NEXT_ACTION
    if artifact_status["concept_md"] == "missing":
        return "Create concept.md for the active series."
    if phase == "concept_draft":
        return "Draft track sources from concept.md."
    if phase == "track_source_draft":
        return "Review existing track source drafts and follow the next source work in concept.md."
    if phase == "source_final":
        return "Review final track sources and prepare the render."
    if phase == "render_final":
        if artifact_status["final_mkv"] != "present" or artifact_status["upload_csv"] != "present":
            return "Create final.mkv and upload.csv for the render-final stage."
        if artifact_status["subtitle_txt"] == "missing" and artifact_status["subtitle_srt"] == "missing":
            return "Create subtitle text or SRT for the rendered series."
        return "Review the rendered series for upload readiness."
    return "Upload the series and record completion in concept.md."


def build_state(
    series_path: Path,
    repo_root: Path,
    phase: Optional[str] = None,
    previous_state: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build the current state payload from filesystem evidence."""
    repo_root = repo_root.resolve()
    series_path = series_path.resolve()
    concept_path = series_path / "concept.md"
    output_dir = series_path / "output"
    tracks_dir = series_path / "input" / "tracks"
    report_path = output_dir / "report.json"
    concept_text = _read_text(concept_path)
    report = _load_report(report_path)
    audio_files = sorted(list(tracks_dir.glob("*.mp3")) + list(tracks_dir.glob("*.wav"))) if tracks_dir.exists() else []
    txt_sources = sorted(tracks_dir.glob("*.txt")) if tracks_dir.exists() else []
    lyric_skill_files = {
        rel_path: _status(repo_root / rel_path)
        for rel_path in LYRIC_SKILL_EVIDENCE_REFS
    }
    source_map_entries = _compilation_source_map_entries(concept_text)
    missing_source_map = [
        entry["source"]
        for entry in source_map_entries
        if not _resolve_source_path(repo_root, entry["source"]).exists()
    ]
    source_map_audio_files = len(source_map_entries) - len(missing_source_map)
    available_audio_files = len(audio_files) if audio_files else source_map_audio_files
    audio_source = "input_tracks" if audio_files else ("concept_track_selection" if source_map_entries else "missing")
    upload_completed = _upload_completed(concept_text)
    final_mkv_status = _status(output_dir / "final.mkv")
    upload_csv_status = _status(output_dir / "upload.csv")
    if upload_completed and final_mkv_status == "missing":
        final_mkv_status = "deleted_after_upload"
    if upload_completed and upload_csv_status == "missing":
        upload_csv_status = "deleted_after_upload"

    artifact_status: dict[str, Any] = {
        "concept_md": _status(concept_path),
        "final_track_sources": "present" if "## Final Track Sources" in concept_text else "missing",
        "final_track_sources_count": _final_track_sources_count(concept_text),
        "report_json": _status(report_path),
        "report_tracks": len(report.get("tracks", [])) if isinstance(report.get("tracks"), list) else 0,
        "audio_files": len(audio_files),
        "available_audio_files": available_audio_files,
        "audio_source": audio_source,
        "source_map": "present" if source_map_entries else "missing",
        "source_map_tracks": len(source_map_entries),
        "source_map_audio_files": source_map_audio_files,
        "source_map_missing": missing_source_map,
        "txt_sources": len(txt_sources),
        "final_mkv": final_mkv_status,
        "upload_csv": upload_csv_status,
        "subtitle_txt": _status(output_dir / "youtube_subtitles_ko_no_timing.txt"),
        "subtitle_srt": _status(output_dir / "youtube_subtitles_ko_timed_estimated.srt"),
        "youtube_metadata": "present" if _metadata_present(concept_text) else "missing",
        "youtube_upload": "completed" if upload_completed else "missing",
        "lyric_skill_package": "present" if all(status == "present" for status in lyric_skill_files.values()) else "missing",
        "lyric_skill_files": lyric_skill_files,
    }

    series_rel = series_path.relative_to(repo_root).as_posix() if series_path.is_relative_to(repo_root) else str(series_path)
    same_series = (previous_state or {}).get("active_series") == series_rel
    prior_phase = (previous_state or {}).get("phase") if same_series else None
    inferred_phase = _infer_phase(artifact_status, concept_text, report)
    selected_phase = phase or prior_phase or inferred_phase
    if selected_phase not in PHASES:
        selected_phase = inferred_phase
    prior_next_action = (previous_state or {}).get("next_action") if same_series and selected_phase == prior_phase else None
    next_action = prior_next_action or _infer_next_action(selected_phase, artifact_status)

    blocked_by = []
    if selected_phase in LOCAL_RENDER_PHASES:
        if artifact_status["final_mkv"] != "present":
            blocked_by.append("output/final.mkv missing for render-final stage")
        if artifact_status["upload_csv"] != "present":
            blocked_by.append("output/upload.csv missing for render-final stage")
    if selected_phase == "upload_ready" and artifact_status["youtube_upload"] != "completed":
        if artifact_status["final_mkv"] != "present":
            blocked_by.append("output/final.mkv missing for upload-ready stage")
        if artifact_status["upload_csv"] != "present":
            blocked_by.append("output/upload.csv missing for upload-ready stage")
    if (
        selected_phase == "upload_ready"
        and artifact_status["youtube_upload"] != "completed"
        and artifact_status["subtitle_txt"] == "missing"
        and artifact_status["subtitle_srt"] == "missing"
    ):
        blocked_by.append("subtitle txt/srt missing for upload-ready stage")
    if selected_phase == "uploaded" and artifact_status["youtube_upload"] != "completed":
        blocked_by.append("uploaded phase requires concept.md upload completion evidence")

    previous_revision = int((previous_state or {}).get("revision", 0) or 0)

    return {
        "schema": "wavvy.state.v1",
        "revision": previous_revision,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "active_series": series_rel,
        "phase": selected_phase,
        "inferred_phase": inferred_phase,
        "next_action": next_action,
        "artifact_status": artifact_status,
        "authoritative_docs": [*AUTHORITATIVE_DOCS, f"{series_rel}/concept.md"],
        "evidence_refs": [*AUTHORITATIVE_DOCS, f"{series_rel}/concept.md", *LYRIC_SKILL_EVIDENCE_REFS],
        "blocked_by": blocked_by,
    }


def load_state(repo_root: Path) -> dict[str, Any]:
    state_path = repo_root / ".ai" / "state.json"
    try:
        with state_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def check_state(
    series_path: Path,
    repo_root: Path,
    state_payload: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Validate declared state against current filesystem evidence."""
    repo_root = repo_root.resolve()
    existing = state_payload if state_payload is not None else load_state(repo_root)
    resolved_series = series_path.resolve()
    requested_series = (
        resolved_series.relative_to(repo_root).as_posix()
        if resolved_series.is_relative_to(repo_root)
        else str(resolved_series)
    )
    phase = (existing or {}).get("phase") if (existing or {}).get("active_series") in (None, requested_series) else None
    current = build_state(series_path, repo_root, phase=phase, previous_state=existing)
    phase = current["phase"]
    artifacts = current["artifact_status"]
    concept_text = _read_text(series_path / "concept.md")

    warnings: list[str] = []
    blockers: list[str] = []

    if existing and existing.get("active_series") and current.get("active_series") != existing.get("active_series"):
        warnings.append("state active_series differs from requested series")

    if phase in SOURCE_FINAL_PHASES:
        source_map_complete = (
            artifacts.get("source_map") == "present"
            and artifacts.get("source_map_tracks", 0) > 0
            and not artifacts.get("source_map_missing")
        )
        if not source_map_complete:
            if artifacts["final_track_sources"] == "missing":
                blockers.append("source_final requires concept.md ## Final Track Sources")
            if artifacts["report_json"] == "missing":
                blockers.append("source_final requires output/report.json")
        elif artifacts["report_json"] == "missing":
            warnings.append("compilation source map is complete; output/report.json will be regenerated by pack")
        if artifacts["youtube_metadata"] == "missing":
            blockers.append("source_final requires concept.md YouTube Metadata/Draft title, description, and tags")
        if artifacts.get("source_map_missing"):
            blockers.append(
                "source_final requires existing source-map audio files: "
                + ", ".join(artifacts["source_map_missing"])
            )
        if artifacts.get("available_audio_files", artifacts["audio_files"]) <= 0:
            blockers.append("source_final requires audio files in input/tracks or concept.md Track Selection source map")
        if artifacts["final_track_sources_count"] and artifacts["report_tracks"]:
            if artifacts["final_track_sources_count"] != artifacts["report_tracks"]:
                blockers.append("Final Track Sources count differs from report track count")

    if phase in LOCAL_RENDER_PHASES:
        if artifacts["final_mkv"] != "present":
            blockers.append("render_final requires local output/final.mkv")
        if artifacts["upload_csv"] != "present":
            blockers.append("render_final requires local output/upload.csv")
    if phase == "upload_ready" and artifacts["youtube_upload"] != "completed":
        if artifacts["final_mkv"] != "present":
            blockers.append("upload_ready requires local output/final.mkv unless upload is already completed")
        if artifacts["upload_csv"] != "present":
            blockers.append("upload_ready requires local output/upload.csv unless upload is already completed")
    elif artifacts["youtube_upload"] != "completed" and (
        "upload" in current.get("next_action", "").lower() or "render" in current.get("next_action", "").lower()
    ):
        if artifacts["final_mkv"] != "present" or artifacts["upload_csv"] != "present":
            warnings.append("render/upload artifacts are missing; this is a blocker only for render_final/upload_ready")

    if (
        phase == "upload_ready"
        and artifacts["youtube_upload"] != "completed"
        and artifacts["subtitle_txt"] == "missing"
        and artifacts["subtitle_srt"] == "missing"
    ):
        blockers.append("upload_ready requires subtitle txt or srt")
    if phase == "uploaded" and artifacts["youtube_upload"] != "completed":
        blockers.append("uploaded phase requires concept.md upload completion evidence")

    if _has_stale_final_todo(concept_text):
        warnings.append("concept.md contains Final Track Sources but still has draft/Suno stale status text")

    result = "PASS" if not blockers else "FAIL"
    return {
        "schema": "wavvy.state.check.v1",
        "result": result,
        "state": current,
        "warnings": warnings,
        "blockers": blockers,
    }


def write_state(repo_root: Path, state_payload: dict[str, Any], if_match: Optional[int] = None) -> Path:
    """Atomically write .ai/state.json."""
    repo_root = repo_root.resolve()
    state_path = repo_root / ".ai" / "state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_state(repo_root)
    current_revision = int(existing.get("revision", 0) or 0)
    if if_match is not None and current_revision != if_match:
        raise ValueError(f"state revision mismatch: expected {if_match}, current {current_revision}")
    state_payload = dict(state_payload)
    state_payload["revision"] = current_revision + 1
    state_payload["updated_at"] = datetime.now().isoformat(timespec="seconds")

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=state_path.parent, delete=False) as tmp:
        json.dump(state_payload, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(state_path)
    return state_path
