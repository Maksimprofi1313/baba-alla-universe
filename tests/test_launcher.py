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


class TaskManagerStorageTests(unittest.TestCase):
    def test_corrupt_json_is_preserved_and_saving_is_blocked(self):
        import json
        from utilities import task_manager

        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory) / "tasks.json"
            original = "{ this is not valid JSON"
            storage.write_text(original, encoding="utf-8")

            with patch.object(task_manager, "TASKS_FILE", str(storage)):
                manager = task_manager.TaskManager()
                self.assertEqual(manager.tasks, [])
                self.assertIsNotNone(manager.load_error)
                with patch.object(task_manager.messagebox, "showerror"):
                    self.assertFalse(manager.save_tasks())

            self.assertEqual(storage.read_text(encoding="utf-8"), original)

    def test_valid_json_tasks_are_loaded(self):
        from utilities import task_manager

        expected = [{"id": "1", "title": "Проверка", "status": "todo"}]
        with tempfile.TemporaryDirectory() as directory:
            storage = Path(directory) / "tasks.json"
            storage.write_text(
                __import__("json").dumps(expected, ensure_ascii=False),
                encoding="utf-8",
            )
            with patch.object(task_manager, "TASKS_FILE", str(storage)):
                manager = task_manager.TaskManager()

        self.assertEqual(manager.tasks, expected)
        self.assertIsNone(manager.load_error)


if __name__ == "__main__":
    unittest.main()
