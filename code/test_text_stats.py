import tempfile
import unittest
from pathlib import Path

from text_stats import count_words, save_csv, tokenize


class TextStatsTest(unittest.TestCase):
    def test_tokenize_normalizes_latin_and_keeps_chinese(self):
        self.assertEqual(tokenize("Git git，科研!"), ["git", "git", "科", "研"])

    def test_count_words(self):
        self.assertEqual(count_words("AI ai Git")["ai"], 2)

    def test_save_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "counts.csv"
            save_csv([("git", 2)], output)
            self.assertIn("git,2", output.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    unittest.main()
