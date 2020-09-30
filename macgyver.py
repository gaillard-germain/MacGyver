#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# macgyver.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Import modules"""
import sys
import pygame
from actor import Actor
from board import Board

class Macgyver:
    """the game in pygame"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("mac")

    def main(self):
        """main function"""
        board = Board(15, 15, 32)
        board.read_map('resources/structure.txt')
        board.set_components()
        mac = Actor(board.start)

        screen = pygame.display.set_mode((board.width, board.height))

        wall_image = pygame.image.load('resources/wall.png')
        floor_image = pygame.image.load('resources/floor.png')
        stairs_image = pygame.image.load('resources/stairs.png')
        guard_image = pygame.image.load('resources/guard.png')
        components_image = [pygame.image.load('resources/needle.png'),
                            pygame.image.load('resources/tube.png'),
                            pygame.image.load('resources/ether.png')]
        mac_image = pygame.image.load('resources/mac.png')
        grave_image = pygame.image.load('resources/grave.png')
        zzz_image = pygame.image.load('resources/zzz.png')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if mac.status == 'alive':
                        if event.key == pygame.K_UP:
                            mac.move(0, -32, board)
                        elif event.key == pygame.K_LEFT:
                            mac.move(-32, 0, board)
                        elif event.key == pygame.K_DOWN:
                            mac.move(0, +32, board)
                        elif event.key == pygame.K_RIGHT:
                            mac.move(+32, 0, board)
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
            screen.blit(floor_image, board.start)
            screen.blit(stairs_image, board.start)
            screen.blit(floor_image, board.end)
            screen.blit(stairs_image, board.end)
            for key, value in board.components.items():
                screen.blit(components_image[value], key)
            screen.blit(floor_image, board.guard)
            if mac.drug:
                screen.blit(zzz_image, board.guard)
            else:
                screen.blit(guard_image, board.guard)
            if mac.status != 'alive':
                if mac.status == 'dead':
                    screen.blit(grave_image, mac.coord)
                    self.display_txt('YOU LOSE', 64, (180, 60, 20), screen,
                                'center', 120)
                elif mac.status == 'escaped':
                    screen.blit(mac_image, mac.coord)
                    self.display_txt('YOU WIN', 64, (20, 60, 180), screen,
                                'center', 120)
                self.display_txt('Press RETURN to Replay', 24, (25, 25, 25),
                                 screen, 'center', 200)
                self.display_txt('Press ESCAPE to Quit', 24, (25, 25, 25),
                                 screen, 'center', 240)
            else:
                screen.blit(mac_image, mac.coord)

            pygame.display.update()

        return 1

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

if __name__ == '__main__':
    Macgyver().main()
