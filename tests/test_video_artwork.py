import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from PIL import Image

from tests.artwork_fixture import make_artwork
from wavvy import ProjectPaths, cli, render_video_from_image
from wavvy_harness.gate import run_gate
from wavvy_harness.video_artwork import MANIFEST, check_video_artwork, file_sha256


class VideoArtworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.series = self.root / "SERIES/20-00"
        self.manifest = make_artwork(self.series)
        (self.series / "concept.md").write_text("# Test series\n", encoding="utf-8")
        self.image = self.series / "input/video-background.png"
        self.thumb = self.series / "input/thumb.jpg"

    def save(self):
        (self.series / MANIFEST).write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_valid_separate_4k_artwork_and_report_binding(self):
        data, errors = check_video_artwork(self.series, image_path=self.image)
        self.assertEqual(errors, [])
        self.assertEqual(data["image"], self.image)
        self.assertEqual(data["thumbnail"], self.thumb)
        self.assertEqual(check_video_artwork(self.series, report={"processing_params": {"video_artwork": data["binding"]}})[1], [])
        self.assertIn("current video artwork", check_video_artwork(self.series, report={})[1][0])

    def test_rejects_thumbnail_renamed_as_video_background(self):
        self.image.write_bytes(self.thumb.read_bytes())
        self.manifest["video_background"]["sha256"] = file_sha256(self.image)
        self.save()
        self.assertIn("renamed copy", check_video_artwork(self.series)[1][0])

    def test_rejects_identical_decoded_pixels_with_different_file_hashes(self):
        with Image.open(self.image) as image:
            # A lossless PNG carried under the thumbnail filename defeats
            # filename/extension/file-hash checks but not decoded-pixel checks.
            image.save(self.thumb, format="PNG", compress_level=0)
        self.manifest["thumbnail"]["sha256"] = file_sha256(self.thumb)
        self.save()
        self.assertNotEqual(file_sha256(self.image), file_sha256(self.thumb))
        self.assertIn("identical decoded pixels", check_video_artwork(self.series)[1][0])

    def test_rejects_non_4k_background(self):
        Image.new("RGB", (1920, 1080), "navy").save(self.image)
        self.manifest["video_background"]["sha256"] = file_sha256(self.image)
        self.save()
        self.assertIn("3840x2160", check_video_artwork(self.series)[1][0])

    def test_rejects_file_hash_role_path_and_origin_drift(self):
        original = copy.deepcopy(self.manifest)
        for field, value in (("sha256", "0" * 64), ("role", "youtube_thumbnail"),
                             ("path", "input/thumb.jpg"), ("path", "../escape.png"), ("origin", "thumbnail")):
            with self.subTest(field=field, value=value):
                self.manifest = copy.deepcopy(original)
                self.manifest["video_background"][field] = value
                self.save()
                self.assertTrue(check_video_artwork(self.series)[1])

    def test_rejects_missing_stale_or_failed_visual_review(self):
        path = self.series / self.manifest["visual_review"]["path"]
        original = json.loads(path.read_text())
        mutations = [lambda r: r["image"].update(sha256="0" * 64),
                     lambda r: r["observations"].update(wavvy_logo_present=False),
                     lambda r: r["observations"].update(title_text_present=True),
                     lambda r: r["observations"].update(bpm_text_present=True),
                     lambda r: r["observations"].pop("other_overlay_text_present"),
                     lambda r: r.update(evidence=""), lambda r: r.update(method="filename"),
                     lambda r: r.update(reviewed_at="2026-10-26")]
        for mutate in mutations:
            review = copy.deepcopy(original)
            mutate(review)
            path.write_text(json.dumps(review), encoding="utf-8")
            self.manifest["visual_review"]["sha256"] = file_sha256(path)
            self.save()
            self.assertTrue(check_video_artwork(self.series)[1])
        path.unlink()
        self.assertTrue(check_video_artwork(self.series)[1])

    def test_pack_preview_and_renderer_refuse_missing_contract_before_media_work(self):
        (self.series / MANIFEST).unlink()
        with patch("wavvy.get_audio_info") as audio_probe, patch("wavvy.subprocess.run") as process:
            for command in ("pack", "preview"):
                result = CliRunner().invoke(cli, [command, str(self.series)] + (["-y"] if command == "pack" else []))
                self.assertNotEqual(result.exit_code, 0)
                self.assertIn("Video artwork", result.output)
            self.assertFalse(render_video_from_image(self.series / "mix.wav", self.image, self.thumb, self.series / "output.mp4"))
            audio_probe.assert_not_called()
            process.assert_not_called()

    def test_uploaded_legacy_status_does_not_bypass_new_render(self):
        (self.series / MANIFEST).unlink()
        (self.series / "concept.md").write_text("## Upload Status\n- YouTube upload: completed\n", encoding="utf-8")
        for command in ("pack", "preview"):
            result = CliRunner().invoke(cli, [command, str(self.series)] + (["-y"] if command == "pack" else []))
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("Video artwork", result.output)

    def test_compilation_never_selects_thumbnail_as_background(self):
        self.image.unlink()
        (self.series / "concept.md").write_text("## Series Type\n- **Type**: Compilation / Best Album\n", encoding="utf-8")
        self.assertIsNone(ProjectPaths(self.series).loop_image)

    def test_renderer_uses_inspected_scene_without_second_logo_overlay(self):
        with patch("wavvy.get_audio_info", return_value={"duration": 1}), patch("wavvy.subprocess.run") as run:
            run.return_value.stdout = "3840,2160"
            self.assertTrue(render_video_from_image(self.series / "mix.wav", self.image, self.thumb,
                                                   self.series / "output.mp4", logo_path=self.image))
            command = run.call_args.args[0]
            inputs = [command[i + 1] for i, token in enumerate(command) if token == "-i"]
            self.assertEqual(inputs, [str(self.image), str(self.series / "mix.wav")])
            self.assertNotIn("-filter_complex", command)

    def test_upload_gate_rejects_changed_artwork_even_with_mocked_validation(self):
        self.manifest["visual_review"]["sha256"] = "0" * 64
        self.save()
        result = run_gate(self.series, self.root, "upload-ready", {"is_valid": True})
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("Video artwork" in error for error in result["blockers"]))

    def test_existing_video_loop_route_is_not_changed(self):
        (self.series / MANIFEST).unlink()
        (self.series / "input/loop.mp4").write_bytes(b"loop")
        self.assertFalse(ProjectPaths(self.series).is_image_mode)
        with patch("wavvy.interactive_pack_plan", return_value=None) as plan:
            result = CliRunner().invoke(cli, ["pack", str(self.series)])
            self.assertEqual(result.exit_code, 0, result.output)
            plan.assert_called_once()
