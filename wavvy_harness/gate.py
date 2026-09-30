"""Stage gates for Wavvy series."""

from __future__ import annotations

import hashlib
import subprocess
import re
from pathlib import Path
from typing import Any

from .state import check_state

LYRIC_SKILL_REQUIRED_FILES = {
    "skill": Path("skills/wavvy-lyricist/SKILL.md"),
    "patterns": Path("skills/wavvy-lyricist/references/patterns.md"),
    "spec": Path("MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md"),
}
LYRIC_OUTPUT_MODES = ("full-lyric-draft", "suno-prompt-only", "review-only")
LYRIC_DRAFT_SECTIONS = ("Source Map", "Constraint Freeze", "Lyric Strategy", "Draft", "Self-Gate")
LYRIC_REVIEW_SECTIONS = ("Source Map", "Constraint Freeze", "Findings", "Verdict")
LYRIC_CONTRACT_GATE_NAMES = (
    "Copyright Safety",
    "Wavvy Identity",
    "Series DNA",
    "Suno Format",
)
LYRIC_REVIEW_AXES = ("Expression", "Connection", "Emotional Flow")


def _check(name: str, passed: bool, detail: str = "") -> dict[str, Any]:
    return {
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
    }


def _status_check(name: str, status: str, detail: str = "", path: Path | None = None) -> dict[str, Any]:
    check: dict[str, Any] = {
        "name": name,
        "status": status,
        "detail": detail,
    }
    if path is not None:
        check["path"] = str(path)
    return check


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _token_count(text: str, token: str) -> int:
    pattern = rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])"
    return len(re.findall(pattern, text))


def _heading_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"^(?:#{{1,6}}\s*)?{re.escape(label)}\s*$", flags=re.MULTILINE)


def _section_position(text: str, label: str) -> int:
    match = _heading_pattern(label).search(text)
    return match.start() if match else -1


def _sections_in_order(text: str, labels: tuple[str, ...]) -> bool:
    positions = [_section_position(text, label) for label in labels]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def _extract_section(text: str, label: str) -> str:
    match = _heading_pattern(label).search(text)
    if not match:
        return ""
    start = match.end()
    next_positions = []
    for candidate in set(LYRIC_DRAFT_SECTIONS + LYRIC_REVIEW_SECTIONS):
        if candidate == label:
            continue
        next_match = _heading_pattern(candidate).search(text, start)
        if next_match:
            next_positions.append(next_match.start())
    end = min(next_positions) if next_positions else len(text)
    return text[start:end].strip()


def _infer_artifact_mode(text: str) -> tuple[str | None, dict[str, int], int]:
    constraint_freeze = _extract_section(text, "Constraint Freeze")
    counts = {mode: _token_count(constraint_freeze, mode) for mode in LYRIC_OUTPUT_MODES}
    total = sum(counts.values())
    mode = next((candidate for candidate, count in counts.items() if count == 1), None) if total == 1 else None
    return mode, counts, total


def _korean_lyric_lines(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "```", "|")):
            continue
        if re.fullmatch(r"(?:\[[^\]]+\]\s*)+", stripped):
            continue
        if re.search(r"[가-힣]", stripped):
            lines.append(stripped)
    return lines


def _field_lines(text: str, label: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(rf"(?im)^\s*[-*]?\s*{re.escape(label)}\s*:\s*(.*?)\s*$", text)
    ]


def _reviewed_body(mode: str, artifact_path: Path, text: str, evidence: str) -> tuple[str, str]:
    """Return the reviewed lyric body and a source error, if any."""
    sources = _field_lines(evidence, "Review Source")
    if len(sources) != 1:
        return "", "Review Source must appear exactly once"
    if mode == "full-lyric-draft":
        if sources[0] != "Draft":
            return "", "full-lyric-draft Review Source must be Draft"
        return _extract_section(text, "Draft"), ""

    if sources[0] == "Draft":
        return "", "review-only Review Source must name a readable lyric file"
    source_path = Path(sources[0])
    if not source_path.is_absolute():
        source_path = artifact_path.parent / source_path
    source_path = source_path.resolve()
    if source_path == artifact_path.resolve() or not source_path.is_file():
        return "", "review-only Review Source must be a separate readable lyric file"
    try:
        source_text = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "", "review-only Review Source cannot be read as UTF-8"
    if _section_position(source_text, "Draft") >= 0:
        return _extract_section(source_text, "Draft"), ""
    has_artifact_metadata = any(_section_position(source_text, label) >= 0 for label in (*LYRIC_DRAFT_SECTIONS, *LYRIC_REVIEW_SECTIONS))
    if source_path.name == "concept.md" or has_artifact_metadata or re.search(r"(?im)^\s*(?:={3,}\s*(?:STYLE|EXCLUDE|LYRICS)|##\s+Final Track Sources)", source_text):
        return "", "review-only source has metadata but no Draft section; provide a lyric-body file"
    return source_text.strip(), ""


def _review_record_checks(
    mode: str, artifact_path: Path, text: str, evidence: str
) -> tuple[list[dict[str, Any]], list[str], list[str], str]:
    """Check review evidence binding and completeness, never the truth of its judgments."""
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []
    decisions: list[str] = []
    body, source_error = _reviewed_body(mode, artifact_path, text, evidence)
    lyric_lines = [line.strip() for line in body.splitlines() if line.strip() and not re.fullmatch(r"(?:\[[^]]+\]\s*)+", line.strip())]
    body_ok = not source_error and any(re.search(r"[가-힣A-Za-z]{2,}", line) for line in lyric_lines)
    checks.append(_status_check("reviewed_lyric_body_present", "PASS" if body_ok else "FAIL", source_error or f"{len(lyric_lines)} lyric lines", artifact_path))
    if not body_ok:
        blockers.append(source_error or "reviewed lyric body is empty or has only structure tags")

    actual_hash = hashlib.sha256(body.encode("utf-8")).hexdigest() if body_ok else ""
    claimed_hashes = _field_lines(evidence, "Source SHA256")
    hash_ok = body_ok and len(claimed_hashes) == 1 and claimed_hashes[0].lower() == actual_hash
    checks.append(_status_check("reviewed_source_sha256_matches", "PASS" if hash_ok else "FAIL", f"actual_sha256={actual_hash}; claimed={','.join(claimed_hashes)}", artifact_path))
    if not hash_ok:
        blockers.append("review evidence is missing, duplicated, or stale for the current lyric body")

    for label in (*LYRIC_REVIEW_AXES, *LYRIC_CONTRACT_GATE_NAMES):
        entries = _field_lines(evidence, label)
        status = ""
        valid = len(entries) == 1
        if valid:
            parts = [part.strip() for part in entries[0].split("|", 2)]
            status = parts[0].upper()
            valid = len(parts) == (3 if label in LYRIC_REVIEW_AXES else 2) and status in {"PASS", "HOLD", "FAIL"}
            if valid and label in LYRIC_REVIEW_AXES:
                quote = parts[1]
                quoted_text = quote[1:-1] if quote.startswith('"') and quote.endswith('"') else ""
                valid = bool(quoted_text.strip()) and quoted_text in body and bool(re.search(r"[가-힣A-Za-z]{2,}", quoted_text))
            if valid:
                valid = bool(parts[-1]) and parts[-1].lower() not in {"n/a", "none", "tbd", "unknown", "미정", "없음"}
        checks.append(_status_check(f"review_{label.lower().replace(' ', '_')}_evidence", "PASS" if valid else "FAIL", status if valid else "missing/duplicate/invalid status, quote, or reason", artifact_path))
        if not valid:
            blockers.append(f"{label} review evidence must appear once with status, {'exact quote, ' if label in LYRIC_REVIEW_AXES else ''}and reason")
        elif status == "FAIL":
            blockers.append(f"{label} review status is FAIL")
        elif status == "HOLD":
            decisions.append(f"{label} review status is HOLD")
    return checks, blockers, decisions, actual_hash


def _lyric_package_checks(repo_root: Path) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []
    evidence_refs: list[str] = []

    paths = {name: repo_root / rel_path for name, rel_path in LYRIC_SKILL_REQUIRED_FILES.items()}
    for name, path in paths.items():
        exists = path.exists()
        checks.append(_status_check(f"{name}_file_present", "PASS" if exists else "FAIL", str(LYRIC_SKILL_REQUIRED_FILES[name]), path))
        if exists:
            evidence_refs.append(LYRIC_SKILL_REQUIRED_FILES[name].as_posix())
        else:
            blockers.append(f"missing required lyric skill file: {LYRIC_SKILL_REQUIRED_FILES[name]}")

    skill_text = _read_text(paths["skill"])
    patterns_text = _read_text(paths["patterns"])
    spec_text = _read_text(paths["spec"])

    front_matter_ok = bool(re.search(r"(?ms)^---\s.*?^name:\s*wavvy-lyricist\s*$.*?^---\s*", skill_text))
    checks.append(_status_check("skill_front_matter_name", "PASS" if front_matter_ok else "FAIL", "name: wavvy-lyricist"))
    if not front_matter_ok:
        blockers.append("SKILL.md front matter must contain name: wavvy-lyricist")

    for mode in LYRIC_OUTPUT_MODES:
        present = mode in skill_text
        checks.append(_status_check(f"skill_names_mode_{mode}", "PASS" if present else "FAIL", mode))
        if not present:
            blockers.append(f"SKILL.md must name output mode: {mode}")

    for label in dict.fromkeys(LYRIC_DRAFT_SECTIONS + LYRIC_REVIEW_SECTIONS):
        present = label in skill_text
        checks.append(_status_check(f"skill_output_section_{label.lower().replace(' ', '_')}", "PASS" if present else "FAIL", label))
        if not present:
            blockers.append(f"SKILL.md must contain output section label: {label}")

    for required_ref in ("MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md", "skills/wavvy-lyricist/references/patterns.md"):
        present = required_ref in skill_text
        checks.append(_status_check(f"skill_references_{Path(required_ref).name}", "PASS" if present else "FAIL", required_ref))
        if not present:
            blockers.append(f"SKILL.md must reference {required_ref}")

    no_external_lyrics = bool(
        re.search(
            r"does not store copied, translated.*external lyric lines|copied/translated external lyric lines are not stored",
            patterns_text,
            flags=re.IGNORECASE | re.DOTALL,
        )
    )
    checks.append(_status_check("patterns_external_lyric_storage_boundary", "PASS" if no_external_lyrics else "FAIL"))
    if not no_external_lyrics:
        blockers.append("patterns.md must state that copied/translated external lyric lines are not stored")

    for heading in ("Self-Gate Contract", "Harness Acceptance Baseline"):
        present = heading in spec_text
        checks.append(_status_check(f"spec_defines_{heading.lower().replace('-', '_').replace(' ', '_')}", "PASS" if present else "FAIL", heading))
        if not present:
            blockers.append(f"skill spec must define {heading}")

    return checks, blockers, evidence_refs


def _lyric_artifact_checks(
    artifact_path: Path,
    requested_mode: str | None,
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str], str]:
    checks: list[dict[str, Any]] = []
    blockers: list[str] = []
    user_decisions: list[str] = []
    evidence_refs = [str(artifact_path)]
    text = _read_text(artifact_path)

    inferred_mode, mode_counts, total_modes = _infer_artifact_mode(text)
    mode = requested_mode or inferred_mode
    mode_detail = ", ".join(f"{key}={value}" for key, value in mode_counts.items())
    mode_ok = total_modes == 1 and (requested_mode is None or inferred_mode == requested_mode)
    checks.append(_status_check("constraint_freeze_mode_exactly_once", "PASS" if mode_ok else "FAIL", mode_detail, artifact_path))
    if not mode_ok:
        blockers.append("Constraint Freeze must name exactly one output mode matching --mode when provided")

    section_labels = LYRIC_REVIEW_SECTIONS if mode == "review-only" else LYRIC_DRAFT_SECTIONS
    sections_ok = _sections_in_order(text, section_labels)
    checks.append(_status_check("required_output_sections_in_order", "PASS" if sections_ok else "FAIL", " > ".join(section_labels), artifact_path))
    if not sections_ok:
        blockers.append("lyric artifact output sections are missing or out of order")

    constraint_freeze = _extract_section(text, "Constraint Freeze")
    draft = _extract_section(text, "Draft")
    self_gate = _extract_section(text, "Self-Gate")

    if mode == "suno-prompt-only":
        korean_lines = _korean_lyric_lines(draft)
        checks.append(
            _status_check(
                "suno_prompt_only_has_no_korean_lyric_rows",
                "PASS" if not korean_lines else "FAIL",
                f"{len(korean_lines)} Korean lyric-like lines",
                artifact_path,
            )
        )
        if korean_lines:
            blockers.append("suno-prompt-only output must not contain full Korean lyric rows")

    actual_hash = ""
    if mode in {"full-lyric-draft", "review-only"}:
        evidence = self_gate if mode == "full-lyric-draft" else _extract_section(text, "Findings")
        review_checks, review_blockers, review_decisions, actual_hash = _review_record_checks(mode, artifact_path, text, evidence)
        checks.extend(review_checks)
        blockers.extend(review_blockers)
        user_decisions.extend(review_decisions)
    elif mode == "suno-prompt-only":
        prompt_lines = [line.strip() for line in draft.splitlines() if line.strip()]
        empty_selected = bool(re.search(r"(?im)^\s*[-*]?\s*suno_input\s*:\s*Empty\s*$", constraint_freeze))
        prompt_ok = (not prompt_lines and empty_selected) or (not empty_selected and 1 <= len(prompt_lines) <= 3 and not any(line.startswith("(") for line in prompt_lines))
        checks.append(_status_check("suno_prompt_shape", "PASS" if prompt_ok else "FAIL", f"{len(prompt_lines)} nonempty lines", artifact_path))
        if not prompt_ok:
            blockers.append("suno-prompt-only Draft must have 1-3 non-parenthesized lines, or an empty Draft with suno_input: Empty")
        for label in LYRIC_CONTRACT_GATE_NAMES:
            entries = _field_lines(self_gate, label)
            parts = [part.strip() for part in entries[0].split("|", 1)] if len(entries) == 1 else []
            valid = len(parts) == 2 and parts[0].upper() in {"PASS", "HOLD", "FAIL"} and bool(parts[1])
            checks.append(_status_check(f"prompt_{label.lower().replace(' ', '_')}_recorded", "PASS" if valid else "FAIL", parts[0] if valid else "missing/duplicate status or reason", artifact_path))
            if not valid:
                blockers.append(f"suno-prompt-only {label} must have one status and reason")
            elif parts[0].upper() == "FAIL":
                blockers.append(f"suno-prompt-only {label} is FAIL")
            elif parts[0].upper() == "HOLD":
                user_decisions.append(f"suno-prompt-only {label} is HOLD")
    else:
        blockers.append("lyric artifact mode is missing or unsupported")

    if mode == "review-only":
        verdict = _extract_section(text, "Verdict")
        verdict_lines = [line.strip() for line in verdict.splitlines() if line.strip()]
        parts = [part.strip() for part in verdict_lines[0].split("|", 1)] if len(verdict_lines) == 1 else []
        verdict_ok = len(parts) == 2 and parts[0].upper() in {"PASS", "HOLD", "FAIL"} and bool(parts[1])
        checks.append(_status_check("review_verdict_recorded", "PASS" if verdict_ok else "FAIL", parts[0] if verdict_ok else "one verdict and reason required", artifact_path))
        if not verdict_ok:
            blockers.append("review-only Verdict must contain exactly one PASS, HOLD, or FAIL with a reason")
        elif parts[0].upper() == "FAIL":
            blockers.append("review-only Verdict is FAIL")
        elif parts[0].upper() == "HOLD":
            user_decisions.append("review-only Verdict is HOLD")
        elif user_decisions or blockers:
            blockers.append("review-only PASS Verdict conflicts with review evidence status")

    return checks, blockers, user_decisions, evidence_refs, actual_hash


def run_lyrics_skill_gate(
    repo_root: Path,
    series_path: Path | None = None,
    artifact_path: Path | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Validate the Wavvy lyric skill package and optional lyric artifact."""
    repo_root = repo_root.resolve()
    checks, blockers, evidence_refs = _lyric_package_checks(repo_root)
    warnings: list[str] = []
    user_decisions: list[str] = []
    actual_hash = ""
    effective_mode = mode or (_infer_artifact_mode(_read_text(artifact_path))[0] if artifact_path else None)

    if series_path is not None:
        concept_path = series_path / "concept.md"
        concept_ok = bool(_read_text(concept_path))
        checks.append(_status_check("series_concept_present", "PASS" if concept_ok else "FAIL", str(concept_path), concept_path))
        evidence_refs.append(str(concept_path))
        if not concept_ok:
            blockers.append("series concept.md is required when a series path is supplied")

    if artifact_path is not None:
        artifact_checks, artifact_blockers, artifact_decisions, artifact_refs, actual_hash = _lyric_artifact_checks(
            artifact_path,
            mode,
        )
        checks.extend(artifact_checks)
        blockers.extend(artifact_blockers)
        user_decisions.extend(artifact_decisions)
        evidence_refs.extend(artifact_refs)

    result = "FAIL" if blockers else ("USER_DECISION" if user_decisions else "PASS")
    if artifact_path is None:
        quality_status = "NOT_REVIEWED"
    elif result == "FAIL":
        quality_status = "RECORD_INVALID"
    elif result == "USER_DECISION":
        quality_status = "RECORD_ON_HOLD"
    else:
        quality_status = "PROMPT_INPUT_CHECKED" if effective_mode == "suno-prompt-only" else "REVIEW_RECORD_CHECKED"
    return {
        "schema": "wavvy.lyrics_skill_gate.v1",
        "stage": "lyrics-review",
        "result": result,
        "scope": "ARTIFACT_RECORD" if artifact_path else "PACKAGE_ONLY",
        "quality_status": quality_status,
        "reviewed_source_sha256": actual_hash,
        "series": str(series_path) if series_path else "",
        "artifact": str(artifact_path) if artifact_path else "",
        "mode": effective_mode or "",
        "checks": checks,
        "warnings": sorted(set(warnings)),
        "blockers": sorted(set(blockers)),
        "user_decisions": sorted(set(user_decisions)),
        "evidence_refs": sorted(set(evidence_refs)),
    }


def _has_media_stream(path: Path, stream_type: str) -> bool:
    selector = "v:0" if stream_type == "video" else "a:0"
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            selector,
            "-show_entries",
            "stream=codec_type",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and stream_type in result.stdout


def run_gate(
    series_path: Path,
    repo_root: Path,
    stage: str,
    validation: dict[str, Any],
    lyric_artifact: Path | None = None,
    lyric_mode: str | None = None,
) -> dict[str, Any]:
    """Run a stage-specific gate."""
    stage = stage.replace("_", "-")
    if stage not in {"source-final", "render-final", "upload-ready", "uploaded", "lyrics-review"}:
        raise ValueError(f"unknown stage: {stage}")

    if stage == "lyrics-review":
        payload = run_lyrics_skill_gate(repo_root, series_path, lyric_artifact, lyric_mode)
        if lyric_artifact is None:
            payload["result"] = "FAIL"
            payload["blockers"].append("lyrics-review requires --artifact; package installation alone does not review a lyric")
        return payload

    checks: list[dict[str, Any]] = []
    warnings: list[str] = []
    blockers: list[str] = []

    validation_passed = bool(validation.get("is_valid"))
    checks.append(_check("validate_project", validation_passed, validation.get("detail", "")))
    if not validation_passed:
        blockers.extend(validation.get("errors", ["validate_project failed"]))

    state_result = check_state(series_path, repo_root, {"phase": stage.replace("-", "_")})
    state = state_result["state"]
    artifacts = state["artifact_status"]
    warnings.extend(state_result.get("warnings", []))
    blockers.extend(state_result.get("blockers", []))
    available_audio_files = artifacts.get("available_audio_files", artifacts.get("audio_files", 0))
    audio_source = artifacts.get("audio_source", "input_tracks")

    source_checks = [
        ("concept_md_present", artifacts["concept_md"] == "present"),
        (
            "final_track_sources_or_source_map_present",
            artifacts["final_track_sources"] == "present" or artifacts.get("source_map") == "present",
        ),
        (
            "report_json_present_or_source_map_ready",
            artifacts["report_json"] == "present"
            or (artifacts.get("source_map") == "present" and not artifacts.get("source_map_missing")),
        ),
        ("youtube_metadata_present", artifacts["youtube_metadata"] == "present"),
        ("audio_files_present", available_audio_files > 0, f"{available_audio_files} audio files via {audio_source}"),
    ]
    for item in source_checks:
        name, passed, *detail = item
        checks.append(_check(name, bool(passed), detail[0] if detail else ""))

    if artifacts["final_track_sources_count"] and artifacts["report_tracks"]:
        counts_match = artifacts["final_track_sources_count"] == artifacts["report_tracks"]
        checks.append(
            _check(
                "final_track_sources_match_report",
                counts_match,
                f"fts={artifacts['final_track_sources_count']} report={artifacts['report_tracks']}",
            )
        )

    tracks_dir = series_path / "input" / "tracks"
    has_txt = tracks_dir.exists() and any(tracks_dir.glob("*.txt"))
    rubric_snapshot = series_path / "rubric_snapshot.json"
    report_rubric = False
    if not has_txt and artifacts["final_track_sources"] == "present" and not rubric_snapshot.exists() and not report_rubric:
        warnings.append("rubric_unverified_after_finalize")

    if stage == "render-final":
        final_mkv = series_path / "output" / "final.mkv"
        upload_csv = series_path / "output" / "upload.csv"
        checks.append(_check("final_mkv_present", final_mkv.exists()))
        checks.append(_check("upload_csv_present", upload_csv.exists()))
        if final_mkv.exists():
            has_video = _has_media_stream(final_mkv, "video")
            has_audio = _has_media_stream(final_mkv, "audio")
            checks.append(_check("final_mkv_video_stream", has_video))
            checks.append(_check("final_mkv_audio_stream", has_audio))
            if not has_video:
                blockers.append("output/final.mkv missing video stream")
            if not has_audio:
                blockers.append("output/final.mkv missing audio stream")

    if stage == "upload-ready":
        upload_completed = artifacts["youtube_upload"] == "completed"
        final_mkv = series_path / "output" / "final.mkv"
        upload_csv = series_path / "output" / "upload.csv"
        checks.append(
            _check(
                "final_mkv_present_or_uploaded",
                final_mkv.exists() or upload_completed,
                artifacts["final_mkv"],
            )
        )
        checks.append(
            _check(
                "upload_csv_present_or_uploaded",
                upload_csv.exists() or upload_completed,
                artifacts["upload_csv"],
            )
        )
        checks.append(_check("youtube_upload_status", True, "completed" if upload_completed else "pending"))
        if final_mkv.exists():
            has_video = _has_media_stream(final_mkv, "video")
            has_audio = _has_media_stream(final_mkv, "audio")
            checks.append(_check("final_mkv_video_stream", has_video))
            checks.append(_check("final_mkv_audio_stream", has_audio))
            if not has_video:
                blockers.append("output/final.mkv missing video stream")
            if not has_audio:
                blockers.append("output/final.mkv missing audio stream")
        has_subtitle = artifacts["subtitle_txt"] == "present" or artifacts["subtitle_srt"] == "present"
        checks.append(_check("subtitle_artifact_present", has_subtitle))

    if stage == "uploaded":
        checks.append(_check("youtube_upload_completed", artifacts["youtube_upload"] == "completed"))
        if artifacts["final_mkv"] == "deleted_after_upload":
            warnings.append("local final.mkv deleted after upload; regenerate with pack if needed")
        if artifacts["upload_csv"] == "deleted_after_upload":
            warnings.append("local upload.csv deleted after upload; regenerate with pack if needed")

    return {
        "schema": "wavvy.gate.v1",
        "stage": stage,
        "result": "PASS" if not blockers else "FAIL",
        "series": str(series_path),
        "checks": checks,
        "warnings": sorted(set(warnings)),
        "blockers": sorted(set(blockers)),
    }
