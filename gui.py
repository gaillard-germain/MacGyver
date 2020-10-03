#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# gui.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Import modules"""
import pygame


class Gui:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))

        self.wall_image = pygame.image.load('resources/wall.png')
        self.floor_image = pygame.image.load('resources/floor.png')
        self.stairs_image = pygame.image.load('resources/stairs.png')
        self.guard_image = pygame.image.load('resources/guard.png')
        self.components_image = [pygame.image.load('resources/needle.png'),
                                 pygame.image.load('resources/tube.png'),
                                 pygame.image.load('resources/ether.png')]
        self.mac_image = pygame.image.load('resources/mac.png')
        self.grave_image = pygame.image.load('resources/grave.png')
        self.zzz_image = pygame.image.load('resources/zzz.png')

    def draw(self, mac, board):
        for coord in board.walls:
            self.screen.blit(self.wall_image, coord)
        for coord in board.corridors:
            self.screen.blit(self.floor_image, coord)
        self.screen.blit(self.floor_image, board.start)
        self.screen.blit(self.stairs_image, board.start)
        self.screen.blit(self.floor_image, board.end)
        self.screen.blit(self.stairs_image, board.end)
        for key, value in board.components.items():
            self.screen.blit(self.components_image[value], key)
        self.screen.blit(self.floor_image, board.guard)
        if mac.drug:
            self.screen.blit(self.zzz_image, board.guard)
        else:
            self.screen.blit(self.guard_image, board.guard)
        if mac.status != 'alive':
            if mac.status == 'dead':
                self.screen.blit(self.grave_image, mac.coord)
                self.display_txt('YOU LOSE', 64, (180, 60, 20), self.screen,
                                 'center', 120)
            elif mac.status == 'escaped':
                self.screen.blit(self.mac_image, mac.coord)
                self.display_txt('YOU WIN', 64, (20, 60, 180), self.screen,
                                 'center', 120)
            self.display_txt('Press RETURN to Replay', 24, (25, 25, 25),
                             self.screen, 'center', 200)
            self.display_txt('Press ESCAPE to Quit', 24, (25, 25, 25),
                             self.screen, 'center', 240)
        else:
            self.screen.blit(self.mac_image, mac.coord)

    def display_txt(self, txt, size, color, surface, x='center', y='center'):
        """display the text in a middle of a surface with pygame
           (just to make my life easier!)"""
        txt = str(txt)
        font = pygame.font.Font('resources/baxoe.ttf', size)
        img_txt = font.render(txt, True, color)
        if x == 'center':
            x = int((surface.get_width() - font.size(txt)[0])/2)
        if y == 'center':
            y = int((surface.get_height() - font.size(txt)[1])/2)
        return surface.blit(img_txt, (x, y))
