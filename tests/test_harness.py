import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from wavvy import FinalizeUploadError, ProjectPaths, TrackInfo, cli, generate_report, parse_track_source, validate_project
from wavvy_harness.doctor import run_ssot_hygiene
from wavvy_harness.gate import run_gate, run_lyrics_skill_gate
from wavvy_harness.state import build_state, check_state


CONCEPT_FINAL = """# Test Series

## YouTube Metadata

### 제목
```text
Playlist | 20:00 | Test | Wavvy
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
            tag = re.fullmatch(r"\[([^\]]+)\]", line)
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


if __name__ == "__main__":
    unittest.main()
