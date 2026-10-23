import csv
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from wavvy import FinalizeUploadError, ProjectPaths, TrackInfo, TrackSource, build_final_track_sources_section, build_untimed_subtitles, cli, compute_track_timestamps, generate_report, parse_track_source, read_filesystem_track_sources, replace_final_track_sources_section, resolve_playback_source_bindings, validate_project, verify_final_selection_source_provenance, verify_release_package
from wavvy_harness.doctor import run_ssot_hygiene
from wavvy_harness.gate import run_gate, run_lyrics_skill_gate
from wavvy_harness.packaging import check_thumbnail_layout, packaging_contract
from wavvy_harness.selected_audio import check_selected_audio
from wavvy_harness.state import build_state, check_state


CONCEPT_FINAL = """# Test Series

## YouTube Metadata

### 제목
```text
Playlist | Test | Study | Wavvy | 20:00
```

### 설명
```text
description
```

### 태그
```text
tag1,tag2
```

## Final Track Sources

### 01. One

- Filename: `01__One__A__Genre__100.wav`

#### STYLE
```text
style
```

#### EXCLUDE
```text
None
```

#### LYRICS
```text
lyrics
```

### 02. Two

- Filename: `02__Two__B__Genre__110.wav`

#### STYLE
```text
style
```

#### EXCLUDE
```text
None
```

#### LYRICS
```text
lyrics
```
"""

CONCEPT_UPLOADED = CONCEPT_FINAL.replace(
    "## YouTube Metadata",
    "## Upload Status\n\n- YouTube upload completed\n- Local final.mkv deleted intentionally after upload.\n\n## YouTube Metadata",
)

CONCEPT_COMPILATION = """# R&B BEST

## Series Type

- **Type**: Compilation / Best Album

## YouTube Draft

### 제목
```text
Playlist | R&B Best | Wavvy
```

### 설명
```text
description
```

### 태그
```text
tag1,tag2
```

## Track Selection

| # | Title | Source | Copied Filename |
|---|---|---|---|
| 01 | One | `SERIES/01/input/tracks/09__One__Warm__RnB__90.wav` | `01__One__Warm__RnB__90.wav` |
| 02 | Two | `SERIES/02/work/norm_tracks/norm_03__Two__Cool__Soul__100.wav` | `02__Two__Cool__Soul__100.wav` |
"""


def make_series(root: Path, concept_text: str = CONCEPT_FINAL) -> Path:
    series = root / "SERIES" / "20-00"
    tracks = series / "input" / "tracks"
    output = series / "output"
    tracks.mkdir(parents=True)
    output.mkdir(parents=True)
    (series / "concept.md").write_text(concept_text, encoding="utf-8")
    (tracks / "01__One__A__Genre__100.wav").write_bytes(b"")
    (tracks / "02__Two__B__Genre__110.wav").write_bytes(b"")
    report = {
        "tracks": [
            {"order": 1, "title": "One", "filename": "01__One__A__Genre__100.wav"},
            {"order": 2, "title": "Two", "filename": "02__Two__B__Genre__110.wav"},
        ]
    }
    (output / "report.json").write_text(json.dumps(report), encoding="utf-8")
    return series


def make_draft_series(root: Path) -> Path:
    series = root / "SERIES" / "17-00"
    tracks = series / "input" / "tracks"
    tracks.mkdir(parents=True)
    (series / "concept.md").write_text("# Test Draft Series\n\n## Series Status\n\nTrack drafts in progress.\n", encoding="utf-8")
    (tracks / "01__Draft.txt").write_text("draft lyrics\n", encoding="utf-8")
    return series


class PackagingContractTests(unittest.TestCase):
    def _fixture(self, root: Path, logo_width: int = 284, time_size: int = 58, wrong_font: bool = False,
                 missing_text: str | None = None, text_offset_x: int = 0, cadence_y: int = 688, tempo_y: int = 719):
        from PIL import Image, ImageDraw, ImageFont

        series = root / "SERIES" / "07-00"
        input_dir = series / "input"
        output_dir = series / "output"
        brand_dir = root / "brand"
        input_dir.mkdir(parents=True)
        output_dir.mkdir()
        brand_dir.mkdir()
        logo_source = Path(__file__).resolve().parents[1] / "brand" / "logo_wavvy.png"
        (brand_dir / "logo_wavvy.png").write_bytes(logo_source.read_bytes())
        (series / "concept.md").write_text(
            "# 07:00\n\n## Packaging Contract\n\n- Playlist repeat: 2\n- Thumbnail layout: input/thumbnail-layout.json\n",
            encoding="utf-8",
        )
        (output_dir / "report.json").write_text(json.dumps({"processing_params": {"repeat": 1}}), encoding="utf-8")
        scene = Image.new("RGB", (1672, 941), (40, 50, 80))
        scene.save(input_dir / "scene.png")
        thumb = scene.copy()
        with Image.open(brand_dir / "logo_wavvy.png") as raw_logo:
            logo = raw_logo.convert("RGBA")
        logo = logo.resize((logo_width, round(logo.height * logo_width / logo.width)), Image.Resampling.LANCZOS)
        thumb.paste(logo, (65, 56), logo)
        font = ImageFont.load_default(size=time_size) if wrong_font else ImageFont.truetype("Pacifico-Regular.ttf", time_size)
        ImageDraw.Draw(thumb).text((343, 78), "07:00", font=font, fill="white")
        if missing_text != "cadence":
            ImageDraw.Draw(thumb).text((64 + text_offset_x, cadence_y), "Cadence", font=ImageFont.truetype("SF-Pro-Display-Thin.otf", 50), fill="white")
        if missing_text != "tempo":
            ImageDraw.Draw(thumb).text((59 + text_offset_x, tempo_y), "180 BPM", font=ImageFont.truetype("HelveticaNeue.ttc", 148, index=9), fill="white")
        thumb.save(input_dir / "thumb.jpg", quality=95)
        (input_dir / "loop.png").write_bytes(b"loop")
        layout = {
            "schema": "wavvy.thumbnail_layout.v1",
            "scene": "input/scene.png",
            "thumbnail": "input/thumb.jpg",
            "reference_psds": ["SERIES/06-00/input/thumb.psd", "SERIES/11-00/input/thumb.psd"],
            "logo": {"asset": "brand/logo_wavvy.png", "x": 65, "y": 56, "source_width": logo_width},
            "time": {"text": "07:00", "font": "Pacifico-Regular", "font_size": time_size, "x": 343, "y": 78},
            "cadence": {"text": "Cadence", "font": "SF-Pro-Display-Thin", "font_size": 50, "x": 64 + text_offset_x, "y": cadence_y},
            "tempo": {"text": "180 BPM", "font": "HelveticaNeue-CondensedBlack", "font_size": 148, "x": 59 + text_offset_x, "y": tempo_y},
        }
        (input_dir / "thumbnail-layout.json").write_text(json.dumps(layout), encoding="utf-8")
        return series

    def test_pack_rejects_repeat_one_before_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self._fixture(Path(tmp))
            result = CliRunner().invoke(cli, ["pack", str(series), "--repeat", "1", "-y"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("requires --repeat 2", result.output)
            self.assertFalse((series / "output" / "final.mkv").exists())

    def test_report_repeat_one_fails_gate_and_two_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = self._fixture(root)
            result = run_gate(series, root, "source-final", {"is_valid": True})
            self.assertEqual(next(item for item in result["checks"] if item["name"] == "playlist_repeat_contract")["status"], "FAIL")
            self.assertTrue(any("playlist repeat" in item for item in result["blockers"]))
            (series / "output" / "report.json").write_text(json.dumps({"processing_params": {"repeat": 2}}), encoding="utf-8")
            result = run_gate(series, root, "source-final", {"is_valid": True})
            self.assertEqual(next(item for item in result["checks"] if item["name"] == "playlist_repeat_contract")["status"], "PASS")

    def test_thumbnail_real_logo_and_pacifico_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = self._fixture(root)
            contract, parse_errors = packaging_contract(series)
            self.assertEqual(parse_errors, [])
            checks, errors = check_thumbnail_layout(series, root, contract["layout_path"])
            self.assertEqual(errors, [])
            self.assertTrue(all(item["status"] == "PASS" for item in checks))

    def test_thumbnail_small_logo_large_time_or_wrong_font_fails(self):
        for case in ("small_logo", "large_time", "wrong_font"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                series = self._fixture(
                    root,
                    logo_width=200 if case == "small_logo" else 284,
                    time_size=85 if case == "large_time" else 58,
                    wrong_font=case == "wrong_font",
                )
                contract, _ = packaging_contract(series)
                checks, errors = check_thumbnail_layout(series, root, contract["layout_path"])
                self.assertTrue(errors)
                expected_name = "thumbnail_time_pixels" if case == "wrong_font" else "thumbnail_reference_proportions"
                self.assertEqual(next(item for item in checks if item["name"] == expected_name)["status"], "FAIL")

    def test_bad_thumbnail_blocks_pack_and_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = self._fixture(root, logo_width=200)
            packed = CliRunner().invoke(cli, ["pack", str(series), "--repeat", "2", "-y"])
            self.assertNotEqual(packed.exit_code, 0)
            self.assertIn("proportions differ", packed.output)
            self.assertFalse((series / "output" / "final.mkv").exists())
            gated = run_gate(series, root, "source-final", {"is_valid": True})
            self.assertEqual(gated["result"], "FAIL")
            self.assertEqual(next(item for item in gated["checks"] if item["name"] == "thumbnail_reference_proportions")["status"], "FAIL")

    def test_missing_cadence_or_tempo_blocks_pack_and_gate(self):
        for missing in ("cadence", "tempo"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                series = self._fixture(root, missing_text=missing)
                contract, _ = packaging_contract(series)
                checks, errors = check_thumbnail_layout(series, root, contract["layout_path"])
                self.assertTrue(errors)
                self.assertEqual(next(item for item in checks if item["name"] == f"thumbnail_{missing}_pixels")["status"], "FAIL")
                packed = CliRunner().invoke(cli, ["pack", str(series), "--repeat", "2", "-y"])
                self.assertNotEqual(packed.exit_code, 0)
                self.assertIn(f"thumbnail {missing}", packed.output)
                gated = run_gate(series, root, "source-final", {"is_valid": True})
                self.assertEqual(gated["result"], "FAIL")

    def test_headline_moved_right_or_cadence_below_tempo_fails_independent_layout(self):
        for case, params in (
            ("moved_right", {"text_offset_x": 886}),
            ("cadence_below", {"cadence_y": 830, "tempo_y": 630}),
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                series = self._fixture(root, **params)
                contract, _ = packaging_contract(series)
                checks, errors = check_thumbnail_layout(series, root, contract["layout_path"])
                self.assertTrue(errors)
                self.assertEqual(next(item for item in checks if item["name"] == "thumbnail_lower_left_layout")["status"], "FAIL")
                self.assertEqual(next(item for item in checks if item["name"] == "thumbnail_cadence_pixels")["status"], "PASS")
                self.assertEqual(next(item for item in checks if item["name"] == "thumbnail_tempo_pixels")["status"], "PASS")
                packed = CliRunner().invoke(cli, ["pack", str(series), "--repeat", "2", "-y"])
                self.assertNotEqual(packed.exit_code, 0)
                self.assertIn("lower left", packed.output)
                gated = run_gate(series, root, "source-final", {"is_valid": True})
                self.assertTrue(any("lower left" in blocker for blocker in gated["blockers"]))


def make_lyric_skill_package(root: Path) -> None:
    skill_dir = root / "skills" / "wavvy-lyricist"
    references_dir = skill_dir / "references"
    spec_dir = root / "MASTER" / "lyrics" / "skills"
    references_dir.mkdir(parents=True)
    spec_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: wavvy-lyricist
description: Test fixture
---

# Wavvy Lyricist

References `MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md` and
`skills/wavvy-lyricist/references/patterns.md`.

Modes: `full-lyric-draft`, `suno-prompt-only`, `review-only`.

For drafts:
1. `Source Map`
2. `Constraint Freeze`
3. `Lyric Strategy`
4. `Draft`
5. `Self-Gate`

For review-only:
1. `Source Map`
2. `Constraint Freeze`
3. `Findings`
4. `Verdict`
""",
        encoding="utf-8",
    )
    (references_dir / "patterns.md").write_text(
        "This reference does not store copied, translated, or closely paraphrased external lyric lines.\n",
        encoding="utf-8",
    )
    (spec_dir / "WAVVY_LYRIC_SKILL_SPEC.md").write_text(
        "# Wavvy Lyric Skill Spec\n\n## Self-Gate Contract\n\n## Harness Acceptance Baseline\n",
        encoding="utf-8",
    )


def write_full_lyric_artifact(path: Path, draft: str, self_gate_extra: str = "", constraint_extra: str = "", bpm: int = 104) -> None:
    body = draft.strip()
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    quote = next((line.strip() for line in body.splitlines() if line.strip() and not line.startswith("[")), "")
    if "draft_scope: full-song" in constraint_extra:
        verse_counts = []
        sung_lines = []
        in_verse = False
        for raw_line in body.splitlines():
            line = raw_line.strip()
            tag = re.fullmatch(r"\[([^\]]+)\](?:[ \t]+\[[^\]]+\])*", line)
            if tag:
                in_verse = bool(re.fullmatch(r"Verse(?:\s+\d+)?", tag.group(1), re.IGNORECASE))
                if in_verse:
                    verse_counts.append(0)
            elif line:
                sung_lines.append(line)
                if in_verse:
                    verse_counts[-1] += 1
        if len(verse_counts) != 3 and "verse_structure_exception" not in constraint_extra:
            constraint_extra += "\n- verse_structure_exception: test song uses a different Verse layout"
        distribution = "; ".join(f"{i}={count}" for i, count in enumerate(verse_counts, 1)) or "none"
        longest = max(sung_lines, key=len, default="")
        self_gate_extra += (
            f'\n- Verse Distribution: PASS | {distribution} | recorded sung rows by verse'
            f'\n- Longest Sung Line: PASS | "{longest}" | checked the densest row aloud'
            f'\n- Short Phrasing: PASS | "{quote}" | this phrase has a natural ending'
            f'\n- Breathing Room: PASS | "{quote}" | the voice rests after this phrase while instruments continue'
        )
    path.write_text(
        f"""Source Map
- `MASTER/SSOT.md`
- `SERIES/17-00/concept.md`

Constraint Freeze
- series: 17-00
- track: 01
- mode: full-lyric-draft
- genre_lane: Pop/R&B
- bpm: {bpm}
- key: unknown
- mood: bright
- vocal_identity: single lead, chest-dominant
- language_policy: Korean
- time_activity_policy: topic is optional
- explicit_overrides: none
- copyright_boundary: no copied, translated, closely paraphrased material
{constraint_extra}

Lyric Strategy
- narrator: first person
- connection: spoken thought
- emotional_movement: may remain still
- hook_or_repetition_role: optional
- density: medium
- suno_handling: full lyric draft, not prompt-only

Draft
{draft}

Self-Gate
- Review Source: Draft
- Source SHA256: {body_hash}
- Expression: PASS | "{quote}" | the speaker can say this directly
- Connection: PASS | "{quote}" | this line connects to the surrounding thought
- Emotional Flow: PASS | "{quote}" | this line carries the current feeling
- Copyright Safety: PASS | original draft
- Wavvy Identity: PASS | Korean single lead
- Series DNA: PASS | fits the target series
- Suno Format: PASS | full lyric draft mode
{self_gate_extra}
""",
        encoding="utf-8",
    )


def write_track_prompt_source(path: Path, style: str, exclude: str = "choir, doubled vocals", bpm: str = "106", key: str = "G Major", vocal: str = "warm male lead", lyrics: str = "[Verse]\n오늘은 웃었어") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"Track: 너와\nBPM: {bpm}\nKey: {key}\nVocal: {vocal}\n\n"
        f"=== STYLE ===\n{style}\n\n=== EXCLUDE ===\n{exclude}\n\n=== LYRICS ===\n{lyrics}\n",
        encoding="utf-8",
    )


def write_review_artifact(path: Path, source: Path, body: str, verdict: str = "PASS | reviewed lines are ready", findings_extra: str = "") -> None:
    body_hash = hashlib.sha256(body.strip().encode("utf-8")).hexdigest()
    quote = next(line.strip() for line in body.splitlines() if line.strip() and not line.startswith("["))
    path.write_text(
        f"""Source Map
- `{source.name}`

Constraint Freeze
- mode: review-only

Findings
- Review Source: {source.name}
- Source SHA256: {body_hash}
- Expression: PASS | "{quote}" | this is a readable utterance
- Connection: PASS | "{quote}" | this follows the speaker's thought
- Emotional Flow: PASS | "{quote}" | this sustains the mood
- Copyright Safety: PASS | source is original
- Wavvy Identity: PASS | Korean solo vocal
- Series DNA: PASS | the track direction fits
- Suno Format: PASS | reviewing lyric body only
{findings_extra}
Verdict
{verdict}
""",
        encoding="utf-8",
    )


class HarnessTests(unittest.TestCase):
    def test_track_filename_accepts_unknown_bpm_without_inventing_a_number(self):
        track = TrackInfo.from_filename(Path("09__한 곡만 더__Buoyant__Indie Rock__NA.wav"))
        self.assertIsNotNone(track)
        self.assertIsNone(track.bpm)

    def test_repeat_timestamp_includes_crossfade_at_pass_boundary(self):
        report = {"processing_params": {"repeat": 2, "fade": 0.8}}
        tracks = [
            {"order": 1, "duration": 10.0},
            {"order": 2, "duration": 20.0},
        ]
        first, repeated = compute_track_timestamps(report, tracks)
        self.assertEqual(first, {1: "00:00", 2: "00:09"})
        self.assertEqual(repeated, {1: "00:28", 2: "00:38"})

    def test_generate_report_crossfade_reduction_uses_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.json"
            tracks = [
                TrackInfo(Path("01__One__A__Genre__100.wav"), 1, "One", "A", "Genre", 100, duration=10.0),
                TrackInfo(Path("02__Two__B__Genre__110.wav"), 2, "Two", "B", "Genre", 110, duration=20.0),
            ]
            self.assertTrue(generate_report(tracks, output, final_duration=58.4, params={"repeat": 2}))
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertAlmostEqual(report["summary"]["crossfade_reduction"], 1.6)

    def test_build_state_infers_source_final_for_minimal_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root)
            make_lyric_skill_package(root)
            state = build_state(series, root)
            self.assertEqual(state["phase"], "source_final")
            self.assertEqual(state["artifact_status"]["final_track_sources_count"], 2)
            self.assertEqual(state["artifact_status"]["report_tracks"], 2)
            self.assertIn("MASTER/SSOT.md", state["authoritative_docs"])
            self.assertIn("MASTER/ai/RUNTIME_RULES.md", state["authoritative_docs"])
            self.assertIn("MASTER/cli/SPEC.md", state["authoritative_docs"])
            self.assertEqual(state["artifact_status"]["lyric_skill_package"], "present")
            self.assertIn("skills/wavvy-lyricist/SKILL.md", state["evidence_refs"])

    def test_state_switch_infers_target_phase_action_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            uploaded = make_series(root, CONCEPT_UPLOADED)
            draft = make_draft_series(root)
            previous = build_state(uploaded, root)
            previous["revision"] = 3
            previous["next_action"] = "Review the 20-00 upload manually."

            switched = build_state(draft, root, previous_state=previous)
            self.assertEqual(switched["active_series"], "SERIES/17-00")
            self.assertEqual(switched["phase"], "track_source_draft")
            self.assertEqual(switched["inferred_phase"], "track_source_draft")
            self.assertEqual(switched["next_action"], "Review existing track source drafts and follow the next source work in concept.md.")
            self.assertEqual(switched["revision"], 3)
            self.assertEqual(switched["artifact_status"]["txt_sources"], 1)
            self.assertEqual(switched["artifact_status"]["youtube_upload"], "missing")
            self.assertIn("SERIES/17-00/concept.md", switched["authoritative_docs"])
            self.assertNotIn("SERIES/20-00/concept.md", switched["evidence_refs"])
            self.assertEqual(switched["blocked_by"], [])

            checked = check_state(draft, root, previous)
            self.assertEqual(checked["state"]["phase"], "track_source_draft")
            self.assertIn("state active_series differs from requested series", checked["warnings"])
            self.assertEqual(checked["blockers"], [])

    def test_state_resume_preserves_same_series_manual_phase_and_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root)
            previous = build_state(series, root)
            previous["phase"] = "track_source_draft"
            previous["next_action"] = "Compare the two chorus options manually."

            resumed = build_state(series, root, previous_state=previous)
            self.assertEqual(resumed["phase"], "track_source_draft")
            self.assertEqual(resumed["inferred_phase"], "source_final")
            self.assertEqual(resumed["next_action"], "Compare the two chorus options manually.")

            (series / "concept.md").write_text(CONCEPT_UPLOADED, encoding="utf-8")
            previous_uploaded = build_state(series, root)
            previous_uploaded["next_action"] = "Review the published upload manually."
            resumed_uploaded = build_state(series, root, previous_state=previous_uploaded)
            self.assertEqual(resumed_uploaded["phase"], "uploaded")
            self.assertEqual(resumed_uploaded["next_action"], "Review the published upload manually.")

    def test_state_phase_change_updates_stale_next_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root)
            previous = build_state(series, root)
            previous["phase"] = "track_source_draft"
            previous["next_action"] = "Review existing track source drafts and follow the next source work in concept.md."

            advanced = build_state(series, root, phase="render_final", previous_state=previous)
            self.assertEqual(advanced["phase"], "render_final")
            self.assertEqual(advanced["next_action"], "Create final.mkv and upload.csv for the render-final stage.")

    def test_state_cli_explicit_phase_and_if_match_on_series_switch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            uploaded = make_series(root, CONCEPT_UPLOADED)
            draft = make_draft_series(root)
            state_path = root / ".ai" / "state.json"
            state_path.parent.mkdir(parents=True)
            previous = build_state(uploaded, root)
            previous["revision"] = 3
            state_path.write_text(json.dumps(previous), encoding="utf-8")

            runner = CliRunner()
            with patch("wavvy._resolve_repo_root", return_value=root):
                written = runner.invoke(cli, ["state", str(draft), "--write", "--phase", "concept_draft", "--if-match", "3", "--json"])
                self.assertEqual(written.exit_code, 0, written.output)
                saved = json.loads(state_path.read_text(encoding="utf-8"))
                self.assertEqual(saved["revision"], 4)
                self.assertEqual(saved["active_series"], "SERIES/17-00")
                self.assertEqual(saved["phase"], "concept_draft")
                self.assertEqual(saved["inferred_phase"], "track_source_draft")
                self.assertEqual(saved["next_action"], "Draft track sources from concept.md.")

                before_rejected_write = state_path.read_bytes()
                rejected = runner.invoke(cli, ["state", str(draft), "--write", "--if-match", "3", "--json"])
                self.assertEqual(rejected.exit_code, 1, rejected.output)
                self.assertIn("state revision mismatch", rejected.output)
                self.assertEqual(state_path.read_bytes(), before_rejected_write)

    def test_lyrics_skill_package_gate_passes_static_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)

            result = run_lyrics_skill_gate(root)

            self.assertEqual(result["result"], "PASS", result)
            checks = {check["name"]: check for check in result["checks"]}
            self.assertEqual(checks["skill_front_matter_name"]["status"], "PASS")
            self.assertEqual(checks["spec_defines_self_gate_contract"]["status"], "PASS")
            self.assertIn("MASTER/lyrics/skills/WAVVY_LYRIC_SKILL_SPEC.md", result["evidence_refs"])
            self.assertEqual(result["scope"], "PACKAGE_ONLY")
            self.assertEqual(result["quality_status"], "NOT_REVIEWED")

    def test_lyrics_skill_artifact_accepts_direct_feeling_time_topic_and_no_image_quota(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Genre: Pop/R&B\nMood: bright\n", encoding="utf-8")
            artifact = root / "artifact.md"
            write_full_lyric_artifact(
                artifact,
                "[Verse]\n퇴근하니까 마음이 아파\n오늘은 조금 쉬고 싶어\n그래도 너랑 얘기할래\n",
            )

            result = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft")

            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(result["quality_status"], "REVIEW_RECORD_CHECKED_SCOPE_UNSPECIFIED")
            self.assertNotIn("object_space_phenomenon_images_minimum", {check["name"] for check in result["checks"]})

    def test_lyrics_skill_artifact_rejects_mode_mismatch_and_stale_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            artifact = root / "draft.md"
            write_full_lyric_artifact(artifact, "[Verse]\n오늘은 조금 쉬고 싶어")

            mismatch = run_lyrics_skill_gate(root, artifact_path=artifact, mode="review-only")
            self.assertEqual(mismatch["result"], "FAIL")
            self.assertIn("constraint_freeze_mode_exactly_once", {check["name"] for check in mismatch["checks"] if check["status"] == "FAIL"})

            artifact.write_text(artifact.read_text(encoding="utf-8").replace("오늘은 조금 쉬고 싶어", "오늘은 조금 더 쉬고 싶어", 1), encoding="utf-8")
            stale = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft")
            self.assertEqual(stale["result"], "FAIL")
            self.assertIn("actual_sha256=", next(check["detail"] for check in stale["checks"] if check["name"] == "reviewed_source_sha256_matches"))

    def test_lyrics_skill_artifact_rejects_blank_quote_and_tag_only_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            artifact = root / "draft.md"
            write_full_lyric_artifact(artifact, "[Verse]\n오늘은 조금 쉬고 싶어")
            artifact.write_text(artifact.read_text(encoding="utf-8").replace('"오늘은 조금 쉬고 싶어"', '"   "'), encoding="utf-8")
            blank_quote = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft")
            self.assertEqual(blank_quote["result"], "FAIL")
            self.assertIn("review_expression_evidence", {check["name"] for check in blank_quote["checks"] if check["status"] == "FAIL"})

            write_full_lyric_artifact(artifact, "[Verse][Chorus]\n[Bridge] [Outro]")
            tag_only = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft")
            self.assertEqual(tag_only["result"], "FAIL")
            self.assertIn("reviewed_lyric_body_present", {check["name"] for check in tag_only["checks"] if check["status"] == "FAIL"})

    def test_lyrics_skill_artifact_gate_rejects_korean_rows_in_suno_prompt_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Genre: Pop/R&B\n", encoding="utf-8")
            artifact = root / "suno.md"
            artifact.write_text(
                """Source Map
- `SERIES/17-00/concept.md`

Constraint Freeze
- mode: suno-prompt-only
- genre_lane: Pop/R&B

Lyric Strategy
- hook_anchor: 다시 올라가

Draft
창가에 빛이 내려와

Self-Gate
- Copyright Safety: PASS | original prompt
- Wavvy Identity: PASS | prompt only
- Series DNA: PASS | Pop/R&B lane
- Suno Format: PASS | prompt-only
""",
                encoding="utf-8",
            )

            result = run_lyrics_skill_gate(root, series, artifact, "suno-prompt-only")

            self.assertEqual(result["result"], "FAIL")
            checks = {check["name"]: check for check in result["checks"]}
            self.assertEqual(checks["suno_prompt_only_has_no_korean_lyric_rows"]["status"], "FAIL")

    def test_lyrics_skill_prompt_only_preserves_intentional_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            artifact = root / "empty.md"
            artifact.write_text("""Source Map
- `SERIES/17-00/concept.md`

Constraint Freeze
- mode: suno-prompt-only
- suno_input: Empty

Lyric Strategy
- density: free Suno generation

Draft

Self-Gate
- Copyright Safety: PASS | no copied lyric input
- Wavvy Identity: PASS | Korean direction comes from the series
- Series DNA: PASS | style prompt carries the series direction
- Suno Format: PASS | Empty input selected
""", encoding="utf-8")
            result = run_lyrics_skill_gate(root, artifact_path=artifact)
            self.assertEqual(result["result"], "PASS", result)
            self.assertEqual(result["mode"], "suno-prompt-only")
            self.assertEqual(result["quality_status"], "PROMPT_INPUT_CHECKED")
            artifact.write_text(artifact.read_text(encoding="utf-8").replace("Draft\n\nSelf-Gate", "Draft\nKorean lyrics about a quiet room\n\nSelf-Gate"), encoding="utf-8")
            self.assertEqual(run_lyrics_skill_gate(root, artifact_path=artifact)["result"], "FAIL")

    def test_lyrics_skill_review_only_binds_to_draft_body_not_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            source = root / "source.md"
            body = "[Verse]\n오늘은 조금 쉬고 싶어\n내일 네 얘기도 들어볼게"
            source.write_text(f"Source Map\n- metadata before\n\nDraft\n{body}\n\nSelf-Gate\n- metadata after\n", encoding="utf-8")
            review = root / "review.md"
            write_review_artifact(review, source, body)

            accepted = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(accepted["result"], "PASS", accepted)
            self.assertEqual(accepted["reviewed_source_sha256"], hashlib.sha256(body.encode("utf-8")).hexdigest())
            self.assertNotIn("review_self_gate", {check["name"] for check in accepted["checks"]})

            source.write_text(source.read_text(encoding="utf-8").replace("metadata before", "changed metadata"), encoding="utf-8")
            self.assertEqual(run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")["result"], "PASS")
            source.write_text(source.read_text(encoding="utf-8").replace("조금 쉬고 싶어", "더 쉬고 싶어"), encoding="utf-8")
            self.assertEqual(run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")["result"], "FAIL")

    def test_lyrics_skill_review_only_rejects_missing_empty_duplicate_and_conflicting_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            source = root / "source.md"
            body = "[Verse]\n오늘은 조금 쉬고 싶어"
            source.write_text(body, encoding="utf-8")
            review = root / "review.md"

            write_review_artifact(review, source, body)
            source.unlink()
            missing = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(missing["result"], "FAIL")
            source.write_text("[Verse][Chorus]", encoding="utf-8")
            empty = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(empty["result"], "FAIL")

            source.write_text(body, encoding="utf-8")
            write_review_artifact(review, source, body, findings_extra='- Expression: HOLD | "오늘은 조금 쉬고 싶어" | revise wording')
            duplicate = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(duplicate["result"], "FAIL")

            write_review_artifact(review, source, body, verdict="PASS | ready")
            review.write_text(review.read_text(encoding="utf-8").replace('Expression: PASS |', 'Expression: HOLD |'), encoding="utf-8")
            conflict = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(conflict["result"], "FAIL")
            self.assertTrue(any("conflicts" in blocker for blocker in conflict["blockers"]))

            write_review_artifact(review, source, body, verdict="HOLD | revise this line")
            held = run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")
            self.assertEqual(held["result"], "USER_DECISION")
            write_review_artifact(review, source, body, verdict="FAIL | line is broken")
            self.assertEqual(run_lyrics_skill_gate(root, artifact_path=review, mode="review-only")["result"], "FAIL")

    def test_lyrics_skill_cli_review_stage_skips_media_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Genre: Pop/R&B\n", encoding="utf-8")
            runner = CliRunner()
            source = root / "source.md"
            body = "[Verse]\n오늘은 조금 쉬고 싶어"
            source.write_text(body, encoding="utf-8")
            review = root / "review.md"
            write_review_artifact(review, source, body)

            with patch("wavvy.git_repo_root", return_value=root), patch(
                "wavvy.validate_project",
                side_effect=AssertionError("lyrics-review must not run media validation"),
            ):
                missing = runner.invoke(cli, ["gate", str(series), "--stage", "lyrics-review", "--json"])
                result = runner.invoke(cli, ["gate", str(series), "--stage", "lyrics-review", "--artifact", str(review), "--mode", "review-only", "--json"])

            self.assertEqual(missing.exit_code, 1, missing.output)
            self.assertEqual(json.loads(missing.output)["quality_status"], "NOT_REVIEWED")
            self.assertEqual(result.exit_code, 0, result.output)
            payload = json.loads(result.output)
            self.assertEqual(payload["schema"], "wavvy.lyrics_skill_gate.v1")
            self.assertEqual(payload["result"], "PASS")
            self.assertEqual(payload["mode"], "review-only")

    def test_full_song_lyric_gate_checks_plan_and_bound_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            source.parent.mkdir(parents=True)
            draft = "[Intro]\n[Verse 1]\n오늘 너와 웃었어\n[Chorus]\n괜찮다고 말했어\n[Verse 2]\n또 얘기했어\n[Chorus]\n괜찮다고 말했어\n[Bridge]\n조금 더 걸었어\n[Final Chorus]\n너와 웃었어\n[Outro]"
            source.write_text(f"Track: 너와\nBPM: 106 (proposed)\n\n=== STYLE ===\nAcoustic neo-soul\n\n=== EXCLUDE ===\n\n=== LYRICS ===\n{draft}\n", encoding="utf-8")
            artifact = root / "draft.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse 1=16; Chorus=8; Verse 2=16; Chorus=8; Bridge=8; Final Chorus=24; Outro=8\n- track_source: SERIES/17-00/input/tracks/03_너와.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)

            runner = CliRunner()
            with patch("wavvy.git_repo_root", return_value=root), patch("wavvy.validate_project", side_effect=AssertionError("lyric review must not run media validation")):
                command = [str(series), "--artifact", str(artifact), "--mode", "full-lyric-draft", "--draft-scope", "full-song", "--json"]
                skill = runner.invoke(cli, ["lyrics-skill", *command])
                gate = runner.invoke(cli, ["gate", str(series), "--stage", "lyrics-review", *command[1:]])

            self.assertEqual(skill.exit_code, 0, skill.output)
            self.assertEqual(gate.exit_code, 0, gate.output)
            payload = json.loads(gate.output)
            self.assertEqual(payload["draft_scope"], "full-song")
            self.assertTrue(payload["full_song_ready"])
            self.assertGreaterEqual(payload["planned_duration_estimate_seconds"], 200)
            self.assertIn("not measured audio", str(payload["checks"]))

            source.write_text(source.read_text(encoding="utf-8").replace("BPM: 106", "BPM: 125"), encoding="utf-8")
            mismatch = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(mismatch["result"], "FAIL")
            self.assertEqual({c["name"]: c["status"] for c in mismatch["checks"]}["full_song_bpm_matches_track_source"], "FAIL")

    def test_new_full_song_breath_evidence_checks_current_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "06_새노래.txt"
            draft = "[Intro]\n[Verse 1]\n오늘은 잠깐 걷자\n천천히 얘기해\n[Chorus]\n바람을 따라가\n[Verse 2]\n길이 조금 길어도\n너랑 있으면 좋아\n[Instrumental]\n[Verse 3]\n한 번 더 쉬었다가\n집으로 돌아가자\n[Outro]"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male lead.", lyrics=draft)
            artifact = root / "new-full-song.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse 1=16; Chorus=12; Verse 2=16; Instrumental=12; Verse 3=16; Outro=16\n- track_source: SERIES/17-00/input/tracks/06_새노래.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            valid = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(valid["result"], "PASS", valid)
            original = artifact.read_text(encoding="utf-8")

            cases = (
                ("- Verse Distribution: PASS | 1=2; 2=2; 3=2", "- Verse Distribution: PASS | 1=2; 2=9; 3=2", "full_song_verse_distribution_evidence"),
                ('- Longest Sung Line: PASS | "한 번 더 쉬었다가"', '- Longest Sung Line: PASS | "천천히 얘기해"', "full_song_longest_sung_line_evidence"),
                ('- Short Phrasing: PASS | "오늘은 잠깐 걷자"', '- Short Phrasing: PASS | "오늘은 잠깐 걷자 / 너랑 있으면 좋아"', "full_song_short_phrasing_evidence"),
                ('- Breathing Room: PASS | "오늘은 잠깐 걷자"', '- Breathing Room: PASS | "없는 가사"', "full_song_breathing_room_evidence"),
            )
            for current, changed, failed_check in cases:
                with self.subTest(failed_check=failed_check):
                    artifact.write_text(original.replace(current, changed), encoding="utf-8")
                    result = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
                    self.assertEqual(result["result"], "FAIL")
                    self.assertEqual({item["name"]: item["status"] for item in result["checks"]}[failed_check], "FAIL")

            artifact.write_text(original.replace("- Breathing Room: PASS", "- Breathing Room: HOLD"), encoding="utf-8")
            hold = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(hold["result"], "USER_DECISION")

    def test_full_song_section_cues_are_not_sung_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic duet\n", encoding="utf-8")
            source = series / "input" / "tracks" / "08_취향.txt"
            draft = "[Intro]\n[Verse 1] [Female]\n오늘은 함께 걷자\n[Chorus] [Male + Female]\n이 길이 좋아\n[Verse 2] [Male]\n너랑 다시 걷자\n[Instrumental] [fingerpicked guitar]\n[Verse 3] [Female]\n잠깐 쉬어 가자\n[Outro]"
            write_track_prompt_source(source, "Acoustic duet, 100 BPM, G Major. Female and male leads.", bpm="100", lyrics=draft)
            artifact = root / "tagged-full-song.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse 1=16; Chorus=16; Verse 2=16; Instrumental=16; Verse 3=16; Outro=4\n- track_source: SERIES/17-00/input/tracks/08_취향.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=100)
            result = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(result["result"], "PASS", result)
            checks = {item["name"]: item["status"] for item in result["checks"]}
            self.assertEqual(checks["full_song_verse_count"], "PASS")
            self.assertEqual(checks["full_song_section_bars_match_draft"], "PASS")

    def test_new_full_song_verse_exception_including_no_verse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "06_새노래.txt"
            draft = "[Intro]\n[Chorus]\n오늘은 천천히 걷자\n이 길에서 쉬어 가자\n[Instrumental]\n[Outro]"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male lead.", lyrics=draft)
            artifact = root / "new-full-song.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Chorus=64; Instrumental=16; Outro=8\n- track_source: SERIES/17-00/input/tracks/06_새노래.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            excepted = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(excepted["result"], "PASS", excepted)
            self.assertIn("none", str(next(check for check in excepted["checks"] if check["name"] == "full_song_verse_distribution_evidence")))
            artifact.write_text(artifact.read_text(encoding="utf-8").replace("- verse_structure_exception: test song uses a different Verse layout\n", ""), encoding="utf-8")
            unexcepted = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual({check["name"]: check["status"] for check in unexcepted["checks"]}["full_song_verse_count"], "FAIL")

    def test_legacy_full_song_exemption_binds_artifact_path_and_draft_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "05_원본.txt"
            draft = "[Intro]\n[Verse 1]\n오늘은 함께 걷자\n[Verse 2]\n조금만 더 걷자\n[Outro]"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male lead.", lyrics=draft)
            artifact = root / ".ai" / "lyrics" / "approved.md"
            artifact.parent.mkdir(parents=True)
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse 1=44; Verse 2=44; Outro=4\n- track_source: SERIES/17-00/input/tracks/05_원본.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            legacy_text = artifact.read_text(encoding="utf-8")
            legacy_text = legacy_text[:legacy_text.index("\n- Verse Distribution:")].rstrip() + "\n"
            legacy_text = legacy_text.replace("- verse_structure_exception: test song uses a different Verse layout\n", "")
            artifact.write_text(legacy_text, encoding="utf-8")
            manifest = root / "MASTER" / "lyrics" / "legacy-full-song-approvals.json"
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text(json.dumps([{"artifact": ".ai/lyrics/approved.md", "draft_sha256": hashlib.sha256(draft.encode("utf-8")).hexdigest()}]), encoding="utf-8")
            approved = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(approved["result"], "PASS", approved)

            revised = draft.replace("조금만 더 걷자", "이번엔 더 걸어가자")
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male lead.", lyrics=revised)
            write_full_lyric_artifact(artifact, revised, constraint_extra=fields, bpm=106)
            revised_text = artifact.read_text(encoding="utf-8")
            artifact.write_text(revised_text[:revised_text.index("\n- Verse Distribution:")].rstrip().replace("- verse_structure_exception: test song uses a different Verse layout\n", "") + "\n", encoding="utf-8")
            revision = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(revision["result"], "FAIL")
            self.assertEqual({check["name"]: check["status"] for check in revision["checks"]}["full_song_verse_count"], "FAIL")

    def test_full_song_scope_does_not_silently_pass_without_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            artifact = root / "draft.md"
            draft = "[Verse]\n오늘은 조금 쉬고 싶어"
            write_full_lyric_artifact(artifact, draft)
            legacy = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft")
            self.assertEqual(legacy["result"], "PASS")
            self.assertEqual(legacy["draft_scope"], "UNSPECIFIED")
            self.assertFalse(legacy["full_song_ready"])
            self.assertEqual(legacy["quality_status"], "REVIEW_RECORD_CHECKED_SCOPE_UNSPECIFIED")

            required = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft", draft_scope="full-song")
            self.assertEqual(required["result"], "FAIL")
            self.assertEqual({c["name"]: c["status"] for c in required["checks"]}["full_lyric_draft_scope"], "FAIL")

            write_full_lyric_artifact(artifact, draft, constraint_extra="- draft_scope: excerpt")
            excerpt = run_lyrics_skill_gate(root, artifact_path=artifact, mode="full-lyric-draft", draft_scope="excerpt")
            self.assertEqual(excerpt["result"], "PASS")
            self.assertFalse(excerpt["full_song_ready"])

    def test_full_song_gate_rejects_missing_intro_short_plan_and_source_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            source.parent.mkdir(parents=True)
            draft = "[Verse]\n오늘은 조금 쉬고 싶어\n[Outro]"
            source.write_text(f"BPM: 106\n=== STYLE ===\nA\n=== EXCLUDE ===\n\n=== LYRICS ===\n{draft}\n", encoding="utf-8")
            artifact = root / "draft.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Verse=16; Outro=4\n- track_source: SERIES/17-00/input/tracks/03_너와.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            failed = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            failures = {check["name"] for check in failed["checks"] if check["status"] == "FAIL"}
            self.assertIn("full_song_intro_outro_tags", failures)
            self.assertIn("full_song_planned_duration", failures)

            source.write_text(source.read_text(encoding="utf-8").replace("오늘은 조금 쉬고 싶어", "오늘은 조금 걷고 싶어"), encoding="utf-8")
            drift = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual({check["name"]: check["status"] for check in drift["checks"]}["full_song_track_source_matches_draft"], "FAIL")

            source.write_text(source.read_text(encoding="utf-8").replace("오늘은 조금 걷고 싶어", "오늘은 조금 쉬고 싶어"), encoding="utf-8")
            fields += "\n- intro_outro_exception: Intro | user requested a direct verse opening"
            fields = fields.replace("Verse=16; Outro=4", "Verse=88; Outro=4")
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            excepted = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
            self.assertEqual(excepted["result"], "PASS", excepted)

    def test_duplicate_track_source_sections_fail_both_prompt_and_lyric_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            draft = "[Intro]\n[Verse]\n오늘은 웃었어\n[Outro]"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male vocal: warm, direct.", lyrics=draft)
            original = source.read_text(encoding="utf-8")
            artifact = root / "draft.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse=88; Outro=4\n- track_source: SERIES/17-00/input/tracks/03_너와.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            runner = CliRunner()
            prompt_command = ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"]

            with patch("wavvy.git_repo_root", return_value=root):
                self.assertEqual(run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")["result"], "PASS")
                self.assertEqual(runner.invoke(cli, prompt_command).exit_code, 0)
                for duplicate in ("=== LYRICS ===\n[Verse]\n갑자기 다른 가사야\n", "=== STYLE ===\nA different style\n"):
                    with self.subTest(duplicate=duplicate.splitlines()[0]):
                        source.write_text(original + "\n" + duplicate, encoding="utf-8")
                        lyric_result = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
                        self.assertEqual(lyric_result["result"], "FAIL")
                        self.assertFalse(lyric_result["full_song_ready"])
                        self.assertIn("duplicate ===", str(lyric_result["blockers"]))
                        prompt_result = runner.invoke(cli, prompt_command)
                        self.assertEqual(prompt_result.exit_code, 1, prompt_result.output)
                        self.assertIn("duplicate ===", str(json.loads(prompt_result.output)["blockers"]))
                        with self.assertRaisesRegex(FinalizeUploadError, "duplicate ==="):
                            parse_track_source(str(source), source.read_text(encoding="utf-8"))

    def test_duplicate_track_source_bpm_header_fails_both_gates_and_archiving(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_lyric_skill_package(root)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            draft = "[Intro]\n[Verse]\n오늘은 웃었어\n[Outro]"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male vocal: warm, direct.", lyrics=draft)
            original = source.read_text(encoding="utf-8")
            artifact = root / "draft.md"
            fields = "- draft_scope: full-song\n- target_duration_seconds: 200\n- meter: 4/4\n- section_bars: Intro=4; Verse=88; Outro=4\n- track_source: SERIES/17-00/input/tracks/03_너와.txt"
            write_full_lyric_artifact(artifact, draft, constraint_extra=fields, bpm=106)
            runner = CliRunner()
            prompt_command = ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"]

            with patch("wavvy.git_repo_root", return_value=root):
                self.assertEqual(run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")["result"], "PASS")
                self.assertEqual(runner.invoke(cli, prompt_command).exit_code, 0)
                for duplicate in ("BPM: 125", "  bPm : 125"):
                    with self.subTest(duplicate=duplicate):
                        changed = original.replace("BPM: 106", f"BPM: 106\n{duplicate}", 1).replace("106 BPM", "125 BPM", 1)
                        source.write_text(changed, encoding="utf-8")
                        lyric_result = run_lyrics_skill_gate(root, series, artifact, "full-lyric-draft", "full-song")
                        self.assertEqual(lyric_result["result"], "FAIL")
                        self.assertFalse(lyric_result["full_song_ready"])
                        self.assertIn("duplicate", str(lyric_result["blockers"]))
                        prompt_result = runner.invoke(cli, prompt_command)
                        self.assertEqual(prompt_result.exit_code, 1, prompt_result.output)
                        self.assertIn("duplicate", str(json.loads(prompt_result.output)["blockers"]))
                        with self.assertRaisesRegex(FinalizeUploadError, "duplicate"):
                            parse_track_source(str(source), source.read_text(encoding="utf-8"))

    def test_track_prompt_gate_checks_actual_new_source_without_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul, up to 125 BPM\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            style = "Acoustic neo-soul, 106 BPM, G Major. One warm mid-low male lead sings in a conversational tone."
            write_track_prompt_source(source, style)
            runner = CliRunner()

            with patch("wavvy.git_repo_root", return_value=root), patch(
                "wavvy.validate_project",
                side_effect=AssertionError("track-prompt must not run media validation"),
            ):
                missing = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--json"])
                accepted = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])

            self.assertEqual(missing.exit_code, 1, missing.output)
            self.assertIn("--artifact", json.loads(missing.output)["blockers"][0])
            self.assertEqual(accepted.exit_code, 0, accepted.output)
            payload = json.loads(accepted.output)
            self.assertEqual(payload["scope"], "NEW_FULL_TRACK_PROMPT_CONTRACT")
            self.assertEqual(payload["quality_status"], "PROMPT_CONTRACT_CHECKED")
            self.assertEqual(payload["source_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_track_prompt_gate_enforces_unicode_style_budget_and_exclude_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            base = "Acoustic neo-soul, 106 BPM, G Major. Male vocal: warm, direct. "
            runner = CliRunner()

            with patch("wavvy.git_repo_root", return_value=root):
                write_track_prompt_source(source, base + "가" * (900 - len(base)), exclude="")
                exact = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                write_track_prompt_source(source, base + "가" * (901 - len(base)), exclude="")
                over = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                write_track_prompt_source(source, base, exclude=", ".join(f"item {i}" for i in range(12)))
                many = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])

            self.assertEqual(exact.exit_code, 0, exact.output)
            self.assertEqual(over.exit_code, 1, over.output)
            self.assertIn("901/900", str(json.loads(over.output)["checks"]))
            self.assertEqual(many.exit_code, 1, many.output)
            self.assertIn("12/8", str(json.loads(many.output)["checks"]))

    def test_track_prompt_gate_rejects_unknown_and_mismatched_proposals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            style = "Acoustic neo-soul, 106 BPM, G Major. Male vocal: warm, direct."
            runner = CliRunner()
            cases = [
                ({"bpm": "unknown"}, "bpm_metadata_matches_style"),
                ({"bpm": "108"}, "bpm_metadata_matches_style"),
                ({"key": "unknown"}, "key_metadata_matches_style"),
                ({"key": "A Minor"}, "key_metadata_matches_style"),
                ({"vocal": "gender unknown"}, "vocal_gender_metadata_matches_style"),
                ({"vocal": "warm female lead"}, "vocal_gender_metadata_matches_style"),
            ]
            with patch("wavvy.git_repo_root", return_value=root):
                for fields, failed_check in cases:
                    with self.subTest(fields=fields):
                        write_track_prompt_source(source, style, **fields)
                        result = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                        self.assertEqual(result.exit_code, 1, result.output)
                        checks = {check["name"]: check["status"] for check in json.loads(result.output)["checks"]}
                        self.assertEqual(checks[failed_check], "FAIL")

    def test_track_prompt_gate_matches_all_explicit_vocal_genders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "08_너와.txt"
            cases = [
                ("warm male lead", "Male vocal", "PASS"),
                ("warm female lead", "Female vocal", "PASS"),
                ("female verses, male and female choruses", "Male and female vocals", "PASS"),
                ("여성 벌스, 남성 여성 후렴", "여성과 남성 보컬", "PASS"),
                ("female and male vocals", "Female vocal", "FAIL"),
                ("female vocal", "Female and male vocals", "FAIL"),
                ("female and male; gender unknown", "Female and male vocals", "FAIL"),
            ]
            with patch("wavvy.git_repo_root", return_value=root):
                for vocal, style_vocal, expected in cases:
                    with self.subTest(vocal=vocal, style_vocal=style_vocal):
                        style = f"Acoustic neo-soul, 106 BPM, G Major. {style_vocal}."
                        write_track_prompt_source(source, style, vocal=vocal)
                        result = CliRunner().invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                        payload = json.loads(result.output)
                        checks = {check["name"]: check["status"] for check in payload["checks"]}
                        self.assertEqual(payload["result"], expected, result.output)
                        self.assertEqual(checks["vocal_gender_metadata_matches_style"], expected)
                        self.assertEqual(result.exit_code, 0 if expected == "PASS" else 1)

    def test_track_prompt_gate_instrumental_remake_requires_instrumental_only_lyrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "07-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("180 BPM instrumental running music\n", encoding="utf-8")
            source = series / "input" / "remakes" / "02_파란불.txt"
            style = "Instrumental indie electronic breakbeat, 180 BPM in D Major. Fast drums and bright guitar."
            runner = CliRunner()
            with patch("wavvy.git_repo_root", return_value=root):
                write_track_prompt_source(source, style, bpm="180", key="D Major", vocal="Instrumental", lyrics="[Instrumental]")
                accepted = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                write_track_prompt_source(source, style, bpm="180", key="D Major", vocal="Instrumental", lyrics="[Instrumental]\nSing this")
                sung = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
                write_track_prompt_source(source, style + " Male lead.", bpm="180", key="D Major", vocal="Instrumental", lyrics="[Instrumental]")
                gendered = runner.invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
            self.assertEqual(accepted.exit_code, 0, accepted.output)
            self.assertEqual(sung.exit_code, 1, sung.output)
            self.assertEqual(gendered.exit_code, 1, gendered.output)
            self.assertIn("instrumental_lyrics_only", str(json.loads(sung.output)["checks"]))
            self.assertIn("vocal_gender_metadata_matches_style", str(json.loads(gendered.output)["checks"]))

    def test_track_prompt_gate_rejects_prior_track03_failure_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = series / "input" / "tracks" / "03_너와.txt"
            base = "Korean acoustic neo-soul, 106 BPM, conversational single lead. "
            style = base + "가" * (949 - len(base))
            write_track_prompt_source(source, style, exclude=", ".join(f"item {i}" for i in range(12)), key="unknown", vocal="single lead; gender unknown")
            with patch("wavvy.git_repo_root", return_value=root):
                result = CliRunner().invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
            self.assertEqual(result.exit_code, 1, result.output)
            checks = {check["name"]: check["status"] for check in json.loads(result.output)["checks"]}
            for name in ("style_character_limit", "exclude_budget", "key_metadata_matches_style", "vocal_gender_metadata_matches_style"):
                self.assertEqual(checks[name], "FAIL", name)

    def test_track_prompt_gate_rejects_source_from_another_series(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "17-00"
            series.mkdir(parents=True)
            (series / "concept.md").write_text("Acoustic neo-soul\n", encoding="utf-8")
            source = root / "SERIES" / "18-00" / "input" / "tracks" / "03_너와.txt"
            write_track_prompt_source(source, "Acoustic neo-soul, 106 BPM, G Major. Male vocal: warm, direct.")
            with patch("wavvy.git_repo_root", return_value=root):
                result = CliRunner().invoke(cli, ["gate", str(series), "--stage", "track-prompt", "--artifact", str(source), "--json"])
            self.assertEqual(result.exit_code, 1, result.output)
            self.assertEqual(json.loads(result.output)["checks"][0]["status"], "FAIL")

    def test_compilation_source_map_counts_as_available_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "RNB-BEST"
            (series / "input").mkdir(parents=True)
            (series / "input" / "thumb.jpg").write_bytes(b"thumb")
            (series / "concept.md").write_text(CONCEPT_COMPILATION, encoding="utf-8")
            source_one = root / "SERIES/01/input/tracks/09__One__Warm__RnB__90.wav"
            source_two = root / "SERIES/02/work/norm_tracks/norm_03__Two__Cool__Soul__100.wav"
            source_one.parent.mkdir(parents=True)
            source_two.parent.mkdir(parents=True)
            source_one.write_bytes(b"one")
            source_two.write_bytes(b"two")

            state = build_state(series, root)
            self.assertEqual(state["phase"], "source_final")
            self.assertEqual(state["artifact_status"]["audio_files"], 0)
            self.assertEqual(state["artifact_status"]["available_audio_files"], 2)
            self.assertEqual(state["artifact_status"]["audio_source"], "concept_track_selection")

            result = check_state(series, root, {"phase": "source_final"})
            self.assertEqual(result["result"], "PASS")

    def test_validate_project_uses_compilation_source_map_when_tracks_dir_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = root / "SERIES" / "RNB-BEST"
            (series / "input").mkdir(parents=True)
            (series / "input" / "thumb.jpg").write_bytes(b"thumb")
            (series / "concept.md").write_text(CONCEPT_COMPILATION, encoding="utf-8")
            source_one = root / "SERIES/01/input/tracks/09__One__Warm__RnB__90.wav"
            source_two = root / "SERIES/02/work/norm_tracks/norm_03__Two__Cool__Soul__100.wav"
            source_one.parent.mkdir(parents=True)
            source_two.parent.mkdir(parents=True)
            source_one.write_bytes(b"one")
            source_two.write_bytes(b"two")

            with patch("wavvy.git_repo_root", return_value=root), patch(
                "wavvy.get_audio_info",
                return_value={"duration": 120.0, "sample_rate": 48000},
            ), patch("wavvy.compute_sha256", return_value="abc123"):
                result = validate_project(ProjectPaths(series))

            self.assertTrue(result.is_valid, result.errors)
            self.assertEqual(len(result.tracks), 2)
            self.assertEqual(result.tracks[0].path, source_one)
            self.assertEqual(result.tracks[0].report_filename, "01__One__Warm__RnB__90.wav")

    def test_check_state_warns_on_final_sources_with_stale_draft_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root, CONCEPT_FINAL + "\n## 미해결 / 다음 라운드\n\n- DRAFT Suno 생성/검수\n")
            result = check_state(series, root, {"phase": "source_final"})
            self.assertEqual(result["result"], "PASS")
            self.assertIn(
                "concept.md contains Final Track Sources but still has draft/Suno stale status text",
                result["warnings"],
            )

    def test_uploaded_phase_allows_deleted_local_render_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root, CONCEPT_UPLOADED)
            result = check_state(series, root, {"phase": "uploaded"})
            self.assertEqual(result["result"], "PASS")
            state = result["state"]
            self.assertEqual(state["phase"], "uploaded")
            self.assertEqual(state["artifact_status"]["youtube_upload"], "completed")
            self.assertEqual(state["artifact_status"]["final_mkv"], "deleted_after_upload")
            self.assertEqual(state["artifact_status"]["upload_csv"], "deleted_after_upload")

    def test_bare_uploaded_text_does_not_mark_upload_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept = CONCEPT_FINAL + "\n## Series Status\n\n- 현재 phase: `uploaded`\n- v0.8 — uploaded 20/20\n"
            series = make_series(root, concept)
            state = build_state(series, root)
            self.assertEqual(state["artifact_status"]["youtube_upload"], "missing")
            self.assertNotEqual(state["phase"], "uploaded")

    def test_not_uploaded_text_does_not_mark_upload_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept = CONCEPT_FINAL + "\n## Upload Status\n\n- YouTube upload: not uploaded yet\n"
            series = make_series(root, concept)
            state = build_state(series, root)
            self.assertEqual(state["artifact_status"]["youtube_upload"], "missing")

    def test_reference_video_url_does_not_mark_upload_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept = "# New Series\n\n## Reference videos\n\n- https://youtu.be/A3psJJwkdSY\n"
            series = make_series(root, concept)
            state = build_state(series, root)
            self.assertEqual(state["artifact_status"]["youtube_upload"], "missing")
            self.assertNotEqual(state["phase"], "uploaded")

    def test_legacy_published_youtube_marker_marks_upload_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            concept = CONCEPT_FINAL + "\n> **YouTube**: https://youtu.be/i1GHmn1WZr4\n"
            series = make_series(root, concept)
            state = build_state(series, root)
            self.assertEqual(state["artifact_status"]["youtube_upload"], "completed")

    def test_upload_ready_gate_passes_when_upload_already_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root, CONCEPT_UPLOADED)
            result = run_gate(series, root, "upload-ready", {"is_valid": True, "errors": [], "warnings": []})
            self.assertEqual(result["result"], "PASS")
            checks = {check["name"]: check for check in result["checks"]}
            self.assertEqual(checks["youtube_upload_status"]["status"], "PASS")
            self.assertEqual(checks["youtube_upload_status"]["detail"], "completed")
            self.assertNotIn("youtube_upload_completed", checks)

    def test_upload_ready_gate_passes_before_upload_without_failed_upload_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = make_series(root)
            output = series / "output"
            (output / "final.mkv").write_bytes(b"placeholder")
            (output / "upload.csv").write_text("video_path,title\nx,y\n", encoding="utf-8")
            (output / "youtube_subtitles_ko_no_timing.txt").write_text("lyrics\n", encoding="utf-8")

            with patch("wavvy_harness.gate._has_media_stream", return_value=True):
                result = run_gate(series, root, "upload-ready", {"is_valid": True, "errors": [], "warnings": []})

            self.assertEqual(result["result"], "PASS")
            checks = {check["name"]: check for check in result["checks"]}
            self.assertEqual(checks["youtube_upload_status"]["status"], "PASS")
            self.assertEqual(checks["youtube_upload_status"]["detail"], "pending")
            self.assertNotIn("youtube_upload_completed", checks)

    def test_ssot_hygiene_scopes_stale_terms_to_entrypoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in [
                "MASTER/SSOT.md",
                "MASTER/ai/RUNTIME_RULES.md",
                "MASTER/MANAGER.md",
                "MASTER/WORKFLOWS.md",
                "MASTER/cli/SPEC.md",
                "MASTER/youtube/YOUTUBE.md",
            ]:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "MASTER/SSOT.md\nMASTER/ai/RUNTIME_RULES.md\nMASTER/MANAGER.md\n"
                    "MASTER/WORKFLOWS.md\nMASTER/cli/SPEC.md\n",
                    encoding="utf-8",
                )
            (root / "AGENTS.md").write_text(
                "MASTER/SSOT.md\nMASTER/ai/RUNTIME_RULES.md\nMASTER/MANAGER.md\nMASTER/WORKFLOWS.md\nMASTER/cli/SPEC.md\n",
                encoding="utf-8",
            )
            (root / "CLAUDE.md").write_text(
                "MASTER/SSOT.md\nMASTER/ai/RUNTIME_RULES.md\nMASTER/MANAGER.md\nMASTER/WORKFLOWS.md\nMASTER/cli/SPEC.md\n",
                encoding="utf-8",
            )
            (root / "wavvy.md").write_text("Wavvy\n", encoding="utf-8")
            (root / ".ai").mkdir()
            (root / ".ai" / "state.json").write_text(
                json.dumps(
                    {
                        "authoritative_docs": [
                            "MASTER/SSOT.md",
                            "MASTER/ai/RUNTIME_RULES.md",
                            "MASTER/cli/SPEC.md",
                        ]
                    }
                ),
                encoding="utf-8",
            )
            archive = root / ".ai" / "peer-review" / "runs" / "old.md"
            archive.parent.mkdir(parents=True)
            archive.write_text("VIBEM final.mp4 Video Crossfade 필수\n", encoding="utf-8")

            checks = run_ssot_hygiene(root)
            required = [check for check in checks if check.get("required")]
            self.assertTrue(required)
            self.assertTrue(all(check["status"] == "pass" for check in required), checks)


class ReleaseVerificationTests(unittest.TestCase):
    def make_reordered_release(self, root: Path) -> Path:
        series = make_series(root)
        tracks_dir = series / "input" / "tracks"
        source_texts = {
            1: "Track: Old One\nOrder: 1\n\n=== STYLE ===\nold-style-one\n\n=== EXCLUDE ===\nold-exclude-one\n\n=== LYRICS ===\n[Intro] [Instrumental]\n\n[Verse]\n나\n",
            2: "Track: Old Two\nOrder: 2\n\n=== STYLE ===\nsubmitted-style-two\n\n=== EXCLUDE ===\nsubmitted-exclude-two\n\n=== LYRICS ===\n[Verse]\n너\n",
        }
        sources = {}
        for original, content in source_texts.items():
            source_path = tracks_dir / f"{original:02d}_old.txt"
            source_path.write_text(content, encoding="utf-8")
            sources[original] = parse_track_source(str(source_path), content)
        report_path = series / "output" / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        manifest = {"workspace": "[test]", "tracks": []}
        slots = []
        candidates = []
        for playback, original, title in ((1, 2, "Renamed Two"), (2, 1, "Renamed One")):
            candidate_id = f"candidate-{original}"
            track = report["tracks"][playback - 1]
            track["title"] = title
            audio = tracks_dir / track["filename"]
            audio.write_bytes(f"audio-{playback}".encode())
            digest = hashlib.sha256(audio.read_bytes()).hexdigest()
            track.update({"sha256": digest, "duration": 60.0})
            manifest["tracks"].append({"order": playback, "approved_title": title,
                                        "input_filename": track["filename"], "candidate_id": candidate_id,
                                        "sha256": digest, "duration_seconds": 60.0})
            slot = {"playback_order": playback, "source_order": original, "title": title,
                    "source_txt": f"input/tracks/{original:02d}_old.txt",
                    "source_sha256": sources[original].sha256,
                    "current_observed_candidates": [{"id": candidate_id}],
                    "candidate_selection_status": "user_selected_for_20_song_sequence"}
            if original == 1:
                slot["lyrics_evidence_ref"] = "input/validation/current-lyrics.json"
            slots.append(slot)
            candidates.append({"order": original, "title": title,
                               "candidates": [{"id": candidate_id}],
                               "decision": {"status": "user_selected_for_20_song_sequence",
                                            "chosen_candidate_id": candidate_id}})
        report_path.write_text(json.dumps(report), encoding="utf-8")
        (series / "input" / "download-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (series / "input" / "playback-order.json").write_text(
            json.dumps({"workspace": "[test]", "slots": slots}), encoding="utf-8")
        (series / "input" / "suno-candidates.json").write_text(
            json.dumps({"workspace": "[test]", "tracks": candidates}), encoding="utf-8")
        evidence_dir = series / "input" / "validation"
        evidence_dir.mkdir()
        (evidence_dir / "current-lyrics.json").write_text(json.dumps({
            "url": "https://suno.com/song/candidate-1",
            "lyrics": "[Intro]\n[Instrumental]\n\n[Verse]\n나",
        }), encoding="utf-8")
        (evidence_dir / "generation-manifest.json").write_text(json.dumps({
            "candidate_ids": ["candidate-2"], "source_sha256": sources[2].sha256,
            "inputs": {"lyrics": sources[2].lyrics, "style": sources[2].style,
                       "exclude_styles": sources[2].exclude},
        }), encoding="utf-8")
        return series

    def test_reordered_sources_bind_by_id_and_original_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_reordered_release(Path(tmp))
            paths = ProjectPaths(series)
            report = json.loads((series / "output" / "report.json").read_text())
            bindings = resolve_playback_source_bindings(
                paths, report["tracks"], read_filesystem_track_sources(paths))
            self.assertEqual([bindings[i].source_order for i in (1, 2)], [2, 1])
            self.assertEqual([bindings[i].prompt_status for i in (1, 2)], ["confirmed", "unverified"])
            self.assertEqual(bindings[2].lyrics_match_status, "bracket_label_line_break_only")
            section, _ = build_final_track_sources_section(
                report, report["tracks"], {i: b.source for i, b in bindings.items()}, "filesystem", bindings)
            self.assertIn("### 01. Renamed Two", section)
            self.assertIn("### 02. Renamed One", section)
            self.assertIn("submitted-style-two", section)
            self.assertNotIn("old-style-one", section)
            self.assertIn("[Intro]\n[Instrumental]", section)

    def test_reordered_sources_reject_wrong_id_hash_and_missing_lyrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_reordered_release(Path(tmp))
            paths = ProjectPaths(series)
            report = json.loads((series / "output" / "report.json").read_text())
            def resolve():
                return resolve_playback_source_bindings(
                    paths, report["tracks"], read_filesystem_track_sources(paths))
            candidate_path = series / "input" / "suno-candidates.json"
            candidates = json.loads(candidate_path.read_text())
            candidates["tracks"][1]["decision"]["chosen_candidate_id"] = "wrong-id"
            candidate_path.write_text(json.dumps(candidates))
            with self.assertRaisesRegex(FinalizeUploadError, "selected ID differs"):
                resolve()
            candidates["tracks"][1]["decision"]["chosen_candidate_id"] = "candidate-1"
            candidate_path.write_text(json.dumps(candidates))
            manifest_path = series / "input" / "download-manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["tracks"][0]["sha256"] = "bad-hash"
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(FinalizeUploadError, "WAV hash"):
                resolve()
            manifest["tracks"][0]["sha256"] = report["tracks"][0]["sha256"]
            manifest_path.write_text(json.dumps(manifest))
            evidence_path = series / "input" / "validation" / "current-lyrics.json"
            evidence = json.loads(evidence_path.read_text())
            evidence["lyrics"] = "different words"
            evidence_path.write_text(json.dumps(evidence))
            with self.assertRaisesRegex(FinalizeUploadError, "lyrics differ"):
                resolve()

            evidence["lyrics"] = "[Intro]\n[Instrumental]\n\n[Verse]\n나"
            evidence_path.write_text(json.dumps(evidence))
            order_path = series / "input" / "playback-order.json"
            order_data = json.loads(order_path.read_text())
            order_data["slots"][0]["source_sha256"] = "bad-source-hash"
            order_path.write_text(json.dumps(order_data))
            with self.assertRaisesRegex(FinalizeUploadError, "source order/SHA"):
                resolve()
            order_data["slots"][0]["source_sha256"] = read_filesystem_track_sources(paths)[1].sha256
            order_path.write_text(json.dumps(order_data))
            generation_path = series / "input" / "validation" / "generation-manifest.json"
            generation = json.loads(generation_path.read_text())
            generation["inputs"]["style"] = "different generation style"
            generation_path.write_text(json.dumps(generation))
            with self.assertRaisesRegex(FinalizeUploadError, "generation input mismatch"):
                resolve()

    def test_reordered_sources_reject_unproven_generation_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_reordered_release(Path(tmp))
            paths = ProjectPaths(series)
            candidate_path = series / "input" / "suno-candidates.json"
            candidates = json.loads(candidate_path.read_text())
            candidates["tracks"][1]["candidates"][0]["source_sha256_at_generation"] = "unverified-claim"
            candidate_path.write_text(json.dumps(candidates))
            report = json.loads((series / "output" / "report.json").read_text())
            with self.assertRaisesRegex(FinalizeUploadError, "no matching manifest"):
                resolve_playback_source_bindings(
                    paths, report["tracks"], read_filesystem_track_sources(paths))

    def test_reordered_release_verifies_archive_without_claiming_old_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_reordered_release(Path(tmp))
            paths = ProjectPaths(series)
            report = json.loads((series / "output" / "report.json").read_text())
            tracks = report["tracks"]
            bindings = resolve_playback_source_bindings(paths, tracks, read_filesystem_track_sources(paths))
            section, _ = build_final_track_sources_section(
                report, tracks, {i: b.source for i, b in bindings.items()}, "filesystem", bindings)
            first, _ = compute_track_timestamps(report, tracks)
            description = f"{first[1]} - 1. Renamed Two\n{first[2]} - 2. Renamed One"
            concept_path = series / "concept.md"
            concept = CONCEPT_FINAL.replace("description\n```", description + "\n```")
            concept_path.write_text(replace_final_track_sources_section(concept, section), encoding="utf-8")
            with (series / "output" / "upload.csv").open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=["video_path", "title", "description", "tags", "thumbnail_path", "visibility"])
                writer.writeheader()
                writer.writerow({"video_path": "final.mkv", "title": "Playlist | Test | Study | Wavvy | 20:00",
                                 "description": description, "tags": "tag1,tag2", "thumbnail_path": "thumb.jpg",
                                 "visibility": "private"})
            self.assertEqual(verify_release_package(paths), [])
            saved = concept_path.read_text(encoding="utf-8")
            concept_path.write_text(saved.replace("- Selected Candidate ID: `candidate-1`", "- Selected Candidate ID: `wrong`"))
            self.assertTrue(any("archived selected source" in error for error in verify_release_package(paths)))
            concept_path.write_text(saved.replace("Unverified for selected recording; see historical source separately", "old-style-one", 1))
            self.assertTrue(any("historical STYLE" in error for error in verify_release_package(paths)))

    def make_release(self, root: Path) -> Path:
        series = make_series(root)
        report_path = series / "output" / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["processing_params"] = {"fade": 0.8, "repeat": 2}
        manifest = {"workspace": "[20:00]", "tracks": []}
        candidate_tracks = []
        for track in report["tracks"]:
            order = track["order"]
            audio = series / "input" / "tracks" / track["filename"]
            source = series / "input" / "tracks" / f"{order:02d}_source.txt"
            source.write_text(f"source-{order}", encoding="utf-8")
            audio.write_bytes(f"audio-{order}".encode())
            digest = hashlib.sha256(audio.read_bytes()).hexdigest()
            track.update({"duration": 60.0, "sha256": digest})
            manifest["tracks"].append({
                "order": order, "approved_title": track["title"], "input_filename": track["filename"],
                "duration_seconds": 60.0, "sha256": digest, "candidate_id": f"candidate-{order}",
            })
            candidate_tracks.append({
                "order": order, "title": track["title"], "source_txt": f"input/tracks/{source.name}",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "candidates": [{"id": f"candidate-{order}"}],
                "decision": {"status": "keep", "chosen_candidate_id": f"candidate-{order}"},
            })
        report_path.write_text(json.dumps(report), encoding="utf-8")
        (series / "input" / "download-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (series / "input" / "suno-candidates.json").write_text(
            json.dumps({"workspace": "[20:00]", "tracks": candidate_tracks}), encoding="utf-8"
        )
        description = "Track List\n00:00 - 01. One\n00:59 - 02. Two\nRepeat\n01:58 - 01. One\n02:58 - 02. Two"
        concept = CONCEPT_FINAL.replace("description\n```", description + "\n```")
        (series / "concept.md").write_text(concept, encoding="utf-8")
        (series / "output" / "upload.csv").write_text(
            'video_path,title,description,tags,thumbnail_path,visibility\n'
            'final.mkv,Playlist | Test | Study | Wavvy | 20:00,"' + description.replace("\n", "\n") + '","tag1,tag2",thumb.jpg,private\n',
            encoding="utf-8",
        )
        return series

    def test_subtitles_strip_structure_but_keep_sung_lines(self):
        concept = CONCEPT_FINAL.replace("- Filename:", "- Source Checksum: `test`\n- Filename:")
        concept = concept.replace("lyrics\n```", "[Intro] [Instrumental]\n[Verse 1] [Female]\n사랑해\n[Chorus] [Strong high chest-mix belt]\n[Chorus] 같이 웃어\n오늘도 [Breath] 좋아\n[Instrumental] [Rhodes reply]\n(instrumental)\n```", 1)
        tracks = [{"order": 1, "title": "One", "filename": "01__One__A__Genre__100.wav"},
                  {"order": 2, "title": "Two", "filename": "02__Two__B__Genre__110.wav"}]
        self.assertEqual(build_untimed_subtitles(concept, tracks), "사랑해\n같이 웃어\n오늘도 좋아\n\nlyrics\n")
        self.assertEqual(build_untimed_subtitles(concept, tracks, repeat=2), "사랑해\n같이 웃어\n오늘도 좋아\n\nlyrics\n\n사랑해\n같이 웃어\n오늘도 좋아\n\nlyrics\n")
        with tempfile.TemporaryDirectory() as tmp:
            series = make_series(Path(tmp), concept)
            report_path = series / "output" / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["processing_params"] = {"repeat": 2}
            report_path.write_text(json.dumps(report), encoding="utf-8")
            result = CliRunner().invoke(cli, ["prepare-subtitles", str(series)])
            self.assertEqual(result.exit_code, 0, result.output)
            destination = series / "output" / "youtube_subtitles_ko_no_timing.txt"
            self.assertEqual(destination.read_text(encoding="utf-8"), "사랑해\n같이 웃어\n오늘도 좋아\n\nlyrics\n\n사랑해\n같이 웃어\n오늘도 좋아\n\nlyrics\n")
            destination.write_text("human edit\n", encoding="utf-8")
            result = CliRunner().invoke(cli, ["prepare-subtitles", str(series)])
            self.assertNotEqual(result.exit_code, 0)
            self.assertEqual(destination.read_text(encoding="utf-8"), "human edit\n")

    def test_current_selected_song_13_lyrics_do_not_leak_directions(self):
        evidence = Path(__file__).resolve().parents[1] / "SERIES/17-30/input/validation/2026-10-22-publish-selected-20/02-current-lyrics.json"
        current_lyrics = json.loads(evidence.read_text(encoding="utf-8"))["lyrics"]
        concept = CONCEPT_FINAL.replace("- Filename:", "- Source Checksum: `test`\n- Filename:")
        concept = concept.replace("lyrics\n```", current_lyrics + "\n```", 1)
        tracks = [{"order": 1, "title": "One", "filename": "01__One__A__Genre__100.wav"},
                  {"order": 2, "title": "Two", "filename": "02__Two__B__Genre__110.wav"}]
        subtitles = build_untimed_subtitles(concept, tracks)
        self.assertIn("버스 옆자리에 앉아", subtitles)
        self.assertIn("이 노래 끝날 때까지", subtitles)
        self.assertNotIn("[Intro]", subtitles)
        self.assertNotIn("[Strong high chest-mix belt]", subtitles)
        self.assertNotIn("[Rhodes reply]", subtitles)

    def test_verify_release_checks_identity_and_chapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            self.assertEqual(verify_release_package(ProjectPaths(series)), [])
            manifest_path = series / "input" / "download-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["tracks"][0]["candidate_id"] = "wrong-candidate"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("selected Suno candidate" in error for error in verify_release_package(ProjectPaths(series))))
            manifest["tracks"][0]["candidate_id"] = "candidate-1"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            candidate_path = series / "input" / "suno-candidates.json"
            candidate_path.unlink()
            self.assertTrue(any("Missing suno-candidates.json" in error for error in verify_release_package(ProjectPaths(series))))
            candidate_path.write_text(json.dumps({"workspace": "[20:00]", "tracks": [
                {"order": i, "title": title, "source_txt": f"input/tracks/{i:02d}_source.txt",
                 "source_sha256": hashlib.sha256(f"source-{i}".encode()).hexdigest(),
                 "candidates": [{"id": f"candidate-{i}"}],
                 "decision": {"status": "keep", "chosen_candidate_id": f"candidate-{i}"}}
                for i, title in ((1, "One"), (2, "Two"))
            ]}), encoding="utf-8")
            (series / "input" / "tracks" / manifest["tracks"][0]["input_filename"]).write_bytes(b"wrong-audio")
            self.assertTrue(any("WAV SHA-256" in error for error in verify_release_package(ProjectPaths(series))))

    def test_verify_release_accepts_one_digit_chapter_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            for path in (series / "concept.md", series / "output" / "upload.csv"):
                text = path.read_text(encoding="utf-8")
                path.write_text(text.replace("01. One", "1. One").replace("02. Two", "2. Two"), encoding="utf-8")
            self.assertEqual(verify_release_package(ProjectPaths(series)), [])

    def test_verify_release_prefers_current_final_selection_over_historical_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            manifest_path = series / "input" / "download-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            selection = {"workspace": "[20:00]", "tracks": []}
            for item in manifest["tracks"]:
                item["candidate_id"] = f"new-{item['order']}"
                selection["tracks"].append({
                    "order": item["order"], "title": item["approved_title"],
                    "candidate_id": item["candidate_id"],
                })
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            selection_path = series / "input" / "suno-final-selection-2026-10-12.json"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            self.assertEqual(verify_release_package(ProjectPaths(series)), [])

            selection["tracks"][0]["candidate_id"] = "wrong-id"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            self.assertTrue(any("final Suno selection ID/title" in error for error in verify_release_package(ProjectPaths(series))))
            selection["tracks"][0]["candidate_id"] = "new-1"
            selection["tracks"][0]["title"] = "Wrong Title"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            self.assertTrue(any("final Suno selection ID/title" in error for error in verify_release_package(ProjectPaths(series))))
            selection["tracks"][0]["title"] = "One"
            selection["workspace"] = "[wrong]"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            self.assertTrue(any("selection workspace" in error for error in verify_release_package(ProjectPaths(series))))

    def test_verify_release_invalid_final_selection_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            selection_path = series / "input" / "suno-final-selection-2026-10-12.json"
            selection_path.write_text("{invalid", encoding="utf-8")
            self.assertTrue(any("Invalid suno-final-selection" in error for error in verify_release_package(ProjectPaths(series))))
            selection_path.write_text(json.dumps({
                "workspace": "[20:00]",
                "tracks": [{"order": 1, "title": "One", "candidate_id": "candidate-1"}],
            }), encoding="utf-8")
            self.assertTrue(any("orders/count" in error for error in verify_release_package(ProjectPaths(series))))

    def test_verify_release_rejects_chapter_drift_and_csv_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            concept_path = series / "concept.md"
            concept_path.write_text(concept_path.read_text(encoding="utf-8").replace("00:59 - 02. Two", "01:00 - 02. Two"), encoding="utf-8")
            errors = verify_release_package(ProjectPaths(series))
            self.assertTrue(any("chapter 2" in error for error in errors))
            self.assertTrue(any("description differs" in error for error in errors))

    def test_verify_release_checks_existing_upload_copy_path_streams_and_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_release(Path(tmp))
            concept = series / "concept.md"
            concept.write_text(concept.read_text(encoding="utf-8") +
                               "\n## Packaging Contract\n\n- Playlist repeat: 2\n- Thumbnail layout: input/thumbnail-layout.json\n", encoding="utf-8")
            (series / "output" / "final.mp4").write_bytes(b"upload-copy")
            report_path = series / "output" / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["summary"] = {"final_duration": 238.4}
            report_path.write_text(json.dumps(report), encoding="utf-8")
            csv_path = series / "output" / "upload.csv"
            csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mkv", str(series / "output" / "final.mp4")), encoding="utf-8")
            good_probe = {"streams": [
                {"codec_type": "video", "codec_name": "h264", "width": 3840, "height": 2160},
                {"codec_type": "audio", "codec_name": "aac"}], "format": {"duration": "238.4"}}
            with patch("wavvy.ffmpeg.probe", return_value=good_probe):
                self.assertEqual(verify_release_package(ProjectPaths(series)), [])
                csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mp4", "final.mkv"), encoding="utf-8")
                self.assertTrue(any("video_path" in error for error in verify_release_package(ProjectPaths(series))))
            csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mkv", "final.mp4"), encoding="utf-8")
            with patch("wavvy.ffmpeg.probe", return_value={"streams": [{"codec_type": "video"}], "format": {"duration": "250"}}):
                errors = verify_release_package(ProjectPaths(series))
            self.assertTrue(any("requires video and audio streams" in error for error in errors))
            self.assertTrue(any("duration differs" in error for error in errors))

    def test_missing_or_low_quality_4k_upload_copy_fails_release_and_upload_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = self.make_release(root)
            concept = series / "concept.md"
            concept.write_text(concept.read_text(encoding="utf-8") +
                               "\n## Packaging Contract\n\n- Playlist repeat: 2\n- Thumbnail layout: input/thumbnail-layout.json\n", encoding="utf-8")
            report_path = series / "output" / "report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["summary"] = {"final_duration": 238.4}
            report_path.write_text(json.dumps(report), encoding="utf-8")
            csv_path = series / "output" / "upload.csv"
            csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mkv", str(series / "output" / "final.mp4")), encoding="utf-8")
            errors = verify_release_package(ProjectPaths(series))
            self.assertTrue(any("upload file is missing" in error for error in errors), errors)
            gate = run_gate(series, root, "upload-ready", {"is_valid": True})
            self.assertTrue(any("upload file is missing" in error for error in gate["blockers"]))

            csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mp4", "final.mkv"), encoding="utf-8")
            errors = verify_release_package(ProjectPaths(series))
            self.assertTrue(any("video_path must identify output/final.mp4" in error for error in errors), errors)
            self.assertTrue(any("upload file is missing" in error for error in errors), errors)
            gate = run_gate(series, root, "upload-ready", {"is_valid": True})
            self.assertTrue(any("video_path must identify output/final.mp4" in error for error in gate["blockers"]))
            self.assertTrue(any("upload file is missing" in error for error in gate["blockers"]))
            csv_path.write_text(csv_path.read_text(encoding="utf-8").replace("final.mkv", "final.mp4"), encoding="utf-8")

            (series / "output" / "final.mp4").write_bytes(b"fake-small-video")
            tiny_probe = {"streams": [
                {"codec_type": "video", "codec_name": "mpeg4", "width": 160, "height": 90},
                {"codec_type": "audio", "codec_name": "mp3"}],
                "format": {"duration": "238.4"}}
            with patch("wavvy_harness.upload_copy.ffmpeg.probe", return_value=tiny_probe):
                errors = verify_release_package(ProjectPaths(series))
                gate = run_gate(series, root, "upload-ready", {"is_valid": True})
            self.assertTrue(any("3840x2160 H.264" in error for error in errors), errors)
            self.assertTrue(any("3840x2160 H.264" in error for error in gate["blockers"]), gate["blockers"])


class SelectedAudioSourceTests(unittest.TestCase):
    def make_instrumental(self, root: Path) -> Path:
        series = ReleaseVerificationTests().make_release(root)
        concept = (series / "concept.md").read_text(encoding="utf-8")
        concept = concept.replace("## Final Track Sources", "## Series Direction\n\n- **Final vocal direction**: Instrumental.\n\n## Final Selected Audio Sources\n\n- Manifest: `input/final-selected-audio-sources.json`\n\n## Final Track Sources")
        (series / "concept.md").write_text(concept, encoding="utf-8")
        report = json.loads((series / "output" / "report.json").read_text(encoding="utf-8"))
        download = json.loads((series / "input" / "download-manifest.json").read_text(encoding="utf-8"))
        selection = {"workspace": "[20:00]", "tracks": [
            {"order": t["order"], "title": t["approved_title"], "candidate_id": t["candidate_id"]}
            for t in download["tracks"]
        ]}
        (series / "input" / "suno-final-selection-test.json").write_text(json.dumps(selection), encoding="utf-8")
        source_sha = hashlib.sha256(b"source-1").hexdigest()
        archive = {"schema": "wavvy.final_selected_audio.v1", "workspace": "[20:00]", "vocal_mode": "instrumental", "tracks": [
            {"order": 1, "title": "One", "candidate_id": "candidate-1", "wav_sha256": report["tracks"][0]["sha256"],
             "start_time": "00:00", "raw_prompt_status": "confirmed", "source_txt": "input/tracks/01_source.txt",
             "source_sha256": source_sha, "observed_style_description": None, "observation_ref": None},
            {"order": 2, "title": "Two", "candidate_id": "candidate-2", "wav_sha256": report["tracks"][1]["sha256"],
             "start_time": "00:59", "raw_prompt_status": "unverified", "observed_style_description": None, "observation_ref": None},
        ]}
        (series / "input" / "final-selected-audio-sources.json").write_text(json.dumps(archive), encoding="utf-8")
        return series

    def test_instrumental_archive_passes_source_and_upload_without_subtitles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            series = self.make_instrumental(root)
            self.assertEqual(check_selected_audio(series), (True, []))
            state = check_state(series, root, {"phase": "source_final"})
            self.assertEqual(state["result"], "PASS", state["blockers"])
            source_gate = run_gate(series, root, "source-final", {"is_valid": True})
            self.assertEqual(source_gate["result"], "PASS", source_gate["blockers"])
            (series / "output" / "final.mkv").write_bytes(b"video")
            with patch("wavvy_harness.gate._has_media_stream", return_value=True):
                upload_gate = run_gate(series, root, "upload-ready", {"is_valid": True})
            self.assertEqual(upload_gate["result"], "PASS", upload_gate["blockers"])
            self.assertFalse((series / "output" / "youtube_subtitles_ko_no_timing.txt").exists())

    def test_archive_rejects_false_identity_timing_and_prompt_claims(self):
        for field, value, message in (
            ("candidate_id", "wrong-id", "candidate ID"),
            ("wav_sha256", "0" * 64, "WAV SHA"),
            ("start_time", "01:00", "start_time"),
            ("source_sha256", "0" * 64, "candidate-to-source binding"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                series = self.make_instrumental(root)
                path = series / "input" / "final-selected-audio-sources.json"
                archive = json.loads(path.read_text(encoding="utf-8"))
                archive["tracks"][0][field] = value
                path.write_text(json.dumps(archive), encoding="utf-8")
                opted, errors = check_selected_audio(series)
                self.assertTrue(opted)
                self.assertTrue(any(message in error for error in errors), errors)
                self.assertEqual(run_gate(series, root, "source-final", {"is_valid": True})["result"], "FAIL")
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_instrumental(Path(tmp))
            path = series / "input" / "final-selected-audio-sources.json"
            archive = json.loads(path.read_text(encoding="utf-8"))
            archive["tracks"][1]["source_txt"] = "input/tracks/02_source.txt"
            path.write_text(json.dumps(archive), encoding="utf-8")
            self.assertTrue(any("unverified raw prompt" in error for error in check_selected_audio(series)[1]))

    def test_archive_requires_explicit_instrumental_and_observation_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_instrumental(Path(tmp))
            concept = series / "concept.md"
            concept.write_text(concept.read_text(encoding="utf-8").replace("Instrumental.", "Vocal."), encoding="utf-8")
            self.assertTrue(any("explicitly declare" in error for error in check_selected_audio(series)[1]))
            concept.write_text(concept.read_text(encoding="utf-8").replace("Vocal.", "Instrumental."), encoding="utf-8")
            path = series / "input" / "final-selected-audio-sources.json"
            archive = json.loads(path.read_text(encoding="utf-8"))
            archive["tracks"][1]["observed_style_description"] = "invented style"
            archive["tracks"][1]["observation_ref"] = "input/suno-candidates.json"
            path.write_text(json.dumps(archive), encoding="utf-8")
            self.assertTrue(any("not bound to candidate" in error for error in check_selected_audio(series)[1]))
            evidence = {"tracks": [
                {"candidate": {"id": "candidate-1", "style_description_ui": "style one"}},
                {"candidate": {"id": "candidate-2", "style_description_ui": "style two"}},
            ]}
            (series / "input" / "observed.json").write_text(json.dumps(evidence), encoding="utf-8")
            archive["tracks"][1]["observed_style_description"] = "style one"
            archive["tracks"][1]["observation_ref"] = "input/observed.json"
            path.write_text(json.dumps(archive), encoding="utf-8")
            self.assertTrue(any("not bound to candidate" in error for error in check_selected_audio(series)[1]))

    def test_finalize_upload_rejects_old_txt_for_new_selected_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            series = self.make_instrumental(Path(tmp))
            report = json.loads((series / "output" / "report.json").read_text(encoding="utf-8"))
            selection_path = series / "input" / "suno-final-selection-test.json"
            selection = json.loads(selection_path.read_text(encoding="utf-8"))
            selection["tracks"][1]["candidate_id"] = "later-cover-not-bound-to-original-txt"
            selection_path.write_text(json.dumps(selection), encoding="utf-8")
            matched = {i: TrackSource(label=str(i), content="", metadata={}, sections={}, sha256=hashlib.sha256(f"source-{i}".encode()).hexdigest()) for i in (1, 2)}
            with self.assertRaisesRegex(FinalizeUploadError, "no recorded source txt/hash"):
                verify_final_selection_source_provenance(ProjectPaths(series), report["tracks"], matched)


if __name__ == "__main__":
    unittest.main()
