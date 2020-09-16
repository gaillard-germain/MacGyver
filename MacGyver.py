#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import pygame

class Macgyver(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        screen = pygame.display.set_mode((480, 480))

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

        return 1

if __name__ == '__main__':
    Macgyver().main()
