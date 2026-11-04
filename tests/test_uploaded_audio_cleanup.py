"""Recorded post-upload audio cleanup: the uploaded gate accepts it, every earlier stage does not.

Synthetic series only. Policy basis: MASTER/SSOT.md Phase Contract (`uploaded` may delete large
local artifacts once upload completion is recorded in concept.md) and Zen's 2026-11-04 decision.
"""

import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from wavvy import ProjectPaths, cli, validate_project
from wavvy_harness.gate import run_gate
from wavvy_harness.state import build_state, check_state, uploaded_audio_cleanup_errors

FILES = {1: "01__One__A__Genre__100.wav", 2: "02__Two__B__Genre__110.wav"}
UPLOAD_COMPLETED = "## Upload Status\n\n- YouTube upload: completed\n\n"
METADATA = """## YouTube Metadata

### 제목
```text
Playlist | Test | Study | Wavvy | 23:30
```

### 설명
```text
description
```

### 태그
```text
tag1,tag2
```

"""
AUDIO_BLOCKER = "source_final requires audio files in input/tracks or concept.md Track Selection source map"
NO_AUDIO_ERROR = "No audio files (MP3/WAV) found in"


def digest(order: int) -> str:
    return hashlib.sha256(f"audio-{order}".encode()).hexdigest()


def final_track_sources(*, hashes: dict[int, str] | None = None, drop_hash_for: int | None = None) -> str:
    lines = ["## Final Track Sources", ""]
    for order, filename in FILES.items():
        lines += [f"### {order:02d}. Track {order}", "", f"- Filename: `{filename}`"]
        if order != drop_hash_for:
            lines.append(f"- SHA-256: `{(hashes or {}).get(order, digest(order))}`")
        lines += ["- Source Checksum: `" + "0" * 64 + "`", "", "#### STYLE", "```text", "style", "```", ""]
    return "\n".join(lines) + "\n"


def write_report(series: Path, hashes: dict[int, str] | None = None) -> None:
    tracks = [{"order": o, "title": f"Track {o}", "filename": f, "sha256": (hashes or {}).get(o, digest(o))}
              for o, f in FILES.items()]
    (series / "output" / "report.json").write_text(json.dumps({"tracks": tracks}), encoding="utf-8")


def make_series(root: Path, *, upload_status: str = UPLOAD_COMPLETED, sources: str | None = None, report: bool = True) -> Path:
    series = root / "SERIES" / "23-30"
    (series / "input" / "tracks").mkdir(parents=True)
    (series / "output").mkdir()
    (series / "input" / "video-background.png").write_bytes(b"png")
    (series / "input" / "thumb.jpg").write_bytes(b"jpg")
    sources = final_track_sources() if sources is None else sources
    (series / "concept.md").write_text("# Test Series\n\n" + upload_status + METADATA + sources, encoding="utf-8")
    if report:
        write_report(series)
    return series


def write_wav(path: Path) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(48000)
        handle.writeframes(b"\x00\x00" * 4800)


class UploadedAudioCleanupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        patcher = patch("wavvy.git_repo_root", return_value=self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def gate(self, series: Path, stage: str) -> tuple[int, dict]:
        result = CliRunner().invoke(cli, ["gate", str(series), "--stage", stage, "--json"])
        return result.exit_code, json.loads(result.output)

    def state_check(self, series: Path) -> tuple[int, dict]:
        result = CliRunner().invoke(cli, ["state", str(series), "--check", "--json"])
        return result.exit_code, json.loads(result.output)

    def test_recorded_upload_and_sources_with_no_audio_pass_uploaded(self):
        series = make_series(self.root)
        code, gate = self.gate(series, "uploaded")
        self.assertEqual((code, gate["result"], gate["blockers"]), (0, "PASS", []))
        checks = {check["name"]: check for check in gate["checks"]}
        self.assertEqual(checks["audio_files_present"]["status"], "PASS")
        self.assertIn("deleted_after_upload", checks["audio_files_present"]["detail"])
        self.assertIn("local audio files deleted after upload; restore them before running pack again", gate["warnings"])

        code, state = self.state_check(series)
        self.assertEqual((code, state["result"]), (0, "PASS"))
        artifacts = state["state"]["artifact_status"]
        self.assertEqual(artifacts["audio_source"], "deleted_after_upload")
        self.assertEqual((artifacts["audio_files"], artifacts["available_audio_files"]), (0, 0))
        self.assertEqual(state["state"]["phase"], "uploaded")
        self.assertIn("Restore the audio before running pack again", state["state"]["next_action"])

        result = CliRunner().invoke(cli, ["validate", str(series)])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("VALIDATION PASSED", result.output)

    def test_missing_tracks_directory_is_the_same_cleanup(self):
        series = make_series(self.root)
        (series / "input" / "tracks").rmdir()
        code, gate = self.gate(series, "uploaded")
        self.assertEqual((code, gate["result"]), (0, "PASS"))

    def test_no_recorded_upload_completion_still_fails(self):
        series = make_series(self.root, upload_status="")
        code, gate = self.gate(series, "uploaded")
        self.assertEqual((code, gate["result"]), (1, "FAIL"))
        self.assertTrue(any(NO_AUDIO_ERROR in blocker for blocker in gate["blockers"]), gate["blockers"])
        self.assertIn(AUDIO_BLOCKER, gate["blockers"])
        self.assertIn("uploaded phase requires concept.md upload completion evidence", gate["blockers"])
        self.assertEqual(self.state_check(series)[1]["state"]["artifact_status"]["audio_source"], "missing")
        self.assertEqual(CliRunner().invoke(cli, ["validate", str(series)]).exit_code, 1)

    def test_empty_pending_conflicting_or_duplicate_upload_status_still_fails(self):
        statuses = {
            "empty": "## Upload Status\n\n",
            "pending": "## Upload Status\n\n- YouTube upload: not uploaded yet\n\n",
            "conflict": "## Upload Status\n\n- YouTube upload: completed\n- YouTube upload: pending\n\n",
            "duplicate": UPLOAD_COMPLETED + UPLOAD_COMPLETED,
        }
        for name, status in statuses.items():
            with self.subTest(status=name):
                series = make_series(self.root / name, upload_status=status)
                self.assertEqual(uploaded_audio_cleanup_errors(series), ["YouTube upload completion is not recorded in concept.md"])
                code, gate = self.gate(series, "uploaded")
                self.assertEqual((code, gate["result"]), (1, "FAIL"))
                self.assertIn(AUDIO_BLOCKER, gate["blockers"])

    def test_completed_upload_without_a_usable_source_record_still_fails(self):
        cases = {
            "no archive": (make_series(self.root / "none", sources=""), "concept.md has no Final Track Sources archive of the deleted audio"),
            "no hash": (make_series(self.root / "nohash", sources=final_track_sources(drop_hash_for=2)),
                        "Final Track Sources track 02 lacks the audio filename or SHA-256"),
            "short hash": (make_series(self.root / "short", sources=final_track_sources(hashes={1: "abc123"})),
                           "Final Track Sources track 01 lacks the audio filename or SHA-256"),
        }
        duplicate = final_track_sources() + f"### 01. Track 1 again\n\n- Filename: `{FILES[1]}`\n- SHA-256: `{digest(1)}`\n"
        cases["duplicate track"] = (make_series(self.root / "dup", sources=duplicate), "Final Track Sources lists track 01 more than once")
        series = make_series(self.root / "disagree")
        write_report(series, hashes={2: digest(1)})
        cases["report disagrees"] = (series, "Final Track Sources differ from output/report.json for track(s) 02")
        for name, (series, reason) in cases.items():
            with self.subTest(case=name):
                self.assertEqual(uploaded_audio_cleanup_errors(series), [reason])
                code, gate = self.gate(series, "uploaded")
                self.assertEqual((code, gate["result"]), (1, "FAIL"))
                self.assertTrue(any(NO_AUDIO_ERROR in blocker for blocker in gate["blockers"]), gate["blockers"])
                self.assertIn(AUDIO_BLOCKER, gate["blockers"])
                self.assertNotEqual(build_state(series, self.root)["artifact_status"]["audio_source"], "deleted_after_upload")

    def test_remaining_audio_files_keep_their_existing_checks(self):
        series = make_series(self.root)
        write_wav(series / "input" / "tracks" / FILES[1])
        code, gate = self.gate(series, "uploaded")
        self.assertEqual((code, gate["result"], gate["blockers"]), (0, "PASS", []))
        artifacts = self.state_check(series)[1]["state"]["artifact_status"]
        self.assertEqual((artifacts["audio_source"], artifacts["available_audio_files"]), ("input_tracks", 1))
        self.assertNotIn("local audio files deleted after upload; restore them before running pack again", gate["warnings"])

        (series / "input" / "tracks" / FILES[1]).write_bytes(b"not audio")
        code, gate = self.gate(series, "uploaded")
        self.assertEqual((code, gate["result"]), (1, "FAIL"))
        self.assertTrue(any("Audio integrity check failed" in blocker for blocker in gate["blockers"]), gate["blockers"])

    def test_stages_before_uploaded_still_require_audio(self):
        for upload_status in (UPLOAD_COMPLETED, ""):
            for stage in ("source-final", "render-final", "upload-ready"):
                with self.subTest(upload=bool(upload_status), stage=stage):
                    series = make_series(self.root / f"{bool(upload_status)}-{stage}", upload_status=upload_status)
                    code, gate = self.gate(series, stage)
                    self.assertEqual((code, gate["result"]), (1, "FAIL"))
                    self.assertTrue(any(NO_AUDIO_ERROR in blocker for blocker in gate["blockers"]), gate["blockers"])
                    self.assertIn(AUDIO_BLOCKER, gate["blockers"])
                    self.assertFalse(validate_project(ProjectPaths(series)).is_valid)

    def test_state_phase_decides_whether_the_cleanup_relieves_the_audio_blocker(self):
        series = make_series(self.root)
        self.assertEqual(check_state(series, self.root, {"phase": "uploaded"})["blockers"], [])
        for phase in ("source_final", "render_final", "upload_ready"):
            with self.subTest(phase=phase):
                result = check_state(series, self.root, {"phase": phase})
                self.assertEqual(result["result"], "FAIL")
                self.assertIn(AUDIO_BLOCKER, result["blockers"])
        # run_gate with an already-valid structural check still fails earlier stages on the state blocker.
        for stage in ("render-final", "upload-ready"):
            with self.subTest(stage=stage):
                gate = run_gate(series, self.root, stage, {"is_valid": True, "errors": [], "warnings": []})
                self.assertEqual(gate["result"], "FAIL")
                self.assertIn(AUDIO_BLOCKER, gate["blockers"])

    def test_pack_and_preview_validation_never_get_the_relief(self):
        series = make_series(self.root)
        result = validate_project(ProjectPaths(series))
        self.assertFalse(result.is_valid)
        self.assertTrue(any(NO_AUDIO_ERROR in error for error in result.errors), result.errors)
        relieved = validate_project(ProjectPaths(series), allow_uploaded_audio_cleanup=True)
        self.assertTrue(relieved.is_valid, relieved.errors)
        self.assertEqual(relieved.tracks, [])


if __name__ == "__main__":
    unittest.main()
