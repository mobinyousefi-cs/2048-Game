#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=
Project: 2048 Game (Tkinter)
File: ui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-08
Updated: 2025-10-08
License: MIT License (see LICENSE file for details)
=
Tkinter UI for the 2048 Game. Uses the Game class from src.game for logic.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from src.game import Game, load_highscore, save_highscore

GRID_SIZE = 4
CELL_SIZE = 110
CELL_PADDING = 10
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
FONT = ("Helvetica", 24, "bold")

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

class GameUI(tk.Frame):
    def __init__(self, master: tk.Tk, game: Game):
        super().__init__(master)
        self.master = master
        self.game = game
        self.highscore = load_highscore()
        self.master.title("2048 - Tkinter Edition")
        self.master.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)

        width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING
        height = width + 80
        self.canvas = tk.Canvas(master, width=width, height=height, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack()

        self._draw_static_board()
        self._bind_keys()
        self.update_ui()

    def _draw_static_board(self):
        self.canvas.create_text(20, 20, anchor="w", text="2048", font=("Helvetica", 28, "bold"), fill="#776e65")
        self.score_text = self.canvas.create_text(20, 52, anchor="w", text=f"Score: {self.game.score}", font=("Helvetica", 14), fill="#f9f6f2")
        self.highscore_text = self.canvas.create_text(200, 52, anchor="w", text=f"Highscore: {self.highscore}", font=("Helvetica", 14), fill="#f9f6f2")

        board_x0 = CELL_PADDING
        board_y0 = 80
        board_x1 = board_x0 + GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING
        board_y1 = board_y0 + GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_PADDING
        self.canvas.create_rectangle(board_x0 - CELL_PADDING // 2, board_y0 - CELL_PADDING // 2, board_x1 + CELL_PADDING // 2, board_y1 + CELL_PADDING // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)

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

        self.canvas.create_text(20, height - 24, anchor="w", text="Use ← ↑ ↓ → or A W S D to play. R to restart. Esc to quit.", font=("Helvetica", 10), fill="#f9f6f2")

    def _bind_keys(self):
        self.master.bind("<Left>", lambda e: self._key_move(self.game.move_left))
        self.master.bind("<Right>", lambda e: self._key_move(self.game.move_right))
        self.master.bind("<Up>", lambda e: self._key_move(self.game.move_up))
        self.master.bind("<Down>", lambda e: self._key_move(self.game.move_down))
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
                self.canvas.itemconfigure(self.cell_items[r][c], fill=color, outline=color)
                if val == 0:
                    self.canvas.itemconfigure(self.cell_texts[r][c], text="")
                else:
                    display_text = str(val)
                    size = 24 if val < 1024 else 18
                    self.canvas.itemconfigure(self.cell_texts[r][c], text=display_text, font=("Helvetica", size, "bold"))

    def _show_message(self, title: str, message: str) -> None:
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.transient(self.master)
        popup.grab_set()
        label = tk.Label(popup, text=message, padx=20, pady=10)
        label.pack()
        button = tk.Button(popup, text="OK", command=popup.destroy, width=12)
        button.pack(pady=(0, 10))
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)
        popup.update_idletasks()
        w = popup.winfo_width()
        h = popup.winfo_height()
        x = self.master.winfo_x() + (self.master.winfo_width() - w) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")


def main():
    root = tk.Tk()
    game = Game()
    ui = GameUI(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()
