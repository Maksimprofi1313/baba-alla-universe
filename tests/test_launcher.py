"""Тесты для игрового лаунчера Baba Alla Universe."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from games import launcher


class DiscoverGamesTests(unittest.TestCase):
    def test_discovers_python_games_in_case_insensitive_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("zeta.py", "Артондо.py", "Alpha.py", "launcher.py", "notes.txt"):
                (root / name).write_text("# test\n", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "hidden.py").write_text("# test\n", encoding="utf-8")

            with patch.object(launcher, "GAMES_DIR", root):
                games = launcher.discover_games()

        self.assertEqual(
            [path.name for path in games],
            ["Alpha.py", "zeta.py", "Артондо.py"],
        )

    def test_returns_empty_list_when_folder_has_no_games(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(launcher, "GAMES_DIR", Path(directory)):
                self.assertEqual(launcher.discover_games(), [])


if __name__ == "__main__":
    unittest.main()
