#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# actor.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

class Actor:
    """Macgiver object his coordinates, his possessions... he can move"""
    def __init__(self, start):
        self.coord = start
        self.backpack = 0
        self.status = 'alive'
        self.drug = False

    def move(self, vector_x, vector_y, board):
        """move mac to the next square"""
        x, y = self.coord
        next_step = (x + vector_x, y + vector_y)
        if next_step in board.corridors:
            self.coord = next_step
            if next_step in board.components:
                del board.components[next_step]
                self.backpack += 1
        elif next_step == board.guard:
            if self.backpack < 3:
                self.status = 'dead'
            else:
                self.coord = next_step
                self.drug = True
        elif next_step == board.end:
            self.coord = next_step
            self.status = 'escaped'
