#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# macgyver.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Import modules"""
import sys
import pygame
from gui import Gui
from board import Board
from actor import Actor


class Macgyver:
    """the game in pygame"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        """main function"""
        board = Board(15, 15, 32)
        board.read_map('resources/structure.txt')
        board.set_components()
        mac = Actor(board.start)
        gui = Gui(board.width, board.height)

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

            gui.draw(mac, board)
            pygame.display.update()

        return 1


if __name__ == '__main__':
    Macgyver().main()
