#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MacGyver.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Import modules"""
import sys
from random import sample
import pygame


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
            for y_index,line in enumerate(data):
                for x_index,char in enumerate(line.strip('\n')):
                    coord = ((x_index * self.tile_size,
                              y_index * self.tile_size))
                    if char == 'w':
                        self.walls.append(coord)
                    else:
                        self.corridors.append(coord)
                        if char == 's':
                            setattr(self, 'start', coord)
                        elif char == 'e':
                            setattr(self, 'end', coord)
                        elif char == 'g':
                            setattr(self, 'guard', coord)

    def set_components(self):
        """randomly pick-up 3 coordinates in a list of available tiles
            and create a dict {coordinate : index}"""
        components = {}
        component_list = sample(list(self.available()), 3)
        for index, component in enumerate(component_list):
            components[component] = index
        setattr(self, 'components', components)



    def available(self):
        """yields free coordinate"""
        for coord in self.corridors:
            if coord!=self.start and coord!=self.end and coord!=self.guard:
                yield coord

class Macgyver:
    """Macgiver object his coordinates, his possessions... he can move"""
    def __init__(self, start):
        self.coord = start
        self.backpack = 0

    def move(self, vector_x, vector_y, board):
        """move Macgyver to the next square"""
        x, y = self.coord
        next_step = (x + vector_x, y + vector_y)
        if next_step in board.corridors:
            if next_step in board.components:
                del board.components[next_step]
                self.backpack += 1
                self.coord = next_step
            elif next_step == board.guard:
                if self.backpack < 3:
                    return 'lose'
                else:
                    self.coord = next_step
            elif next_step == board.end:
                self.coord = next_step
                return 'win'
            else:
                self.coord = next_step
            return 'running'
        else:
            return 'running'

def display_txt(txt, size, color, surface, x = 'center', y = 'center'):
    """display the text in a middle of a surface with pygame
       (just to make my life easier!)"""
    txt = str(txt)
    font = pygame.font.Font('resources/stocky.ttf', size)
    img_txt = font.render(txt, True, color)
    if x == 'center':
        x = int((surface.get_width() - font.size(txt)[0])/2)
    if y == 'center':
        y = int((surface.get_height() - font.size(txt)[1])/2)
    return surface.blit(img_txt, (x, y))

class App:
    """the game in pygame"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        """main function"""
        board = Board(15, 15, 32)
        board.read_map('resources/structure.txt')
        board.set_components()
        macgyver = Macgyver(board.start)

        screen = pygame.display.set_mode((board.width, board.height))

        wall_image = pygame.image.load('resources/wall.png')
        floor_image = pygame.image.load('resources/floor.png')
        door_image = pygame.image.load('resources/trapdoor.png')
        guard_image = pygame.image.load('resources/guard.png')
        components_image = [pygame.image.load('resources/niddle.png'),
                            pygame.image.load('resources/tube.png'),
                            pygame.image.load('resources/ether.png')]
        mac_image = pygame.image.load('resources/mac.png')
        splash_image = pygame.image.load('resources/splash.png')

        game_status = 'running'

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if game_status == 'running':
                        if event.key == pygame.K_UP:
                            game_status = macgyver.move(0, -32, board)
                        elif event.key == pygame.K_LEFT:
                            game_status = macgyver.move(-32, 0, board)
                        elif event.key == pygame.K_DOWN:
                            game_status = macgyver.move(0, +32, board)
                        elif event.key == pygame.K_RIGHT:
                            game_status = macgyver.move(+32, 0, board)
                    else:
                        if event.key == pygame.K_RETURN:
                            return self.main()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            for coord in board.walls:
                screen.blit(wall_image, coord)
            for coord in board.corridors:
                screen.blit(floor_image, coord)
            screen.blit(door_image, board.start)
            screen.blit(door_image, board.end)
            for key, value in board.components.items():
                screen.blit(components_image[value], key)
            screen.blit(guard_image, board.guard)
            screen.blit(mac_image, macgyver.coord)

            if game_status != 'running':
                if game_status == 'lose':
                    mac_image = splash_image
                    display_txt('YOU LOSE', 40, (180, 60, 20), screen,
                                'center', 100)
                elif game_status == 'win':
                    display_txt('YOU WIN', 40, (20, 60, 180), screen,
                                'center', 100)
                display_txt('Press RETURN to Replay', 14, (25, 25, 25), screen,
                            'center', 170)
                display_txt('Press ESCAPE to Quit', 14, (25, 25, 25), screen,
                            'center', 200)

            pygame.display.update()

        return 1

if __name__ == '__main__':
    App().main()
