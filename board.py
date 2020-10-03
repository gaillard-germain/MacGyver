#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# board.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Import modules"""
from random import sample


class Board:
    """board object which regroup the coordinates of the game's elements
       (walls, start, end, guard, components...)"""
    def __init__(self, x_tile, y_tile, tile_size):
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.tile_size = tile_size
        self.walls = []
        self.corridors = []

    @property
    def width(self):
        """board's width in px"""
        return self.x_tile * self.tile_size

    @property
    def height(self):
        """board's height in px"""
        return self.y_tile * self.tile_size

    def read_map(self, map_path):
        """reads a .txt : 'w'=wall, 's'=start, 'e'=end, 'g'=guard, ' '=empty"""
        with open(map_path, 'r') as data:
            for y_index, line in enumerate(data):
                for x_index, char in enumerate(line.strip('\n')):
                    coord = ((x_index * self.tile_size,
                              y_index * self.tile_size))
                    if char == 'w':
                        self.walls.append(coord)
                    elif char == 's':
                        setattr(self, 'start', coord)
                    elif char == 'e':
                        setattr(self, 'end', coord)
                    elif char == 'g':
                        setattr(self, 'guard', coord)
                    else:
                        self.corridors.append(coord)

    def set_components(self):
        """randomly pick-up 3 coordinates in a list of available tiles
            and create a dict {coordinate : index}"""
        components = {}
        component_list = sample(self.corridors, 3)
        for index, component in enumerate(component_list):
            components[component] = index
        setattr(self, 'components', components)
