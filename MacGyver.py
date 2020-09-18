#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MacGyver.py
# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import json
from random import sample
import pygame

"""un objet plateau qui regroupe les coordonnées des différents éléments du jeu
(murs, depart, arrivée, guarde, equipements...) grace à un fichier json"""
class Board:
    def __init__(self, x_tile, y_tile, tile_size, map_path):
        self.width = x_tile * tile_size
        self.height = y_tile * tile_size
        self.walls = []
        self.corridors = []
        # ouvre fichier json
        with open(map_path) as file:
            data = json.load(file)
        # iter sur 2 boucle pour avoir ligne et colonnes soit
        # un tuple de coordonnées une fois multiplier par la largeur d'une case
        for y_index,line in enumerate(data):
            for x_index,char in enumerate(line):
                coord = ((x_index*tile_size,y_index*tile_size))
                if char == 'w':
                    self.walls.append(coord)
                else:
                    self.corridors.append(coord)
                    if char == 's':
                        setattr(self, 'start', coord)
                    elif char == 'e':
                        setattr(self, 'exit', coord)
                    elif char == 'g':
                        setattr(self, 'guard', coord)
        # recup 3 coordonnées aleatoire parmis les cases libres
        self.components = sample(self.corridors, 3)

"""Le jeu"""
class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MacGyver")

    def main(self):
        # initialise l'instance de Board(15 case large, 15 case haut,
        # case de 32px, la map en json)
        board = Board(15, 15, 32,'resources/structure.json')
        # la fenetre pygame
        screen = pygame.display.set_mode((board.width, board.height))
        # charge les images depuis le rep resources
        wall_image = pygame.image.load('resources/wall.png')
        floor_image = pygame.image.load('resources/floor.png')
        mac_image = pygame.image.load('resources/mac.png')
        guard_image = pygame.image.load('resources/guard.png')
        component_image = pygame.image.load('resources/dart.png')

        mac = mac_image.get_rect()
        mac.topleft = board.start

        while True:
            # boucle d'ecoute d'evenements pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        next_step = (mac.left, mac.top - 32)
                        if next_step in board.corridors:
                            mac.topleft = next_step
                    elif event.key == pygame.K_LEFT:
                        next_step = (mac.left - 32, mac.top)
                        if next_step in board.corridors:
                            mac.topleft = next_step
                    elif event.key == pygame.K_DOWN:
                        next_step = (mac.left, mac.top + 32)
                        if next_step in board.corridors:
                            mac.topleft = next_step
                    elif event.key == pygame.K_RIGHT:
                        next_step = (mac.left + 32, mac.top)
                        if next_step in board.corridors:
                            mac.topleft = next_step
            # affiche les images et rafraichi...
            screen.fill((50, 50, 50))
            for coord in board.walls:
                screen.blit(wall_image, coord)
            for coord in board.corridors:
                screen.blit(floor_image, coord)
            for coord in board.components:
                screen.blit(component_image, coord)
            screen.blit(guard_image, board.guard)
            screen.blit(mac_image, mac.topleft)
            pygame.display.update()

        return 1

if __name__ == '__main__':
    App().main()
