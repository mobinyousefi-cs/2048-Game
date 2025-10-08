#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=
Project: 2048 Game (Tkinter)
File: test_game_logic.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-08
Updated: 2025-10-08
License: MIT License (see LICENSE file for details)
=
Pytest unit tests for the game logic (src.game.Game).
"""

import copy
import pytest
from src.game import Game


def test_spawn_and_reset():
    g = Game()
    # after initialization there should be some non-zero tiles
    assert any(v != 0 for row in g.grid for v in row)
    g.reset()
    assert g.score == 0
    assert any(v != 0 for row in g.grid for v in row)


def test_move_left_simple_merge():
    g = Game()
    g.grid = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    moved = g.move_left()
    assert moved
    assert g.grid[0][0] == 4


def test_no_move_when_locked():
    g = Game()
    g.grid = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert not g.can_move()
