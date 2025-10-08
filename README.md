# =

Project: 2048 Game (Tkinter)
File: README.md
Author: Mobin Yousefi (GitHub: [https://github.com/mobinyousefi-cs](https://github.com/mobinyousefi-cs))
Created: 2025-10-02
Updated: 2025-10-02
License: MIT License (see LICENSE file for details)
===================================================

# 2048 — Tkinter Edition

A compact, well-structured implementation of the 2048 puzzle game in Python using Tkinter for the UI.

## Structure

```
my_2048_project/
├── src/
│   ├── __init__.py
│   ├── game.py
│   └── ui.py
├── tests/
│   └── test_game_logic.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Running

* Run the UI: `python -m src.ui` or `python src/ui.py`.
* Run tests: `pytest`

## Notes

* The game logic is contained in `src/game.py` which is easy to unit test.
* Highscore is stored in `~/.2048_highscore.json`.
* If you want a single-file runnable version, use `2048_game.py`.
