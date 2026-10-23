import unittest

from wavvy_harness.youtube_titles import validate_youtube_title


class YouTubeTitleTests(unittest.TestCase):
    def test_existing_titles_and_documented_compilation_form_pass(self):
        titles = (
            ("17-30", "Playlist | 오렌지 한 입처럼 산뜻한 그루브 🍊 | MODERN R&B · NEO SOUL | 카페 · 산책 · 작업 · 드라이브 · 노동요 | Wavvy | 17:30"),
            ("07-00", "Playlist | 상쾌하게 달릴 준비 됐나요?! 🏃 | 180 BPM Running Mix · 2Hour | Wavvy | 07:00"),
            ("RNB-BEST", "Playlist | R&B Best | 와..이 노래 제목 뭐야? ✨ 틀자마자 리듬에 그루비 😎 | CHILL · R&B · SOUL | 카페 · 작업 · 매장 음악 | Wavvy"),
            ("RNB-BEST", "Playlist | 들을수록 좋은 R&B ✨ | R&B · SOUL | 카페 · 작업 | Wavvy | R&B Best"),
        )
        for series, title in titles:
            with self.subTest(series=series):
                self.assertEqual(validate_youtube_title(title, series), [])

    def test_wrong_slot_and_missing_brand_fail(self):
        title = "Playlist | 산뜻한 그루브 🍊 | MODERN R&B · NEO SOUL | 카페 · 작업 | Wavvy | 17:00"
        errors = validate_youtube_title(title, "17-30")
        self.assertIn("YouTube title must end with series time 17:30", errors)
        self.assertTrue(validate_youtube_title(title.replace("Wavvy", "Other"), "17-00"))

    def test_empty_section_and_too_long_fail(self):
        title = "Playlist |  | MODERN R&B | 카페 | Wavvy | 17:30"
        self.assertIn("YouTube title has an empty section", validate_youtube_title(title, "17-30"))
        self.assertTrue(any("exceeds 100" in error for error in validate_youtube_title(title + "x" * 100, "17-30")))


if __name__ == "__main__":
    unittest.main()
