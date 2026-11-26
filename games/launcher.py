"""Единое меню запуска игр Baba Alla Universe.

Запуск из корня репозитория:
    python games/launcher.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

GAMES_DIR = Path(__file__).resolve().parent
LAUNCHER_NAME = Path(__file__).name


def discover_games() -> list[Path]:
    """Находит Python-игры в этой папке, кроме самого лаунчера."""
    return sorted(
        (
            path
            for path in GAMES_DIR.glob("*.py")
            if path.name != LAUNCHER_NAME
        ),
        key=lambda path: path.name.casefold(),
    )


def main() -> int:
    while True:
        games = discover_games()
        print("\n" + "=" * 54)
        print("          BABA ALLA UNIVERSE — ИГРОВОЕ МЕНЮ")
        print("=" * 54)

        if not games:
            print("В папке games пока нет игр.")
            return 0

        for index, game in enumerate(games, start=1):
            print(f"{index:>2}. {game.stem}")

        print("\n  0. Выход")
        choice = input("\nВыбери игру: ").strip()

        if choice == "0":
            print("Баба Алла отпускает тебя... пока что.")
            return 0

        if not choice.isdigit() or not 1 <= int(choice) <= len(games):
            print("Такого пункта нет. Попробуй ещё раз.")
            continue

        selected = games[int(choice) - 1]
        print(f"\nЗапускаю: {selected.stem}\n")
        try:
            result = subprocess.run([sys.executable, str(selected)], check=False)
            if result.returncode:
                print(f"Игра завершилась с кодом {result.returncode}.")
        except OSError as error:
            print(f"Не удалось запустить игру: {error}")

        input("\nНажми Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из Baba Alla Universe.")
        raise SystemExit(0)
