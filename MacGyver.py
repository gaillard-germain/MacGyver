#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import pygame

"""Fonction qui génére une liste de coordonnées à partir d'un fichier .txt,
celle-ci me sert a afficher le plateau de jeux avec pygame"""
def dedale_gen():
    dedale = []
    with open('resources/structure.txt', 'r') as data:
        for y_index,line in enumerate(data):
            line = line.strip('\n')
            for x_index,char in enumerate(line):
                if char != ' ':
                    dedale.append((x_index*32,y_index*32))
    return dedale

"""Mon application"""
class App(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        screen = pygame.display.set_mode((480, 480))
        dedale = dedale_gen()
        wall_image = pygame.image.load('resources/wall.png')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for coord in dedale:
                screen.blit(wall_image, coord)
            pygame.display.update()

        return 0

if __name__ == '__main__':
    App().main()
