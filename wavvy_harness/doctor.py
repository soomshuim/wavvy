"""Environment checks for Wavvy harness operations."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


REQUIRED_MODULES = {
    "click": "click",
    "ffmpeg-python": "ffmpeg",
    "pandas": "pandas",
    "ffmpeg-normalize": "ffmpeg_normalize",
    "Pillow": "PIL",
}

REQUIRED_BINARIES = ["ffmpeg", "ffprobe", "git"]
DEFAULT_PEER_REVIEW_SCRIPT = Path("~/Project/agent-center/scripts/peer-review/orchestrate.sh").expanduser()
DEFAULT_FFMPEG_FULL = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")
REQUIRED_SSOT_DOCS = [
    "AGENTS.md",
    "CLAUDE.md",
    "MASTER/SSOT.md",
    "MASTER/ai/RUNTIME_RULES.md",
    "MASTER/MANAGER.md",
    "MASTER/WORKFLOWS.md",
    "MASTER/cli/SPEC.md",
    "MASTER/youtube/YOUTUBE.md",
    "wavvy.md",
]
CORE_ROUTER_TARGETS = [
    "MASTER/SSOT.md",
    "MASTER/ai/RUNTIME_RULES.md",
    "MASTER/MANAGER.md",
    "MASTER/WORKFLOWS.md",
    "MASTER/cli/SPEC.md",
]
ENTRYPOINT_DOCS = ["AGENTS.md", "CLAUDE.md", "MASTER/ai/RUNTIME_RULES.md"]
STALE_ENTRYPOINT_PATTERNS = {
    "stale_project_name_vibem": r"\bVIBEM\b",
    "stale_output_final_mp4": r"final\.mp4",
    "unconditional_video_crossfade": r"Video Crossfade 필수|vfade --test.*pack",
}
STATE_REQUIRED_DOCS = {
    "MASTER/SSOT.md",
    "MASTER/ai/RUNTIME_RULES.md",
    "MASTER/cli/SPEC.md",
}


def _check_module(package_name: str, module_name: str) -> dict[str, Any]:
    present = importlib.util.find_spec(module_name) is not None
    return {
        "name": package_name,
        "module": module_name,
        "required": True,
        "status": "pass" if present else "fail",
    }


def _binary_version(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        return ""
    try:
        result = subprocess.run(
            [path, "-version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except Exception:
        return path
    first_line = result.stdout.splitlines()[0] if result.stdout else path
    return first_line.strip()


def _check_binary(binary: str) -> dict[str, Any]:
    path = shutil.which(binary)
    return {
        "name": binary,
        "path": path or "",
        "version": _binary_version(binary) if path else "",
        "required": True,
        "status": "pass" if path else "fail",
    }


def _check_writable_temp(repo_root: Path) -> dict[str, Any]:
    base = repo_root / ".ai" / "tmp"
    try:
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=base, prefix="doctor-", delete=True) as tmp:
            tmp.write("ok")
            tmp.flush()
        return {"name": "workspace_writable", "path": str(base), "required": True, "status": "pass"}
    except Exception as exc:
        return {
            "name": "workspace_writable",
            "path": str(base),
            "required": True,
            "status": "fail",
            "detail": str(exc),
        }


def _check_disk(repo_root: Path) -> dict[str, Any]:
    usage = shutil.disk_usage(repo_root)
    free_gib = usage.free / (1024**3)
    status = "pass" if free_gib >= 5 else "warn"
    return {
        "name": "disk_free",
        "path": str(repo_root),
        "required": False,
        "status": status,
        "free_gib": round(free_gib, 2),
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _check_required_ssot_docs(repo_root: Path) -> dict[str, Any]:
    missing = [rel for rel in REQUIRED_SSOT_DOCS if not (repo_root / rel).exists()]
    return {
        "name": "ssot_docs_present",
        "required": True,
        "status": "pass" if not missing else "fail",
        "detail": "" if not missing else f"missing: {', '.join(missing)}",
    }


def _check_router_targets(repo_root: Path) -> dict[str, Any]:
    missing = []
    for router in ["AGENTS.md", "CLAUDE.md"]:
        text = _read_text(repo_root / router)
        for target in CORE_ROUTER_TARGETS:
            if target not in text:
                missing.append(f"{router}:{target}")
    return {
        "name": "router_targets_consistent",
        "required": True,
        "status": "pass" if not missing else "fail",
        "detail": "" if not missing else f"missing: {', '.join(missing)}",
    }


def _check_entrypoint_stale_patterns(repo_root: Path) -> dict[str, Any]:
    hits = []
    for rel in ENTRYPOINT_DOCS:
        text = _read_text(repo_root / rel)
        for label, pattern in STALE_ENTRYPOINT_PATTERNS.items():
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                hits.append(f"{rel}:{label}")
    return {
        "name": "entrypoint_stale_patterns_absent",
        "required": True,
        "status": "pass" if not hits else "fail",
        "detail": "" if not hits else f"hits: {', '.join(hits)}",
    }


def _check_state_authoritative_docs(repo_root: Path) -> dict[str, Any]:
    state_path = repo_root / ".ai" / "state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "name": "state_authoritative_docs_current",
            "path": str(state_path),
            "required": True,
            "status": "fail",
            "detail": f"cannot read state: {exc}",
        }

    authoritative_docs = set(state.get("authoritative_docs", []))
    missing = sorted(STATE_REQUIRED_DOCS - authoritative_docs)
    return {
        "name": "state_authoritative_docs_current",
        "path": str(state_path),
        "required": True,
        "status": "pass" if not missing else "fail",
        "detail": "" if not missing else f"missing: {', '.join(missing)}",
    }


def _check_no_tracked_ds_store(repo_root: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {
            "name": "tracked_ds_store_absent",
            "required": False,
            "status": "warn",
            "detail": "not a git repository or git ls-files failed",
        }
    tracked = [line for line in result.stdout.splitlines() if line.endswith(".DS_Store")]
    return {
        "name": "tracked_ds_store_absent",
        "required": True,
        "status": "pass" if not tracked else "fail",
        "detail": "" if not tracked else f"tracked: {', '.join(tracked)}",
    }


def run_ssot_hygiene(repo_root: Path) -> list[dict[str, Any]]:
    """Run deterministic SSOT/router drift checks."""
    repo_root = repo_root.resolve()
    return [
        _check_required_ssot_docs(repo_root),
        _check_router_targets(repo_root),
        _check_entrypoint_stale_patterns(repo_root),
        _check_state_authoritative_docs(repo_root),
        _check_no_tracked_ds_store(repo_root),
    ]


def run_doctor(repo_root: Path) -> dict[str, Any]:
    """Run deterministic local dependency checks."""
    repo_root = repo_root.resolve()
    checks: list[dict[str, Any]] = []

    for package_name, module_name in REQUIRED_MODULES.items():
        checks.append(_check_module(package_name, module_name))

    for binary in REQUIRED_BINARIES:
        checks.append(_check_binary(binary))

    peer_script = Path(os.environ.get("WAVVY_PEER_REVIEW_SCRIPT", str(DEFAULT_PEER_REVIEW_SCRIPT))).expanduser()
    checks.append(
        {
            "name": "peer_review_script",
            "path": str(peer_script),
            "required": True,
            "status": "pass" if peer_script.exists() else "fail",
        }
    )

    checks.append(
        {
            "name": "ffmpeg_full_drawtext",
            "path": str(DEFAULT_FFMPEG_FULL),
            "required": False,
            "status": "pass" if DEFAULT_FFMPEG_FULL.exists() else "warn",
        }
    )
    checks.append(_check_disk(repo_root))
    checks.append(_check_writable_temp(repo_root))
    checks.extend(run_ssot_hygiene(repo_root))

    blockers = [check for check in checks if check.get("required") and check.get("status") == "fail"]
    warnings = [check for check in checks if check.get("status") == "warn"]

    return {
        "schema": "wavvy.doctor.v1",
        "repo": str(repo_root),
        "result": "PASS" if not blockers else "FAIL",
        "checks": checks,
        "warnings": warnings,
        "blockers": blockers,
    }
