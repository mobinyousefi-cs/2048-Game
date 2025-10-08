#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=
Project: 2048 Game (Tkinter)
File: 2048_game.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-08
Updated: 2025-10-08
License: MIT License (see LICENSE file for details)
=
Single-file implementation with UI included — ready to run.
"""

from __future__ import annotations

import json
import os
import random
import tkinter as tk
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


# Configuration & Constants
GRID_SIZE = 4
START_TILES = 2
WINDOW_TITLE = "2048 - Tkinter Edition"
CELL_SIZE = 110
CELL_PADDING = 10
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
FONT = ("Helvetica", 24, "bold")
HIGHSCORE_FILE = Path.home() / ".2048_highscore.json"

TILE_COLORS = {
    0: EMPTY_CELL_COLOR,
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

# ---------------------------
# Helper functions
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


# ---------------------------
# Game logic (testable)
@dataclass
class Game:
    size: int = GRID_SIZE
    grid: List[List[int]] = field(default_factory=list)
    score: int = 0

    def __post_init__(self):
        if not self.grid:
            self.grid = [[0] * self.size for _ in range(self.size)]
            for _ in range(START_TILES):
                self.spawn_random()

    def reset(self):
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

    def _compress_line(self, line: List[int]) -> Tuple[List[int], int]:
        new = [v for v in line if v != 0]
        new += [0] * (len(line) - len(new))
        return new, 0

    def _merge_line(self, line: List[int]) -> Tuple[List[int], int]:
        gained = 0
        compressed, _ = self._compress_line(line)
        for i in range(len(compressed) - 1):
            if compressed[i] != 0 and compressed[i] == compressed[i + 1]:
                compressed[i] *= 2
                compressed[i + 1] = 0
                gained += compressed[i]
        final, _ = self._compress_line(compressed)
        return final, gained

    def move_left(self) -> bool:
        moved = False
        total_gained = 0
        for r in range(self.size):
            new_line, gained = self._merge_line(self.grid[r])
            if new_line != self.grid[r]:
                moved = True
                self.grid[r] = new_line
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


# ---------------------------
# UI Layer
class GameUI(tk.Frame):
    def __init__(self, master: tk.Tk, game: Game):
        super().__init__(master)
        self.master = master
        self.game = game
        self.highscore = load_highscore()
        self.master.title(WINDOW_TITLE)
        self.master.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)

        width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING
        height = width + 80  # extra for score
        self.canvas = tk.Canvas(master, width=width, height=height, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack()

        self._draw_static_board()
        self._bind_keys()
        self.update_ui()

    def _draw_static_board(self):
        # Title and score area
        self.canvas.create_text(20, 20, anchor="w", text="2048", font=("Helvetica", 28, "bold"), fill="#776e65")
        self.score_text = self.canvas.create_text(20, 52, anchor="w", text=f"Score: {self.game.score}", font=("Helvetica", 14), fill="#f9f6f2")
        self.highscore_text = self.canvas.create_text(200, 52, anchor="w", text=f"Highscore: {self.highscore}", font=("Helvetica", 14), fill="#f9f6f2")

        # Board background
        board_x0 = CELL_PADDING
        board_y0 = 80
        board_x1 = board_x0 + GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING
        board_y1 = board_y0 + GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING
        # draw rounded rectangle-like background
        self.canvas.create_rectangle(board_x0 - CELL_PADDING // 2, board_y0 - CELL_PADDING // 2, board_x1 + CELL_PADDING // 2, board_y1 + CELL_PADDING // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)

        # create cell rects placeholders
        self.cell_items = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.cell_texts = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = board_x0 + c * (CELL_SIZE + CELL_PADDING)
                y = board_y0 + r * (CELL_SIZE + CELL_PADDING)
                rect = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=EMPTY_CELL_COLOR, outline=EMPTY_CELL_COLOR, width=0)
                text = self.canvas.create_text(x + CELL_SIZE / 2, y + CELL_SIZE / 2, text="", font=FONT)
                self.cell_items[r][c] = rect
                self.cell_texts[r][c] = text

        # Add small instructions
        self.canvas.create_text(20, height - 24, anchor="w", text="Use ← ↑ ↓ → or A W S D to play. R to restart. Esc to quit.", font=("Helvetica", 10), fill="#f9f6f2")

    def _bind_keys(self):
        self.master.bind("<Left>", lambda e: self._key_move(self.game.move_left))
        self.master.bind("<Right>", lambda e: self._key_move(self.game.move_right))
        self.master.bind("<Up>", lambda e: self._key_move(self.game.move_up))
        self.master.bind("<Down>", lambda e: self._key_move(self.game.move_down))
        # WASD
        self.master.bind("a", lambda e: self._key_move(self.game.move_left))
        self.master.bind("d", lambda e: self._key_move(self.game.move_right))
        self.master.bind("w", lambda e: self._key_move(self.game.move_up))
        self.master.bind("s", lambda e: self._key_move(self.game.move_down))
        self.master.bind("r", lambda e: self.restart())
        self.master.bind("<Escape>", lambda e: self.master.quit())

    def _key_move(self, move_fn):
        moved = move_fn()
        if moved:
            self.update_ui()
            if self.game.score > self.highscore:
                self.highscore = self.game.score
                save_highscore(self.highscore)
            if self.game.is_win():
                self._show_message("You Win!", "Congratulations — you reached 2048! Press R to play again.")
            elif not self.game.can_move():
                self._show_message("Game Over", f"No moves left. Final score: {self.game.score}. Press R to restart.")

    def restart(self):
        self.game.reset()
        self.update_ui()

    def update_ui(self):
        # update score and board
        self.canvas.itemconfigure(self.score_text, text=f"Score: {self.game.score}")
        self.canvas.itemconfigure(self.highscore_text, text=f"Highscore: {self.highscore}")
        board_x0 = CELL_PADDING
        board_y0 = 80
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = board_x0 + c * (CELL_SIZE + CELL_PADDING)
                y = board_y0 + r * (CELL_SIZE + CELL_PADDING)
                val = self.game.grid[r][c]
                color = TILE_COLORS.get(val, TILE_COLORS[max(k for k in TILE_COLORS.keys() if isinstance(k, int))])
                # update rect
                self.canvas.itemconfigure(self.cell_items[r][c], fill=color, outline=color)
                # update text
                if val == 0:
                    self.canvas.itemconfigure(self.cell_texts[r][c], text="")
                else:
                    display_text = str(val)
                    # adjust font size for large numbers
                    size = 24 if val < 1024 else 18
                    self.canvas.itemconfigure(self.cell_texts[r][c], text=display_text, font=("Helvetica", size, "bold"))

    def _show_message(self, title: str, message: str) -> None:
        # Modal-like message using a toplevel
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.transient(self.master)
        popup.grab_set()
        label = tk.Label(popup, text=message, padx=20, pady=10)
        label.pack()
        button = tk.Button(popup, text="OK", command=popup.destroy, width=12)
        button.pack(pady=(0, 10))
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)
        # center the popup
        popup.update_idletasks()
        w = popup.winfo_width()
        h = popup.winfo_height()
        x = self.master.winfo_x() + (self.master.winfo_width() - w) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")


# ---------------------------
# Entry point
def main():
    random.seed()
    root = tk.Tk()
    game = Game()
    ui = GameUI(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()
