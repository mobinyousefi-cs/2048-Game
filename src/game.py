#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=
Project: 2048 Game (Tkinter)
File: game.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-08
Updated: 2025-10-08
License: MIT License (see LICENSE file for details)
=
Testable game logic for 2048. Keep UI and logic separate to simplify testing.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

# Configuration
GRID_SIZE = 4
START_TILES = 2
HIGHSCORE_FILE = Path.home() / ".2048_highscore.json"

@dataclass
class Game:
    size: int = GRID_SIZE
    grid: List[List[int]] = field(default_factory=list)
    score: int = 0

    def __post_init__(self):
        if not self.grid:
            self.reset()

    def reset(self) -> None:
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        for _ in range(START_TILES):
            self.spawn_random()

    def spawn_random(self) -> None:
        empty = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def _compress_line(self, line: List[int]) -> List[int]:
        new = [v for v in line if v != 0]
        new += [0] * (len(line) - len(new))
        return new

    def _merge_line(self, line: List[int]) -> Tuple[List[int], int]:
        gained = 0
        compressed = self._compress_line(line)
        for i in range(len(compressed) - 1):
            if compressed[i] != 0 and compressed[i] == compressed[i + 1]:
                compressed[i] *= 2
                compressed[i + 1] = 0
                gained += compressed[i]
        final = self._compress_line(compressed)
        return final, gained

    def move_left(self) -> bool:
        moved = False
        total_gained = 0
        for r in range(self.size):
            new_line, gained = self._merge_line(self.grid[r])
            if new_line != self.grid[r]:
                self.grid[r] = new_line
                moved = True
                total_gained += gained
        if moved:
            self.score += total_gained
            self.spawn_random()
        return moved

    def move_right(self) -> bool:
        self._reverse_grid()
        moved = self.move_left()
        self._reverse_grid()
        return moved

    def move_up(self) -> bool:
        self._transpose_grid()
        moved = self.move_left()
        self._transpose_grid()
        return moved

    def move_down(self) -> bool:
        self._transpose_grid()
        moved = self.move_right()
        self._transpose_grid()
        return moved

    def _transpose_grid(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid)]

    def _reverse_grid(self) -> None:
        self.grid = [list(reversed(row)) for row in self.grid]

    def can_move(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return True
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def is_win(self, target: int = 2048) -> bool:
        return any(self.grid[r][c] >= target for r in range(self.size) for c in range(self.size))


# Highscore helpers
def load_highscore() -> int:
    try:
        if HIGHSCORE_FILE.exists():
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                return int(data.get("highscore", 0))
    except Exception:
        pass
    return 0


def save_highscore(value: int) -> None:
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as fh:
            json.dump({"highscore": value}, fh)
    except Exception:
        pass


if __name__ == "__main__":
    g = Game()
    print("2048 Game — Quick CLI Test")
    for row in g.grid:
        print(row)
    print("Score:", g.score)
    print("Import Game from src.game in your tests or UI module.")
